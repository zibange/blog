/* 硬见 — Article page logic */
(function () {
  'use strict';

  const $ = (s, el = document) => el.querySelector(s);
  const $$ = (s, el = document) => Array.from(el.querySelectorAll(s));

  const params = new URLSearchParams(location.search);
  const slug = params.get('slug');

  const state = {
    manifest: null,
    article: null,
    toc: [],
  };

  /* ---------- Theme ---------- */
  function initTheme() {
    const saved = localStorage.getItem('yingjian-theme');
    if (saved) document.documentElement.setAttribute('data-theme', saved);
    $('#themeToggle')?.addEventListener('click', () => {
      const cur = document.documentElement.getAttribute('data-theme');
      const next = cur === 'dark' ? 'light' : 'dark';
      document.documentElement.setAttribute('data-theme', next);
      localStorage.setItem('yingjian-theme', next);
    });
  }

  /* ---------- Helpers ---------- */
  function fmtDate(iso) {
    if (!iso) return '';
    const d = new Date(iso);
    return `${d.getFullYear()} 年 ${d.getMonth() + 1} 月 ${d.getDate()} 日`;
  }
  function categoryName(id) {
    const c = (state.manifest?.categories || []).find(c => c.id === id);
    return c ? c.name : id;
  }
  function isRelative(href) {
    return !/^(https?:|mailto:|data:|tel:|#|\/)/i.test(href);
  }
  function resolvePath(href) {
    if (!href) return href;
    if (!isRelative(href)) return href;
    return `articles/${slug}/${href.replace(/^\.\//, '')}`;
  }
  function slugify(text) {
    return text
      .replace(/<[^>]+>/g, '')
      .trim()
      .replace(/\s+/g, '-')
      .replace(/[^\p{L}\p{N}\-一-龥]/gu, '')
      .toLowerCase() || 'section';
  }
  function stripHtml(s) {
    return (s || '').replace(/<[^>]+>/g, '').trim();
  }

  /* ---------- Render cover + header ---------- */
  function renderCover() {
    const a = state.article;
    const cover = resolvePath(a.cover);
    const cat = categoryName(a.category);
    const coverEl = $('#cover');
    coverEl.innerHTML = `
      <img src="${cover}" alt="${a.title}" onerror="this.style.opacity=0.15">
      <div class="article-cover-inner">
        <span class="cat">◆ ${cat}</span>
        <h1>${a.title}</h1>
        <div class="article-meta-bar">
          <span>${fmtDate(a.date)}</span>
          <span class="sep">·</span>
          <span>${a.readTime || 15} 分钟阅读</span>
        </div>
      </div>`;
    document.title = `${a.title} — 硬见`;
  }

  /* ---------- Markdown rendering ---------- */
  function renderMarkdown(md) {
    state.toc = [];
    marked.setOptions({ gfm: true, breaks: false });
    // Protect LaTeX spans from markdown inline parsing (_ and ^ would become em/sup)
    const mathSpans = [];
    let src = md.replace(/(?<!\\)(\$\$[\s\S]*?\$\$|\$[^$\n]*?\$)/g, m => {
      mathSpans.push(m);
      return `MATHBLOCKTOKEN${mathSpans.length - 1}MATHBLOCKTOKEN`;
    });
    let html = marked.parse(src);
    html = html.replace(/MATHBLOCKTOKEN(\d+)MATHBLOCKTOKEN/g, (m, i) => mathSpans[+i]);
    html = DOMPurify.sanitize(html, { ADD_ATTR: ['target', 'rel'] });

    // Post-process DOM: heading ids + TOC, image/link paths, cover dedup
    const container = document.createElement('div');
    container.innerHTML = html;

    // Headings: assign ids + collect TOC
    const usedIds = new Set();
    $$('h2, h3, h4', container).forEach(h => {
      const plain = stripHtml(h.textContent);
      let id = slugify(plain);
      let n = 1;
      while (usedIds.has(id)) { id = `${slugify(plain)}-${++n}`; }
      usedIds.add(id);
      h.id = id;
      const level = parseInt(h.tagName.charAt(1), 10);
      if (level >= 2 && level <= 3) state.toc.push({ id, text: plain, level });
    });

    // Images: rewrite relative src, wrap in figure with caption
    $$('img', container).forEach(img => {
      const src = img.getAttribute('src') || '';
      if (isRelative(src)) img.setAttribute('src', resolvePath(src));
      img.setAttribute('loading', 'lazy');
      const alt = img.getAttribute('alt') || '';
      if (alt && !img.parentElement.matches('figure')) {
        const fig = document.createElement('figure');
        fig.style.cssText = 'margin:28px 0;';
        img.parentNode.insertBefore(fig, img);
        fig.appendChild(img);
        const cap = document.createElement('figcaption');
        cap.style.cssText = 'text-align:center;color:var(--text-faint);font-size:0.85rem;margin-top:10px;';
        cap.textContent = alt;
        fig.appendChild(cap);
      }
    });

    // Links: rewrite relative href, external target
    $$('a', container).forEach(a => {
      const href = a.getAttribute('href') || '';
      if (isRelative(href)) a.setAttribute('href', resolvePath(href));
      else if (/^https?:/i.test(href)) {
        a.setAttribute('target', '_blank');
        a.setAttribute('rel', 'noopener');
      }
    });

    // Tables: wrap in scroll container
    $$('table', container).forEach(tbl => {
      if (!tbl.parentElement.matches('.table-scroll')) {
        const wrap = document.createElement('div');
        wrap.className = 'table-scroll';
        wrap.style.overflowX = 'auto';
        tbl.parentNode.insertBefore(wrap, tbl);
        wrap.appendChild(tbl);
      }
    });

    // Remove duplicate cover (first image matching the declared cover)
    if (state.article.cover) {
      const coverFull = resolvePath(state.article.cover).toLowerCase();
      const firstImg = container.querySelector('img');
      if (firstImg) {
        const firstSrc = (firstImg.getAttribute('src') || '').toLowerCase();
        if (firstSrc === coverFull) {
          const fig = firstImg.closest('figure');
          (fig || firstImg).remove();
        }
      }
    }

    // Render LaTeX (KaTeX) if available; degrades to plain text if CDN is unreachable
    if (typeof renderMathInElement === 'function') {
      try {
        renderMathInElement(container, {
          delimiters: [
            { left: '$$', right: '$$', display: true },
            { left: '$', right: '$', display: false }
          ],
          throwOnError: false
        });
      } catch (e) { /* keep raw text */ }
    }

    return container.innerHTML;
  }

  /* ---------- TOC ---------- */
  function renderTOC() {
    const toc = state.toc.filter(t => t.level <= 3 && t.level >= 2);
    const nav = $('#toc');
    if (!toc.length) {
      nav.innerHTML = '<div style="color:var(--text-faint);font-size:0.85rem;">暂无目录</div>';
      return;
    }
    nav.innerHTML = toc.map(t =>
      `<a href="#${t.id}" class="toc-h${t.level}" data-id="${t.id}">${t.text}</a>`
    ).join('');
    $$('#toc a').forEach(a => {
      a.addEventListener('click', e => {
        e.preventDefault();
        const el = document.getElementById(a.dataset.id);
        if (el) {
          const y = el.getBoundingClientRect().top + window.scrollY - 90;
          window.scrollTo({ top: y, behavior: 'smooth' });
        }
      });
    });
  }

  /* ---------- Scroll: progress + TOC active + back-to-top ---------- */
  function initScroll() {
    const progress = $('#progress');
    const backTop = $('#backTop');

    function onScroll() {
      const doc = document.documentElement;
      const scrollTop = window.scrollY || doc.scrollTop;
      const height = doc.scrollHeight - doc.clientHeight;
      const pct = height > 0 ? (scrollTop / height) * 100 : 0;
      progress.style.width = pct + '%';

      backTop.classList.toggle('show', scrollTop > 600);

      // TOC active
      const headings = $$('.article-content h2, .article-content h3');
      let current = null;
      for (const h of headings) {
        const top = h.getBoundingClientRect().top;
        if (top < 140) current = h.id;
        else break;
      }
      $$('#toc a').forEach(a => {
        a.classList.toggle('active', a.dataset.id === current);
      });
    }
    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();

    backTop.addEventListener('click', () => window.scrollTo({ top: 0, behavior: 'smooth' }));
  }

  /* ---------- Prev / Next ---------- */
  function renderArticleNav() {
    const list = (state.manifest.articles || []).slice().sort((a, b) => (b.date || '').localeCompare(a.date || ''));
    const idx = list.findIndex(a => a.slug === slug);
    const prev = idx > 0 ? list[idx - 1] : null;
    const next = idx < list.length - 1 ? list[idx + 1] : null;
    const wrap = $('#articleNav');

    const card = (a, dir) => {
      if (!a) return '<div></div>';
      const label = dir === 'prev' ? '← 上一篇' : '下一篇 →';
      return `<a href="article.html?slug=${a.slug}" class="${dir}">
        <div class="label">${label}</div>
        <div class="t">${a.title}</div>
      </a>`;
    };
    wrap.innerHTML = card(prev, 'prev') + card(next, 'next');
  }

  /* ---------- Init ---------- */
  async function init() {
    initTheme();

    if (!slug) {
      $('#content').innerHTML = '<p style="color:var(--text-muted);">未指定文章。<a href="index.html" style="color:var(--accent);">返回首页</a></p>';
      return;
    }

    try {
      const res = await fetch(`articles.json?v=${Date.now()}`, { cache: 'no-store' });
      state.manifest = await res.json();
      state.article = state.manifest.articles.find(a => a.slug === slug);
      if (!state.article) throw new Error('Article not found');

      renderCover();

      const mdRes = await fetch(`articles/${slug}/${state.article.file}?v=${Date.now()}`, { cache: 'no-store' });
      if (!mdRes.ok) throw new Error('MD fetch failed');
      const md = await mdRes.text();

      let html = renderMarkdown(md);

      $('#content').innerHTML = html;

      // highlight code
      $$('#content pre code').forEach(block => {
        hljs.highlightElement(block);
      });

      renderTOC();
      renderArticleNav();
      initScroll();
    } catch (e) {
      $('#cover').innerHTML = '';
      $('#content').innerHTML = `<p style="color:var(--text-muted);">加载失败：${e.message}。<a href="index.html" style="color:var(--accent);">返回首页</a></p>`;
      console.error(e);
    }
  }

  document.addEventListener('DOMContentLoaded', init);
})();
