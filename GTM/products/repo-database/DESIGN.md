---
name: GTM — The Departure Board
description: repo-database GTM 页面的车站翻牌出发板设计系统（deep-green enamel hall · bone flaps · amber service · stamp-red human marks）
colors:
  amber: "#f5a623"
  amber-deep: "#c77f0a"
  hall-ground: "#0b150f"
  enamel: "#0d1a14"
  enamel-panel: "#0e1a13"
  line-structural: "#22382b"
  line-soft: "#1a2d21"
  flap: "#f2eee2"
  flap-edge: "#d9d3c1"
  flap-ink: "#22301f"
  stamp: "#c8452c"
  stamp-ink: "#b3382c"
  ink: "#e8e4d8"
  ink-dim: "#a8b3a4"
  ink-faint: "#77857a"
  paper-ink: "#2b2b28"
  paper-dim: "#6b6a5f"
typography:
  display:
    fontFamily: "Saira Condensed, Noto Sans SC, sans-serif"
    fontSize: "clamp(2.5rem, 4vw, 4.5rem)"
    fontWeight: 800
    lineHeight: 1.1
    letterSpacing: "0.01em"
  headline:
    fontFamily: "Saira Condensed, Noto Sans SC, sans-serif"
    fontSize: "1.1875rem"
    fontWeight: 700
    lineHeight: 1.3
    letterSpacing: "0.03em"
  body:
    fontFamily: "Saira, Noto Sans SC, PingFang SC, Microsoft YaHei, sans-serif"
    fontSize: "1.03125rem"
    fontWeight: 400
    lineHeight: 1.6
    letterSpacing: "normal"
  flap-data:
    fontFamily: "Spline Sans Mono, SF Mono, Consolas, monospace"
    fontSize: "1.03125rem"
    fontWeight: 500
    lineHeight: 1.4
    letterSpacing: "0.01em"
  label:
    fontFamily: "Spline Sans Mono, SF Mono, Consolas, monospace"
    fontSize: "0.8125rem"
    fontWeight: 500
    lineHeight: 1.4
    letterSpacing: "0.1em"
rounded:
  paper: "3px"
  control: "4px"
  flap: "6px"
  stamp: "6px"
  ticket: "8px"
  card: "10px"
  frame: "14px"
components:
  button-primary:
    backgroundColor: "{colors.amber}"
    textColor: "#1c1204"
    rounded: "{rounded.ticket}"
    padding: "18px 30px 16px"
  button-primary-hover:
    backgroundColor: "{colors.amber}"
  button-secondary:
    backgroundColor: "transparent"
    textColor: "{colors.ink}"
    rounded: "{rounded.ticket}"
    padding: "18px 26px"
  card-enamel:
    backgroundColor: "{colors.enamel}"
    textColor: "{colors.ink-dim}"
    rounded: "{rounded.card}"
    padding: "24px 20px"
  card-paper:
    backgroundColor: "#f4eddc"
    textColor: "{colors.paper-ink}"
    rounded: "{rounded.paper}"
    padding: "30px 24px 22px"
  stamp-badge:
    backgroundColor: "transparent"
    textColor: "{colors.stamp-ink}"
    rounded: "{rounded.stamp}"
    padding: "3px 9px"
---

# Design System: GTM — The Departure Board

> 范围声明：本系统只描述 `GTM/` 出发板页面的视觉世界。仓库内 `web/` 另有一套独立 UI 世界（近黑 `#0c0c0e`、JetBrains Mono + Outfit、亮暗双主题），两套世界互不继承。本文件基于建成代码 `GTM/gtm.css` 提取，非规划文档。

## Overview

**Creative North Star: "THE ROLL · 翻牌出发板"**

整个页面是一座深绿珐琅面的车站出发大厅：机器把上千个仓库排进时刻表，人把值得留下的钉在板上。所有视觉决策都从"物理车站器具"出发——板是挂在墙上的重物（大而软的环境影 + 顶部内高光的珐琅反光），翻牌是骨白塑料片（渐变面 + 中缝 + 翻转动画），告示是钉在软木板上的纸卡（纸色渐变、微倾斜、红墨印章），谱系是地铁线路图（粗线、圆站牌、虚线表亲）。

密度上是"时刻表式密排 + 告示卡式留白"的交替：出发板行与行之间只有 1px 软分隔线（信息器具），叙事段之间则是 `clamp(72px, 9vw, 120px)` 的大段呼吸。双语文本是站牌的本体语言——每块标牌都是"中文主标 + 英文/拼音副标"成对出现，不是装饰而是车站标识系统的构成规则。

**Key Characteristics:**
- 深绿珐琅分层底：大厅底色比板面更深一层，一切器具浮在其上
- 骨白翻牌是唯一的"亮面材质"，承担所有真实数据展示
- 琥珀 = 机器/服务状态；印章红 = 人工判断痕迹；绿 PASS 章 = CI 放行——三色各司其职
- 硬底边阴影 + 软环境影的"实物厚度"深度模型
- 全部数字用等宽 tabular-nums，像真的排班数据

## Colors

调色板是一套"深夜车站"分层：三个近黑绿做底与板面，骨白做亮面与文字，琥珀做唯一强调，印章红做人工标记，纸色系只存在于告示卡内部。

### Primary
- **琥珀运行色 Amber** (#f5a623)：所有"服务在此运行"的信号——CTA 票根、车站时钟、图标、链接、表头、发车站牌。深一档的 **Amber Deep** (#c77f0a) 只用于票根底边（按压厚度）。

### Secondary
- **印章红 Stamp** (#c8452c / 章墨 #b3382c)：人工判断的痕迹——告示卡 5/5 评级章、章色链接、谱系图第二条线路。红色永远不用于机器状态。

### Tertiary
- **线路编码色组**（#e8991a / #4f8a6d / #6b8ba4 / #8a7f68）：谱系地铁图专用的线路区分色，属数据编码，不作系统强调色复用。放行绿 **PASS Green** (#6fae87) 专用于闸口 PASS 章。

### Neutral
- **大厅底 Hall Ground** (#0b150f)：页面最深底色，body 背景。
- **珐琅面 Enamel** (#0d1a14)：浮起的器具面——板框内衬、公式块、闸口卡、站牌填充。
- **条带面板 Enamel Panel** (#0e1a13)：段落交替条带背景（机器时刻表、发车前检查），比珐琅略亮半档。
- **结构线 / 软线** (#22382b / #1a2d21)：器具外框线 / 板内行分隔线，两级边框纪律。
- **骨白翻牌 Flap** (#f2eee2)：亮面材质 + 高亮文字双职能；**Flap Edge** (#d9d3c1) 是翻牌底缘；**Flap Ink** (#22301f) 是翻牌上的墨。
- **墨阶 Ink** (#e8e4d8 / #a8b3a4 / #77857a)：正文 / 次级 / 元信息三级文字。
- **纸墨 Paper Ink** (#2b2b28 / #6b6a5f)：告示卡内部专用墨色，深浅两级。

### Named Rules
**The Red-Ink-Is-Human Rule.** 印章红只出现在"人做过判断"的地方（评级章、人工痕迹链接、人工谱系线）。机器调度、自动化、数据一律用琥珀。绿色只表示 CI 放行。三色越界即语义错误。

**The Two-Inks Rule.** 深墨只写在亮材质上（flap-ink 写在骨白翻牌、paper-ink 写在纸卡），浅墨只写在暗底上。琥珀底 CTA 用自己的深褐墨 #1c1204，不用任何灰阶。

## Typography

**Display Font:** Saira Condensed（DIN 系车站字，回退 Noto Sans SC）——所有"站牌嗓音"：标题、按钮、表头、章面、步骤名。
**Body Font:** Saira（回退 Noto Sans SC → PingFang SC → Microsoft YaHei）——正文叙述。
**Flap/Mono Font:** Spline Sans Mono（回退 SF Mono → Consolas）——一切"板上真实数据"：翻牌仓库名、时钟、公式、命令、元信息标签、表格首列。

**Character:** 压缩的工业站牌字给出调度权威，等宽字给出"这是真实排班数据"的证据感，Noto Sans SC 兜住中文站牌。三者互不混用：叙述归 Saira，标牌归 Condensed，数据归 Mono。

### Hierarchy
- **Display** (Saira Condensed 800, `clamp(38px, 5.6vw, 72px)`，行高 1.06)：大厅主标，中文块骨白实色、英文块琥珀 0.52em 次级。
- **Section title** (Saira Condensed 800, `clamp(30px, 4vw, 44px)`，行高 1.1)：每段主标；其下必挂一行 Mono 13px / .28em 琥珀英副标（成对标识）。
- **Headline** (Saira Condensed 700, 19px)：步骤名、卡片标题。
- **Body** (Saira 400, 16.5px，行高 1.6，≤62ch)：叙述与 lede；次级 14.5px。
- **Flap data** (Spline Sans Mono 500, 16.5px，tabular-nums)：翻牌仓库名。
- **Label** (Spline Sans Mono 500, 10.5–13px，字距 .08–.14em)：元信息、dt 标签、日期。

### Named Rules
**The Transit-Voice Rule.** 标牌文字永远 Saira Condensed 700/800 + 字距，正文永远 Saira 常宽。等宽字只写"板上会出现的真实数据"，不用于标题或正文强调。

## Layout

内容容器 `max-width: 1160px` 居中（票根 CTA 同宽，快速发车窄版 880px）。段落垂直节奏 `clamp(72px, 9vw, 120px)`，水平内边距 `clamp(20px, 4vw, 48px)`。背景以"大厅底 → 面板条带 → 大厅底"交替制造车站分区。

出发板行是 4 列网格 `190px minmax(0,1fr) 110px 96px`（线路 / 翻牌 / 星数 / 评分），行间仅 `--line-soft` 1px 分隔。公式块用 `minmax(0,·)` 轨道防止不可断行内容撑爆网格。

断点阶梯：**1024px**（how-grid 落单列、闸口 2 列、告示 1 列、时钟隐藏）→ **760px**（板行收 3 列、评分列隐藏、CTA 竖排、地铁图 720px 横滚）→ **640px**（板行改两行堆叠 grid-areas：line+stars / dest 通栏）→ **480px**（顶栏收紧）→ **380px**（翻牌字号 11.5px 并允许换行）。所有内容网格轨道必须 `minmax(0,1fr)`，禁止裸 `1fr`。

## Elevation & Depth

深度模型是"实物厚度"，不是纸面卡片浮起：每个浮起器具由三种影子合成——**硬底边影**（`0 4px 0 <材质深一档>`，读作物体厚度，按压时减薄）、**软环境影**（大半径低透明黑，读作悬挂/摆放）、**内顶高光**（`inset 0 1px 0 rgba(242,238,226,.05~.06)`，读作珐琅反光）。无发光、无彩色投影。

### Shadow Vocabulary
- **挂板影** (`0 24px 60px rgba(0,0,0,.5)` + `inset 0 1px 0 rgba(242,238,226,.06)`)：出发板框。
- **票根影** (`0 4px 0 var(--amber-deep)` + `0 16px 34px rgba(0,0,0,.45)`；hover `0 6px 0`，active `0 2px 0`)：琥珀 CTA 的可按压厚度。
- **翻牌影** (`inset 0 -2px 0 rgba(0,0,0,.18)` + `0 3px 8px rgba(0,0,0,.35)`)：单片翻牌的料厚。
- **纸卡影** (`0 14px 30px rgba(0,0,0,.42)` + `0 2px 6px rgba(0,0,0,.3)`)：钉在板上的告示纸。

### Named Rules
**The Edge-Shadow Rule.** 有"可按压感"的元件（CTA）必须带 `0 Npx 0 <深一档材质色>` 硬底边影，且 hover/active 通过增减 N 表达按压；环境影只补充悬挂感，永不单独承担深度。

## Shapes

圆角阶梯按器具语义分派：纸卡 3px（纸的硬挺）、控件/翻牌 4–6px、票根 8px、珐琅卡 10px、板框 14px。签名几何：**铆钉**（板框对角 ::before/::after 10px 径向渐变圆钉）、**票根打孔**（CTA 左右 18px 底色圆孔 ::before/::after）、**纸卡微倾**（±0.35–0.7deg 交错，hover 回正上浮 4px）、**章面微倾**（5/5 章 -7deg、PASS 章 +8deg）、**虚线表亲**（地铁图 dashed 轨道 3 3 与虚线边框卡）。图标一律内联 stroke SVG，琥珀描边，44px 珐琅底方章（8px 圆角）承载。

## Components

### Buttons
- **Shape:** 票根 8px 圆角、打孔双圆；ghost 按钮 8px 圆角 1px 结构线描边。
- **Primary（票根 CTA）:** 琥珀渐变底（#f5a623→#e8991a）+ 深褐墨 #1c1204 + `18px 30px 16px` 内距；主标 Saira Condensed 800 21px + small 12.5px 副标。
- **Hover / Active:** translateY(-2px)/厚度加深的悬浮，active translateY(1px)/厚度减薄的按压；focus-visible 琥珀 2px outline，offset 3px。
- **Secondary / Ghost:** 透明底 + 结构线描边，hover 描边与文字转琥珀 + 6% 琥珀底。
- **Toggle（语言切换）:** Mono 13px 700、4px 圆角小方钮，hover 同 ghost。

### Split-Flap Row（签名组件）
- 出发板一行四列；翻牌片骨白渐变（48.5% 处断色制造翻片中缝）+ ::after 1.5px 中缝线 + `flapFlip` 0.5s `cubic-bezier(.45,0,.35,1)` rotateX 翻转（50% 处 brightness .72）。
- 轮换节奏 4s + 行序 ×350ms stagger；`prefers-reduced-motion` 下禁用动画、6s 直接换字。

### Cards
- **Enamel 卡（闸口）:** 珐琅底 + 1px 结构线 + 10px 圆角 + `24px 20px`；右上角 PASS 绿章（rotate 8deg, opacity .85）。
- **Paper 卡（告示）:** 纸色渐变（#f4eddc→#e9e0c9）+ 3px 圆角 + 顶部 14px 红色圆钉 + 微倾 + Mono 章名牌与 2.5px 章框评级章；内部全用纸墨两级。

### Stamp Badges
- 章面 = Condensed 800 + 2–2.5px 同色描边框 + 4–6px 圆角 + ±7–8deg 旋转 + radial mask 轻微印泥不匀（#c8452c 系）。

### Code / Formula Block
- 珐琅底 + 1px 结构线 + 10px 圆角 + `20px 22px` + 内顶高光；Mono 13.5px 行高 1.75，`white-space: pre` + `overflow-x: auto`。

### Navigation
- 站牌顶栏 sticky：88% 底色 + 10px blur + 1px 结构线下缘；左品牌圆徽（琥珀）+ 双语站名，右时钟（Mono 琥珀时间）+ 语言钮 + 票根 Star 钮。≤1024px 时钟退场。

## Do's and Don'ts

### Do:
- **Do** 一切数字（星数、评分、时刻）用 Spline Sans Mono + `font-variant-numeric: tabular-nums`。
- **Do** 每块中文标牌成对给出英文/副标，作为车站标识系统的固定构成。
- **Do** 任何入场动画都配 `prefers-reduced-motion` 的降级路径（直接换字、去过渡）。
- **Do** 数据网格轨道写 `minmax(0,1fr)`，防不可断行内容（pre、长仓库名）撑爆布局。

### Don't:
- **Don't** 对大号展示文字做渐变填充——骨白主标是实色 `var(--flap)`（渐变字在建成后已被判为赝品材质并移除）。
- **Don't** 让印章红出现在机器/自动化的语义上，或让琥珀出现在人工判断的语义上（三色分职见 Red-Ink-Is-Human Rule）。
- **Don't** 使用图标字体或 glyph 字符图标；只用内联 stroke SVG。
- **Don't** 用彩色发光或大面积模糊投影制造深度——深度只有"厚度 + 悬挂 + 珐琅反光"三件套。
- **Don't** 底色偏离绿系（不许蓝黑或暖奶油化大厅底色）。
