#!/usr/bin/env python3
"""Generate AI tools page from YAML data."""

import yaml
import os

def build_page():
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_path = os.path.join(base, "_data/ai-tools.yml")
    output_path = os.path.join(base, "topic/ai-tools/index.html")

    with open(data_path) as f:
        data = yaml.safe_load(f)

    paid = data["paid"]
    free = data["free"]

    def render_card(tool, idx, is_free=False):
        delay = idx * 0.025 if not is_free else idx * 0.04 + 0.8
        featured = " featured" if tool.get("featured") else ""
        wide = " wide" if tool.get("wide") else ""
        card_class = f"tool-card{' free-card' if is_free else ''}{featured}{wide}"

        plan = tool.get("plan", "")
        if tool.get("price"):
            plan = f'{plan} · {tool.get("price")}'

        url = tool.get("url", "")
        usage = tool.get("usage", "")

        # Render URL as clickable link
        if url and url.startswith("http"):
            url_html = f'<a href="{url}" target="_blank" rel="noopener" class="link-val link-url">{url.replace("https://", "").replace("http://", "")}</a>'
        else:
            url_html = f'<span class="link-val placeholder">{url or "—"}</span>'

        # Render usage as text
        if usage and not usage.startswith("["):
            usage_html = f'<span class="link-val">{usage}</span>'
        else:
            usage_html = f'<span class="link-val placeholder">{usage or "—"}</span>'

        return f"""
        <article class="{card_class}" style="--delay: {delay:.3f}s">
          <div class="card-top">
            <span class="card-icon">{tool.get("icon", "")}</span>
            <span class="card-name">{tool.get("name", "")}</span>
          </div>
          <div class="card-plan">{plan}</div>
          <div class="card-links">
            <div class="link-row">
              <span class="link-label">URL</span>
              {url_html}
            </div>
            <div class="link-row">
              <span class="link-label">用量</span>
              {usage_html}
            </div>
          </div>
        </article>"""

    paid_cards = "\n".join(render_card(tool, i) for i, tool in enumerate(paid))
    free_cards = "\n".join(render_card(tool, i, True) for i, tool in enumerate(free))

    html = f"""---
layout: default
nav_active_ai_tools: is-active
title: AI Tools | AI 工具链
description: Allen 的 AI 工具链清单，包含编程开发、对话助手、创作工具等订阅与用量信息。
---

<div class="ai-tools-v3">

  <header class="ai-hero">
    <span class="ai-badge">AI TOOLCHAIN</span>
    <h1 class="ai-title">我的 AI 工具链</h1>
    <p class="ai-subtitle">{len(paid)} paid · {len(free)} free</p>
  </header>

  <main class="ai-main">

    <!-- PAID SUBSCRIPTIONS -->
    <section class="ai-section">
      <div class="section-header">
        <span class="section-num">01</span>
        <h2 class="section-title">付费订阅</h2>
        <span class="section-count">{len(paid)}</span>
      </div>
      <div class="tool-grid">
{paid_cards}
      </div>
    </section>

    <!-- FREE TOOLS -->
    <section class="ai-section">
      <div class="section-header">
        <span class="section-num">02</span>
        <h2 class="section-title">免费工具</h2>
        <span class="section-count">{len(free)}</span>
      </div>
      <div class="tool-grid free-grid">
{free_cards}
      </div>
    </section>

  </main>
</div>

<style>
.ai-tools-v3 {{
  background: var(--bg);
  color: var(--text);
  min-height: 100vh;
}}
.ai-hero {{
  max-width: 1100px;
  margin: 0 auto;
  padding: 5rem 2rem 3.5rem;
  border-bottom: 1px solid var(--border);
}}
.ai-badge {{
  display: inline-block;
  font-size: 0.65rem;
  letter-spacing: 0.2em;
  color: var(--text-muted);
  text-transform: uppercase;
  margin-bottom: 1.25rem;
  animation: fadeUp 0.5s ease-out both;
}}
.ai-title {{
  font-size: clamp(2rem, 5vw, 3.25rem);
  font-weight: 600;
  letter-spacing: -0.03em;
  line-height: 1.1;
  margin-bottom: 0.6rem;
  animation: fadeUp 0.5s ease-out 0.05s both;
}}
.ai-subtitle {{
  font-size: 0.875rem;
  color: var(--text-muted);
  font-weight: 400;
  letter-spacing: 0.02em;
  animation: fadeUp 0.5s ease-out 0.1s both;
}}
.ai-main {{
  max-width: 1100px;
  margin: 0 auto;
  padding: 3rem 2rem 6rem;
}}
.ai-section {{
  margin-bottom: 4rem;
}}
.section-header {{
  display: flex;
  align-items: baseline;
  gap: 0.75rem;
  margin-bottom: 1.5rem;
}}
.section-num {{
  font-size: 0.65rem;
  color: var(--text-muted);
  letter-spacing: 0.1em;
}}
.section-title {{
  font-size: 0.95rem;
  font-weight: 500;
  letter-spacing: -0.01em;
}}
.section-count {{
  font-size: 0.75rem;
  color: var(--text-muted);
  margin-left: auto;
}}
.tool-grid {{
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
  gap: 1px;
  background: var(--border);
  border: 1px solid var(--border);
  border-radius: 6px;
  overflow: hidden;
}}
.tool-card {{
  background: var(--bg-subtle);
  padding: 1.25rem;
  display: flex;
  flex-direction: column;
  gap: 0.6rem;
  transition: background 0.15s ease;
  animation: cardReveal 0.4s ease-out var(--delay, 0s) both;
}}
.tool-card:hover {{ background: var(--bg-hover); }}
.tool-card.wide {{ grid-column: span 2; }}
@media (max-width: 540px) {{ .tool-card.wide {{ grid-column: span 1; }} }}
.card-top {{ display: flex; align-items: center; gap: 0.6rem; }}
.card-icon {{ font-size: 0.9rem; flex-shrink: 0; opacity: 0.6; }}
.card-name {{ font-size: 0.875rem; font-weight: 500; }}
.card-plan {{ font-size: 0.75rem; color: var(--text-muted); }}
.card-links {{ display: flex; flex-direction: column; gap: 0.3rem; padding-top: 0.75rem; border-top: 1px solid var(--border); }}
.link-row {{ display: flex; justify-content: space-between; gap: 0.5rem; align-items: center; }}
.link-label {{ font-size: 0.65rem; text-transform: uppercase; letter-spacing: 0.08em; color: var(--text-muted); flex-shrink: 0; }}
.link-val {{ font-size: 0.75rem; color: var(--text-secondary); text-align: right; word-break: break-all; }}
.link-url {{
  text-decoration: none;
  transition: color 0.15s ease;
}}
.link-url:hover {{ color: var(--text); opacity: 1; }}
.placeholder {{ color: var(--text-muted); font-style: italic; }}
@keyframes cardReveal {{ from {{ opacity: 0; transform: translateY(4px); }} to {{ opacity: 1; transform: translateY(0); }} }}
@media (max-width: 640px) {{
  .ai-hero {{ padding: 3.5rem 1.25rem 2.5rem; }}
  .ai-main {{ padding: 2rem 1.25rem 4rem; }}
  .tool-grid {{ grid-template-columns: 1fr; }}
}}
</style>"""

    with open(output_path, "w") as f:
        f.write(html)

    print(f"Generated: {output_path}")
    print(f"  - Paid tools: {len(paid)}")
    print(f"  - Free tools: {len(free)}")

if __name__ == "__main__":
    build_page()
