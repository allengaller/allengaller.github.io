#!/usr/bin/env node
// GTM 数据提取：遍历 AI+*/ 源文档，解析「商业模式 BIZ」章节的结构化 GTM 字段，
// 与 docs/data/ideas.json 关联，输出 GTM/data/gtm.json。所有数字可溯源到源文档。
import fs from 'node:fs';
import path from 'node:path';

const ROOT = process.cwd();
const OUT = path.join(ROOT, 'GTM', 'data', 'gtm.json');

const BIZ_RE = /###\s*4\.\s*商业模式\s*BIZ[^\n]*\n([\s\S]*?)(?=\n###\s*5\.|\n##\s[^#]|\n##\s*$|$)/;

const PRICING_RULES = [
  ['subscription', /订阅|SaaS|会员制|按月|按年|seat|per seat|\/月|\/年|\/人/i],
  ['usage', /按量|用量|按调用|API调用|API 调用|按次|计量|token/i],
  ['take_rate', /抽成|佣金|分成|GMV|交易额|take rate/i],
  ['project', /项目制|定制|私有化|买断|license| Licence|硬件|一次性|实施/i],
  ['freemium', /免费增值|freemium|基础免费|免费版|开源/i],
  ['ads', /广告/i],
];
const STRATEGY_RULES = [
  ['plg', /PLG|产品驱动|自助服务|self-?serve|病毒|自传播/i],
  ['sales', /销售驱动|直销|大客户|\bKA\b|地推|\bBD\b|电销|销售团队/i],
  ['content', /内容营销|社区|SEO|KOL|自媒体|直播|私域|口碑/i],
  ['channel', /渠道|代理|经销|集成商|合作伙伴|战略合作/i],
  ['trial', /免费试用|free trial|试用转化/i],
];

function field(block, nameRe) {
  const m = block.match(new RegExp('(?:' + nameRe + ')[^\\n：:]*[）)]?\\s*[：:]\\s*([^\\n]+)'));
  return m ? m[1].trim() : null;
}
function matchAll(rules, text) {
  const hits = [];
  for (const [key, re] of rules) if (re.test(text)) hits.push(key);
  return hits;
}
function extractRatio(block) {
  const pats = [
    /LTV\s*\/\s*CAC[^：:\n]*[：:]\s*(?:约|≈|>=?|≥)?\s*([0-9]+(?:\.[0-9]+)?)/i,
    /LTV\/CAC\s*(?:比值)?\s*(?:约|≈|>=?|≥|=)\s*([0-9]+(?:\.[0-9]+)?)/i,
    /LTV\s*\/\s*CAC\s*(?:约为?|≈|>=?|≥|=)\s*([0-9]+(?:\.[0-9]+)?)/i,
  ];
  for (const p of pats) {
    const m = block.match(p);
    if (m) {
      const v = parseFloat(m[1]);
      if (v > 0 && v <= 200) return v;
    }
  }
  return null;
}
const median = (a) => {
  if (!a.length) return null;
  const s = [...a].sort((x, y) => x - y);
  const m = Math.floor(s.length / 2);
  return s.length % 2 ? s[m] : (s[m - 1] + s[m]) / 2;
};
const mean = (a) => (a.length ? a.reduce((s, x) => s + x, 0) / a.length : null);
const r1 = (v) => (v == null ? null : Math.round(v * 100) / 100);

const ideas = JSON.parse(fs.readFileSync(path.join(ROOT, 'docs', 'data', 'ideas.json'), 'utf8'));
const list = Array.isArray(ideas) ? ideas : ideas.ideas;
const byId = new Map(list.map((it) => [it.id, it]));

const tracks = fs.readdirSync(ROOT).filter((d) => d.startsWith('AI+') && fs.statSync(path.join(ROOT, d)).isDirectory());
const files = [];
for (const t of tracks) {
  for (const f of fs.readdirSync(path.join(ROOT, t)).filter((f) => f.endsWith('.md'))) {
    files.push(path.join(ROOT, t, f));
  }
}

const coverage = { files: files.length, bizSection: 0, pricing: 0, ratio: 0, moat: 0, strategy: 0 };
const records = [];
const ratioValues = [];
const pricingCounts = {};
const strategyCounts = {};

for (const file of files) {
  const id = path.basename(file, '.md');
  const meta = byId.get(id);
  if (!meta) continue;
  const src = fs.readFileSync(file, 'utf8');
  const m = src.match(BIZ_RE);
  const rec = {
    id,
    title: meta.title,
    track: meta.track,
    grade: meta.grade,
    overall: meta.overallScore,
    biz: meta.dimensions?.biz ?? null,
    market: meta.dimensions?.market ?? null,
    pricing: [],
    strategies: [],
    ratio: null,
    pricingText: null,
    arpu: null,
    ltv: null,
    cac: null,
    moat: null,
    bizRaw: null,
  };
  if (m) {
    coverage.bizSection++;
    rec.bizRaw = m[1].trim();
    rec.pricingText = field(m[1], '收费模式');
    rec.arpu = field(m[1], '预估客单价|客单价');
    rec.ltv = field(m[1], 'LTV');
    rec.cac = field(m[1], 'CAC');
    rec.moat = field(m[1], '护城河');
    rec.pricing = rec.pricingText ? matchAll(PRICING_RULES, rec.pricingText) : [];
    if (rec.pricing.length) {
      coverage.pricing++;
      for (const p of rec.pricing) pricingCounts[p] = (pricingCounts[p] || 0) + 1;
    }
    rec.strategies = matchAll(STRATEGY_RULES, m[1]);
    if (rec.strategies.length) {
      coverage.strategy++;
      for (const s of rec.strategies) strategyCounts[s] = (strategyCounts[s] || 0) + 1;
    }
    rec.ratio = extractRatio(m[1]);
    if (rec.ratio != null) {
      coverage.ratio++;
      ratioValues.push(rec.ratio);
    }
    if (rec.moat) coverage.moat++;
  }
  records.push(rec);
}

const dims = ['pain', 'market', 'solution', 'biz', 'compete', 'feasibility'];
const dimMeans = {};
for (const d of dims) dimMeans[d] = r1(mean(list.map((i) => i.dimensions?.[d]).filter((v) => typeof v === 'number')));

const weakest = {};
for (const it of list) {
  const ks = dims.filter((k) => typeof it.dimensions?.[k] === 'number');
  if (!ks.length) continue;
  const min = Math.min(...ks.map((k) => it.dimensions[k]));
  for (const k of ks.filter((k) => it.dimensions[k] === min)) weakest[k] = (weakest[k] || 0) + 1;
}

const byGrade = {};
for (const g of ['S', 'A', 'B', 'C', 'D']) {
  const sub = list.filter((i) => i.grade === g);
  if (!sub.length) continue;
  byGrade[g] = {
    n: sub.length,
    bizMean: r1(mean(sub.map((i) => i.dimensions?.biz).filter((v) => typeof v === 'number'))),
    marketMean: r1(mean(sub.map((i) => i.dimensions?.market).filter((v) => typeof v === 'number'))),
    overallMean: r1(mean(sub.map((i) => i.overallScore).filter((v) => typeof v === 'number'))),
  };
}

const byTrack = {};
for (const it of list) {
  if (typeof it.dimensions?.biz !== 'number') continue;
  (byTrack[it.track] = byTrack[it.track] || []).push(it.dimensions.biz);
}
const trackProfiles = Object.entries(byTrack)
  .filter(([, a]) => a.length >= 10)
  .map(([track, a]) => ({ track, n: a.length, bizMean: r1(mean(a)) }))
  .sort((x, y) => y.bizMean - x.bizMean);

const RATIO_BUCKETS = [
  ['<1', (v) => v < 1],
  ['1–3', (v) => v >= 1 && v < 3],
  ['3–5', (v) => v >= 3 && v < 5],
  ['5–10', (v) => v >= 5 && v < 10],
  ['10–30', (v) => v >= 10 && v < 30],
  ['30+', (v) => v >= 30],
];
const ratioHistogram = RATIO_BUCKETS.map(([label, fn]) => ({ label, n: ratioValues.filter(fn).length }));
const ratioGe3 = ratioValues.filter((v) => v >= 3).length;

const out = {
  meta: {
    generatedAt: new Date().toISOString(),
    sources: { ideas: list.length, markdown: files.length },
    coverage,
    note: '所有字段由 GTM/build.js 从 AI+*/ 源文档「### 4. 商业模式 BIZ」章节解析；自报数字为语料原文陈述，非本站核实。',
  },
  stats: {
    dimMeans,
    weakest,
    byGrade,
    trackProfiles,
    pricingCounts,
    strategyCounts,
    ratio: { n: ratioValues.length, median: median(ratioValues), ge3: ratioGe3, histogram: ratioHistogram },
  },
  records,
};

fs.mkdirSync(path.dirname(OUT), { recursive: true });
fs.writeFileSync(OUT, JSON.stringify(out, null, 1));
console.log('records', records.length, 'coverage', JSON.stringify(coverage));
console.log('pricing', JSON.stringify(pricingCounts));
console.log('strategies', JSON.stringify(strategyCounts));
console.log('ratio n=' + ratioValues.length, 'median', median(ratioValues), 'ge3', ratioGe3, 'histogram', JSON.stringify(ratioHistogram));
