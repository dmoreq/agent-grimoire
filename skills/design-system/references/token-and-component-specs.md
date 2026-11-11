# Token, Archetype, Typography, Layout, and Component Specifications

Reference for `design-system`. It defines the 3-tier token model, the 13 palette archetypes, the 4 typographic voices, the 6 layout architectures, naming rules, theme parity, component spec format, responsive rules, and the implementation handoff. Mix rules live in `composition-grammar.md`. Do not restate them here.

## 1. Three-Tier Token Model

| Tier | Purpose | Example names | Consumer |
| :--- | :--- | :--- | :--- |
| Primitive | Raw scale values | `--stone-50` to `--stone-950`, `--space-1` to `--space-12`, `--radius-sm`, `--duration-fast` | Never used directly by components |
| Semantic | Role-based meaning | `--bg-canvas`, `--bg-surface`, `--bg-subtle`, `--text-primary`, `--intent-danger`, `--border-subtle`, `--focus-ring` | Components and layouts |
| Component | Component-scoped bindings | `--button-bg-hover`, `--button-border-focus`, `--input-border-error` | One component family |

Rules:
- A component references semantic or component tokens only.
- A semantic token maps to a primitive token, never to a raw value in two places.
- A theme changes semantic mappings, not component names.
- Token names use lowercase kebab-case with a role prefix.

## 2. Zen Minimalism Art Style & The 7 Curated Archetypes

Zen Minimalism is not restricted to a single warm-beige palette. It spans seven classical Japanese aesthetic principles (*Shibumi*, *Ma*, *Wabi-Sabi*, *Kanso*, *Seijaku*, *Datsuzoku*, *Yugen*) across warm earth, cool mineral, high-contrast sumi ink, architectural shoji grids, and nocturnal kintsugi depth.

- **Monochrome + 1 Accent (Organic & Mineral Surfaces)**: at least 90% of the viewport uses a calm neutral surface ramp tinted toward natural paper, limestone, rice paper, mineral mist, or obsidian charcoal. Reserve one intentional accent hue for the primary CTA, numbered chapter index, and active focus ring. Reserve status colors for live system feedback, never decorative badges.
- **Ma (Whitespace over boxes)**: treat emptiness as an active design material. Use 3.5-5.25rem macro spacing between sections (or `1px` exposed hairlines in `shoji-bento` grids) and 0.5-1rem micro spacing inside groups. Prefer a 1px hairline over a nested bordered card. Never place a bordered or shadowed card inside another.
- **Shibumi (Understated Typography & Prose Rhythm)**: use at most 2 primary font families (an editorial serif plus a UI sans, or a technical grotesk plus a humanist sans) and one monospace data face. Use at most 5 size tokens for product UI or the 9 editorial report roles below for reports. Hero KPI metrics may reach 2.5x-3x body; a page-title display may reach 3x+. Use display weights 300/350/400 (or 500 for sans-dominant voices), body 400, UI 500, and emphasis 600; never 700. Keep left-aligned axes, 60ch-70ch measure, and `tabular-nums` on numeric data. Cap prose paragraphs at 2-3 sentences (`<= 60 words`) so copy reads with calm authority.
- **Kanso (Typography as the primary graphic)**: do not add decorative illustrations, gradient blobs, floating 3D shapes, glassmorphism, or icon tiles above headings.
- No unmotivated purple-to-blue gradient: avoid `#8b5cf6` to `#3b82f6` as a default hero.
- No neon cyberpunk glow on B2B, admin, or data surfaces.
- No pure `#000000` or `#808080` neutrals on warm-paper palettes. Tint toward warm charcoal (`#22201E`), sumi ink (`#141413`), or deep indigo slate (`#16212B`). `apple-hig` dark canvas may keep its published `#000000`.
- No emoji as a functional icon. Use an SVG icon with an accessible name.
- No centered body text in an operational screen (reserve centered chapter headers strictly for contemplative single-column views like `zen-garden`).
- No decorative animation without a reduced-motion guard.

### The 7 Zen Minimalism Palette Archetypes (Dual Light/Dark Tokens)

The last column is the canonical triple. Use it on that palette's best-fit job. Other legal pairs are in `composition-grammar.md`.

| Archetype ID | Aesthetic Principle & Register | Light Mode (`--bg-canvas` / `--bg-surface` / `--bg-subtle` / `--text-primary` / `--text-secondary` / `--border-subtle` / `--border-strong` / `--intent-primary` / `--accent-subtle`) | Dark Mode (`--bg-canvas` / `--bg-surface` / `--bg-subtle` / `--text-primary` / `--text-secondary` / `--border-subtle` / `--border-strong` / `--intent-primary` / `--accent-subtle`) | Canonical triple |
| :--- | :--- | :--- | :--- | :--- |
| **`dossier`** | **Shibumi Clinical Dossier** *(Understated warm authority)* | `#F7F4EE` / `#FDFBF7` / `#EFEAE1` / `#22201E` / `#5A5550` / `#E0D9CE` / `#B8AFA3` / `#9E583B` (Muted Clay) / `#F2E5DF` | `#141210` / `#1D1A17` / `#27231F` / `#F5EFE6` / `#B8AFA6` / `#2E2924` / `#4A423B` / `#D48462` / `#2C1F1A` | `V1` (`Fraunces` + `Inter`) · `L1: sidebar-rail` |
| **`zen-garden`** | **Karesansui Dry Garden** *(Contemplative *Ma* & *Shizen*)* | `#F4F1EA` / `#F9F7F2` / `#EAE5DB` / `#2B2A27` / `#5E5C56` / `#DCD6CA` / `#BDB5A6` / `#4A6B53` (Kyoto Moss) / `#E3ECE5` | `#131614` / `#1B201C` / `#232A25` / `#ECEFE9` / `#ADB5AE` / `#29312B` / `#414D44` / `#7FA989` / `#1E2B22` | `V2` (`Cormorant Garamond` + `Inter`) · `L2: contemplative-column` |
| **`chronicle`** | **Kinfolk Slow Chronicle** *(*Wabi-Sabi* tactile editorial)* | `#FBF9F5` / `#F5F0E6` / `#EBE4D6` / `#211E1B` / `#5C564F` / `#E3DAC9` / `#C2B6A1` / `#A65638` (Terracotta) / `#EFE0D9` | `#161311` / `#201B18` / `#2A2420` / `#F7F1E8` / `#BAAFA4` / `#332B26` / `#4F433B` / `#DF8666` / `#2F1F19` | `V2` (`Cormorant Garamond` + `Plus Jakarta Sans`) · `L3: chapter-banner` |
| **`sumi-ink`** | **Sumi-e Ink Wash** *(*Kanso* stark rice-paper & brush ink)* | `#F6F6F4` / `#FFFFFF` / `#EBEBE7` / `#141413` / `#52524E` / `#DCDCD6` / `#AEAEA6` / `#B8332A` (Hanko Vermilion) / `#F7E3E1` | `#0E0E0E` / `#161615` / `#20201E` / `#F2F2EE` / `#B0B0A8` / `#2A2A27` / `#454540` / `#E55A4F` / `#2E1816` | `V1` (`Newsreader` + `Inter`) · `L4: fukinsei-split` or `L1` |
| **`shoji-grid`** | **Shoji Architectural Lattice** *(*Seijaku* structural 1px order)* | `#F8F7F4` / `#FFFFFF` / `#F0EFEA` / `#18181B` / `#52525B` / `#E4E3DD` / `#B8B6AE` / `#2E5A88` (Slate Cobalt) / `#E3ECF5` | `#0F1115` / `#161920` / `#1F242D` / `#F1F3F7` / `#A6B0C0` / `#262C36` / `#3D4656` / `#689BF2` / `#192436` | `V3` (`IBM Plex Sans` + `IBM Plex Mono`) · `L5: shoji-bento` |
| **`aizome-indigo`** | **Aizome Mineral Craft** *(*Datsuzoku* cool technical trust)* | `#F3F6F8` / `#FAFBFD` / `#E6EDF2` / `#16212B` / `#4A5A68` / `#D3DEE6` / `#9FB2C2` / `#264348` (Japan Indigo) / `#DFECEF` | `#0D151C` / `#14202B` / `#1C2C3A` / `#EBF1F5` / `#9EB1C2` / `#233545` / `#3A5369` / `#64A2B8` / `#162A33` | `V3` (`Space Grotesk` / `IBM Plex Sans` + `JetBrains Mono`) · `L1` or `L5` |
| **`yugen-noir`** | **Yugen Kintsugi Nocturne** *(*Yugen* shadowy depth & gold seam)* | `#F5F3EF` / `#FCFBF9` / `#EBE7DF` / `#1C1A17` / `#57524A` / `#DDD7CB` / `#B5AC9C` / `#9A7228` (Burnished Ochre) / `#F3ECE0` | `#0B0B0C` / `#131316` / `#1C1C21` / `#EFECE6` / `#AEA89E` / `#25252C` / `#3E3D47` / `#D4A853` (Kintsugi Gold) / `#282215` | `V2` (`Instrument Serif` + `Inter`) · `L6: yugen-canvas` |

### Scientific, Platform, and Monochrome Palettes

These six publish the roles below. Hex values match the **ux-product-shaper** archetype catalog. Map `--bg-subtle`, borders, and `--accent-subtle` with alpha of the published ink or accent, then measure contrast. Do not add a hue.

| Archetype ID | Canonical triple | Light (`--bg-canvas` / `--bg-surface` / `--text-primary` / `--intent-primary`) | Dark (`--bg-canvas` / `--bg-surface` / `--text-primary` / `--intent-primary`) | Published extras |
| :--- | :--- | :--- | :--- | :--- |
| **`simple-white`** | `V4` · `L2: contemplative-column` | `#FFFFFF` / `#FFFFFF` / `#111827` / `#1D4ED8` | `#0B0F19` / `#111827` / `#F9FAFB` / `#60A5FA` | Tufte spines, zero interior gridlines |
| **`plotly-white`** | `V4` · `L1: sidebar-rail` | `#FFFFFF` / `#FFFFFF` / `#1E293B` / `#636EFA` | `#0F172A` / `#1E293B` / `#F8FAFC` / `#818CF8` | Grid `#EBF0F8`. Chart series `#636EFA`, `#00CC96`, `#EF553B` |
| **`ggplot2-grammar`** | `V3` · `L5: shoji-bento` | `#FFFFFF` / `#EBEBEB` / `#262626` / `#F8766D` | `#121316` / `#1E2026` / `#F3F4F6` / `#FF8A80` | Panel grid `#FFFFFF`. Second chart series `#00BFC4` (dark `#26C6DA`), not a second UI accent |
| **`apple-hig`** | `V4` · `L1: sidebar-rail` | `#F5F5F7` / `#FFFFFF` / `#1D1D1F` / `#0071E3` | `#000000` / `#1C1C1E` / `#F5F5F7` / `#0A84FF` | 16px squircles. Dark canvas may keep this published `#000000` |
| **`material-you`** | `V4` · `L6: yugen-canvas` | `#F8F9FA` / `#F1F3F4` / `#1F1F1F` / `#0B57D0` | `#131314` / `#1E1F20` / `#E3E3E3` / `#A8C7FA` | 24px shadowless cards, pill indicators |
| **`geist-zinc`** | `V3` · `L5: shoji-bento` | `#FFFFFF` / `#FFFFFF` / `#09090B` / `#18181B` | `#09090B` / `#121215` / `#FAFAFA` / `#E4E4E7` | Hairline `#E4E4E7`. Status `#10B981`, `#F59E0B`, `#EF4444` |

## 3. Typography, Four Curated Voices, Spacing, Radius, and Motion Scales

### Four Curated Typographic Voices (`<= 2` primary font families + `1` monospace data face)

| Voice ID | `--font-display` | `--font-sans` | `--font-mono` | Display Weight & Tracking | Best-Fit Archetypes |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **`V1: editorial-authority`** | `'Fraunces'` or `'Newsreader'`, `"Iowan Old Style"`, `Georgia`, `serif` | `'Inter'`, `-apple-system`, `sans-serif` | `'JetBrains Mono'`, `ui-monospace`, `monospace` | `350`-`400`, `-0.022em`, `font-optical-sizing: auto` | `dossier`, `sumi-ink` |
| **`V2: classical-lyrical`** | `'Cormorant Garamond'` or `'Instrument Serif'`, `"Palatino Linotype"`, `Georgia`, `serif` | `'Plus Jakarta Sans'` or `'Inter'`, `-apple-system`, `sans-serif` | `'JetBrains Mono'`, `ui-monospace`, `monospace` | `300`-`400`, `-0.015em`, lyrical italics (`<em>`) | `zen-garden`, `chronicle`, `yugen-noir` |
| **`V3: technical-shibumi`** | `'IBM Plex Sans'` or `'Space Grotesk'`, `-apple-system`, `sans-serif` | `'IBM Plex Sans'`, `-apple-system`, `sans-serif` | `'IBM Plex Mono'` or `'JetBrains Mono'`, `monospace` | `400`-`500`, `-0.02em`, crisp geometric/grotesk | `shoji-grid`, `aizome-indigo` |
| **`V4: humanist-clarity`** | `'DM Sans'`, `-apple-system`, `sans-serif` | `'Inter'`, `-apple-system`, `sans-serif` | `'JetBrains Mono'`, `ui-monospace`, `monospace` | `400`-`500`, `-0.018em`, zero-ornament functional UI | Compact SaaS forms, mobile flows, settings |

### Product UI Type Scale (5 roles)

| Token | Size | Use |
| :--- | :--- | :--- |
| `--text-xs` | 0.75rem | Labels, captions, uppercase monospace eyebrows |
| `--text-sm` | 0.875rem | Secondary body, table cells |
| `--text-base` | 1rem | Body |
| `--text-lg` | 1.25rem | Section heading, lead paragraph |
| `--text-display` | 2.25rem+ | Page title, hero metric, chapter index |

Use at most 2 primary font families and one monospace data face. Do not add a third display face. Keep prose at 60ch-70ch, target 66ch. Apply `font-variant-numeric: tabular-nums` to metrics, prices, dates, and table numbers.

### Editorial Report Extension (9 roles)

Reports use these nine roles instead of the five product tokens. Component aliases may select a per-preset value.

| Role | Size | Use |
| :--- | :--- | :--- |
| `--text-xs` | 0.75rem | Eyebrows, labels, table headers, nav numbers |
| `--text-sm` | 0.875rem | Secondary body, table cells, section leads, code |
| `--text-base` | 0.95rem | Body prose |
| `--text-md` | 1.25rem | Summary/details, lead |
| `--text-lg` | 1.65rem | Section headings, thesis |
| `--text-xl` | 2rem | Zen/Chronicle section headings |
| `--text-2xl` | 2.5rem | KPI figures |
| `--text-3xl` | 2.85rem | Chapter indices |
| `--text-display` | `clamp(2.35rem, 4.2vw, 3.6rem)` | Page title; Zen/Chronicle override to `clamp(2.65rem, 4.8vw, 4.1rem)` |

Minimums: body prose `>= 0.9375rem`, labels `>= 0.75rem`, code and body monospace `>= 0.82rem`.

### Six Layout Architectures (Spatial Geometries)

| Layout ID | CSS Grid / Structural Pattern | Section / Cell Padding | When to Use |
| :--- | :--- | :--- | :--- |
| **`L1: sidebar-rail`** | `grid-template-columns: 240px 1fr; gap: 3rem; max-width: 1220px` | `3.5rem 0` | Technical audits, engineering dossiers, multi-chapter documentation (`dossier`, `aizome-indigo`). |
| **`L2: contemplative-column`** | `grid-template-columns: 1fr; max-width: 960px` with centered `640px` headers | `5.25rem 0` | Reflective essays, architectural narratives, linear reading (`zen-garden`). |
| **`L3: chapter-banner`** | `grid-template-columns: 1fr; max-width: 1020px` with `auto 240px 1fr` top chapter banner | `4.75rem 0` | Executive QBRs, magazine-style strategic reviews (`chronicle`). |
| **`L4: fukinsei-split`** | `grid-template-columns: minmax(280px, 38fr) 62fr; gap: 3.5rem; max-width: 1320px` | `4rem 0` | Asymmetric counterbalance (*Fukinsei*) for interactive explainers, scrollytelling, or master-detail specs (`sumi-ink`). |
| **`L5: shoji-bento`** | Exposed hairline grid (`background: var(--border-subtle); gap: 1px; border: 1px solid var(--border-strong)`) | `1.5rem 1.75rem` per cell | High-density developer specs, KPI matrices, modular bento layouts with zero nested cards (`shoji-grid`). |
| **`L6: yugen-canvas`** | Primary stage (`1fr`) + progressive disclosure `<details>` or collapsible `360px` context drawer | `3rem 0` | Deep workspaces, nocturnal command views, studio canvases (`yugen-noir`). |

### Spacing scale

Use a 4px base: `0.25rem`, `0.5rem`, `0.75rem`, `1rem`, `1.5rem`, `2rem`, `3rem`, `4rem`, `5.25rem`. Macro whitespace must exceed micro whitespace.

### Radius and motion

| Token | Value | Use |
| :--- | :--- | :--- |
| `--radius-none` | `0px` | `shoji-grid` flush cells, `sumi-ink` architectural blocks |
| `--radius-xs` | `0.375rem` | `chronicle` cards |
| `--radius-sm` | `0.25rem` | Inputs, chips, `zen-garden` / `aizome-indigo` cards |
| `--radius-md` | `0.5rem` | `dossier` / `yugen-noir` cards, buttons |
| `--radius-lg` | `0.75rem` | Modals, large panels |
| `--duration-fast` | `100ms` | Hover, focus |
| `--duration-base` | `180ms` | Expand, collapse |
| `--duration-slow` | `260ms` | Route or modal transition |

Wrap non-essential motion in `@media (prefers-reduced-motion: no-preference)`.

## 4. Theme Parity

| Check | Light target | Dark target |
| :--- | :--- | :--- |
| Body text on canvas | >= 4.5:1 | >= 4.5:1 |
| Secondary text on surface | >= 4.5:1 | >= 4.5:1 |
| Large text | >= 3.0:1 | >= 3.0:1 |
| Active UI boundary | >= 3.0:1 | >= 3.0:1 |
| Focus ring against adjacent surface | >= 3.0:1 | >= 3.0:1 |
| Disabled text | Still readable, clearly inactive | Still readable, clearly inactive |

Record the measured ratio next to each semantic pair. Do not claim parity without a measurement.

## 5. Component Specification Template

```markdown
# Component: <Name>

## Anatomy
- Root:
- Parts:
- Slots:

## Variants
| Variant | Use | Forbidden combination |
| :--- | :--- | :--- |
| primary | Main action | Never more than one per screen |
| secondary | Supporting action | Not for destructive work |
| danger | Destructive action | Requires confirmation |

## Props and Slots
| Name | Type | Required | Notes |
| :--- | :--- | :--- | :--- |

## States
| State | Visual | Behavior | Acceptance |
| :--- | :--- | :--- | :--- |
| default | | | |
| hover | | | |
| active | | | |
| focus-visible | | | |
| disabled | | | |
| loading | | | |
| error | | | |
| empty | | | |

## Usage
- Use when:
- Do not use when:
- Nearest alternative:

## Do / Do Not
- Do:
- Do not:

## Acceptance Criteria
- Visual:
- Behavioral:
- Accessibility:
```

Rules:
- Prefer semantic variants over boolean props. More than three boolean mode props is a smell.
- Each interactive component defines focus-visible, disabled, and loading where applicable.
- Each component states its accessible name and keyboard behavior.
- Each component references tokens, not raw values.

## 6. Responsive Layout Rules

| Concern | Rule |
| :--- | :--- |
| Macro layout | CSS Grid with `auto-fit` and `minmax()` |
| Local alignment | Flexbox |
| Reusable component | Container query with `container-type: inline-size` |
| Minimum width | 320px without horizontal page scroll |
| Maximum width | 1440px and above with a readable measure |
| Zoom | 200% without loss of content or function |
| Touch target | >= 24x24px, preferably 44x44px on mobile |
| Long text | `text-wrap: pretty`; headings use `text-wrap: balance` |
| Chip overflow | `+n` disclosure, not a clipped row |
| Tables | Horizontal scroll container, never page-level overflow |

## 7. Implementation Handoff

| Artifact | Destination |
| :--- | :--- |
| `tokens.css` / `tokens.json` | `html-report`, `plotly-dash`, `dashboard-design`, `python-pro`, `flutter-ui-responsive-a11y` |
| Component spec | The implementation skill and `code-review` |
| 8-state matrix | The implementation skill and `ui-accessibility` |
| Design system decisions | `docs/designs/YYYY-MM-DD_design-system_<topic>.md` |
| Legacy token retirement | `deprecation-migration` |

Handoff checklist:
- [ ] Locked palette (`dossier`, `zen-garden`, `chronicle`, `sumi-ink`, `shoji-grid`, `aizome-indigo`, `yugen-noir`, `simple-white`, `plotly-white`, `ggplot2-grammar`, `apple-hig`, `material-you`, or `geist-zinc`), layout geometry (`L1`-`L6`), typographic voice (`V1`-`V4`), and the composition ID from `composition-grammar.md` are recorded.
- [ ] Token roles and values are final.
- [ ] Light and dark parity is measured.
- [ ] Component anatomy, variants, and states are complete.
- [ ] Responsive rules and touch targets are stated.
- [ ] The implementation skill is named.
- [ ] `ui-accessibility` and `ux-critic` are named as post-implementation gates.

## 8. Anti-Patterns

- Hardcoded hex or arbitrary pixel values in a component.
- A component consuming `--slate-700` instead of `--text-secondary`.
- Boolean prop explosion for visual modes.
- Nested cards with competing borders.
- A second token system created beside the first.
- Theme parity asserted from a screenshot without a ratio.
- A token rename with no migration path.
- A component spec without states or acceptance criteria.

## 9. YAGNI Token and Prop Diet

- Emit at most 20-25 semantic tokens for a standalone app.
- No unused tokens or 10-step color ramps with no callers.
- Add component tokens only when a state transition cannot be expressed with semantic tokens.
- Native primitives first: `dialog`, `details`/`summary`, `input type="date"`, native `select` for 7 or fewer options, CSS Grid/Flex, and `@container` before custom JS or a UI library.
- Rule of Three: keep markup inline until the same visual and behavioral pattern repeats at least 3 times.
- Compound components over boolean props. More than three boolean mode props is a smell.

| Rationalization | Reality |
| :--- | :--- |
| Add a search bar, filter pills, and notification icon so the page looks complete. | Unrequested chrome is visual noise and maintenance debt. Do not render it. |
| Wrap each metric in a shadowed card with an icon badge. | Nested cards and decorative icons reduce the data-ink ratio. Use whitespace and type hierarchy. |
| Build a reusable component with 10 configuration props for future flexibility. | Premature abstraction violates the Rule of Three. Write concrete inline code until the pattern repeats. |
| Skip empty, error, and focus states to keep the code minimal. | Minimalism removes decoration, never usability scaffolding, state honesty, or accessibility. |

## 10. Static Minimalism Gate

- [ ] Every declared token has an active caller.
- [ ] No raw hex, rgb, or arbitrary pixel value outside the token files.
- [ ] No bordered or shadowed card inside another.
- [ ] No wrapper chain longer than three layout-neutral divs.
- [ ] Destructive actions use `--intent-danger`.
- [ ] At most one primary-filled CTA per view.
- [ ] At most three boolean mode props per component.
- [ ] At most 2 primary font families plus one monospace data face; 5 product sizes or 9 editorial report roles.
