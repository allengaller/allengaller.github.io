#!/usr/bin/env python3
"""
Quality gate for the published artifact (_site/).

Run after _scripts/build.py. Catches regressions that a successful build does
not: content that should never be published, unrendered template leftovers,
and pages missing the metadata the site depends on.

Usage:
  python3 _scripts/build.py --force && python3 _scripts/check-quality.py
"""
import json
import os
import re
import sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(BASE, "_site")
MANIFEST = os.path.join(BASE, "_data", "gtm-products.json")

REQUIRED_FILES = ["index.html", "404.html", "sitemap.xml", "feed.xml",
                  "robots.txt", "humans.txt", "manifest.webmanifest",
                  "LICENSE", "licensing/index.html"]

# Text that must never appear in a published page.
TEMPLATE_ARTIFACTS = ("{%", "{{ page.", "{{ content", "{{ site.")


def load_products():
    with open(MANIFEST, encoding="utf-8") as f:
        return json.load(f)["products"]


def html_pages():
    for root, _, files in os.walk(SITE):
        for name in files:
            if name.endswith(".html"):
                yield os.path.join(root, name)


def check_private(products, errors):
    """private:true products must not exist anywhere under _site/."""
    for p in products:
        if not p.get("private"):
            continue
        slug = p["slug"]
        for rel in (f"GTM/products/{slug}/index.html", f"_gtm_docs/{slug}/index.html"):
            if os.path.exists(os.path.join(SITE, rel)):
                errors.append(f"published a private product: {rel} ({p['repo']})")

    portal = os.path.join(SITE, "GTM", "index.html")
    if os.path.exists(portal):
        with open(portal, encoding="utf-8") as f:
            html = f.read()
        for p in products:
            if p.get("private") and f'href="/GTM/products/{p["slug"]}/"' in html:
                errors.append(f"GTM portal still links private product: {p['slug']}")

    sitemap = os.path.join(SITE, "sitemap.xml")
    if os.path.exists(sitemap):
        with open(sitemap, encoding="utf-8") as f:
            xml = f.read()
        for p in products:
            if p.get("private") and f"/GTM/products/{p['slug']}/" in xml:
                errors.append(f"sitemap lists private product: {p['slug']}")


def check_public_products(products, errors):
    """Every public product must have a built page."""
    for p in products:
        if p.get("private") or p.get("type") == "internal":
            continue
        rel = f"GTM/products/{p['slug']}/index.html"
        if not os.path.exists(os.path.join(SITE, rel)):
            errors.append(f"public product not built: {rel}")


def check_required_files(errors):
    for rel in REQUIRED_FILES:
        path = os.path.join(SITE, rel)
        if not os.path.exists(path):
            errors.append(f"missing artifact: {rel}")
        elif os.path.getsize(path) == 0:
            errors.append(f"empty artifact: {rel}")


def check_rendered_pages(errors):
    """No unrendered template syntax, leaked frontmatter, or missing SEO basics."""
    count = 0
    for path in html_pages():
        rel = os.path.relpath(path, SITE)
        count += 1
        with open(path, encoding="utf-8") as f:
            text = f.read()

        head = text[:400]
        if head.startswith("---\n") or head.startswith("---\r\n"):
            errors.append(f"{rel}: frontmatter leaked into published page")
            continue

        # GTM product snapshots are copied verbatim from their origin repos, so
        # their <head> is not ours to complete: they legitimately carry no
        # canonical for this site, and their own relative-link markup is expected.
        is_synced = rel.startswith("GTM/products/") \
            and text[:200].lower().lstrip().startswith("<!doctype") \
            and "site-nav" not in text[:4000]
        if not is_synced:
            for token in TEMPLATE_ARTIFACTS:
                if token in text:
                    errors.append(f"{rel}: unrendered template token {token!r}")
                    break

        if "<html" in text and 'lang="' not in text[:text.index("<html") + 200]:
            errors.append(f"{rel}: <html> without lang attribute")
        if "<title>" not in text or re.search(r"<title>\s*</title>", text):
            errors.append(f"{rel}: empty <title>")
        if 'name="description"' not in text:
            errors.append(f"{rel}: no meta description")
        if 'rel="canonical"' not in text:
            if not is_synced:
                errors.append(f"{rel}: no canonical link")

        for m in re.finditer(r'<script type="application/ld\+json"[^>]*>(.*?)</script>',
                             text, re.DOTALL):
            body = m.group(1).strip()
            if not body:
                errors.append(f"{rel}: empty JSON-LD block")
                continue
            try:
                json.loads(body)
            except json.JSONDecodeError as e:
                errors.append(f"{rel}: invalid JSON-LD ({e.msg} at line {e.lineno})")
    return count


def check_escaping(errors):
    """Titles rendered into <title> must not carry raw markdown or markup."""
    bad = []
    for path in html_pages():
        rel = os.path.relpath(path, SITE)
        with open(path, encoding="utf-8") as f:
            m = re.search(r"<title>(.*?)</title>", f.read(), re.DOTALL)
        if not m:
            continue
        title = m.group(1)
        if title.startswith("#") or "\\n" in title or "{" in title or "}" in title:
            bad.append((rel, title[:80]))
    for rel, title in bad:
        errors.append(f"{rel}: suspicious page title {title!r}")


def main():
    if not os.path.isdir(SITE):
        print("  ❌ _site/ not found — run python3 _scripts/build.py first")
        sys.exit(1)

    errors = []
    products = load_products()
    check_required_files(errors)
    check_private(products, errors)
    check_public_products(products, errors)
    pages = check_rendered_pages(errors)
    check_escaping(errors)

    sitemap = os.path.join(SITE, "sitemap.xml")
    located = 0
    if os.path.exists(sitemap):
        with open(sitemap, encoding="utf-8") as f:
            located = f.read().count("<loc>")

    print(f"  checked {pages} page(s), {located} sitemap URL(s), "
          f"{len(products)} GTM product(s)")
    if errors:
        unique = sorted(set(errors))
        print(f"\n  ❌ {len(unique)} quality problem(s):")
        for e in unique:
            print(f"     {e}")
        sys.exit(1)
    print("  ✅ quality gate passed")


if __name__ == "__main__":
    main()
