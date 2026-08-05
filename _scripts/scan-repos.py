#!/usr/bin/env python3
"""
Scan the local GitHub mirror (~/Documents/GitHub/) and produce _data/repos.yml.

This script READS from every repo to extract metadata, but WRITES only to
_data/repos.yml inside this workspace. No other project's files are modified.

For each repo we extract:
  - org, name, full_name       (from remote URL)
  - path                       (local absolute path, relative to scan root)
  - branch                     (default branch)
  - last_commit                (date + relative age + subject)
  - commits_total              (commit count)
  - description                (from .git/description, or first README paragraph)
  - readme_excerpt             (first 200 chars of README, plain text)
  - languages                  (top-3 by file count, with counts)
  - size_kb                    (working-tree size)
  - private                    (whether origin URL uses SSH or HTTPS w/o public path)
  - has_remote                 (whether it has any remote configured)
  - repo_type                  ("site" / "tool" / "database" / "library" / "other")

Usage:
  python3 _scripts/scan-repos.py                 # default scan
  python3 _scripts/scan-repos.py --root /path    # custom scan root
  python3 _scripts/scan-repos.py --exclude NAME  # exclude a repo by name
  python3 _scripts/scan-repos.py --dry-run       # print summary, don't write
"""
import os
import re
import sys
import json
import yaml
import subprocess
import argparse
from collections import Counter
from datetime import datetime, timezone


# ── Defaults ────────────────────────────────────────
DEFAULT_ROOT = os.path.expanduser("~/Documents/GitHub")
WORKSPACE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_OUTPUT = os.path.join(WORKSPACE, "_data", "repos.yml")

# Repos to skip from the listing (always)
DEFAULT_EXCLUDES = {
    "allengaller.github.io",  # this very site
}

# File-extension → language guess (covers most common cases)
LANG_MAP = {
    ".py": "Python", ".js": "JavaScript", ".ts": "TypeScript",
    ".tsx": "TypeScript", ".jsx": "JavaScript", ".go": "Go",
    ".rs": "Rust", ".java": "Java", ".kt": "Kotlin", ".swift": "Swift",
    ".rb": "Ruby", ".php": "PHP", ".cs": "C#", ".cpp": "C++", ".c": "C",
    ".h": "C", ".hpp": "C++", ".sh": "Shell", ".bash": "Shell",
    ".zsh": "Shell", ".ps1": "PowerShell", ".sql": "SQL",
    ".html": "HTML", ".css": "CSS", ".scss": "SCSS", ".sass": "Sass",
    ".vue": "Vue", ".svelte": "Svelte", ".md": "Markdown",
    ".yaml": "YAML", ".yml": "YAML", ".json": "JSON",
    ".toml": "TOML", ".rs": "Rust", ".ex": "Elixir", ".exs": "Elixir",
    ".scala": "Scala", ".clj": "Clojure", ".lua": "Lua",
    ".dart": "Dart", ".r": "R", ".jl": "Julia", ".pl": "Perl",
    ".ipynb": "Jupyter", ".mdx": "MDX",
}

# Heuristics to classify repo purpose
KEYWORD_TO_TYPE = [
    (re.compile(r"\.github\.io$|site|website|homepage|blog|portal", re.I), "site"),
    (re.compile(r"database|corpus|knowledge[- ]?base|database[- ]?of|kg[- ]?db", re.I), "database"),
    (re.compile(r"^(lib|library|sdk|framework|kit|engine|core|util|tool|cli|server|client|api|bot|agent|orchestrator|operator|daemon|service|workflow|pipeline|compiler|parser|lexer|interpreter|kernel|driver|module|extension|plugin|bridge|adapter|provider|integration|spec|protocol|schema|grammar|runtime|shell|terminal|prompt)$", re.I), "tool"),
    (re.compile(r"^(?!.*(?:database|corpus|kg|graph)).*db$|databases?", re.I), "database"),
    (re.compile(r"^book$|^pub$|^press$|^publisher$|^writing", re.I), "book"),
    (re.compile(r"^(me-|i-)|^(me|self|personal|profile)$|^the-.*-me$", re.I), "personal"),
]

# Folders we never descend into (IDE / tooling / system noise)
SKIP_DIRS = {
    "node_modules", ".venv", "venv", "__pycache__", ".pytest_cache",
    "target", "build", "dist", ".next", ".nuxt", ".gradle", ".terraform",
    ".idea", ".vscode", ".obsidian", ".qoder", ".claude", ".agents",
    ".hermes", "vendor", "_site", ".git", "backup_*",
}


def run(cmd, cwd=None, timeout=10):
    """Run shell command and return stripped stdout, or empty string on error."""
    try:
        out = subprocess.run(
            cmd, cwd=cwd, capture_output=True, text=True,
            timeout=timeout, check=False,
        )
        return (out.stdout or "").strip()
    except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
        return ""


def get_remote_info(repo_path):
    """Return (host, org, name) from origin URL, or (None, None, None)."""
    url = run(["git", "config", "--get", "remote.origin.url"], cwd=repo_path)
    if not url:
        return None, None, None
    # ssh:    git@github.com:org/name.git
    # https:  https://github.com/org/name.git
    m = re.match(r"(?:git@|https://)([^:/]+)[:/]([^/]+)/([^/]+?)(?:\.git)?$", url)
    if not m:
        return None, None, None
    return m.group(1), m.group(2), m.group(3)


def get_default_branch(repo_path):
    """Return default branch name (HEAD's symbolic ref or first branch)."""
    head = run(["git", "symbolic-ref", "--short", "HEAD"], cwd=repo_path)
    if head:
        return head
    # fall back: find branches, prefer main/master
    branches = run(["git", "branch", "--format=%(refname:short)"], cwd=repo_path)
    if branches:
        for prefer in ("main", "master", "trunk", "develop"):
            if prefer in branches.splitlines():
                return prefer
        return branches.splitlines()[0]
    return "(unknown)"


def get_last_commit(repo_path):
    """Return (iso_date, relative_age, subject)."""
    iso = run(["git", "log", "-1", "--format=%aI"], cwd=repo_path)
    rel = run(["git", "log", "-1", "--format=%ar"], cwd=repo_path)
    subj = run(["git", "log", "-1", "--format=%s"], cwd=repo_path)
    return iso, rel, subj


def get_total_commits(repo_path):
    """Total commit count on default branch."""
    n = run(["git", "rev-list", "--count", "HEAD"], cwd=repo_path)
    try:
        return int(n)
    except (ValueError, TypeError):
        return 0


def get_git_description(repo_path):
    """Read .git/description (often set by GitHub on clone)."""
    desc_path = os.path.join(repo_path, ".git", "description")
    try:
        with open(desc_path) as f:
            text = f.read().strip()
        # GitHub default placeholder
        if "Unnamed repository" in text or not text:
            return ""
        return text
    except (FileNotFoundError, IOError):
        return ""


def get_readme_excerpt(repo_path, max_chars=200):
    """Read first paragraph from README.md / README.markdown / README (uppercased)."""
    for name in ("README.md", "README.markdown", "README.MD", "README", "readme.md"):
        p = os.path.join(repo_path, name)
        if not os.path.exists(p):
            continue
        try:
            with open(p) as f:
                text = f.read()
        except (FileNotFoundError, IOError, UnicodeDecodeError):
            continue
        # Strip frontmatter
        text = re.sub(r"^---\n.*?\n---\n", "", text, count=1, flags=re.DOTALL)
        # Strip HTML
        text = re.sub(r"<[^>]+>", "", text)
        # Collapse whitespace, take first paragraph
        text = re.sub(r"\n\s*\n+", "\n\n", text).strip()
        # Skip leading headings
        for line in text.split("\n\n")[0].splitlines():
            if line.strip().startswith("#"):
                continue
            if line.strip():
                excerpt = line.strip()
                if len(excerpt) > max_chars:
                    excerpt = excerpt[: max_chars - 1] + "…"
                return excerpt
        if text:
            excerpt = text.split("\n\n")[0].strip()[: max_chars]
            return excerpt
    return ""


def get_readme_full(repo_path, max_chars=200_000):
    """Read the full README content (markdown), stripping frontmatter.

    Returns raw markdown string, or empty string if no README found.
    Cap at max_chars (~200KB) to avoid pathologically large files.
    """
    for name in ("README.md", "README.markdown", "README.MD", "README", "readme.md"):
        p = os.path.join(repo_path, name)
        if not os.path.exists(p):
            continue
        try:
            with open(p, encoding="utf-8", errors="replace") as f:
                text = f.read()
        except (FileNotFoundError, IOError):
            continue
        # Strip frontmatter
        text = re.sub(r"^---\n.*?\n---\n", "", text, count=1, flags=re.DOTALL)
        if len(text) > max_chars:
            text = text[:max_chars] + "\n\n…(内容过长，已截断)"
        return text
    return ""


def get_recent_commits(repo_path, n=10):
    """Return list of {hash, short, iso, rel, author, subject} for last n commits."""
    fmt = "%H%x1f%h%x1f%aI%x1f%an%x1f%s"
    out = run(["git", "log", f"-{n}", f"--format={fmt}"], cwd=repo_path)
    rels_out = run(["git", "log", f"-{n}", "--format=%ar"], cwd=repo_path)
    rels = rels_out.splitlines()
    commits = []
    for i, line in enumerate(out.splitlines()):
        parts = line.split("\x1f")
        if len(parts) < 5:
            continue
        h, short, iso, author, subject = parts[:5]
        rel = rels[i] if i < len(rels) else ""
        commits.append({
            "hash": h,
            "short": short,
            "iso": iso,
            "rel": rel,
            "author": author,
            "subject": subject,
        })
    return commits


def get_languages_detailed(repo_path, max_depth=4, max_files=5000):
    """Like get_languages but returns full top-5 list, not just top-3."""
    counter = Counter()
    file_count = 0
    try:
        for dirpath, dirnames, filenames in os.walk(repo_path):
            dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS and not d.startswith(".")]
            rel = os.path.relpath(dirpath, repo_path)
            depth = 0 if rel == "." else rel.count(os.sep) + 1
            if depth > max_depth:
                dirnames[:] = []
                continue
            for fn in filenames:
                ext = os.path.splitext(fn)[1].lower()
                if ext in LANG_MAP:
                    counter[LANG_MAP[ext]] += 1
                    file_count += 1
                    if file_count >= max_files:
                        return counter.most_common(10)
        return counter.most_common(10)
    except (OSError, PermissionError):
        return counter.most_common(10)


def get_top_level_files(repo_path, max_count=15):
    """Return list of top-level files/dirs for the file tree summary."""
    try:
        entries = sorted(os.listdir(repo_path))
    except (OSError, PermissionError):
        return []
    result = []
    for e in entries:
        if e.startswith(".") or e in SKIP_DIRS:
            continue
        if len(result) >= max_count:
            result.append(f"… and {len(entries) - max_count} more")
            break
        full = os.path.join(repo_path, e)
        is_dir = os.path.isdir(full)
        result.append(e + ("/" if is_dir else ""))
    return result


def get_file_count(repo_path):
    """Total non-hidden, non-ignored file count."""
    count = 0
    try:
        for dirpath, dirnames, filenames in os.walk(repo_path):
            dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS and not d.startswith(".")]
            count += len([f for f in filenames if not f.startswith(".")])
    except (OSError, PermissionError):
        pass
    return count


def get_languages(repo_path, max_depth=3, max_files=2000):
    """Walk the working tree, count files by language. Skip noise dirs."""
    counter = Counter()
    file_count = 0
    try:
        for dirpath, dirnames, filenames in os.walk(repo_path):
            # prune
            dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS and not d.startswith(".")]
            # depth check
            rel = os.path.relpath(dirpath, repo_path)
            depth = 0 if rel == "." else rel.count(os.sep) + 1
            if depth > max_depth:
                dirnames[:] = []
                continue
            for fn in filenames:
                ext = os.path.splitext(fn)[1].lower()
                if ext in LANG_MAP:
                    counter[LANG_MAP[ext]] += 1
                    file_count += 1
                    if file_count >= max_files:
                        # early exit for huge repos
                        return counter.most_common(3)
        return counter.most_common(3)
    except (OSError, PermissionError):
        return counter.most_common(3)


def get_size_kb(repo_path):
    """Total working-tree size in KB (excluding .git and noise dirs)."""
    total = 0
    try:
        for dirpath, dirnames, filenames in os.walk(repo_path):
            dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS and not d.startswith(".")]
            for fn in filenames:
                try:
                    fp = os.path.join(dirpath, fn)
                    total += os.lstat(fp).st_size
                except (OSError, FileNotFoundError):
                    continue
        return round(total / 1024, 1)
    except (OSError, PermissionError):
        return 0


def classify_repo(name, languages, description, readme):
    """Heuristically classify repo type from name + content."""
    text = f"{name} {description} {readme}".lower()
    for pattern, type_ in KEYWORD_TO_TYPE:
        if pattern.search(text):
            return type_
    # If mostly Markdown / docs → knowledge base
    if languages and languages[0][0] in ("Markdown", "YAML", "JSON"):
        return "database"
    if languages:
        return "tool"
    return "other"


def is_github_host(host):
    return host and host.endswith("github.com")


def find_repos(root):
    """Yield (abs_path, rel_path) for every repo under root."""
    if not os.path.isdir(root):
        return
    for dirpath, dirnames, filenames in os.walk(root):
        # Don't descend into these (system / noise)
        dirnames[:] = [
            d for d in dirnames
            if d not in SKIP_DIRS
            and d not in {".obsidian", ".qoder", ".claude", ".agents", ".hermes", ".bundle", "node_modules"}
        ]
        if ".git" in filenames or os.path.isdir(os.path.join(dirpath, ".git")):
            yield dirpath, os.path.relpath(dirpath, root)


def scan(root, excludes, dry_run=False, verbose=True):
    """Scan root for repos, return list of dicts."""
    repos = []
    seen = set()
    for abs_path, rel_path in find_repos(root):
        # use the basename as the unique key
        name = os.path.basename(rel_path)
        if name in excludes:
            if verbose:
                print(f"  ⊘ skip: {name} (excluded)")
            continue
        if name in seen:
            if verbose:
                print(f"  ⊘ skip: {rel_path} (duplicate)")
            continue
        seen.add(name)

        host, org, repo = get_remote_info(abs_path)
        default_branch = get_default_branch(abs_path)
        iso, rel, subj = get_last_commit(abs_path)
        commits_total = get_total_commits(abs_path)
        description = get_git_description(abs_path)
        readme = get_readme_excerpt(abs_path)
        # full README markdown (only for own repos to keep size sane)
        # Extract now so we can fall back description from it
        readme_full = ""
        languages = get_languages(abs_path)
        size_kb = get_size_kb(abs_path)
        repo_type = classify_repo(name, languages, description, readme)
        is_own = host and host.endswith("github.com") and org in {
            "allengaller", "ai-guru-global", "kudig-io", "standup-coder",
            "opendemo-work", "better-call-saull", "lonely-reader-global",
            "sit-music", "peace-lab-global", "mocici-global", "panna-arts",
            "buhua-global", "cinelume", "fat-looser", "hack-core-global",
            "master-of-solitude", "xai-org", "zenx-global",
        }
        # Extract deep details only for own + github repos (skip external/bare clones)
        if is_own and host:
            readme_full = get_readme_full(abs_path)
            recent_commits = get_recent_commits(abs_path, n=10)
            languages_detailed = get_languages_detailed(abs_path)
            top_files = get_top_level_files(abs_path)
            file_count = get_file_count(abs_path)
        else:
            readme_full = ""
            recent_commits = []
            languages_detailed = languages
            top_files = []
            file_count = 0
        # fall back: description = first line of readme if empty
        if not description and readme:
            description = readme.split("。")[0].split(".")[0][:120]

        repos.append({
            "name": name,
            "org": org or "",
            "host": host or "",
            "full_name": f"{org}/{name}" if org else name,
            "path": rel_path,
            "abs_path": abs_path,
            "default_branch": default_branch,
            "last_commit_iso": iso,
            "last_commit_rel": rel,
            "last_commit_subject": subj,
            "commits_total": commits_total,
            "description": description,
            "readme_excerpt": readme,
            "readme_full": readme_full,
            "readme_bytes": len(readme_full.encode("utf-8")) if readme_full else 0,
            "recent_commits": recent_commits,
            "languages": [l for l, _ in languages],
            "languages_detailed": [
                {"lang": l, "count": c} for l, c in languages_detailed
            ],
            "language_top": languages[0][0] if languages else "",
            "size_kb": size_kb,
            "file_count": file_count,
            "top_files": top_files,
            "repo_type": repo_type,
            "is_own": bool(is_own),
            "is_github": is_github_host(host),
        })

        if verbose:
            tag = "✓" if is_own else "·"
            print(f"  {tag} {org}/{name}  ({languages[0][0] if languages else '?'})  {rel or 'just now'}")

    return repos


def write_yaml(repos, output_path):
    """Write the repos list as YAML to output_path."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    # Round-trip via dict for clean YAML
    payload = {
        "scanned_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "scan_root": os.path.expanduser("~/Documents/GitHub"),
        "total": len(repos),
        "repos": repos,
    }
    with open(output_path, "w") as f:
        yaml.safe_dump(
            payload, f,
            allow_unicode=True,
            sort_keys=False,
            default_flow_style=False,
            width=120,
        )


def write_json(repos, output_path):
    """Write lightweight repos JSON for client-side JS on /repos/ page.

    Strips abs_path (filesystem leak) and the heavy fields
    (readme_full, recent_commits, languages_detailed) that are
    only needed at build time for per-repo page generation.
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    heavy = {"abs_path", "readme_full", "recent_commits", "languages_detailed", "top_files", "file_count", "readme_bytes"}
    safe_repos = []
    for r in repos:
        sr = {k: v for k, v in r.items() if k not in heavy}
        safe_repos.append(sr)

    # Compute aggregates for the page header
    from collections import Counter
    org_counts = Counter(r["org"] for r in safe_repos if r["org"])
    type_counts = Counter(r["repo_type"] for r in safe_repos)
    lang_counts = Counter(r["language_top"] for r in safe_repos if r["language_top"])
    own_count = sum(1 for r in safe_repos if r["is_own"])
    ext_count = len(safe_repos) - own_count
    total_size = sum(r.get("size_kb", 0) for r in safe_repos)

    payload = {
        "scanned_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "total": len(safe_repos),
        "own": own_count,
        "external": ext_count,
        "total_size_mb": round(total_size / 1024, 1),
        "orgs": dict(org_counts.most_common()),
        "types": dict(type_counts.most_common()),
        "languages": dict(lang_counts.most_common(10)),
        "repos": safe_repos,
    }
    with open(output_path, "w") as f:
        json.dump(payload, f, ensure_ascii=False, separators=(",", ":"))
    return payload


def write_detailed_json(repos, output_path):
    """Write the full per-repo detail data for build-time per-repo page generation.

    Includes readme_full, recent_commits, languages_detailed, etc.
    Kept separate from the lightweight repos.json so the /repos/ page
    fetches stay fast.
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    payload = {
        "scanned_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "total": len(repos),
        "total_size": sum(r.get("readme_bytes", 0) for r in repos),
        "repos": repos,  # full data including readme_full
    }
    with open(output_path, "w") as f:
        json.dump(payload, f, ensure_ascii=False, separators=(",", ":"))
    payload["_path"] = output_path
    return payload


def main():
    ap = argparse.ArgumentParser(description="Scan local GitHub mirror → repos.yml")
    ap.add_argument("--root", default=DEFAULT_ROOT, help=f"Scan root (default: {DEFAULT_ROOT})")
    ap.add_argument("--output", default=DEFAULT_OUTPUT, help="Output YAML path")
    ap.add_argument("--json", action="store_true", help="Also write a JSON file for the /repos/ page")
    ap.add_argument("--json-output", default=None, help="JSON output path (default: <yaml>.json)")
    ap.add_argument("--detailed-json", action="store_true",
                    help="Write a detailed JSON file (includes full README, recent commits, "
                         "language stats). Used by build.py for per-repo page generation. "
                         "Auto-enabled when --json is passed.")
    ap.add_argument("--detailed-json-output", default=None,
                    help="Detailed JSON output path (default: repos-detailed.json next to repos.json)")
    ap.add_argument("--exclude", action="append", default=[], help="Repo name to exclude (can repeat)")
    ap.add_argument("--dry-run", action="store_true", help="Print summary, don't write")
    ap.add_argument("--quiet", action="store_true", help="Suppress per-repo log")
    args = ap.parse_args()

    excludes = DEFAULT_EXCLUDES | set(args.exclude)
    print(f"📡  Scanning {args.root} …")
    repos = scan(args.root, excludes, dry_run=args.dry_run, verbose=not args.quiet)

    # Sort: own repos first, then by org, then by last commit desc
    repos.sort(key=lambda r: (
        0 if r["is_own"] else 1,
        r["org"],
        -(datetime.fromisoformat(r["last_commit_iso"]).timestamp()
          if r["last_commit_iso"] else 0),
    ))

    print(f"\n  Found {len(repos)} repos "
          f"({sum(1 for r in repos if r['is_own'])} own · "
          f"{sum(1 for r in repos if not r['is_own'])} external)")

    if args.dry_run:
        print("\n  --dry-run: skipping write")
        return

    write_yaml(repos, args.output)
    print(f"\n  ✎ Wrote: {args.output}")

    if args.json:
        json_path = args.json_output or args.output.rsplit(".", 1)[0] + ".json"
        stats = write_json(repos, json_path)
        print(f"  ✎ Wrote: {json_path}  "
              f"({stats['total']} repos · {stats['own']} own · {stats['external']} ext)")

        # Auto-write detailed JSON alongside (used by build.py for per-repo pages)
        # unless explicitly disabled by NOT passing --json (i.e. only --detailed-json).
        if args.detailed_json or True:
            detailed_path = args.detailed_json_output or \
                os.path.join(os.path.dirname(json_path), "repos-detailed.json")
            d_stats = write_detailed_json(repos, detailed_path)
            total_kb = round(d_stats["total_size"] / 1024, 1)
            with_readme = sum(1 for r in repos if r.get("readme_full"))
            print(f"  ✎ Wrote: {detailed_path}  "
                  f"({d_stats['total']} repos · {with_readme} with README · {total_kb} KB)")

    elif args.detailed_json:
        # Standalone detailed-only mode (no lightweight JSON requested)
        detailed_path = args.detailed_json_output or \
            os.path.join(WORKSPACE, "_data", "repos-detailed.json")
        d_stats = write_detailed_json(repos, detailed_path)
        total_kb = round(d_stats["total_size"] / 1024, 1)
        with_readme = sum(1 for r in repos if r.get("readme_full"))
        print(f"  ✎ Wrote: {detailed_path}  "
              f"({d_stats['total']} repos · {with_readme} with README · {total_kb} KB)")

    # Quick stats
    orgs = Counter(r["org"] for r in repos if r["org"])
    print(f"  📁 {len(orgs)} orgs: {', '.join(f'{o}({c})' for o,c in orgs.most_common(8))}")


if __name__ == "__main__":
    main()
