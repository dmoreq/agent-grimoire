# Composition Grammar

Reference for `design-system`. Palette, layout, voice, and density are separate axes. This file owns the mix rules. Token values stay in `token-and-component-specs.md`. Domain fit stays in the **ux-product-shaper** archetype catalog.

## 1. Record

Write one composition ID:

`palette × layout × voice × density × primary-module`

Example: `aizome-indigo × L4 × V4 × high-density × chart`.

`data-preset` is the palette ID (one of the 13). `data-layout` is `L1`–`L6`. `data-voice` is `V1`–`V4`. When `data-layout` or `data-voice` is absent, use that palette's canonical triple. New work sets both attributes whenever they differ from the canonical triple.

Primary module is one of `thesis`, `table`, `chart`, `canvas`, `form`.

## 2. Closed Rules (about 70%)

These slots are not creative:

- Palette, voice, layout, and spacing come from the published catalogs. No 14th hue, no 5th voice, no font weight `700`.
- At most 2 primary families plus 1 monospace face, taken from the chosen voice.
- Monochrome surface plus 1 accent. Status colors stay status colors.
- Body text >= 4.5:1. Large text and UI boundaries >= 3:1. Measure both themes.
- No nested bordered cards, neon, purple-blue hero gradients, emoji icons, or unrequested chrome.
- Surface mode matches the job. Split incompatible postures into two screens.
- One focal point, one primary CTA, the 8 states, and WCAG 2.2 AA targets.
- Chart colors stay semantic. Do not place the dossier clay series on `aizome-indigo`, `plotly-white`, `ggplot2-grammar`, or `geist-zinc`.
- Family grammar holds: `L5` cells stay flush hairlines; `simple-white` keeps Tufte spines; `apple-hig` squircles do not sit inside an `L5` lattice; `material-you` stays shadowless; `V2` italics do not set a dense numeric table.
- Radius stays on the shared scale, except the published family radii: `apple-hig` 16px squircles, `material-you` 24px cards and pill indicators.

Density defaults from the surface mode. The owner may lock the other value in the pair.

| Surface mode | Density |
| :--- | :--- |
| Mode A | Contemplative. Balanced only when the owner locks it. |
| Mode B | High-density. Balanced only when the owner locks it. |
| Mode C | Balanced. High-density only when the owner locks it. |

## 3. Open Choices (at most 4)

When the owner did not lock the axis:

1. Which legal palette in the job band.
2. Which legal layout in the job band.
3. Which legal voice in the job band.
4. Which primary module, justified in one sentence from the screen's primary question.

A fifth invention (new color, extra chrome, extra font) fails review.

## 4. Job Bands

Rows are ordered. Index 0 is the first row. The canonical triple is legal on that palette's best-fit job. It is one row here, not the only row.

| Job band ID | Legal compositions |
| :--- | :--- |
| `editorial-brief` | `dossier×L1×V1`, `sumi-ink×L4×V1`, `chronicle×L3×V2` |
| `long-form` | `zen-garden×L2×V2`, `sumi-ink×L2×V1`, `chronicle×L3×V2` |
| `ops-monitor` | `shoji-grid×L5×V3`, `geist-zinc×L5×V4`, `aizome-indigo×L1×V3` |
| `quant-surface` | `plotly-white×L1×V4`, `simple-white×L2×V4`, `ggplot2-grammar×L5×V3`, `aizome-indigo×L4×V3` |
| `studio-night` | `yugen-noir×L6×V2`, `sumi-ink×L6×V1`, `geist-zinc×L6×V4` |
| `native-consumer` | `apple-hig×L1×V4`, `material-you×L6×V4` |
| `developer-console` | `geist-zinc×L5×V3`, `shoji-grid×L1×V3`, `aizome-indigo×L5×V3` |

## 5. Selection

1. An axis the owner names is fixed. Silence does not delegate. "You pick" or an equivalent phrase does.
2. When the owner is present and axes are open, grill with Gate 1. Offer up to 3 unranked rows from the job band. Do not offer three skins of `dossier`.
3. When the owner delegates, classify one job band. Reuse a composition already recorded for the same product and the same job band.
4. Otherwise take the stable index of the task slug:

`int(SHA-256(task-slug).hexdigest()[:8], 16) % band_size`

Encode the slug as UTF-8. The slug matches `^[a-z0-9]+(-[a-z0-9]+)*$`. The same slug returns the same row.

Worked checks: `close-brief` in `editorial-brief` (size 3) is index 2, `chronicle×L3×V2`. `latency-wall` in `ops-monitor` (size 3) is index 0, `shoji-grid×L5×V3`.

5. If a locked axis leaves no row in the band, stop under Contradiction Halt. Ask the owner to change the axis or the band.
6. If the chosen row shares fewer than 2 differences among palette, layout, and voice with another band's composition in the same product, advance to the next row. Wrap once. If every row collides, keep the row and change the primary module.
7. Write one sentence for the primary module. Same product and same job band reuse the recorded composition. Variety is across job bands.

## 6. Illegal Mixes

Fail the composition when any line is true:

- `L2` with high-density.
- `L5` with squircle cards or nested cards.
- `V2` as the face of a dense numeric table.
- Two accents, or an accent used as a status color.
- A drop shadow on a `material-you` surface.
- A warm decorative gradient on `geist-zinc`.
- A palette, layout, or voice ID outside the catalogs.
- Pure `#000000` ink on a warm-paper palette. `apple-hig` dark canvas may keep its published `#000000`.
