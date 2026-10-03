/* =============================================================
 * 硬见 · 站内文档答疑（无 AI 纯检索版）
 *
 * 运行原理：
 *   1. 打开面板时才懒加载 corpus.json（由 ai-chatbot/build_corpus.py 从
 *      blog/articles/**\/*.md 生成），首屏零开销
 *   2. 浏览器内中文分词（Intl.Segmenter，退化 bigram）+ 倒排索引 + BM25 打分
 *   3. 取 top-K 原文片段作为"答案"，高亮命中词，附文章出处链接
 *
 * 特性：无 AI、无接口、无密钥、无后端；答案即站内文章原文摘录。
 * 外观：复用博客的 CSS 主题变量，跟随 data-theme 自动切换明暗。
 *
 * 安全边界：纯新增文件，不修改博客任何既有 JS / JSON / 样式。
 * 后续接 AI 时只需替换 composeAnswer() 为"把片段喂给 LLM"，检索层完全复用。
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

  /* ---------------- 中文分词 ----------------
   * 索引与查询必须用同一个分词器，否则召回会错位。
   */
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

  /* ---------------- 索引与检索 ---------------- */
  var corpus = null, index = null, loading = false, loadFailed = false;

  function buildIndex(chunks) {
    var df = new Map();   // 词 -> 出现在多少片段中
    var tfList = [];      // 每个片段的词频表
    var lens = [];        // 每个片段的词数
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

    // BM25
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

    // 加成：整句命中 > 标题命中 > 词命中标题
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

  /* ---------------- 组装答案 ---------------- */
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

  /* ---------------- 样式（复用博客主题变量，自动明暗） ---------------- */
  var css = [
    '.hw-fab{position:fixed;right:24px;bottom:24px;width:52px;height:52px;border-radius:50%;',
    ' background:var(--accent,#c9a227);color:var(--bg,#0a0a0b);border:1px solid var(--border-light,transparent);',
    ' cursor:pointer;display:grid;place-items:center;z-index:100001;',
    ' box-shadow:0 12px 32px -8px rgba(0,0,0,.45);transition:transform .2s var(--ease,ease),opacity .2s;}',
    '.hw-fab:hover{transform:scale(1.07);}',
    '.hw-fab.hw-lift{bottom:92px;}',                    /* 文章页有"回到顶部"按钮时上移避让 */
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
  var hasBackTop = !!document.querySelector('.back-top');   // 文章页专用的避让判断

  var fab = document.createElement('button');
  fab.className = 'hw-fab' + (hasBackTop ? ' hw-lift' : '');
  fab.type = 'button';
  fab.setAttribute('aria-label', '打开站内答疑助手');
  // 机器人图标：天线 + 圆角头部 + 侧翼 + 双眼 + 微笑嘴
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
        '<div class="hw-sub" id="hwSub">基于本站文章检索 · 无 AI 生成</div>' +
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

  /* ---------------- 数据加载（懒加载：首次打开面板才拉取） ---------------- */
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

  function handleSend(text) {
    var q = (text || input.value || '').trim();
    if (!q) return;
    input.value = '';
    addUser(q);

    ensureCorpus().then(function (ok) {
      if (!ok) {
        addBot('资料加载失败。请确认：<br>① 通过本地服务器访问（不要双击打开 HTML）；'
             + '<br>② <code>assets/qa/corpus.json</code> 存在。');
        return;
      }
      var hits = search(q);
      var ans = composeAnswer(q, hits);
      addBot(ans.html);
      if (!ans.weak) addRelated(ans.related);
    });
  }

  sendBtn.addEventListener('click', function () { handleSend(); });
  input.addEventListener('keydown', function (e) { if (e.key === 'Enter') handleSend(); });
  closeBtn.addEventListener('click', function () { panel.hidden = true; });
  fab.addEventListener('click', function () {
    panel.hidden = !panel.hidden;
    if (!panel.hidden) {
      ensureCorpus();
      setTimeout(function () { input.focus(); }, 60);
    }
  });
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && !panel.hidden) panel.hidden = true;
  });

  addBot('你好，我是<b>站内文档答疑</b>助手。<br>'
       + '我会从本站文章里检索相关内容，把<b>原文片段</b>和出处给你 —— 不生成、不编造。<br>'
       + '点下方文章名，或直接输入问题试试。');
})();
