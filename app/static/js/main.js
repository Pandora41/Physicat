document.addEventListener('DOMContentLoaded', () => {
  // 1. Check for reduced motion preference
  const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  
  if (!prefersReducedMotion) {
    // 2. Smooth Transform-based Parallax
    const parallaxElements = document.querySelectorAll('.parallax-layer');
    let scrollY = 0;
    let ticking = false;

    const updateParallax = () => {
      parallaxElements.forEach(el => {
        const speed = parseFloat(el.dataset.parallaxSpeed) || 0.1;
        const rect = el.getBoundingClientRect();
        
        // Only calculate if element is near viewport (performance optimization)
        if (rect.top < window.innerHeight + 100 && rect.bottom > -100) {
          const yPos = -(scrollY * speed);
          el.style.transform = `translate3d(0, ${yPos}px, 0)`;
        }
      });
      ticking = false;
    };

    window.addEventListener('scroll', () => {
      scrollY = window.scrollY;
      if (!ticking) {
        window.requestAnimationFrame(updateParallax);
        ticking = true;
      }
    }, { passive: true });

    // Initial call to set positions
    updateParallax();
  }

  // 3. Intersection Observer for Fade-in Animations
  const observerOptions = {
    root: null,
    rootMargin: '0px',
    threshold: 0.1
  };

  const observer = new IntersectionObserver((entries, obs) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('is-visible');
        obs.unobserve(entry.target); // Only animate once
      }
    });
  }, observerOptions);

  document.querySelectorAll('.fade-in-section').forEach(section => {
    observer.observe(section);
  });
});