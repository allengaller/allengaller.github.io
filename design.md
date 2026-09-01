# Design — Allen Galler 曹亚仑 (allengaller.github.io)

A locked design system for this site. Every page reads this file before
emitting code. Do not regenerate per page — extend or amend this file when
the system needs to grow.

## Genre

editorial — Editorial × Technical, content-led, calm density, mono accent
discipline. The site is a personal-brand hub (home + GTM portal + topic
pages), not a marketing site; ornamentation is restrained, typography and
hierarchy carry the brand.

## Theme

Light/dark auto via `prefers-color-scheme`. Single warm accent + secondary
gold for tiny highlights only.

| Token | Light | Dark | Role |
| --- | --- | --- | --- |
| `--bg` | `#fbfaf7` | `#0b0a08` | Page surface (paper) |
| `--bg-subtle` | `#f3f1ec` | `#131210` | Raised surface |
| `--bg-hover` | `#ebe8e1` | `#1c1b18` | Hover wash |
| `--ink` | `#14130f` | `#f5f3ee` | Primary text |
| `--ink-soft` | `#2b2a26` | `#d4d1c8` | Secondary text |
| `--text-secondary` | `#4a4842` | `#b4b1a8` | Tertiary text |
| `--text-muted` | `#8a877e` | `#7a7872` | Meta / labels |
| `--text-faint` | `#b8b5ac` | `#4a4944` | Disabled / hairlines |
| `--border` | `#e2dfd6` | `#2a2925` | Hairline divider |
| `--border-hover` | `#cdc9bc` | `#3d3c37` | Hairline on hover |
| `--border-strong` | `#14130f` | `#f5f3ee` | Strong border (dark-on-light / light-on-dark) |
| `--accent` | `#c8553d` (terracotta) | `#e07858` | Single warm accent (≤5 % per page) |
| `--accent-soft` | `rgba(200,85,61,.08)` | `rgba(224,120,88,.12)` | Accent wash (selection / hover / em-underline) |
| `--accent-fg` | `#ffffff` | `#0b0a08` | Text on accent |
| `--gold` | `#b08a3e` | `#d4a857` | Secondary accent (tiny highlights: chapter marks, em-underline) |
| `--gold-soft` | `rgba(176,138,62,.14)` | `rgba(212,168,87,.16)` | Gold wash |
| `--selection-bg` | `#c8553d` | `#e07858` | Text selection |
| `--selection-fg` | `#ffffff` | `#0b0a08` | Selection text |
| `--focus-ring` | `0 0 0 2px var(--bg), 0 0 0 4px var(--accent)` | same | Visible focus halo |
| `--atmosphere` | `radial-gradient(ellipse 90 % 60 % at 80 % −10 %, rgba(200,85,61,.06), transparent 60 %)` | `rgba(224,120,88,.08)`)` | Hero glow (very subtle) |

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
- Reveal: `[data-reveal]` elements are hidden `opacity:0; translateY(24px); filter:blur(4px)`; IO adds `.is-revealed`. Respect `prefers-reduced-motion: reduce` → opacity-only ≤150 ms crossfade, no translate/blur.
- Easing applies to `transform` and `opacity` only — never layout properties.

## Microinteractions stance

- Silent success (no celebratory toast).
- Hover delay 0 ms (instant). Tooltips 800 ms.
- Focus ring uses `--focus-ring` (halo around element), never animates in.
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
2. **Honest metrics.** Stats come from a real source. `4500+ docs / 10+ tools / 5+ years` are seeded counts the user supplied; `{{ gtm_total }}` is injected from `_data/gtm-products.json` at build time. Never invent "+47 %" or "trusted by 50,000+".
3. **No decorative ornament glyphs.** No standalone ✦ / ❒ / ◊ / ⌘ as visual decoration in section breaks; arrows are functional (`→`/`↗`) or absent.
4. **Locked component voice for the audience/featured/collab sections on home.** Audience cards: title + description, no icon. Featured cards: banner image (when project provides one) + type label + title + description + tag row.
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
| `/404.html` | none (special) | none | — |
| `/GTM/` | front matter | `default` | `_data/gtm-products.json` (for `{{ gtm_total }}` + `{{ gtm_cards }}`) |
| `/GTM/personal/` | front matter | `default` | — |
| `/GTM/products/<slug>/` | **mirror only**, do not edit | `default` | — |
| `/_gtm_docs/<slug>/` | **mirror only**, do not edit | `default` | — |

`_data/gtm-products.json` is the **single source of truth** for GTM counts,
groups, badges, and card layouts. Both `/GTM/` and `/` consume it via the
build-time `{{ gtm_total }}` / `{{ gtm_cards }}` placeholders.

## Maintenance rules

- When extending, edit this file *first*, then implement.
- When amending the colour system, keep both light + dark in lockstep.
- When changing the type scale, prefer adjusting the existing h1 sizes
  before introducing new variants.
- Do not introduce new icon libraries. Arrows live as inline SVG or text.
- Never delete a section heading rhythm from a page; keep mono eyebrow +
  display h1 pattern.