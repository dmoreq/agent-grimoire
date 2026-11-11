# Product, Design Discovery, and State Contracts

Reference for `ux-product-shaper`. It defines the Spec-Design-Driven 5-Axis Discovery Grill, the 3 Surface Modes, the 7 Zen Aesthetic Archetypes, the 6 Layout Architectures, the 4-Lens UI/UX Brainstorm Cards, information architecture rules, the 8-state matrix, and the Zero-Decision `PRODUCT.md` template.

## 1. Surface Mode (3 Postures)

| Dimension | Mode A: Swiss / Zen Editorial (Persuade & Experience) | Mode B: Shibumi Utilitarian (Operate & Read) | Mode C: Shoji / Studio Hybrid (Create & Inspect) |
| :--- | :--- | :--- | :--- |
| Primary goal | Convince, delight, communicate narrative clarity | Complete a high-signal task or audit with low cognitive load | Author, explore, or compare artifacts in a calm workspace |
| Examples | Landing page, portfolio, executive chronicle, essay | Admin console, clinical/engineering dossier, data table, settings | Split-pane notebook, document studio, code/design inspector |
| Typography | Expressive display face, large scale contrast | Legible UI face or crisp serif, compact scale, tabular numbers | Balanced UI sans + precision mono, calm hierarchy |
| Layout | Asymmetry (*Fukinsei*), editorial rhythm, one strong focal point | Predictable grid, dense but aligned, one primary action | Primary canvas stage + collapsible *Yugen* context drawer or *Shoji* lattice |
| Motion | Orchestrated entry, deliberate reveal | Functional feedback only, under 200ms | Crisp drawer/panel transitions (`120-180ms`), zero bounce |
| Density | Low, generous *Ma* whitespace (`>= 40%`) | High data-ink ratio, progressive disclosure | Medium-high in inspector rails; airy on the primary canvas |
| Minimalist Register | Swiss editorial: page-title display at 3x+ and KPI/hero metrics at 2.5x-3x, asymmetry, at least 40% negative space, one focal CTA | Utilitarian: data-ink ratio, Jakob familiarity, tabular numbers, no decorative banner | Studio restraint: `1px` exposed hairlines, recessed tool wells, keyboard-first navigation |
| Navigation | Story anchors and a single CTA | Persistent navigation (<= 4 items), breadcrumbs, filters | Compact rail or command bar + contextual breadcrumbs |
| Failure mode | Style hides the action or slows reading | A brand hero competes with the task | Chrome squeezes the canvas below readable measure |

If a screen mixes incompatible postures (such as a persuasive marketing hero above a dense operational table), split it into two surfaces.

## 2. The 5-Axis Spec-Design-Driven Grill Bank

During Gate 1, grill the user one question at a time (with a 1-sentence hypothesis and confidence `%`) or present an unranked 3-option trade-off table when they ask to compare options upfront. Never mark an option `(Recommended)`.

### Axis 1: Surface Mode Question Template
- **Prompt**: "Is this surface meant to persuade/narrate (`Mode A: Editorial`), execute high-density operational/analytical reading (`Mode B: Utilitarian`), or support interactive creation/inspection (`Mode C: Studio Hybrid`)? *(Hypothesis: Mode B at 80% confidence based on your benchmark tables.)*"

### Axis 2: Style Family & Aesthetic Archetype Catalog (13 Curated Archetypes Across 4 Families)
Present up to 3 archetypes across the 4 style families (Zen Minimalism, Scientific & Plotly Grammar, Platform Native, Modern Monochrome) so the user can choose between warm organic paper, pure scientific white, `ggplot2` warm-grey plot panels, Apple HIG frosted daylight, Material 3 tonal containers, or Vercel Geist zinc monochrome:

| Archetype ID | Family & Principle | Light Canvas / Card / Ink / Accent | Dark Canvas / Card / Ink / Accent | Best-Fit Domain & Failure Condition |
| :--- | :--- | :--- | :--- | :--- |
| **`dossier`** | **Zen Minimalism** (*Shibumi* — understated authority) | `#F7F4EE` / `#FDFBF7` / `#22201E` / `#9E583B` (Muted Clay) | `#141210` / `#1D1A17` / `#F5EFE6` / `#D48462` | Engineering audits, benchmark evaluations, decision memos. *Fails when*: brand requires pure white or cool corporate neutrality. |
| **`zen-garden`** | **Zen Minimalism** (*Ma* & *Shizen* — organic stillness) | `#F4F1EA` / `#F9F7F2` / `#2B2A27` / `#4A6B53` (Kyoto Moss) | `#131614` / `#1B201C` / `#ECEFE9` / `#7FA989` | Contemplative essays, architectural reviews, sustainability narratives. *Fails when*: used for high-frequency trading or dense admin forms. |
| **`chronicle`** | **Zen Minimalism** (*Wabi-Sabi* — warm tactile editorial) | `#FBF9F5` / `#F5F0E6` / `#211E1B` / `#A65638` (Terracotta) | `#161311` / `#201B18` / `#F7F1E8` / `#DF8666` | Executive QBRs, product launches, long-form strategic storytelling. *Fails when*: applied to compact utility modals. |
| **`sumi-ink`** | **Zen Minimalism** (*Kanso* — stark brush contrast) | `#F6F6F4` / `#FFFFFF` / `#141413` / `#B8332A` (Hanko Vermilion) | `#0E0E0E` / `#161615` / `#F2F2EE` / `#E55A4F` | Financial filings, legal/policy specs, monochrome editorial portfolios. *Fails when*: vermilion accent is overused on non-focal elements. |
| **`shoji-grid`** | **Zen Minimalism** (*Seijaku* — structural `1px` order) | `#F8F7F4` / `#FFFFFF` / `#18181B` / `#2E5A88` (Slate Cobalt) | `#0F1115` / `#161920` / `#F1F3F7` / `#689BF2` | Developer tools, API docs, modular bento dashboards, system architecture specs. *Fails when*: `1px` grid cells contain nested bordered cards. |
| **`aizome-indigo`** | **Zen Minimalism** (*Datsuzoku* — calm technical trust) | `#F3F6F8` / `#FAFBFD` / `#16212B` / `#264348` (Japan Indigo) | `#0D151C` / `#14202B` / `#EBF1F5` / `#64A2B8` | Cloud infrastructure, security audits, healthcare/fintech SaaS, quant research. *Fails when*: warm sepia chart palettes are mixed unadjusted into cool indigo surfaces. |
| **`yugen-noir`** | **Zen Minimalism** (*Yugen* — shadowy depth, dark-first) | `#F5F3EF` / `#FCFBF9` / `#1C1A17` / `#9A7228` (Burnished Ochre) | `#0B0B0C` / `#131316` / `#EFECE6` / `#D4A853` (Kintsugi Gold) | Media/creative studios, executive night-mode command centers, AI/ML observability. *Fails when*: gold accent is applied to large fills with low text contrast. |
| **`simple-white`** | **Scientific & Plotly** (`simple_white` / Tufte Spine) | `#FFFFFF` / `#FFFFFF` / `#111827` / `#1D4ED8` (Academic Blue) | `#0B0F19` / `#111827` / `#F9FAFB` / `#60A5FA` | Academic papers, quantitative whitepapers, print-first statistical reports with crisp black L-axis spines, external tick marks, and zero gridlines. *Fails when*: wide multi-series charts lack hover or grid reference lines. |
| **`plotly-white`** | **Scientific & Plotly** (`plotly_white` Analytical Grid) | `#FFFFFF` / `#FFFFFF` / `#1E293B` / `#636EFA` (Plotly Royal) | `#0F172A` / `#1E293B` / `#F8FAFC` / `#818CF8` | Data science notebooks, BI analytics dashboards, multi-series line/scatter explorers using `#EBF0F8` (`1px`) gridlines and `#636EFA`/`#00CC96`/`#EF553B` traces. *Fails when*: used for literary long-form essays. |
| **`ggplot2-grammar`** | **Scientific & Plotly** (`ggplot2` Grammar of Graphics) | `#FFFFFF` / `#EBEBEB` (plot/card panel) / `#262626` / `#F8766D` (gg Coral) & `#00BFC4` (gg Teal) | `#121316` / `#1E2026` / `#F3F4F6` / `#FF8A80` & `#26C6DA` | Statistical modeling, faceted small multiples (`facet_col`), R/Tidyverse research outputs where `#EBEBEB` grey panels with crisp `#FFFFFF` gridlines anchor precision. *Fails when*: applied to marketing landing pages. |
| **`apple-hig`** | **Platform Native** (Apple HIG / Cupertino Daylight) | `#F5F5F7` / `#FFFFFF` / `#1D1D1F` / `#0071E3` (System Blue) | `#000000` / `#1C1C1E` / `#F5F5F7` / `#0A84FF` | Consumer/prosumer macOS & iOS dashboards, wealth trackers, health metrics with `#F5F5F7` grouped canvas, continuous `16px` squircle cards, and `backdrop-filter: blur(20px)` vibrancy headers. *Fails when*: over-packed with dense `1px` table borders. |
| **`material-you`** | **Platform Native** (Google Material 3 Tonal Surface) | `#F8F9FA` / `#F1F3F4` (`Surface Container`) / `#1F1F1F` / `#0B57D0` (Google Blue) | `#131314` / `#1E1F20` / `#E3E3E3` / `#A8C7FA` | Cross-platform workspace apps, Android/Flutter & web productivity consoles using shadowless tonal surface elevation (`Surface Container Low/High`), `24px` cards, and `9999px` pill active indicators. *Fails when*: heavy drop shadows are mixed with tonal fills. |
| **`geist-zinc`** | **Modern Monochrome** (Vercel Geist / Shadcn Zinc) | `#FFFFFF` / `#FFFFFF` / `#09090B` / `#18181B` (Zinc Primary) | `#09090B` / `#121215` / `#FAFAFA` / `#E4E4E7` | Modern developer SaaS, AI/infra consoles, minimal white-and-black apps with pure `#FFFFFF` canvas, `1px solid #E4E4E7` (`zinc-200`) razor borders, zero shadows, and semantic status dots (`#10B981`, `#F59E0B`, `#EF4444`). *Fails when*: warm decorative gradients are injected. |

### Axis 3: Layout Architecture Catalog (6 Structural Geometries)

| Layout ID | Geometry & CSS Grid | Spatial Rhythm | Best For / Avoid For |
| :--- | :--- | :--- | :--- |
| **`L1: sidebar-rail`** | `240px` sticky chapter sidebar + `1fr` fluid evidence column (`1220px` max) | `3.5rem` section pad, `3rem` column gap | Multi-section audits, technical specs, documentation (`dossier` default). *Avoid for*: short 1-screen forms. |
| **`L2: contemplative-column`** | Centered single column (`960px` shell, `65ch` prose, `640px` headers) | `5.25rem` vertical *Ma* breathing room | Long-form essays, post-mortems, single-flow wizards (`zen-garden` default). *Avoid for*: multi-table side-by-side comparisons. |
| **`L3: chapter-banner`** | `1020px` magazine column with full-width `auto 240px 1fr` horizontal chapter headers | `4.75rem` section pad, oversized pull-quotes | Executive narratives, QBRs, case studies (`chronicle` default). *Avoid for*: dense CRUD admin consoles. |
| **`L4: fukinsei-split`** | Asymmetric golden-ratio split (`38%` sticky narrative/context + `62%` interactive stage, `1320px` max) | Intentional counterbalance (`Fukinsei`); generous left margin | Interactive explainers, scrollytelling, product showcases, Master-Detail workflows. *Avoid for*: wide 10-column spreadsheets. |
| **`L5: shoji-bento`** | Exposed `1px solid var(--border)` CSS Grid lattice (`gap: 1px; background: var(--border)`) where cells sit flush | Zero outer card shadows, zero nested cards, `1.5rem-2rem` cell padding | System architecture matrices, KPI command strips, developer spec sheets (`shoji-grid` default). *Avoid for*: lyrical prose essays. |
| **`L6: yugen-canvas`** | Full-viewport primary canvas (`100%`) with progressive-disclosure `<details>` or slide-over inspector drawer (`360px`) | Calm uncluttered stage; secondary metadata hidden until invoked | Studios, graph explorers, clean workflow tools. *Avoid for*: print-only static memos unless drawer content expands in `@media print`. |

### Axis 4: Typographic Voice Pairings (4 Curated Voices)

| Voice ID | Display / Heading (`--font-display`) | Body / UI (`--font-sans`) | Data / Code (`--font-mono`) | Character & Optical Tuning |
| :--- | :--- | :--- | :--- | :--- |
| **`V1: editorial-authority`** | `'Fraunces'` or `'Newsreader'` (weight `350`/`400`, optical size auto) | `'Inter'` (`400`/`500`) | `'JetBrains Mono'` | Crisp, modern editorial authority with high small-size legibility (`dossier`, `sumi-ink`). |
| **`V2: classical-lyrical`** | `'Cormorant Garamond'` or `'Instrument Serif'` (`300`/`400`, expressive italics) | `'Plus Jakarta Sans'` or `'Inter'` | `'JetBrains Mono'` | Literary, contemplative, high-contrast grace (`zen-garden`, `chronicle`, `yugen-noir`). |
| **`V3: technical-shibumi`** | `'IBM Plex Sans'` or `'Space Grotesk'` (`400`/`500`, tight `-0.02em` tracking) | `'IBM Plex Sans'` (`400`/`500`) | `'IBM Plex Mono'` | Sans-dominant Swiss-Japanese industrial precision (`shoji-grid`, `aizome-indigo`). |
| **`V4: humanist-clarity`** | `'DM Sans'` (`400`/`500`) | `'Inter'` (`400`/`500`) | `'JetBrains Mono'` | Quiet, zero-ornament functional UI for settings, forms, and mobile-first flows. |

## 3. Four-Lens UI/UX Brainstorm Cards (Pre-Brief Stress Test)

Before locking Gate 2, evaluate the chosen 5-axis design against these four stateless checks (dispatch in parallel on Tier 1 hosts or run sequentially in cold-read order on Tier 2 hosts):

1. **Lens 1: Kanso / YAGNI Subtractor**: Which requested or implied widget, nav item, filter, or card border can be deleted without hurting the primary user decision? Are there more than 4 nav items or 4 KPIs?
2. **Lens 2: Cognitive Load & Ma Rhythm**: Does the first viewport pass the 2-second squint test with a single focal point? Is macro whitespace (`3.5rem-5.25rem`) strictly larger than micro group spacing (`0.5rem-1rem`)?
3. **Lens 3: State & Edge-Case Honesty**: What happens when the dataset is empty, 1 row, 10,000 rows, slow (`3s` latency), partially failed, or translated into German (+40% string length)?
4. **Lens 4: Aesthetic-Domain Register Fit**: Does the recorded composition match the job band in the **design-system** composition grammar? A legal cross of palette and layout passes. A canonical triple outside that palette's best-fit job fails. Casual asymmetry still fails on financial numbers that need tabular precision.

## 4. YAGNI Exclusions

Build only the views, inputs, and controls the prompt requires. Unless the prompt asks for them, do not render:

- Top navbar or sidebar.
- Search input or filter bar.
- Notification bell.
- Avatar or profile menu.
- Settings gear.
- Dark-mode toggle.
- Pagination controls.
- Export CSV or PDF button.

Rules:
- One primary CTA per view. Demote secondary actions to text, ghost controls, or progressive disclosure.
- At most 4 top-level navigation items.
- At most 3-4 summary KPIs.
- Record a "What We Are NOT Building" list in the brief.
- **Lazy, Not Negligent**: YAGNI removes speculative features and abstraction, never the 8 states, validation, WCAG 2.2 AA, or 24x24px targets.

## 5. Information Architecture Rules

1. **One primary decision per screen.** Name it in one sentence. If two decisions compete, split the screen.
2. **One focal point.** The most important metric or action must be unmistakable within two seconds.
3. **Three to five chunks.** Limit the first view to 3-5 progressive disclosure groups. More groups raise scanning cost.
4. **Hick's Law.** Each additional equal-weight choice increases decision time. Group or hide secondary choices.
5. **Jakob's Law.** Users expect familiar placement. Do not relocate navigation, search, or primary actions without a strong reason.
6. **Progressive disclosure.** Show the decision first, details on demand. Use explicit expand controls, not hidden hover-only content.
7. **Recovery path.** Every primary flow needs a cancel, back, undo, or retry path.
8. **Scope boundary.** Record what the screen intentionally does not do. Unowned edge cases become future defects.
9. **Wording budget.** Cap section leads at `<= 25 words` and body paragraphs at `2-3 sentences` (`<= 60 words`).

## 6. The 8-State Matrix

Define every state before implementation. Each state needs realistic example data and an acceptance check.

| State | Purpose | Required UI behavior | Anti-pattern |
| :--- | :--- | :--- | :--- |
| Ideal | Prove the normal case | Complete layout with real domain data | Lorem Ipsum, John Doe, fake numbers |
| Empty | Explain absence and offer the next step | One sentence of cause plus a primary action | Blank panel, disabled everything, no guidance |
| Loading | Preserve trust during a wait | Skeleton that matches final geometry, or inline spinner; announce with `aria-live` | Whole-screen dim that looks disabled; layout jump |
| Partial | Show value before everything arrives | Render available rows or modules, label the pending part | Hide all data until the slowest request finishes |
| Error / Validation | Explain cause and recovery | Inline field message, specific cause, exact fix, preserved input | Red border alone, generic toast, cleared form |
| Disabled / Read-Only | Explain why unavailable | Visible control with helper text or tooltip describing the condition to enable it | Silent grey control, no reason, no path forward |
| Text Overflow / i18n | Survive longer content | Wrap, truncate with disclosure, `+n` chips, long URL handling | Clip, overlap, horizontal page scroll |
| Keyboard / Screen Reader | Equal access without a mouse | Logical tab order, visible focus, Escape closes, focus returns to the trigger, `aria-live` for async updates | Mouse-only controls, focus lost after modal close, unlabeled inputs |

## 7. Zero-Decision Product & UI/UX Brief Template

Save as `docs/designs/YYYY-MM-DD_product-brief_<topic>.md`.

```markdown
# Product Brief: <Surface Name>

- Date: YYYY-MM-DD
- Owner: <name>
- Status: Draft | Approved (Gate 1 & Gate 2 Locked)
- Source spec: <path or link>

## Audience and Job

- Primary user:
- Job to be done:
- One-sentence screen thesis (<= 20 words):
- Current workaround:

## Locked 5-Axis Spec-Design-Driven Matrix

| Axis | Locked Choice | Rationale & Rejected Alternatives |
| :--- | :--- | :--- |
| 1. Surface Mode | Mode A (Editorial) \| Mode B (Utilitarian) \| Mode C (Studio Hybrid) | |
| 2. Style Family & Archetype | `dossier` \| `zen-garden` \| `chronicle` \| `sumi-ink` \| `shoji-grid` \| `aizome-indigo` \| `yugen-noir` \| `simple-white` \| `plotly-white` \| `ggplot2-grammar` \| `apple-hig` \| `material-you` \| `geist-zinc` | |
| 3. Layout Architecture | `L1: sidebar-rail` \| `L2: contemplative-column` \| `L3: chapter-banner` \| `L4: fukinsei-split` \| `L5: shoji-bento` \| `L6: yugen-canvas` | |
| 4. Typographic Voice | `V1: editorial-authority` \| `V2: classical-lyrical` \| `V3: technical-shibumi` \| `V4: humanist-clarity` | |
| 5. Density & Chrome Scope | Contemplative \| Balanced \| High-Density Operational | |
| Composition | `<palette> × <layout> × <voice> × <density> × <primary-module>` | |
| Creative note | One sentence: the primary module and the job reason. | |

## Primary Flow

1. Entry:
2. Primary action:
3. Completion signal:
4. Recovery path:

## Information Architecture

- Focal point:
- First-view chunks (3-5):
- Out of scope:

## What We Are NOT Building

- Unrequested navigation, search, filter, account, or export chrome
- Single-use wrappers and speculative configuration
- Decorative cards, badges, or illustrations without a task role

## 8-State Contract

| State | Example data | UI behavior | Acceptance check |
| :--- | :--- | :--- | :--- |
| Ideal | | | |
| Empty | | | |
| Loading | | | |
| Partial | | | |
| Error / Validation | | | |
| Disabled / Read-Only | | | |
| Text Overflow / i18n | | | |
| Keyboard / Screen Reader | | | |

## Success Metrics

- Metric:
- Event or signal:
- Target:
```

## 8. Anti-Patterns

- Silently defaulting to a single warm-beige theme without grilling the user when domain or aesthetic requirements are open.
- Shipping the canonical triple for a job outside that palette's best-fit row.
- Coding before the 5-Axis Design Matrix and Surface Mode are fixed.
- Treating the happy path as the whole screen.
- Using placeholder names or numbers in a brief that reviewers will treat as real.
- Loading states that remove layout geometry or look disabled.
- Error states that say "Something went wrong" without a cause or fix.
- Disabled controls with no explanation.
- Hover-only disclosure that keyboard users cannot reach.
- Mixing a persuasive hero with an operational task on one screen.
- Adding a search bar, filter pills, or notification icon so the page "looks complete". This violates YAGNI.
- Wrapping every metric in a shadowed card with an icon badge. This violates the data-ink ratio.
- Building a reusable component with many configuration props for future flexibility. This violates the Rule of Three.
- Skipping empty, error, or focus states to keep the code minimal. This violates the Lazy, Not Negligent boundary.

## 9. Gate Checklist

- [ ] Gate 1 Socratic grill locked all 5 design axes with the owner.
- [ ] Surface Mode recorded with a reason.
- [ ] YAGNI exclusions list exists and bans unrequested chrome.
- [ ] One primary CTA per view; at most 4 top-level navigation items; at most 3-4 KPIs.
- [ ] One focal point per screen.
- [ ] Primary flow includes completion and recovery.
- [ ] All eight states have example data and acceptance checks.
- [ ] Out-of-scope items are explicit, including the "What We Are NOT Building" list.
- [ ] Success metrics name an event or signal.
- [ ] The brief path uses `docs/designs/YYYY-MM-DD_product-brief_<topic>.md`.
