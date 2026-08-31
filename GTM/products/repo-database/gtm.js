/* GTM — The Departure Board: flap rotation (real catalog data),
   station clock, zh/en switch. Zero dependencies. */

const BOARD_DATA = {
  "ai-engineering": [
    { n: "anomalyco/opencode", s: 197000 },
    { n: "anthropics/skills", s: 172107 },
    { n: "garrytan/gstack", s: 127000 },
    { n: "unslothai/unsloth", s: 69000 }
  ],
  "ai-agents": [
    { n: "openclaw/openclaw", s: 380000 },
    { n: "NousResearch/hermes-agent", s: 216000 },
    { n: "Shubhamsaboo/awesome-llm-apps", s: 134515 },
    { n: "bytedance/deer-flow", s: 70000 }
  ],
  "interview-career": [
    { n: "jwasham/coding-interview-university", s: 359685 },
    { n: "trekhleb/javascript-algorithms", s: 196550 },
    { n: "Snailclimb/JavaGuide", s: 158014 },
    { n: "yangshun/tech-interview-handbook", s: 142146 }
  ],
  "fullstack-arch": [
    { n: "donnemartin/system-design-primer", s: 365155 },
    { n: "ByteByteGoHq/system-design-101", s: 87367 },
    { n: "binhnguyennus/awesome-scalability", s: 73432 },
    { n: "chaos-mesh/chaos-mesh", s: 7849 }
  ],
  "maas-platform": [
    { n: "vllm-project/vllm", s: 89589 },
    { n: "BerriAI/litellm", s: 56885 },
    { n: "langfuse/langfuse", s: 33496 },
    { n: "sgl-project/sglang", s: 32213 }
  ],
  "ai-mental-health": [
    { n: "Emo-gml/PsyLLM", s: 51 },
    { n: "UKPLab/arxiv2026-graph2counsel", s: 3 },
    { n: "coding-groot/cactus", s: 45 },
    { n: "AIwithhassan/safespace-ai-therapist", s: 8 }
  ],
  "creative-coding": [
    { n: "terkelg/awesome-creative-coding", s: 15121 },
    { n: "openframeworks/openFrameworks", s: 10409 },
    { n: "nannou-org/nannou", s: 6733 },
    { n: "gcui-art/suno-api", s: 3133 }
  ],
  "culture-arts": [
    { n: "chinese-poetry/chinese-poetry", s: 52975 },
    { n: "meetqy/aspoem", s: 2868 },
    { n: "LingDong-/cope", s: 479 },
    { n: "dh-tech/awesome-digital-humanities", s: 396 }
  ],
  "mind-philosophy": [
    { n: "SecurityRonin/alaya", s: 13 },
    { n: "dosanko-tousan/Gemini-Abhidhamma-Alignment", s: 3 },
    { n: "Greatbeing/Yogacara", s: 1 },
    { n: "FrankNavratil/buddhist-psychology-course", s: 1 }
  ],
  "mindfulness-apps": [
    { n: "giekaton/vipassana-app", s: 9 },
    { n: "happyruss/vipassana_android", s: 4 }
  ]
};

const REDUCED_MOTION = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

/* ---- Flap rotation ---- */

const fmt = (n) => n.toLocaleString("en-US");

document.querySelectorAll(".brow").forEach((row, rowIdx) => {
  const line = row.dataset.line;
  const items = BOARD_DATA[line];
  if (!items || items.length < 2) return;

  const flap = row.querySelector(".flap");
  const nameEl = row.querySelector(".flap-name");
  const starsEl = row.querySelector(".r-stars");
  let idx = 0;

  const swap = () => {
    idx = (idx + 1) % items.length;
    nameEl.textContent = items[idx].n;
    starsEl.textContent = fmt(items[idx].s);
  };

  if (REDUCED_MOTION) {
    setInterval(swap, 6000);
    return;
  }

  setInterval(() => {
    flap.classList.remove("flipping");
    void flap.offsetWidth;
    flap.classList.add("flipping");
    setTimeout(swap, 250);
  }, 4000 + rowIdx * 350);
});

/* ---- Station clock ---- */

const clockTime = document.getElementById("clockTime");
const clockDate = document.getElementById("clockDate");
const pad = (n) => String(n).padStart(2, "0");

function tickClock() {
  const now = new Date();
  clockTime.textContent = `${pad(now.getHours())}:${pad(now.getMinutes())}:${pad(now.getSeconds())}`;
  clockDate.textContent = now.toLocaleDateString("en-CA", { year: "numeric", month: "short", day: "2-digit" });
}
tickClock();
setInterval(tickClock, REDUCED_MOTION ? 30000 : 1000);

/* ---- Language switch ---- */

const I18N = {
  zh: {
    "h1main": "机器排万仓，人工留 117。",
    "h1sub": "Machine-ranked thousands, human-kept 117.",
    "brandSub": "GitHub 宝藏仓库",
    "lede": "四路数据源每月聚合 1000+ 仓库，经过评分、评审、CI 校验——最后钉在这块板上的，是真正值得你时间的 117 篇档案。",
    "boardTitle": "出发时刻",
    "boardService": "每月发车 · MONTHLY SERVICE",
    "boardUpdated": "数据截至 2026-08",
    "boardFoot": "每一行都是 catalog 真实档案 · 板上翻牌每 4 秒轮换一次",
    "ctaStar": "Star on GitHub",
    "ctaStarSub": "收藏这座正在发车的档案库",
    "ctaIndex": "浏览 117 篇档案 →",
    "howTitle": "机器时刻表",
    "flow1T": "四路抓取",
    "flow1P": "Awesome 榜单 ×8、GitHub Search API、Hacker News、DEV.to，由 scripts/scrape.py 每月聚合。",
    "flow2T": "评分排序",
    "flow2P": "stars + forks + 参与度 + 增长势头 ×10 + 提交活跃 ×2——势头信号用真实 commit 数据校准。",
    "flow3T": "人工评审",
    "flow3P": "值得留下的仓库逐个手写六段式档案：技术栈、特性、场景、个人评价、关联资源。",
    "flow4T": "CI 放行",
    "flow4P": "catalog.py validate 强制校验字段、文件名与内链，月度工作流自动刷新 stars 与索引。",
    "formulaT": "综合得分",
    "formulaNote": "公式原样来自 README——机器只负责把队列排出来，进不进库由人说了算。",
    "wfCap": "月度自动化的四班列车",
    "wfHead1": "班次", "wfHead2": "发车时刻", "wfHead3": "任务",
    "wf1": "全量四源抓取，提交 repos.json",
    "wf2": "增量抓取 + refresh + 重建索引",
    "wf3": "web/ 发布 GitHub Pages",
    "noticesTitle": "站长告示",
    "noticesLede": "档案不是摘要生成的，是一篇一篇写出来的。三张告示，直接从 catalog 里钉上来。",
    "nc1": "跨 13+ 编码 agent harness 的「方法论技能包」——把 brainstorming / TDD / systematic-debugging 等工程实践装成可被任何 harness 加载的 SKILL.md，~28k stars，harness 工程的标杆方法论库。",
    "nc2": "转行软件工程师的自学路线图，把 CS 核心课程压缩成一份可执行的数月学习计划——README 置顶阅读清单的总路线图。",
    "nc3": "PagedAttention 起家的高吞吐 LLM 推理引擎，事实上的 MaaS 平台推理层标准底座——十个 MaaS 档案里第一个写完的。",
    "ncLink": "阅读完整档案 →",
    "lineageTitle": "范式谱系",
    "lineageLede": "catalog/_lineage/ 追踪五个范式的来龙去脉：谁首创、谁衍生、谁混血。像查线路图一样查一个想法的祖先。",
    "cousinNote": "同期表亲 · 独立演化",
    "lgOrigin": "范式源头", "lgDeriv": "catalog 内衍生品", "lgCousin": "同期表亲（独立演化）",
    "gateTitle": "发车前检查",
    "gate1T": "schema 校验",
    "gate1P": "8 个必填 frontmatter 字段缺失即非零退出：name、url、domain、type、discovered、updated、rating、summary。",
    "gate2T": "文件名规范",
    "gate2P": "只取 repo 部分，小写、下划线转连字符——Project-HAMi/HAMi 必须落成 hami.md。",
    "gate3T": "内链可达",
    "gate3P": "正文里每一条指向其他档案的 Markdown 链接都必须解析到真实文件，断链即拦截。",
    "gate4T": "100 个测试用例",
    "gate4P": "scripts / catalog / frontend 三层 pytest 全离线运行，CI 在每次 push 与 PR 上执行。",
    "qsTitle": "自行发车",
    "qsLede": "全部数据随仓库分发，克隆即可离线浏览——无需联网、无需 token。",
    "qs1": "取票 · 克隆与安装",
    "qs2": "检票 · 本地浏览 UI",
    "qs3": "建档 · 生成档案草稿",
    "qsNote": "想要在线版本？Fork 后在 Settings → Pages 选择 GitHub Actions，deploy-pages.yml 会把 web/ 发布到你的 github.io——这座车站随时可以复制。",
    "termLine": "本次列车终点：你的下一个好仓库。",
    "ctaStar2": "Star repo-database",
    "ctaStarSub2": "117 篇档案 · 10 个领域 · 每月发车",
    "footCurated": "人工策展的 GitHub 仓库知识库",
    "footIssues": "报告问题"
  },
  en: {
    "h1main": "Machine-ranked thousands, human-kept 117.",
    "h1sub": "机器排万仓，人工留 117。",
    "brandSub": "GitHub Treasure",
    "lede": "Four data sources aggregate 1,000+ repos every month. After scoring, review, and CI checks, what stays pinned to this board is the 117 profiles actually worth your time.",
    "boardTitle": "出发时刻",
    "boardService": "Monthly service",
    "boardUpdated": "Data as of Aug 2026",
    "boardFoot": "Every row is a real catalog profile · flaps rotate every 4 seconds",
    "ctaStar": "Star on GitHub",
    "ctaStarSub": "Star this repository while it departs",
    "ctaIndex": "Browse all 117 profiles →",
    "howTitle": "机器时刻表",
    "flow1T": "Four-source intake",
    "flow1P": "8 Awesome lists, GitHub Search API, Hacker News, and DEV.to — aggregated monthly by scripts/scrape.py.",
    "flow2T": "Score & rank",
    "flow2P": "stars + forks + engagement + momentum ×10 + commit activity ×2 — momentum grounded in real commit data.",
    "flow3T": "Human review",
    "flow3P": "Repos worth keeping get a hand-written six-section profile: stack, features, use cases, assessment, related resources.",
    "flow4T": "CI clearance",
    "flow4P": "catalog.py validate enforces schema, filenames, and internal links; monthly workflows refresh stars and the index.",
    "formulaT": "综合得分",
    "formulaNote": "The formula, verbatim from the README — the machine ranks the queue, but a person decides what enters the catalog.",
    "wfCap": "Four scheduled services every month",
    "wfHead1": "Service", "wfHead2": "Schedule", "wfHead3": "Mission",
    "wf1": "Full four-source scrape, commits repos.json",
    "wf2": "Incremental fetch + refresh + rebuild index",
    "wf3": "Publishes web/ to GitHub Pages",
    "noticesTitle": "站长告示",
    "noticesLede": "Profiles are not generated summaries — they are written one by one. Three notices, pinned straight from the catalog.",
    "nc1": "A methodology skill pack spanning 13+ coding agent harnesses — brainstorming / TDD / systematic-debugging and more, packaged as SKILL.md any harness can load. ~28k stars; the reference library for harness engineering.",
    "nc2": "A self-study roadmap for switching into software engineering, compressing the CS core into a months-long actionable plan — the master list atop the README reading queue.",
    "nc3": "The high-throughput LLM inference engine that started with PagedAttention — the de-facto serving base of MaaS platforms, and the first of ten MaaS profiles written.",
    "ncLink": "Read the full profile →",
    "lineageTitle": "范式谱系",
    "lineageLede": "catalog/_lineage/ traces five paradigms: who originated them, who derived from them, who hybridized. Look up an idea's ancestors like a transit map.",
    "cousinNote": "cousin · independent evolution",
    "lgOrigin": "Paradigm origin", "lgDeriv": "Derivatives in catalog", "lgCousin": "Cousin (independent evolution)",
    "gateTitle": "发车前检查",
    "gate1T": "Schema check",
    "gate1P": "Missing any of 8 required frontmatter fields fails the build: name, url, domain, type, discovered, updated, rating, summary.",
    "gate2T": "Filename rules",
    "gate2P": "Repo part only, lowercased, underscores to hyphens — Project-HAMi/HAMi must land as hami.md.",
    "gate3T": "Internal links",
    "gate3P": "Every Markdown link to another profile must resolve to a real file; a dead link blocks the build.",
    "gate4T": "100 test cases",
    "gate4P": "Three pytest layers — scripts / catalog / frontend — run fully offline; CI executes on every push and PR.",
    "qsTitle": "自行发车",
    "qsLede": "All data ships with the repository. Clone it and browse offline — no network, no token.",
    "qs1": "Ticket · clone & install",
    "qs2": "Gate · browse the UI locally",
    "qs3": "File · draft a profile",
    "qsNote": "Want it hosted? Fork, then choose GitHub Actions under Settings → Pages — deploy-pages.yml publishes web/ to your github.io. This station is built to be copied.",
    "termLine": "本次列车终点：你的下一个好仓库。",
    "ctaStar2": "Star repo-database",
    "ctaStarSub2": "117 profiles · 10 domains · monthly service",
    "footCurated": "A human-curated GitHub repository knowledge base",
    "footIssues": "Report an issue"
  }
};

const langToggle = document.getElementById("langToggle");
let lang = localStorage.getItem("gtm-lang") || "zh";

function applyLang(next) {
  lang = next;
  document.documentElement.dataset.lang = lang;
  document.documentElement.lang = lang === "zh" ? "zh-CN" : "en";
  const dict = I18N[lang];
  document.querySelectorAll("[data-i18n]").forEach((el) => {
    const v = dict[el.dataset.i18n];
    if (typeof v === "string") el.textContent = v;
  });
  langToggle.textContent = lang === "zh" ? "EN" : "中";
  localStorage.setItem("gtm-lang", lang);
}

langToggle.addEventListener("click", () => applyLang(lang === "zh" ? "en" : "zh"));
applyLang(lang);
