# HTML Report Scaffold (Zen Minimalism 7-Preset, 6-Layout & Editorial Typography Architecture)

Reference for `html-report`. Copy the skeleton and trim only data sections the report does not need. Preserve the Google Fonts `<link>`, the 7-preset system (`dossier` default, `zen-garden`, `chronicle`, `sumi-ink`, `shoji-grid`, `aizome-indigo`, `yugen-noir`) with distinct typography and spatial geometry per preset, dual light/dark theme parity, offline self-containment, and print fidelity.

## 1. The Seven Curated Presets, Layouts & Typography Pairings

| Preset Attribute | UI Label & Zen Principle | Default? | Palette, Typography Pairing & Spatial Layout Architecture |
| :--- | :--- | :--- | :--- |
| `data-preset="dossier"` | **Clinical Dossier** (*Shibumi*) | **Yes (Default)** | **Palette**: Soft Parchment (`#F7F4EE`), Cream (`#FDFBF7`), Muted Clay (`#9E583B`).<br>**Typography**: `'Fraunces'` (optical-size variable editorial serif, weight `350`/`400`) + `'Inter'` (precision UI sans) + `'JetBrains Mono'` (tabular data).<br>**Layout (`L1`)**: Compact `240px` sticky chapter sidebar (`01`-`06`) + fluid evidence column (`1220px` max-width). |
| `data-preset="zen-garden"` | **Zen Garden** (*Karesansui* / *Ma*) | Option 2 | **Palette**: Raked Limestone (`#F4F1EA`), Warm Stone (`#F9F7F2`), Kyoto Moss (`#4A6B53`).<br>**Typography**: `'Cormorant Garamond'` (high-contrast classical serif, weight `300`/`400`, lyrical italics) + `'Inter'` (weight `400`/`500`, airy `1.75` line-height) + `'JetBrains Mono'`.<br>**Layout (`L2`)**: Centered `960px` contemplative single-column flow with `5.25rem` vertical *Ma* breathing room. |
| `data-preset="chronicle"` | **Slow Chronicle** (*Wabi-Sabi*) | Option 3 | **Palette**: Warm Paper (`#FBF9F5`), Sand (`#F5F0E6`), Earth Terracotta (`#A65638`).<br>**Typography**: `'Cormorant Garamond'` (oversized `1.65rem` pull-quotes & chapter banners, weight `300`/`400`) + `'Plus Jakarta Sans'` (warm geometric humanist body) + `'JetBrains Mono'`.<br>**Layout (`L3`)**: `1020px` single-column magazine flow with full-width horizontal chapter headers (`01`-`06`). |
| `data-preset="sumi-ink"` | **Sumi-e Ink Wash** (*Kanso* / *Fukinsei*) | Option 4 | **Palette**: Rice Paper (`#F6F6F4`), Pure Washi (`#FFFFFF`), Sumi Charcoal (`#141413`), Hanko Vermilion (`#B8332A`).<br>**Typography**: `'Newsreader'` (sharp literary editorial serif, weight `350`/`400`) + `'Inter'` + `'JetBrains Mono'`.<br>**Layout (`L4`)**: Asymmetric *Fukinsei* golden-ratio split (`38%` sticky narrative context + `62%` evidence stage, `1320px` max-width). |
| `data-preset="shoji-grid"` | **Shoji Architectural Lattice** (*Seijaku*) | Option 5 | **Palette**: Shoji White (`#F8F7F4`), Crisp Alabaster (`#FFFFFF`), Zinc Ink (`#18181B`), Slate Cobalt (`#2E5A88`).<br>**Typography**: `'IBM Plex Sans'` (weight `400`/`500`, industrial Swiss-Japanese clarity) + `'IBM Plex Mono'` (`tabular-nums`).<br>**Layout (`L5`)**: Exposed `1px` structural hairline bento lattice (`1280px` max-width, flush cells, zero outer card radius). |
| `data-preset="aizome-indigo"` | **Aizome Mineral Craft** (*Datsuzoku*) | Option 6 | **Palette**: Mineral Mist (`#F3F6F8`), Ice Stone (`#FAFBFD`), Deep Slate (`#16212B`), Japan Indigo (`#264348`).<br>**Typography**: `'Space Grotesk'` (display headings, weight `400`/`500`) + `'IBM Plex Sans'` (body) + `'JetBrains Mono'`.<br>**Layout (`L1`/`L5`)**: `240px` sticky rail + crisp technical evidence grid (`1240px` max-width). |
| `data-preset="yugen-noir"` | **Yugen Kintsugi Nocturne** (*Yugen*) | Option 7 | **Palette**: Warm Alabaster (`#F5F3EF` light) / Obsidian Lacquer (`#0B0B0C` dark), Burnished Ochre (`#9A7228` light) / Kintsugi Gold (`#D4A853` dark).<br>**Typography**: `'Instrument Serif'` (weight `400`, refined verticality) + `'Inter'` + `'JetBrains Mono'`.<br>**Layout (`L6`)**: Progressive-depth primary stage (`1120px` max-width) with high-contrast gold-seam thesis callouts and collapsible deep-dive drawers. |

The reference defines all seven presets. A generated report keeps **exactly one** preset token block and deletes the other six. It never includes a runtime preset switcher.

`data-preset` is the palette. Optional `data-layout` (`L1`–`L6`) and `data-voice` (`V1`–`V4`) record a mix from the **design-system** composition grammar. When either attribute is absent, use the canonical layout and voice in the table above. Do not add a second preset block to express a mix.

## 2. Document Skeleton (with Required Google Fonts Link)

```html
<!DOCTYPE html>
<html lang="en" data-preset="dossier" data-layout="L1" data-voice="V1" data-theme="light">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta http-equiv="Content-Security-Policy" content="default-src 'none'; script-src 'unsafe-inline'; style-src 'unsafe-inline' https://fonts.googleapis.com; font-src https://fonts.gstatic.com; img-src data:; connect-src 'none'; object-src 'none'; base-uri 'none'; form-action 'none'">
  <title>Report Title</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,500;1,300;1,400;1,500&amp;family=Fraunces:ital,opsz,wght@0,9..144,300..500;1,9..144,300..400&amp;family=Inter:wght@400;500;600&amp;family=JetBrains+Mono:wght@400;500;600&amp;family=Plus+Jakarta+Sans:wght@400;500;600&amp;display=swap" rel="stylesheet">
  <style>
    /* 1. One-Preset Color & Typography Tokens + Dark Theme Parity */
    /* 2. Micro-Typesetting, Optical Sizing & Zen Ma Spacing */
    /* 3. Preset Layout Engine (dossier, zen-garden, chronicle) */
    /* 4. Print Stylesheet */
  </style>
</head>
<body>
  <a class="skip" href="#summary">Skip to summary</a>
  <div class="report-shell">
    <header class="report-header">
      <div class="header-title-group">
        <h1>Declarative Finding Title</h1>
        <p class="meta">2026-10-28 · Cohort N = 4,365,797 · Revision abc1234</p>
      </div>
      <button type="button" id="theme-toggle" class="theme-toggle no-print"
              aria-label="Toggle color theme" aria-pressed="false">Theme</button>
    </header>

    <nav class="section-nav no-print" aria-label="Sections">
      <a href="#summary"><span class="nav-num">01</span> Summary</a>
      <a href="#findings"><span class="nav-num">02</span> Findings</a>
      <a href="#evidence"><span class="nav-num">03</span> Evidence</a>
    </nav>

    <main>
      <section id="summary" class="report-section">
        <div class="section-sidebar">
          <span class="chapter-index">01</span>
          <h2>Executive Summary</h2>
          <p class="section-lead">Concise context sentence (<= 25 words) framing the scope and primary decision.</p>
        </div>
        <div class="section-content">
          <div class="thesis-box" id="thesis-statement">
            <p>One- or two-sentence declarative thesis stating the exact primary metric, <em>delta</em>, and operational consequence.</p>
          </div>
          <div class="kpi-grid">
            <article class="kpi">
              <span class="kpi-label">Top-1 Accuracy</span>
              <strong>78.52%</strong>
              <span class="subtext">Baseline: 70.16% (<span class="delta-pos">+8.36 pp</span>)</span>
            </article>
            <article class="kpi">
              <span class="kpi-label">Evaluated Volume</span>
              <strong>4,365,797</strong>
              <span class="subtext">100% Converted Cohort</span>
            </article>
          </div>
        </div>
      </section>

      <section id="findings" class="report-section">
        <div class="section-sidebar">
          <span class="chapter-index">02</span>
          <h2>Core Findings</h2>
          <p class="section-lead">Short narrative guide explaining what the comparison table proves.</p>
        </div>
        <div class="section-content">
          <div class="table-wrap">
            <table>
              <thead><tr><th scope="col">Category</th><th scope="col" class="num">Current</th><th scope="col" class="num">Baseline</th><th scope="col" class="num">Delta</th></tr></thead>
              <tbody><!-- rows --></tbody>
            </table>
          </div>
          <details open>
            <summary>01 · Architectural Driver or Evidence Note</summary>
            <p>Short 2-3 sentence explanation grounded in exact mechanism and code/data reference.</p>
          </details>
        </div>
      </section>
    </main>
  </div>

  <script>
    /* preset switcher, theme toggle, expand/collapse, table filter, copy summary */
  </script>
</body>
</html>
```

## 3. Preset Color & Typography Tokens (Distinct Font Pairings per Preset)

```css
/* Shared editorial type roles (9), radius scale, and data palette.
   Keep only the preset block chosen for the report; delete the other two. */
:root {
  --text-xs: 0.75rem;
  --text-sm: 0.875rem;
  --text-base: 0.95rem;
  --text-md: 1.25rem;
  --text-lg: 1.65rem;
  --text-xl: 2rem;
  --text-2xl: 2.5rem;
  --text-3xl: 2.85rem;
  --radius-xs: 0.375rem;
  --radius-sm: 0.25rem;
  --radius-md: 0.5rem;
}

/* DEFAULT PRESET: dossier (The Shibumi Clinical Dossier — Fraunces + Inter + JetBrains Mono) */
:root,
:root[data-preset="dossier"] {
  --bg-page: #F7F4EE;
  --bg-card: #FDFBF7;
  --bg-subtle: #EFEAE1;
  --text-primary: #22201E;
  --text-secondary: #5A5550;
  --border: #E0D9CE;
  --border-strong: #B8AFA3;
  --accent: #9E583B;
  --accent-subtle: #F2E5DF;
  --status-ok: #2B6648;
  --status-bad: #992B2B;
  --chart-ps: #9E583B;
  --chart-prod: #5A5550;
  --chart-old: #878079;
  --chart-pos: #2B6648;
  --chart-neg: #992B2B;

  --font-display: 'Fraunces', "Iowan Old Style", "Palatino Linotype", Georgia, serif;
  --font-sans: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
  --font-mono: 'JetBrains Mono', ui-monospace, SFMono-Regular, Menlo, monospace;
  --display-weight: 350;
  --display-tracking: -0.022em;
  --display-size: clamp(2.35rem, 4.2vw, 3.6rem);
  --text-thesis: 1.42rem;
  --chapter-size: var(--text-3xl);
  --kpi-size: var(--text-2xl);
  --body-lh: 1.65;

  --radius-card: var(--radius-md);
  --section-pad: 3.5rem;
  --container-max: 1220px;
}

/* PRESET 2: zen-garden (Karesansui Dry Rock Garden — Cormorant Garamond + Airy Inter + JetBrains Mono) */
:root[data-preset="zen-garden"] {
  --bg-page: #F4F1EA;
  --bg-card: #F9F7F2;
  --bg-subtle: #EAE5DB;
  --text-primary: #2B2A27;
  --text-secondary: #5E5C56;
  --border: #DCD6CA;
  --border-strong: #BDB5A6;
  --accent: #4A6B53;
  --accent-subtle: #E3ECE5;
  /* Shared warm data palette: Zen Garden charts match Dossier. */
  --status-ok: #2B6648;
  --status-bad: #992B2B;
  --chart-ps: #9E583B;
  --chart-prod: #5A5550;
  --chart-old: #878079;
  --chart-pos: #2B6648;
  --chart-neg: #992B2B;

  --font-display: 'Cormorant Garamond', "Iowan Old Style", Georgia, serif;
  --font-sans: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
  --font-mono: 'JetBrains Mono', ui-monospace, SFMono-Regular, Menlo, monospace;
  --display-weight: 400;
  --display-tracking: -0.012em;
  --display-size: clamp(2.65rem, 4.8vw, 4.1rem);
  --text-thesis: 1.6rem;
  --chapter-size: var(--text-3xl);
  --kpi-size: 2.75rem;
  --body-lh: 1.75;

  --radius-card: var(--radius-sm);
  --section-pad: 5.25rem;
  --container-max: 960px;
}

/* PRESET 3: chronicle (Kinfolk Slow-Living Chronicle — Cormorant Garamond + Plus Jakarta Sans + JetBrains Mono) */
:root[data-preset="chronicle"] {
  --bg-page: #FBF9F5;
  --bg-card: #F5F0E6;
  --bg-subtle: #EBE4D6;
  --text-primary: #211E1B;
  --text-secondary: #5C564F;
  --border: #E3DAC9;
  --border-strong: #C2B6A1;
  --accent: #A65638;
  --accent-subtle: #EFE0D9;
  --status-ok: #356348;
  --status-bad: #962D2D;
  --chart-ps: #A65638;
  --chart-prod: #5C564F;
  --chart-old: #8C847A;
  --chart-pos: #356348;
  --chart-neg: #962D2D;

  --font-display: 'Cormorant Garamond', "Iowan Old Style", Georgia, serif;
  --font-sans: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
  --font-mono: 'JetBrains Mono', ui-monospace, SFMono-Regular, Menlo, monospace;
  --display-weight: 400;
  --display-tracking: -0.015em;
  --display-size: clamp(2.65rem, 4.8vw, 4.1rem);
  --text-thesis: 1.65rem;
  --chapter-size: 2.35rem;
  --kpi-size: 2.75rem;
  --body-lh: 1.7;

  --radius-card: var(--radius-xs);
  --section-pad: 4.75rem;
  --container-max: 1020px;
}

/* PRESET 4: sumi-ink (Sumi-e Ink Wash & Hanko Vermilion — Newsreader + Inter + JetBrains Mono) */
:root[data-preset="sumi-ink"] {
  --bg-page: #F6F6F4;
  --bg-card: #FFFFFF;
  --bg-subtle: #EBEBE7;
  --text-primary: #141413;
  --text-secondary: #52524E;
  --border: #DCDCD6;
  --border-strong: #AEAEA6;
  --accent: #B8332A;
  --accent-subtle: #F7E3E1;
  --status-ok: #256343;
  --status-bad: #9E2626;
  --chart-ps: #B8332A;
  --chart-prod: #52524E;
  --chart-old: #85857F;
  --chart-pos: #256343;
  --chart-neg: #9E2626;

  --font-display: 'Newsreader', "Iowan Old Style", Georgia, serif;
  --font-sans: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
  --font-mono: 'JetBrains Mono', ui-monospace, SFMono-Regular, Menlo, monospace;
  --display-weight: 350;
  --display-tracking: -0.02em;
  --display-size: clamp(2.45rem, 4.4vw, 3.8rem);
  --text-thesis: 1.48rem;
  --chapter-size: var(--text-3xl);
  --kpi-size: var(--text-2xl);
  --body-lh: 1.68;

  --radius-card: 0px;
  --section-pad: 4rem;
  --container-max: 1320px;
}

/* PRESET 5: shoji-grid (Shoji Architectural Lattice — IBM Plex Sans + IBM Plex Mono) */
:root[data-preset="shoji-grid"] {
  --bg-page: #F8F7F4;
  --bg-card: #FFFFFF;
  --bg-subtle: #F0EFEA;
  --text-primary: #18181B;
  --text-secondary: #52525B;
  --border: #E4E3DD;
  --border-strong: #B8B6AE;
  --accent: #2E5A88;
  --accent-subtle: #E3ECF5;
  --status-ok: #246345;
  --status-bad: #9C2B2B;
  --chart-ps: #2E5A88;
  --chart-prod: #52525B;
  --chart-old: #82828A;
  --chart-pos: #246345;
  --chart-neg: #9C2B2B;

  --font-display: 'IBM Plex Sans', -apple-system, BlinkMacSystemFont, sans-serif;
  --font-sans: 'IBM Plex Sans', -apple-system, BlinkMacSystemFont, sans-serif;
  --font-mono: 'IBM Plex Mono', ui-monospace, SFMono-Regular, Menlo, monospace;
  --display-weight: 400;
  --display-tracking: -0.022em;
  --display-size: clamp(2.25rem, 3.8vw, 3.25rem);
  --text-thesis: 1.32rem;
  --chapter-size: 2.35rem;
  --kpi-size: 2.35rem;
  --body-lh: 1.62;

  --radius-card: 0px;
  --section-pad: 3rem;
  --container-max: 1280px;
}

/* PRESET 6: aizome-indigo (Aizome Mineral Craft — Space Grotesk + IBM Plex Sans + JetBrains Mono) */
:root[data-preset="aizome-indigo"] {
  --bg-page: #F3F6F8;
  --bg-card: #FAFBFD;
  --bg-subtle: #E6EDF2;
  --text-primary: #16212B;
  --text-secondary: #4A5A68;
  --border: #D3DEE6;
  --border-strong: #9FB2C2;
  --accent: #264348;
  --accent-subtle: #DFECEF;
  --status-ok: #236647;
  --status-bad: #992B2B;
  --chart-ps: #264348;
  --chart-prod: #4A5A68;
  --chart-old: #788A99;
  --chart-pos: #236647;
  --chart-neg: #992B2B;

  --font-display: 'Space Grotesk', -apple-system, BlinkMacSystemFont, sans-serif;
  --font-sans: 'IBM Plex Sans', -apple-system, BlinkMacSystemFont, sans-serif;
  --font-mono: 'JetBrains Mono', ui-monospace, SFMono-Regular, Menlo, monospace;
  --display-weight: 400;
  --display-tracking: -0.024em;
  --display-size: clamp(2.3rem, 4vw, 3.45rem);
  --text-thesis: 1.38rem;
  --chapter-size: 2.5rem;
  --kpi-size: 2.45rem;
  --body-lh: 1.65;

  --radius-card: var(--radius-sm);
  --section-pad: 3.5rem;
  --container-max: 1240px;
}

/* PRESET 7: yugen-noir (Yugen Kintsugi Nocturne — Instrument Serif + Inter + JetBrains Mono) */
:root[data-preset="yugen-noir"] {
  --bg-page: #F5F3EF;
  --bg-card: #FCFBF9;
  --bg-subtle: #EBE7DF;
  --text-primary: #1C1A17;
  --text-secondary: #57524A;
  --border: #DDD7CB;
  --border-strong: #B5AC9C;
  --accent: #9A7228;
  --accent-subtle: #F3ECE0;
  --status-ok: #2B6648;
  --status-bad: #992B2B;
  --chart-ps: #9A7228;
  --chart-prod: #57524A;
  --chart-old: #878079;
  --chart-pos: #2B6648;
  --chart-neg: #992B2B;

  --font-display: 'Instrument Serif', "Palatino Linotype", Georgia, serif;
  --font-sans: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
  --font-mono: 'JetBrains Mono', ui-monospace, SFMono-Regular, Menlo, monospace;
  --display-weight: 400;
  --display-tracking: -0.015em;
  --display-size: clamp(2.65rem, 4.8vw, 4.1rem);
  --text-thesis: 1.55rem;
  --chapter-size: var(--text-3xl);
  --kpi-size: 2.65rem;
  --body-lh: 1.7;

  --radius-card: var(--radius-md);
  --section-pad: 4.25rem;
  --container-max: 1120px;
}

/* Dark Theme Parity (Auto OS + Manual Toggle) */
@media (prefers-color-scheme: dark) {
  :root:not([data-theme="light"]) {
    --bg-page: #141210;
    --bg-card: #1D1A17;
    --bg-subtle: #27231F;
    --text-primary: #F5EFE6;
    --text-secondary: #B8AFA6;
    --border: #2E2924;
    --border-strong: #4A423B;
    --accent: #D48462;
    --accent-subtle: #2C1F1A;
    --status-ok: #68B684;
    --status-bad: #E06D6D;
    --chart-ps: #D48462;
    --chart-prod: #B8AFA6;
    --chart-old: #A8988A;
    --chart-pos: #68B684;
    --chart-neg: #E06D6D;
  }
}

:root[data-theme="dark"] {
  --bg-page: #141210;
  --bg-card: #1D1A17;
  --bg-subtle: #27231F;
  --text-primary: #F5EFE6;
  --text-secondary: #B8AFA6;
  --border: #2E2924;
  --border-strong: #4A423B;
  --accent: #D48462;
  --accent-subtle: #2C1F1A;
  --status-ok: #68B684;
  --status-bad: #E06D6D;
  --chart-ps: #D48462;
  --chart-prod: #B8AFA6;
  --chart-old: #A8988A;
  --chart-pos: #68B684;
  --chart-neg: #E06D6D;
}
```

## 4. Base, Micro-Typesetting, Preset Layout Engine, and Components

```css
* { box-sizing: border-box; }
html {
  font-size: 16px;
  scroll-behavior: smooth;
  font-synthesis: none;
  text-rendering: optimizeLegibility;
}
body {
  margin: 0;
  background: var(--bg-page);
  color: var(--text-primary);
  font-family: var(--font-sans);
  font-size: var(--text-base);
  line-height: var(--body-lh);
  font-feature-settings: "kern" 1, "liga" 1, "calt" 1;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}
.report-shell { max-width: var(--container-max); margin: 0 auto; padding: 0 2rem 5rem; }
p, li { max-width: 66ch; text-wrap: pretty; }
h1, h2, h3 {
  font-family: var(--font-display);
  font-weight: var(--display-weight);
  letter-spacing: var(--display-tracking);
  font-optical-sizing: auto;
  font-feature-settings: "kern" 1, "liga" 1, "calt" 1;
  line-height: 1.12;
  text-wrap: balance;
  break-after: avoid;
}
.kpi-label, .tag {
  font-family: var(--font-mono);
  font-size: var(--text-xs);
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  color: var(--text-secondary);
}
.meta, .num, .kpi, td.num, th.num {
  font-family: var(--font-mono);
  font-variant-numeric: tabular-nums;
  letter-spacing: -0.01em;
}
.meta { font-size: var(--text-sm); color: var(--text-secondary); margin: 0; }

.report-header {
  display: flex;
  flex-wrap: wrap;
  gap: 2rem;
  align-items: flex-start;
  justify-content: space-between;
  padding: 4rem 0 2.5rem;
  border-bottom: 1px solid var(--border-strong);
}
.header-title-group h1 {
  font-size: var(--display-size);
  line-height: 1.06;
  margin: 0.5rem 0 0.85rem;
  max-width: 20ch;
}
:root[data-preset="zen-garden"] .header-title-group h1,
:root[data-preset="chronicle"] .header-title-group h1 {
  line-height: 1.04;
}
.theme-toggle { align-self: flex-start; }
button, .filter-input {
  font-family: var(--font-sans);
  font-size: var(--text-sm);
  font-weight: 500;
  min-height: 2rem;
  padding: 0.38rem 0.8rem;
  color: var(--text-primary);
  background: var(--bg-card);
  border: 1px solid var(--border-strong);
  border-radius: 999px;
  cursor: pointer;
}

.section-nav {
  position: sticky;
  top: 0;
  z-index: 10;
  display: flex;
  gap: 1.75rem;
  padding: 0.9rem 0;
  background: var(--bg-page);
  border-bottom: 1px solid var(--border);
  overflow-x: auto;
}
.section-nav a { color: var(--text-secondary); text-decoration: none; font-size: var(--text-sm); font-weight: 500; white-space: nowrap; }
.section-nav a .nav-num { font-family: var(--font-mono); font-size: var(--text-xs); color: var(--accent); margin-right: 0.35rem; }

/* DEFAULT LAYOUT (dossier): Compact 240px Sticky Chapter Sidebar + Evidence Column */
.report-section {
  padding: var(--section-pad) 0;
  border-bottom: 1px solid var(--border);
  display: grid;
  grid-template-columns: 240px 1fr;
  gap: 3rem;
  align-items: start;
}
.section-sidebar { position: sticky; top: 3.75rem; }
.chapter-index {
  font-family: var(--font-display);
  font-weight: 300;
  font-size: var(--chapter-size);
  line-height: 0.95;
  letter-spacing: -0.03em;
  color: var(--accent);
  font-optical-sizing: auto;
  font-feature-settings: "kern" 1, "liga" 1, "calt" 1;
  display: block;
  margin-bottom: 0.45rem;
}
.section-sidebar h2 { font-size: var(--text-lg); margin: 0 0 0.65rem; }
:root[data-preset="zen-garden"] .section-sidebar h2,
:root[data-preset="chronicle"] .section-sidebar h2 { font-size: var(--text-xl); }
.section-lead { font-size: var(--text-sm); color: var(--text-secondary); margin: 0; line-height: 1.6; }

/* PRESET 2 LAYOUT (zen-garden): Centered Contemplative Flow + Extra Ma Whitespace */
:root[data-preset="zen-garden"] .report-section { grid-template-columns: 1fr; gap: 2.25rem; }
:root[data-preset="zen-garden"] .section-sidebar { position: static; text-align: center; max-width: 640px; margin: 0 auto 0.5rem; }
:root[data-preset="zen-garden"] .thesis-box { border-left: 1px solid var(--border-strong); border-top: 2px solid var(--accent); text-align: center; }
:root[data-preset="zen-garden"] .thesis-box p { margin: 0 auto; font-size: 1.6rem; font-style: italic; }

/* PRESET 3 LAYOUT (chronicle): Kinfolk Horizontal Chapter Banner + Editorial Pull-Quotes */
:root[data-preset="chronicle"] .report-section { grid-template-columns: 1fr; gap: 2.25rem; }
:root[data-preset="chronicle"] .section-sidebar {
  position: static;
  display: grid;
  grid-template-columns: auto 240px 1fr;
  align-items: baseline;
  gap: 1.5rem;
  border-bottom: 1px solid var(--border-strong);
  padding-bottom: 1rem;
}
:root[data-preset="chronicle"] .chapter-index { font-size: 2.35rem; margin-bottom: 0; }
:root[data-preset="chronicle"] .thesis-box p { font-size: 1.65rem; line-height: 1.38; }

/* PRESET 4 LAYOUT (sumi-ink): Fukinsei Asymmetric 38% / 62% Split */
:root[data-preset="sumi-ink"] .report-section { grid-template-columns: minmax(260px, 38%) 1fr; gap: 3.5rem; }
:root[data-preset="sumi-ink"] .thesis-box { border-left: 4px solid var(--accent); }

/* PRESET 5 LAYOUT (shoji-grid): Exposed 1px Structural Lattice */
:root[data-preset="shoji-grid"] .report-section { grid-template-columns: 220px 1fr; gap: 0; border-left: 1px solid var(--border); border-right: 1px solid var(--border); }
:root[data-preset="shoji-grid"] .section-sidebar { padding: 1.5rem; border-right: 1px solid var(--border); }
:root[data-preset="shoji-grid"] .section-content { padding: 1.5rem; }

/* PRESET 7 LAYOUT (yugen-noir): Progressive-Depth Stage + Gold Seam */
:root[data-preset="yugen-noir"] .thesis-box { border-left: 3px solid var(--accent); border-top: 1px solid var(--accent); }

.thesis-box {
  background: var(--bg-card);
  border: 1px solid var(--border-strong);
  border-left: 3px solid var(--accent);
  padding: 1.6rem 1.85rem;
  margin-bottom: 2rem;
  border-radius: var(--radius-card);
}
.thesis-box p {
  font-family: var(--font-display);
  font-weight: var(--display-weight);
  font-size: var(--text-thesis);
  line-height: 1.4;
  letter-spacing: -0.01em;
  font-optical-sizing: auto;
  font-feature-settings: "kern" 1, "liga" 1, "calt" 1;
  margin: 0;
  max-width: 54ch;
}
.thesis-box p em, .thesis-box p strong { color: var(--accent); font-weight: 400; font-style: italic; }

.kpi-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(195px, 1fr)); gap: 1.1rem; margin-bottom: 2rem; }
.kpi { padding: 1.35rem 1.3rem; background: var(--bg-card); border: 1px solid var(--border); border-radius: var(--radius-card); }
.kpi strong {
  display: block;
  font-family: var(--font-display);
  font-weight: var(--display-weight);
  font-size: var(--kpi-size);
  letter-spacing: -0.025em;
  line-height: 1.05;
  font-optical-sizing: auto;
  font-feature-settings: "kern" 1, "liga" 1, "calt" 1;
  margin: 0.55rem 0 0.35rem;
}
.kpi .subtext { font-family: var(--font-sans); color: var(--text-secondary); font-size: var(--text-sm); line-height: 1.5; }
.delta-pos { font-family: var(--font-mono); color: var(--status-ok); font-weight: 600; }
.delta-neg { font-family: var(--font-mono); color: var(--status-bad); font-weight: 600; }

.table-wrap { overflow-x: auto; margin: 1.25rem 0 1.75rem; border: 1px solid var(--border); border-radius: var(--radius-card); background: var(--bg-card); }
table { border-collapse: collapse; width: 100%; font-size: var(--text-sm); }
th, td { padding: 0.75rem 0.95rem; text-align: left; border-bottom: 1px solid var(--border); }
thead th { background: var(--bg-subtle); font-family: var(--font-mono); font-size: var(--text-xs); font-weight: 500; text-transform: uppercase; letter-spacing: 0.08em; color: var(--text-secondary); }
tbody th { background: transparent; font-family: var(--font-sans); font-size: var(--text-sm); font-weight: 500; text-transform: none; letter-spacing: 0; color: var(--text-primary); }
tr:hover td, tr:hover tbody th { background: var(--bg-subtle); }
.num, th.num { text-align: right; font-family: var(--font-mono); font-size: var(--text-sm); }

svg.chart { width: 100%; height: auto; display: block; background: var(--bg-card); border: 1px solid var(--border); border-radius: var(--radius-card); padding: 0.5rem; }
svg text { font-family: var(--font-mono); fill: var(--text-secondary); font-variant-numeric: tabular-nums; }

details { margin: 0.9rem 0; padding: 1.1rem 1.35rem; background: var(--bg-card); border: 1px solid var(--border); border-radius: var(--radius-card); }
summary { cursor: pointer; font-family: var(--font-display); font-size: var(--text-md); font-weight: var(--display-weight); letter-spacing: -0.01em; font-optical-sizing: auto; font-feature-settings: "kern" 1, "liga" 1, "calt" 1; }
pre, code { font-family: var(--font-mono); font-size: 0.82rem; background: var(--bg-subtle); padding: 0.14rem 0.4rem; border-radius: 4px; }
pre { overflow-x: auto; padding: 0.85rem; }

@media (max-width: 900px) {
  .report-section { grid-template-columns: 1fr; gap: 1.5rem; }
  .section-sidebar { position: static; }
  :root[data-preset="chronicle"] .section-sidebar { grid-template-columns: 1fr; gap: 0.4rem; }
}
```

## 5. Print CSS

```css
@media print {
  .no-print, nav, button, .filter-input, .skip { display: none !important; }
  body { background: #ffffff !important; color: #000000 !important; font-size: 10.5pt; line-height: 1.45; }
  .report-shell, main { max-width: 100% !important; padding: 0 !important; margin: 0 !important; }
  .report-section { grid-template-columns: 1fr !important; padding: 1.25rem 0 !important; gap: 0.75rem !important; }
  details:not([open]) > *:not(summary) { display: block !important; }
  section, .kpi, table, figure, details, .thesis-box { break-inside: avoid; page-break-inside: avoid; box-shadow: none !important; }
  h1, h2, h3 { break-after: avoid; }
  *, *::before, *::after { animation: none !important; transition: none !important; opacity: 1 !important; }
  @page { margin: 16mm 14mm; }
}
```

## 6. Interaction Patterns (Theme Toggle + Table Filter)

```js
const root = document.documentElement;

function storageGet(key) {
  try { return localStorage.getItem(key); } catch { return null; }
}

function storageSet(key, value) {
  try { localStorage.setItem(key, value); } catch { /* file:// or privacy mode */ }
}

const themeButton = document.getElementById("theme-toggle");
themeButton?.addEventListener("click", () => {
  const next = root.dataset.theme === "dark" ? "light" : "dark";
  root.dataset.theme = next;
  themeButton.setAttribute("aria-pressed", next === "dark" ? "true" : "false");
  storageSet("report-theme", next);
});

const storedTheme = storageGet("report-theme");
if (storedTheme) {
  root.dataset.theme = storedTheme;
  themeButton?.setAttribute("aria-pressed", storedTheme === "dark" ? "true" : "false");
}

function attachTableTools(table) {
  const rows = Array.from(table.tBodies[0].rows);
  if (rows.length <= 6) return;
  const input = document.createElement("input");
  input.type = "search";
  input.className = "filter-input no-print";
  input.placeholder = "Filter rows...";
  input.addEventListener("input", () => {
    const needle = input.value.toLowerCase();
    rows.forEach((row) => {
      row.hidden = !row.innerText.toLowerCase().includes(needle);
    });
  });
  table.parentElement.before(input);
}

document.querySelectorAll("table").forEach(attachTableTools);
```

## 7. Native SVG Chart Interaction & Data Labels

Use this pattern when the report contains bars, points, or segments. The table remains the accessible source of truth. Do not add a chart library for hover or labels.

### Markup

```html
<svg class="chart" role="group" aria-labelledby="chart-title chart-desc">
  <title id="chart-title">...</title>
  <desc id="chart-desc">...</desc>
  <rect x="72" y="69.2" width="26" height="150.8" fill="var(--chart-ps)"
        role="img" tabindex="0" data-series="Upgraded"
        data-tip="Upgraded Hit@1 · 78.52%" aria-label="Upgraded Hit@1 78.52%">
    <title>Upgraded Hit@1 78.52%</title>
  </rect>
  <text class="data-label above" aria-hidden="true" pointer-events="none"
        x="85" y="63.2" text-anchor="middle">78.52</text>
  <circle class="chart-point" role="img" tabindex="0" cx="46" cy="82.6" r="3"
          fill="var(--chart-ps)" data-series="Upgraded" data-day="2026-10-05"
          data-tip="2026-10-05 · Upgraded · 78.80%"
          aria-label="2026-10-05, Upgraded, 78.80%" data-chart-point="true"></circle>
  <text class="data-label point-upgraded" aria-hidden="true" pointer-events="none"
        x="51" y="76.6" text-anchor="start">78.80</text>
</svg>
<div class="chart-tooltip" id="chart-tooltip" role="status" aria-live="polite"></div>
```

Add `data-day` to the matching table row: `<tr data-day="2026-10-05" tabindex="0">`.

### CSS

```css
.chart [data-tip] { cursor: pointer; transition: opacity 0.15s ease, filter 0.15s ease; }
.chart [data-tip]:hover, .chart [data-tip]:focus-visible { filter: brightness(1.08); outline: 2px solid var(--accent); outline-offset: 2px; }
.chart .chart-point { stroke: var(--bg-card); stroke-width: 1; }
.chart .chart-point.is-active { stroke: var(--text-primary); stroke-width: 2; }
.chart.is-dimmed [data-series] { opacity: 0.28; }
.chart.is-dimmed [data-series].is-active { opacity: 1; }
.chart-tooltip { position: fixed; z-index: 30; max-width: 18rem; padding: 0.5rem 0.75rem; background: var(--bg-card); color: var(--text-primary); border: 1px solid var(--border-strong); border-radius: var(--radius-sm); font-size: var(--text-sm); line-height: 1.4; pointer-events: none; visibility: hidden; opacity: 0; transition: opacity 0.12s ease, transform 0.12s ease; }
.chart-tooltip[data-open="true"] { visibility: visible; opacity: 1; }
.chart-tooltip strong { display: block; font-weight: 600; }
.chart-tooltip span { color: var(--text-secondary); }
.data-label { font-family: var(--font-mono); font-size: 12px; font-weight: 500; pointer-events: none; }
.data-label.above { fill: var(--text-secondary); }
.data-label.inside { fill: var(--bg-card); }
.data-label.point-upgraded { fill: var(--chart-ps); }
.data-label.point-captured { fill: var(--chart-old); }
.data-label.point-production { fill: var(--chart-prod); }
tr.is-highlighted { background: var(--accent-subtle) !important; }
tr[data-day]:focus-visible { outline: 2px solid var(--accent); outline-offset: -2px; }
@media (prefers-reduced-motion: reduce) { .chart [data-tip], .chart-tooltip { transition: none; } }
@media print { .chart-tooltip { display: none !important; } }
```

### Interaction JS

```js
const tooltip = document.getElementById("chart-tooltip");

function place(event) {
  const pad = 12;
  const box = tooltip.getBoundingClientRect();
  let x = event.clientX + pad;
  let y = event.clientY + pad;
  if (x + box.width > window.innerWidth - pad) x = event.clientX - box.width - pad;
  if (y + box.height > window.innerHeight - pad) y = event.clientY - box.height - pad;
  tooltip.style.left = `${Math.max(pad, x)}px`;
  tooltip.style.top = `${Math.max(pad, y)}px`;
}

function placeAt(target) {
  const rect = target.getBoundingClientRect();
  const box = tooltip.getBoundingClientRect();
  let x = rect.left + rect.width / 2 - box.width / 2;
  let y = rect.top - box.height - 8;
  if (y < 12) y = rect.bottom + 8;
  x = Math.min(Math.max(12, x), window.innerWidth - box.width - 12);
  tooltip.style.left = `${x}px`;
  tooltip.style.top = `${y}px`;
}

function show(target, event) {
  const text = target.dataset.tip;
  if (!text) return;
  const [head, ...rest] = text.split(" · ");
  tooltip.replaceChildren();
  const strong = document.createElement("strong");
  strong.textContent = head;
  tooltip.append(strong);
  if (rest.length) {
    const span = document.createElement("span");
    span.textContent = rest.join(" · ");
    tooltip.append(span);
  }
  tooltip.dataset.open = "true";
  if (event) place(event); else placeAt(target);
}

const hide = () => { tooltip.dataset.open = "false"; };

document.querySelectorAll(".chart [data-tip]").forEach((mark) => {
  mark.addEventListener("pointerenter", (event) => show(mark, event));
  mark.addEventListener("pointermove", place);
  mark.addEventListener("pointerleave", hide);
  mark.addEventListener("focus", () => show(mark));
  mark.addEventListener("blur", hide);
});

document.querySelectorAll(".legend [data-series]").forEach((item) => {
  const figure = item.parentElement.querySelector("figure");
  const chart = figure?.querySelector(".chart");
  if (!chart) return;
  const activate = () => {
    chart.classList.add("is-dimmed");
    chart.querySelectorAll("[data-series]").forEach((mark) => {
      mark.classList.toggle("is-active", mark.dataset.series === item.dataset.series);
    });
  };
  const deactivate = () => {
    chart.classList.remove("is-dimmed");
    chart.querySelectorAll("[data-series]").forEach((mark) => mark.classList.remove("is-active"));
  };
  item.addEventListener("pointerenter", activate);
  item.addEventListener("pointerleave", deactivate);
  item.addEventListener("focus", activate);
  item.addEventListener("blur", deactivate);
});

document.querySelectorAll("[data-chart-point]").forEach((point) => {
  const row = document.querySelector(`tr[data-day="${point.dataset.day}"]`);
  const on = () => row?.classList.add("is-highlighted");
  const off = () => row?.classList.remove("is-highlighted");
  point.addEventListener("pointerenter", on);
  point.addEventListener("pointerleave", off);
  point.addEventListener("focus", on);
  point.addEventListener("blur", off);
});
document.querySelectorAll("tr[data-day]").forEach((row) => {
  const points = document.querySelectorAll(`[data-chart-point][data-day="${row.dataset.day}"]`);
  const on = () => points.forEach((point) => point.classList.add("is-active"));
  const off = () => points.forEach((point) => point.classList.remove("is-active"));
  row.addEventListener("pointerenter", on);
  row.addEventListener("pointerleave", off);
  row.addEventListener("focusin", on);
  row.addEventListener("focusout", off);
});
```

### Label rules

- Percentages use two decimals (`78.52`); counts use `k`/`M` (`501k`). Exact values stay in the tooltip and table.
- Keep labels at least `12px`. Place them horizontally above or below marks; widen bar centres to at least `44px` when five-character labels would collide.
- Inside a colored bar, use `fill="var(--bg-card)"` and verify contrast in both themes.
- Every data label is `aria-hidden="true"` and `pointer-events="none"`; the mark's `aria-label` carries the exact value.
- Never label every point on a dense series; label extrema or the focal series and leave the rest to the tooltip.
- Verify no overlap at 320px and 1440px, in light and dark themes, and in print.

## 8. Controlled Chart.js Opt-In

Use this block only when complex interactive charting is required, the user explicitly approves the CDN, the page shows an offline warning, and the tag carries a verified SHA-384 SRI hash. When approved, also add `https://cdn.jsdelivr.net` to the CSP `script-src` directive:

```html
<p class="no-print">This report loads Chart.js from a CDN. Offline viewing shows a static fallback.</p>
<script
  src="https://cdn.jsdelivr.net/npm/chart.js@4.4.1/dist/chart.umd.min.js"
  integrity="sha384-9nhczxUqK87bcKHh20fSQcTGD4qq5GhayNYSYWqwBkINBhOfQLg/P5HG5lF1urn4"
  crossorigin="anonymous"></script>
```

## 9. Structural Self-Check

Run the validator against the generated file. A non-zero exit blocks delivery:

```bash
python3 <skill-dir>/scripts/check_html_report.py <report>.html
```

`<skill-dir>` is the directory containing this skill, for example `~/.agents/skills/html-report`.

The validator checks the document skeleton, exactly one preset token block with no switcher, optional `data-layout` and `data-voice`, the Theme control, the Google Fonts stylesheet, CSP directives, dual-theme and reduced-motion CSS, print rules, optical sizing, `tabular-nums`, focus visibility, table headers, button types, duplicate IDs, inline event handlers, URL schemes, inline network calls, exact-origin external assets, sidecar paths, secret patterns, unresolved placeholders, and chart interaction markers when charts exist. It does not judge visual quality; run the render matrix in `references/review-gate.md`.

Keep this manual grep block as a fallback when the script cannot run. It cannot prove exact origins or size bounds; use the validator for the blocking verdict.

```bash
test -f <report>.html
grep -q '<!DOCTYPE html>' <report>.html
test "$(grep -o 'data-preset="[^"]*"' <report>.html | sort -u | wc -l | tr -d ' ')" -eq 1
! grep -q 'preset-' <report>.html
! grep -q 'expand-' <report>.html
! grep -q 'collapse-' <report>.html
! grep -q 'copy-sum' <report>.html
grep -q 'id="theme-toggle"' <report>.html
grep -q 'Content-Security-Policy' <report>.html
grep -q "connect-src 'none'" <report>.html
grep -q "base-uri 'none'" <report>.html
grep -q "form-action 'none'" <report>.html
grep -q 'fonts.googleapis.com' <report>.html
grep -q 'display=swap' <report>.html
# Check the font family for the chosen preset:
grep -q 'Fraunces' <report>.html          # dossier
# grep -q 'Cormorant+Garamond' <report>.html  # zen-garden / chronicle
grep -q 'prefers-color-scheme' <report>.html
grep -q 'prefers-reduced-motion' <report>.html
grep -q 'focus-visible' <report>.html
grep -q 'font-optical-sizing' <report>.html
grep -q '@media print' <report>.html
grep -q 'tabular-nums' <report>.html
! grep -Eq ' on[a-z]+=' <report>.html
! grep -q 'sendBeacon' <report>.html
! grep -q 'http-equiv="refresh"' <report>.html
! grep -q '<base ' <report>.html
! grep -q 'javascript:' <report>.html
! grep -q 'fetch' <report>.html
! grep -q 'REPLACE' <report>.html
```

## 10. Render Evidence

Capture the views required by the Visual Quality Bar in `references/review-gate.md`. Use browser automation already available in the environment; do not install a new browser stack without approval.

```bash
mkdir -p .tmp/report-review
# Playwright CLI, when already installed
npx playwright screenshot --viewport-size=1440,900 --full-page --color-scheme=light "file://$PWD/<report>.html" .tmp/report-review/desktop-light.png
npx playwright screenshot --viewport-size=390,844 --full-page --color-scheme=dark "file://$PWD/<report>.html" .tmp/report-review/mobile-dark.png
npx playwright pdf "file://$PWD/<report>.html" .tmp/report-review/report-print.pdf
```

If Playwright is unavailable, use the host browser's headless screenshot and print-to-PDF modes. If neither exists, stop the gate and request screenshots from the user. Do not substitute source inspection for rendered evidence.

Delete only captures that the review record does not link. Keep the screenshots referenced by the record.

## 11. Review Record

Use the template in `references/review-gate.md` section 6. Write the record beside the report, or in the host artifact directory for a session-only report.
