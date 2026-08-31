# mcp4coder GTM 策略（GTM Page 背后的框架）

> 本目录是对外转化用 GTM 落地页及其策略依据。页面入口：[`index.html`](index.html)

---

## 1. 定位声明（Positioning Statement)

> **对于** 需要为 AI Agent 接入多个外部工具的团队，**mcp4coder** 是一个**自托管 MCP Server 统一框架**，它把 37 个 Server / 200+ Tools 收敛进一套代码库，内置 Web 管理、工作流编排与企业级安全。**与** 逐个安装社区 MCP Server **不同**，mcp4coder 用统一基类（`BaseMCPServer`）接管 Server 全生命周期，把「每接一个工具」的边际成本从"周"压到"小时"。

一句话主信息（页面 Hero）：
**「37 Servers. One Framework. 零胶水代码。」**

## 2. 目标客户分层（ICP Segmentation）

| 分层 | 画像 | 核心痛点 | 页面主张 | 首选转化动作 |
|------|------|----------|----------|--------------|
| **ICP-A** AI 应用工程师 | 写 Agent / Copilot，追求接入速度 | 逐个接 MCP、协议适配繁琐 | 一次接入 200+ Tools | Quickstart clone |
| **ICP-B** 平台 / 基础设施团队 | 对安全边界、数据主权、可观测性负责 | 密钥失控、黑盒运行、无审计 | 自托管 + 统一认证 + 健康检查 | 看架构 / 部署文档 |
| **ICP-C** 独立开发者 & 创业者 | 要交付速度，预算敏感 | 自建工具链耗时数周 | MIT 免费、拿来即用 | Clone / Star |

## 3. 信息屋（Messaging House）

**屋顶（核心承诺）**：一套框架，统管全部 MCP Server。

**四根支柱（对应页面 SEC.02）**：
1. **统一抽象** — `BaseMCPServer`：新增 Server = 实现 2 个方法
2. **可视化运维** — `/ui` 管理界面 + 健康检查 + Swagger 自动文档
3. **编排与异步** — 可视化工作流设计器 + Celery/Redis
4. **安全与交付** — JWT + API Key 双认证、E2B 沙箱、Docker 自托管

**地基（信任证据，全部为项目事实，不虚构数据）**：
- 37 个 Server、200+ Tools、13 个场景类目（页面含完整可验收目录）
- MIT License；FastAPI + Celery + Redis 技术栈；生产强制 `JWT_SECRET_KEY`

## 4. 页面叙事结构（= GTM 最佳实践对照）

| 页面区块 | GTM 实践 |
|----------|----------|
| 公告条 + 导航 CTA | 常设转化入口（开源/自托管/规模三个信任词） |
| Hero：主张 + 双 CTA + 终端演示 + 指标条 | 8 秒内说清 What/Why/For Whom；产品演示即信任 |
| SEC.01 痛点 | Problem-Agitate：先讲"你的 Agent 不缺工具，缺管理" |
| SEC.02 能力 Bento | Features → Benefits 翻译（每个能力配一段代码/命令证据） |
| SEC.03 三类 ICP 卡 | Segmentation：访客自我识别，各取转化路径 |
| SEC.04 37 Server 目录 | Proof-of-Substance：宣称可验证，反"营销空话" |
| SEC.05 对比表 | Differentiation + 决策临界点提示（>5 个工具时框架胜出） |
| SEC.06 Quickstart | Activation：把上手摩擦压到 3 条命令 |
| SEC.07 FAQ | Objection Handling：区别/安全/门槛/License/按需启用/接入 |
| Final CTA | 情绪收口 + 最低摩擦动作（一行 clone 命令） |

**红线**：不虚构用户数、Star 数、客户证言；所有数字均可回溯到 README。

## 5. 转化路径与衡量（Metrics）

**主转化**：GitHub 访问（Star/Fork）· **次转化**：Quickstart 执行（clone → pip install → 启动）

| 漏斗层 | 指标 | 采集方式（建议） |
|--------|------|------------------|
| 到达 | UV / 跳出率 | 站点分析（Plausible/GA） |
| 兴趣 | Hero CTA 点击率、目录区停留 | 事件埋点（data-gtm 属性） |
| 意向 | GitHub 外链点击、FAQ 展开数 | 外链点击埋点 |
| 激活 | clone 后 `/health` 首次 200 | 项目侧匿名计数（opt-in） |

## 6. 渠道与动作（Channel Playbook，首季度）

1. **GitHub 即渠道**：README 头部挂 GTM 页链接；Topics 优化（`mcp` / `model-context-protocol` / `ai-agents`）
2. **开发者社区**：MCP 官方 servers 目录提交、V2EX / 掘金 / 知乎「37 Server 实测」技术长文（目录区即素材）
3. **搜索意图**：页面 meta 针对「MCP Server 集合 / MCP 管理平台 / self-host MCP」类关键词
4. **场景内容**：每类 ICP 一篇 use case（Agent 工具链 10 分钟接入 / 平台团队安全清单 / 创业者产品底座）
5. **节奏**：每个 Server 新增/大版本 = 一次公告条更新 + 一轮社区分发（页面 `V2026.8` 字段随之滚动）

## 7. 维护约定

- 数字（Server 数 / Tool 数 / 类目数）变更时，同步更新 Hero 指标条、目录区和本文件
- 新增 FAQ 由 GitHub Issues 高频问题驱动，每月回顾一次
