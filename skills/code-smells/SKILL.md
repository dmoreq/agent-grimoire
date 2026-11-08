---
name: code-smells
description: >-
  Find as many code smells as possible and write a refactor plan for the user
  to approve. The plan names each smell and the excess lines that cut could
  delete. Not for editing code or for cross-module LOC harvest.
risk: safe
source: local
date_added: "2026-11-06"
---

# Code Smells

The KPI is smells placed in a refactor plan. Find them. Do not edit code. The user approves the plan before any skill edits.

- Load `references/fowler-catalog.md` for the 21 types, the signal, and who would edit after approval.

## When to Use

- A review suspects structural smells beyond a single complexity number.
- The user asks for a smell scan of a Python package.
- Several smell names might apply and need one table.

## When Not to Use

- Diff correctness, security, or test gaps (`code-review`).
- Nesting or naming cleanup after the smell is already named (`code-simplification`).
- Shadow flags, reinvented helpers, or DTO clones across modules (`codebase-minimalism`).
- Writing new code (`code-minimalism`).

## Workflow

### 1. Scan

```bash
python3 skills/code-smells/scripts/smell_scan.py <root> \
  --out-dir .tmp/code-smells
```

Read `.tmp/code-smells/smell_summary.md` only. Outputs must stay inside `--out-dir`.

### 2. Manual rows

Fill the manual rows in `references/fowler-catalog.md` for the scanned package. Run `git log` for Divergent Change and Shotgun Surgery only when the user allows history. Without history, mark those two rows "insufficient data".

### 3. Plan

Write one row per confirmed smell this skill owns: smell, file, line, benefit, and `cut_loc`. `cut_loc` is lines the later edit would delete minus lines it would add. Do not invent `cut_loc`. Mark `blocked` when the row is a heuristic, dead code, a public signature, a webhook, or a `getattr` target. Hand cross-module copies, Primitive Obsession, Alternative Classes, and Dead Code to `codebase-minimalism` or `deprecation-migration`. Those rows are not in this plan's counts.

### 4. KPI

`Smells found` is confirmed rows this skill owns, excluding `insufficient data` and rows handed off. `Smells in plan` is that set minus `blocked` rows. If `Smells found` is 0, effectiveness is `n/a`.

- Smells found: N
- Smells in plan: N
- Effectiveness: in plan / found

Stop. Do not edit the scanned code.

## Gotchas

- 13 script rows plus 8 manual rows cover the 21-type catalog. That is type coverage, not instance recall.
- Feature Envy, Temporary Field, and Speculative Generality are heuristics.
- Non-Python files are not scanned. Say so.
- A `blocked` row stays in the plan as blocked. It is not a smell in plan.

## Related Skills

- Use **code-simplification** when a confirmed structural smell should be rewritten without a behavior change.
- Use **codebase-minimalism** when the row is Primitive Obsession, Duplicate Code across modules, Dead Code, or Alternative Classes.
- Use **verify-and-stop** after the plan and the smell KPI are written.

## Final Checklist

- [ ] Script summary read
- [ ] Eight manual rows filled or marked insufficient
- [ ] The plan lists benefit and `cut_loc` for each owned smell
- [ ] KPI is smells found and smells in plan only
- [ ] No scanned code was edited
