---
name: data-visualization
description: >-
  Build analytical Plotly and Matplotlib/Seaborn charts with form-first selection,
  Zen Minimalism warm organic palettes, colorblind-safe contrast, anti-overlap QA, and SVG export.
  Not for Mermaid/architecture diagrams, Dash apps, or stakeholder narrative.
risk: safe
source: local
date_added: "2026-08-23"
---

# Data Visualization Skill

Create clear, accurate, readable charts with Plotly (default for interactive/HTML/Kaleido SVG) or Matplotlib/Seaborn (when static publication figures are requested). Choose the visual form before the library, enforce **Zen Minimalism** (*Kanso* high data-ink ratio, *Ma* breathing room, and *Shibumi* warm organic palettes), and never deliver overlapping text.

## When to Use
- Analytical charts for reports, notebooks, or exploratory data analysis
- Selecting the right visual form for a distribution, comparison, trend, or relationship
- Exporting vector SVG or high-DPI PNG figures for reports
- Fixing unreadable charts (label collisions, clipped axes, poor color contrast)

## When Not to Use
- Comparisons that are clearer as a compact Markdown table
- Architecture / sequence / state diagrams (`technical-reporting` Mermaid)
- Interactive multi-page web dashboards (`plotly-dash`)
- Computing statistical metrics or running A/B tests (`data-science`)

## Related Skills
- Use **dashboard-design** when embedding charts into multi-metric KPI strips, ranked breakdown lists, or monitoring grids.
- Use **ui-accessibility** to audit chart contrast, legends, and text alternatives for WCAG 2.2.
- Use **data-science** or **polars-duckdb** to compute and validate metrics before plotting.
- Use **html-report** when exported SVG or Plotly figures must be assembled into one offline HTML deliverable. Follow the locked composition.
- Use **plotly-dash** when the figure becomes an interactive application.
- Use **technical-reporting** when embedding exported SVG figures into a saved markdown report.
- Use **data-storytelling** when the chart supports an executive business recommendation.

## 1. Form Before Chart Library (Is It Even a Chart?)
Before writing plotting code, match the data cardinality to the right representation:
- **1 number + delta/trend** -> Use a KPI callout or inline stat, not a 1-bar chart.
- **1 ratio against a capacity limit** -> Use a progress bar or bullet meter, not a 2-slice pie chart.
- **Exact lookup values matter more than shape, or > 7 high-cardinality classes** -> Use a sorted Markdown table with explicit numbers and `%` deltas.
- **> 5 time-series lines on one axis (spaghetti plot)** -> Highlight 1-2 focal series in color against muted stone gray context lines, or split into small multiples (`facet_col` / `facet_row`).

## 2. Chart Selection Matrix

| Analytical Purpose | Preferred Form | Avoid |
| :--- | :--- | :--- |
| **Compare categories** | Horizontal bar (when labels > 8 chars or > 5 categories) / vertical bar | Pie / donut with > 4 slices, 3D bars |
| **Distribution & spread** | Histogram + median/p95 markers, box + strip, raincloud / violin | Mean-only bar chart with error bars hiding multimodal skew |
| **Trend over time** | Line chart (with shaded CI band if noisy) | Bar chart with truncated non-zero y-axis |
| **Relationship / joint** | Scatter (with alpha / hexbin for N > 2,000), residual plot | Dual-axis charts with arbitrary scale ratios |
| **Part-to-whole** | 100% stacked horizontal bar (<= 5 parts) | Stacked area with > 4 volatile series |
| **Model evaluation** | Calibration reliability curve, PR curve, lift/gain chart, confusion matrix | Raw ROC curve alone on heavily imbalanced data |

## 3. Semantic Color, Zen Minimalism & Accessibility Discipline
Every color in a chart must perform exactly one of four jobs:
1. **Highlight / Focal vs. Context (Shared Warm Data Family)**: Focal `--chart-ps` is muted clay `#9E583B` in Dossier and Zen Garden, and terracotta `#A65638` in Chronicle. Secondary `--chart-prod` `#5A5550`, baseline/historical `--chart-old` `#878079`, positive `--chart-pos` `#2B6648`, and negative `--chart-neg` `#992B2B` are shared across presets. Zen Garden keeps moss `#4A6B53` for UI chrome but uses the Dossier chart palette. Every data color must hold >= 3:1 against the page surface.
2. **Categorical (unordered groups, <= 6 classes)**: Use a colorblind-safe qualitative palette (Okabe-Ito: `#0072B2`, `#E69F00`, `#009E73`, `#CC79A7`, `#56B4E9`, `#D55E00` or warm earthy equivalents with verified >= 3:1 contrast). Group tail categories into `"Other"` (`var(--chart-old)`, `#878079`).
3. **Sequential (ordered magnitude, low -> high)**: Use a perceptually uniform ramp (`Viridis`, `Cividis`, or single-hue warm terracotta/sage).
4. **Diverging (deviation around a meaningful zero/baseline)**: Use a symmetric two-hue ramp (`RdBu`, `Coolwarm`, or Crimson-to-Forest) anchored strictly at the neutral reference value (`zmid=0`).
- **Consistency Invariant**: When generating multiple charts in one analysis, bind each category (`"PlaceSearch"`, `"Historical"`, `"Control"`, `"Treatment"`) to the same CSS variable (`var(--chart-ps)`, `var(--chart-prod)`, `var(--chart-old)`, `var(--chart-pos)`, `var(--chart-neg)`) across every figure.

## 4. Plotly Built-In Templates (`simple_white`, `plotly_white`, `ggplot2`) & Anti-Overlap Rules
- Use `plotly.express` (`px`) for concise construction; refine with `fig.update_layout()` and `fig.update_traces()`.
- **Select the Plotly Template Matching the Locked Palette**: `simple-white` uses `simple_white`, `plotly-white` uses `plotly_white`, and `ggplot2-grammar` uses `ggplot2`. Other palettes keep the semantic series in section 3, remapped to that family's published data colors. Do not reuse the dossier clay series on a cool or scientific surface.
  - **`simple_white`** *(Publication / Tufte Spine)*: Pure `#FFFFFF` canvas, zero interior gridlines, crisp axis lines (`showline=True, ticks="outside"`). Best for high data-ink academic figures, executive print memos, and charts with direct data labels.
  - **`plotly_white`** *(Default Clean Analytical)*: Pure `#FFFFFF` canvas with delicate `#EBF0F8` gridlines (`1px`) and zero outer plot box. Best for interactive dashboards and multi-series comparisons where gridlines aid value lookup.
  - **`ggplot2`** *(Wickham / Wilkinson Grammar of Graphics)*: Signature `#EBEBEB` warm-grey plot canvas (`plot_bgcolor="#EBEBEB"`, `paper_bgcolor="#FFFFFF"`) with crisp `#FFFFFF` major and minor gridlines and `#F8766D` / `#00BFC4` / `#619CFF` data marks. Best for statistical distributions, faceted small multiples (`facet_col`), and R/Tidyverse-familiar audiences.
- Always set an explicit `template`, `width`, and `height` (e.g., `width=900, height=520`), and axis automargins:
  ```python
  fig.update_layout(template="plotly_white", width=900, height=520, margin=dict(l=60, r=40, t=70, b=60))
  fig.update_xaxes(automargin=True, title_text="...")
  fig.update_yaxes(automargin=True, title_text="...")
  ```
- **Kanso & Ma Chart Hygiene (Anti-Overlap Protocol)**:
  - Use `font-family: var(--font-mono)`, `font-variant-numeric: tabular-nums`, and at least `0.75rem` for axes, ticks, legends, and direct labels.
  - Direct labels: percentages use two decimals, counts use `k`/`M`, and labels stay `aria-hidden` with `pointer-events="none"`. Widen bar centres to at least `44px` when five-character labels would collide; exact values stay in the table and tooltip.
  - Strip heavy outer chart borders, background fills, and vertical gridlines when direct bar labels are present.
  - Never label every point on dense series; annotate only top-N, extrema, or threshold crossings.
  - Place legends outside the plot canvas (`orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1`) or label lines directly at their right endpoint.
  - Switch to a horizontal bar chart (`orientation="h"`) whenever category labels collide or rotate > 30 degrees.
  - Export static report figures as vector `.svg` via **Kaleido** (`fig.write_image("chart.svg", width=900, height=520)`) and visually inspect the rendered output.

## Visual QA Checklist
- [ ] Visual form matches purpose (table used when exact lookup beats shape)
- [ ] Palette matches data semantics, and every data color holds >= 3:1 against the page surface
- [ ] Chart text uses mono + tabular numerals at >= 0.75rem
- [ ] Category colors stay identical across all figures in the same report
- [ ] Zero overlapping or clipped titles, axis ticks, data labels, or legends
- [ ] Direct labels use two decimals for percentages, abbreviate counts, and leave exact values in the table
- [ ] Units (`%`, `pp`, `USD`, `ms`, `N=...`) explicitly stated in title/subtitle or axis labels
- [ ] Exported `.svg`/`.png` verified at target display dimensions
