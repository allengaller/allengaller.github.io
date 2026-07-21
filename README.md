# allengaller.github.io

**法喜** 的个人品牌总入口 —— Cloud Native SRE · AI Toolsmith · Knowledge Architect

在线访问：https://allengaller.github.io

---

## 站点结构

| 入口 | 路径 | 说明 |
|------|------|------|
| Home | `/` | 个人简介 + 代表项目 + 合作场景 |
| Projects | `/projects/` | 36 个项目、11 个工作室、6 份语料库的完整导航 |
| Links | `/topic/links/` | 云原生 / 数据 / 开发 / AI / 生活资源链接 |
| AI Tools | `/topic/ai-tools/` | 29 付费 + 7 免费 AI 工具订阅清单 |
| About | `/about/` | 背景、能力、合作方式 |
| Archive | `/topic/archive/` | 33 篇早期技术写作 + 2 份语料库（已停止更新） |

---

## 技术栈

- **静态站点**：Jekyll 风格 frontmatter + 自研 Python 构建脚本
- **构建**：`python3 _scripts/build.py`（增量构建 + 内容哈希缓存）
- **样式**：单文件 `assets/css/main.css`（826 行）+ `corpus.css`（586 行），单色设计系统
- **部署**：GitHub Pages（`master` 分支根目录）
- **字体**：Inter (Google Fonts) + SF Pro 本地优先
- **图标**：favicon.svg (主) + favicon-32.png + favicon-180.png (Apple touch)
- **社交卡片**：og-default.png (1200×630) 自动生成

---

## 本地开发

```bash
# 增量构建（推荐，秒级）
python3 _scripts/build.py

# 强制全量重新构建
python3 _scripts/build.py --force

# 清空 _site 后再构建（适合排查问题时使用）
python3 _scripts/build.py --clean

# 重新生成 favicon 变体与 og-default.png
python3 _scripts/generate-favicons.py

# 重新生成 AI Tools 页面
python3 _scripts/generate-ai-tools.py
```

构建产物在 `_site/`，本地预览可以：

```bash
cd _site && python3 -m http.server 4000
# → http://localhost:4000
```

---

## 添加一个新页面

1. 在对应目录创建 `index.html`，顶部带 Jekyll frontmatter：

   ```yaml
   ---
   layout: default
   title: 页面标题
   description: SEO 描述
   nav_active_xxx: is-active   # 可选：让导航高亮
   ---
   ```

2. 在 `_scripts/build.py` 的 `PAGES` 列表中注册：

   ```python
   ("新路径/index.html", "新路径/index.html", 0.5, "monthly"),
   ```

3. `python3 _scripts/build.py` —— 仅该页面会重新构建。

---

## 设计原则

- **克制优先**：单色系统、最多 720px 主宽度、单一字体尺度
- **少即是多**：避免装饰性元素，留白承担节奏
- **数据驱动**：可变内容走 YAML / 脚本，不写死在 HTML
- **GitHub Pages 友好**：无服务端逻辑、无外部 JS 依赖

---

## 归档说明

`_archive/` 目录存放早期主题页面（云原生 / 数据 / 编程语言 / 音乐 / 减肥语料库），共 33 篇。这些内容**已停止更新**，仅作长期参考保留，对外通过 `/topic/archive/` 统一索引。
