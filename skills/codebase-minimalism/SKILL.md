---
name: codebase-minimalism
description: >-
  Write an excess-LOC refactor plan for duplicate concepts, shadow flags, DTO
  clones, or reinvented helpers. Trigger on slim, debloat, reduce LOC, cut
  excess lines, or review a codebase for duplicate or excess code.
  Not for a bug-only diff review, a smell-only scan, editing code,
  YAGNI-on-write, or public API sunsets.
risk: safe
source: local
date_added: "2026-11-06"
---

# Codebase Minimalism

The KPI is excess LOC placed in a refactor plan. Find duplicate concepts across modules. Do not edit code. The user approves the plan before any skill edits. Do not write new code under YAGNI rules here (`code-minimalism` owns that). A new shared symbol is allowed in the plan only when it replaces deleted copies.

- Load `references/semantic-duplication-matrix.md` when classifying alerts.
- Load `references/refactor-blueprint.md` when building the canonical table.

## When to Use

- The user says slim, debloat, reduce LOC, cut excess lines, or review the codebase for duplicate or excess code.
- The scope is the tree or more than one module, not a single bug diff.
- Reinvented helpers, validators, or formatters appear in more than one directory or language.
- Shadow boolean flags or string categories duplicate an Enum or typed state.
- DTOs and models proliferate (`UserData`, `UserProfile`, `UserDTO`) with overlapping fields.
- Business logic issues raw HTTP while a project client or SDK exists.

## When Not to Use

- Writing the smallest new implementation (`code-minimalism`).
- Local nesting, naming, or accidental complexity in working code (`code-simplification`).
- Sunsetting a published API, shim, or facade (`deprecation-migration`).
- Directory README or spec drift (`codebase-contracts`).
- A single-diff review with no cross-module harvest (`code-review`).

## Workflow

### 1. Harvest

Avoid sequential file reads. Run the bundled extractor:

```bash
python3 skills/codebase-minimalism/scripts/universal_extractor.py <root> \
  --out-dir .tmp/codebase-minimalism
```

Read `.tmp/codebase-minimalism/universal_summary.md` only. Add `--full-symbols` when a specific alert needs the symbol dump. Optional `--synonyms map.json` supplies domain aliases. Outputs must stay inside `--out-dir`.

### 2. Cluster

Partition **alerts**, not the full symbol table, into bounded contexts. Confirm each HIGH or MEDIUM alert against the two files named in the row.

### 3. Critique (three lenses, one pass)

Keep the pass in-thread when the cluster is under ~100 lines (`rules/AGENTS.md` §1). Spawn subagents only above that threshold.

1. Canonical type or Enum versus shadow flags and DTO clones.
2. Duplicate helpers versus stdlib or an existing shared module.
3. Accuracy and side effects. Unmeasured latency goes to `python-performance`. Do not invent numbers.

### 4. Blueprint

Write the lexicon in `references/refactor-blueprint.md`. Each proposed row has a benefit and `cut_loc`: lines the later edit would delete minus lines it would add. Do not invent `cut_loc`. Mark `blocked` for a public signature, an unproven dead-code candidate, a webhook, or a `getattr` target, and send those to `deprecation-migration`. Blocked rows are not in the KPI.

### 5. KPI

`Excess LOC found` is the sum of `cut_loc` on proposed rows only. This skill does not report a smell count. If there is no proposed row, effectiveness is `n/a`.

- Excess LOC found: N

Stop. Do not edit the scanned code. Optional saved report: `docs/reports/YYYY-MM-DD_codebase-minimalism-audit_<topic>.md` with a slug matching `^[a-z0-9]+(-[a-z0-9]+)*$`.

## Gotchas

- Greedy DRY: identical lines in different bounded contexts with different reasons to change stay separate.
- Dead-code candidates are Python-only and are not proof a public symbol is unused.
- Non-Python harvest is regex-approximate. Confirm before collapsing.
- Enum replacements must preserve external default values.

## Related Skills

- Use **aw-first** for fast static index queries (`aw reuse`, `aw impact`, `aw callers`) to detect semantic duplication, client bypasses, and 1-caller wrappers.
- Use **code-minimalism** when the finding is "do not write this helper" on a new path.
- Use **deprecation-migration** when the canonical replacement is a public or facade symbol.
- Use **python-testing** to lock inputs and outputs before any edit.
- Use **verify-and-stop** after the plan and the LOC KPI are written.

## Final Checklist

- [ ] Extractor ran; summary read; no full-symbol dump unless needed
- [ ] Alerts clustered by domain; each kept alert confirmed in source
- [ ] The plan lists benefit and `cut_loc` for each proposed row
- [ ] KPI is excess LOC found only
- [ ] No scanned code was edited
- [ ] Greedy DRY and public-surface checks applied
