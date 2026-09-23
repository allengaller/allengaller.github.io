/* 不花 GTM · 渲染与动效（尊重 prefers-reduced-motion） */
(function () {
  'use strict';
  document.documentElement.classList.add('js');
  var D = window.GTM;
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var palette = ['--candy', '--sun', '--leaf', '--sea', '--mint'];

  function cssVar(n) { return getComputedStyle(document.documentElement).getPropertyValue(n).trim(); }

  /* ---- Hero dot map: 1 dot = 1 city ---- */
  var dotmap = document.getElementById('dotmap');
  if (dotmap) {
    var frag = document.createDocumentFragment();
    for (var i = 0; i < D.cityCount; i++) {
      var d = document.createElement('span');
      d.className = 'dot';
      d.style.background = 'var(' + palette[i % palette.length] + ')';
      d.title = '已覆盖城市 ' + (i + 1);
      frag.appendChild(d);
    }
    dotmap.appendChild(frag);
  }

  /* ---- Bar charts ---- */
  function bars(el, rows, labelFn) {
    if (!el) return;
    var max = rows[0][1];
    rows.forEach(function (r, idx) {
      var row = document.createElement('div');
      row.className = 'bar-row';
      var label = document.createElement('span');
      label.className = 'label';
      label.textContent = labelFn(r[0]);
      var track = document.createElement('span');
      track.className = 'track';
      var fill = document.createElement('span');
      fill.className = 'fill';
      fill.style.background = 'var(' + palette[idx % palette.length] + ')';
      track.appendChild(fill);
      var val = document.createElement('span');
      val.className = 'val num';
      val.textContent = r[1];
      row.appendChild(label); row.appendChild(track); row.appendChild(val);
      el.appendChild(row);
      requestAnimationFrame(function () {
        setTimeout(function () { fill.style.width = Math.round((r[1] / max) * 100) + '%'; }, reduce ? 0 : 120 + idx * 60);
      });
    });
  }
  bars(document.getElementById('catBars'), D.topCategories, function (k) { return D.catLabel[k] || k; });
  bars(document.getElementById('cityBars'), D.topCities, function (k) { return k; });

  /* ---- Count-up metrics ---- */
  function countUp(el) {
    var target = parseInt(el.dataset.count, 10);
    if (reduce) { el.textContent = target.toLocaleString(); return; }
    var t0 = null, dur = 1200;
    function step(t) {
      if (!t0) t0 = t;
      var p = Math.min((t - t0) / dur, 1);
      var eased = 1 - Math.pow(1 - p, 4);
      el.textContent = Math.round(target * eased).toLocaleString();
      if (p < 1) requestAnimationFrame(step);
    }
    requestAnimationFrame(step);
  }
  document.querySelectorAll('[data-count]').forEach(countUp);

  /* ---- Flywheel SVG ---- */
  var wheel = document.getElementById('wheel');
  if (wheel) {
    var nodes = [
      ['数据资产', '--candy'], ['内容分发', '--sea'],
      ['打卡留存', '--leaf'], ['合作变现', '--sun']
    ];
    var cx = 210, cy = 210, R = 150;
    var ns = 'http://www.w3.org/2000/svg';
    var svg = document.createElementNS(ns, 'svg');
    svg.setAttribute('viewBox', '0 0 420 420');
    var spin = document.createElementNS(ns, 'g');
    spin.setAttribute('class', 'spin');
    var dash = document.createElementNS(ns, 'circle');
    dash.setAttribute('cx', cx); dash.setAttribute('cy', cy); dash.setAttribute('r', R);
    dash.setAttribute('fill', 'none');
    dash.setAttribute('stroke', cssVar('--ink-soft'));
    dash.setAttribute('stroke-width', '2.5');
    dash.setAttribute('stroke-dasharray', '4 10');
    spin.appendChild(dash);
    nodes.forEach(function (n, i) {
      var a = (Math.PI / 2) * i - Math.PI / 2;
      var x = cx + R * Math.cos(a), y = cy + R * Math.sin(a);
      var g = document.createElementNS(ns, 'g');
      var c = document.createElementNS(ns, 'circle');
      c.setAttribute('cx', x); c.setAttribute('cy', y); c.setAttribute('r', 52);
      c.setAttribute('fill', 'var(' + n[1] + ')');
      c.setAttribute('stroke', cssVar('--ink-strong'));
      c.setAttribute('stroke-width', '3');
      var t = document.createElementNS(ns, 'text');
      t.setAttribute('x', x); t.setAttribute('y', y + 6);
      t.setAttribute('text-anchor', 'middle');
      t.setAttribute('font-size', '17'); t.setAttribute('font-weight', '700');
      t.setAttribute('fill', cssVar('--ink-strong'));
      t.textContent = n[0];
      g.appendChild(c); g.appendChild(t);
      spin.appendChild(g);
    });
    svg.appendChild(spin);
    var core = document.createElementNS(ns, 'text');
    core.setAttribute('x', cx); core.setAttribute('y', cy + 8);
    core.setAttribute('text-anchor', 'middle');
    core.setAttribute('font-size', '26'); core.setAttribute('font-weight', '900');
    core.setAttribute('fill', cssVar('--candy-deep'));
    core.textContent = '不花';
    svg.appendChild(core);
    wheel.appendChild(svg);
  }

  /* ---- Scroll reveal (enhance-only) ---- */
  var revealEls = document.querySelectorAll('[data-reveal]');
  if (!reduce && 'IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) { e.target.classList.add('revealed'); io.unobserve(e.target); }
      });
    }, { threshold: 0.15 });
    revealEls.forEach(function (el) { io.observe(el); });
  } else {
    revealEls.forEach(function (el) { el.classList.add('revealed'); });
  }

  /* ---- Back to top ---- */
  var top = document.getElementById('btnTop');
  if (top) {
    var onScroll = function () { top.hidden = window.scrollY < 900; };
    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();
    top.addEventListener('click', function () { window.scrollTo({ top: 0, behavior: reduce ? 'auto' : 'smooth' }); });
  }
})();
