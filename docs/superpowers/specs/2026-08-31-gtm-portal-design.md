# GTM 门户设计 — 汇总所有 Go-to-Market 页面

日期：2026-08-31 · 状态：已批准（用户对话确认）

## 目标

在 `allengaller.github.io` 上提供一个公网入口，汇总用户跨 8 个组织/账号、30+ 个仓库的全部 GTM 页面，任何访客可一站式浏览。

## 决策记录

| 决策点 | 结论 |
|---|---|
| 用途 | 公网发布（非本地工具） |
| 聚合形态 | 统一托管：各仓库 GTM 页面**只读复制**进本仓库，单点部署，不修改源仓库 |
| 私有仓库 | 9 个全部纳入；内容要点已向用户披露并获批准 |
| 入口位置 | `/GTM/` 改造为门户；原个人品牌页迁至 `/GTM/products/allengaller/` |
| 卡片分组 | 按产品域（工具 / 知识库 / 内容与游戏），与个人品牌三重飞轮同构 |

## 架构

```
各仓库 GTM/（只读复制）
   │  _scripts/sync-gtm.py ← _data/gtm-products.json（manifest，唯一事实源）
   ▼
GTM/products/<slug>/        ← 副本提交进本仓库（28 个独立页）
_gtm_docs/<slug>/index.html ← 2 个纯 markdown 战略文档仓库渲染成的页面源
   │  build.py（扩展：静态目录复制 + 动态 docs 页注册 + sitemap 收录）
   ▼
_site/GTM/                  ← index.html 门户（layout 渲染，{{ gtm_cards }} 由 manifest 注入）
_site/GTM/products/<slug>/  ← 产品页原样（不套 layout，保留各自视觉）
```

- 产品页为自包含 HTML（已全量扫描：无绝对路径引用），整目录复制即可工作。
- sync 脚本向每个复制页注入一个固定的「↩ GTM 门户」回链芯片（带标记注释，幂等）。
- 2 个无页面仓库（ai-guru-database、lolipop-database）的 markdown 战略文档用站点现有 markdown 管线渲染成页面，套站点 layout。
- 2 个空目录仓库（awesome-company、make-friends）不纳入。

## 门户页 /GTM/

- 套站点 layout；设计语言沿用主站系统（Fraunces / 纸白墨色 / 陶土红），只加 `.gtmp-*` 新类。
- 结构：开场（总计数 + 论点）→ 置顶特色卡（个人品牌页）→ 三组卡片网格（工具 10 / 知识库 13 / 内容 6）。
- 卡片：产品名、一句话（取自各页 meta description，不编造）、来源组织、`内部` 微标（私有仓库）。
- 全站导航新增 GTM 项；sitemap 自动收录全部 30 个产品页。

## 数据

- manifest：`_data/gtm-products.json`，字段 `slug / repo / name / tagline / group / private / type / source`。
- 新增产品流程：manifest 加一行 → `python3 _scripts/sync-gtm.py` → `python3 _scripts/build.py`。

## 验证

构建零告警；内链检查覆盖全部复制页；30 个产品 URL 全量 curl 200；门户页四视口（桌面/移动 × 明/暗）截图检查；抽查产品页渲染与回链。

## 约束

- 不修改任何源仓库文件（只读复制）。
- 同步幂等：重跑 sync 覆盖副本；副本以本仓库 git 历史为准。
