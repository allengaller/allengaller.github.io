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

Products flagged "private": true are never synced into the published tree;
build.py also withholds them from _site/. Their last snapshot is kept under
_attic/gtm-private/ for reference only.
"""
import json
import os
import posixpath
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

# Escaped references to these are served as raw bytes, not GitHub's HTML wrapper.
ASSET_RE = re.compile(r"\.(png|jpe?g|gif|svg|webp|avif|ico|css|js|woff2?|ttf|mp4|webm|pdf)$", re.I)
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


def _origin_base(entry):
    """Directory the snapshot's relative links resolve against, inside its repo."""
    source = entry.get("source", "GTM").replace(os.sep, "/")
    if entry.get("source_kind") == "single-file":
        return os.path.dirname(source)
    return source


def rewrite_escaping_links(slug, entry, problems):
    """Point snapshot links that escape the copied directory at the origin repo.

    A synced page still reaches anything copied alongside it, but `../docs/x.md`
    resolved against the origin checkout, which this site does not carry — so those
    references become GitHub URLs at sync time and stay verbatim otherwise.
    """
    dst_dir = os.path.join(PRODUCTS_DIR, slug)
    repo = entry["repo"]
    branch = entry.get("branch", "main")
    base = _origin_base(entry)
    rewritten = 0

    for root, _, files in os.walk(dst_dir):
        sub = os.path.relpath(root, dst_dir).replace(os.sep, "/")
        sub_dir = "" if sub == "." else sub
        for name in files:
            if not name.endswith(".html"):
                continue
            path = os.path.join(root, name)
            with open(path, encoding="utf-8") as f:
                html = f.read()

            def fix(m):
                nonlocal rewritten
                attr, url, tail = m.group(1), m.group(2), m.group(3)
                if not url or "${" in url or url.startswith((
                        "http://", "https://", "mailto:", "tel:", "#", "data:",
                        "javascript:", "/")):
                    return m.group(0)
                clean = url.split("#")[0].split("?")[0]
                if not clean:
                    return m.group(0)
                local = posixpath.normpath(posixpath.join(sub_dir, clean))
                if not local.startswith(".."):
                    if os.path.exists(os.path.join(dst_dir, local.replace("/", os.sep))):
                        return m.group(0)  # shipped alongside the page
                    if clean.lower().endswith("favicon.svg"):
                        rewritten += 1
                        return f"{attr}/favicon.svg{tail}"  # missing upstream
                    return m.group(0)

                origin = posixpath.normpath(posixpath.join(base, sub_dir, clean))
                if origin.startswith(".."):
                    problems.append(f"{slug}: {name} links above the origin repo: {url}")
                    return m.group(0)
                is_asset = bool(ASSET_RE.search(clean))
                if is_asset:
                    target = f"https://raw.githubusercontent.com/{repo}/{branch}/{origin}"
                else:
                    target = f"https://github.com/{repo}/blob/{branch}/{origin}"
                rewritten += 1
                return f'{attr}{target}{tail}'

            new = re.sub(r'((?:href|src)=")([^"]*)(")', fix, html)
            if new != html:
                with open(path, "w", encoding="utf-8") as f:
                    f.write(new)
    return rewritten


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
        shutil.copytree(src, dst, ignore=shutil.ignore_patterns(".*"))
    n = rewrite_escaping_links(slug, entry, problems)
    if n:
        print(f"    {slug}: repointed {n} link(s) at {entry['repo']}")
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


def _resolves_on_site(path):
    """Does this site actually serve a root-absolute path?

    Snapshots are served from /GTM/products/<slug>/, so '/x' resolves against the
    host root no matter what the origin repo intended. That is only harmless when
    the host really has /x — otherwise the mirrored page ships a dead link.
    """
    rel = path.lstrip("/")
    if not rel:
        return True
    target = os.path.join(BASE, rel.replace("/", os.sep))
    return os.path.exists(target) or os.path.exists(os.path.join(target, "index.html"))


def verify_snapshot(e, problems):
    """Validate the committed snapshot for one manifest entry (no source repo needed)."""
    slug = e["slug"]
    if e["type"] == "page":
        index = os.path.join(PRODUCTS_DIR, slug, "index.html")
        if not os.path.exists(index):
            problems.append(f"{slug}: GTM/products/{slug}/index.html missing (run sync)")
            return
        with open(index, encoding="utf-8") as f:
            html = f.read()
        if BACKLINK_MARKER not in html:
            problems.append(f"{slug}: back-link chip missing (re-run sync)")
        for m in re.finditer(r'(?:src|href)="(/(?!/)[^"]*)"', html):
            path = m.group(1).split("#")[0].split("?")[0]
            if not _resolves_on_site(path):
                problems.append(f"{slug}: absolute ref {path} resolves nowhere on this site")
    elif e["type"] == "docs":
        if not os.path.exists(os.path.join(DOCS_DIR, slug, "index.html")):
            problems.append(f"{slug}: docs page missing (run sync)")


def check(entries, problems):
    """Local pre-sync validation: source repos present + snapshots consistent."""
    for e in entries:
        if e["type"] == "internal" or e.get("private"):
            continue
        src = os.path.join(WORKSPACE, e["repo"], e.get("source", "GTM"))
        if not os.path.exists(src):
            problems.append(f"{e['slug']}: source missing {e.get('source')}")
            continue
        verify_snapshot(e, problems)
    _check_stray_dirs(entries, problems)


def check_committed(entries, problems):
    """CI validation on the committed tree only — no sibling repos required."""
    for e in entries:
        if e["type"] == "internal" or e.get("private"):
            continue
        verify_snapshot(e, problems)
    for e in entries:
        if not e.get("private"):
            continue
        slug = e["slug"]
        for leaked in (os.path.join(PRODUCTS_DIR, slug), os.path.join(DOCS_DIR, slug)):
            if os.path.exists(leaked):
                problems.append(
                    f"{slug}: private product still published at {os.path.relpath(leaked, BASE)}"
                    " (move to _attic/gtm-private/)")
    _check_stray_dirs(entries, problems)


def _check_stray_dirs(entries, problems):
    slugs = {e["slug"] for e in entries}
    for name in sorted(os.listdir(PRODUCTS_DIR)) if os.path.isdir(PRODUCTS_DIR) else []:
        if name not in slugs and os.path.isdir(os.path.join(PRODUCTS_DIR, name)):
            problems.append(f"stray dir GTM/products/{name}/ not in manifest (archive to _attic/)")


def main():
    check_only = "--check" in sys.argv[1:]
    committed_only = "--check-committed" in sys.argv[1:]
    entries = load_manifest()
    problems = []
    if committed_only:
        check_committed(entries, problems)
    elif check_only:
        check(entries, problems)
    else:
        done = 0
        skipped_private = 0
        for e in entries:
            if e.get("private"):
                skipped_private += 1
                continue
            if e["type"] == "page":
                if sync_page(e, problems):
                    done += 1
            elif e["type"] == "docs":
                if sync_docs(e, problems):
                    done += 1
        print(f"  synced {done} product(s) → GTM/products/ + _gtm_docs/")
        if skipped_private:
            print(f"  withheld {skipped_private} private product(s) (snapshots in _attic/gtm-private/)")
        check(entries, problems)

    if problems:
        print(f"\n  ❌ {len(problems)} problem(s):")
        for p in problems:
            print(f"     {p}")
        sys.exit(1)
    print("  ✅ all GTM products verified" if check_only or committed_only else "  ✅ sync clean")


if __name__ == "__main__":
    main()
