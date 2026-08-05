/* ─────────────────────────────────────────────────────────
   Cmd+K Command Palette — global jump & search
   ─────────────────────────────────────────────────────────
   - Triggered by Cmd+K (mac) / Ctrl+K (others) or "/"
   - Searches across static pages + indexed repos
   - Arrow keys + Enter to navigate, Esc to close
   - Loads /_data/repos.json (lightweight) for repo search
   ───────────────────────────────────────────────────────── */
(function () {
  'use strict';

  // ── Static pages registry (always available) ──
  const PAGES = [
    { name: 'Home',         url: '/',                 hint: '首页 · 概览',            keywords: 'home index landing' },
    { name: 'Projects',     url: '/projects/',        hint: '精选项目 · 6 个 banner',  keywords: 'projects featured portfolio' },
    { name: 'Repos',        url: '/repos/',           hint: '本地 GitHub 镜像总览',     keywords: 'repos github index all' },
    { name: 'Links',        url: '/topic/links/',     hint: '常用外部链接集合',         keywords: 'links bookmarks external' },
    { name: 'AI Tools',     url: '/topic/ai-tools/',  hint: 'AI 工具分类与推荐',        keywords: 'ai tools llm gpt' },
    { name: 'About',        url: '/about/',           hint: '关于我 · 三重身份',        keywords: 'about bio profile sre' },
    { name: 'Archive',      url: '/topic/archive/',   hint: '归档总览',                 keywords: 'archive history' },
    { name: 'Sitemap',      url: '/sitemap.xml',      hint: '站点地图',                 keywords: 'sitemap xml' },
    { name: 'humans.txt',   url: '/humans.txt',       hint: '这个站点的来龙去脉',       keywords: 'humans credits' },
    { name: 'RSS Feed',     url: '/feed.xml',         hint: '最近更新的仓库',           keywords: 'rss atom feed subscribe' },
    { name: 'security.txt', url: '/.well-known/security.txt', hint: '安全联系方式',        keywords: 'security contact' },
    { name: 'Source on GitHub', url: 'https://github.com/allengaller/allengaller.github.io', hint: '本站源码',     keywords: 'source code github' },
  ];

  let repoIndex = null;
  let loadingPromise = null;
  let open = false;
  let activeIdx = 0;
  let filtered = [];
  let modal, input, list, hint, status;

  // ── Build DOM once ──
  function buildModal() {
    if (modal) return;
    const wrap = document.createElement('div');
    wrap.id = 'palette';
    wrap.setAttribute('role', 'dialog');
    wrap.setAttribute('aria-modal', 'true');
    wrap.setAttribute('aria-label', '命令面板');
    wrap.hidden = true;
    wrap.innerHTML = `
      <div class="palette-backdrop" data-palette-close></div>
      <div class="palette-panel" role="document">
        <div class="palette-input-row">
          <svg class="palette-icon" viewBox="0 0 16 16" width="16" height="16" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true">
            <circle cx="7" cy="7" r="5"/>
            <path d="M11 11 L14 14" stroke-linecap="round"/>
          </svg>
          <input id="palette-input" type="text" placeholder="跳到… 搜索仓库、页面、链接"
                 autocomplete="off" spellcheck="false" aria-label="搜索">
          <kbd class="palette-kbd">esc</kbd>
        </div>
        <ul id="palette-list" class="palette-list" role="listbox" aria-label="搜索结果"></ul>
        <div class="palette-foot">
          <span id="palette-status" class="palette-status">输入关键词 · ↑↓ 移动 · ↵ 跳转</span>
          <span class="palette-foot-hint"><kbd>↑↓</kbd> 移动 · <kbd>↵</kbd> 打开 · <kbd>esc</kbd> 关闭</span>
        </div>
      </div>
    `;
    document.body.appendChild(wrap);
    modal = wrap;
    input = wrap.querySelector('#palette-input');
    list = wrap.querySelector('#palette-list');
    status = wrap.querySelector('#palette-status');

    wrap.addEventListener('click', (e) => {
      if (e.target.matches('[data-palette-close]')) close();
    });
    input.addEventListener('input', () => render(input.value));
    input.addEventListener('keydown', onKey);
    list.addEventListener('click', (e) => {
      const li = e.target.closest('[data-idx]');
      if (li) jump(parseInt(li.dataset.idx, 10));
    });
  }

  // ── Load repo index lazily ──
  function loadRepoIndex() {
    if (repoIndex) return Promise.resolve(repoIndex);
    if (loadingPromise) return loadingPromise;
    loadingPromise = fetch('/_data/repos.json', { cache: 'force-cache' })
      .then((r) => r.ok ? r.json() : { repos: [] })
      .then((d) => {
        repoIndex = (d.repos || []).filter((r) => r.is_own).map((r) => ({
          name: r.name,
          org: r.org,
          full_name: r.full_name,
          url: `/repos/${r.org}/${r.name}/`,
          hint: `${r.org} · ${r.language_top || '—'} · ${r.commits_total || 0} commits`,
          keywords: `${r.name} ${r.org} ${r.description || ''} ${r.readme_excerpt || ''} ${(r.languages || []).join(' ')}`.toLowerCase(),
        }));
        return repoIndex;
      })
      .catch(() => { repoIndex = []; return repoIndex; });
    return loadingPromise;
  }

  // ── Search ──
  function searchAll(query) {
    const q = query.trim().toLowerCase();
    if (!q) {
      // Empty query: show top pages
      return PAGES.slice(0, 8).map((p, i) => ({ ...p, type: 'page', idx: i }));
    }
    const out = [];
    // Pages
    PAGES.forEach((p) => {
      const hay = `${p.name} ${p.hint} ${p.keywords}`.toLowerCase();
      const score = scoreMatch(q, hay, p.name.toLowerCase());
      if (score > 0) out.push({ ...p, type: 'page', score });
    });
    // Repos (only own)
    if (repoIndex) {
      repoIndex.forEach((r) => {
        const score = scoreMatch(q, r.keywords, r.name.toLowerCase());
        if (score > 0) out.push({ ...r, type: 'repo', score });
      });
    }
    out.sort((a, b) => b.score - a.score);
    return out.slice(0, 12);
  }

  function scoreMatch(query, hay, primary) {
    if (!hay) return 0;
    if (primary === query) return 1000;
    if (primary.startsWith(query)) return 500;
    if (hay.includes(query)) {
      // Boost if it's near the start
      const idx = hay.indexOf(query);
      return 200 - Math.min(idx, 100);
    }
    // Fuzzy: every char in order
    let qi = 0;
    for (let i = 0; i < hay.length && qi < query.length; i++) {
      if (hay[i] === query[qi]) qi++;
    }
    return qi === query.length ? 30 : 0;
  }

  function render(query) {
    filtered = searchAll(query);
    if (filtered.length === 0) {
      list.innerHTML = `<li class="palette-empty">没有匹配的结果 · 试试别的关键词</li>`;
      status.textContent = query ? `没有匹配 " ${query} "` : '输入关键词开始搜索';
      return;
    }
    activeIdx = Math.min(activeIdx, filtered.length - 1);
    list.innerHTML = filtered.map((item, i) => {
      const isActive = i === activeIdx ? 'is-active' : '';
      const icon = item.type === 'repo'
        ? `<svg class="palette-item-icon" viewBox="0 0 16 16" width="14" height="14" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true"><path d="M2 2.5L8 1L14 2.5V13.5L8 15L2 13.5V2.5Z"/><path d="M2 2.5L8 4L14 2.5"/><path d="M8 4V15"/></svg>`
        : `<svg class="palette-item-icon" viewBox="0 0 16 16" width="14" height="14" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true"><path d="M2 13V3L8 1L14 3V13L8 15L2 13Z"/><path d="M2 3L8 5L14 3"/><path d="M8 5V15"/></svg>`;
      return `<li class="palette-item ${isActive}" data-idx="${i}" role="option" aria-selected="${i === activeIdx}">
        ${icon}
        <span class="palette-item-name">${escapeHtml(item.name)}</span>
        <span class="palette-item-hint">${escapeHtml(item.hint || '')}</span>
        <span class="palette-item-type">${item.type === 'repo' ? '仓库' : '页面'}</span>
      </li>`;
    }).join('');
    status.textContent = `${filtered.length} 个结果 · 当前 ${activeIdx + 1}/${filtered.length}`;
    // Scroll active into view
    const activeEl = list.querySelector('.palette-item.is-active');
    if (activeEl) activeEl.scrollIntoView({ block: 'nearest' });
  }

  function onKey(e) {
    if (e.key === 'ArrowDown') {
      e.preventDefault();
      activeIdx = (activeIdx + 1) % Math.max(filtered.length, 1);
      render(input.value);
    } else if (e.key === 'ArrowUp') {
      e.preventDefault();
      activeIdx = (activeIdx - 1 + filtered.length) % Math.max(filtered.length, 1);
      render(input.value);
    } else if (e.key === 'Enter') {
      e.preventDefault();
      jump(activeIdx);
    } else if (e.key === 'Escape') {
      e.preventDefault();
      close();
    }
  }

  function jump(idx) {
    const item = filtered[idx];
    if (!item) return;
    if (item.url.startsWith('http')) {
      window.open(item.url, '_blank', 'noopener');
    } else {
      window.location.href = item.url;
    }
  }

  function openPalette() {
    if (open) return;
    buildModal();
    open = true;
    modal.hidden = false;
    document.body.classList.add('palette-open');
    input.value = '';
    activeIdx = 0;
    loadRepoIndex(); // start loading (don't await)
    render('');
    setTimeout(() => input.focus(), 30);
  }

  function close() {
    if (!open) return;
    open = false;
    modal.hidden = true;
    document.body.classList.remove('palette-open');
    input.value = '';
  }

  // ── Global keybindings ──
  document.addEventListener('keydown', (e) => {
    // Cmd+K (mac) / Ctrl+K (others)
    if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === 'k') {
      e.preventDefault();
      open ? close() : openPalette();
      return;
    }
    // "/" when not typing
    if (e.key === '/' && !open) {
      const t = e.target;
      const isTyping = t && (t.tagName === 'INPUT' || t.tagName === 'TEXTAREA' || t.isContentEditable);
      if (isTyping) return;
      e.preventDefault();
      openPalette();
    }
    if (e.key === 'Escape' && open) {
      e.preventDefault();
      close();
    }
  });

  function escapeHtml(s) {
    return String(s == null ? '' : s).replace(/[&<>"']/g, (c) => ({
      '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;',
    }[c]));
  }

  // ── Trigger hook (for [data-palette-trigger] buttons) ──
  document.addEventListener('click', (e) => {
    const t = e.target.closest('[data-palette-trigger]');
    if (!t) return;
    e.preventDefault();
    open ? close() : openPalette();
  });

  // ── Public API ──
  window.__palette = { open: openPalette, close };
})();
