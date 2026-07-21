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

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE_DIR = os.path.join(BASE, "_site")
CACHE_FILE = os.path.join(SITE_DIR, ".build-cache.json")
SITE_URL = "https://allengaller.github.io"

# (source path, dest path, sitemap priority, changefreq)
PAGES = [
    ("index.html",                       "index.html",                       1.0, "weekly"),
    ("about/index.html",                 "about/index.html",                 0.8, "monthly"),
    ("projects/index.html",              "projects/index.html",              0.8, "weekly"),
    ("topic/links/index.html",           "topic/links/index.html",           0.6, "monthly"),
    ("topic/ai-tools/index.html",        "topic/ai-tools/index.html",        0.6, "monthly"),
    ("topic/archive/index.html",         "topic/archive/index.html",         0.5, "yearly"),
    ("404.html",                         "404.html",                         None, None),  # not in sitemap
]

NAV_PAGES = {
    "index.html":                "nav_active_home",
    "about/index.html":          "nav_active_about",
    "projects/index.html":       "nav_active_projects",
    "topic/links/index.html":    "nav_active_links",
    "topic/ai-tools/index.html": "nav_active_ai_tools",
    "topic/archive/index.html":  "nav_active_archive",
}

STATIC_FILES = [
    ("assets/css/main.css",   "assets/css/main.css"),
    ("assets/css/corpus.css", "assets/css/corpus.css"),
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
    return out


def build_page(src_rel, dst_rel, layout_html, cache, force=False):
    """Build a page by applying layout to content. Returns True if built."""
    src_path = os.path.join(BASE, src_rel)
    dst_path = os.path.join(SITE_DIR, dst_rel)

    if not os.path.exists(src_path):
        print(f"  Skipped (not found): {src_rel}")
        return False

    src_h = file_hash(src_path)
    layout_h = file_hash(os.path.join(BASE, "_layouts/default.html"))

    cache_key = f"page:{src_rel}:src"
    layout_key = f"page:{src_rel}:layout"
    if not force and cache.get(cache_key) == src_h and cache.get(layout_key) == layout_h:
        return False  # unchanged

    page_url = "/" + dst_rel.replace("index.html", "").rstrip("/")
    if page_url == "/":
        page_url = "/"

    rendered = render_page(src_path, layout_html, page_url)

    os.makedirs(os.path.dirname(dst_path), exist_ok=True)
    with open(dst_path, 'w') as f:
        f.write(rendered)

    cache[cache_key] = src_h
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


def check_internal_links(strict=False):
    """Verify every internal href in _site/ resolves to a real file. Returns (issues, total)."""
    issues = []
    total = 0
    if not os.path.isdir(SITE_DIR):
        return issues, total

    for root, _, files in os.walk(SITE_DIR):
        for fname in files:
            if not fname.endswith(".html"):
                continue
            path = os.path.join(root, fname)
            with open(path) as f:
                html = f.read()
            for href in re.findall(r'href="([^"]+)"', html):
                if href.startswith(("http://", "https://", "mailto:", "tel:", "javascript:", "#")):
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

    if do_clean:
        clean_site()

    cache = {} if force or do_clean else load_cache()

    with open(os.path.join(BASE, "_layouts/default.html")) as f:
        layout_html = f.read()

    copy_static_files(cache, force)

    built, skipped = 0, 0
    for src_rel, dst_rel, _priority, _changefreq in PAGES:
        if build_page(src_rel, dst_rel, layout_html, cache, force):
            print(f"  Built: {dst_rel}")
            built += 1
        else:
            skipped += 1

    if not no_sitemap:
        generate_sitemap(cache, force)

    save_cache(cache)

    # Link check (always run; warn unless --strict)
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
            print(f"\n  ✅ Link check: {total} internal link(s) resolve")

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
