# allengaller.github.io

**Allen Galler** 的个人品牌总入口 —— Cloud Native SRE · AI Toolsmith · Knowledge Architect

在线访问：https://allengaller.github.io

---

## 站点结构

| 入口 | 路径 | 说明 |
|------|------|------|
| Home | `/` | 个人简介 + 代表项目 + 合作场景 |
| Projects | `/projects/` | 10 个代表项目，按应用 / 开放工具 / 知识库三分组导航 |
| **Repos** | `/repos/` | **本地 GitHub 镜像全索引（81 仓库自动扫描，其中 75 个属自有组织）** |
| Links | `/topic/links/` | 云原生 / 数据 / 开发 / AI / 生活资源链接 |
| AI Tools | `/topic/ai-tools/` | 36 款 AI 工具订阅清单（编程 / 对话 / 创作 / 陪伴 / Agent / 本地） |
| About | `/about/` | 背景、能力、合作方式 |
| Archive | `/topic/archive/` | 33 篇早期技术写作 + 2 份语料库（已停止更新） |

---

## 技术栈

- **静态站点**：Jekyll 风格 frontmatter + 自研 Python 构建脚本
- **构建**：`python3 _scripts/build.py`（增量构建 + 内容哈希缓存 + 内链检查）
- **样式**：`assets/css/main.css`（单色设计系统，Fraunces + Geist + JetBrains Mono）
- **部署**：GitHub Actions → `.github/workflows/deploy.yml` 跑 build.py 产出 `_site/`，由 `actions/deploy-pages` 发布
  （Pages 的 Source 必须是 "GitHub Actions"；`_config.yml` 不参与构建）
- **质量门禁**：`_scripts/sync-gtm.py --check-committed` 校验 GTM 快照完整性，`_scripts/check-quality.py` 校验产物
  （私有产品不落地、无未渲染模板、JSON-LD 可解析、必需文件非空），任一失败即阻断发布
- **交互**：`assets/js/site.js`（vanilla, 0 依赖：scroll progress / back-to-top / reveal / magnetic CTA）
- **数据**：`scan-repos.py` 自动从 `~/Documents/GitHub/` 提取 81 个仓库元数据
- **字体**：Fraunces (display, variable) + Geist (body) + JetBrains Mono (code)
- **图标**：favicon.svg + favicon-32.png + favicon-180.png
- **社交卡片**：og-default.png (1200×630) 自动生成

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

# 提交 GTM 产品快照（从 ~/Documents/GitHub/<org>/<repo>/GTM 整目录同步）
# 需要先 clone 源仓库；CI 不跑这个，只跑 --check-committed
python3 _scripts/sync-gtm.py

# 本地跑一遍 CI 的完整链路
python3 _scripts/sync-gtm.py --check-committed \
  && python3 _scripts/build.py --force --strict \
  && python3 _scripts/check-quality.py

# 重新生成 favicon 变体与 og-default.png
python3 _scripts/generate-favicons.py
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
_data/repos.json            (机读，58KB)
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

## 许可证

- 站点源码、构建脚本、我自己撰写的文字与 `assets/` 中自绘图形：**MIT**（正本见 [`LICENSE`](LICENSE)，面向读者的说明见 [`/licensing/`](https://allengaller.github.io/licensing/)）。
  页脚 "Open source · MIT" 即指向该页。
- `GTM/products/**`：从各产品仓库同步的**逐字快照**，版权归原项目，按原仓库声明的条款使用，本站不重新授权。
- `repos/**` 与 `_data/repos.*`：第三方仓库的名称、描述、主题、提交记录与 README 摘录来自 GitHub 公开接口，归各自作者。
- 商标与 "Allen Galler" 名称不在 MIT 授权范围内。
- `_attic/**`：已下架内容，不随构建发布（见下节与 `_attic/README.md`）。

---

## 归档说明

早期技术写作（云原生 / 数据 / 编程语言 / 音乐 / 减肥语料库，共 33 篇）**原稿不在本仓库**，
分散在自有知识库仓库（如 `kudig-io/kudig-database`、`sit-music/sit-music-database`、
`fat-looser/fat-looser-database`）。对外只通过 `/topic/archive/` 提供索引，内容**已停止更新**，
仅作长期参考保留。

> 已知欠债：`topic/archive/index.html` 的条目目前仍是 `href="#"` 占位，未接回原稿仓库。

`assets/banners/` 的 6 张项目 banner 与生成脚本 `_scripts/generate-bunicipals.py` 已整体移入
`_attic/banners/`：首页改版后没有任何页面引用它们，但仍按原样保留，需要时把目录移回、
在 `build.py` 的 `STATIC_FILES` 里恢复 6 行即可。登记见 `_attic/README.md`。
渲染这些 banner 的整套旧卡片 CSS（`.project-grid` / `.project-card` / `.project-banner` /
`.project-list` / `.project-item`，共 170 行）同步移入 `_attic/css/main__project-card-list.css`，
逐字粘回 `assets/css/main.css` 即可恢复。

> 上游待修：`GTM/products/global-goodnews/` 的署名仍是「法喜 / Allen Galler + Mavis」
> （`index.html:598`、`index.html:1338`、`README.md:4`）。该目录是 `peace-lab-global/global-goodnews`
> 的逐字快照，在本站改写会在下一次 `sync-gtm.py` 被覆盖，因此必须在源仓库更正后重新同步。
