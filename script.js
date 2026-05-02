// ── Cursor (desktop only — skip if nav doesn't exist / no hover)
    if (window.matchMedia('(hover: hover) and (pointer: fine)').matches) {
      const cursor = document.getElementById('cursor');
      const ring   = document.getElementById('cursorRing');
      if (cursor && ring) {
        document.addEventListener('mousemove', e => {
          cursor.style.left = e.clientX + 'px';
          cursor.style.top  = e.clientY + 'px';
          setTimeout(() => { ring.style.left = e.clientX + 'px'; ring.style.top = e.clientY + 'px'; }, 80);
        });
        document.querySelectorAll('a, button').forEach(el => {
          el.addEventListener('mouseenter', () => { cursor.style.transform = 'translate(-50%,-50%) scale(2)'; ring.style.width = '56px'; ring.style.height = '56px'; });
          el.addEventListener('mouseleave', () => { cursor.style.transform = 'translate(-50%,-50%) scale(1)'; ring.style.width = '36px'; ring.style.height = '36px'; });
        });
      }
    }

    // ── Typewriter
    const phrases = [
      'nmap -sV -O target.network',
      'sqlmap --dbs --level=5',
      'msfconsole -q -x "use exploit/..."',
      'hashcat -a 0 -m 1000 hash.txt',
      'python3 exploit.py --rhost target',
    ];
    let pi = 0, ci = 0, deleting = false;
    const el = document.getElementById('typeText');
    function type() {
      const phrase = phrases[pi];
      if (!deleting) {
        el.textContent = phrase.slice(0, ++ci);
        if (ci === phrase.length) { deleting = true; setTimeout(type, 1800); return; }
      } else {
        el.textContent = phrase.slice(0, --ci);
        if (ci === 0) { deleting = false; pi = (pi + 1) % phrases.length; }
      }
      setTimeout(type, deleting ? 40 : 70);
    }
    setTimeout(type, 1200);

    // ── Scroll reveal
    const observer = new IntersectionObserver(entries => {
      entries.forEach(e => { if (e.isIntersecting) e.target.classList.add('visible'); });
    }, { threshold: 0.1 });
    document.querySelectorAll('.reveal').forEach(el => observer.observe(el));

    // ── Hamburger menu
    const hamburger = document.getElementById('hamburger');
    const mobileMenu = document.getElementById('mobileMenu');
    function closeMenu() { hamburger.classList.remove('active'); mobileMenu.classList.remove('open'); }
    if (hamburger && mobileMenu) {
      hamburger.addEventListener('click', () => {
        hamburger.classList.toggle('active');
        mobileMenu.classList.toggle('open');
      });
      mobileMenu.querySelectorAll('a').forEach(a => {
        a.addEventListener('click', closeMenu);
      });
    }