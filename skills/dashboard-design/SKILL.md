---
name: dashboard-design
description: >-
  Clean, honest dashboard UI for web and native — KPI cards, charts, heatmaps,
  bullet graphs, same-elapsed-time comparisons, ranked breakdowns, date range
  pickers, filters, responsive grids, and screenshot QA.
risk: safe
source: "https://github.com/abdiraimov-otabek/dashboard-design-skill"
date_added: "2026-11-08"
---

# Dashboard Design Skill

Design clean, honest, wordless dashboard interfaces for web and native platforms. A dashboard answers **one question per screen at first glance**, highlights anomalies without visual noise, and places decisive action one click away.

## When to Use
- Designing, building, or refactoring an analytics, revenue, metrics, or operational dashboard.
- Creating KPI summary cards, same-elapsed-time comparison periods, or sparklines.
- Laying out responsive dashboard grids from ultrawide (3440px) to mobile viewports (375px).
- Structuring ranked breakdown lists with inline share bars or classed heatmap grids.
- Performing visual critique or screenshot QA on data-dense monitoring surfaces.

## When Not to Use
- Creating standalone static publication figures or statistical chart exports (`data-visualization`).
- Defining foundational design tokens, typography scales, or component libraries (`design-system`).
- Initial information architecture, user journey research, or product problem contracts (`ux-product-shaper`).
- WCAG 2.2 accessibility conformance audits or focus trap verification (`ui-accessibility`).
- Adversarial UI subtraction or pure heuristic reviews without data-density concerns (`ux-critic`).

## Related Skills
- Use **ux-product-shaper** to frame the primary user question, target audience, Surface Mode, and 8-state contract.
- Use **design-system** to map semantic tokens (`--bg-canvas`, `--bg-surface`, `--intent-danger`), fonts, and theme parity.
- Use **data-visualization** for chart mark selection, Plotly construction, anti-overlap rules, and SVG export.
- Use **ui-accessibility** to audit data mark contrast (>= 3:1), keyboard traversal, and screen-reader summaries.
- Use **ux-critic** to execute the 1-second squint test, identify clutter, and enforce visual hierarchy.
- Use **html-report** when compiling the dashboard into a standalone offline HTML artifact.
- Use **plotly-dash** when implementing the dashboard as an interactive multi-page Python web application.

## Artifact Paths
- Dashboard design spec: `docs/designs/YYYY-MM-DD_dashboard-spec_<topic>.md`.
- Follow the artifact slug and containment rule in `rules/AGENTS.md` §4 (`^[a-z0-9]+(-[a-z0-9]+)*$`).
- Session fallback: the conversation artifact directory with the identical ISO date prefix.

## Core Principles

- **First glance**: The reader extracts primary status in 3 seconds without hover interactions. Design for this first.
- **Monitor sequence**: Overview -> Anomalies needing attention -> Closer look -> Action. Action triggers sit adjacent to anomalies.
- **Quiet**: Calm until an anomaly occurs. Neutral surfaces and one primary entity hue for healthy data; saturated color reserved exclusively for attention.
- **Wordless**: Display labels, tabular figures, units, and 1-2 word baselines ("vs last week"). Place explanations inside tooltips. Zero sentences outside tooltips and empty states.
- **Honest**: Every repeated metric matches exactly. Comparison windows cover identical elapsed times. Tiny sample bases display raw counts instead of distorted percentages.

Detailed perceptual science (Cleveland & McGill encoding ladder, preattentive attributes, scales): [references/perception.md](references/perception.md).

## Build or Redesign Workflow

1. **Define the Primary Question**: Identify the single question the screen answers, the 3-6 primary numbers answering it, the explicit anomaly thresholds, and the immediate action for each anomaly. Seed a fixed fixture covering all anomaly states (see [references/qa.md](references/qa.md)).
2. **Select Visual Forms**: Select marks from the encoding ladder ([references/perception.md](references/perception.md)): position or length for quantities, classed heatmaps for discrete grids, bullet graphs against static targets, sparklines for historical shape.
3. **Establish Layout Hierarchy**: Position global controls (date range, filters, live indicator) at top -> KPI summary strip -> primary anomaly view -> ranked breakdown panels -> detail logs. Maintain above-the-fold visibility at 1440x900 for monitoring views. Prevent empty card holes. See [references/layout.md](references/layout.md).
4. **Bind Semantic Tokens**: Establish light and dark tokens before implementing components ([references/tokens.md](references/tokens.md)).
5. **Implement Components**: Follow patterns in [references/components.md](references/components.md) and implementations in [references/snippets.md](references/snippets.md) (Web / Tailwind / TypeScript) or [references/swiftui.md](references/swiftui.md) (SwiftUI / Swift Charts).
6. **Cover the 8 States**: Verify empty, loading, stale, partial, and overflow states.
7. **Execute QA Protocol**: Verify independent known totals, execute the zero-sentence wordless audit, run the 1-second salience squint test, and capture multi-viewport screenshots ([references/qa.md](references/qa.md)).

## Critique Protocol

Evaluate live screens or screenshots in this sequence:
1. **Verdict**: One direct line ("Functional, lacks anomaly salience").
2. **Effective Elements**: 2-4 concrete strengths.
3. **Ranked Findings**:
   - *Honesty*: Conflicting numbers, misleading sparkline baselines, unrepresentative delta bases.
   - *Salience*: Eye path alignment with primary anomaly.
   - *Hierarchy*: Competing visual weights, cluttered headers.
   - *Wordless Violation*: Explanatory sentences outside tooltips.
   - *Component Smells*: Review against smell table in [references/qa.md](references/qa.md).
4. **Remediation**: Execute targeted single-pass fixes and verify with before/after captures. See [references/case-study-school-dashboard.md](references/case-study-school-dashboard.md).

## Universal Design Rules

- **Entity Color Mapping**: Bind one hue per distinct entity (e.g., blue for traffic, emerald for revenue). Reserve amber/red strictly for threshold breaches. Secondary series and past periods remain neutral gray.
- **Contextual Baselines**: Every headline metric provides explicit comparison ("compared to what?"). An unfinished period displays dashed lines and neutral comparison values.
- **Numeric Precision**: Use tabular figures (`font-variant-numeric: tabular-nums`). Right-align numeric columns. Compact values on axes (1k, 5M). Render `<0.1%` for non-zero micro-shares; display `—` for missing data, never fake 0.
- **Comparison Deltas**: Flip green and red for lower-is-better metrics (churn, latency, cost). Bases under 5 display raw previous count ("was 1" in gray) rather than noisy percentages.
- **Selection State**: Render active selection as a soft tinted fill with a faint inset ring (`rounded-xl bg-accent/[.06] ring-1 ring-inset ring-accent/20`), avoiding heavy underlines or borders.
- **Ranked Breakdown Bars**: Render share proportions as slim 3px rounded tracks along the row bottom edge (`bg-line/70`), avoiding tinted rectangular backdrops behind text.
- **Responsive Scaling**: Expand layout to 4 columns on ultrawide viewports (>= 1800px); preserve multi-column heatmaps and collapse secondary chips on 375px mobile screens.
