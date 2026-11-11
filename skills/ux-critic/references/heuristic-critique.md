# Heuristic Critique

Reference for `ux-critic`. It defines the six critique dimensions, the squint test, Nielsen's ten heuristics, the steering vocabulary, severity, and the report template.

## 1. Six Critique Dimensions

### 1.1 Focal Point and Squint Test

Blur the screenshot or step back until text is unreadable. The primary metric, action, or message must remain the dominant shape.

Pass conditions:
- One element wins the first two seconds.
- The focal element matches the product brief's primary task.
- Secondary cards do not share the same weight, border, and color as the primary one.

Failure signals:
- Four identical KPI cards with no dominant metric.
- A decorative illustration heavier than the primary action.
- The eye lands on a logo or navigation before the task.

### 1.2 Spatial Rhythm, *Ma*, and Layout Geometry (`L1`-`L6`)

Pass conditions:
- Macro whitespace between sections is larger than micro whitespace inside a group.
- Left edges align across headings, cards, and table columns (or follow the chosen layout geometry: `L1: sidebar-rail`, `L2: contemplative-column`, `L3: chapter-banner`, `L4: fukinsei-split`, `L5: shoji-bento`, `L6: yugen-canvas`).
- Spacing comes from a 4px or 8px scale, not arbitrary values.
- In `L5: shoji-bento` lattices, `1px` exposed hairlines separate flush cells with zero nested bordered cards inside cells.
- Typography stays within 2 primary families plus one monospace face across the 4 curated voices (`V1`-`V4`).
- Reports use the 9 editorial roles; product UI uses at most 5 size tokens.
- Prose measure stays within 60ch-70ch, target 66ch.

Failure signals:
- Section gaps smaller than card padding.
- Mixed alignment axes across the same column.
- Nested bordered cards inside a `shoji-bento` lattice.
- A third display face or an arbitrary one-off font size.
- A prose column wider than 70ch or narrower than 60ch.

### 1.3 State Honesty

Pass conditions:
- Empty states explain why and offer the next action.
- Loading preserves layout geometry and does not look disabled.
- Errors name the cause and the recovery step.
- Disabled controls explain why they are unavailable.
- Partial data is labeled, not hidden.

Failure signals:
- A skeleton with a different height than the final content.
- A greyed-out screen for loading.
- An empty panel with no CTA.
- A success toast while the list is unchanged.

### 1.4 Microcopy and Clarity

Pass conditions:
- Labels are specific verbs: "Create workspace", not "Submit".
- Errors state what happened and what to do next.
- Helper text appears before the mistake, not after.
- The same concept uses one term throughout.
- Body paragraphs stay at 2-3 sentences (`<= 60 words`) with one job each.
- Display weights stay at 300-400 (or 500 for sans-dominant `V3`/`V4`); UI labels use 500; emphasis uses 600; 700 is absent.
- Body prose is at least 0.9375rem, labels at least 0.75rem, and code at least 0.82rem.
- Numeric columns, deltas, and axes use tabular numerals.
- Chart labels are readable and non-overlapping: percentages use two decimals, counts are abbreviated, and exact values remain in the table.

Failure signals:
- "Something went wrong" with no recovery.
- Two names for the same object.
- A destructive action labeled like a safe one.
- A wall-of-text paragraph, or the same idea repeated across paragraphs.
- A 700-weight display heading, 0.7rem labels, or proportional numeric columns.
- Integer-only percent labels, overlapping chart labels, or a chart that hides exact values from keyboard users.

### 1.5 Mode Fit and Zen Archetype Fidelity

Pass conditions:
- Persuade surfaces (`Mode A`) use expressive hierarchy and narrative.
- Operate surfaces (`Mode B`) use density, familiarity, and calm hierarchy.
- Studio hybrid surfaces (`Mode C`) keep tool chrome recessed (`1px` shoji borders, collapsible *Yugen* drawers) so the primary canvas breathes.
- The visual palette, layout, and voice match the recorded composition and the domain's trust requirements. A legal cross-axis mix passes. A canonical triple outside that palette's best-fit job fails.

Failure signals:
- A brand hero inside an admin console.
- Casual asymmetric wabi-sabi applied to financial or clinical numbers where tabular precision is required.
- Decorative motion in a high-frequency workflow.

### 1.6 YAGNI and Signifier Honesty

Pass conditions:
- Every visible control was requested or is required to complete the task.
- No unrequested navbar, sidebar, search, filter, notification, avatar, settings, dark-mode toggle, pagination, or export control.
- Interactive controls are recognizable without hover discovery: fill contrast, border definition, cursor pointer, and hover/active feedback.
- No decorative icon tiles, vanity metrics, or badge clutter.

Failure signals:
- A search bar or filter bar that the prompt never requested.
- A ghost button that looks like a label.
- A metric card added for visual balance with no decision value.

## 2. Dieter Rams Red-Team

Score the screen against five Rams principles before Nielsen:

| Principle | Question | Failure signal |
| :--- | :--- | :--- |
| #4 Good design is understandable | Is the primary action obvious without a manual? | The user must hover or guess |
| #5 Unobtrusive | Does decoration stay out of the task's way? | A hero illustration or gradient competes with the work |
| #6 Honest | Do states and affordances match reality? | A loading state looks disabled; a success toast with no change |
| #8 Thorough down to the last detail | Are alignment, states, and edge cases complete? | Empty/error states are missing; baselines are misaligned |
| #10 Less, but better | Did we remove before adding? | Extra cards, badges, and subtitles with no task role |

## 3. Squint Test Procedure

1. View the screenshot at 100% on the shipping viewport.
2. Apply a blur of 6-10px, or step back until text is unreadable.
3. Identify the first three shapes that attract attention.
4. Compare that order with the intended hierarchy in the product brief.
5. Record the mismatch as a finding with the screenshot path.

## 4. Nielsen's Ten Heuristics

| Heuristic | Evidence to collect | Failure example |
| :--- | :--- | :--- |
| 1. Visibility of system status | Loading, saving, success, error states | No feedback after a destructive action |
| 2. Match with the real world | Labels and metaphors | Internal jargon in a user-facing label |
| 3. User control and freedom | Cancel, undo, back, escape | A modal with no close path |
| 4. Consistency and standards | Components, terms, navigation | Two button styles for the same action |
| 5. Error prevention | Confirmation, constraints, defaults | Destructive action without confirmation |
| 6. Recognition rather than recall | Visible options, context | A code the user must remember from another screen |
| 7. Flexibility and efficiency | Shortcuts, bulk actions, presets | Every task requires the full wizard |
| 8. Aesthetic and minimalist design | Signal-to-noise ratio | Decorative badges on every row |
| 9. Error recovery | Cause, fix, preserved input | Cleared form after validation failure |
| 10. Help and documentation | Inline help, empty-state guidance | A blank screen with no explanation |

Mark each heuristic `Pass`, `Fail`, or `Not applicable`. A heuristic without evidence is `Not applicable`, not `Pass`.

## 5. Steering Vocabulary

Run subtraction in this order before any polish: `distill`, `quieter`, `clarify`, then `polish`. Use `bolder` or `harden` only after subtraction, when hierarchy or resilience still needs work.

| Command | Use when | Concrete actions |
| :--- | :--- | :--- |
| `distill` | The screen carries redundant elements | Remove duplicate labels, decorative borders, non-actionable badges; merge repeated metadata |
| `bolder` | The focal point is weak | Increase the primary metric to 3x body size; raise contrast on the primary action; remove competing cards |
| `quieter` | The screen is aggressive or noisy | Reduce saturation; replace filled surfaces with subtle backgrounds; increase whitespace |
| `clarify` | Labels or errors are vague | Rewrite the label as a verb and object; state cause and recovery in the error |
| `polish` | The structure is right but craft is uneven | Align baselines and edges; unify radii; normalize spacing; smooth transitions |
| `harden` | The screen fails under real content | Add overflow handling, long-string wrapping, partial-data states, slow-loading behavior |

Use more than one command only when the finding spans multiple dimensions. Name the command in every finding.

## 6. Severity

| Severity | Definition | Ship effect |
| :--- | :--- | :--- |
| Critical | The primary task is unclear, impossible, or dishonest | Do not ship |
| Important | A significant hierarchy, state, or clarity defect with a workaround | Ship with fixes |
| Suggestion | A clear improvement with no task failure | Schedule |
| Nit | Minor polish | Optional |

## 7. Critique Report Template

Save as `docs/reports/YYYY-MM-DD_ux-critique_<topic>.md`.

```markdown
# UX Critique: <Topic>

- Date: YYYY-MM-DD
- Revision: <commit>
- Viewports: <desktop, mobile>
- Locked 5-Axis Matrix: <Mode A/B/C · Archetype · Layout L1-L6 · Voice V1-V4 · Density>
- Evidence: <screenshot paths>
- Product brief: <path>
- Design system: <path>
- Accessibility gate: Pass | Not run

## Verdict

<Two sentences: the main strength and the main weakness.>

## Keep

- <1-2 elements that already exemplify "less, but better">

## The One Deletion

- **THE ONE DELETION**: <single element, wrapper, or control to remove completely>
- Reason: <why this is the highest-leverage deletion>

## Findings

### <Issue Title>

- Severity: Critical | Important | Suggestion | Nit
- Dimension: Focal point and squint test | Spatial rhythm, *Ma*, and layout geometry (`L1`-`L6`) | State honesty | Microcopy, *Kanso* wording, and paragraph rhythm | Mode fit, archetype fidelity, and *Shibumi* restraint | YAGNI and signifier honesty
- Heuristic: <Nielsen number or Not applicable>
- Evidence: <screenshot path and region>
- Finding: <what is wrong>
- Steering: `distill` | `bolder` | `quieter` | `clarify` | `polish` | `harden`
- Fix direction: <concrete change, no code>

## Prioritized Fixes

1. <highest impact fix>
2. <next fix>

## Ship Recommendation

- Verdict: Ship | Ship with fixes | Do not ship
- Blocking findings:
```

## 8. Anti-Patterns

- Critiquing source code instead of a rendered screen.
- Vague feedback such as "make it pop" or "improve the UX".
- Proposing a full redesign for a spacing defect.
- Ignoring the product brief's Surface Mode or recorded composition.
- Failing a legal cross of palette and layout because it is not the canonical triple.
- Treating an accessibility failure as a visual preference.
- Inventing a user metric without evidence.
- Marking an untested heuristic as a pass.
- Polishing before running the subtraction pass.
- Adding visual elements to "balance" a layout instead of removing noise.
- Accepting a minimal design that removes clickability signifiers, focus, labels, or states.

## 9. Anti-Rationalization

| Rationalization | Reality |
| :--- | :--- |
| Add a search bar, filter pills, and notification icon so the page looks complete. | Unrequested chrome is visual noise and maintenance debt. If it was not requested, do not render it. |
| Wrap each metric in a shadowed card with an icon badge. | Nested cards and decorative icons reduce the data-ink ratio. Use whitespace and type hierarchy. |
| Build a reusable component with 10 configuration props for future flexibility. | Premature abstraction violates the Rule of Three. Write concrete inline code until the pattern repeats. |
| Skip empty, error, and focus states to keep the code minimal. | Minimalism removes decoration, never usability scaffolding, state honesty, or accessibility. |
