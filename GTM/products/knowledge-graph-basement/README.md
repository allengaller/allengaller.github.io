# GTM — knowledge-graph-basement

> 单文件落地页：`GTM/index.html`（无构建、无依赖，双击即开；`graph-data.json` 是页面内嵌数据的源文件）。
> 本文档记录页面遵循的 GTM 最佳实践、渠道计划与衡量指标。

---

## 1. 定位（Positioning）

**一句话**：把任意 Markdown 文件夹变成知识的活地图——一条命令，十六种视角，数据不出本机。

**定位声明模板**（Geoffrey Moore, *Crossing the Chasm*）：

> 对于**拥有 200+ 笔记的 Obsidian / LLM-wiki 用户**（目标客户），
> **knowledge-graph-basement** 是一个**静态知识图谱生成器**（产品类别），
> 它能**把语料的真实结构渲染成 16 种可视化，并输出可发布的静态站点**（核心收益）。
> 与 **Obsidian graph view** 不同（主要竞品），我们的图谱**可分享、可查询、可被 LLM 读取**（关键差异）。

**三条信息主线**（messaging pillars，页面内容按此组织）：

| 支柱 | 用户语言 | 页面对应 |
|---|---|---|
| 看见结构 | "我写了 1000 条笔记，这个月只重读过 3 条" | Problem 三卡片 + punch line |
| 一个索引，十六种视角 | "不是又一个花瓶图，是能回答不同问题的镜头" | 16 views 网格 |
| 数据主权 | "零配置、纯静态、你的笔记不搬家" | How it works + FAQ 第一条 |

## 2. 目标客户（ICP）与任务（JTBD）

| 画像 | JTBD（待完成任务） | 触达渠道 |
|---|---|---|
| Obsidian 重度用户（200+ 笔记） | 看清花园里哪里茂密、哪里荒废 | r/Obsidian、PKM Discord、少数派 |
| LLM-wiki / AI agent 构建者 | 给 agent 提供结构化上下文，而非向量碎片 | Show HN、Twitter/X AI 圈、即刻 |
| 研究/写作团队 | 让 docs 文件夹的覆盖与盲区在站会上可见 | LinkedIn、HN、Indie Hackers |
| 教育/课程设计者 | 上课前看清课程概念是否成网 | 教育技术社区、HN |

页面 "Who it's for" 一节即按此自认证分流——访客对号入座后转化率显著高于通用文案。

## 3. 页面 ↔ 最佳实践映射

| 区块 | GTM 实践 |
|---|---|
| Hero | 3 秒内回答"这是什么、给谁、下一步做什么"；主 CTA 唯一（waitlist） |
| Hero 活体图谱 | Show, don't tell：页面本身就是产品 demo（数据为真实语料子图：101 节点 / 111 边 / 8 簇，提取自 `data/index.json`） |
| Stats band | 可量化证明；数字全部真实（226 文档 / 226 链接，来自 `data/meta.json`） |
| Problem | 痛点用用户语言复述（agitation），再给出转折句 |
| How it works | 3 条**真实存在**的命令（bootstrap / index / dev），消除"又要折腾"的顾虑 |
| 16 views | 展示广度护城河；LIVE/NEXT 徽章**诚实标注**4 个已上线、12 个在路线图 |
| Who it's for | ICP 分流自认证 |
| 对比表 | 与 Obsidian graph view / Gephi / grep 正面差异（只说事实，不贬损） |
| Pricing | 核心开源免费打消顾虑（MIT），Cloud 为唯一付费转化点；early-bird "锁价" 制造合理稀缺 |
| FAQ | 异议处理顺序 = 信任门槛顺序：隐私 → 兼容 → 规模 → 价格 → 路线图 → 现在能用吗 |
| Final CTA | 单一转化目标贯穿全页（waitlist），风险逆转承诺（"one email, no spam"） |

**诚实性边界**（上线前必须知晓）：

- Pricing 为**计划价**，页面已标注 "pre-launch"；表单为**纯前端演示**（本地成功态，无后端收集）。接入真实收集前建议接 Formspree / Tally / 自建 endpoint。
- "16 views" 中 4 个已上线（force-graph / timeline / calendar / treemap），页面用徽章如实区分。
- 品牌名在页面上用短名 "graph basement"，仓库名与 GitHub 链接保持一致。

## 4. 渠道与发布节奏（Channel plan）

**发布前**（本周）：
1. 表单接后端（Tally / Formspree，10 分钟），或先换成 mailto。
2. 页面部署到 Netlify（仓库已有 `netlify.toml`；`GTM/` 可作为独立 site 拖入 Netlify Drop）。
3. 接入极简统计（Plausible / Umami，比 GA 更符合"无遥测"人设——只统计 PV 与转化，不追踪个体）。

**发布日**（T-day）：
- **Show HN**（首选渠道，标题即定位句："Show HN: I turned my Markdown notes into 16 living graphs"），附 live demo 链接。周二–周四，美东上午发。
- **Reddit** r/Obsidian + r/PKMS：语气改为分享经验（"I built this because my 400-note vault felt dead"），防营销感。
- **Product Hunt**：备好 3 张 GIF（力导向图 / treemap / 日历热图），tagline 用 hero 副标题。
- **中文圈**：少数派、V2EX /create、即刻 PKM 圈。

**发布后**（T+1 ~ T+30）：
- 每个渠道一个 UTM：`?utm_source=hn&utm_campaign=launch`（页面不改也能用）。
- 把 16 views 网格里每个 NEXT 视图的上线做成单独的更新帖（4 次免费返场流量）。

## 5. 衡量（KPIs）

| 指标 | 基准（waitlist 落地页） | 动作阈值 |
|---|---|---|
| 访客 → waitlist 转化率 | 8–15%（工具类 waitlist 页经验区间） | < 5%：先改 hero 副标题，再改首图 |
| Hero 主 CTA 点击率 | ≥ 30% | < 20%：价值主张不清晰，A/B 两版 H1 |
| 滚动到 Pricing 的比例 | ≥ 50% | 低：说明中段流失，砍 Problem 篇幅 |
| FAQ 展开率 | ≥ 25% | 高展开+低转化 = 定价/隐私异议未解，改 FAQ 或定价 |
| Show HN 帖 upvote→访问率 | 观察值 | — |

埋点最小集：`cta_hero_click`、`cta_nav_click`、`cta_pricing_click`、`wl_submit`、`scroll_depth(50/75/100)`。

## 6. 实验 backlog（按优先级）

1. H1 A/B：「Your notes already are a graph.」 vs 「1000 notes in. 3 re-read this month.」
2. Hero 右侧活体图谱 → 换成录屏 demo（更直白，但失去"页面即产品"的巧思）。
3. 增加"它看起来长这样"截图墙（等 MVP2 视图上线后）。
4. Waitlist 排名机制（"你在第 N 位"）提升分享率。
5. SEO：为 16 个视图各建一篇文档页（`/views/force-graph/`），长尾承接。

## 7. 本地预览

```bash
cd GTM
python3 -m http.server 8080   # 或直接双击 index.html（无外部请求依赖，仅字体走 CDN）
```
