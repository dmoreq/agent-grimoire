---
name: code-smells
description: >-
  Detect Fowler code smells across a Python tree and name the remaining smell
  types by hand. Not for correctness review, YAGNI-on-write, or cross-module
  semantic duplication.
risk: safe
source: local
date_added: "2026-11-06"
---

# Code Smells

Name smell types from a closed Fowler catalog and report candidates. Do not fix them here.

- Load `references/fowler-catalog.md` for the 21 types, the signal, and the handoff.

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

Before the scan, write the cleanup targets for the scoped files: `50%` and `75%` of scoped LOC. Scoped LOC is the line count of the files in this scan, not the whole repository. Do not run the script until both targets are written.

### 1. Scan

```bash
python3 skills/code-smells/scripts/smell_scan.py <root> \
  --out-dir .tmp/code-smells
```

Read `smell_summary.md` only. Outputs must stay inside `--out-dir`.

### 2. Manual rows

Fill the manual rows in `references/fowler-catalog.md` for the scanned package. Run `git log` for Divergent Change and Shotgun Surgery only when the user allows history. Without history, mark those two rows "insufficient data".

### 3. Table

One row per confirmed candidate: smell, file, line, handoff skill, and `Reducible LOC: N`. `N` is lines removed minus lines added if the sketched fix landed. Use `Reducible LOC: unknown` when no replacement is sketched. Do not invent `N`. Close with `Reducible LOC total: N`, the sum of the numeric rows. Then write `Cleanup level: P%` where `P` = that total / scoped LOC, plus `50% target: met` or `not met` and `75% target: met` or `not met`. If the total is unknown, write `Cleanup level: unknown` and mark both targets `not met`. Stop. Edit only if the user asked.

## Gotchas

- 13 script rows plus 8 manual rows cover the 21-type catalog. That is type coverage, not instance recall.
- Feature Envy, Temporary Field, and Speculative Generality are heuristics.
- Non-Python files are not scanned. Say so.
- Do not delete code from a smell row.

## Related Skills

- Use **code-simplification** when a confirmed structural smell should be rewritten without a behavior change.
- Use **codebase-minimalism** when the row is Primitive Obsession, Duplicate Code across modules, Dead Code, or Alternative Classes.
- Use **verify-and-stop** after the table is written unless the user asked to edit.

## Final Checklist

- [ ] Script summary read
- [ ] Eight manual rows filled or marked insufficient
- [ ] Each kept row names a handoff and a `Reducible LOC` value
- [ ] Targets `50%` and `75%` were written before the scan
- [ ] The table ends with `Reducible LOC total` and a cleanup level against both targets
- [ ] No edit unless requested
