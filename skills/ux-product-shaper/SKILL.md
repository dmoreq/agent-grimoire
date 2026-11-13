---
name: ux-product-shaper
description: >-
  Spec-design-driven UI/UX discovery and shaping: run a multi-turn Socratic
  design grill (Gate 1 & Gate 2), lock Surface Mode (A/B/C), Style Family &
  Archetype (13 presets across 4 families), layout geometry, wording pacing,
  and an 8-state completeness contract before UI work. Not for token files or code.
risk: safe
source: local
date_added: "2026-10-28"
---

# UX Product Shaper Skill (Spec-Design-Driven UI/UX)

Turn an ambiguous UI/UX request or feature intent into an owner-approved, Zero-Decision product and design brief (`PRODUCT.md`) before any token file or UI code is written. Enforce **Spec-Design-Driven UI/UX**: active Socratic interrogation across 5 design axes, unranked option presentation under Architecture Ownership (`rules/AGENTS.md` §2), four-lens UI/UX brainstorm stress-testing, essentialist information rhythm, and an 8-state completeness contract.

## When to Use
- Starting a new UI surface, screen, report, dashboard, or interactive flow.
- A spec exists (`spec-driven-design`) or a prompt arrives with open visual, layout, palette, or interaction choices.
- The user wants to be grilled back-and-forth to lock layout, style family, typography, and states before coding.
- A design review keeps finding missing states, aesthetic drift, or unclear flows.

## When Not to Use
- Generating 3-tier W3C DTCG CSS/JSON token files and component specs after the brief is approved (`design-system`).
- WCAG conformance audit and keyboard testing (`ui-accessibility`).
- Implementation in HTML, React, Vue, Svelte, Flutter, or a Python UI stack (`html-report`, `plotly-dash`, `python-pro`, `flutter-ui-responsive-a11y`).
- Adversarial critique of an already rendered screen (`ux-critic`).
- Backend or CLI feature scoping without a user interface (`spec-driven-design`).

## Artifact Path
- Product & UI/UX spec brief (`PRODUCT.md`): `docs/designs/YYYY-MM-DD_product-brief_<topic>.md`. Topic slugs follow the artifact slug and containment rule in `rules/AGENTS.md` §4.
- Session fallback: the host artifact directory with the same ISO date prefix.
- Never write an undated file at the repository root.

## Workflow

### Step 0: Intake & Context Grounding
Read predecessor artifacts in order: explicit design/spec path (`docs/designs/`), existing brand/token files, then interactive chat. Identify which of the 5 Spec-Design-Driven axes are already constrained and which remain open.

### Step 1: Gate 1 — The 5-Axis Spec-Design-Driven Socratic Grill
Do not silently auto-pick a theme or layout when requirements are open. Grill the user with **one focused question per turn** (attaching a 1-sentence hypothesis and confidence `%`), or present an **unranked 3-option comparison table** (with mechanism, trade-off, and failure mode — no `(Recommended)` label, per `rules/AGENTS.md` §2 Architecture Ownership) across any unresolved axis (full 13-archetype catalog in `references/product-and-state-contracts.md`):

| Axis | Decision to Lock | Unranked Options to Grill User On |
| :--- | :--- | :--- |
| **1. Surface Mode** | Primary user posture | **Mode A: Swiss / Zen Editorial** (persuade/narrate, >= 40% *Ma*) · **Mode B: Shibumi Utilitarian** (operate/read, high data-ink, tabular precision) · **Mode C: Shoji / Studio Hybrid** (create/inspect, split canvas + context rail) |
| **2. Style Family & Archetype** | Visual family & palette (13 presets across 4 families) | **Zen (7)**: `dossier`, `zen-garden`, `chronicle`, `sumi-ink`, `shoji-grid`, `aizome-indigo`, `yugen-noir` · **Scientific (3)**: `simple-white`, `plotly-white`, `ggplot2-grammar` · **Platform (2)**: `apple-hig`, `material-you` · **Monochrome (1)**: `geist-zinc` |
| **3. Layout Geometry** | Spatial grid & reading flow (6 layouts) | **`L1: sidebar-rail`** (`240px + 1fr`) · **`L2: contemplative-column`** (`65ch` centered) · **`L3: chapter-banner`** (horizontal headers) · **`L4: fukinsei-split`** (`38%/62%` asymmetric) · **`L5: shoji-bento`** (`1px` exposed lattice) · **`L6: yugen-canvas`** (primary stage + drawer) |
| **4. Typographic Voice** | Font pairing mood (<= 2 primary + 1 mono) | **`V1: editorial-authority`** (`Fraunces`/`Newsreader` + `Inter`) · **`V2: classical-lyrical`** (`Cormorant Garamond`/`Instrument Serif` + `Plus Jakarta Sans`) · **`V3: technical-shibumi`** (`IBM Plex Sans`/`Space Grotesk` + `IBM Plex Mono`) · **`V4: humanist-clarity`** (`DM Sans`/`Inter` + `JetBrains Mono`) |
| **5. Density & Chrome** | Pacing & YAGNI exclusions | **Contemplative** (`5.25rem` pad, zero filter chrome) · **Balanced Editorial** (`3.5rem` pad, inline table search) · **High-Density Operational** (`1.5rem-2rem` pad, keyboard shortcuts, anomaly badges) |

**Grill Rules**:
1. Stop asking when you can predict the owner's reaction to the next three questions.
2. Accept only an explicit confirmation (`yes`, or explicit option selection like `Mode B + plotly-white + L5 + V4`). Silence does not lock Gate 1 unless preset selection is explicitly delegated.
3. When the owner delegates the look, follow the **design-system** composition grammar: job band, a recorded product+band composition, or the stable task-slug index. Record the composition ID and one primary-module sentence. A named axis stays fixed. Do not default to `dossier` + `L1` + `V1`.
4. Halt immediately on contradictory requirements under the Contradiction Halt rule in `rules/AGENTS.md` §2. State the tension and ask the owner to split the surfaces or pick one posture.

### Step 2: Classify Surface Mode & Enforce YAGNI / Kanso Scope
| Register | Use for | Visual posture |
| :--- | :--- | :--- |
| Mode A: Swiss / Zen Editorial | Marketing, portfolio, executive chronicle, launch, architectural essay | Page-title display at 3x+ body and KPI/hero metrics at 2.5x-3x, intentional asymmetry or contemplative centered flow, at least 40% *Ma* negative space, one focal CTA above the fold |
| Mode B: Shibumi Utilitarian | B2B SaaS, clinical/engineering dossier, admin console, data table, settings | High data-ink ratio, Jakob familiarity, tabular numbers, compact sticky chapter guides or hairline grids, zero decorative banners or theatrical motion |
| Mode C: Shoji / Studio Hybrid | Document/code editors, AI workspaces, design canvases, split-pane analytical notebooks | Quiet structural chrome (`1px` exposed borders), calm canvas focus, collapsible context/inspector drawers, keyboard-first command ergonomics |

If a surface mixes incompatible postures, split it into separate screens.

**YAGNI & Kanso Scope**:
1. Build only the views, inputs, and controls required by the prompt and locked in Gate 1.
2. Do not add unrequested top navbars, sidebars, search inputs, filter bars, notification bells, avatar menus, settings gears, dark-mode toggles, pagination, or export buttons.
3. Keep one primary CTA per view. Demote secondary actions to text, ghost controls, or progressive disclosure.
4. Cap top-level navigation at 4 numbered items and summary KPIs at 3-4 high-signal metrics.
5. Record a "What We Are NOT Building" list in the product brief.

### Step 3: Map Information Architecture, Ma Rhythm, and Wording Budget
1. Name the primary decision or task on the screen in a single declarative sentence (`<= 20 words`).
2. Place one focal point per screen. Competing equal-weight cards are a failure.
3. Limit the first view to 3-5 progressive disclosure chunks separated by generous whitespace.
4. **Wording & Paragraphing Contract**: cap section lead descriptions at `<= 25 words` and body paragraphs at `2-3 sentences` (`<= 60 words`). Ban filler instructions, marketing superlatives, and passive voice.
5. Trace the primary flow from entry to completion and to recovery.
6. Apply ecosystem familiarity (Jakob): keep navigation and control placement where users expect it.

### Step 4: Four-Lens UI/UX Brainstorm Check & 8-State Matrix Lock
Challenge the locked design against the four UI/UX Goldfish lenses in `references/product-and-state-contracts.md` (`Kanso/YAGNI`, `Cognitive Load & Ma Rhythm`, `State & Edge-Case Honesty`, `Aesthetic-Domain Fit`). Define all eight states there: required behavior and anti-pattern for each.

### Step 5: Write the Zero-Decision Product & UI/UX Brief (Gate 2)
Use the template in `references/product-and-state-contracts.md`. Save the brief to `docs/designs/YYYY-MM-DD_product-brief_<topic>.md`. It must contain:
- Audience, job to be done, and primary 1-sentence screen thesis.
- Locked 5-Axis Spec-Design-Driven Matrix (Surface Mode, Style Family & Archetype ID, Layout Architecture ID, Typographic Voice ID, Density tier).
- Composition ID (`palette × layout × voice × density × primary-module`) and one creative sentence for the primary module.
- Primary flow, recovery path, and out-of-scope items ("What We Are NOT Building").
- The complete 8-state matrix with realistic example data.
- Success metrics and the event or signal that proves each one.

### Step 6: Hand Off
Hand the brief to `design-system` for tokens, component specs, and responsive rules, or to `html-report` / `dashboard-design` when using a built-in preset. Do not start visual styling or implementation in this skill.

## Rules
- Never silently guess an aesthetic archetype, layout architecture, or surface mode when the prompt leaves them open; run the Gate 1 Socratic grill first.
- Present multi-path design choices as unranked options (up to 3 per axis, no `(Recommended)` tag).
- No Lorem Ipsum, John Doe, or fake numeric placeholders.
- No unrequested navigation, search, filter, account, or export chrome.
- No loading state that is visually indistinguishable from disabled.
- No error signaled by color alone.
- No implementation before the 5-Axis Design Matrix and the 8-state matrix are fixed.
- **Lazy, Not Negligent**: YAGNI removes speculative chrome and abstraction, never the 8 states, validation, WCAG 2.2 AA, or 24x24px targets.
- Ask one open-ended question at a time during intake.
- Stop on contradictory requirements under the Contradiction Halt rule in `rules/AGENTS.md` §2.

## Verification Checklist
- [ ] Gate 1 resolved all 5 design axes by owner confirmation, or by the delegated composition rule.
- [ ] Surface Mode (`Mode A`, `Mode B`, or `Mode C`) is recorded and justified.
- [ ] The composition ID is recorded. A delegated look uses the job band, not the canonical triple, unless that job is the palette's best fit.
- [ ] A YAGNI exclusions list exists and bans unrequested chrome.
- [ ] Each screen has one named focal point and one primary CTA.
- [ ] Section leads (`<= 25 words`) and paragraphs (`2-3 sentences`, `<= 60 words`) obey *Kanso* and *Ma* wording budgets.
- [ ] The primary flow includes a recovery path.
- [ ] All eight states are defined with realistic data.
- [ ] The brief uses an ISO-dated path under `docs/designs/`.
- [ ] The handoff to `design-system` is explicit.

## Related Skills
- Use **spec-driven-design** for the approved feature spec and Critical User Journeys before shaping.
- Use **dashboard-design** when shaping operational, analytics, or metric monitoring surfaces.
- Use **design-system** to turn the brief into tokens, component specs, and responsive rules.
- Use **html-report** when the shaped deliverable is a single-file HTML report across the 13 curated presets.
- Use **ux-critic** to red-team the rendered result after implementation.
