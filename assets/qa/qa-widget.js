/* =============================================================
 * 硬见 · 站内文档答疑（云端优先 + 本地兜底 · 服务端 RAG 版）
 *
 * 运行原理：
 *   1. 打开面板时优先请求「云端后端」/api/kb/search（腾讯轻量云），
 *      由服务端做 BM25 检索；若配置了免费 LLM key，则升级为生成式 RAG。
 *   2. 云端不可用（网络 / 混合内容 / CORS）时，自动降级为浏览器内
 *      分词 + 倒排索引 + BM25 检索（原纯前端方案），保证离线也能用。
 *   3. 答案即站内文章原文片段摘录，或 LLM 基于片段生成的回答 + 出处。
 *
 * 安全边界：纯新增文件，不修改博客任何既有 JS / JSON / 样式。
 * 前端零强依赖后端：后端下线也不影响博客与答疑功能（走本地兜底）。
 * ============================================================= */
(function () {
  'use strict';

  /* ---------------- 配置 ---------------- */
  // 以本脚本自身位置定位 corpus.json，避免相对路径受页面层级影响
  var SELF_SRC = (document.currentScript && document.currentScript.src) || location.href;
  var CORPUS_URL = new URL('corpus.json', SELF_SRC).href;
  var TOP_K = 3;          // 返回的相关片段数
  var SNIPPET_LEN = 300;  // 主答案片段长度
  var WEAK_SCORE = 2.0;   // 低于此分视为"没找到明确答案"
  var BM25 = { k1: 1.5, b: 0.75 };

  // 云端后端候选地址（按顺序尝试，命中即返回，全部失败则降级浏览器本地 BM25）
  //
  // 2026-10-04 定版：域名 hadrwarewatch.icu 因服务器不支持 ICP 备案，
  // 标准 443 端口会被腾讯云网络层拦截，因此后端 HTTPS 走 **8443 非标准端口**
  // （nginx 侧 TLS 终结，回源 backend:5000 走 Docker 内网 HTTP）。
  // 浏览器混合内容规则只校验协议（https）不看端口，故 :8443 可被 HTTPS 博客正常调用。
  // 后续若完成备案，把首项改回 https://hadrwarewatch.icu 即可，无需再动代码逻辑。
  var USE_BACKEND = true;
  var API_CANDIDATES = [
    'https://hadrwarewatch.icu:8443',   // 主用：已备案前唯一可用通道（非标准端口 TLS）
    'https://api.hardwarewatch.de5.net', // 备用：de5.net 主人开启托管证书后自动生效
    'https://hadrwarewatch.icu',        // 备用：备案通过后切回标准 443
    'http://101.42.4.134'               // 兜底：仅本地 HTTP 预览环境可用（HTTPS 页会被混合内容拦）
  ];

  /* ---------------- 超时分级 + 云端熔断器（2026-10-04 P0） ----------------
   * 背景（实测）：后端关机时，4 个候选「流式 9s×4 → 一次性 8s×4」串行硬等，
   *   用户要 30~54s 才看到答案；且每条提问都重走一遍，等于降级功能白做。
   * 三处优化：
   *   1. 超时分级：主用 6s，备用 3.5s（原来是 9s/8s 一刀切）。
   *   2. 网络级失败（超时 / Failed to fetch）直接跳本地，不再重复走一次性接口——
   *      既然 TCP 连不上，流式与一次性必然同结果。
   *   3. 熔断器：确认云端不可达后记忆状态，期间提问直接本地（零等待）；
   *      冷却期结束自动后台探活，恢复后无感回到云端。
   */
  var TMO = { primary: 6000, backup: 3500, probe: 3000, budget: 9000, budgetSearch: 7000 };
  var CB = {
    KEY: 'hw_cb_v1',
    FAILS_TO_TRIP: 1,       // 整条候选链走完仍失败即跳闸（已经试过所有地址了）
    OPEN_BASE_MS: 60000,    // 首次冷却 60s
    OPEN_MAX_MS: 600000,    // 冷却上限 10min（指数退避封顶）
    state: 'closed',        // closed | open | half
    fails: 0,
    openUntil: 0,
    coolMs: 60000,
    probing: false
  };
  var cloudNetFail = false; // 最近一次云端尝试是否为「网络级不可达」

  function isNetworkErr(e) {
    if (!e) return false;
    if (e.name === 'AbortError' || e.name === 'TypeError') return true;
    return /network|fetch|timeout/i.test(e.message || '');
  }

  function cbSave() {
    try {
      sessionStorage.setItem(CB.KEY, JSON.stringify({
        s: CB.state, f: CB.fails, u: CB.openUntil, c: CB.coolMs
      }));
    } catch (e) {}
  }
  function cbLoad() {
    try {
      var raw = sessionStorage.getItem(CB.KEY);
      if (!raw) return;
      var o = JSON.parse(raw);
      if (o && o.s) {
        CB.state = o.s; CB.fails = o.f || 0;
        CB.openUntil = o.u || 0; CB.coolMs = o.c || CB.OPEN_BASE_MS;
      }
    } catch (e) {}
  }
  // 跳闸：断开 + 冷却期翻倍（避免后端真宕机时频繁探测）
  function cbTrip() {
    CB.state = 'open';
    CB.openUntil = Date.now() + CB.coolMs;                  // 本次冷却用当前时长（首跳 60s）
    CB.coolMs = Math.min(CB.coolMs * 2, CB.OPEN_MAX_MS);    // 下次翻倍，封顶 10min
    CB.fails = 0;
    cbSave();
    var applied = Math.round((CB.openUntil - Date.now()) / 1000);
    console.warn('[qa-widget] 云端不可达 → 熔断 ' + applied + 's（下次冷却 '
                 + Math.round(CB.coolMs / 1000) + 's），期间直接走本地检索');
  }
  function cbReset() {
    if (CB.state !== 'closed') console.warn('[qa-widget] 云端已恢复');
    CB.state = 'closed'; CB.fails = 0; CB.openUntil = 0; CB.coolMs = CB.OPEN_BASE_MS;
    cbSave();
  }
  function cbOnFail() {
    CB.fails++;
    if (CB.state === 'half' || CB.fails >= CB.FAILS_TO_TRIP) cbTrip();
  }
  // 本次提问是否允许走云端（open 冷却中 / half 探测中 → 否）
  function cbAllowCloud() {
    if (!USE_BACKEND) return false;
    if (CB.state === 'closed') return true;
    if (CB.state === 'open' && Date.now() >= CB.openUntil) {
      CB.state = 'half'; cbSave();   // 冷却结束 → 半开，等后台探活结果
    }
    return false;
  }
  // 后台探活：只打 /api/health（不烧 token、不走 LLM），成功即闭合恢复云端
  function cbProbe() {
    if (CB.probing || !API_CANDIDATES.length) return;
    CB.probing = true;
    var ctrl = ('AbortController' in window) ? new AbortController() : null;
    var timer = setTimeout(function () { if (ctrl) ctrl.abort(); }, TMO.probe);
    var opts = { cache: 'no-store' };
    if (ctrl) opts.signal = ctrl.signal;
    fetch(API_CANDIDATES[0] + '/api/health', opts)
      .then(function (r) {
        clearTimeout(timer);
        if (!r.ok) throw new Error('HTTP ' + r.status);
        return r.json();
      })
      .then(function (d) {
        if (d && (d.ok === true || d.status === 'ok' || d.kb)) cbReset();
        else throw new Error('unexpected payload');
      })
      .catch(function (e) {
        clearTimeout(timer);
        console.warn('[qa-widget] 探活失败(' + API_CANDIDATES[0] + ')', e && e.message);
        cbTrip();   // 探活失败 → 回到断开，冷却翻倍
      })
      .then(function () { CB.probing = false; });
  }
  // 冷却已过则后台探活（不阻塞本次回答）
  function cbMaybeProbe() {
    if (!USE_BACKEND) return;
    if (CB.state === 'open' && Date.now() >= CB.openUntil) { CB.state = 'half'; cbSave(); }
    if (CB.state === 'half') cbProbe();
  }

  /* ---------------- 中文分词 ---------------- */
  var SEG = (typeof Intl !== 'undefined' && Intl.Segmenter)
    ? new Intl.Segmenter('zh-CN', { granularity: 'word' })
    : null;

  function segCJK(run) {
    if (SEG) {
      var out = [];
      var it = SEG.segment(run);
      for (var s of it) {
        if (s.isWordLike && s.segment) out.push(s.segment);
      }
      if (out.length) return out;
    }
    var bigram = [];
    for (var i = 0; i < run.length - 1; i++) bigram.push(run.slice(i, i + 2));
    if (run.length === 1) bigram.push(run);
    return bigram;
  }

  function tokenize(text) {
    var t = (text || '').toLowerCase();
    var toks = [];
    var latin = t.match(/[a-z][a-z0-9]*/g);
    if (latin) toks = toks.concat(latin);
    var cjk = t.match(/[\u4e00-\u9fa5]+/g);
    if (cjk) cjk.forEach(function (run) { toks = toks.concat(segCJK(run)); });
    return toks;
  }

  /* ---------------- 索引与检索（本地兜底用） ---------------- */
  var corpus = null, index = null, loading = false, loadFailed = false;

  function buildIndex(chunks) {
    var df = new Map();
    var tfList = [];
    var lens = [];
    chunks.forEach(function (c) {
      var toks = tokenize(c.text + ' ' + c.article + ' ' + (c.section || ''));
      var tf = new Map();
      toks.forEach(function (t) { tf.set(t, (tf.get(t) || 0) + 1); });
      tfList.push(tf);
      lens.push(toks.length);
      tf.forEach(function (v, k) { df.set(k, (df.get(k) || 0) + 1); });
    });
    var total = lens.reduce(function (a, b) { return a + b; }, 0);
    return { df: df, tfList: tfList, lens: lens, N: chunks.length, avgdl: total / Math.max(chunks.length, 1) };
  }

  function search(query) {
    var qToks = Array.from(new Set(tokenize(query)));
    var raw = (query || '').trim().toLowerCase();
    var scores = new Array(corpus.chunks.length).fill(0);

    qToks.forEach(function (t) {
      var df = index.df.get(t);
      if (!df) return;
      var idf = Math.log(1 + (index.N - df + 0.5) / (df + 0.5));
      for (var i = 0; i < corpus.chunks.length; i++) {
        var f = index.tfList[i].get(t);
        if (!f) continue;
        var dl = index.lens[i];
        var denom = f + BM25.k1 * (1 - BM25.b + BM25.b * dl / index.avgdl);
        scores[i] += idf * (f * (BM25.k1 + 1)) / denom;
      }
    });

    corpus.chunks.forEach(function (c, i) {
      if (scores[i] <= 0) return;
      var text = c.text.toLowerCase();
      var title = (c.article || '').toLowerCase();
      if (raw && text.indexOf(raw) >= 0) scores[i] += 6;
      if (raw && title.indexOf(raw) >= 0) scores[i] += 4;
      qToks.forEach(function (t) { if (title.indexOf(t) >= 0) scores[i] += 1.2; });
    });

    return scores
      .map(function (s, i) { return { score: s, chunk: corpus.chunks[i] }; })
      .filter(function (x) { return x.score > 0; })
      .sort(function (a, b) { return b.score - a.score; })
      .slice(0, TOP_K);
  }

  /* ---------------- 片段截取与高亮 ---------------- */
  function escapeHtml(s) {
    return (s || '').replace(/[&<>"']/g, function (m) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[m];
    });
  }

  function makeSnippet(text, query) {
    var lower = text.toLowerCase();
    var raw = (query || '').trim().toLowerCase();
    var pos = raw ? lower.indexOf(raw) : -1;
    if (pos < 0) {
      var toks = Array.from(new Set(tokenize(query))).sort(function (a, b) { return b.length - a.length; });
      for (var i = 0; i < toks.length; i++) {
        var p = lower.indexOf(toks[i]);
        if (p >= 0) { pos = p; break; }
      }
    }
    var start = pos > 40 ? pos - 40 : 0;
    var slice = text.slice(start, start + SNIPPET_LEN);
    if (start > 0) slice = '…' + slice;
    if (start + SNIPPET_LEN < text.length) slice = slice + '…';
    return slice;
  }

  function highlight(text, query) {
    var html = escapeHtml(text);
    var toks = Array.from(new Set(tokenize(query)))
      .filter(function (t) { return t.length >= 1; })
      .sort(function (a, b) { return b.length - a.length; });
    var raw = (query || '').trim();
    var patterns = [];
    if (raw) patterns.push(escapeHtml(raw));
    toks.forEach(function (t) { patterns.push(escapeHtml(t)); });
    patterns.forEach(function (p) {
      if (!p) return;
      var re = new RegExp(p.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'), 'gi');
      html = html.replace(re, function (m) { return '<mark>' + m + '</mark>'; });
    });
    return html;
  }

  /* ---------------- 组装本地答案（兜底用） ---------------- */
  function composeAnswer(query, hits) {
    if (!hits.length) {
      var cats = (corpus.articles || []).map(function (a) { return a.categoryName; }).filter(Boolean);
      var uniq = Array.from(new Set(cats)).slice(0, 6).join(' / ');
      return {
        html: '<div>抱歉，我在站内文章中没找到相关内容。</div>'
            + '<div class="hw-tip">可以换个说法，或试试这些方向：' + escapeHtml(uniq) + '</div>',
        weak: true, related: []
      };
    }

    var best = hits[0];
    var weak = best.score < WEAK_SCORE;
    var c = best.chunk;
    var link = c.url;
    var snippet = highlight(makeSnippet(c.text, query), query);

    var html = '';
    if (weak) html += '<div class="hw-warn">没有找到明确答案，以下是最相近的内容：</div>';
    html += '<div class="hw-atitle">' + escapeHtml(c.article) + '</div>';
    if (c.section && c.section !== c.article) {
      html += '<div class="hw-asection">' + escapeHtml(c.section) + '</div>';
    }
    html += '<div class="hw-atext">' + snippet + '</div>';
    html += '<div class="hw-alink"><a href="' + link + '" target="_blank" rel="noopener">查看原文 →</a></div>';

    var related = hits.slice(1).map(function (h) {
      return { title: h.chunk.article, section: h.chunk.section, url: h.chunk.url };
    });

    return { html: html, weak: weak, related: related };
  }

  /* ---------------- 云端后端检索（优先） ---------------- */
  // 顺序尝试多个候选地址，命中即返回；全部失败返回 null（触发本地兜底）
  function backendSearch(q) {
    if (!USE_BACKEND) return Promise.resolve(null);
    var netFail = false;
    var deadline = Date.now() + TMO.budgetSearch;
    function tryOne(i) {
      if (i >= API_CANDIDATES.length) return Promise.resolve(null);
      if (i > 0 && Date.now() + 800 >= deadline) return Promise.resolve(null);
      var base = API_CANDIDATES[i];
      var url = base + '/api/kb/search?q=' + encodeURIComponent(q) + '&top_k=' + TOP_K;
      var ctrl = ('AbortController' in window) ? new AbortController() : null;
      var timeout = (i === 0) ? TMO.primary : Math.min(TMO.backup, Math.max(1200, deadline - Date.now()));
      var timer = ctrl ? setTimeout(function () { ctrl.abort(); }, timeout) : null;
      var opts = { cache: 'no-store' };
      if (ctrl) opts.signal = ctrl.signal;
      return fetch(url, opts)
        .then(function (r) {
          if (timer) clearTimeout(timer);
          if (!r.ok) throw new Error('HTTP ' + r.status);
          return r.json();
        })
        .then(function (data) {
          if (data && data.error) return null;   // 后端明确报错（如语料不可用），降级
          return data;
        })
        .catch(function (e) {
          if (timer) clearTimeout(timer);
          if (isNetworkErr(e)) netFail = true;
          console.warn('[qa-widget] 云端不可用(' + base + ')', e && e.message);
          return tryOne(i + 1);
        });
    }
    return tryOne(0).then(function (d) { cloudNetFail = netFail; return d; });
  }

  // 把后端返回的命中片段渲染成与本地一致的结构
  function renderHits(q, hits, weakOverride) {
    if (!hits || !hits.length) {
      addBot('抱歉，我在站内文章中没找到相关内容。可以换个说法试试。');
      return;
    }
    var best = hits[0];
    var weak = (typeof weakOverride === 'boolean') ? weakOverride : (best.score < WEAK_SCORE);
    var link = best.url;
    var snippet = highlight(makeSnippet(best.text || '', q), q);

    var html = '';
    if (weak) html += '<div class="hw-warn">没有找到明确答案，以下是最相近的内容：</div>';
    html += '<div class="hw-atitle">' + escapeHtml(best.article) + '</div>';
    if (best.section && best.section !== best.article) {
      html += '<div class="hw-asection">' + escapeHtml(best.section) + '</div>';
    }
    html += '<div class="hw-atext">' + snippet + '</div>';
    html += '<div class="hw-alink"><a href="' + link + '" target="_blank" rel="noopener">查看原文 →</a></div>';
    addBot(html);
    if (!weak && hits.length > 1) {
      addRelated(hits.slice(1).map(function (h) {
        return { title: h.article, section: h.section, url: h.url };
      }));
    }
  }

  function renderBackend(q, data) {
    if (data.mode === 'rag' && data.answer) {
      sub.textContent = '云端 AI 答疑 · 已生成答案';
      var answerHtml = escapeHtml(data.answer).replace(/\n/g, '<br>');
      addBot(answerHtml);
      if (data.hits && data.hits.length) {
        addRelated(data.hits.map(function (h) {
          return { title: h.article, section: h.section, url: h.url };
        }));
      }
      return;
    }
    // retrieval 模式（或未启用 LLM）：展示后端返回的片段
    sub.textContent = '云端检索 · 已连接';
    renderHits(q, data.hits, data.weak);
  }

  /* ---------------- 流式问答（SSE，优先路径） ---------------- */
  // 同样的模型耗时下，流式把"看到第一个字"的等待从数秒压到百毫秒级。
  // 任一步失败都会退回一次性接口 /api/kb/search，再失败才降级本地 BM25。
  var USE_STREAM = true;

  function supportsStream() {
    return typeof window.ReadableStream !== 'undefined'
        && typeof window.TextDecoder !== 'undefined'
        && typeof window.AbortController !== 'undefined';
  }

  function parseSSEBlock(block) {
    var name = 'message', data = '';
    block.split(/\r?\n/).forEach(function (line) {
      if (line.indexOf('event:') === 0) name = line.slice(6).trim();
      else if (line.indexOf('data:') === 0) data += line.slice(5).trim();
    });
    if (!data) return null;
    try { return { name: name, data: JSON.parse(data) }; }
    catch (e) { return null; }
  }

  // 建一个可增量写入的气泡（流式边收边渲染）
  function addBotStream() {
    var row = document.createElement('div');
    row.className = 'hw-msg bot';
    var b = document.createElement('div');
    b.className = 'hw-bubble';
    row.appendChild(b);
    body.appendChild(row);
    scrollEnd();
    return b;
  }

  function paintBubble(bubble, text, typing) {
    bubble.innerHTML = escapeHtml(text).replace(/\n/g, '<br>')
      + (typing ? '<span class="hw-cursor"></span>' : '');
    scrollEnd();
  }

  // 返回 'ok' | 'rate_limited' | 'fail'
  function streamAsk(q) {
    var netFail = false;
    var deadline = Date.now() + TMO.budget;   // 整条链的总时间预算
    function tryOne(i) {
      if (i >= API_CANDIDATES.length) return Promise.resolve('fail');
      // 预算耗尽就不再试：剩下的候选与已失败的往往是同一台服务器，等下去只是干耗
      if (i > 0 && Date.now() + 800 >= deadline) return Promise.resolve('fail');
      var base = API_CANDIDATES[i];
      var url = base + '/api/kb/stream?q=' + encodeURIComponent(q) + '&top_k=' + TOP_K;
      var ctrl = new AbortController();
      var timeout = (i === 0) ? TMO.primary : Math.min(TMO.backup, Math.max(1200, deadline - Date.now()));
      var timer = setTimeout(function () { ctrl.abort(); }, timeout);

      var bubble = null, acc = '', meta = null, doneInfo = null, gotDelta = false, closed = false;

      function finalize() {
        if (closed) return;
        closed = true;
        clearTimeout(timer);
        if (!gotDelta) return false;          // 没有正文 → 交给降级路径渲染片段
        paintBubble(bubble, acc, false);
        if (meta && meta.hits && meta.hits.length) {
          addRelated(meta.hits.map(function (h) {
            return { title: h.article, section: h.section, url: h.url };
          }));
        }
        if (doneInfo && doneInfo.cached) sub.textContent = '云端 AI 答疑 · 缓存命中';
        else if (doneInfo && doneInfo.mode === 'rag') sub.textContent = '云端 AI 答疑 · 已生成答案';
        else sub.textContent = '云端检索 · 已连接';
        return true;
      }

      return fetch(url, {
        cache: 'no-store',
        signal: ctrl.signal,
        headers: { Accept: 'text/event-stream' }
      }).then(function (r) {
        if (r.status === 429) {
          var e = new Error('rate_limited');
          e.rateLimited = true;
          throw e;
        }
        if (!r.ok) throw new Error('HTTP ' + r.status);
        var ct = r.headers.get('Content-Type') || '';
        if (ct.indexOf('text/event-stream') === -1) throw new Error('not-sse');
        return r.body.getReader();
      }).then(function (reader) {
        var dec = new TextDecoder('utf-8');
        var buf = '';
        function pump() {
          return reader.read().then(function (chunk) {
            if (chunk.done) {
              clearTimeout(timer);
              return finalize() ? 'ok' : 'fail';
            }
            buf += dec.decode(chunk.value, { stream: true });
            var blocks = buf.split('\n\n');
            buf = blocks.pop();
            blocks.forEach(function (b) {
              var ev = parseSSEBlock(b);
              if (!ev) return;
              if (ev.name === 'meta') {
                meta = ev.data;
                if (meta.hits && meta.hits.length) {
                  sub.textContent = '云端 AI 答疑 · 参考《' + meta.hits[0].article + '》';
                }
              } else if (ev.name === 'delta') {
                if (!ev.data.text) return;
                if (!bubble) bubble = addBotStream();
                acc += ev.data.text;
                gotDelta = true;
                paintBubble(bubble, acc, true);
              } else if (ev.name === 'done') {
                doneInfo = ev.data;
              }
            });
            return pump();
          });
        }
        return pump();
      }).catch(function (e) {
        clearTimeout(timer);
        if (e && e.rateLimited) return 'rate_limited';
        if (isNetworkErr(e)) netFail = true;
        console.warn('[qa-widget] 流式不可用(' + base + ')', e && e.message);
        return tryOne(i + 1);
      });
    }
    return tryOne(0).then(function (st) {
      cloudNetFail = netFail;
      if (st !== 'fail') return st;
      return netFail ? 'fail_network' : 'fail_app';
    });
  }

  /* ---------------- 样式（复用博客主题变量，自动明暗） ---------------- */
  var css = [
    '.hw-fab{position:fixed;right:24px;bottom:24px;width:52px;height:52px;border-radius:50%;',
    ' background:var(--accent,#c9a227);color:var(--bg,#0a0a0b);border:1px solid var(--border-light,transparent);',
    ' cursor:pointer;display:grid;place-items:center;z-index:100001;',
    ' box-shadow:0 12px 32px -8px rgba(0,0,0,.45);transition:transform .2s var(--ease,ease),opacity .2s;}',
    '.hw-fab:hover{transform:scale(1.07);}',
    '.hw-fab.hw-lift{bottom:92px;}',
    '.hw-panel{position:fixed;right:24px;bottom:88px;width:382px;max-width:calc(100vw - 32px);',
    ' height:min(560px,calc(100vh - 130px));background:var(--bg-elevated,#16161a);',
    ' border:1px solid var(--border,#26262c);border-radius:16px;overflow:hidden;z-index:100002;',
    ' display:flex;flex-direction:column;color:var(--text,#ebe6da);',
    ' font-family:var(--font-sans,-apple-system,"PingFang SC","Microsoft YaHei",sans-serif);',
    ' box-shadow:var(--shadow-lg,0 30px 60px -20px rgba(0,0,0,.7));',
    ' animation:hw-in .22s var(--ease,ease);}',
    '.hw-panel.hw-lift{bottom:156px;}',
    '.hw-panel[hidden]{display:none;}',
    '@keyframes hw-in{from{opacity:0;transform:translateY(10px) scale(.98);}to{opacity:1;transform:none;}}',
    '.hw-head{display:flex;align-items:flex-start;justify-content:space-between;gap:8px;',
    ' padding:14px 16px;background:var(--surface,#1c1c21);border-bottom:1px solid var(--border,#26262c);}',
    '.hw-title{font-size:14.5px;font-weight:600;letter-spacing:.01em;}',
    '.hw-sub{font-size:11px;color:var(--text-muted,#9b9586);margin-top:3px;}',
    '.hw-close{background:transparent;border:none;color:var(--text-muted,#9b9586);cursor:pointer;',
    ' width:26px;height:26px;display:grid;place-items:center;border-radius:6px;flex:none;}',
    '.hw-close:hover{background:var(--surface-hover,#232329);color:var(--text,#ebe6da);}',
    '.hw-body{flex:1;overflow-y:auto;padding:16px;background:var(--bg-soft,#101013);}',
    '.hw-body::-webkit-scrollbar{width:6px;}',
    '.hw-body::-webkit-scrollbar-thumb{background:var(--border-light,#34343b);border-radius:3px;}',
    '.hw-msg{display:flex;margin-bottom:12px;}',
    '.hw-msg.user{justify-content:flex-end;}',
    '.hw-bubble{max-width:84%;padding:10px 13px;border-radius:14px;font-size:13.5px;line-height:1.75;word-break:break-word;}',
    '.hw-msg.bot .hw-bubble{background:var(--surface,#1c1c21);border:1px solid var(--border,#26262c);',
    ' color:var(--text,#ebe6da);border-bottom-left-radius:4px;}',
    '.hw-msg.user .hw-bubble{background:var(--accent,#c9a227);color:var(--bg,#0a0a0b);border-bottom-right-radius:4px;}',
    '.hw-bubble mark{background:var(--accent-glow,rgba(201,162,39,.35));color:inherit;padding:0 2px;border-radius:2px;}',
    '.hw-atitle{font-weight:600;margin-bottom:2px;}',
    '.hw-asection{color:var(--text-muted,#9b9586);font-size:12px;margin-bottom:8px;}',
    '.hw-atext{line-height:1.8;}',
    '.hw-alink{margin-top:10px;}',
    '.hw-alink a{color:var(--accent,#c9a227);text-decoration:none;font-size:12.5px;border-bottom:1px solid transparent;}',
    '.hw-alink a:hover{border-bottom-color:currentColor;}',
    '.hw-warn{color:var(--accent,#c9a227);font-size:12.5px;margin-bottom:6px;}',
    '.hw-cursor{display:inline-block;width:6px;height:1em;margin-left:2px;vertical-align:-2px;',
    ' background:var(--accent,#c9a227);animation:hw-blink 1s steps(2,start) infinite;}',
    '@keyframes hw-blink{to{visibility:hidden;}}',
    '.hw-tip{margin-top:6px;color:var(--text-muted,#9b9586);font-size:12.5px;}',
    '.hw-rel{margin-top:10px;padding-top:8px;border-top:1px dashed var(--border-light,#34343b);}',
    '.hw-rel-title{font-size:11px;color:var(--text-faint,#65605a);margin-bottom:5px;letter-spacing:.04em;}',
    '.hw-rel a{display:block;font-size:12.5px;color:var(--text-muted,#9b9586);text-decoration:none;margin:4px 0;',
    ' white-space:nowrap;overflow:hidden;text-overflow:ellipsis;}',
    '.hw-rel a:hover{color:var(--accent,#c9a227);}',
    '.hw-chips{display:flex;flex-wrap:wrap;gap:7px;padding:0 16px 12px;background:var(--bg-soft,#101013);',
    ' max-height:96px;overflow-y:auto;border-bottom:1px solid var(--border,#26262c);}',
    '.hw-chip{font-size:12px;padding:5px 10px;border:1px solid var(--border,#26262c);',
    ' background:var(--surface,#1c1c21);color:var(--text-muted,#9b9586);border-radius:999px;cursor:pointer;',
    ' transition:all .18s var(--ease,ease);}',
    '.hw-chip:hover{border-color:var(--accent,#c9a227);color:var(--accent,#c9a227);}',
    '.hw-foot{display:flex;gap:8px;padding:12px 16px;background:var(--bg-elevated,#16161a);}',
    '.hw-input{flex:1;min-width:0;border:1px solid var(--border-light,#34343b);background:var(--surface,#1c1c21);',
    ' color:var(--text,#ebe6da);border-radius:10px;padding:9px 12px;font-size:13.5px;outline:none;',
    ' font-family:inherit;transition:border-color .18s;}',
    '.hw-input:focus{border-color:var(--accent,#c9a227);}',
    '.hw-input::placeholder{color:var(--text-faint,#65605a);}',
    '.hw-send{border:1px solid var(--accent,#c9a227);background:var(--accent,#c9a227);color:var(--bg,#0a0a0b);',
    ' border-radius:10px;padding:0 15px;font-size:13px;font-weight:600;cursor:pointer;font-family:inherit;',
    ' transition:opacity .18s;}',
    '.hw-send:hover{opacity:.85;}',
    '@media (max-width:520px){',
    ' .hw-panel{right:12px;left:12px;width:auto;max-width:none;bottom:86px;}',
    ' .hw-panel.hw-lift{bottom:150px;}',
    ' .hw-fab{right:16px;bottom:20px;width:48px;height:48px;}',
    ' .hw-fab.hw-lift{bottom:84px;}',
    '}'
  ].join('\n');

  var styleEl = document.createElement('style');
  styleEl.id = 'hw-qa-style';
  styleEl.textContent = css;
  document.head.appendChild(styleEl);

  /* ---------------- DOM ---------------- */
  var hasBackTop = !!document.querySelector('.back-top');

  var fab = document.createElement('button');
  fab.className = 'hw-fab' + (hasBackTop ? ' hw-lift' : '');
  fab.type = 'button';
  fab.setAttribute('aria-label', '打开站内答疑助手');
  fab.innerHTML = '<svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
    + 'stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
    + '<path d="M12 3.4v2.1"/>'
    + '<circle cx="12" cy="2.4" r="1.1" fill="currentColor" stroke="none"/>'
    + '<rect x="4.2" y="5.5" width="15.6" height="12" rx="3.6"/>'
    + '<path d="M2.4 10.6v2.8M21.6 10.6v2.8"/>'
    + '<circle cx="9" cy="11" r="1.25" fill="currentColor" stroke="none"/>'
    + '<circle cx="15" cy="11" r="1.25" fill="currentColor" stroke="none"/>'
    + '<path d="M9.4 14.2a3.4 3.4 0 0 0 5.2 0"/>'
    + '</svg>';
  document.body.appendChild(fab);

  var panel = document.createElement('section');
  panel.className = 'hw-panel' + (hasBackTop ? ' hw-lift' : '');
  panel.hidden = true;
  panel.setAttribute('aria-label', '站内文档答疑');
  panel.innerHTML =
    '<div class="hw-head">' +
      '<div>' +
        '<div class="hw-title">站内文档答疑</div>' +
        '<div class="hw-sub" id="hwSub">云端检索优先 · 离线自动降级</div>' +
      '</div>' +
      '<button class="hw-close" type="button" aria-label="关闭">' +
        '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M18 6 6 18M6 6l12 12"/></svg>' +
      '</button>' +
    '</div>' +
    '<div class="hw-body" id="hwBody"></div>' +
    '<div class="hw-chips" id="hwChips"></div>' +
    '<div class="hw-foot">' +
      '<input class="hw-input" id="hwInput" type="text" placeholder="输入你的问题…" autocomplete="off">' +
      '<button class="hw-send" id="hwSend" type="button">发送</button>' +
    '</div>';
  document.body.appendChild(panel);

  var body = panel.querySelector('#hwBody');
  var input = panel.querySelector('#hwInput');
  var sendBtn = panel.querySelector('#hwSend');
  var closeBtn = panel.querySelector('.hw-close');
  var chips = panel.querySelector('#hwChips');
  var sub = panel.querySelector('#hwSub');

  /* ---------------- 数据加载（本地兜底语料，懒加载） ---------------- */
  function ensureCorpus() {
    if (corpus) return Promise.resolve(true);
    if (loading) return Promise.resolve(false);
    if (loadFailed) return Promise.resolve(false);
    loading = true;
    sub.textContent = '正在载入文章索引…';
    return fetch(CORPUS_URL + '?v=' + Date.now(), { cache: 'no-store' })
      .then(function (r) {
        if (!r.ok) throw new Error('HTTP ' + r.status);
        return r.json();
      })
      .then(function (data) {
        corpus = data;
        index = buildIndex(corpus.chunks || []);
        sub.textContent = '已索引 ' + corpus.articles.length + ' 篇文章 · ' + corpus.chunks.length + ' 个片段';
        buildChips();
        loading = false;
        return true;
      })
      .catch(function (e) {
        console.error('[qa-widget] 语料加载失败', e);
        loading = false;
        loadFailed = true;
        sub.textContent = '索引载入失败';
        return false;
      });
  }

  function buildChips() {
    chips.innerHTML = '';
    (corpus.articles || []).slice(0, 8).forEach(function (a) {
      var chip = document.createElement('button');
      chip.className = 'hw-chip';
      chip.type = 'button';
      chip.textContent = a.title.length > 12 ? a.title.slice(0, 12) + '…' : a.title;
      chip.title = a.title;
      chip.addEventListener('click', function () { handleSend(a.title); });
      chips.appendChild(chip);
    });
  }

  /* ---------------- 交互 ---------------- */
  function scrollEnd() { body.scrollTop = body.scrollHeight; }

  function addUser(text) {
    var row = document.createElement('div');
    row.className = 'hw-msg user';
    var b = document.createElement('div');
    b.className = 'hw-bubble';
    b.textContent = text;
    row.appendChild(b);
    body.appendChild(row);
    scrollEnd();
  }

  function addBot(html) {
    var row = document.createElement('div');
    row.className = 'hw-msg bot';
    var b = document.createElement('div');
    b.className = 'hw-bubble';
    b.innerHTML = html;
    row.appendChild(b);
    body.appendChild(row);
    scrollEnd();
  }

  function addRelated(related) {
    if (!related || !related.length) return;
    var html = '<div class="hw-rel"><div class="hw-rel-title">相关段落</div>';
    related.forEach(function (r) {
      var label = r.title + (r.section && r.section !== r.title ? ' · ' + r.section : '');
      html += '<a href="' + r.url + '" target="_blank" rel="noopener">' + escapeHtml(label) + '</a>';
    });
    html += '</div>';
    addBot(html);
  }

  // 降级链：云端一次性接口 → 本地 BM25
  function localAnswer(q) {
    sub.textContent = '本地离线检索 · 云端暂不可达';
    ensureCorpus().then(function (ok) {
      if (!ok) {
        addBot('资料加载失败。请确认：<br>① 通过本地服务器访问（不要双击打开 HTML）；'
             + '<br>② <code>assets/qa/corpus.json</code> 存在。');
        return;
      }
      var hits = search(q);
      var ans = composeAnswer(q, hits);
      // ensureCorpus() 会把副标题改成「已索引 N 篇」，这里补回离线状态说明（P1）
      sub.textContent = '本地离线检索 · 已索引 ' + corpus.articles.length + ' 篇';
      addBot(ans.html);
      if (!ans.weak) addRelated(ans.related);
    });
  }

  function plainAsk(q) {
    backendSearch(q).then(function (data) {
      // 后端返回了有效结果（不管是否有命中片段都走后端渲染）
      if (data && data.hits) {
        cbReset();
        renderBackend(q, data);
        return;
      }
      if (cloudNetFail) cbOnFail();
      localAnswer(q);
    });
  }

  function handleSend(text) {
    var q = (text || input.value || '').trim();
    if (!q) return;
    input.value = '';
    addUser(q);

    // 熔断器断开期间：直接走本地，用户零等待；冷却结束后后台探活，恢复自动生效
    if (!cbAllowCloud()) {
      localAnswer(q);
      cbMaybeProbe();
      return;
    }

    if (USE_STREAM && supportsStream()) {
      sub.textContent = '云端 AI 答疑 · 正在思考…';
      streamAsk(q).then(function (st) {
        if (st === 'ok') { cbReset(); return; }
        if (st === 'rate_limited') {
          addBot('提问太频繁了，请稍等一会儿再试。');   // 429 说明服务活着，不熔断
          return;
        }
        // 网络级不可达：TCP 都连不上，一次性接口必然同样失败，直接跳本地不再重复等
        if (cloudNetFail) { cbOnFail(); localAnswer(q); return; }
        plainAsk(q);          // 仅应用级失败（非 SSE / HTTP 错误）才试一次性接口 → 本地兜底
      });
      return;
    }
    plainAsk(q);
  }

  sendBtn.addEventListener('click', function () { handleSend(); });
  input.addEventListener('keydown', function (e) { if (e.key === 'Enter') handleSend(); });
  closeBtn.addEventListener('click', function () { panel.hidden = true; });
  fab.addEventListener('click', function () {
    panel.hidden = !panel.hidden;
    if (!panel.hidden) {
      // 仅在云端可用时预热，避免熔断期间还去硬等一个连不上的地址
      if (CB.state === 'closed' && !corpus && !loadFailed) backendSearch('');
      cbMaybeProbe();   // 冷却已过则后台探活，后端恢复后无需刷新页面即自动回到云端
      setTimeout(function () { input.focus(); }, 60);
    }
  });
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && !panel.hidden) panel.hidden = true;
  });

  cbLoad();   // 恢复熔断状态（仅当前标签页有效，关掉即忘，避免长期误判云端不可用）

  addBot('你好，我是<b>站内文档答疑</b>助手。<br>'
       + '优先由<b>云端后端</b>检索本站文章并作答；云端不可用时自动切换为本地检索。<br>'
       + '点下方文章名，或直接输入问题试试。');
})();
