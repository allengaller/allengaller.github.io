/* GTM 增刊 — 自包含数据层与交互；数据由 GTM/build.js 生成（GTM/data/gtm.json） */
const RM = matchMedia('(prefers-reduced-motion: reduce)').matches;
const INK = '#191614', RED = '#d6362b', RED_INK = '#a93226', GRAPHITE = '#6e685c', HAIR = 'rgba(25,22,20,0.18)';
const MONO = 'Spline Sans Mono, monospace', DIDONE = 'Bodoni Moda, serif';
const PAGE = 60;

const PRICING_CN = { subscription: '订阅制', usage: '按量计费', take_rate: '交易抽成', project: '项目制 / 买断', freemium: '免费增值', ads: '广告' };
const STRATEGY_CN = { plg: 'PLG 产品驱动', sales: '销售驱动', content: '内容 / 社区', channel: '渠道 / 伙伴', trial: '试用转化' };

const esc = (s) => String(s ?? '').replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[c]);
const fmt2 = (v) => (v == null ? '--' : Number(v).toFixed(2));
const folioNo = (id) => `NO.${/^\d+/.exec(String(id))?.[0].padStart(4, '0') ?? '----'}`;
const $ = (id) => document.getElementById(id);

let DATA = null;
let filtered = [];
let page = 0;
let lastFocus = null;

async function main() {
  const res = await fetch('./data/gtm.json?v=1');
  DATA = await res.json();
  fillStats();
  drawCharts();
  bindLedger();
  reveal();
}

function fillStats() {
  const { stats, meta } = DATA;
  const cov = meta.coverage;
  const set = (id, v) => { const el = $(id); if (el) el.textContent = v; };
  set('h-biz', fmt2(stats.dimMeans.biz));
  set('h-total', meta.sources.ideas);
  set('s-total', meta.sources.ideas);
  set('s-biz', fmt2(stats.dimMeans.biz));
  set('s-compete', fmt2(stats.dimMeans.compete));
  set('s-weakest', stats.weakest.biz);
  set('s-weakest-pct', Math.round((stats.weakest.biz / meta.sources.ideas) * 100) + '%');
  set('s-section', cov.bizSection);
  set('t-solution', fmt2(stats.dimMeans.solution));
  set('t-pain', fmt2(stats.dimMeans.pain));
  set('t-biz', fmt2(stats.dimMeans.biz));
  set('t-compete', fmt2(stats.dimMeans.compete));
  set('t-wbiz', stats.weakest.biz);
  set('t-wcompete', stats.weakest.compete);
  set('c1-n', meta.sources.ideas);
  set('sb-wbiz', stats.weakest.biz);
  set('sb-wbiz-pct', Math.round((stats.weakest.biz / meta.sources.ideas) * 100) + '%');
  set('sb-wcompete', stats.weakest.compete);
  set('sb-abiz', fmt2(stats.byGrade.A?.bizMean));
  set('sb-bbiz', fmt2(stats.byGrade.B?.bizMean));
  set('u-n', stats.ratio.n);
  set('u-median', stats.ratio.median);
  set('u-ge3', Math.round((stats.ratio.ge3 / stats.ratio.n) * 100) + '%');
  set('u-biz', fmt2(stats.dimMeans.biz));
  set('c2-n', stats.ratio.n);
  const pc = stats.pricingCounts;
  set('p-n', cov.pricing);
  set('p-sub', pc.subscription ?? 0);
  set('p-sub-pct', Math.round(((pc.subscription ?? 0) / cov.pricing) * 100) + '%');
  set('p-proj', pc.project ?? 0);
  set('p-take', pc.take_rate ?? 0);
  set('p-usage', pc.usage ?? 0);
  set('p-free', pc.freemium ?? 0);
  set('g-n', cov.strategy);
  set('g-content', stats.strategyCounts.content ?? 0);
  set('g-channel', stats.strategyCounts.channel ?? 0);
  set('g-sales', stats.strategyCounts.sales ?? 0);
  set('g-plg', stats.strategyCounts.plg ?? 0);
  const tp = stats.trackProfiles;
  set('tr-top-name', tp[0]?.track);
  set('tr-top', fmt2(tp[0]?.bizMean));
  set('tr-bot-name', tp[tp.length - 1]?.track);
  set('tr-bot', fmt2(tp[tp.length - 1]?.bizMean));
  $('track-tbody').innerHTML = [...tp.slice(0, 3), ...tp.slice(-3)].map((t, i) =>
    `<tr><td>${esc(t.track)}</td><td>${t.n}</td><td class="num ${i < 3 ? 'hi' : ''}">${fmt2(t.bizMean)}</td></tr>`).join('');
  set('l-section', cov.bizSection);
  set('l-all', meta.sources.ideas);
  set('sb-section', cov.bizSection);
  set('sb-files', meta.sources.markdown);
  set('sb-cover', Math.round((cov.bizSection / meta.sources.markdown) * 100) + '%');
  set('sb-sub', Math.round(((pc.subscription ?? 0) / cov.pricing) * 100) + '%');
  set('sb-pricing-n', cov.pricing);
  set('sb-median', stats.ratio.median);
  set('sb-low', stats.ratio.histogram[0].n + stats.ratio.histogram[1].n);
  set('cv-section', cov.bizSection);
  set('cv-files', meta.sources.markdown);
  set('cv-pricing', cov.pricing);
  set('cv-ratio', cov.ratio);
  set('cv-moat', cov.moat);
}

function baseOpt() {
  return {
    animation: !RM,
    textStyle: { fontFamily: MONO, color: GRAPHITE },
    grid: { left: 118, right: 64, top: 8, bottom: 28 },
  };
}
function hbarChart(el, cats, values, redIdx, fmt = (v) => v) {
  const ch = echarts.init(el);
  ch.setOption({
    ...baseOpt(),
    xAxis: { type: 'value', max: Math.max(...values) * 1.12, splitLine: { lineStyle: { color: HAIR } }, axisLabel: { fontFamily: MONO, fontSize: 10, color: GRAPHITE } },
    yAxis: { type: 'category', inverse: true, data: cats, axisLine: { show: false }, axisTick: { show: false }, axisLabel: { fontFamily: MONO, fontSize: 11, color: (v) => (redIdx.includes(cats.indexOf(v)) ? RED_INK : GRAPHITE) } },
    series: [{
      type: 'bar', barWidth: 9,
      data: values.map((v, i) => ({ value: v, itemStyle: { color: redIdx.includes(i) ? RED : INK } })),
      label: { show: true, position: 'right', fontFamily: DIDONE, fontSize: 14, fontWeight: 700, color: INK, formatter: (p) => fmt(p.value) },
    }],
  });
  return ch;
}

const charts = [];
function drawCharts() {
  const { stats } = DATA;
  const dims = [
    ['PAIN 痛点', stats.dimMeans.pain], ['MARKET 市场', stats.dimMeans.market],
    ['SOLUTION 方案', stats.dimMeans.solution], ['BIZ 商业模式', stats.dimMeans.biz],
    ['COMPETE 竞争', stats.dimMeans.compete], ['FEASIBILITY 可行', stats.dimMeans.feasibility],
  ];
  charts.push(hbarChart($('chart-dims'), dims.map((d) => d[0]), dims.map((d) => d[1]), [3], (v) => v.toFixed(2)));

  const hist = stats.ratio.histogram;
  const ratioCh = echarts.init($('chart-ratio'));
  ratioCh.setOption({
    ...baseOpt(),
    grid: { left: 40, right: 20, top: 24, bottom: 30 },
    xAxis: { type: 'category', data: hist.map((h) => h.label), axisLine: { lineStyle: { color: INK } }, axisTick: { show: false }, axisLabel: { fontFamily: MONO, fontSize: 11, color: GRAPHITE } },
    yAxis: { type: 'value', splitLine: { lineStyle: { color: HAIR } }, axisLabel: { fontFamily: MONO, fontSize: 10, color: GRAPHITE } },
    series: [{
      type: 'bar', barWidth: '58%',
      data: hist.map((h, i) => ({ value: h.n, itemStyle: { color: i < 2 ? RED : INK } })),
      label: { show: true, position: 'top', fontFamily: DIDONE, fontSize: 14, fontWeight: 700, color: INK },
      markLine: {
        symbol: 'none',
        lineStyle: { color: RED, type: 'dashed', width: 1.5 },
        label: { formatter: '健康线 3', fontFamily: MONO, fontSize: 10, color: RED_INK, position: 'insideEndTop' },
        data: [{ xAxis: 1.5 }],
      },
    }],
  });
  charts.push(ratioCh);

  const pc = stats.pricingCounts;
  const pCats = Object.keys(PRICING_CN).map((k) => [PRICING_CN[k], pc[k] ?? 0]).sort((a, b) => b[1] - a[1]);
  charts.push(hbarChart($('chart-pricing'), pCats.map((c) => c[0]), pCats.map((c) => c[1]), [0]));

  const sc = stats.strategyCounts;
  const sCats = Object.keys(STRATEGY_CN).map((k) => [STRATEGY_CN[k], sc[k] ?? 0]).sort((a, b) => b[1] - a[1]);
  charts.push(hbarChart($('chart-strategy'), sCats.map((c) => c[0]), sCats.map((c) => c[1]), []));

  addEventListener('resize', () => charts.forEach((c) => c.resize()));
}

/* ---------- 账本 ---------- */
const state = { q: '', grades: new Set(), pricing: '', sort: 'biz', all: false };

const hasGTM = (r) => r.pricing.length > 0 || r.ratio != null;

function applyFilters() {
  let rows = DATA.records.filter((r) => state.all || hasGTM(r));
  if (state.q) {
    const q = state.q.toLowerCase();
    rows = rows.filter((r) => r.title.toLowerCase().includes(q) || r.track.toLowerCase().includes(q));
  }
  if (state.grades.size) rows = rows.filter((r) => state.grades.has(r.grade));
  if (state.pricing) rows = rows.filter((r) => r.pricing.includes(state.pricing));
  const key = state.sort;
  rows.sort((a, b) => (b[key] ?? -1) - (a[key] ?? -1));
  filtered = rows;
  page = 0;
  renderTable();
}

function renderTable() {
  const total = filtered.length;
  const pages = Math.max(1, Math.ceil(total / PAGE));
  page = Math.min(page, pages - 1);
  const slice = filtered.slice(page * PAGE, page * PAGE + PAGE);
  $('count-line').textContent = `${total} 件档案`;
  $('empty').hidden = total !== 0;
  $('pg-info').textContent = `第 ${total ? page + 1 : 0} / ${pages} 页`;
  $('pg-prev').disabled = page === 0;
  $('pg-next').disabled = page >= pages - 1;
  $('ledger-body').innerHTML = slice.map((r) => {
    const idx = DATA.records.indexOf(r);
    const ratioCell = r.ratio != null
      ? `<td class="ratio${r.ratio < 3 ? ' low' : ''}">${r.ratio}:1</td>`
      : `<td class="ratio none">—</td>`;
    return `<tr tabindex="0" data-idx="${idx}" role="button" aria-label="调阅 ${esc(r.title)}">
      <td><span class="stamp stamp-${esc(r.grade)}" aria-label="等级 ${esc(r.grade)}">${esc(r.grade)}</span></td>
      <td><div class="ttl">${esc(r.title)}</div><div class="sub">${esc(r.pricingText ?? '（无收费模式档案）')}</div></td>
      <td class="trk">${esc(r.track)}</td>
      <td class="score">${fmt2(r.biz)}</td>
      ${ratioCell}
      <td class="pg">${folioNo(r.id)}</td>
    </tr>`;
  }).join('');
}

function bindLedger() {
  applyFilters();
  $('q').addEventListener('input', (e) => { state.q = e.target.value.trim(); applyFilters(); });
  document.querySelectorAll('.grade-toggle').forEach((b) =>
    b.addEventListener('click', () => {
      const g = b.dataset.g;
      const on = b.getAttribute('aria-pressed') === 'true';
      b.setAttribute('aria-pressed', String(!on));
      on ? state.grades.delete(g) : state.grades.add(g);
      applyFilters();
    }));
  $('f-pricing').addEventListener('change', (e) => { state.pricing = e.target.value; applyFilters(); });
  $('f-sort').addEventListener('change', (e) => { state.sort = e.target.value; applyFilters(); });
  $('f-all').addEventListener('change', (e) => { state.all = e.target.checked; applyFilters(); });
  $('pg-prev').addEventListener('click', () => { page--; renderTable(); });
  $('pg-next').addEventListener('click', () => { page++; renderTable(); });
  $('clear-filters').addEventListener('click', () => {
    state.q = ''; state.grades.clear(); state.pricing = ''; state.all = false;
    $('q').value = ''; $('f-pricing').value = ''; $('f-all').checked = false;
    document.querySelectorAll('.grade-toggle').forEach((b) => b.setAttribute('aria-pressed', 'false'));
    applyFilters();
  });
  $('ledger-body').addEventListener('click', (e) => {
    const tr = e.target.closest('tr[data-idx]');
    if (tr) openDrawer(tr);
  });
  $('ledger-body').addEventListener('keydown', (e) => {
    if (e.key !== 'Enter' && e.key !== ' ') return;
    const tr = e.target.closest('tr[data-idx]');
    if (tr) { e.preventDefault(); openDrawer(tr); }
  });
  $('d-close').addEventListener('click', closeDrawer);
  $('scrim').addEventListener('click', closeDrawer);
  addEventListener('keydown', (e) => { if (e.key === 'Escape') closeDrawer(); });
}

function openDrawer(tr) {
  const r = DATA.records[Number(tr.dataset.idx)];
  if (!r) return;
  lastFocus = tr;
  $('d-folio').textContent = folioNo(r.id);
  $('d-title').textContent = r.title;
  $('d-track').textContent = `${r.track} · 等级 ${r.grade}`;
  $('d-biz').textContent = fmt2(r.biz);
  $('d-market').textContent = fmt2(r.market);
  $('d-overall').textContent = fmt2(r.overall);
  $('d-ratio').textContent = r.ratio != null ? `${r.ratio}:1` : '—';
  $('d-tags').innerHTML = [...r.pricing.map((p) => PRICING_CN[p]), ...r.strategies.map((s) => STRATEGY_CN[s])]
    .map((t) => `<span class="tag">${esc(t)}</span>`).join('') || '<span class="tag">无 GTM 标签</span>';
  const dl = $('d-dossier');
  if (r.bizRaw) {
    const entries = [];
    for (const line of r.bizRaw.split('\n')) {
      const m = line.match(/^-\s*([^：:]{2,24})[：:]\s*(.+)$/);
      if (m) entries.push(`<dt>${esc(m[1])}</dt><dd>${esc(m[2])}</dd>`);
    }
    dl.innerHTML = entries.join('') || `<dd>${esc(r.bizRaw.slice(0, 400))}</dd>`;
  } else {
    dl.innerHTML = '<dd>该档案源文档无「商业模式 BIZ」章节。</dd>';
  }
  const src = $('d-src');
  src.href = encodeURI(`../${r.track}/${r.id}.md`);
  src.textContent = `源文档 ${r.track}/${r.id}.md →`;
  $('drawer').classList.add('open');
  $('scrim').classList.add('on');
  $('d-close').focus();
}
function closeDrawer() {
  if (!$('drawer').classList.contains('open')) return;
  $('drawer').classList.remove('open');
  $('scrim').classList.remove('on');
  lastFocus?.focus();
}

function reveal() {
  const io = new IntersectionObserver((es) => {
    for (const e of es) if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); }
  }, { threshold: 0.12 });
  document.querySelectorAll('.rv').forEach((el) => io.observe(el));
}

main();
