<style>
.fat-hero {
  position: relative;
  padding: 64px 0 48px;
  margin-bottom: 48px;
  text-align: center;
  overflow: hidden;
}
.fat-hero::before {
  content: '';
  position: absolute;
  inset: 0;
  background: radial-gradient(ellipse 70% 60% at 50% 0%, rgba(212, 114, 106, 0.12) 0%, transparent 70%);
  pointer-events: none;
}
.fat-hero::after {
  content: '';
  position: absolute;
  bottom: 0; left: 50%;
  transform: translateX(-50%);
  width: 200px; height: 1px;
  background: linear-gradient(90deg, transparent, var(--coral), transparent);
}
.fat-hero-badge {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 8px 20px;
  background: rgba(212, 114, 106, 0.1);
  border: 1px solid rgba(212, 114, 106, 0.25);
  border-radius: 50px;
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.7rem;
  color: var(--coral);
  letter-spacing: 3px;
  margin-bottom: 24px;
  text-transform: uppercase;
}
.fat-hero-badge svg {
  width: 14px; height: 14px;
  fill: var(--coral);
}
.fat-hero h1 {
  font-family: 'Noto Serif SC', serif;
  font-size: clamp(2.5rem, 6vw, 4rem);
  font-weight: 700;
  background: linear-gradient(135deg, var(--text) 0%, var(--coral) 50%, var(--gold) 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  letter-spacing: 8px;
  margin-bottom: 16px;
  animation: fadeInUp 0.8s ease-out;
}
.fat-hero-desc {
  font-size: 1.05rem;
  color: var(--text-secondary);
  max-width: 600px;
  margin: 0 auto;
  line-height: 1.8;
  animation: fadeInUp 0.8s ease-out 0.15s both;
}
.fat-hero-meta {
  display: flex;
  justify-content: center;
  gap: 32px;
  margin-top: 32px;
  animation: fadeInUp 0.8s ease-out 0.3s both;
}
.fat-hero-meta-item {
  text-align: center;
}
.fat-hero-meta-num {
  font-family: 'JetBrains Mono', monospace;
  font-size: 2rem;
  font-weight: 600;
  color: var(--coral);
  display: block;
}
.fat-hero-meta-label {
  font-size: 0.75rem;
  color: var(--text-dim);
  letter-spacing: 2px;
  text-transform: uppercase;
}
.fat-github-link {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  padding: 14px 28px;
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: var(--radius-md);
  color: var(--text);
  text-decoration: none;
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.85rem;
  margin-top: 32px;
  transition: all 0.3s ease;
  backdrop-filter: blur(8px);
  animation: fadeInUp 0.8s ease-out 0.4s both;
}
.fat-github-link:hover {
  border-color: var(--coral);
  box-shadow: var(--shadow-md), 0 0 30px rgba(212, 114, 106, 0.15);
  transform: translateY(-3px);
}
.fat-github-link svg {
  width: 20px; height: 20px;
  fill: var(--text);
}
.section-title {
  display: flex;
  align-items: center;
  gap: 16px;
  margin: 56px 0 32px;
  padding-bottom: 16px;
  border-bottom: 1px solid var(--border);
}
.section-title-icon {
  width: 40px; height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--bg-tertiary);
  border-radius: var(--radius-md);
  border: 1px solid var(--border);
}
.section-title-icon svg {
  width: 20px; height: 20px;
  fill: var(--coral);
}
.section-title h2 {
  font-family: 'Noto Serif SC', serif;
  font-size: 1.3rem;
  font-weight: 600;
  color: var(--text);
  letter-spacing: 3px;
  margin: 0;
  padding: 0;
  border: none;
}
.section-title::after { display: none; }
.module-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
  gap: 20px;
  margin: 0 0 40px;
}
.module-card {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  padding: 24px;
  text-decoration: none;
  transition: all 0.35s ease;
  position: relative;
  overflow: hidden;
  backdrop-filter: blur(8px);
}
.module-card::before {
  content: '';
  position: absolute;
  top: 0; left: 0; right: 0;
  height: 3px;
  background: linear-gradient(90deg, var(--coral), var(--gold));
  opacity: 0;
  transition: opacity 0.3s ease;
}
.module-card:hover {
  border-color: rgba(212, 114, 106, 0.4);
  box-shadow: var(--shadow-lg), 0 0 40px rgba(212, 114, 106, 0.1);
  transform: translateY(-5px);
}
.module-card:hover::before {
  opacity: 1;
}
.module-card-num {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.65rem;
  color: var(--coral);
  letter-spacing: 2px;
  margin-bottom: 12px;
  opacity: 0.8;
}
.module-card h3 {
  font-family: 'Noto Serif SC', serif;
  font-size: 1.05rem;
  font-weight: 600;
  color: var(--text);
  margin-bottom: 10px;
  letter-spacing: 1px;
}
.module-card p {
  font-size: 0.85rem;
  color: var(--text-dim);
  line-height: 1.7;
  margin: 0;
}
.module-card.green-accent::before {
  background: linear-gradient(90deg, var(--jade), var(--coral));
}
.featured-section {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  padding: 32px;
  margin: 40px 0;
  backdrop-filter: blur(8px);
  position: relative;
}
.featured-section::before {
  content: '';
  position: absolute;
  top: -1px; left: 40px; right: 40px;
  height: 2px;
  background: linear-gradient(90deg, transparent, var(--coral), transparent);
}
.featured-label {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 6px 14px;
  background: rgba(212, 114, 106, 0.1);
  border: 1px solid rgba(212, 114, 106, 0.2);
  border-radius: 50px;
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.65rem;
  color: var(--coral);
  letter-spacing: 2px;
  margin-bottom: 20px;
}
.featured-section h3 {
  font-family: 'Noto Serif SC', serif;
  font-size: 1.3rem;
  color: var(--text);
  margin-bottom: 12px;
  letter-spacing: 2px;
}
.featured-section p {
  color: var(--text-secondary);
  font-size: 0.95rem;
  line-height: 1.8;
}
.tag-list {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-top: 20px;
}
.tag {
  padding: 6px 14px;
  background: var(--bg-tertiary);
  border: 1px solid var(--border);
  border-radius: 50px;
  font-size: 0.8rem;
  color: var(--text-secondary);
  transition: all 0.25s ease;
}
.tag:hover {
  border-color: var(--coral);
  color: var(--coral);
  background: rgba(212, 114, 106, 0.05);
}
.disclaimer {
  background: rgba(212, 114, 106, 0.05);
  border: 1px solid rgba(212, 114, 106, 0.15);
  border-radius: var(--radius-md);
  padding: 20px 24px;
  margin: 40px 0;
  font-size: 0.85rem;
  color: var(--text-dim);
  line-height: 1.7;
}
.disclaimer strong {
  color: var(--coral);
}
@keyframes fadeInUp {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>

<div class="fat-hero">
  <div class="fat-hero-badge">
    <svg viewBox="0 0 24 24"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/></svg>
    Evidence-Based
  </div>
  <h1>减肥知识语料库</h1>
  <p class="fat-hero-desc">
    基于循证医学和运动科学的减肥知识体系。<br>
    涵盖生理学、心理学、医疗、健身、药物、营养六大核心模块。
  </p>
  <div class="fat-hero-meta">
    <div class="fat-hero-meta-item">
      <span class="fat-hero-meta-num">30+</span>
      <span class="fat-hero-meta-label">Documents</span>
    </div>
    <div class="fat-hero-meta-item">
      <span class="fat-hero-meta-num">6</span>
      <span class="fat-hero-meta-label">Modules</span>
    </div>
    <div class="fat-hero-meta-item">
      <span class="fat-hero-meta-num">EBM</span>
      <span class="fat-hero-meta-label">Based</span>
    </div>
  </div>
  <a href="https://github.com/fat-looser/fat-looser-database" target="_blank" class="fat-github-link">
    <svg viewBox="0 0 24 24"><path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/></svg>
    View on GitHub
  </a>
</div>

<div class="disclaimer">
  <strong>免责声明：</strong>本数据库内容仅供参考和教育用途，不构成医疗建议。任何减肥计划的实施，尤其涉及药物治疗和医疗干预，请务必咨询专业医疗人员。
</div>

<div class="featured-section">
  <div class="featured-label">
    <svg width="10" height="10" viewBox="0 0 24 24" fill="currentColor"><path d="M12 17.27L18.18 21l-1.64-7.03L22 9.24l-7.19-.61L12 2 9.19 8.63 2 9.24l5.46 4.73L5.82 21z"/></svg>
    About This Project
  </div>
  <h3>Fat Looser Database</h3>
  <p>
    一个基于循证医学和运动科学的减肥知识体系。所有内容基于权威医学文献、临床指南和运动科学研究，采用 Markdown 格式存储，便于检索、维护和版本管理。适用于普通读者、健身教练、营养咨询师和医疗健康从业者。
  </p>
  <div class="tag-list">
    <span class="tag">循证医学</span>
    <span class="tag">运动科学</span>
    <span class="tag">营养学</span>
    <span class="tag">心理学</span>
    <span class="tag">临床医学</span>
    <span class="tag">健康管理</span>
  </div>
</div>

<div class="section-title">
  <div class="section-title-icon">
    <svg viewBox="0 0 24 24"><path d="M3 13h2v-2H3v2zm0 4h2v-2H3v2zm0-8h2V7H3v2zm4 4h14v-2H7v2zm0 4h14v-2H7v2zM7 7v2h14V7H7z"/></svg>
  </div>
  <h2>模块导航</h2>
</div>

<div class="module-grid">
  <a href="https://github.com/fat-looser/fat-looser-database/tree/main/01-physiology" target="_blank" class="module-card">
    <div class="module-card-num">01</div>
    <h3>生理学基础</h3>
    <p>代谢、脂肪形成、能量平衡、激素、身体成分</p>
  </a>
  <a href="https://github.com/fat-looser/fat-looser-database/tree/main/02-psychology" target="_blank" class="module-card">
    <div class="module-card-num">02</div>
    <h3>减肥心理学</h3>
    <p>动机、行为改变、情绪化饮食、心理障碍</p>
  </a>
  <a href="https://github.com/fat-looser/fat-looser-database/tree/main/03-medical" target="_blank" class="module-card">
    <div class="module-card-num">03</div>
    <h3>医疗干预</h3>
    <p>评估、治疗方案、减重手术、并发症</p>
  </a>
  <a href="https://github.com/fat-looser/fat-looser-database/tree/main/04-fitness" target="_blank" class="module-card">
    <div class="module-card-num">04</div>
    <h3>健身运动</h3>
    <p>有氧、力量训练、HIIT、运动计划、恢复</p>
  </a>
  <a href="https://github.com/fat-looser/fat-looser-database/tree/main/05-medication" target="_blank" class="module-card">
    <div class="module-card-num">05</div>
    <h3>药物治疗</h3>
    <p>合法药物、作用机制、使用指南、副作用</p>
  </a>
  <a href="https://github.com/fat-looser/fat-looser-database/tree/main/06-nutrition" target="_blank" class="module-card green-accent">
    <div class="module-card-num">06</div>
    <h3>食疗营养</h3>
    <p>饮食原则、营养素、膳食计划、流行饮食法</p>
  </a>
</div>
