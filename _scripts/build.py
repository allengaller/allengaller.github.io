#!/usr/bin/env python3
"""
Static site builder — processes Jekyll-style HTML with layouts.
Supports incremental builds (skip unchanged files) and nav active state.
Usage: python3 _scripts/build.py [--force]
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
CACHE_FILE = os.path.join(BASE, "_site/.build-cache.json")

NAV_PAGES = {
    "index.html": "nav_active_home",
    "about/index.html": "nav_active_about",
    "projects/index.html": "nav_active_projects",
    "topic/links/index.html": "nav_active_links",
    "topic/ai-tools/index.html": "nav_active_ai_tools",
}

STATIC_FILES = [
    ("assets/css/main.css", "_site/assets/css/main.css"),
    ("sitemap.xml", "_site/sitemap.xml"),
    ("favicon.svg", "_site/favicon.svg"),
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
        with open(CACHE_FILE) as f:
            return json.load(f)
    return {}


def save_cache(cache):
    """Save build cache."""
    os.makedirs(os.path.dirname(CACHE_FILE), exist_ok=True)
    with open(CACHE_FILE, "w") as f:
        json.dump(cache, f, indent=2)


def copy_static_files(cache, force=False):
    """Copy static assets, skip if unchanged."""
    for src_rel, dst_rel in STATIC_FILES:
        src_path = os.path.join(BASE, src_rel)
        dst_path = os.path.join(SITE_DIR, dst_rel.replace("_site/", ""))
        if not os.path.exists(src_path):
            continue
        src_h = file_hash(src_path)
        if not force and cache.get(src_rel) == src_h:
            continue
        os.makedirs(os.path.dirname(dst_path), exist_ok=True)
        shutil.copy2(src_path, dst_path)
        cache[src_rel] = src_h
        print(f"  Copied: {src_rel}")


def extract_frontmatter(html):
    """Extract Jekyll frontmatter and return (metadata, content_without_frontmatter)."""
    match = re.match(r'^---\n(.*?)\n---\n', html, re.DOTALL)
    if match:
        meta = yaml.safe_load(match.group(1))
        content = html[match.end():]
        return meta, content
    return {}, html


def build_page(src_rel, dst_rel, cache, force=False):
    """Build a page by applying layout to content. Returns True if built."""
    src_path = os.path.join(BASE, src_rel)
    dst_path = os.path.join(SITE_DIR, dst_rel.replace("_site/", ""))

    if not os.path.exists(src_path):
        print(f"  Skipped (not found): {src_rel}")
        return False

    src_h = file_hash(src_path)
    layout_h = file_hash(os.path.join(BASE, "_layouts/default.html"))

    # Check if source or layout changed
    cache_key = f"{src_rel}:src"
    layout_key = f"{src_rel}:layout"
    if not force and cache.get(cache_key) == src_h and cache.get(layout_key) == layout_h:
        return False  # unchanged

    with open(src_path) as f:
        src = f.read()

    meta, content = extract_frontmatter(src)

    with open(os.path.join(BASE, "_layouts/default.html")) as f:
        layout = f.read()

    # Replace page variables
    layout = layout.replace('{{ page.title }}', meta.get('title', ''))
    layout = layout.replace('{{ page.description }}', meta.get('description', ''))

    # Replace nav_active_* variables
    for key in NAV_PAGES.values():
        placeholder = '{{ page.' + key + ' }}'
        layout = layout.replace(placeholder, meta.get(key, ''))

    layout = layout.replace('{{ content }}', content)

    os.makedirs(os.path.dirname(dst_path), exist_ok=True)
    with open(dst_path, 'w') as f:
        f.write(layout)

    # Update cache
    cache[cache_key] = src_h
    cache[layout_key] = layout_h

    return True


def main():
    force = "--force" in sys.argv
    cache = {} if force else load_cache()

    pages = [
        ("index.html", "_site/index.html"),
        ("about/index.html", "_site/about/index.html"),
        ("projects/index.html", "_site/projects/index.html"),
        ("topic/links/index.html", "_site/topic/links/index.html"),
        ("topic/ai-tools/index.html", "_site/topic/ai-tools/index.html"),
    ]

    copy_static_files(cache, force)

    built, skipped = 0, 0
    for src, dst in pages:
        if build_page(src, dst, cache, force):
            print(f"  Built: {dst}")
            built += 1
        else:
            skipped += 1

    save_cache(cache)

    if skipped:
        print(f"\n  {built} built, {skipped} unchanged (use --force to rebuild all)")
    else:
        print(f"\n  {built} pages built")


if __name__ == "__main__":
    main()
