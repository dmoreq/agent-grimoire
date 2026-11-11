---
name: html-report
description: >-
  Build a single-file, offline-first, interactive, print-ready HTML report for
  audits, architecture explainers, comparison matrices, and decision memos using
  13 curated presets across Zen Minimalism, Scientific/Plotly, Platform Native,
  and Modern Monochrome. Not for short answers or server apps.
risk: safe
source: local
date_added: "2026-10-28"
---

# HTML Report Skill

Deliver findings as one offline-capable HTML file. HTML is a presentation format; the analysis and numbers come from the owning skill. Every report ships with one palette from **13 built-in presets** across 4 style families. Layout (`data-layout`) and voice (`data-voice`) are separate axes. Mix rules live in the **design-system** composition grammar.

## When to Use
- The user asks for an HTML report, visual explainer, dashboard page, audit page, or decision memo.
- A report exceeds about 100 lines of Markdown.
- Tables have 4+ rows or 3+ columns and need spatial layout, filtering, or collapsible sections.
- The reader needs browser viewing or print-to-PDF output.

## When Not to Use
- Short conversational answers, quick snippets, or lists under about 100 lines.
- Files that live in version control and are edited by hand: `README.md`, `CHANGELOG.md`, `SKILL.md`, ADRs.
- Agent-to-agent payloads or source briefs intended for model ingestion.
- Server-backed interactive apps with callbacks or routing (`plotly-dash`).
- Chart design, palette selection, or anti-overlap QA (`data-visualization`).
- Editable Markdown reports and Mermaid diagrams (`technical-reporting`).

## Artifact Path
- Persistent report: `docs/reports/YYYY-MM-DD_<topic>.html`. Topic slugs follow the artifact slug and containment rule in `rules/AGENTS.md` §4.
- Session fallback: the host artifact directory, with the same ISO date prefix.
- Emit one file. Inline CSS, JavaScript, SVG, and data. Do not create a sidecar asset folder.
- Keep the file under 1 MB. Aggregate or downsample embedded data.
- Never write an undated file at the repository root.
- Review artifacts (screenshots, audits, record) live in `.tmp/` or `docs/reports/`, never beside the report.

## Preset & Typography Contract (Single Preset Across 13 Curated Archetypes)

Exactly one preset is fixed at generation time via `data-preset` on `<html>`; never expose a runtime preset switcher. `data-preset` is the palette. Set `data-layout` (`L1`–`L6`) and `data-voice` (`V1`–`V4`) from the locked composition. When either attribute is absent, use that palette's canonical triple. Offer 2-3 unranked job-band options, or follow the locked choice from `ux-product-shaper`. Hex, type, and geometry live in `references/html-report-scaffold.md`:

- **Zen Minimalism (7)**: `dossier`, `zen-garden`, `chronicle`, `sumi-ink`, `shoji-grid`, `aizome-indigo`, `yugen-noir`.
- **Scientific & Plotly Grammar (3)**: `simple-white`, `plotly-white`, `ggplot2-grammar`.
- **Platform Native & Modern Monochrome (3)**: `apple-hig`, `material-you`, `geist-zinc`.

Load the Google Fonts stylesheet with `display=swap` and local fallbacks; it is the only default network request. The approved Chart.js exception in Step 2 is the sole additional request. Use a 60ch-70ch measure, body prose `>=0.9375rem`, labels `>=0.75rem`, and code `>=0.82rem`. Token blocks, nine editorial roles, and layout rules live in `references/html-report-scaffold.md`.

## Chart Interaction Contract
- Use native SVG, not a library: hover/focus tooltip, legend dimming, and chart/table cross-highlight.
- Always show data labels: percentages two decimals (`78.52`), counts `k`/`M` (`501k`). Labels `>=12px`, `aria-hidden`, `pointer-events="none"`, never overlapping. Exact values stay in the tooltip and table.
- Chart SVG uses `role="group"`; each mark uses `role="img"`, `tabindex="0"`, `aria-label`; tooltip uses `role="status"` and `visibility`. Respect reduced motion and print.
- The table is the accessible source; see the scaffold pattern.

## Wording & Paragraphing Rules
1. **Essentialist Prose (*Kanso*)**: Strip ornamental adjectives, hype superlatives, and throat-clearing intros. Open every section with a single declarative thesis sentence containing the primary number and direction.
2. **Paragraph Breathing Room (*Ma*)**: Keep paragraphs at 2-3 sentences, <= 60 words (60ch-70ch measure; target 66ch). Never emit dense wall-of-text paragraphs.
3. **Understated Precision (*Shibumi*)**: State exact deltas (`+8.36 pp`, `N = 4,365,797`) in calm, active voice.
4. **Sequential Chapter Rhythm**: Guide the eye through numbered chapters (`01`, `02`, `03`...) where the chapter lead states *why it matters* in <= 25 words before presenting the table or chart.

## Visual Quality Bar (Blocking)

Judge rendered output, never source alone. Render matrix, hard-fail list, craft minimums, and record template: `references/review-gate.md`.

- Render the chosen preset at desktop 1440x900, mobile 390x844, 320px reflow, and print/PDF in light and dark.
- Any overlap, clipping, horizontal scroll, contrast failure, broken control, console error, external request outside the font stylesheet, or unexpanded print detail blocks delivery.
- Missing screenshots block delivery; keep the screenshots the review record links, and delete only unreferenced captures.

## Workflow

### Step 1: Calibrate Scope and Preset
Choose one palette from the 13-preset catalog and the layout and voice from the locked composition. Honor user instructions, then project tokens from **design-system**, then the canonical triple. Ban generic SaaS purple gradients, neon dashboards, rainbow charts, emoji headers, and nested cards; never use pure `#000000` ink on warm paper presets.

### Step 2: Enforce a Self-Contained and Secure Architecture
- Emit `<!DOCTYPE html>` with `meta charset`, `meta viewport`, a restrictive `Content-Security-Policy` meta, the Google Fonts `<link>`, inline `<style>`, and inline `<script>`.
- Never call `fetch()` or a live API. The font stylesheet and the approved Chart.js block are the only network requests; keep local fallbacks. Never load Tailwind.
- Redact credential-shaped strings, HTML-escape interpolated text, and allow the controlled Chart.js exception only when the user explicitly approves, the page shows an offline warning, and the script tag carries a verified SRI hash. When approved, add `https://cdn.jsdelivr.net` to the CSP `script-src`.

### Step 3: Implement Dual-Theme Tokens and Responsive Typography
- Define per-preset tokens on `:root` with `prefers-color-scheme` and manual `data-theme` overrides; keep exactly one `:root[data-preset="..."] { ... }` token block. Preset-scoped layout overrides may remain.
- Use `rem` units. Body prose `>=0.9375rem`, labels `>=0.75rem`, code `>=0.82rem`. Use the nine editorial roles and print rules in `references/html-report-scaffold.md`.

### Step 4: Structure for Scanning and Progressive Disclosure
1. Header: declarative title, one provenance line, and a single `Theme` button. No eyebrow, status pill, preset switcher, expand/collapse, or copy-summary controls.
2. Use numbered section navigation for 4+ sections, a thesis callout, and 3-4 KPI cards. Keep the primary conclusion visible without a click.
3. Tag audit claims as `FACT`, `INFERENCE`, `DECISION`, or `RISK`; cite `file:line` or a source. Wrap wide tables in `.table-wrap`; put secondary detail inside `<details>`.
4. Use `addEventListener`, never inline `onclick`. Apply **design-system** YAGNI: one primary action, no unrequested chrome, whitespace over nested cards.

### Step 5: Guarantee Print and PDF Fidelity
Include the `@media print` block from `references/html-report-scaffold.md` to hide chrome, force white background/black text at 10.5pt, collapse split grids, expand `<details>`, prevent page breaks inside blocks, and set `@page` margins to 16mm by 14mm.

### Step 6: Mandatory Delivery Gate

This review gate is blocking. Do not call the report complete until every profile gate passes; an unrun gate is a fail. Full classification rules, repair loop, and record template: `references/review-gate.md`.

| Report profile | Required gates, in order |
| :--- | :--- |
| Internal | Structural self-check -> rendered visual inspection -> `verify-and-stop` |
| Shared | Structural self-check -> rendered visual inspection -> `ui-accessibility` -> `verify-and-stop` |
| Print | Structural self-check -> rendered visual inspection -> `ui-accessibility` -> `verify-and-stop` |
| Executive | Structural self-check -> rendered visual inspection -> `ui-accessibility` -> `ux-critic` -> `verify-and-stop` |

- **Classify by consumption**: Internal is session-only, unshared, and unprinted; Shared is persisted, attached, or read by others; Print is any print/PDF intent; Executive is a decision or leadership audience. If two profiles fit, choose the stricter one; when uncertain, default to Shared.
- **Structural check**: run `scripts/check_html_report.py` from this skill directory; it must exit 0 with `PASS`.
- **Visual check**: render the chosen preset at desktop 1440x900, mobile 390x844, 320px reflow, and print/PDF in light and dark. Fix Critical and Important findings and re-render; bound the loop to 2 cycles.
- **Shared / Print**: `ui-accessibility` must return `Pass` (with print/PDF layout checked for Print).
- **Executive**: `ux-critic` must return `Ship` or `Ship with fixes` with zero Critical findings.
- **Record**: write `docs/reports/YYYY-MM-DD_<topic>_review.md` and link screenshots and audits. Missing screenshots, an unrun audit, or `Not tested` blocks delivery.
- `verify-and-stop` remains the final decisive check: one file, one preset, no request outside the font stylesheet or approved Chart.js exception, both themes render, print expands details.

## Verification Checklist
- [ ] Single HTML file with inline CSS/JS/SVG/data, Google Fonts `<link>`, and CSP meta (`default-src`, `connect-src`, `object-src`, `base-uri`, `form-action` `'none'`).
- [ ] One preset fixed; no preset switcher; `data-layout` and `data-voice` set when they differ from the canonical triple; minimal header.
- [ ] Profile classified; display weights `300`-`600` with optical sizing; prose obeys the 2-3 sentence, <= 60 word, 60ch-70ch budget.
- [ ] No Tailwind CDN, no `fetch()`, no secrets; light, dark, and print (`details` expanded) work.
- [ ] Desktop, mobile, 320px reflow, and print rendered and inspected; Shared/Print passed `ui-accessibility`; Executive passed `ux-critic`.

## Related Skills
- Use **ux-product-shaper** to run the 5-Axis Spec-Design-Driven grill first.
- Use **design-system** for project tokens, component specs, theme parity, and the minimalism/YAGNI doctrine.
- Use **ui-accessibility** for shared, interactive, or print reports; audit contrast, keyboard, focus, and table semantics.
- Use **ux-critic** for executive or decision reports; critique hierarchy, state honesty, and microcopy.
- Use **technical-reporting** for Markdown reports, ADRs, Mermaid, and `docs/reports/YYYY-MM-DD_*.md` conventions.
- Use **data-visualization** for chart selection, palettes, anti-overlap QA, and SVG export.
- Use **plotly-dash** for server callbacks, routing, `dcc.Store`, or background jobs.
- Use **data-storytelling** for a Hook -> Ask decision narrative.
- Use **verify-and-stop** for the decisive artifact check.
