#!/usr/bin/env python3
"""
Static site builder — processes Jekyll-style HTML with layouts.
Usage: python3 _scripts/build.py
"""
import os
import re
import yaml
import shutil

BASE = "/Users/allengaller/Documents/GitHub/allengaller/allengaller.github.io"

def copy_assets():
    """Copy assets to _site."""
    src_css = os.path.join(BASE, "assets/css/main.css")
    dst_css = os.path.join(BASE, "_site/assets/css/main.css")
    os.makedirs(os.path.dirname(dst_css), exist_ok=True)
    if os.path.exists(src_css):
        shutil.copy2(src_css, dst_css)
        print(f"Copied: {dst_css}")

def extract_frontmatter(html):
    """Extract Jekyll frontmatter and return (metadata, content_without_frontmatter)."""
    match = re.match(r'^---\n(.*?)\n---\n', html, re.DOTALL)
    if match:
        meta = yaml.safe_load(match.group(1))
        content = html[match.end():]
        return meta, content
    return {}, html

def build_page(src_path, dst_path):
    """Build a page by applying layout to content."""
    with open(src_path) as f:
        src = f.read()

    meta, content = extract_frontmatter(src)

    # Read layout
    with open(os.path.join(BASE, "_layouts/default.html")) as f:
        layout = f.read()

    # Replace page variables
    layout = layout.replace('{{ page.title }}', meta.get('title', ''))
    layout = layout.replace('{{ page.description }}', meta.get('description', ''))
    layout = layout.replace('{{ content }}', content)

    # Fix relative URLs
    def fix_link(m):
        href = m.group(1)
        if href.startswith('/') and not href.startswith('//'):
            return f'href="{href}"'
        return m.group(0)

    layout = re.sub(r'href="(/[^"]*)"', fix_link, layout)

    def fix_src(m):
        src = m.group(1)
        if src.startswith('/') and not src.startswith('//'):
            return f'src="{src}"'
        return m.group(0)

    layout = re.sub(r'src="(/[^"]*)"', fix_src, layout)

    # Ensure output dir exists
    os.makedirs(os.path.dirname(dst_path), exist_ok=True)

    with open(dst_path, 'w') as f:
        f.write(layout)

    print(f"Built: {dst_path}")

def main():
    copy_assets()

    pages = [
        ("index.html", "_site/index.html"),
        ("about/index.html", "_site/about/index.html"),
        ("projects/index.html", "_site/projects/index.html"),
        ("topic/links/index.html", "_site/topic/links/index.html"),
        ("topic/ai-tools/index.html", "_site/topic/ai-tools/index.html"),
    ]

    for src, dst in pages:
        src_path = os.path.join(BASE, src)
        dst_path = os.path.join(BASE, dst)
        if os.path.exists(src_path):
            build_page(src_path, dst_path)
        else:
            print(f"Skipped (not found): {src}")

if __name__ == "__main__":
    main()