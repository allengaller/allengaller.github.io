# DESIGN — ResolveAgent GTM 策略中枢

<!-- impeccable:design-sidecar 1 · surface: GTM/index.html · seed: 69c678c1 · mode: persuade -->

记录自已构建页面（ground truth），非意图。世界：**调度控制室 / 调度总图**（用户锁定融合：总图主导 + 终端会话、对撞机事件回放为控制室仪器 + 类别标准转化层）。

**Register（2026-08-31 用户定向）**：全页向"绝对可信的企业级"收敛，以总图区块的冷色纪律为锚点——暖奶油/琥珀底全部退役为石板冷底，无 glow，无装饰性动效；仪表元素只用仪器语法（状态 LED、方位刻度、mono 数据）。

## World

把每一次 Kubernetes 告警当作一趟列车：意图进站（枢纽「告警入口」），四条线路分岔（FTA / 技能 / RAG / 代码分析），终点站是根因。页面即一张运行中的调度总图 + 翻牌发车板。拒绝居中 hero + 三卡网格。

## Palette

| Token | Hex | 用途 |
|---|---|---|
| `--bg` | #0b1220 | 页面底（深夜蓝，控制室暗光场景） |
| `--bg2` | #0e1626 | 交替区块底 |
| `--panel/--panel2` | #111c30 / #0d1524 | 卡片/仪器面板 |
| `--ink/--ink2/--ink3` | #e8eef7 / #a7b4c9 / #7d8da6 | 正文三级（均 ≥4.5:1） |
| `--fta` | #ff6b35 | 线路1 故障树（信号橙，主 CTA 同色） |
| `--rag` | #00c2a8 | 线路2 检索增强（青） |
| `--skill` | #7c6cff | 线路3 技能（紫） |
| `--code` | #ffc94d | 线路4 代码分析（琥珀）+ 焦点环/选区 |
| `--flap/--flapbg` | #dfe8f4 / #1b2536 | 翻牌冷白字 / 石板牌底（`--flapbg2` #141c2b 下半） |
| 状态绿 | #3fb950 / #9fe3b0 | SYSTEM OK、终端成功行、会话 LED |

四线路色在全页（总图、回放径迹、ICP 站点、flywheel）保持同一套，是“四线”身份的唯一集合。

## Type

- Display：Barlow 800/900（拉丁）+ Noto Sans SC 900（中文标题）。
- 发车板/时刻表/标签：Barlow Condensed 600/700，宽字距。
- 数据/终端/统计：JetBrains Mono（tabular-nums）。
- 正文：Noto Sans SC 400/500，measure ≤62ch。
- 无 gradient text；强调靠 weight/size；无 eyebrow/kicker。

## Components

- **翻牌牌格 `.ftile`**：石板冷底渐变上下半 + 中线，冷白字；翻转动画 `flip`（rotateX）。状态列语义色：已发车=绿、运行中=冷白、待调度=琥珀（`.fstatus .warn/.ok`）。
- **发车板 `.board/.flapgrid`**：6 列（时间/ID/告警/→/路由/状态），头部含 LED + SYSTEM OK + 时钟；发车仅由 chip 调度触发，无随机空翻。
- **站名铭牌 `.plate`**：三层（线路 tag+名 / 机制 / mono 统计），圆角矩形描边。
- **终点站 `.term`**：大号线路名 + “→ 根因” + 英文小字。
- **线路 `.line`**：当前路径实线加粗，备选虚线（实/虚状态律）。
- **枢纽 `.hub`**：冷白双环 + 铃铛 + 「告警入口」。
- **意图 chips `.chip`**：圆角胶囊，选中转橙。
- **stamped CTA `.stampcta`**：总图右下大号橙块（comp 签名）。
- **终端 `.termwin`**：深底 mono 会话，栏头为绿色状态 LED + 「调度会话审计 · AUDIT TRACE」（mac 红黄绿圆点已退役），逐行 `linein` 显现。
- **事件回放 `.scope`**：同心环 + 方位刻度环 + 四径迹（无 glow；hover/click 隔离，幽灵虚线=竞争假设）。
- **时刻表 `.timetable/.ttrow`** + **状态牌 `.stat`**（已发车/筹备中/规划中）。
- **指标 `.metric`**：mono 大数字 + 线路色。

## Motion

签名时刻 = 翻牌发车 + 列车沿选中线路行驶（`getPointAtLength`）+ ticker 叙述 classify→dispatch→evaluate→corpus.write→根因。其余区块仅一次性 `rise` 显现（默认可见，动画为增强）。`prefers-reduced-motion` 全关。

## Browser surfaces

`::selection` 琥珀、细滚动条、`:focus-visible` 琥珀环、caret、tabular-nums 均已主题化。

## Responsive

≤960px：回放/flywheel/战略单列、指标两列、nav 链接隐藏、总图横向滚动（min-width 980）、翻牌缩字号。

## A11y

跳转链接、aria-label（总图/回放/模拟器）、ticker `aria-live`、对比 ≥4.5:1、键盘可达 chips/trk/CTA。

## 未决 / 需替换

调用计数、里程碑状态、北极星指标均为**示意**，正式发布前以实测数据替换；无真实客户/基准/证言。
