---
name: 命令行语料数据库 · 语料星座图谱
description: 深墨星野上的琥珀星座 × 米纸索引卡——真实语料数据库的活星图设计系统（seed ad6c4c93）
colors:
  ink-0: "#050d1c"
  ink-1: "#0a1424"
  ink-2: "#101d33"
  amber: "#d09b43"
  amber-bright: "#e8b96a"
  amber-soft: "rgba(208, 155, 67, 0.16)"
  line-ink: "rgba(233, 200, 138, 0.16)"
  cream: "#eddfc5"
  cream-2: "#f3e9d6"
  ink-on-cream: "#071322"
  ink-on-cream-2: "#3d4a5c"
  text-1: "#eddfc5"
  text-2: "#cbb391"
typography:
  display:
    fontFamily: "Spectral, Noto Serif SC, serif"
    fontSize: "clamp(28px, 2.6vw, 40px)"
    fontWeight: 600
    lineHeight: 1.1
  headline:
    fontFamily: "Noto Serif SC, Songti SC, serif"
    fontSize: "clamp(19px, 1.5vw, 25px)"
    fontWeight: 700
    letterSpacing: "0.1em"
  numeral:
    fontFamily: "JetBrains Mono, Menlo, monospace"
    fontSize: "clamp(38px, 4vw, 56px)"
    fontWeight: 500
    lineHeight: 1
    fontFeature: "tabular-nums"
  body:
    fontFamily: "Noto Sans SC, PingFang SC, sans-serif"
    fontSize: "16px"
    fontWeight: 400
    lineHeight: 1.7
  label:
    fontFamily: "Noto Sans SC, PingFang SC, sans-serif"
    fontSize: "14px"
    letterSpacing: "0.14em"
rounded:
  sm: "3px"
  md: "6px"
  pill: "999px"
spacing:
  section: "72px 40px"
  section-mobile: "56px 22px"
  row: "20px 0"
  button: "13px 28px"
components:
  button-primary:
    backgroundColor: "{colors.amber}"
    textColor: "{colors.ink-0}"
    rounded: "{rounded.pill}"
    padding: "{spacing.button}"
  button-ghost:
    backgroundColor: "transparent"
    textColor: "{colors.text-1}"
    rounded: "{rounded.pill}"
    padding: "{spacing.button}"
---

# Design System: 命令行语料数据库 · 语料星座图谱

## Overview

**Creative North Star: "语料星座图谱"（The Corpus Constellation）**

页面本身是语料库的活星图：深墨蓝的星野承载真实数据的星座，琥珀金是光，米纸索引卡是档案馆的温度。左侧图谱用规模说话（100 领域的真实散布），右侧米纸卡用质量说话（一条命令的三件套实文），两者并置构成"规模 × 质量"的双重证词。拒绝品类默认的"深色 hero + 特性卡片"排布——这里的深色不是氛围滤镜，而是天文台；浅色不是留白，而是档案纸。

一切结构性线条都是 1px 发丝线，带琥珀色温；一切数据（数字、命令名、路径）都是 JetBrains Mono 等宽字；一切装饰都服务于"纸与星"这两位主角。动效只有一个作者时刻：搜索即点亮（全场压暗至 16%，命中处琥珀辉光）。

**Key Characteristics:**
- 深墨星野（#050d1c 基底 + 径向提亮）上只允许琥珀色发光
- 米纸索引卡（#eddfc5）承载实物隐喻：打孔边、回形针、圆形骑缝章
- 1px 琥珀发丝线是唯一的结构线语言
- 数据永远等宽 + 表格数字（tabular-nums）
- 单一作者动效：搜索即点亮

## Colors

冷天文台与暖档案馆的对话：深墨蓝三个层次做地，琥珀金一个声部做光，米纸两档做纸，全部次级文字由琥珀/米色调出而非灰。

### Primary
- **琥珀金** (#d09b43): 星宿节点、大数字、主按钮、命中辉光。是这个世界的唯一光源，占屏 ≤10%。
- **亮琥珀** (#e8b96a): 悬停态、点亮态文本、code 前景。琥珀的"高光档"。

### Neutral
- **深墨零** (#050d1c): 页面基底、终端底色、按压深色。
- **深墨一** (#0a1424): 星野渐变中层、米纸卡上的深色钮。
- **深墨二** (#101d33): 星野渐变亮核（径向提亮用）。
- **米纸** (#eddfc5): 索引卡纸面、深底上的正文文字色（同一值双职）。
- **米纸二** (#f3e9d6): 纸面径向高光。
- **墨字** (#071322): 纸上的正文与标题。
- **墨字次** (#3d4a5c): 纸上的说明文字（墨的灰化，不引入纯灰）。
- **暖沙** (#cbb391): 深底上的次级文字（琥珀减淡，不是灰）。
- **发丝线** (rgba(233, 200, 138, 0.16)): 一切 1px 结构线。

### Named Rules
**The Hairline Rule（发丝线规则）。** 所有结构线恒为 1px、恒带琥珀色温（rgba(233,200,138,.09–.28)），永不使用纯灰或超过 1px 的分隔线。
**The No-Gray Rule（无灰规则）。** 深底次级文字用 --text-2（#cbb391），纸上次级文字用 --ink-on-cream-2（#3d4a5c）——都从主色调出，禁止引入无彩灰。
**The Tabular Amber Rule（数据即琥珀）。** 一切数字与等宽数据使用 JetBrains Mono + tabular-nums，大数字以琥珀呈现。

## Typography

**Display Font:** Spectral（拉丁）+ Noto Serif SC（中文），回退 Songti SC
**Body Font:** Noto Sans SC，回退 PingFang SC
**Label/Mono Font:** JetBrains Mono，回退 Menlo

**Character:** 衬线承担"档案馆的正式"，等宽承担"机器的可信"，无衬线只做正文搬运工。展示字永远衬线，数据永远等宽，两者绝不混用。

### Hierarchy
- **Display** (Spectral 600, clamp(28–40px)): 纸卡上的命令名（deepspeed）。
- **Headline** (Noto Serif SC 700, clamp(19–25px), 0.1em): 纸卡导语（"什么是每条命令的三件套"）、区块标题。
- **Numeral** (JetBrains Mono 500, clamp(38–56px), tabular): 统计带大数字（100/1137/741）。
- **Body** (Noto Sans SC 400, 16px, 1.7): 正文与说明。
- **Label** (13–14px, 0.06–0.14em): 图例、单位、步骤注释。

### Named Rules
**The Mono-for-Data Rule。** 等宽字体只用于代码、命令、路径与测量数字；绝不作为"技术感"戏服。

## Layout

首屏是严格的空间合同：左 58% 全高星图 + 右 42% 米纸卡（grid 58fr/42fr，高 calc(100vh-331px)，钳制 560–800px），其下全宽流水线带与统计/动作条。内容区块统一 section 节奏 72px/40px（≤720px 收窄为 56px/22px）。断点两级：1080px（双栏叠为单栏、网格降为两列）、720px（单列、隐藏次级导航）。星图 SVG viewBox 1000×880 绝对铺满左栏。

## Elevation & Depth

平铺系统。深度只来自三种光：星野径向渐变（#101d33→#050d1c）、SVG 节点的辉光（drop-shadow 琥珀）、主按钮的一枚环境光晕（`0 6px 24px -8px rgba(208,155,67,.55)`）。纸卡的"厚度"由打孔边与回形针的实物隐喻承担，不靠阴影。禁止零偏移彩色光晕与硬偏移块影。

## Shapes

直角为骨、细圆为饰：输入框与命令框 rx 3px，打孔与徽章 6px，按钮全胶囊 999px。纸上世界有自己的形状语言——左缘打孔条（1px 竖线 + 11px 打孔胶囊）、右上回形针（手绘 SVG 线稿，#96402c）、三枚圆形骑缝章（1.6px 圆环 + 手绘 SVG 图形，各自微旋 -8°/6°/-5°）。

## Components

### Buttons
- **Shape:** 全胶囊（999px），13px×28px 内距，15.5px 字号 + 0.06em
- **Primary:** 琥珀底墨字，18px 线稿图标，悬停提亮至 #e8b96a 并上浮 1px
- **Ghost:** 透明底 + 发丝线描边，悬停转琥珀描边与亮琥珀文字

### Search Field（星图检索）
- **Style:** 深墨底 + 发丝线描边胶囊，内嵌 20px 线稿放大镜，等宽占位文本
- **Behavior:** 输入即触发星图点亮；`?q=` 深链直达点亮态

### Folio Card（米纸索引卡）
- **Background:** 米纸径向渐变（#f3e9d6→#eddfc5→#e6d5b8），左缘打孔条
- **Anatomy:** 导语 + 饰线 → 00127|命令名 分栏头 → 三行（圆章 + 标题 + 正文）→ 等宽链接行 → 真实性注脚
- **Border:** 行间 1px 墨色发丝线（rgba(7,19,34,.12–.28)）

### Constellation（星座图）
- **节点:** 领域 r=2.2+√cmds×0.75，命令 r≈2.1–2.6，琥珀色
- **连线:** 1px 发丝线；聚焦簇辐条 + 簇内关联线，命中时两端点亮
- **States:** 搜索压暗非命中至 opacity .16（0.45s），命中组琥珀描边 + 辉光 + 0.14 琥珀底

## Do's and Don'ts

### Do:
- **Do** 用 1px 琥珀发丝线（rgba(233,200,138,.16)）画一切结构线。
- **Do** 让数据永远是 JetBrains Mono + tabular-nums，大数字用琥珀。
- **Do** 在深底用 #cbb391、纸上用 #3d4a5c 做次级文字。
- **Do** 保持"纸与星"双材质：深色区只发光不投影，纸面区只打孔不描边框。
- **Do** 每一条对外数字、命令名、引文都取自真实语料文件。

### Don't:
- **Don't** 引入无彩灰或第二色相（当前世界只有墨、琥珀、米纸、印章赭红 #a2591f/#96402c）。
- **Don't** 用超过 1px 的分隔线、彩色左边条、零偏移光晕或硬偏移块影。
- **Don't** 在标题上方加 kicker/eyebrow 小标签——标题自己开口。
- **Don't** 用 emoji 或 Unicode 字形充当图标；一切图形是手绘 SVG 线稿（1.5–1.7px 描边）。
- **Don't** 编造数据：星图与纸卡上的每个数字都必须能指回 CORPUS/YAML 真实文件。
