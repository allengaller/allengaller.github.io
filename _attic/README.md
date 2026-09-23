# _attic — 归档区（不发布）

本目录存放**已从站点下架、但仍需保留原文**的产物。`_scripts/build.py` 不读取这里，
GitHub Pages（Jekyll 与 Actions 两条链路）也不会发布这里，因此内容保留但不对外。

下架原因逐条记录如下，删除一律先移到这里，不直接 rm。

## banners/

首页早期版本给 6 个代表项目各配一张 600×200 抽象 SVG banner。改版后的首页不再引用
`assets/banners/**`（`grep -r "/assets/banners/" _site` 为空），但 `build.py` 仍把 6 个文件
原样复制进 `_site/`，白占 ~28 KB 公开体积。连生成脚本一起归档：

| 归档文件 | 原公开 URL |
|---|---|
| `banners/etcd-guardian.svg` | `https://allengaller.github.io/assets/banners/etcd-guardian.svg` |
| `banners/kudig.svg` | `https://allengaller.github.io/assets/banners/kudig.svg` |
| `banners/leetcast.svg` | `https://allengaller.github.io/assets/banners/leetcast.svg` |
| `banners/mcp4coder.svg` | `https://allengaller.github.io/assets/banners/mcp4coder.svg` |
| `banners/opendemo.svg` | `https://allengaller.github.io/assets/banners/opendemo.svg` |
| `banners/resolve-agent.svg` | `https://allengaller.github.io/assets/banners/resolve-agent.svg` |
| `banners/generate-bunicipals.py` | —（原 `_scripts/generate-bunicipals.py`，不发布） |

若外部仍有热链指向上述 URL，那几条链接会落到 404：把目录 `git mv` 回 `assets/banners/`、
在 `build.py` 的 `STATIC_FILES` 恢复对应 6 行即可，一秒回滚。
脚本的 `BANNER_DIR` 由自身位置推导仓库根，放在这里重跑仍会写回 `assets/banners/`。

顺带一条事实记录：banner 的配色（`#0e0e0e` / `#c8553d` / `#f5f3ee`）早于现有 design token
（`--bg #fcfcfa` / `--accent #b4442c`），即便重新启用也需要按 token 重绘。

## css/

`banners/` 的下架留下的另一半：那 6 张 banner 当初由 `.project-card` 网格渲染，首页改版后
换成了 `.featured-card`（标题 + 一句说明 + 仓库地址行，无图），整套旧组件的 CSS 就再没有
任何页面或镜像引用了。

| 归档文件 | 内容 | 体积 |
|---|---|---|
| `css/main__project-card-list.css` | 原 `assets/css/main.css` 380–545 行（`.project-grid` / `.project-card` / `.project-banner` / `.project-body` / `.project-type` / `.project-tags` / `.project-list` / `.project-item` 及 `.item-main` / `.item-tags` / `.item-arrow`）+ `@media (max-width: 640px)` 里那 3 行 `.project-item` 覆盖 | 4372 B（其中 ~36 B 是本文件抬头说明） |

逐字粘贴回 `assets/css/main.css` 即可恢复，无需改任何页面。原位置留了四行说明注释。

## gtm-private/

`_data/gtm-products.json` 中标记 `"private": true` 的 GTM 产品快照。这些页面本身
面向内部/未公开产品线，不应出现在公开门户，也不应进 sitemap。

| 归档目录 | 来源仓库 | 类型 |
|---|---|---|
| `agent-up/` | ai-guru-global/agent-up | page |
| `fintech-database/` | better-call-saull/fintech-database | page |
| `idea-database/` | allengaller/idea-database | page |
| `lonely-reader-database/` | lonely-reader-global/lonely-reader-database | page |
| `ai-guru-database/` | ai-guru-global/ai-guru-database | docs（原 `_gtm_docs/ai-guru-database/`） |
| `ai-book/` | allengaller/ai-book | page |
| `buhua-database/` | buhua-global/buhua-database | page |
| `xiao-guan/` | peace-lab-global/xiao-guan | page |

`_scripts/sync-gtm.py` 会跳过这些条目，不再回写 `GTM/products/`。若某个产品转为公开：
把 manifest 里的 `private` 改为 `false` → 将目录移回 `GTM/products/`（或 `_gtm_docs/`）
→ 跑 `python3 _scripts/sync-gtm.py && python3 _scripts/build.py`。

## 行级下架（内容不发布，但在此留痕）

以下条目从公开文件中移除，原文记录在此，不直接删掉就算完。

| 位置 | 原内容 | 原因 |
|---|---|---|
| `.well-known/security.txt:2` | `Contact: mailto:hello@allengaller.github.io` | `allengaller.github.io` 不是可收信域名，这条地址永远收不到回复；安全通报改走 GitHub Security Advisories |
| `_data/repos-detailed.json`（`allengaller/claw` recent_commits） | `memory: sherlock OSINT scan for caoyalun + allengaller (2026-07-11)` | 提交信息里出现第三方 GitHub 用户名与针对个人的调查记录，不应出现在公开页面；`scan-repos.py` 的 `scrub_subject()` 之后会自动拦同类提交 |
| `assets/css/main.css`（原 1213 行，Animations 段） | `@keyframes revealUp { from { opacity: 0; transform: translateY(24px); filter: blur(4px); } to { opacity: 1; transform: translateY(0); filter: blur(0); } }` | 全站只有定义、没有任何 `animation:` 引用它；滚动进场改由 `[data-reveal]` 的 transition 实现（同文件 v2 段），定义与那份 transition 完全重复 |

> 注意：这两条仍存在于本仓库的 **git 历史**中。若要彻底消除，需要改写历史（`filter-repo` 强推），
> 属于不可逆操作，须由本人决定后执行。

## 其他归档约定

- 未被任何页面引用的静态资源（图片、脚本）移入本目录对应子目录，并在原位置留一行说明
  （资源注册表在 `_scripts/build.py` 的 `STATIC_FILES`，所以说明写在那里，见 banners 条目）。
- 归档条目要在本文件登记，避免变成无人认领的孤儿文件。
- **不主动清理**：`GTM/products/**` 里看着"没被引用"的文件（16 个，含一张 1.45 MB PNG）一律不动。
  那些是上游仓库的逐字快照，`sync-gtm.py --check-committed` 按目录整体比对，本站单方面裁剪
  会让每次同步都报漂移，而且镜像页自带 `<style>`，站内引用检查本来就测不到它们的真实用法。

## 已知陈物（未归档，等本人决定）

`dist/`：13 MB / 173 个文件的一整棵旧构建树，已被 `.gitignore` 忽略、未被 git 跟踪，
仓库里没有任何文件引用它，构建产物实际在 `_site/`。它不是发布内容，也没进 `_attic/`
（归档区是跟踪目录，塞进去反而把这棵陈旧副本变成需要维护的"资产"）。
本地 `rm -rf dist` 即可，属于本人决定范围内的清理，故仅在此登记一次。

`assets/css/main.css` 其余 **29 个无引用类名**（26 条整块死规则，3746 B）：
`audience-card/grid/icon`、`collab-item/list`、`domain-eyebrow(-count)`、`gtmp-card-badge`、
`overview-band/list/item/num/label`、`page-header`、`page-main`、`projects-section`、
`projects-tagline`、`role-list/item/num/body/title/desc/arrow`、`scenario-list/item/num/body`、
`section-lede`。它们是首页从"卡片网格"改成"编号行 + `.featured-card`"之前的组件，与上面
`css/` 那条同源，但**没有整体下架**，原因有两条：

- 其中 32 条规则把死类名和活类名写在同一个选择器里（如 `.about-header, .projects-header,
  .links-header { … }`），只能拆选择器清，不能整块删——回归风险由页面实际渲染决定；
- `role-*` / `scenario-*` / `overview-*` 三组是 `design.md` 里"Locked component voice"点名的
  组件家族，删 CSS 与改设计约束应当是同一次决定，不由清理顺手带走。

想收尾时：先逐屏截图确认这些区块真的没有页面用到（`_site` 里 grep 类名为空即可），
再把整块死规则按 `css/` 那节的方式移入 `_attic/css/`，`check-quality.py` 前后各跑一次。
