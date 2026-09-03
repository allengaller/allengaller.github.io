/* ─────────────────────────────────────────────────────────
   Allen Galler — site.js
   Minimal vanilla JS for: scroll progress, back-to-top,
   scroll-triggered reveals, magnetic CTAs.
   No dependencies. ~1KB minified.
   ───────────────────────────────────────────────────────── */
(function () {
  'use strict';

  // ── Scroll progress bar ──────────────────────────────
  const progressBar = document.getElementById('scroll-progress');
  if (progressBar) {
    let ticking = false;
    const updateProgress = () => {
      const h = document.documentElement;
      const scrolled = h.scrollTop;
      const max = h.scrollHeight - h.clientHeight;
      const pct = max > 0 ? Math.min(100, (scrolled / max) * 100) : 0;
      progressBar.style.transform = `scaleX(${pct / 100})`;
      ticking = false;
    };
    document.addEventListener('scroll', () => {
      if (!ticking) {
        requestAnimationFrame(updateProgress);
        ticking = true;
      }
    }, { passive: true });
  }

  // ── Back-to-top button ───────────────────────────────
  const backToTop = document.getElementById('back-to-top');
  if (backToTop) {
    const toggleVisible = () => {
      const show = window.scrollY > 600;
      backToTop.classList.toggle('is-visible', show);
    };
    backToTop.addEventListener('click', () => {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });
    document.addEventListener('scroll', toggleVisible, { passive: true });
    toggleVisible();
  }

  // ── Scroll-triggered reveals (IntersectionObserver) ──
  const revealEls = document.querySelectorAll('[data-reveal]');
  if (revealEls.length && 'IntersectionObserver' in window) {
    const io = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add('is-revealed');
            io.unobserve(entry.target);
          }
        });
      },
      { rootMargin: '0px 0px -10% 0px', threshold: 0.05 }
    );
    revealEls.forEach((el) => io.observe(el));
  } else {
    // Fallback: just reveal everything
    revealEls.forEach((el) => el.classList.add('is-revealed'));
  }

  // ── Magnetic CTAs (subtle, only on coarse pointers) ───
  // Skip on touch devices to avoid jank.
  const isCoarse = window.matchMedia('(pointer: coarse)').matches;
  if (!isCoarse) {
    const magneticEls = document.querySelectorAll('.btn-primary, .home-actions .btn');
    magneticEls.forEach((el) => {
      let raf = 0;
      const onMove = (e) => {
        const rect = el.getBoundingClientRect();
        const x = e.clientX - rect.left - rect.width / 2;
        const y = e.clientY - rect.top - rect.height / 2;
        // very subtle, only ~10% pull
        cancelAnimationFrame(raf);
        raf = requestAnimationFrame(() => {
          el.style.transform = `translate(${x * 0.1}px, ${y * 0.1}px)`;
        });
      };
      const onLeave = () => {
        cancelAnimationFrame(raf);
        el.style.transform = '';
      };
      el.addEventListener('mousemove', onMove);
      el.addEventListener('mouseleave', onLeave);
    });
  }

  // ── Reduce motion check (double safety net) ───────────
  const prefersReduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (prefersReduced) {
    document.querySelectorAll('[data-reveal]').forEach((el) => el.classList.add('is-revealed'));
  }
})();
