# Design — Allen Galler (allengaller.github.io)

A locked design system for this site. Every page reads this file before
emitting code. Do not regenerate per page — extend or amend this file when
the system needs to grow.

## Genre

editorial — Editorial × Technical, content-led, calm density, mono accent
discipline. The site is a personal-brand hub (home + GTM portal + topic
pages), not a marketing site; ornamentation is restrained, typography and
hierarchy carry the brand.

## Theme

Light only — dark mode was removed; the site is locked to a professional
light theme. Single warm accent + secondary gold for tiny highlights only.
Text tokens meet WCAG AA (≥ 4.5:1) on `--bg`.

| Token | Value | Role |
| --- | --- | --- |
| `--bg` | `#fcfcfa` | Page surface (paper) |
| `--bg-subtle` | `#f4f3ee` | Raised surface |
| `--bg-hover` | `#eceae4` | Hover wash |
| `--ink` | `#14130f` | Primary text |
| `--ink-soft` | `#2b2a26` | Secondary text |
| `--text-secondary` | `#4a4842` | Tertiary text |
| `--text-muted` | `#6f6c63` | Meta / labels (5.1:1 on `--bg`) |
| `--text-faint` | `#767369` | Smallest captions that still carry meaning (4.6:1 — AA floor) |
| `--ornament` | `#b8b5ac` | Decoration only, 2.0:1 — never text a person must read |
| `--border` | `#e2dfd6` | Hairline divider |
| `--border-hover` | `#cdc9bc` | Hairline on hover |
| `--border-strong` | `#14130f` | Strong border |
| `--accent` | `#b4442c` (brick terracotta) | Single warm accent (≤5 % per page), 5.3:1 on `--bg` |
| `--accent-soft` | `rgba(180,68,44,.08)` | Accent wash (selection / hover / em-underline) |
| `--accent-fg` | `#ffffff` | Text on accent |
| `--accent-dark` | `#93351f` | Accent ink — hover on accent surfaces, and small text sitting on `--accent-soft` (raw `--accent` on the wash is 4.45:1, below AA) |
| `--gold` | `#b08a3e` | Secondary accent (tiny highlights: chapter marks, em-underline; large display numerals) — 3.1:1, never small text |
| `--gold-ink` | `#876629` | Same hue at 5.2:1 — the only gold allowed to carry text (eyebrows, mono labels, badges) |
| `--gold-soft` | `rgba(176,138,62,.14)` | Gold wash |
| `--selection-bg` | `#b4442c` | Text selection |
| `--selection-fg` | `#ffffff` | Selection text |
| `--focus-ring` | `0 0 0 2px var(--bg), 0 0 0 4px var(--accent)` | Visible focus halo |
| `--atmosphere` | `radial-gradient(ellipse 90 % 60 % at 80 % −10 %, rgba(180,68,44,.06), transparent 60 %)` | Hero glow (very subtle) |

### Contrast audit scope

The AA floor above holds for **every first-party page** (home, topic, repos,
licensing, 404, the `/GTM/` portal, and the 76 build-generated `/repos/**`
pages). Two classes of hit are knowingly accepted:

- **`/GTM/products/**`** — verbatim upstream mirrors (see Page taxonomy: "mirror
  only, do not edit"). Each carries its own `<style>` block with a dark ink
  palette; restyling them would break the fidelity that makes the snapshot
  useful as evidence. Their accessibility is the upstream author's.
- **`.ornament` (`✦`) at 2.0:1** — the glyph is `aria-hidden="true"` and sits
  beside a text heading that already carries the meaning, so WCAG treats it as
  pure decoration and sets no floor.

## Typography

| Role | Face | Weight | Notes |
| --- | --- | --- | --- |
| Display | **Fraunces** (variable serif, opsz 9–144, SOFT/WONK axes) | 400–560 | hero h1, section h1, page h1. All roman (no italic). |
| Body | **Geist** | 400 (300 for hairlines) | paragraphs, descriptions, nav, buttons |
| Mono | **JetBrains Mono** | 400/500 | eyebrow labels, meta, code blocks, .stat labels, .tag |

Type scale:
- h1 (home): `clamp(4.5rem, 14vw, 9rem)` weight 400, Fraunces opsz 144 SOFT 30 WONK 0, letter-spacing −0.05em, line-height 0.85
- h1 (page-header / gtm / personal): `clamp(1.875rem, 5vw, 2.75rem)` weight 500, letter-spacing −0.03em
- h1 (gtm-h1): `clamp(2.5rem, 5.4vw, 4.3rem)` weight 560, letter-spacing −0.02em
- h1 (gtmp-h1): `clamp(2.4rem, 5vw, 3.9rem)` weight 560, letter-spacing −0.015em
- h2 (section-title): mono uppercase 0.72 rem, weight 500, letter-spacing 0.18 em, color `--text-muted`, optional `01 ·` numeric prefix
- h3 (card title): `clamp(1.0625rem, 1.4vw, 1.25rem)` weight 500
- body: `1rem / 1.6`
- small: `0.875 rem`
- mono-meta: `0.72 rem`, letter-spacing 0.06 em

## Spacing & Geometry

- 4-pt scale: `--space-1=4, -2=8, -3=12, -4=16, -5=24, -6=32, -7=48, -8=64, -9=96`
- `--radius` = 4 px (default), `--radius-sm` = 2 px (chips, tags)
- `--max-width` = 720 px (prose), `--max-width-wide` = 1080 px (cards/grids)
- `--nav-height` = 56 px, `--gutter` = 24 px (desktop) / 20 px (mobile)
- Borders use `1 px` hairlines, not shadows.

## Motion

- Easings: `--ease-out: cubic-bezier(.16, 1, .3, 1)`, `--ease-in-out: cubic-bezier(.65, 0, .35, 1)`, `--ease-spring: cubic-bezier(.34, 1.56, .64, 1)`
- Durations: `--dur-fast` 180 ms, `--dur-base` 320 ms, `--dur-slow` 600 ms
- Reveal: `.js [data-reveal]` (the `.js` class is set by a synchronous inline script in `<head>`) is hidden `opacity:0; translateY(24px); filter:blur(4px)`; IO adds `.is-revealed`. A page whose script never runs — JS off, CSP, a 404 on `site.js` — therefore shows its content instead of a blank document. `prefers-reduced-motion: reduce` forces `opacity:1; transform:none; filter:none`, i.e. the content is simply there.
- Easing applies to `transform` and `opacity` only — never layout properties.

## Microinteractions stance

- Silent success (no celebratory toast).
- Hover delay 0 ms (instant). Tooltips 800 ms.
- Plain links underline on `:hover` / `:active`; components that already carry their own hover cue (`.btn`, `.site-nav a`, `.footer-license`) opt out. Never `opacity` on hover — it drops already-muted text below 4.5:1 and looks washed out on inverted surfaces.
- Focus ring uses `--focus-ring` (halo around element), never animates in. Under `forced-colors: active` every ring falls back to `outline: 2px solid Highlight`, because high-contrast mode discards `box-shadow`.
- All interactive elements MUST design **all 8 states**: default, hover, `:focus-visible`, `:active`, disabled, loading, error, success.
- Animations animate `transform` / `opacity` only.

## CTA voice

- Primary: filled `--accent`, `--accent-fg` text, `--radius` 4 px, padding `0.6rem 1rem`. Label is action verb + object.
- Secondary: outline `var(--border-strong)` 1 px, transparent fill, ink text. On hover, fills `--bg-hover`.
- Tertiary: text + small arrow `→` or `↗`.

## Per-page allowances

- **Home / personal / about / projects / repos / 404** — typography-led, no enrichment.
- **topic/links, topic/ai-tools, topic/archive** — long lists; pagination optional; no decoration.
- **GTM portal (/GTM/)** — typography + Fraunces display with thin gold underline on em; three grouped card grids; closing CTA block. **This is the only page that uses the gold `em` underline.**

## What every page MUST share

- Accent colour and placement (≤ 5 % per viewport).
- Fraunces + Geist + JetBrains Mono pairing.
- CTA shape (border-radius 4 px, padding rhythm 0.6 × 1 rem).
- Section heading rhythm (mono uppercase `0.72 rem` eyebrow + display h1 / h2 below).
- Reveal mechanism (`[data-reveal]` IO + `prefers-reduced-motion` collapse).
- Hairline borders, no shadows.

## What pages MAY differ on

- **Hero density** — Home uses Fraunces over-size hero (`clamp(4.5rem, 14vw, 9rem)`). GTM uses mid-weight display h1 (`clamp(2.5rem, 5.4vw, 4.3rem)`). Personal mirrors GTM.
- **Section set** — Home: hero / stats / featured / audience / collab. GTM: opening / featured / groups / close. Personal: hero / three stations / methods.
- **Footer depth** — Home/Personal: 1-line meta + 2-line sub. Topic pages: trimmed. 404: minimal.

## Correction clauses (anti-AI-slop)

These MUST hold across every page; an audit that finds any of these failing is
a stop-ship:

1. **No italic display headings.** `<em>` inside an `<h1>`/`<h2>`/`<h3>` is rendered with `font-style: normal` + accent colour + 2 px gold underline (`text-underline-offset: 0.14em`). Body copy `<em>` inside `<p>` may use italic — that's body emphasis, not display.
2. **Honest metrics.** Stats come from a real source. `4500+ docs / 5+ years` are seeded counts the user supplied; every other count is derived at build time — `{{ gtm_total }}` / `{{ gtm_cards }}` from `_data/gtm-products.json`, and `{{ stat.* }}` (repos, orgs, knowledge bases, tools, archive entries, AI tools, featured projects) from `_data/repos.json` and the listing pages themselves. Never hand-type a number a `grep` can count, and never invent "+47 %" or "trusted by 50,000+".
3. **No decorative ornament glyphs.** No standalone ✦ / ❒ / ◊ / ⌘ as visual decoration in section breaks; arrows are functional (`→`/`↗`) or absent.
4. **Locked component voice for the reach/featured/closing sections on home.** Reach rows (`.reach-item`): two-digit number + title + one-line description + a functional `→`; no icon. Featured cards (`.featured-card`): title + one-line description + the repo URL line; no image — the six project banners these cards once led with are archived (`_attic/banners/`), together with the `.project-grid` / `.project-banner` / `.project-list` CSS that rendered them (`_attic/css/main__project-card-list.css`). Closing is prose + a `.btn` row.
5. **Re-drawn chrome forbidden.** No fake browser bars / fake code-block windows / fake IDE frames. Screenshots are wrapped in `<figure>` with optional hairline border.
6. **No two-line clickable text.** Buttons / nav links / footer links / CTAs render on one line at all viewports (no horizontal squeeze that forces wrap). Mobile nav scrolls horizontally if needed.

## Exports

### tokens.css

The `:root` block lives at the top of `assets/css/main.css` and is the single
source of truth for every page. Pages MUST consume tokens by name
(`var(--accent)`), never inline hex / rgb / hsl / OKLCH values outside the
token block.

### Tailwind v4 `@theme` (not in use)

This project is plain HTML + CSS. Tailwind is intentionally not adopted.

### DTCG `tokens.json` (not in use)

DTCG format is reserved for a future tool integration.

### shadcn/ui CSS variables (not in use)

No shadcn dependency.

## Page taxonomy

| Route | Front matter source | Layout | Build deps |
| --- | --- | --- | --- |
| `/` | front matter in `index.html` | `default` | `_data/gtm-products.json` (for `{{ gtm_total }}`) |
| `/about/` | front matter | `default` | — |
| `/projects/` | front matter | `default` | — |
| `/repos/` | front matter | `default` | — |
| `/topic/links/` | front matter | `default` | — |
| `/topic/ai-tools/` | front matter | `default` | — |
| `/topic/archive/` | front matter | `default` | — |
| `/licensing/` | front matter | `default` | — |
| `/404.html` | front matter | `default` | — (excluded from sitemap) |
| `/GTM/` | front matter | `default` | `_data/gtm-products.json` (for `{{ gtm_total }}` + `{{ gtm_cards }}`) |
| `/GTM/products/allengaller/` | front matter, authored as `GTM/personal/index.html` | `default` | — |
| `/GTM/products/<slug>/` | **mirror only**, do not edit | `default` | — |
| `/_gtm_docs/<slug>/` | **mirror only**, do not edit | `default` | — |

`_data/gtm-products.json` is the **single source of truth** for GTM counts,
groups, badges, and card layouts. Both `/GTM/` and `/` consume it via the
build-time `{{ gtm_total }}` / `{{ gtm_cards }}` placeholders.

"Mirror only, do not edit" forbids hand edits and forbids `build.py` injecting
site chrome into a mirror (that is why the mirrors sit outside `PAGES` /
`STATIC_FILES`). It does not forbid the two transforms `_scripts/sync-gtm.py`
applies while writing the snapshot, because they are re-derived from the source
on every sync and `--check-committed` re-runs them before comparing:

- repo-relative asset/doc links rewritten to absolute `github.com` URLs, so a
  mirror never resolves a link against this domain;
- a ~682-byte back-link chip (marker comment + `<a class="gtmp-back">` + its own
  `<style>`) inserted before `</body>`, so each mirror page has one way back to
  `/GTM/`. 19 pages carry it — 13 KB across the whole site. It is stripped and
  re-inserted, so re-running sync is idempotent.

### URL shape and metadata

GitHub Pages 301-redirects an extensionless path to its trailing-slash form, so
the slash form is the only URL worth advertising. Every published URL comes from
one helper, `build.py:_dir_url()`, and the canonical, `og:url`, `hreflang` and
sitemap `<loc>` all read it — they cannot drift apart.

- **canonical** — trailing slash on every page, `/` for the home page.
- **hreflang** — a single `x-default`. One language at one URL; a `zh-CN`
  alternate would only point back at the page it sits on.
- **sitemap `<lastmod>`** — emitted for `/repos/**` only, from the repo's real
  commit date. Hand-written pages and GTM mirrors carry no per-page date, and a
  build-clock `lastmod` resets every run and churns the crawler's cache.
- **repo tagline / meta description / `SoftwareSourceCode.description`** — one
  path through `build.py:_plain()`, which drops README heading, badge, link and
  emphasis syntax before it can reach a search snippet.
- **robots.txt** blocks `/404.html`; nothing else is private (`_attic/` is never
  built, so it never reaches `_site/`).

Knowingly not done — each would invent data rather than correct it:

- `og:type` stays `website` everywhere, including repo pages: there are no
  articles here, and `article` would promise authorship metadata the pages
  do not carry.
- no `twitter:site`: there is no verifiable X handle for this identity.
- `SoftwareSourceCode.url` points at GitHub on purpose — `url` is where the
  *item* lives, `codeRepository` where it is cloned; the page's own address is
  already the document canonical.


## Maintenance rules

- When extending, edit this file *first*, then implement.
- When amending the colour system, keep the light theme AA-compliant (≥ 4.5:1 for text).
- When changing the type scale, prefer adjusting the existing h1 sizes
  before introducing new variants.
- Do not introduce new icon libraries. Arrows live as inline SVG or text.
- Never delete a section heading rhythm from a page; keep mono eyebrow +
  display h1 pattern.