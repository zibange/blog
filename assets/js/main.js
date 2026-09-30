/* 硬见 — Home page logic */
(function () {
  'use strict';

  const $ = (s, el = document) => el.querySelector(s);
  const $$ = (s, el = document) => Array.from(el.querySelectorAll(s));

  const state = {
    manifest: null,
    activeCategory: 'all',
  };

  /* ---------- Theme ---------- */
  function initTheme() {
    const saved = localStorage.getItem('yingjian-theme');
    if (saved) document.documentElement.setAttribute('data-theme', saved);
    const btn = $('#themeToggle');
    if (btn) btn.addEventListener('click', () => {
      const cur = document.documentElement.getAttribute('data-theme');
      const next = cur === 'dark' ? 'light' : 'dark';
      document.documentElement.setAttribute('data-theme', next);
      localStorage.setItem('yingjian-theme', next);
    });
  }

  /* ---------- Date formatting ---------- */
  function fmtDate(iso) {
    if (!iso) return '';
    const d = new Date(iso);
    return `${d.getFullYear()}.${String(d.getMonth() + 1).padStart(2, '0')}.${String(d.getDate()).padStart(2, '0')}`;
  }

  function categoryName(id, manifest) {
    const c = (manifest.categories || []).find(c => c.id === id);
    return c ? c.name : id;
  }

  /* ---------- Render filters ---------- */
  function renderFilters() {
    const wrap = $('#filters');
    const cats = state.manifest.categories || [];
    const all = [{ id: 'all', name: '全部' }].concat(cats);
    wrap.innerHTML = all.map(c =>
      `<button class="filter-chip ${c.id === state.activeCategory ? 'active' : ''}" data-cat="${c.id}">${c.name}</button>`
    ).join('');
    $$('.filter-chip', wrap).forEach(btn => {
      btn.addEventListener('click', () => {
        state.activeCategory = btn.dataset.cat;
        renderFilters();
        renderGrid();
      });
    });
  }

  /* ---------- Render grid ---------- */
  function renderGrid() {
    const grid = $('#grid');
    let list = (state.manifest.articles || []).slice();
    if (state.activeCategory !== 'all') {
      list = list.filter(a => a.category === state.activeCategory);
    }
    // sort by date desc
    list.sort((a, b) => (b.date || '').localeCompare(a.date || ''));

    $('#articleCount').textContent = `（${list.length}）`;
    $('#statCount').textContent = state.manifest.articles.length;
    $('#catCount').textContent = (state.manifest.categories || []).length;

    if (!list.length) {
      grid.innerHTML = '<div style="grid-column:1/-1;text-align:center;color:var(--text-muted);padding:60px 0;">该分类下暂无文章</div>';
      return;
    }

    grid.innerHTML = list.map((a, i) => {
      const featured = i === 0 && state.activeCategory === 'all';
      const cover = `articles/${a.slug}/${a.cover}`;
      const cat = categoryName(a.category, state.manifest);
      return `
        <a class="card ${featured ? 'featured' : ''}" href="article.html?slug=${a.slug}" style="animation-delay:${i * 0.06}s">
          <div class="card-cover">
            <img src="${cover}" alt="${a.title}" loading="lazy" onerror="this.style.display='none'">
          </div>
          <div class="card-body">
            <span class="card-tag">${cat}</span>
            <h3 class="card-title">${a.title}</h3>
            <p class="card-excerpt">${a.excerpt || ''}</p>
            <div class="card-meta">
              <span>${fmtDate(a.date)}</span>
              <span class="dot"></span>
              <span>${a.readTime || 15} min 阅读</span>
            </div>
            <span class="read-more">阅读全文 →</span>
          </div>
        </a>`;
    }).join('');
  }

  /* ---------- Init ---------- */
  async function init() {
    initTheme();
    try {
      const res = await fetch(`articles.json?v=${Date.now()}`, { cache: 'no-store' });
      state.manifest = await res.json();
      document.title = `${state.manifest.site.title} — ${state.manifest.site.subtitle}`;
      renderFilters();
      renderGrid();
    } catch (e) {
      $('#grid').innerHTML = '<div style="grid-column:1/-1;text-align:center;color:var(--text-muted);">加载文章列表失败，请通过本地服务器访问（不要直接双击打开 HTML）。</div>';
      console.error(e);
    }
  }

  document.addEventListener('DOMContentLoaded', init);
})();
