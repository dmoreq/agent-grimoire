---
name: design-system
description: >-
  Build and maintain a 3-tier W3C DTCG design token system, dual light/dark themes,
  13 curated archetypes across 4 style families (Zen Minimalism, Scientific/Plotly,
  Platform Native, Modern Monochrome), 4 typographic voices, 6 layout geometries,
  and a job-band composition grammar.
risk: safe
source: local
date_added: "2026-10-28"
---

# Design System Skill

Own the visual contract between product intent and implementation: tokens, palettes, typography, layout geometry, components, states, responsive rules, and the handoff to code across **4 Style Families (13 Curated Archetypes)**.

## When to Use
- Bootstrapping a visual identity for a new product, dashboard, or report surface.
- Translating a locked 5-Axis Design Matrix from `ux-product-shaper` into W3C DTCG tokens and component specs.
- Creating or updating a token system, theme, or component library across Zen Minimalism, Scientific/Plotly (`simple-white`, `plotly-white`, `ggplot2-grammar`), Platform Native (`apple-hig`, `material-you`), or Modern Monochrome (`geist-zinc`).
- Retheming an application for light and dark modes with measured WCAG parity.
- Auditing hardcoded colors, spacing, or one-off variants.

## When Not to Use
- UX discovery, Socratic 5-axis design grilling, information architecture, or the 8-state product contract (`ux-product-shaper`).
- WCAG conformance audit and keyboard testing (`ui-accessibility`).
- Writing production UI code (`html-report`, `plotly-dash`, `python-pro`, `flutter-ui-responsive-a11y`).
- Adversarial critique of a rendered screen (`ux-critic`).
- Feature scoping without a user interface (`spec-driven-design`).

## Artifact Paths
- Design system spec: `docs/designs/YYYY-MM-DD_design-system_<topic>.md`. Topic slugs follow the artifact slug and containment rule in `rules/AGENTS.md` §4.
- Token export: `docs/designs/YYYY-MM-DD_tokens_<topic>.css` and `.json`.
- Session fallback: the host artifact directory with the same ISO date prefix.
- Never write an undated file at the repository root.

## Workflow

### Step 1: Lock the Style Family & Archetype (13 Presets), Layout Geometry & Typographic Voice
1. Read the product brief from `ux-product-shaper`: Surface Mode, archetype, layout, voice, audience, and constraints. If the look is open, present up to 3 unranked job-band rows from `references/composition-grammar.md`. If the look is delegated, use that file's stable task-slug rule. Emit the canonical triple only on that palette's best-fit job.
2. **Monochrome + 1 Accent Across 4 Style Families (13 Archetypes)**: render at least 90% of the viewport from a neutral ramp paired with high-contrast ink, reserving one accent for the primary CTA, chapter index, and focus ring. Hex rows live in `references/token-and-component-specs.md`:
   - **Zen Minimalism (7)**: `dossier`, `zen-garden`, `chronicle`, `sumi-ink`, `shoji-grid`, `aizome-indigo`, `yugen-noir`.
   - **Scientific & Plotly Grammar (3)**: `simple-white`, `plotly-white`, `ggplot2-grammar`.
   - **Platform Native Minimalism (2)**: `apple-hig`, `material-you`.
   - **Modern Developer Monochrome (1)**: `geist-zinc`.
   - Reserve status colors for live system feedback, never decorative badges.
3. Ban unmotivated purple-to-blue gradients, neon glows on B2B surfaces, decorative blobs, icon tiles above headings, or untinted `#808080`.
4. **Typography Caps & Four Curated Voices**:
   - Declare at most 2 primary font families per active view plus one monospace data face (`--font-mono`).
   - Select one of the 4 voices in `references/token-and-component-specs.md`: **V1 Editorial Authority** (`Fraunces`/`Newsreader` + `Inter`), **V2 Classical Lyrical** (`Cormorant Garamond`/`Instrument Serif` + `Plus Jakarta Sans`/`Inter`), **V3 Technical Shibumi** (`IBM Plex Sans`/`Space Grotesk` + `IBM Plex Mono`), or **V4 Humanist Clarity** (`DM Sans`/`Inter` + `JetBrains Mono`).
   - Use at most 5 size tokens for product UI, or the 9 editorial roles in the reference for reports.
   - Use display weights `300`/`350`/`400` (or `500`-`600` for sans-dominant `V3`/`V4`), body `400`, UI `500`, and emphasis `600`. Apply tight letter-spacing (`-0.02em`) and `font-optical-sizing: auto` on display headings and hero figures.
   - Size hero KPI figures at `2.5x-3x` body; page-title display may reach `3x+` body.
   - Apply `font-variant-numeric: tabular-nums` and `--font-mono` to numeric columns, deltas, and SVG chart axes. Keep prose paragraphs to 2-3 sentences (`<= 60 words`, `60ch-70ch` measure, target `66ch`).
5. **Spatial Rhythm & Six Layout Architectures**: use `L1`–`L6` in `references/token-and-component-specs.md`. Use 3.5-5.25rem macro spacing between sections and 0.5-1rem micro spacing inside groups. Prefer a 1px hairline or tonal surface shift over nested bordered cards. Legal mixes are in `references/composition-grammar.md`.

### Step 2: Build the Three-Tier Token System
Full token, archetype, voice, layout, and component templates live in `references/token-and-component-specs.md`.

| Tier | Contains | Rule |
| :--- | :--- | :--- |
| Primitive | Raw color ramps, 4px spacing scale, radii, durations | Never consumed directly by components |
| Semantic | Surface, text, intent, border, focus, typography roles | The only tier components may reference |
| Component | Explicit bindings for hover, active, focus-visible, disabled | Scoped to one component family |

Required semantic roles:
- Surfaces: `--bg-canvas`, `--bg-surface`, `--bg-subtle`, `--bg-elevated`, `--bg-overlay`.
- Text: `--text-primary`, `--text-secondary`, `--text-muted`, `--text-on-accent`.
- Intent: `--intent-primary`, `--intent-danger`, `--intent-warning`, `--intent-success`.
- Borders and focus: `--border-subtle`, `--border-strong`, `--focus-ring`.
- Destructive actions must use `--intent-danger`, never the primary accent.

**YAGNI token diet**:
- Emit at most 20-25 semantic tokens for a standalone app. Add component tokens only when a state transition cannot be expressed with semantic tokens.
- Do not emit unused tokens or a 10-step color ramp with no callers. Every declared token must have an active caller.

### Step 3: Verify Theme Parity
- Body text contrast is at least 4.5:1 in both light and dark themes across all 13 archetypes.
- Large text and active UI boundaries are at least 3.0:1.
- Export `tokens.css` and `tokens.json` with identical role names.

### Step 4: Write Component Specifications
Every component spec contains:
- Anatomy, semantic variants (prefer `variant="danger"` over boolean flags), props/slots, and states (`default`, `hover`, `active`, `focus-visible`, `disabled`, `loading`, `error`, `empty`).
- Usage rules, do/do not examples, and visual/behavioral/accessibility acceptance criteria.
- **YAGNI handoff**: native primitives first (`dialog`, `details`/`summary`, `input type="date"`, native `select`, CSS Grid/Flex, `@container`), Rule of Three before extracting wrappers, compound components over boolean mode props (more than 3 boolean props is a design smell), and zero nested bordered cards.

### Step 5: Define Responsive Layout Rules
- Use CSS Grid with `auto-fit` and `minmax()` for macro layout; Flexbox for local alignment; `@container` for reusable components.
- Support 320px to 1440px and 200% browser zoom without horizontal page scroll.
- Keep touch targets at least 24x24px (preferably 44x44px on mobile).
- Use `text-wrap: balance` on headings, `text-wrap: pretty` on body text, and `@media (prefers-reduced-motion: no-preference)` on motion.

### Step 6: Hand Off to Implementation
- Hand tokens and specs to `html-report`, `plotly-dash`, `dashboard-design`, `python-pro`, or `flutter-ui-responsive-a11y`.
- Give the implementer the token files, component acceptance criteria, and the 8-state matrix from `ux-product-shaper`.
- Hand the result to `ui-accessibility` for the WCAG audit and to `ux-critic` for heuristic critique.
- When retiring an old token or component, use `deprecation-migration`.

## Static Minimalism Gate
Before handoff, fail the design system if any check fails:
- [ ] Any declared token has zero active references.
- [ ] Any raw hex, rgb, or arbitrary pixel value appears outside the token files.
- [ ] Any bordered or shadowed card is nested inside another.
- [ ] Any wrapper chain exceeds three consecutive layout-neutral divs.
- [ ] Any destructive action uses the primary accent instead of `--intent-danger`.
- [ ] Any view has more than one primary-filled CTA.
- [ ] Any component has more than three boolean mode props.

## Rules
- No hardcoded hex, rgb, or arbitrary pixel values outside the token files.
- No component consumes a primitive token directly.
- No unused token or 10-step ramp without an active caller.
- No more than 2 primary font families plus one monospace data face; no more than 5 product sizes or 9 editorial report roles.
- No nested bordered or shadowed cards.
- No unrequested navigation, search, filter, account, or export chrome.
- No boolean-prop explosion: more than three boolean mode props is a design smell.
- No theme parity claim without measured contrast.
- No token rename without a migration path and a consumer audit.
- **Lazy, Not Negligent**: YAGNI removes speculative tokens and components, never states, validation, WCAG 2.2 AA, or 24x24px targets.
- No production UI code in this skill; hand off to the implementation skill.

## Verification Checklist
- [ ] Style Family & Archetype (`dossier`, `zen-garden`, `chronicle`, `sumi-ink`, `shoji-grid`, `aizome-indigo`, `yugen-noir`, `simple-white`, `plotly-white`, `ggplot2-grammar`, `apple-hig`, `material-you`, or `geist-zinc`), layout (`L1`-`L6`), and voice (`V1`-`V4`) are recorded.
- [ ] The composition ID (`palette × layout × voice × density × primary-module`) follows `references/composition-grammar.md`.
- [ ] Palette uses Monochrome + 1 Accent; status colors are reserved for live states.
- [ ] At most 2 primary font families plus one monospace data face are declared within the 5-product or 9-editorial-role budget.
- [ ] Three token tiers exist with at most 20-25 semantic tokens and active callers.
- [ ] Light and dark parity is measured, not assumed.
- [ ] Every component spec has anatomy, variants, states, and acceptance criteria.
- [ ] Responsive rules cover 320px, 1440px, and 200% zoom, and the Static Minimalism Gate passes.
- [ ] Token export uses ISO-dated files under `docs/designs/` and names implementation/audit skills.

## Related Skills
- Use **ux-product-shaper** for the 5-Axis Spec-Design-Driven grill, Surface Mode, and 8-state contract before tokens.
- Use **dashboard-design** when component tokens and specs target operational or analytics monitoring dashboards.
- Use **ui-accessibility** to audit contrast, focus, target size, and reduced motion.
- Use **html-report** to implement the system in a single-file HTML deliverable across the 13 curated presets.
- Use **plotly-dash** to implement the system in a server-backed Dash application.
- Use **deprecation-migration** when retiring tokens or components with active consumers.
- Use **flutter-ui-responsive-a11y** when the design tokens are implemented in Flutter via Material 3 `ThemeExtension`.
