# HTML Report Review Gate

Reference for `html-report`. The delivery gate is blocking: a gate that was not run is a fail, not a pass.

## 1. Visual Quality Bar

A report is not done when the HTML validates. It is done when the rendered pages pass this bar. Judge rendered output, never source alone.

### Render Matrix

| View | Viewport | Required coverage | Pass condition |
| :--- | :--- | :--- | :--- |
| Desktop | 1440x900 | Chosen preset in light and dark; other presets only for requested variant comparisons | No overlap, clipping, or content wider than the viewport; hierarchy is obvious at a glance |
| Mobile | 390x844 | Chosen preset in light and dark | Single column; no horizontal page scroll; controls remain usable |
| Narrow reflow | 320px wide | Chosen preset | No clipped content and no horizontal page scroll |
| Print/PDF | A4 | Chosen preset | Details expanded, chrome hidden, no clipped text, no break inside cards or tables |

Capture every required view before judging it. Screenshots are review evidence, not report assets: keep the screenshots the record links, and delete only unreferenced captures after the review record is complete.

### Hard Fails

Any one of these blocks delivery:
- Horizontal page scroll at 390px or 320px, or content wider than the viewport.
- Overlapping, clipped, or truncated text, chart labels, legends, or navigation.
- Body contrast below 4.5:1, or large-text and UI-boundary contrast below 3:1, in any theme or state.
- A missing, invisible, or low-contrast focus ring.
- A preset or theme that loses tokens, flashes unstyled content, or leaves unreadable text.
- A broken theme toggle, table filter, chart tooltip, legend dimming, or cross-highlight control.
- Placeholder text, empty charts, dead controls, or a browser console error.
- A network request outside the Google Fonts stylesheet or the approved Chart.js exception.
- A missing or invalid Content-Security-Policy meta, or a CSP directive that permits an unapproved origin.
- A credential-shaped string in the report; report the pattern class only, never the value.
- Print output with clipped content, visible chrome, or collapsed `<details>`.
- More than two non-monospace font families, or more than one decorative accent outside status and chart palettes.
- Nested bordered or shadowed cards, more than one card radius, or KPI cards in one row with visibly unequal heights.

### Craft Minimums

- Squint test: the primary metric or decision is unmistakable within two seconds on desktop and mobile.
- Macro spacing is 3-5.25rem between sections; micro spacing is 0.5-1rem inside groups.
- Body text is at least 0.9375rem, labels at least 0.75rem, monospace at least 0.82rem.
- Numeric columns, KPI values, and timestamps use `tabular-nums` and share a baseline.
- Charts have zero label collisions, hover/focus tooltips, legend dimming, chart/table cross-highlight, and an accessible title, description, or table fallback.
- Long tables scroll inside `.table-wrap`, never the page.
- The chosen preset keeps one information hierarchy; no second preset block or switcher survives.

## 2. Profile Classification

Classify from how the report will be consumed, not from effort or convenience:
- **Internal**: stays in the current session, is not attached to shared work, and will not be printed.
- **Shared**: persisted under `docs/reports/`, attached to a PR, ticket, wiki, or chat, or read by anyone other than the requester.
- **Print**: any print-to-PDF intent, even for an internal report.
- **Executive**: a decision memo, leadership or board audience, or a report that recommends a decision.

The Theme button does not make a report "interactive" for classification; every report carries one. If two profiles fit, choose the stricter one. When uncertain, default to **Shared**.

## 3. Universal Gates

Every profile runs these gates in order:
1. **Structural self-check**: run `python3 <skill-dir>/scripts/check_html_report.py <report>.html`, where `<skill-dir>` is the directory containing this skill. Require exit code 0 and `PASS`; confirm exactly one preset and no switcher. Fix every failure and rerun.
2. **Rendered visual inspection**: render the matrix in section 1. Inspect every image or PDF page. Grep and source reading do not count.
3. **Fix and re-check**: fix every Critical or Important finding, then re-render the affected views. Bound the loop to 2 cycles. If a Critical defect remains after 2 cycles, stop and report it as blocked; do not ship a known-bad page.
4. **Record evidence**: write `docs/reports/YYYY-MM-DD_<topic>_review.md` using the template in section 6. For a session-only report, write the same record to the host artifact directory. Link the accessibility audit, critique, and screenshot paths.

## 4. Profile Gates

- **Internal**: universal gates plus `verify-and-stop`.
- **Shared**: universal gates, then `ui-accessibility`, then `verify-and-stop`. Require a `Pass` verdict with measured contrast, keyboard order, visible focus, `<details>` disclosure, table headers, 24x24px targets, 320px reflow, and print layout. A `Fail`, `Not tested`, or missing verdict blocks delivery.
- **Print**: same as Shared, with the print/PDF layout check explicitly required.
- **Executive**: universal gates, then `ui-accessibility`, then `ux-critic`, then `verify-and-stop`. Require `Ship` or `Ship with fixes` and zero Critical findings. `Do not ship` blocks delivery.

## 5. Blocking Rules

- Do not describe the report as complete, delivered, or ready until every gate for its profile passes. A gate that was not run is a fail, not a pass.
- Missing screenshots, an unrun audit, or a `Not tested` criterion blocks delivery. Report the missing evidence and ask the user for screenshots when no browser automation exists.
- Do not claim "visually verified" from source code, CSS tokens, or a clean grep.
- Do not deliver while a gate is `Fail` or blocked. State the blocker and the exact evidence needed.
- Never publish or upload the file to an external service without explicit confirmation.
- Save the `.html` file, give the path, and return a concise executive summary in chat. Do not dump raw HTML.
- `verify-and-stop` remains the final decisive check: one file, one preset, no request outside the Google Fonts stylesheet or approved Chart.js exception, both themes render, print preview expands details. It does not replace the visual gate.

## 6. Review Record Template

Write the record beside the report, or in the host artifact directory for a session-only report. Delete rows that do not apply to the profile; never delete a gate the profile requires.

```markdown
# Report Review: <topic>

- Report: `docs/reports/YYYY-MM-DD_<topic>.html`
- Profile: Internal | Shared | Print | Executive
- Preset rendered: <dossier | zen-garden | chronicle | sumi-ink | shoji-grid | aizome-indigo | yugen-noir>
- Views rendered: desktop 1440x900, mobile 390x844, 320px reflow, print/PDF
- Themes rendered: light, dark

| Gate | Evidence | Verdict |
| :--- | :--- | :--- |
| Structural self-check | validator output | Pass |
| Visual Quality Bar | screenshot paths | Pass |
| `ui-accessibility` | `docs/reports/YYYY-MM-DD_a11y-audit_<topic>.md` | Pass |
| `ux-critic` | `docs/reports/YYYY-MM-DD_ux-critique_<topic>.md` | Ship |
| `verify-and-stop` | decisive command output | Pass |

## Findings

| Severity | Finding | Fix | Re-check |
| :--- | :--- | :--- | :--- |

Final verdict: Pass | Fail
```
