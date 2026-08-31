#!/usr/bin/env python3
"""
Sync GTM product pages from source repos into this site (read-only copy).

Reads _data/gtm-products.json and, per entry:
  * type "page"   : copy the source GTM directory (or single file) into
                    GTM/products/<slug>/ and inject a portal back-link chip
  * type "docs"   : render the source GTM/*.md strategy docs into
                    _gtm_docs/<slug>/index.html (site layout applied at build)
  * type "internal": skip (page is built from this repo, e.g. GTM/personal/)

Usage:
  python3 _scripts/sync-gtm.py           # sync all
  python3 _scripts/sync-gtm.py --check   # validate manifest ↔ disk, no writes
"""
import json
import os
import re
import shutil
import sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build import _md, _rewrite_readme_links  # noqa: E402  (shared rendering)

MANIFEST = os.path.join(BASE, "_data", "gtm-products.json")
WORKSPACE = os.path.dirname(os.path.dirname(BASE))  # ~/Documents/GitHub (product repos live at <org>/<repo>)
PRODUCTS_DIR = os.path.join(BASE, "GTM", "products")
DOCS_DIR = os.path.join(BASE, "_gtm_docs")

BACKLINK_MARKER = "gtm-portal-backlink (managed by _scripts/sync-gtm.py)"
BACKLINK_BLOCK = f'''<!-- {BACKLINK_MARKER} -->
<a class="gtmp-back" href="/GTM/" aria-label="返回 GTM 门户">&#8617; GTM 门户</a>
<style>
.gtmp-back{{position:fixed;right:1rem;bottom:1rem;z-index:2147483000;
font:500 12px/1 ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;
letter-spacing:.05em;text-decoration:none;padding:.6rem .85rem;border-radius:999px;
color:#14130f;background:rgba(251,250,247,.92);border:1px solid rgba(20,19,15,.16);
box-shadow:0 2px 12px rgba(20,19,15,.14);backdrop-filter:blur(6px);
transition:transform .15s ease,box-shadow .15s ease}}
.gtmp-back:hover{{transform:translateY(-1px);box-shadow:0 4px 16px rgba(20,19,15,.22)}}
@media (prefers-color-scheme:dark){{.gtmp-back{{color:#f5f2ea;background:rgba(20,19,15,.88);
border-color:rgba(245,242,234,.22)}}}}
</style>'''


def load_manifest():
    with open(MANIFEST, encoding="utf-8") as f:
        return json.load(f)["products"]


def inject_backlink(html):
    # strip any previously injected block so re-sync stays idempotent
    pattern = re.compile(
        r"<!-- " + re.escape(BACKLINK_MARKER) + r" -->.*?</style>\n?", re.DOTALL)
    html = pattern.sub("", html)
    if "</body>" in html.lower():
        idx = html.lower().rindex("</body>")
        return html[:idx] + BACKLINK_BLOCK + "\n" + html[idx:]
    return html + "\n" + BACKLINK_BLOCK


def sync_page(entry, problems):
    slug = entry["slug"]
    src = os.path.join(WORKSPACE, entry["repo"], entry.get("source", "GTM"))
    dst = os.path.join(PRODUCTS_DIR, slug)
    if not os.path.exists(src):
        problems.append(f"{entry['repo']}: source missing: {entry.get('source')}")
        return
    if os.path.exists(dst):
        shutil.rmtree(dst)
    if entry.get("source_kind") == "single-file":
        os.makedirs(dst, exist_ok=True)
        shutil.copy2(src, os.path.join(dst, "index.html"))
    else:
        shutil.copytree(src, dst, ignore=shutil.ignore_patterns(".DS_Store"))
    index_path = os.path.join(dst, "index.html")
    if not os.path.exists(index_path):
        problems.append(f"{slug}: no index.html after copy")
        return
    with open(index_path, encoding="utf-8") as f:
        html = f.read()
    with open(index_path, "w", encoding="utf-8") as f:
        f.write(inject_backlink(html))
    return True


def sync_docs(entry, problems):
    slug = entry["slug"]
    src = os.path.join(WORKSPACE, entry["repo"], entry.get("source", "GTM"))
    dst = os.path.join(DOCS_DIR, slug)
    if not os.path.isdir(src):
        problems.append(f"{entry['repo']}: docs source missing: {entry.get('source')}")
        return
    md_files = sorted(f for f in os.listdir(src) if f.endswith(".md"))
    if not md_files:
        problems.append(f"{slug}: no markdown files in docs source")
        return
    # README first as overview, the rest alphabetical
    md_files.sort(key=lambda f: (f != "README.md", f))

    sections = []
    toc = []
    for i, name in enumerate(md_files, 1):
        with open(os.path.join(src, name), encoding="utf-8") as f:
            text = f.read()
        html = _md(text)
        full_name = entry["repo"]
        html = _rewrite_readme_links(html, full_name, "main")
        stem = os.path.splitext(name)[0]
        sec_id = f"gtm-sec-{i}"
        toc.append(f'<li><a href="#{sec_id}">{stem}</a></li>')
        sections.append(f'<section class="gtmp-docs-sec" id="{sec_id}">\n{html}\n</section>')

    fm_title = json.dumps(f"{entry['name']} · GTM 战略文档", ensure_ascii=False)
    fm_desc = json.dumps(entry["tagline"], ensure_ascii=False)
    page = f'''---
layout: default
title: {fm_title}
description: {fm_desc}
nav_active_gtm: is-active
---
<div class="gtmp-docs">
  <header class="gtmp-docs-head">
    <p class="gtmp-eyebrow"><a href="/GTM/">GTM 门户</a><span class="gtmp-sep">/</span><span>战略文档</span></p>
    <h1 class="gtmp-docs-title">{entry["name"]}</h1>
    <p class="gtmp-docs-sub">{entry["tagline"]}</p>
    <p class="gtmp-docs-meta">来源 <code>{entry["repo"]}</code> · 渲染自 {len(md_files)} 篇 Markdown 战略文档</p>
    <nav class="gtmp-docs-toc" aria-label="文档目录">
      <ol>{"".join(toc)}</ol>
    </nav>
  </header>
  <div class="gtmp-docs-body">
    {chr(10).join(sections)}
  </div>
</div>
'''
    os.makedirs(dst, exist_ok=True)
    with open(os.path.join(dst, "index.html"), "w", encoding="utf-8") as f:
        f.write(page)
    return True


def check(entries, problems):
    slugs = {e["slug"] for e in entries}
    for e in entries:
        slug = e["slug"]
        if e["type"] == "internal":
            continue
        src = os.path.join(WORKSPACE, e["repo"], e.get("source", "GTM"))
        if not os.path.exists(src):
            problems.append(f"{slug}: source missing {e.get('source')}")
            continue
        if e["type"] == "page":
            index = os.path.join(PRODUCTS_DIR, slug, "index.html")
            if not os.path.exists(index):
                problems.append(f"{slug}: {index} missing (run sync)")
                continue
            with open(index, encoding="utf-8") as f:
                html = f.read()
            if BACKLINK_MARKER not in html:
                problems.append(f"{slug}: back-link chip missing (re-run sync)")
            for m in re.finditer(r'(?:src|href)="(/(?!/)[^"]*)"', html):
                path = m.group(1).split("#")[0].split("?")[0]
                if not path.lstrip("/").startswith("GTM/"):
                    problems.append(f"{slug}: absolute path ref /{path} would break under subpath")
        elif e["type"] == "docs":
            if not os.path.exists(os.path.join(DOCS_DIR, slug, "index.html")):
                problems.append(f"{slug}: docs page missing (run sync)")
    if os.path.isdir(PRODUCTS_DIR):
        for name in sorted(os.listdir(PRODUCTS_DIR)):
            if name not in slugs and os.path.isdir(os.path.join(PRODUCTS_DIR, name)):
                problems.append(f"stray dir GTM/products/{name}/ not in manifest (remove manually)")


def main():
    check_only = "--check" in sys.argv[1:]
    entries = load_manifest()
    problems = []
    if check_only:
        check(entries, problems)
    else:
        done = 0
        for e in entries:
            if e["type"] == "page":
                if sync_page(e, problems):
                    done += 1
            elif e["type"] == "docs":
                if sync_docs(e, problems):
                    done += 1
        print(f"  synced {done} product(s) → GTM/products/ + _gtm_docs/")
        check(entries, problems)

    if problems:
        print(f"\n  ❌ {len(problems)} problem(s):")
        for p in problems:
            print(f"     {p}")
        sys.exit(1)
    print("  ✅ all GTM products verified" if check_only else "  ✅ sync clean")


if __name__ == "__main__":
    main()
