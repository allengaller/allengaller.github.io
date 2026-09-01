# Product

<!-- impeccable:product-schema 1 -->

<!-- 注意：本文件由 impeccable init 在提问通道不可用时推断写入（2026-08-29），
     依据站点既有内容（_config.yml、index.html frontmatter/JSON-LD）与 GitHub 仓库调研。
     标注 [inferred] 的事实未经用户当面确认，可随时修正。 -->

## Platform

web

## Stack

Jekyll 静态站点（kramdown/GFM，GitHub Pages 部署），原生 HTML + 单文件 `assets/css/main.css` 设计系统，零框架、零构建步骤。[inferred]

## Users

- **潜在合作方/客户**：评估技术顾问、工具共创、知识产品化合作的技术决策者。[inferred]
- **招聘方**：判断强项、战绩与适配岗位的工程管理者。
- **开发者与技术粉丝**：查看开源工具与知识资产的使用者、贡献者。
- **内容读者**：经由内容矩阵（播客、专题、链接页）进入的受众。

## Product Purpose

Allen Galler 曹亚仑的个人品牌总入口：聚合 80+ 开源仓库、4500+ 知识文档与内容矩阵，把技术经验呈现为可复用工具、可增长知识资产与可长期经营的个人品牌。成功 = 访客在数秒内理解三重身份并找到自己的入口（合作/招聘/开源/内容）。

## Positioning

在 Cloud Native、AI Tooling、Knowledge Architecture 三者交叉地带持续产出的独立开源作者。邻居产品无法复制的差异：以 SRE 生产级深度为信任基石（Kudig 70+ 分析器、EtcdGuardian Operator），同时把方法论沉淀为 "-database" 知识库范式（既是人读手册，也是 Agent RAG 语料），并独立产品化为工具矩阵（me-os、nerd-portal、LeetCast 等）。

## Operating Context

访客从 GitHub、搜索引擎、社交链接进入；页面须同时服务中文与国际受众（zh-CN 为主，技术术语保留英文）。Jekyll + GitHub Pages，无后端；所有链接为静态出站。

## Capabilities and Constraints

- 静态页面，无服务端；交互限于原生 JS（滚动揭示、滚动进度）。
- 必须继承既有设计系统（main.css tokens：纸白/墨色/陶土红强调、Fraunces/Geist/JetBrains Mono、明暗自动双模式）。
- 数据资产：`_data/repos.json`、`_data/repos-detailed.json` 含全部仓库索引。
- 未决：联系邮箱等转化终点（页面中不得虚构联系方式）。

## Brand Commitments

- 名称：Allen Galler 曹亚仑。
- 定位短语：Cloud Native SRE · AI Toolsmith · Knowledge Architect（站点 tagline，全站一致）。
- 声音：高产开源黑客；编辑感 × 技术感（Editorial × Technical），克制、有证据、不浮夸。
- 命名体系：`*-database` = 知识库，`*-global` = 品牌产品线，组织有 kudig-io、standup-coder、ai-guru-global、opendemo-work 等。

## Evidence on Hand

- 代表项目（首页已展示，均真实）：ResolveAgent（AIOps Agent）、Kudig（K8s 节点诊断，70+ 分析器 + eBPF）、EtcdGuardian（etcd 备份 Operator）、LeetCast（AI 对话式刷题播客）、mcp4coder（MCP 工具生态）、OpenDemo（518+ 技术演示）。
- 数字（站点已公开）：4500+ 文档与知识资产、10+ 开源工具、5+ 年云原生实践。
- 仓库全索引：`_data/repos.json` / `_data/repos-detailed.json`、`/repos/` 页面。
- 缺失：真实客户证言、付费案例、联系方式邮箱 — 不得虚构，需要用户提供。

## Product Principles

1. 证据先于主张：每个能力声明必须落到可验证的仓库、数字或工件。
2. 三重身份一个叙事：SRE 深度建立信任，AI 工具化展示前瞻，知识架构证明可持续。
3. 知识即产品：知识库不是文档附属，而是与工具同级的产品线。
4. 克制的密度：信息量大但排版编辑化，不用装饰性元素填充。
