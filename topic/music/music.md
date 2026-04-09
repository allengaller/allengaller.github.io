<style>
.music-hero {
  position: relative;
  padding: 64px 0 48px;
  margin-bottom: 48px;
  text-align: center;
  overflow: hidden;
}
.music-hero::before {
  content: '';
  position: absolute;
  inset: 0;
  background: radial-gradient(ellipse 70% 60% at 50% 0%, rgba(94, 196, 182, 0.15) 0%, transparent 70%);
  pointer-events: none;
}
.music-hero::after {
  content: '';
  position: absolute;
  bottom: 0; left: 50%;
  transform: translateX(-50%);
  width: 200px; height: 1px;
  background: linear-gradient(90deg, transparent, var(--gold), transparent);
}
.music-hero-badge {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 8px 20px;
  background: rgba(94, 196, 182, 0.1);
  border: 1px solid rgba(94, 196, 182, 0.25);
  border-radius: 50px;
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.7rem;
  color: var(--jade);
  letter-spacing: 3px;
  margin-bottom: 24px;
  text-transform: uppercase;
}
.music-hero-badge svg {
  width: 14px; height: 14px;
  fill: var(--jade);
}
.music-hero h1 {
  font-family: 'Noto Serif SC', serif;
  font-size: clamp(2.5rem, 6vw, 4rem);
  font-weight: 700;
  background: linear-gradient(135deg, var(--text) 0%, var(--jade) 50%, var(--gold) 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  letter-spacing: 8px;
  margin-bottom: 16px;
  animation: fadeInUp 0.8s ease-out;
}
.music-hero-desc {
  font-size: 1.05rem;
  color: var(--text-secondary);
  max-width: 600px;
  margin: 0 auto;
  line-height: 1.8;
  animation: fadeInUp 0.8s ease-out 0.15s both;
}
.music-hero-meta {
  display: flex;
  justify-content: center;
  gap: 32px;
  margin-top: 32px;
  animation: fadeInUp 0.8s ease-out 0.3s both;
}
.music-hero-meta-item {
  text-align: center;
}
.music-hero-meta-num {
  font-family: 'JetBrains Mono', monospace;
  font-size: 2rem;
  font-weight: 600;
  color: var(--jade);
  display: block;
}
.music-hero-meta-label {
  font-size: 0.75rem;
  color: var(--text-dim);
  letter-spacing: 2px;
  text-transform: uppercase;
}
.music-github-link {
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
.music-github-link:hover {
  border-color: var(--jade);
  box-shadow: var(--shadow-md), 0 0 30px rgba(94, 196, 182, 0.15);
  transform: translateY(-3px);
}
.music-github-link svg {
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
  fill: var(--gold);
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
  background: linear-gradient(90deg, var(--jade), var(--gold));
  opacity: 0;
  transition: opacity 0.3s ease;
}
.module-card:hover {
  border-color: var(--border-strong);
  box-shadow: var(--shadow-lg), 0 0 40px rgba(94, 196, 182, 0.1);
  transform: translateY(-5px);
}
.module-card:hover::before {
  opacity: 1;
}
.module-card-num {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.65rem;
  color: var(--jade);
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
.module-card.coral-accent::before {
  background: linear-gradient(90deg, var(--coral), var(--gold));
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
  background: linear-gradient(90deg, transparent, var(--jade), transparent);
}
.featured-label {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 6px 14px;
  background: rgba(201, 169, 110, 0.1);
  border: 1px solid rgba(201, 169, 110, 0.2);
  border-radius: 50px;
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.65rem;
  color: var(--gold);
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
  border-color: var(--jade);
  color: var(--jade);
  background: rgba(94, 196, 182, 0.05);
}
@keyframes fadeInUp {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>

<div class="music-hero">
  <div class="music-hero-badge">
    <svg viewBox="0 0 24 24"><path d="M12 3v10.55c-.59-.34-1.27-.55-2-.55-2.21 0-4 1.79-4 4s1.79 4 4 4 4-1.79 4-4V7h4V3h-6z"/></svg>
    Corpus Database
  </div>
  <h1>音乐知识语料库</h1>
  <p class="music-hero-desc">
    按照专业音乐院校完整知识体系构建的开放学习资源库。<br>
    从基本乐理到音乐治疗，十大专业方向全覆盖。
  </p>
  <div class="music-hero-meta">
    <div class="music-hero-meta-item">
      <span class="music-hero-meta-num">140+</span>
      <span class="music-hero-meta-label">Documents</span>
    </div>
    <div class="music-hero-meta-item">
      <span class="music-hero-meta-num">10</span>
      <span class="music-hero-meta-label">Modules</span>
    </div>
    <div class="music-hero-meta-item">
      <span class="music-hero-meta-num">CC</span>
      <span class="music-hero-meta-label">License</span>
    </div>
  </div>
  <a href="https://github.com/sit-music/sit-music-database" target="_blank" class="music-github-link">
    <svg viewBox="0 0 24 24"><path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/></svg>
    View on GitHub
  </a>
</div>

<div class="featured-section">
  <div class="featured-label">
    <svg width="10" height="10" viewBox="0 0 24 24" fill="currentColor"><path d="M12 17.27L18.18 21l-1.64-7.03L22 9.24l-7.19-.61L12 2 9.19 8.63 2 9.24l5.46 4.73L5.82 21z"/></svg>
    Featured Project
  </div>
  <h3>SIT Music Database</h3>
  <p>
    一个把音乐学院四年本科课程体系搬到 GitHub 上的项目。不是干巴巴的教科书搬运，每篇文档都用大白话写，该打比方打比方，该举例子举例子。专业术语全部标注英文原文和对应语言来源。
  </p>
  <div class="tag-list">
    <span class="tag">基本乐理</span>
    <span class="tag">视唱练耳</span>
    <span class="tag">作曲理论</span>
    <span class="tag">音乐学</span>
    <span class="tag">音乐教育</span>
    <span class="tag">音乐科技</span>
    <span class="tag">音乐产业</span>
    <span class="tag">指挥</span>
    <span class="tag">音乐治疗</span>
  </div>
</div>

<div class="section-title">
  <div class="section-title-icon">
    <svg viewBox="0 0 24 24"><path d="M3 13h2v-2H3v2zm0 4h2v-2H3v2zm0-8h2V7H3v2zm4 4h14v-2H7v2zm0 4h14v-2H7v2zM7 7v2h14V7H7z"/></svg>
  </div>
  <h2>模块导航</h2>
</div>

<div class="module-grid">
  <a href="https://github.com/sit-music/sit-music-database/tree/main/00-Music-Fundamentals" target="_blank" class="module-card">
    <div class="module-card-num">00</div>
    <h3>基本乐理</h3>
    <p>Music Fundamentals</p>
  </a>
  <a href="https://github.com/sit-music/sit-music-database/tree/main/01-Sight-Singing-and-Ear-Training" target="_blank" class="module-card">
    <div class="module-card-num">01</div>
    <h3>视唱练耳</h3>
    <p>Sight Singing & Ear Training</p>
  </a>
  <a href="https://github.com/sit-music/sit-music-database/tree/main/02-Music-Performance" target="_blank" class="module-card">
    <div class="module-card-num">02</div>
    <h3>音乐表演</h3>
    <p>Performance (39 docs)</p>
  </a>
  <a href="https://github.com/sit-music/sit-music-database/tree/main/03-Composition-and-Music-Theory" target="_blank" class="module-card">
    <div class="module-card-num">03</div>
    <h3>作曲理论</h3>
    <p>Composition & Theory</p>
  </a>
  <a href="https://github.com/sit-music/sit-music-database/tree/main/04-Musicology" target="_blank" class="module-card">
    <div class="module-card-num">04</div>
    <h3>音乐学</h3>
    <p>Musicology (26 docs)</p>
  </a>
  <a href="https://github.com/sit-music/sit-music-database/tree/main/05-Music-Education" target="_blank" class="module-card">
    <div class="module-card-num">05</div>
    <h3>音乐教育</h3>
    <p>Music Education</p>
  </a>
  <a href="https://github.com/sit-music/sit-music-database/tree/main/06-Music-Technology" target="_blank" class="module-card">
    <div class="module-card-num">06</div>
    <h3>音乐科技</h3>
    <p>Music Technology</p>
  </a>
  <a href="https://github.com/sit-music/sit-music-database/tree/main/07-Music-Industry-and-Management" target="_blank" class="module-card">
    <div class="module-card-num">07</div>
    <h3>音乐产业</h3>
    <p>Industry & Management</p>
  </a>
  <a href="https://github.com/sit-music/sit-music-database/tree/main/08-Conducting" target="_blank" class="module-card">
    <div class="module-card-num">08</div>
    <h3>指挥</h3>
    <p>Conducting</p>
  </a>
  <a href="https://github.com/sit-music/sit-music-database/tree/main/09-Music-Therapy" target="_blank" class="module-card">
    <div class="module-card-num">09</div>
    <h3>音乐治疗</h3>
    <p>Music Therapy</p>
  </a>
</div>
