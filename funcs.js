    const copy = (el) => {
      const pre = document.querySelector(el);
      if (!pre) return;
      const code = pre.innerText;
      navigator.clipboard.writeText(code).then(() => {
        const btn = document.querySelector(`[data-copy="${el}"]`);
        if (!btn) return;
        const old = btn.textContent;
        btn.textContent = 'Copied!';
        setTimeout(() => (btn.textContent = old), 1500);
      });
    };
    document.addEventListener('click', (e) => {
      const t = e.target;
      if (t.matches('.copy-btn')) {
        const target = t.getAttribute('data-copy');
        copy(target);
      }
    });

    // Auto-enable dark Prism theme when user prefers dark
    const darkLink = document.getElementById('prism-dark');
    const mq = window.matchMedia('(prefers-color-scheme: dark)');
    if (mq.matches) darkLink.disabled = false;
    mq.addEventListener?.('change', (ev) => { darkLink.disabled = !ev.matches; });
