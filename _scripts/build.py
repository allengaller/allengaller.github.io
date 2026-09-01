#!/usr/bin/env python3
"""
Static site builder — processes Jekyll-style HTML with layouts.

Supports:
  * Incremental builds (skip unchanged files) via content-hash cache
  * Nav active state
  * --clean:    wipe _site/ before building
  * --force:    rebuild all pages (ignore cache)
  * --strict:   fail on broken internal links
  * --no-sitemap:   skip sitemap generation
  * --no-link-check: skip internal link verification
  * Sitemap auto-generated from the page registry

Usage:
  python3 _scripts/build.py             # incremental build
  python3 _scripts/build.py --force     # rebuild all pages (ignore cache)
  python3 _scripts/build.py --clean     # wipe _site/ then incremental build
  python3 _scripts/build.py --strict    # fail on broken internal links
"""
import os
import re
import sys
import json
import yaml
import shutil
import hashlib
import subprocess
import html as _html
from datetime import datetime

try:
    import markdown as _markdown
    _MARKDOWN_OK = True
except ImportError:
    _MARKDOWN_OK = False

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE_DIR = os.path.join(BASE, "_site")
CACHE_FILE = os.path.join(SITE_DIR, ".build-cache.json")
SITE_URL = "https://allengaller.github.io"

# (source path, dest path, sitemap priority, changefreq)
PAGES = [
    ("index.html",                       "index.html",                       1.0, "weekly"),
    ("about/index.html",                 "about/index.html",                 0.8, "monthly"),
    ("projects/index.html",              "projects/index.html",              0.8, "weekly"),
    ("repos/index.html",                 "repos/index.html",                 0.7, "daily"),
    ("topic/links/index.html",           "topic/links/index.html",           0.6, "monthly"),
    ("topic/ai-tools/index.html",        "topic/ai-tools/index.html",        0.6, "monthly"),
    ("topic/archive/index.html",         "topic/archive/index.html",         0.5, "yearly"),
    ("GTM/index.html",                   "GTM/index.html",                   0.8, "weekly"),
    ("GTM/personal/index.html",          "GTM/products/allengaller/index.html", 0.7, "weekly"),
    ("404.html",                         "404.html",                         None, None),  # not in sitemap
]

# Pages whose build must also depend on other files (portal cards come from the manifest)
EXTRA_DEPS = {
    "GTM/index.html": ["_data/gtm-products.json"],
    "index.html": ["_data/gtm-products.json"],
}

NAV_PAGES = {
    "index.html":                "nav_active_home",
    "about/index.html":          "nav_active_about",
    "projects/index.html":       "nav_active_projects",
    "repos/index.html":          "nav_active_repos",
    "topic/links/index.html":    "nav_active_links",
    "topic/ai-tools/index.html": "nav_active_ai_tools",
    "topic/archive/index.html":  "nav_active_archive",
    "GTM/index.html":            "nav_active_gtm",
}

STATIC_FILES = [
    ("assets/css/main.css",   "assets/css/main.css"),
    ("assets/js/site.js",     "assets/js/site.js"),
    ("assets/js/palette.js",  "assets/js/palette.js"),
    ("_data/repos.json",      "_data/repos.json"),
    ("_data/repos.yml",       "_data/repos.yml"),
    ("assets/banners/resolve-agent.svg", "assets/banners/resolve-agent.svg"),
    ("assets/banners/kudig.svg",          "assets/banners/kudig.svg"),
    ("assets/banners/etcd-guardian.svg",  "assets/banners/etcd-guardian.svg"),
    ("assets/banners/leetcast.svg",       "assets/banners/leetcast.svg"),
    ("assets/banners/mcp4coder.svg",      "assets/banners/mcp4coder.svg"),
    ("assets/banners/opendemo.svg",       "assets/banners/opendemo.svg"),
    ("sitemap.xml",           "sitemap.xml"),
    ("robots.txt",            "robots.txt"),
    ("humans.txt",            "humans.txt"),
    ("manifest.webmanifest",  "manifest.webmanifest"),
    ("favicon.svg",           "favicon.svg"),
    ("favicon-32.png",        "favicon-32.png"),
    ("favicon-180.png",       "favicon-180.png"),
    ("og-default.png",        "og-default.png"),
    ("404.html",              "404.html"),
    (".well-known/security.txt", ".well-known/security.txt"),
    ("feed.xml",              "feed.xml"),
]


def file_hash(path):
    """Return MD5 hash of file content."""
    if not os.path.exists(path):
        return ""
    with open(path, "rb") as f:
        return hashlib.md5(f.read()).hexdigest()


def load_cache():
    """Load build cache (maps source path -> hash at last build)."""
    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE) as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError):
            return {}
    return {}


def save_cache(cache):
    """Save build cache."""
    os.makedirs(os.path.dirname(CACHE_FILE), exist_ok=True)
    with open(CACHE_FILE, "w") as f:
        json.dump(cache, f, indent=2)


def clean_site():
    """Wipe _site/ entirely."""
    if os.path.exists(SITE_DIR):
        shutil.rmtree(SITE_DIR)
        print(f"  Cleaned: {SITE_DIR}/")


def copy_static_files(cache, force=False):
    """Copy static assets, skip if unchanged."""
    copied = 0
    for src_rel, dst_rel in STATIC_FILES:
        src_path = os.path.join(BASE, src_rel)
        dst_path = os.path.join(SITE_DIR, dst_rel)
        if not os.path.exists(src_path):
            continue
        src_h = file_hash(src_path)
        if not force and cache.get(f"static:{src_rel}") == src_h:
            continue
        os.makedirs(os.path.dirname(dst_path), exist_ok=True)
        shutil.copy2(src_path, dst_path)
        cache[f"static:{src_rel}"] = src_h
        copied += 1
    if copied:
        print(f"  Static: {copied} copied")


def extract_frontmatter(html):
    """Extract Jekyll frontmatter and return (metadata, content_without_frontmatter)."""
    match = re.match(r'^---\n(.*?)\n---\n', html, re.DOTALL)
    if match:
        try:
            meta = yaml.safe_load(match.group(1)) or {}
        except yaml.YAMLError as e:
            print(f"  YAML error in frontmatter: {e}")
            meta = {}
        content = html[match.end():]
        return meta, content
    return {}, html


def render_page(src_path, layout_html, page_url):
    """Render a page by applying layout to content. Returns rendered HTML."""
    with open(src_path) as f:
        src = f.read()

    meta, content = extract_frontmatter(src)

    out = layout_html
    out = out.replace('{{ page.title }}', str(meta.get('title', '')))
    out = out.replace('{{ page.description }}', str(meta.get('description', '')))
    out = out.replace('{{ page.url }}', page_url)

    # Handle `{{ page.robots | default: 'index,follow' }}` pattern
    robots_value = meta.get('robots', 'index,follow')
    if not robots_value:
        robots_value = 'index,follow'
    out = out.replace("{{ page.robots | default: 'index,follow' }}", str(robots_value))
    out = out.replace('{{ page.robots }}', str(robots_value))

    for key in NAV_PAGES.values():
        placeholder = '{{ page.' + key + ' }}'
        out = out.replace(placeholder, str(meta.get(key, '')))

    # JSON-LD (optional; defaults to empty string)
    jsonld = meta.get('jsonld', '')
    if jsonld is None:
        jsonld = ''
    jsonld = str(jsonld).strip()
    out = out.replace('{{ page.jsonld }}', jsonld)

    out = out.replace('{{ content }}', content)

    # GTM portal injections (no-op on pages without the placeholders);
    # must run after content substitution — the placeholders live in page bodies
    out = out.replace('{{ gtm_total }}', str(_gtm_total()))
    out = out.replace('{{ gtm_cards }}', _gtm_cards_html())
    return out


def build_page(src_rel, dst_rel, layout_html, cache, force=False):
    """Build a page by applying layout to content. Returns True if built."""
    src_path = os.path.join(BASE, src_rel)
    dst_path = os.path.join(SITE_DIR, dst_rel)

    if not os.path.exists(src_path):
        print(f"  Skipped (not found): {src_rel}")
        return False

    src_h = file_hash(src_path)
    dep_h = "".join(file_hash(os.path.join(BASE, d)) for d in EXTRA_DEPS.get(src_rel, []))
    layout_h = file_hash(os.path.join(BASE, "_layouts/default.html"))

    cache_key = f"page:{src_rel}:src"
    layout_key = f"page:{src_rel}:layout"
    if not force and cache.get(cache_key) == src_h + dep_h and cache.get(layout_key) == layout_h:
        return False  # unchanged

    page_url = "/" + dst_rel.replace("index.html", "").rstrip("/")
    if page_url == "/":
        page_url = "/"

    rendered = render_page(src_path, layout_html, page_url)

    os.makedirs(os.path.dirname(dst_path), exist_ok=True)
    with open(dst_path, 'w') as f:
        f.write(rendered)

    cache[cache_key] = src_h + dep_h
    cache[layout_key] = layout_h
    return True


def generate_sitemap(cache, force=False):
    """Generate sitemap.xml from the page registry. Updates cache with content hash."""
    dst_path = os.path.join(SITE_DIR, "sitemap.xml")

    url_entries = []
    for src_rel, dst_rel, priority, changefreq in PAGES:
        # Skip pages with None priority (e.g. 404)
        if priority is None:
            continue
        page_url = "/" + dst_rel.replace("index.html", "").rstrip("/")
        if page_url == "/":
            page_url = ""
        url_entries.append((page_url, priority, changefreq))

    # Append per-repo pages (sourced from generated registry)
    repo_pages = cache.get("repo_pages:list", [])
    for repo_url, iso in repo_pages:
        url_entries.append((repo_url, 0.5, "monthly"))

    # Append GTM portal product pages (page / docs ship under /GTM/products/;
    # the internal product's URL is already in PAGES)
    for product in load_gtm_manifest():
        if product.get("type") == "internal":
            continue
        slug = product.get("slug", "")
        if slug:
            url_entries.append((f"/GTM/products/{slug}/", 0.6, "weekly"))

    body = '<?xml version="1.0" encoding="UTF-8"?>\n'
    body += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    for url, priority, changefreq in url_entries:
        body += f"  <url>\n    <loc>{SITE_URL}{url}</loc>\n"
        body += f"    <priority>{priority}</priority>\n"
        body += f"    <changefreq>{changefreq}</changefreq>\n  </url>\n"
    body += "</urlset>\n"

    new_hash = hashlib.md5(body.encode()).hexdigest()
    cache_key = "sitemap:generated"
    if not force and cache.get(cache_key) == new_hash:
        return  # unchanged

    os.makedirs(os.path.dirname(dst_path), exist_ok=True)
    with open(dst_path, 'w') as f:
        f.write(body)
    cache[cache_key] = new_hash
    print("  Built: sitemap.xml")


# ─────────────────────────────────────────────────────────
# GTM portal (manifest-driven)
# ─────────────────────────────────────────────────────────

def load_gtm_manifest():
    """Load the GTM products manifest (_data/gtm-products.json)."""
    path = os.path.join(BASE, "_data", "gtm-products.json")
    if not os.path.exists(path):
        print("  ⚠️  _data/gtm-products.json missing — GTM portal cards will be empty")
        return []
    with open(path) as f:
        data = json.load(f)
    return data.get("products", [])


_GTM_CARDS_CACHE = {}


def _gtm_total():
    """Total number of GTM products listed in the manifest."""
    if "total" not in _GTM_CARDS_CACHE:
        _GTM_CARDS_CACHE["total"] = len(load_gtm_manifest())
    return _GTM_CARDS_CACHE["total"]


def _gtm_cards_html():
    """Render the GTM portal card groups from the manifest (memoized per build).

    Emits one section per group (tools / knowledge / content); products with
    type=internal are owned by their own pages and are not listed.
    """
    if "html" in _GTM_CARDS_CACHE:
        return _GTM_CARDS_CACHE["html"]

    products = [p for p in load_gtm_manifest() if p.get("type") != "internal"]
    groups = [
        ("tools", "产品与工具"),
        ("knowledge", "知识库"),
        ("content", "内容作品"),
    ]
    sections = []
    for key, label in groups:
        items = [p for p in products if p.get("group") == key]
        if not items:
            continue
        cards = []
        for p in items:
            org = p.get("repo", "").split("/")[0] if p.get("repo") else ""
            badge = '<span class="gtmp-card-badge">内部</span>' if p.get("private") else ""
            cards.append(
                f'<a class="gtmp-card" href="/GTM/products/{_h(p.get("slug", ""))}/">'
                f'<span class="gtmp-card-name">{_h(p.get("name") or p.get("slug", ""))}</span>'
                f'<span class="gtmp-card-tagline">{_h(p.get("tagline", ""))}</span>'
                f'<span class="gtmp-card-meta"><span class="gtmp-card-org">{_h(org)}</span>{badge}</span>'
                f'</a>'
            )
        sections.append(
            f'<section class="gtmp-group reveal" data-reveal id="{key}">'
            f'<h2 class="gtmp-group-title">{_h(label)}'
            f'<span class="gtmp-group-count">{len(items)}</span></h2>'
            f'<div class="gtmp-grid">{"".join(cards)}</div>'
            f'</section>'
        )

    _GTM_CARDS_CACHE["html"] = "".join(sections)
    return _GTM_CARDS_CACHE["html"]


def copy_gtm_products(cache, force=False):
    """Mirror synced GTM product pages (GTM/products/) into _site/, hash-incremental.

    Skips dotfiles and directories reserved for build_page-rendered products
    (their _site/ copies come from build_page instead).
    """
    src_root = os.path.join(BASE, "GTM", "products")
    dst_root = os.path.join(SITE_DIR, "GTM", "products")
    if not os.path.isdir(src_root):
        return
    protected = {
        p.get("slug")
        for p in load_gtm_manifest()
        if p.get("type") in ("internal", "docs")
    }

    seen = set()
    copied = 0
    for root, dirs, files in os.walk(src_root):
        dirs[:] = [d for d in dirs if not d.startswith(".")]
        for fname in sorted(files):
            if fname.startswith("."):
                continue
            src_path = os.path.join(root, fname)
            rel = os.path.relpath(src_path, src_root)
            if rel.split(os.sep)[0] in protected:
                continue
            seen.add(rel)
            dst_path = os.path.join(dst_root, rel)
            src_h = file_hash(src_path)
            if not force and cache.get(f"gtmprod:{rel}") == src_h and os.path.exists(dst_path):
                continue
            os.makedirs(os.path.dirname(dst_path), exist_ok=True)
            shutil.copy2(src_path, dst_path)
            cache[f"gtmprod:{rel}"] = src_h
            copied += 1

    removed = 0
    if os.path.isdir(dst_root):
        for root, dirs, files in os.walk(dst_root, topdown=False):
            for fname in files:
                dst_path = os.path.join(root, fname)
                rel = os.path.relpath(dst_path, dst_root)
                if rel in seen or rel.split(os.sep)[0] in protected:
                    continue
                os.remove(dst_path)
                cache.pop(f"gtmprod:{rel}", None)
                removed += 1
            for d in dirs:
                dir_path = os.path.join(root, d)
                if not os.listdir(dir_path):
                    os.rmdir(dir_path)

    if copied or removed:
        print(f"  GTM products: {copied} copied, {removed} removed")


# ─────────────────────────────────────────────────────────
# Per-repo detail pages
# ─────────────────────────────────────────────────────────

def _md(text):
    """Render markdown to HTML safely. Fallback to escaped text on error."""
    if not _MARKDOWN_OK or not text:
        return _html.escape(text or "")
    try:
        return _markdown.markdown(
            text,
            extensions=["fenced_code", "tables", "toc", "sane_lists", "nl2br"],
        )
    except Exception as e:
        return f"<pre>{_html.escape(text)}</pre>"


def _rewrite_readme_links(html, full_name, branch):
    """Rewrite relative links/images in rendered README to point at GitHub.

    - `href="./foo"` and `href="docs/foo.md"` → `https://github.com/.../blob/<branch>/<path>`
    - `src="./foo.png"`  → `https://raw.githubusercontent.com/.../<branch>/<path>`
    - Already-absolute URLs, anchors, mailto: are left alone.
    """
    if not html or not full_name or not branch:
        return html
    blob_base = f"https://github.com/{full_name}/blob/{branch}/"
    raw_base = f"https://raw.githubusercontent.com/{full_name}/{branch}/"

    def fix_href(m):
        url = m.group(2)
        if not url or url.startswith(("http://", "https://", "mailto:", "tel:", "#",
                                       "data:", "javascript:")):
            return m.group(0)
        if _looks_relative(url):
            path = url[2:] if url.startswith("./") else url
            return f'{m.group(1)}{blob_base}{path}{m.group(3)}'
        return m.group(0)

    def fix_src(m):
        url = m.group(2)
        if not url or url.startswith(("http://", "https://", "data:")):
            return m.group(0)
        if _looks_relative(url):
            path = url[2:] if url.startswith("./") else url
            return f'{m.group(1)}{raw_base}{path}{m.group(3)}'
        return m.group(0)

    html = re.sub(r'(href=")([^"]*)(")', fix_href, html)
    html = re.sub(r'(src=")([^"]*)(")', fix_src, html)
    return html


def _looks_relative(url):
    """Heuristic: is this URL relative to the repo root?"""
    if not url:
        return False
    if url.startswith("./") or url.startswith("../"):
        return True
    clean = url.split("#", 1)[0].split("?", 1)[0]
    if not clean or clean.startswith("/"):
        return False
    if ":" in clean.split("/")[0]:  # has scheme like //host or http://
        return False
    # Bare filename (no slash) — e.g. LICENSE, README.md, CONTRIBUTING.md
    if "/" not in clean:
        return True
    # Multi-segment path — e.g. docs/foo.md, ./subdir/file
    return True


def _h(s):
    """HTML-escape a string for safe interpolation."""
    if s is None:
        return ""
    return _html.escape(str(s))


def _lang_bar(languages_detailed):
    """Render a horizontal language bar from [{lang, count}, ...]."""
    if not languages_detailed:
        return ""
    total = sum(item.get("count", 0) for item in languages_detailed) or 1
    palette = [
        "#c8553d", "#d9a45b", "#8aa888", "#5b7a99", "#9b7eb3",
        "#c97a83", "#6a8e7f", "#b89260", "#7c8aa6", "#a4806b",
    ]
    bar = "".join(
        f'<span class="lang-seg" style="width:{(item["count"]/total)*100:.2f}%;background:{palette[i % len(palette)]}" title="{_h(item["lang"])} · {item["count"]} 文件"></span>'
        for i, item in enumerate(languages_detailed)
    )
    legend = "".join(
        f'<span class="lang-legend-item"><span class="lang-dot" style="background:{palette[i % len(palette)]}"></span>{_h(item["lang"])} <span class="lang-count">{item["count"]}</span></span>'
        for i, item in enumerate(languages_detailed)
    )
    return f'<div class="lang-bar"><div class="lang-bar-track">{bar}</div><div class="lang-legend">{legend}</div></div>'


def _file_tree(top_files):
    """Render the top-level file list as a small tree."""
    if not top_files:
        return '<p class="muted small">— 没有可显示的顶级文件</p>'
    items = "".join(f'<li class="file-tree-item">{_h(f)}</li>' for f in top_files)
    return f'<ul class="file-tree">{items}</ul>'


def _recent_commits(commits, n=5):
    """Render the most recent N commits as a sidebar list."""
    if not commits:
        return '<p class="muted small">— 没有最近的提交</p>'
    items = []
    for c in commits[:n]:
        sha = c.get("short", "")
        subject = c.get("subject", "")
        rel = c.get("rel", "")
        items.append(
            f'<li class="recent-commit">'
            f'<code class="commit-sha">{_h(sha[:7])}</code>'
            f'<span class="commit-subject" title="{_h(subject)}">{_h(subject)}</span>'
            f'<span class="commit-rel">{_h(rel)}</span>'
            f'</li>'
        )
    return f'<ol class="recent-commit-list">{"".join(items)}</ol>'


def _format_size(kb):
    if not kb:
        return "—"
    if kb < 1024:
        return f"{kb:.0f} KB"
    return f"{kb/1024:.1f} MB"


def _format_date(iso):
    if not iso:
        return "—"
    try:
        d = datetime.fromisoformat(iso)
        return d.strftime("%Y-%m-%d")
    except (ValueError, TypeError):
        return "—"


def _build_repo_page(repo, related):
    """Render one repo's full HTML detail page (returns string)."""
    org = repo.get("org") or ""
    name = repo.get("name") or ""
    full_name = repo.get("full_name") or f"{org}/{name}"
    description = (repo.get("description") or repo.get("readme_excerpt") or
                   "本仓库由本地 Git 镜像自动生成。")
    lang_top = repo.get("language_top") or "—"
    last_iso = repo.get("last_commit_iso") or ""
    last_rel = repo.get("last_commit_rel") or ""
    last_subject = repo.get("last_commit_subject") or ""
    branch = repo.get("default_branch") or "main"
    commits_total = repo.get("commits_total") or 0
    size_kb = repo.get("size_kb") or 0
    file_count = repo.get("file_count") or 0
    repo_type = repo.get("repo_type") or "other"
    readme_full = repo.get("readme_full") or ""
    languages_detailed = repo.get("languages_detailed") or []
    recent_commits = repo.get("recent_commits") or []
    top_files = repo.get("top_files") or []
    is_own = repo.get("is_own", False)
    github_url = f"https://github.com/{full_name}"
    clone_url = f"https://github.com/{full_name}.git"

    # README → HTML
    if readme_full:
        readme_html = _md(readme_full)
        # Rewrite relative ./  links to GitHub blob URLs
        readme_html = _rewrite_readme_links(readme_html, full_name, branch)
    else:
        readme_html = (
            '<div class="readme-empty">'
            '<p>本仓库没有 <code>README</code>。</p>'
            f'<p><a href="{github_url}" target="_blank" rel="noopener">在 GitHub 上查看 →</a></p>'
            '</div>'
        )

    # Related repos (same org, excluding self)
    if related:
        related_html_items = "".join(
            f'<li class="related-repo-item">'
            f'<a href="/repos/{_h(r.get("org"))}/{_h(r.get("name"))}/" class="related-repo-link">'
            f'<span class="related-repo-name">{_h(r.get("name"))}</span>'
            f'<span class="related-repo-meta">{_h(r.get("language_top") or "—")} · {r.get("commits_total", 0)} commits</span>'
            f'</a></li>'
            for r in related[:5]
        )
        related_html = f'<ul class="related-repo-list">{related_html_items}</ul>'
    else:
        related_html = '<p class="muted small">— 没有同组织下的其他仓库</p>'

    # JSON-LD SoftwareSourceCode
    jsonld = {
        "@context": "https://schema.org",
        "@type": "SoftwareSourceCode",
        "name": name,
        "description": description,
        "url": github_url,
        "codeRepository": github_url,
        "dateModified": last_iso,
        "programmingLanguage": [
            ld.get("lang") for ld in languages_detailed if ld.get("lang")
        ],
        "author": {
            "@type": "Person",
            "name": "Allen Galler (曹亚仑)",
            "url": "https://allengaller.github.io/about/",
        },
    }
    jsonld_str = json.dumps(jsonld, ensure_ascii=False, indent=None, separators=(",", ":"))

    page_title = f"{name} · {org}"
    page_url = f"/repos/{org}/{name}/"
    # Trim and clean description; YAML-quoted via json.dumps below
    page_desc = description[:160].replace("\n", " ").strip()
    # Always quote to be safe with special YAML chars
    page_desc_yaml = json.dumps(page_desc, ensure_ascii=False)
    page_title_yaml = json.dumps(page_title, ensure_ascii=False)

    # Stats
    stats = [
        ("默认分支", branch, "branch"),
        ("提交总数", f"{commits_total:,}", "commits"),
        ("最近活动", f"{_format_date(last_iso)} · {last_rel}", "activity"),
        ("仓库大小", _format_size(size_kb), "size"),
        ("文件数", f"{file_count:,}" if file_count else "—", "files"),
    ]
    stats_html = "".join(
        f'<div class="stat-item stat-{meta}">'
        f'<span class="stat-label">{_h(label)}</span>'
        f'<span class="stat-value">{_h(val)}</span>'
        f'</div>'
        for label, val, meta in stats
    )

    # Eyebrow type badge
    own_badge = '<span class="badge-own">OWN</span>' if is_own else '<span class="badge-ext">EXT</span>'

    # Last commit dot + subject (sidebar header)
    last_commit_dot = (
        f'<div class="last-commit-summary">'
        f'<span class="last-commit-rel">{_h(last_rel)}</span>'
        f'<span class="last-commit-subject">{_h(last_subject)}</span>'
        f'</div>'
    )

    # Action buttons
    actions = (
        f'<div class="repo-actions">'
        f'<a class="btn-action btn-primary" href="{github_url}" target="_blank" rel="noopener">'
        f'在 GitHub 查看 ↗</a>'
        f'<button class="btn-action btn-ghost" type="button" data-copy="{_h(clone_url)}" data-copy-label="Clone">'
        f'<code>git clone</code></button>'
        f'</div>'
    )

    return f'''---
layout: default
title: {page_title_yaml}
description: {page_desc_yaml}
nav_active_repos: is-active
jsonld: {jsonld_str}
---
<div class="repo-detail" data-org="{_h(org)}" data-name="{_h(name)}">

  <header class="repo-hero">
    <p class="repo-eyebrow">
      <a href="/repos/" class="repo-back-link">Repos</a>
      <span class="repo-breadcrumb-sep">/</span>
      <a href="/repos/?filter=org:{_h(org)}" class="repo-org-link">{_h(org)}</a>
      <span class="repo-breadcrumb-sep">/</span>
      <span class="repo-name-eyebrow">{_h(name)}</span>
      {own_badge}
    </p>
    <h1 class="repo-title">{_h(name)}</h1>
    <p class="repo-tagline">{_h(description)}</p>
    {actions}
  </header>

  <div class="repo-body">

    <article class="repo-readme">
      <div class="readme-content markdown-body">
        {readme_html}
      </div>
    </article>

    <aside class="repo-sidebar">

      <section class="sidebar-section">
        <h3 class="sidebar-h">概览</h3>
        <div class="stat-grid">{stats_html}</div>
        {last_commit_dot}
      </section>

      <section class="sidebar-section">
        <h3 class="sidebar-h">语言</h3>
        {_lang_bar(languages_detailed)}
      </section>

      <section class="sidebar-section">
        <h3 class="sidebar-h">最近提交</h3>
        {_recent_commits(recent_commits, n=5)}
        <a class="sidebar-link" href="{github_url}/commits/{branch}/" target="_blank" rel="noopener">查看全部 →</a>
      </section>

      <section class="sidebar-section">
        <h3 class="sidebar-h">目录结构</h3>
        {_file_tree(top_files)}
      </section>

      <section class="sidebar-section">
        <h3 class="sidebar-h">同组织的仓库</h3>
        {related_html}
      </section>

    </aside>

  </div>

</div>

<script>
/* ── per-repo page: copy clone URL ── */
(function () {{
  'use strict';
  document.querySelectorAll('.btn-action[data-copy]').forEach(function (btn) {{
    btn.addEventListener('click', function () {{
      var url = btn.getAttribute('data-copy');
      var label = btn.getAttribute('data-copy-label') || 'Copy';
      if (navigator.clipboard && navigator.clipboard.writeText) {{
        navigator.clipboard.writeText(url).then(function () {{
          var orig = btn.innerHTML;
          btn.innerHTML = '已复制 ✓';
          setTimeout(function () {{ btn.innerHTML = orig; }}, 1400);
        }}).catch(function () {{ fallback(); }});
      }} else {{ fallback(); }}
      function fallback() {{
        var ta = document.createElement('textarea');
        ta.value = url;
        document.body.appendChild(ta);
        ta.select();
        try {{ document.execCommand('copy'); btn.innerHTML = '已复制 ✓'; }} catch (e) {{}}
        document.body.removeChild(ta);
        setTimeout(function () {{ btn.innerHTML = '<code>git clone</code>'; }}, 1400);
      }}
    }});
  }});
}})();
</script>

<style>
/* ──────────── Per-repo detail page ──────────── */
.repo-detail {{ width: 100%; }}

.repo-hero {{
  padding: 4.5rem 0 2.5rem;
  border-bottom: 1px solid var(--border);
  margin-bottom: 2.5rem;
}}

.repo-eyebrow {{
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 0.5rem;
  font-family: var(--font-mono);
  font-size: 0.7rem;
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 0.14em;
  color: var(--text-muted);
  margin: 0 0 1.25rem;
}}

.repo-back-link,
.repo-org-link {{
  color: var(--text-secondary);
  text-decoration: none;
  border-bottom: 1px solid transparent;
  transition: color 0.2s, border-color 0.2s;
}}
.repo-back-link:hover,
.repo-org-link:hover {{
  color: var(--accent);
  border-bottom-color: var(--accent);
}}

.repo-breadcrumb-sep {{
  color: var(--text-muted);
  opacity: 0.5;
}}

.repo-name-eyebrow {{
  color: var(--text);
  font-weight: 600;
}}

.badge-own,
.badge-ext {{
  font-family: var(--font-mono);
  font-size: 0.625rem;
  font-weight: 500;
  letter-spacing: 0.12em;
  padding: 0.15rem 0.5rem;
  border-radius: 3px;
  margin-left: 0.5rem;
}}
.badge-own {{
  background: var(--accent-soft);
  color: var(--accent);
  border: 1px solid var(--accent);
}}
.badge-ext {{
  background: transparent;
  color: var(--text-muted);
  border: 1px solid var(--border);
}}

.repo-title {{
  font-family: var(--font-display);
  font-size: clamp(2.5rem, 6vw, 4.5rem);
  font-weight: 400;
  font-variation-settings: "opsz" 144, "SOFT" 30, "WONK" 0;
  letter-spacing: -0.04em;
  line-height: 0.95;
  color: var(--text);
  margin: 0 0 1rem;
}}

.repo-tagline {{
  font-family: var(--font-display);
  font-size: clamp(1.05rem, 1.4vw, 1.25rem);
  font-weight: 300;
  font-style: italic;
  line-height: 1.5;
  color: var(--text-secondary);
  letter-spacing: -0.005em;
  margin: 0 0 1.75rem;
  max-width: 60ch;
}}

.repo-actions {{
  display: flex;
  gap: 0.75rem;
  flex-wrap: wrap;
}}

.btn-action {{
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  font-family: var(--font-mono);
  font-size: 0.8rem;
  font-weight: 500;
  letter-spacing: 0.04em;
  padding: 0.55rem 1rem;
  border-radius: var(--radius);
  border: 1px solid var(--border);
  background: var(--bg-subtle);
  color: var(--text);
  text-decoration: none;
  cursor: pointer;
  transition: all 0.2s var(--ease-out);
}}
.btn-action code {{
  font-size: 0.75em;
  color: var(--text-secondary);
}}
.btn-action:hover {{
  border-color: var(--accent);
  color: var(--accent);
  transform: translateY(-1px);
}}
.btn-primary {{
  background: var(--accent);
  color: #fff;
  border-color: var(--accent);
}}
.btn-primary:hover {{
  background: var(--accent-dark);
  color: #fff;
  border-color: var(--accent-dark);
}}

/* ── body two columns ── */
.repo-body {{
  display: grid;
  grid-template-columns: minmax(0, 1.7fr) minmax(0, 1fr);
  gap: 3.5rem 4rem;
  align-items: start;
  padding-bottom: 5rem;
}}
@media (max-width: 960px) {{
  .repo-body {{ grid-template-columns: 1fr; gap: 2.5rem; }}
}}

/* ── readme ── */
.repo-readme {{ min-width: 0; }}
.readme-content {{
  font-family: var(--font-body);
  font-size: 0.95rem;
  line-height: 1.7;
  color: var(--text);
  max-width: 78ch;
}}
.readme-content h1,
.readme-content h2,
.readme-content h3,
.readme-content h4 {{
  font-family: var(--font-display);
  font-weight: 500;
  font-variation-settings: "opsz" 100;
  letter-spacing: -0.02em;
  margin: 2rem 0 0.75rem;
  color: var(--text);
  line-height: 1.25;
}}
.readme-content h1 {{ font-size: 1.85rem; margin-top: 2.5rem; }}
.readme-content h2 {{ font-size: 1.5rem; border-bottom: 1px solid var(--border); padding-bottom: 0.3rem; }}
.readme-content h3 {{ font-size: 1.2rem; }}
.readme-content p {{ margin: 0 0 1rem; color: var(--text-secondary); }}
.readme-content a {{
  color: var(--accent);
  text-decoration: none;
  border-bottom: 1px solid color-mix(in srgb, var(--accent) 30%, transparent);
  transition: border-color 0.2s;
}}
.readme-content a:hover {{ border-bottom-color: var(--accent); }}
.readme-content ul, .readme-content ol {{ margin: 0 0 1rem 1.5rem; color: var(--text-secondary); }}
.readme-content li {{ margin-bottom: 0.3rem; }}
.readme-content blockquote {{
  margin: 1.5rem 0;
  padding: 0.75rem 1.25rem;
  border-left: 3px solid var(--accent);
  background: var(--bg-subtle);
  color: var(--text-secondary);
  font-style: italic;
  font-family: var(--font-display);
  font-size: 1.05rem;
  border-radius: 0 var(--radius) var(--radius) 0;
}}
.readme-content blockquote p {{ margin: 0.3rem 0; }}
.readme-content code {{
  font-family: var(--font-mono);
  font-size: 0.875em;
  background: var(--bg-subtle);
  padding: 0.1rem 0.35rem;
  border-radius: 3px;
  color: var(--text);
}}
.readme-content pre {{
  background: var(--code-bg);
  color: var(--code-fg);
  padding: 1rem 1.25rem;
  border-radius: var(--radius);
  overflow-x: auto;
  margin: 1rem 0;
  font-size: 0.85rem;
  line-height: 1.6;
  border: 1px solid var(--border);
}}
.readme-content pre code {{
  background: transparent;
  padding: 0;
  color: inherit;
  font-size: inherit;
}}
.readme-content table {{
  border-collapse: collapse;
  margin: 1rem 0;
  width: 100%;
  font-size: 0.9rem;
}}
.readme-content th, .readme-content td {{
  border: 1px solid var(--border);
  padding: 0.5rem 0.75rem;
  text-align: left;
}}
.readme-content th {{
  background: var(--bg-subtle);
  font-weight: 600;
}}
.readme-content img {{
  max-width: 100%;
  height: auto;
  border-radius: var(--radius);
}}
.readme-content hr {{
  border: none;
  border-top: 1px solid var(--border);
  margin: 2rem 0;
}}
.readme-empty {{
  padding: 2rem 0;
  text-align: center;
  color: var(--text-muted);
  font-style: italic;
}}

/* ── sidebar ── */
.repo-sidebar {{
  display: flex;
  flex-direction: column;
  gap: 2rem;
  position: sticky;
  top: 2rem;
  max-height: calc(100vh - 4rem);
  overflow-y: auto;
  padding-right: 0.5rem;
}}
@media (max-width: 960px) {{
  .repo-sidebar {{ position: static; max-height: none; overflow: visible; }}
}}
.repo-sidebar::-webkit-scrollbar {{ width: 4px; }}
.repo-sidebar::-webkit-scrollbar-thumb {{ background: var(--border); border-radius: 2px; }}

.sidebar-section {{
  padding: 1.25rem;
  background: var(--bg-subtle);
  border: 1px solid var(--border);
  border-radius: var(--radius);
}}
.sidebar-h {{
  font-family: var(--font-mono);
  font-size: 0.7rem;
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 0.14em;
  color: var(--text-muted);
  margin: 0 0 1rem;
}}

.stat-grid {{
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 0.6rem 1rem;
  margin-bottom: 1rem;
}}
.stat-item {{
  display: flex;
  flex-direction: column;
  gap: 0.15rem;
}}
.stat-label {{
  font-family: var(--font-mono);
  font-size: 0.625rem;
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  color: var(--text-muted);
}}
.stat-value {{
  font-family: var(--font-display);
  font-size: 0.95rem;
  font-weight: 500;
  color: var(--text);
  font-variant-numeric: tabular-nums;
  letter-spacing: -0.01em;
}}
.last-commit-summary {{
  padding-top: 0.75rem;
  border-top: 1px dashed var(--border);
  display: flex;
  flex-direction: column;
  gap: 0.2rem;
}}
.last-commit-rel {{
  font-family: var(--font-mono);
  font-size: 0.7rem;
  color: var(--accent);
  letter-spacing: 0.04em;
}}
.last-commit-subject {{
  font-size: 0.8rem;
  color: var(--text-secondary);
  line-height: 1.4;
}}

/* ── language bar ── */
.lang-bar {{ display: flex; flex-direction: column; gap: 0.5rem; }}
.lang-bar-track {{
  display: flex;
  height: 8px;
  border-radius: 4px;
  overflow: hidden;
  background: var(--bg);
}}
.lang-seg {{
  display: block;
  height: 100%;
  transition: opacity 0.2s;
}}
.lang-seg:hover {{ opacity: 0.85; }}
.lang-legend {{
  display: flex;
  flex-wrap: wrap;
  gap: 0.35rem 0.6rem;
  font-size: 0.7rem;
}}
.lang-legend-item {{
  display: inline-flex;
  align-items: center;
  gap: 0.3rem;
  color: var(--text-secondary);
  font-family: var(--font-mono);
}}
.lang-dot {{
  display: inline-block;
  width: 8px;
  height: 8px;
  border-radius: 2px;
}}
.lang-count {{ color: var(--text-muted); font-size: 0.85em; }}

/* ── recent commits ── */
.recent-commit-list {{
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 0.65rem;
}}
.recent-commit {{
  display: flex;
  align-items: baseline;
  gap: 0.5rem;
  font-size: 0.78rem;
  line-height: 1.4;
}}
.commit-sha {{
  font-family: var(--font-mono);
  font-size: 0.7rem;
  color: var(--accent);
  background: var(--accent-soft);
  padding: 0.1rem 0.35rem;
  border-radius: 3px;
  white-space: nowrap;
  flex-shrink: 0;
}}
.commit-subject {{
  color: var(--text-secondary);
  flex: 1;
  min-width: 0;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}}
.commit-rel {{
  font-family: var(--font-mono);
  font-size: 0.65rem;
  color: var(--text-muted);
  white-space: nowrap;
  flex-shrink: 0;
}}
.sidebar-link {{
  display: inline-block;
  margin-top: 0.75rem;
  font-family: var(--font-mono);
  font-size: 0.7rem;
  color: var(--accent);
  text-decoration: none;
  letter-spacing: 0.04em;
  border-bottom: 1px solid transparent;
  transition: border-color 0.2s;
}}
.sidebar-link:hover {{ border-bottom-color: var(--accent); }}

/* ── file tree ── */
.file-tree {{
  list-style: none;
  padding: 0;
  margin: 0;
  font-family: var(--font-mono);
  font-size: 0.75rem;
  color: var(--text-secondary);
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}}
.file-tree-item {{
  padding: 0.2rem 0;
  border-bottom: 1px dashed var(--border);
  word-break: break-all;
}}
.file-tree-item:last-child {{ border-bottom: none; }}

/* ── related repos ── */
.related-repo-list {{
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}}
.related-repo-item {{
  border-bottom: 1px dashed var(--border);
  padding-bottom: 0.4rem;
}}
.related-repo-item:last-child {{ border-bottom: none; }}
.related-repo-link {{
  display: flex;
  flex-direction: column;
  gap: 0.15rem;
  text-decoration: none;
  color: var(--text);
  padding: 0.25rem 0;
  transition: color 0.2s;
}}
.related-repo-link:hover {{ color: var(--accent); }}
.related-repo-name {{
  font-family: var(--font-display);
  font-size: 0.95rem;
  font-weight: 500;
  letter-spacing: -0.01em;
}}
.related-repo-meta {{
  font-family: var(--font-mono);
  font-size: 0.65rem;
  color: var(--text-muted);
  letter-spacing: 0.04em;
}}

/* ── muted helpers ── */
.muted {{ color: var(--text-muted); }}
.small {{ font-size: 0.8rem; }}
</style>
'''


def build_repo_pages(cache, force=False, layout_html=None):
    """Generate per-repo detail pages from _data/repos-detailed.json.

    Returns list of (page_url, last_commit_iso) tuples for sitemap use.
    Pages that haven't changed are skipped via content-hash cache.
    """
    detailed_path = os.path.join(BASE, "_data", "repos-detailed.json")
    if not os.path.exists(detailed_path):
        return []
    try:
        with open(detailed_path) as f:
            data = json.load(f)
    except (json.JSONDecodeError, OSError) as e:
        print(f"  ⚠️  Could not load repos-detailed.json: {e}")
        return []

    if layout_html is None:
        with open(os.path.join(BASE, "_layouts/default.html")) as f:
            layout_html = f.read()

    layout_h = file_hash(os.path.join(BASE, "_layouts/default.html"))

    repos = data.get("repos", [])
    # Build org index for related lookups
    by_org = {}
    for r in repos:
        org = r.get("org")
        if not org:
            continue
        by_org.setdefault(org, []).append(r)

    built = 0
    skipped = 0
    pages_for_sitemap = []

    for repo in repos:
        org = repo.get("org") or ""
        name = repo.get("name") or ""
        if not org or not name:
            continue
        if not (repo.get("is_own") and repo.get("is_github")):
            continue  # only build pages for own GitHub repos

        # Related: same org, exclude self
        related = [r for r in by_org.get(org, []) if r.get("name") != name][:5]

        page_rel = f"repos/{org}/{name}/index.html"
        page_url = f"/repos/{org}/{name}/"
        dst_path = os.path.join(SITE_DIR, page_rel)

        # Cache key = hash of relevant repo data + related + layout hash
        payload_for_hash = {
            "repo": {k: v for k, v in repo.items() if k != "abs_path"},
            "related_names": [r.get("name") for r in related],
            "layout_h": layout_h,
        }
        payload_str = json.dumps(payload_for_hash, sort_keys=True, ensure_ascii=False)
        content_h = hashlib.md5(payload_str.encode()).hexdigest()
        cache_key = f"repo_page:{org}/{name}"
        if not force and cache.get(cache_key) == content_h and os.path.exists(dst_path):
            skipped += 1
            if repo.get("last_commit_iso"):
                pages_for_sitemap.append((page_url, repo["last_commit_iso"]))
            continue

        # Render the inner HTML and apply the layout
        inner = _build_repo_page(repo, related)
        rendered = _apply_layout(inner, layout_html, page_url)
        os.makedirs(os.path.dirname(dst_path), exist_ok=True)
        with open(dst_path, "w") as f:
            f.write(rendered)
        cache[cache_key] = content_h
        built += 1
        if repo.get("last_commit_iso"):
            pages_for_sitemap.append((page_url, repo["last_commit_iso"]))

    if built:
        print(f"  Repo pages: {built} built, {skipped} unchanged")
    elif skipped:
        print(f"  Repo pages: {skipped} unchanged (use --force to rebuild)")

    cache["repo_pages:list"] = pages_for_sitemap
    return pages_for_sitemap


def _apply_layout(src_html, layout_html, page_url):
    """Like render_page() but accepts an already-rendered string + layout.

    Strips Jekyll frontmatter from src_html, substitutes placeholders in
    the layout, and injects src_html as {{ content }}.
    """
    meta, content = extract_frontmatter(src_html)
    out = layout_html
    out = out.replace('{{ page.title }}', str(meta.get('title', '')))
    out = out.replace('{{ page.description }}', str(meta.get('description', '')))
    out = out.replace('{{ page.url }}', page_url)
    robots_value = meta.get('robots', 'index,follow')
    if not robots_value:
        robots_value = 'index,follow'
    out = out.replace("{{ page.robots | default: 'index,follow' }}", str(robots_value))
    out = out.replace('{{ page.robots }}', str(robots_value))
    for key in NAV_PAGES.values():
        placeholder = '{{ page.' + key + ' }}'
        out = out.replace(placeholder, str(meta.get(key, '')))
    jsonld = meta.get('jsonld', '')
    if jsonld is None:
        jsonld = ''
    out = out.replace('{{ page.jsonld }}', str(jsonld).strip())
    out = out.replace('{{ content }}', content)
    return out


# ─────────────────────────────────────────────────────────
# RSS / Atom feed
# ─────────────────────────────────────────────────────────

def _rfc2822(iso):
    if not iso:
        return ""
    try:
        from email.utils import format_datetime
        d = datetime.fromisoformat(iso)
        return format_datetime(d)
    except (ValueError, TypeError, ImportError):
        return iso


def generate_rss(cache, force=False):
    """Atom feed at /feed.xml listing the 30 most recently active own repos."""
    detailed_path = os.path.join(BASE, "_data", "repos-detailed.json")
    if not os.path.exists(detailed_path):
        return
    try:
        with open(detailed_path) as f:
            data = json.load(f)
    except (json.JSONDecodeError, OSError):
        return

    repos = [r for r in data.get("repos", []) if r.get("is_own") and r.get("last_commit_iso")]
    repos.sort(key=lambda r: r["last_commit_iso"], reverse=True)
    repos = repos[:30]

    updated = repos[0]["last_commit_iso"] if repos else datetime.utcnow().isoformat() + "Z"

    parts = ['<?xml version="1.0" encoding="UTF-8"?>']
    parts.append('<feed xmlns="http://www.w3.org/2005/Atom">')
    parts.append(f'  <title>{_h("Allen Galler — Repos")}</title>')
    parts.append(f'  <subtitle>{_h("My own GitHub repos, sorted by latest activity")}</subtitle>')
    parts.append(f'  <link href="{SITE_URL}/feed.xml" rel="self"/>')
    parts.append(f'  <link href="{SITE_URL}/"/>')
    parts.append(f'  <id>{SITE_URL}/</id>')
    parts.append(f'  <updated>{_h(updated)}</updated>')
    parts.append('  <author><name>Allen Galler (曹亚仑)</name><uri>https://allengaller.github.io/about/</uri></author>')

    for r in repos:
        full_name = r.get("full_name", "")
        if not full_name:
            continue
        name = r.get("name", "")
        org = r.get("org", "")
        desc = (r.get("description") or r.get("readme_excerpt") or "").strip().replace("\n", " ")[:200]
        iso = r.get("last_commit_iso", "")
        page_url = f"{SITE_URL}/repos/{org}/{name}/"
        gh_url = f"https://github.com/{full_name}"
        commit_iso = iso
        if commit_iso and not commit_iso.endswith("Z"):
            commit_iso = commit_iso  # already has offset
        parts.append('  <entry>')
        parts.append(f'    <title>{_h(name)}</title>')
        parts.append(f'    <link href="{_h(page_url)}"/>')
        parts.append(f'    <link href="{_h(gh_url)}" rel="related"/>')
        parts.append(f'    <id>{_h(page_url)}</id>')
        if commit_iso:
            parts.append(f'    <updated>{_h(commit_iso)}</updated>')
            parts.append(f'    <published>{_h(commit_iso)}</published>')
        if desc:
            parts.append(f'    <summary>{_h(desc)}</summary>')
        parts.append(f'    <author><name>{_h(r.get("last_commit_author") or "曹亚仑")}</name></author>')
        parts.append('  </entry>')
    parts.append('</feed>')

    body = "\n".join(parts) + "\n"
    new_hash = hashlib.md5(body.encode()).hexdigest()
    cache_key = "feed:generated"
    if not force and cache.get(cache_key) == new_hash:
        return
    dst_path = os.path.join(SITE_DIR, "feed.xml")
    with open(dst_path, "w") as f:
        f.write(body)
    cache[cache_key] = new_hash
    print(f"  Built: feed.xml ({len(repos)} entries)")


# ─────────────────────────────────────────────────────────
# External link checker
# ─────────────────────────────────────────────────────────

def check_external_links(timeout=8, max_links=80):
    """Spot-check a sample of external links across the site. Reports non-2xx."""
    import urllib.request
    import urllib.error
    import socket
    socket.setdefaulttimeout(timeout)

    hrefs = []
    seen = set()
    for root, _, files in os.walk(SITE_DIR):
        for fname in files:
            if not fname.endswith(".html"):
                continue
            path = os.path.join(root, fname)
            try:
                with open(path) as f:
                    html = f.read()
            except (OSError, IOError):
                continue
            for m in re.finditer(r'href="(https?://[^"]+)"', html):
                url = m.group(1)
                if url in seen:
                    continue
                seen.add(url)
                hrefs.append((os.path.relpath(path, SITE_DIR), url))

    # Prioritize: GitHub URLs, then anything else. Cap to max_links.
    github = [h for h in hrefs if "github.com" in h[1]]
    other = [h for h in hrefs if "github.com" not in h[1]]
    sample = (github + other)[:max_links]

    issues = []
    for src, url in sample:
        try:
            req = urllib.request.Request(url, method="HEAD",
                                         headers={"User-Agent": "allengaller-site-linkcheck/1.0"})
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                code = resp.status
        except urllib.error.HTTPError as e:
            # Some servers reject HEAD; try GET on small range
            if e.code in (405, 403):
                try:
                    req = urllib.request.Request(url, method="GET",
                                                 headers={"User-Agent": "allengaller-site-linkcheck/1.0",
                                                          "Range": "bytes=0-1024"})
                    with urllib.request.urlopen(req, timeout=timeout) as resp:
                        code = resp.status
                except urllib.error.HTTPError as e2:
                    code = e2.code
                except Exception:
                    code = -1
            else:
                code = e.code
        except Exception:
            code = -1
        if code < 0 or code >= 400:
            issues.append((src, url, code))

    return issues, len(sample)


def check_internal_links(strict=False):
    """Verify every internal href in _site/ resolves to a real file. Returns (issues, total).

    Pages under GTM/products/ that were verbatim-synced from their source repos
    are skipped: their links are relative to the origin checkout, not this site.
    """
    issues = []
    total = 0
    if not os.path.isdir(SITE_DIR):
        return issues, total

    built_products = {
        f"GTM/products/{p.get('slug')}/index.html"
        for p in load_gtm_manifest()
        if p.get("type") in ("internal", "docs")
    }

    for root, _, files in os.walk(SITE_DIR):
        for fname in files:
            if not fname.endswith(".html"):
                continue
            path = os.path.join(root, fname)
            rel_path = os.path.relpath(path, SITE_DIR)
            if rel_path.startswith("GTM/products/") and rel_path not in built_products:
                continue
            with open(path) as f:
                html = f.read()
            for href in re.findall(r'href="([^"]+)"', html):
                if href.startswith(("http://", "https://", "mailto:", "tel:", "javascript:", "data:", "#")):
                    continue
                # Skip template-literal placeholders (e.g. ${url} in inline JS)
                if "${" in href or "`" in href:
                    continue
                # Skip JS string-concat artifacts (e.g. "' + href + '")
                if "'" in href and (" + " in href or "href +" in href):
                    continue
                # Skip obvious JS expressions
                if any(tok in href for tok in (" + ", "href +", "url +", "encodeURI")):
                    continue
                target = href.split("#")[0].split("?")[0]
                if not target:
                    continue
                total += 1
                if target.startswith("/"):
                    resolved = os.path.normpath(os.path.join(SITE_DIR, target.lstrip("/")))
                else:
                    resolved = os.path.normpath(os.path.join(os.path.dirname(path), target))
                if not os.path.exists(resolved):
                    if not resolved.endswith("/") and os.path.exists(resolved + "/index.html"):
                        continue
                    if not resolved.endswith(".html") and os.path.exists(resolved + ".html"):
                        continue
                    issues.append((path, href))

    return issues, total


def main():
    args = set(sys.argv[1:])
    force = "--force" in args
    do_clean = "--clean" in args
    no_sitemap = "--no-sitemap" in args
    auto_scan = "--auto-scan" in args

    if do_clean:
        clean_site()

    cache = {} if force or do_clean else load_cache()

    with open(os.path.join(BASE, "_layouts/default.html")) as f:
        layout_html = f.read()

    # Pre-build sanity: ensure _data/repos.json exists; auto-scan if missing
    repos_json = os.path.join(BASE, "_data", "repos.json")
    if not os.path.exists(repos_json):
        if auto_scan:
            print("  ⚙️  _data/repos.json missing — running scan-repos.py --json")
            r = subprocess.run(
                [sys.executable, os.path.join(BASE, "_scripts", "scan-repos.py"), "--json", "--quiet"],
                cwd=BASE, capture_output=True, text=True,
            )
            if r.returncode != 0:
                print(f"  ⚠️  scan-repos failed (exit {r.returncode}); the /repos/ page will show an error")
            else:
                print("  ✓ scan-repos completed")
        else:
            print("  ⚠️  _data/repos.json not found. The /repos/ page will show a load error.")
            print("     → Run: python3 _scripts/scan-repos.py --json")
            print("     → Or:  python3 _scripts/build.py --auto-scan")

    copy_static_files(cache, force)
    copy_gtm_products(cache, force)

    built, skipped = 0, 0
    for src_rel, dst_rel, _priority, _changefreq in PAGES:
        if build_page(src_rel, dst_rel, layout_html, cache, force):
            print(f"  Built: {dst_rel}")
            built += 1
        else:
            skipped += 1

    # Generate GTM docs pages (markdown strategic docs rendered via the site layout)
    docs_built = 0
    for product in load_gtm_manifest():
        if product.get("type") == "docs":
            slug = product.get("slug", "")
            if build_page(f"_gtm_docs/{slug}/index.html", f"GTM/products/{slug}/index.html", layout_html, cache, force):
                print(f"  Built: GTM/products/{slug}/ (docs)")
                docs_built += 1

    # Generate per-repo detail pages (only when repos-detailed.json exists)
    build_repo_pages(cache, force, layout_html=layout_html)

    # Generate RSS feed
    generate_rss(cache, force)

    if not no_sitemap:
        generate_sitemap(cache, force)

    save_cache(cache)

    # Internal link check (always run; warn unless --strict)
    skip_links = "--no-link-check" in args
    if not skip_links:
        issues, total = check_internal_links()
        if issues:
            print(f"\n  ⚠️  {len(issues)} broken internal link(s) (out of {total} checked):")
            for src, href in issues:
                rel_src = os.path.relpath(src, SITE_DIR)
                print(f"     {rel_src}  →  {href}")
            if "--strict" in args:
                print("\n  ❌ --strict: aborting due to broken links")
                sys.exit(1)
        else:
            print(f"\n  ✅ Internal link check: {total} internal link(s) resolve")

    # External link spot-check (only when explicitly requested)
    if "--strict-external" in args:
        ext_issues, ext_total = check_external_links()
        if ext_issues:
            print(f"\n  ⚠️  {len(ext_issues)} external link(s) with issues (out of {ext_total} checked):")
            for src, url, code in ext_issues[:20]:
                rel_src = os.path.relpath(src, SITE_DIR)
                print(f"     {rel_src}  →  {url}  ({code})")
        else:
            print(f"\n  ✅ External link check: {ext_total} external link(s) OK")

    summary = f"\n  {built} built, {skipped} unchanged"
    if force:
        summary += " (force)"
    if do_clean:
        summary += " (clean)"
    if skipped:
        summary += "  ·  use --force to rebuild all"
    print(summary + "\n")


if __name__ == "__main__":
    main()
