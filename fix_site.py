#!/usr/bin/env python3
"""Qwerty Labs site fixes: safe batch + conversion upgrades (cursor/typewriter/banner removal, WhatsApp, CSP, links, translations)."""
import re, sys

def apply(path, subs, label):
    with open(path, encoding='utf-8') as f:
        c = f.read()
    orig = c
    report = []
    for pattern, repl, min_count in subs:
        before = c
        c = re.sub(pattern, repl, c, flags=re.S)
        n = c.count(repl) - before.count(repl) if isinstance(repl, str) else None
        # count actual replacements made
        if c == before:
            report.append(f"  !! NO MATCH: {pattern[:70]}")
    if c == orig:
        print(f"== {label}: NO CHANGES (check patterns)")
    else:
        print(f"== {label}: modified ({len(orig)-len(c)} bytes net)")
    with open(path, 'w', encoding='utf-8') as f:
        f.write(c)

# ---------- script.js: full rewrite (cursor + typewriter removed) ----------
with open('script.js', encoding='utf-8') as f:
    js = f.read()
new_js = """// ── Scroll reveal
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
"""
with open('script.js', 'w', encoding='utf-8') as f:
    f.write(new_js)
print("== script.js: rewritten (cursor + typewriter removed)")

# ---------- shared snippets ----------
CSP = '<meta http-equiv="Content-Security-Policy" content="default-src \'self\'; script-src \'unsafe-inline\'; font-src fonts.gstatic.com fonts.googleapis.com; style-src \'unsafe-inline\' fonts.googleapis.com; img-src \'self\' data:; frame-ancestors \'none\'">'
NOSCRIPT = '  <noscript><style>.reveal{opacity:1 !important;transform:none !important;}</style></noscript>'
WA_CSS = """
    /* ── WhatsApp Float ── */
    .wa-float {
      position: fixed; bottom: 1.5rem; right: 1.5rem; z-index: 9990;
      display: flex; align-items: center; gap: 0.6rem;
      background: #25D366; color: #fff; text-decoration: none;
      font-family: 'Share Tech Mono', monospace; font-size: 0.8rem;
      letter-spacing: 0.08em; text-transform: uppercase;
      padding: 0.7rem 1.1rem; border-radius: 999px;
      box-shadow: 0 4px 16px rgba(37,211,102,0.35);
      transition: transform 0.2s, box-shadow 0.2s;
    }
    .wa-float:hover { transform: translateY(-2px); box-shadow: 0 6px 24px rgba(37,211,102,0.5); }
    .wa-float svg { width: 20px; height: 20px; fill: #fff; }
"""
WA_HTML = """
  <!-- WhatsApp float — TODO: replace 52XXXXXXXXXX with QWERTY business number -->
  <a class="wa-float" href="https://wa.me/52XXXXXXXXXX?text=Hola%20QWERTY%20Security%20Labs" target="_blank" rel="noopener">
    <svg viewBox="0 0 24 24"><path d="M12.04 2c-5.46 0-9.91 4.45-9.91 9.91 0 1.75.46 3.45 1.32 4.95L2.05 22l5.25-1.38c1.45.79 3.08 1.21 4.74 1.21 5.46 0 9.91-4.45 9.91-9.91S17.5 2 12.04 2zm5.83 14.14c-.25.7-1.45 1.33-2.02 1.42-.52.08-1.17.11-1.89-.12-.44-.14-1-.32-1.71-.63-3.01-1.3-4.98-4.33-5.13-4.53-.15-.2-1.22-1.63-1.22-3.11 0-1.48.78-2.21 1.05-2.51.28-.3.61-.38.81-.38.2 0 .41 0 .59.01.19.01.44-.07.69.53.25.61.86 2.11.94 2.26.08.15.13.33.02.53-.1.2-.15.33-.3.51-.15.18-.32.4-.46.53-.15.15-.31.32-.13.63.18.3.79 1.31 1.7 2.12 1.17 1.04 2.16 1.36 2.46 1.51.3.15.48.13.66-.08.18-.2.76-.89.96-1.19.2-.3.41-.25.68-.15.28.1 1.76.83 2.06.98.3.15.51.23.58.35.08.13.08.71-.17 1.4z"/></svg>
    WhatsApp
  </a>
"""

# ---------- index.html (EN) ----------
apply('index.html', [
    (r'      overflow-x: hidden;\n      cursor: none;\n    }', '      overflow-x: hidden;\n    }', 1),
    (r'    \.cursor, \.cursor-ring \{ display: none; \}\n    @media \(hover: hover\) and \(pointer: fine\) \{\n.*?\n    \}\n', '', 1),
    (r'      cursor: none;', '      cursor: pointer;', 3),
    (r'    \.typewriter \{[^}]*\}\n    \.typewriter span \{.*?\n    @keyframes blink \{ 50% \{ border-color: transparent; \} \}\n', '', 1),
    (r'      \.typewriter \{ font-size: 0\.85rem; word-break: break-all; \}\n', '', 1),
    (r'  <div class="cursor" id="cursor"></div>\n  <div class="cursor-ring" id="cursorRing"></div>\n', '', 1),
    (r'    <p class="typewriter"><span id="typeText"></span></p>\n', '', 1),
    (r'© 2025 QWERTY', '© 2026 QWERTY', 1),
    (r'        <li><a href="#process">Process</a></li>\n        <li><a href="#contact">Contact</a></li>',
     '        <li><a href="#process">Process</a></li>\n        <li><a href="comparativa.html">Compare</a></li>\n        <li><a href="#contact">Contact</a></li>', 1),
    (r'    <a href="#process">Process</a>\n    <a href="#contact">Contact</a>',
     '    <a href="#process">Process</a>\n    <a href="comparativa.html">Compare</a>\n    <a href="#contact">Contact</a>', 1),
    (r'      <li><a href="#process">Process</a></li>\n      <li><a href="#contact">Contact</a></li>',
     '      <li><a href="#process">Process</a></li>\n      <li><a href="comparativa.html">Compare</a></li>\n      <li><a href="#contact">Contact</a></li>', 1),
    (r'  </style>\n</head>', '  </style>\n' + NOSCRIPT + '\n</head>', 1),
    (r'  </style>\n', '  </style>\n' + WA_CSS + '\n', 1),
    (r'  <script src="script.js"></script>\n</body>', '  <script src="script.js"></script>\n' + WA_HTML + '\n</body>', 1),
], 'index.html')

# ---------- es/index.html ----------
apply('es/index.html', [
    (r'      overflow-x: hidden;\n      cursor: none;\n    }', '      overflow-x: hidden;\n    }', 1),
    (r'    \.cursor, \.cursor-ring \{ display: none; \}\n    @media \(hover: hover\) and \(pointer: fine\) \{\n.*?\n    \}\n', '', 1),
    (r'      cursor: none;', '      cursor: pointer;', 3),
    (r'    \.typewriter \{[^}]*\}\n    \.typewriter span \{.*?\n    @keyframes blink \{ 50% \{ border-color: transparent; \} \}\n', '', 1),
    (r'      \.typewriter \{ font-size: 0\.85rem; word-break: break-all; \}\n', '', 1),
    (r'  <div class="cursor" id="cursor"></div>\n  <div class="cursor-ring" id="cursorRing"></div>\n', '', 1),
    (r'    <p class="typewriter"><span id="typeText"></span></p>\n', '', 1),
    (r'© 2025 QWERTY', '© 2026 QWERTY', 1),
    (r'  <meta name="description" content="Offensive security and ISO 27001 consulting for businesses on the US–Mexico border\. Pentesting, vulnerability assessments, DSO como Servicio\.">',
     '  <meta name="description" content="Consultoría en seguridad ofensiva e ISO 27001 para empresas en la frontera México–EE.UU. Pentesting, evaluaciones de vulnerabilidad, DSO como Servicio.">', 1),
    (r'  <meta property="og:url" content="https://jatcalleros\.github\.io/qwerty_labs/">',
     '  <meta property="og:url" content="https://jatcalleros.github.io/qwerty_labs/es/">', 1),
    (r'        <li><a href="#process">Proceso</a></li>\n        <li><a href="#contact">Contacto</a></li>',
     '        <li><a href="#process">Proceso</a></li>\n        <li><a href="comparativa.html">Comparativa</a></li>\n        <li><a href="#contact">Contacto</a></li>', 1),
    (r'    <a href="#process">Proceso</a>\n    <a href="#contact">Contacto</a>',
     '    <a href="#process">Proceso</a>\n    <a href="comparativa.html">Comparativa</a>\n    <a href="#contact">Contacto</a>', 1),
    (r'      <li><a href="#process">Proceso</a></li>\n      <li><a href="#contact">Contacto</a></li>',
     '      <li><a href="#process">Proceso</a></li>\n      <li><a href="comparativa.html">Comparativa</a></li>\n      <li><a href="#contact">Contacto</a></li>', 1),
    (r'  </style>\n</head>', '  </style>\n' + NOSCRIPT + '\n</head>', 1),
    (r'  </style>\n', '  </style>\n' + WA_CSS + '\n', 1),
    (r'  <script src="/qwerty_labs/script.js"></script>\n</body>', '  <script src="/qwerty_labs/script.js"></script>\n' + WA_HTML + '\n</body>', 1),
], 'es/index.html')

# ---------- comparativa.html (EN) ----------
apply('comparativa.html', [
    (r'font-size: 32px;', 'font-size: 18px;', 1),
    (r'  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>\n', '  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>\n  ' + CSP + '\n', 1),
    (r'Why <span class="accent">QWERTY Security Labs</span>??', 'Why <span class="accent">QWERTY Security Labs</span>?', 1),
    (r'</p></p>', '</p>', 1),
    (r'    <div style="background:var\(--surface\);border:1px solid var\(--border\);border-left:4px solid var\(--accent\);padding:1\.5rem 2rem;margin:2rem 0;display:flex;align-items:center;gap:1\.5rem;flex-wrap:wrap;">\n.*?</div>\n', '', 1),
    (r'<td>Te atiende</td>', '<td>Who you deal with</td>', 1),
    (r'<td>Precio Pyme</td>', '<td>SME pricing</td>', 1),
    (r'<td>Presencia local</td>', '<td>Local presence</td>', 1),
    (r'<td>Precio</td>', '<td>Pricing</td>', 1),
    (r'<td>Certificaciones del equipo</td>', '<td>Team certifications</td>', 1),
    (r'<td>Conocen tu realidad</td>', '<td>They know your reality</td>', 1),
    (r'<td>Experiencia en BPOs y maquiladoras</td>', '<td>BPO &amp; maquiladora experience</td>', 1),
    (r'<td>Costo real</td>', '<td>Real cost</td>', 1),
    (r'<td>Cobertura</td>', '<td>Coverage</td>', 1),
    (r'<td>Herramientas</td>', '<td>Tools</td>', 1),
    (r'<td>Objetividad</td>', '<td>Objectivity</td>', 1),
    (r'<td>Stack profesional actualizado</td>', '<td>Updated professional toolset</td>', 1),
    (r'Las PyMEs son el blanco #1 de ataques \n        porque "no creen que les vaya a pasar"\. La pregunta no es <em>si</em> te van a atacar, \n        sino <em>cuándo</em> — y si tendrás la documentación \(ISO 27001, pentest\) para demostrar \n        debida diligencia ante clientes, aseguradoras y reguladores\.',
     'SMEs are the #1 target of attacks \n        because they do not believe it will happen to them. The question is not <em>if</em> you will be attacked, \n        but <em>when</em> — and whether you will have the documentation (ISO 27001, pentest) to show \n        due diligence to clients, insurers, and regulators.', 1),
    (r'<strong>Dato adicional:</strong> México registra un déficit de al menos 25,000 especialistas en \n        ciberseguridad — la escasez de talento es real y el mercado lo siente\.',
     '<strong>Additional fact:</strong> Mexico has a shortage of at least 25,000 cybersecurity specialists \n        — the talent gap is real and the market feels it.', 1),
    (r'Para la PyME en Chihuahua o el norte de México que necesita seguridad real \n        — no una factura de consultora grande ni el "mi cuñado le sabe"\. \n        Para la empresa que valora la atención directa, los precios claros \n        y un especialista que vive la seguridad todos los días\.',
     'For the SME in Chihuahua or northern Mexico that needs real security \n        — not a big-consultancy invoice, not "my brother-in-law knows computers." \n        For the company that values direct attention, clear pricing, \n        and a specialist who lives security every day.', 1),
], 'comparativa.html')

# ---------- es/comparativa.html ----------
apply('es/comparativa.html', [
    (r'font-size: 32px;', 'font-size: 18px;', 1),
    (r'  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>\n', '  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>\n  ' + CSP + '\n', 1),
    (r'    <div style="background:var\(--surface\);border:1px solid var\(--border\);border-left:4px solid var\(--accent\);padding:1\.5rem 2rem;margin:2rem 0;display:flex;align-items:center;gap:1\.5rem;flex-wrap:wrap;">\n.*?</div>\n', '', 1),
], 'es/comparativa.html')

print("\nDone. Next: verification.")
