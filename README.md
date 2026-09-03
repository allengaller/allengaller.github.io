# allengaller.github.io

**Allen Galler 曹亚仑** 的个人品牌总入口 —— Cloud Native SRE · AI Toolsmith · Knowledge Architect

在线访问：https://allengaller.github.io

---

## 站点结构

| 入口 | 路径 | 说明 |
|------|------|------|
| Home | `/` | 个人简介 + 代表项目 + 合作场景 |
| Projects | `/projects/` | 36 个精选项目、11 个工作室、6 份语料库的完整导航 |
| **Repos** | `/repos/` | **本地 GitHub 镜像全索引（85+ 仓库自动扫描）** |
| Links | `/topic/links/` | 云原生 / 数据 / 开发 / AI / 生活资源链接 |
| AI Tools | `/topic/ai-tools/` | 36 款 AI 工具订阅清单（编程 / 对话 / 创作 / 陪伴 / Agent / 本地） |
| About | `/about/` | 背景、能力、合作方式 |
| Archive | `/topic/archive/` | 33 篇早期技术写作 + 2 份语料库（已停止更新） |

---

## 技术栈

- **静态站点**：Jekyll 风格 frontmatter + 自研 Python 构建脚本
- **构建**：`python3 _scripts/build.py`（增量构建 + 内容哈希缓存 + 内链检查）
- **样式**：`assets/css/main.css`（单色设计系统，Fraunces + Geist + JetBrains Mono）
- **部署**：GitHub Pages（`master` 分支根目录）
- **交互**：`assets/js/site.js`（vanilla, 0 依赖：scroll progress / back-to-top / reveal / magnetic CTA）
- **数据**：`scan-repos.py` 自动从 `~/Documents/GitHub/` 提取 85+ 仓库元数据
- **字体**：Fraunces (display, variable) + Geist (body) + JetBrains Mono (code)
- **图标**：favicon.svg + favicon-32.png + favicon-180.png
- **社交卡片**：og-default.png (1200×630) 自动生成
- **项目 banner**：6 个项目各有抽象 SVG banner

---

## 本地开发

```bash
# 1. 扫描本地仓库（生成 _data/repos.{yml,json}）
python3 _scripts/scan-repos.py --json

# 2. 增量构建（推荐，秒级）
python3 _scripts/build.py

# 或：自动扫描 + 构建（如果 _data/repos.json 缺失）
python3 _scripts/build.py --auto-scan

# 强制全量重新构建
python3 _scripts/build.py --force

# 清空 _site 后再构建
python3 _scripts/build.py --clean

# 严格模式：内链错误即退出非 0
python3 _scripts/build.py --strict

# 重新生成 favicon 变体与 og-default.png
python3 _scripts/generate-favicons.py

# 重新生成 6 个项目 banner SVG
python3 _scripts/generate-bunicipals.py
```

构建产物在 `_site/`，本地预览：

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

## Repos 页数据流

```
~/Documents/GitHub/*        (只读，扫描)
        ↓
_scripts/scan-repos.py     (只读所有 .git 元数据)
        ↓
_data/repos.json            (机读，36KB)
_data/repos-detailed.json   (机读，供 build.py 生成仓库详情页)
_data/repos.yml             (本地人读产物，已 gitignore，不提交)
        ↓
repos/index.html            (fetch /_data/repos.json，JS 渲染)
        ↓
_site/repos/index.html      (build.py 走 layout 渲染)
_site/_data/repos.json      (build.py 静态拷贝)
```

**关键约束**：
- `scan-repos.py` 只读其他项目的 `.git/`，**绝不修改任何项目文件**
- 数据生成与页面渲染完全解耦
- 数据文件本身可版本控制

---

## 设计原则

- **克制优先**：单色系统、最多 1080px 主宽度、单一字体尺度
- **少即是多**：避免装饰性元素，留白承担节奏
- **数据驱动**：可变内容走 YAML / JSON / 脚本，不写死在 HTML
- **GitHub Pages 友好**：无服务端逻辑、无外部 JS 依赖
- **零依赖 JS**：vanilla，rAF 节流 + IntersectionObserver

---

## 归档说明

`_archive/` 目录存放早期主题页面（云原生 / 数据 / 编程语言 / 音乐 / 减肥语料库），共 33 篇。这些内容**已停止更新**，仅作长期参考保留，对外通过 `/topic/archive/` 统一索引。
