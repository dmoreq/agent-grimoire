---
name: ux-product-shaper
description: >-
  Shape product context, information architecture, user flows, Surface Mode,
  Zen Minimalism microcopy/paragraph pacing, and an 8-state completeness contract
  before UI work. Use when starting a UI project, designing a screen or flow, or
  clarifying ambiguous UX requirements. Not for visual styling, token systems,
  implementation, or code review.
risk: safe
source: local
date_added: "2026-10-28"
---

# UX Product Shaper Skill

Turn an approved feature intent into a product brief that UI work can execute. Fix the surface mode, Zen Minimalism information rhythm (*Kanso*, *Ma*, *Shibumi*), and the state model before any visual or code decision.

## When to Use
- Starting a new UI surface, screen, or flow.
- A feature spec exists but the interface behavior is still ambiguous.
- The team needs an information architecture, navigation model, or empty/error state plan.
- A design review keeps finding missing states or an unclear user flow.

## When Not to Use
- Visual styling, typography, or tokens (`design-system`).
- Accessibility audit and WCAG conformance (`ui-accessibility`).
- Implementation in HTML, React, Vue, Svelte, or a Python UI stack (`html-report`, `plotly-dash`, `python-pro`).
- Adversarial critique of rendered UI (`ux-critic`).
- Feature scoping without a user interface (`spec-driven-design`).

## Artifact Path
- Product brief (`PRODUCT.md`): `docs/designs/YYYY-MM-DD_product-brief_<topic>.md`. Topic slugs follow the artifact slug and containment rule in `rules/AGENTS.md` §4.
- Session fallback: the host artifact directory with the same ISO date prefix.
- Never write an undated file at the repository root.

## Workflow

### Step 1: Classify the Surface Mode and Minimalist Register
| Register | Use for | Visual posture |
| :--- | :--- | :--- |
| Mode A: Swiss / Zen Editorial | Marketing, portfolio, executive chronicle, launch, brand campaign | Page-title display at 3x+ body and KPI/hero metrics at 2.5x-3x, intentional asymmetry or contemplative centered flow, at least 40% *Ma* negative space, one focal CTA above the fold |
| Mode B: Shibumi Utilitarian | B2B SaaS, clinical/engineering dossier, admin console, data table, settings | High data-ink ratio, Jakob familiarity, tabular numbers, compact sticky chapter guides, zero decorative banners or theatrical motion |

If a surface mixes both, split it into separate screens. Do not blend a brand hero into a dense operations table.

### Step 2: Enforce YAGNI & Kanso Scope
1. Build only the views, inputs, and controls required by the prompt.
2. Do not add unrequested top navbars, sidebars, search inputs, filter bars, notification bells, avatar menus, settings gears, dark-mode toggles, pagination, or export buttons.
3. Keep one primary CTA per view. Demote secondary actions to text, ghost controls, or progressive disclosure.
4. Cap top-level navigation at 4 numbered items and summary KPIs at 3-4 high-signal biomarker metrics.
5. Record a "What We Are NOT Building" list in the product brief.

### Step 3: Map Information Architecture, Ma Rhythm, and Wording Budget
1. Name the primary decision or task on the screen in a single declarative sentence (`<= 20 words`).
2. Place one focal point per screen. Competing equal-weight cards are a failure.
3. Limit the first view to 3-5 progressive disclosure chunks separated by generous *Ma* whitespace.
4. **Zen Wording & Paragraphing Contract**: cap section lead descriptions at `<= 25 words` and body paragraphs at `2-3 sentences` (`<= 60 words`). Ban filler instructions, marketing superlatives, and passive voice.
5. Trace the primary flow from entry to completion and to recovery.
6. Apply ecosystem familiarity (Jakob): keep navigation and control placement where users expect it.

### Step 4: Lock the 8-State Matrix
Every screen must define all eight states before implementation. The full matrix is in `references/product-and-state-contracts.md`.

| State | Required behavior | Anti-pattern |
| :--- | :--- | :--- |
| Ideal | Real domain data, complete layout | Lorem Ipsum, John Doe, placeholder metrics |
| Empty | Explain why it is empty and offer the primary action | Blank panel with no next step |
| Loading | Preserve geometry with a skeleton or inline spinner | Dim the whole view like a disabled control |
| Partial | Show what exists and what is still pending | Hide the screen until every row arrives |
| Error / Validation | Name the cause and the exact recovery action inline | Red border alone, generic toast |
| Disabled / Read-Only | Explain why unavailable and how to enable it | Silent grey control with no helper text |
| Text Overflow / i18n | Handle 40% longer strings, long URLs, chip wrapping with `+n` | Clip text or force horizontal scroll |
| Keyboard / Screen Reader | Logical tab order, Escape dismissal, focus return, `aria-live` | Mouse-only interaction, focus lost after modal close |

### Step 5: Write the Product Brief
Use the template in the reference. Save the brief with the ISO-dated path. The brief is the `PRODUCT.md` contract for the surface. It must contain:
- Audience and job to be done.
- Surface Mode and the reason for it.
- Primary flow, recovery path, and out-of-scope items.
- The complete 8-state matrix with realistic example data.
- Success metrics and the event or signal that proves each one.

### Step 6: Hand Off
Hand the brief to `design-system` for tokens, component specs, and responsive rules. Do not start visual styling or implementation in this skill.

## Rules
- No Lorem Ipsum, John Doe, or fake numeric placeholders.
- No unrequested navigation, search, filter, account, or export chrome.
- No loading state that is visually indistinguishable from disabled.
- No error signaled by color alone.
- No implementation before Surface Mode and the 8-state matrix are fixed.
- **Lazy, Not Negligent**: YAGNI removes speculative chrome and abstraction, never the 8 states, validation, WCAG 2.2 AA, or 24x24px targets.
- Ask one open-ended question at a time during intake.
- Stop on contradictory requirements under the Contradiction Halt rule in `rules/AGENTS.md` §2.

## Verification Checklist
- [ ] Surface Mode is recorded and justified.
- [ ] A YAGNI exclusions list exists and bans unrequested chrome.
- [ ] Each screen has one named focal point and one primary CTA.
- [ ] Section leads (`<= 25 words`) and paragraphs (`2-3 sentences`) obey *Kanso* and *Ma* wording budgets.
- [ ] The primary flow includes a recovery path.
- [ ] All eight states are defined with realistic data.
- [ ] The brief uses an ISO-dated path under `docs/designs/`.
- [ ] The handoff to `design-system` is explicit.

## Related Skills
- Use **spec-driven-design** for the approved feature spec and Critical User Journeys before shaping.
- Use **dashboard-design** when shaping operational, analytics, or metric monitoring surfaces.
- Use **design-system** to turn the brief into tokens, component specs, and responsive rules.
- Use **ux-critic** to red-team the rendered result after implementation.
