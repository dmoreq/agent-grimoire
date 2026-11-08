---
name: design-system
description: >-
  Build and maintain a 3-tier W3C DTCG design token system, dual light/dark themes,
  Zen Minimalism editorial typography, component specifications, and responsive layout rules.
  Use when bootstrapping a visual identity, creating or updating a design system, or
  handing design to code. Not for UX research, accessibility audits, or feature specs.
risk: safe
source: local
date_added: "2026-10-28"
---

# Design System Skill

Own the visual contract between product intent and implementation: tokens, typography, components, states, responsive rules, and the handoff to code, grounded in **Zen Minimalism** (*Kanso*, *Ma*, *Shibumi*).

## When to Use
- Bootstrapping a visual identity for a new product or surface.
- Creating or updating a token system, theme, or component library.
- Retheming an application for light and dark modes.
- Writing component specs before implementation.
- Auditing hardcoded colors, spacing, or one-off variants.

## When Not to Use
- UX research, information architecture, or the 8-state product contract (`ux-product-shaper`).
- WCAG conformance audit and keyboard testing (`ui-accessibility`).
- Writing production UI code (`html-report`, `plotly-dash`, `python-pro`).
- Adversarial critique of a rendered screen (`ux-critic`).
- Feature scoping without a user interface (`spec-driven-design`).

## Artifact Paths
- Design system spec: `docs/designs/YYYY-MM-DD_design-system_<topic>.md`. Topic slugs follow the artifact slug and containment rule in `rules/AGENTS.md` §4.
- Token export: `docs/designs/YYYY-MM-DD_tokens_<topic>.css` and `.json`.
- Session fallback: the host artifact directory with the same ISO date prefix.
- Never write an undated file at the repository root.

## Workflow

### Step 1: Set the Minimalist Aesthetic & Editorial Typography Direction
1. Read the product brief from `ux-product-shaper`: Surface Mode, audience, and constraints.
2. Choose one register: Swiss/Zen editorial (Mode A) or Shibumi utilitarian (Mode B).
3. **Monochrome + 1 Accent (Warm Organic Neutrals)**: render at least 90% of the viewport from a warm organic surface ramp (such as parchment `#F7F4EE`, raked limestone `#F4F1EA`, or warm paper `#FBF9F5` in light mode; deep espresso `#141210` in dark mode) paired with warm charcoal ink (`#22201E`). Reserve one earthy accent color (muted clay `#9E583B`, Kyoto moss `#4A6B53`, or terracotta `#A65638`) for the primary CTA, chapter index, and active focus ring. Reserve status colors for live system feedback, never decorative badges.
4. Do not default to purple-to-blue gradients, neon glows on B2B surfaces, decorative blobs, glassmorphism, icon tiles above headings, or pure untinted `#000000` and `#808080`.
5. **Typography Caps & Editorial Craft**:
   - Declare at most 2 primary font families per active view (an expressive editorial serif display face such as `'Fraunces'` or `'Cormorant Garamond'` paired with a clean UI sans such as `'Inter'` or `'Plus Jakarta Sans'`) plus one monospace data face (`'JetBrains Mono'`). Never add a third display face.
   - Use at most 5 size tokens for product UI, or the 9 editorial roles in the reference for reports.
   - Always load the real webfont stylesheet (e.g., Google Fonts `<link>`) with graceful system fallbacks so editorial serifs never degrade into flat legacy system fonts when online.
   - Use display weights `300`/`350`/`400`, body `400`, UI `500`, and emphasis `600`; never use `700`. Apply tight letter-spacing (`-0.02em`) and `font-optical-sizing: auto` on display headings, chapter indices, and hero figures.
   - Size hero KPI figures at `2.5x-3x` body. A page-title display may reach `3x+` body; do not use `3x+` for KPI figures.
   - Apply `font-variant-numeric: tabular-nums` and `--font-mono` to numeric columns, deltas, and SVG chart axes. Keep prose paragraphs to 2-3 sentences (`<= 60 words`, `60ch-70ch` measure, target `66ch`).
6. **Ma (Whitespace over boxes)**: treat negative space as an active structural element. Use 3.5-5.25rem macro spacing between sections and 0.5-1rem micro spacing inside groups. Prefer a 1px hairline over nested bordered cards.

### Step 2: Build the Three-Tier Token System
The full token and component templates are in `references/token-and-component-specs.md`.

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
- Do not emit unused tokens or a 10-step color ramp with no callers.
- Every declared token must have an active caller.

### Step 3: Verify Theme Parity
- Body text contrast is at least 4.5:1 in both light and dark themes.
- Large text and active UI boundaries are at least 3.0:1.
- Hover, focus-visible, active, and disabled states keep readable contrast.
- The same semantic role resolves to the same meaning in both themes.
- Export `tokens.css` and `tokens.json` with identical role names.

### Step 4: Write Component Specifications
Every component spec contains:
- Anatomy: named parts and their nesting.
- Variants: semantic names, not boolean explosions. Prefer `variant="danger"` over `isDestructive`, `isCompact`, `hasFooter`.
- Props and slots: required, optional, and forbidden combinations.
- States: default, hover, active, focus-visible, disabled, loading, error, empty where applicable.
- Usage rules: when to use, when not to use, and the nearest alternative.
- Do and do not examples.
- Acceptance criteria: visual, behavioral, and accessibility checks.

**YAGNI implementation handoff**:
- **Native primitives first**: use `dialog`, `details`/`summary`, `input type="date"`, native `select` for 7 or fewer options, CSS Grid/Flex, and `@container` before custom JS or a UI library.
- **Rule of Three**: keep markup inline until the same visual and behavioral pattern repeats at least 3 times. Do not create single-use wrappers or generic config-driven components.
- **Compound components**: compose via children or slots, or explicit semantic variants. More than three boolean mode props is a design smell.

Avoid nested card slop. Do not place bordered cards inside bordered cards; use whitespace, `--bg-subtle`, or hairline dividers.

### Step 5: Define Responsive Layout Rules
- Use CSS Grid with `auto-fit` and `minmax()` for macro layout; Flexbox for local alignment.
- Use container queries for reusable components; page-level media queries alone break narrow sidebars.
- Support 320px to 1440px and 200% browser zoom without horizontal page scroll.
- Keep touch targets at least 24x24px, preferably 44x44px on mobile.
- Use `text-wrap: balance` on headings and `text-wrap: pretty` on body text.
- Wrap motion in `@media (prefers-reduced-motion: no-preference)`.

### Step 6: Hand Off to Implementation
- Hand tokens and specs to `html-report` for a single-file HTML report (`dossier`, `zen-garden`, or `chronicle`), `plotly-dash` for a Dash application, or `python-pro` for a Python-served UI.
- Give the implementer the token files, component acceptance criteria, and the state matrix from `ux-product-shaper`.
- Hand the result to `ui-accessibility` for the WCAG audit and to `ux-critic` for heuristic critique.
- Tell the implementer to follow the YAGNI rung ladder: native primitives first, inline until the Rule of Three, compound components over boolean props, and no unrequested chrome.
- When retiring an old token or component, use `deprecation-migration` to keep consumers working during the transition.

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
- [ ] Aesthetic direction and editorial typography pairing are recorded and justified.
- [ ] Palette uses Monochrome + 1 Accent with warm organic surfaces; status colors are reserved for live states.
- [ ] At most 2 primary font families plus one monospace data face are declared.
- [ ] Size tokens are within the 5-product or 9-editorial-role budget.
- [ ] Three token tiers exist with semantic roles.
- [ ] At most 20-25 semantic tokens; every token has an active caller.
- [ ] Light and dark parity is measured, not assumed.
- [ ] Every component spec has anatomy, variants, states, and acceptance criteria.
- [ ] Responsive rules cover 320px, 1440px, and 200% zoom.
- [ ] The Static Minimalism Gate passes.
- [ ] Token export uses ISO-dated files under `docs/designs/`.
- [ ] Handoff names the implementation skill and the audit skills.

## Related Skills
- Use **ux-product-shaper** for the product brief, Surface Mode, and 8-state contract before tokens.
- Use **dashboard-design** when component tokens and specs target operational or analytics monitoring dashboards.
- Use **ui-accessibility** to audit contrast, focus, target size, and reduced motion.
- Use **html-report** to implement the system in a single-file HTML deliverable (`dossier`, `zen-garden`, or `chronicle`).
- Use **plotly-dash** to implement the system in a server-backed Dash application.
- Use **deprecation-migration** when retiring tokens or components with active consumers.
- Use **flutter-ui-responsive-a11y** when the design tokens are implemented in Flutter via Material 3 `ThemeExtension`.
