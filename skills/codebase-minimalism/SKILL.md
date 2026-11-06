---
name: codebase-minimalism
description: >-
  Audit semantic duplication, shadow flags, reinvented utilities, and DTO clones
  across Python, TypeScript, Dart, Go, and Rust using a symbol harvest.
  Not for YAGNI-on-write, local readability refactors, or public API sunsets.
risk: safe
source: local
date_added: "2026-11-06"
---

# Codebase Minimalism

Harvest symbols and cluster semantic duplication across modules and languages. Produce a `Legacy -> Canonical` map. Do not write new code under YAGNI rules here (`code-minimalism` owns that).

- Load `references/semantic-duplication-matrix.md` when classifying alerts.
- Load `references/refactor-blueprint.md` when building the canonical table.

## When to Use

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

Before the harvest, write the cleanup targets for the scoped files: `50%` and `75%` of scoped LOC. Scoped LOC is the line count of the files in this bounded context, not the whole repository. Do not run the extractor until both targets are written.

### 1. Harvest

Avoid sequential file reads. Run the bundled extractor:

```bash
python3 skills/codebase-minimalism/scripts/universal_extractor.py <root> \
  --out-dir .tmp/codebase-minimalism
```

Read `universal_summary.md` only. Add `--full-symbols` when a specific alert needs the symbol dump. Optional `--synonyms map.json` supplies domain aliases. Outputs must stay inside `--out-dir` (default `.tmp/codebase-minimalism/`).

### 2. Cluster

Partition **alerts**, not the full symbol table, into bounded contexts. Confirm each HIGH or MEDIUM alert against the two files named in the row.

### 3. Critique (three lenses, one pass)

Keep the pass in-thread when the cluster is under ~100 lines (`rules/AGENTS.md` §1). Spawn subagents only above that threshold.

1. Canonical type or Enum versus shadow flags and DTO clones.
2. Duplicate helpers versus stdlib or an existing shared module.
3. Accuracy and side effects. Hand off measured latency questions; do not invent numbers.

### 4. Blueprint

Write the lexicon in `references/refactor-blueprint.md`. Add `Reducible LOC: N` on each row. `N` is lines removed minus lines added if that replacement landed. Use `Reducible LOC: unknown` when no replacement is sketched. Do not invent `N`. Close with `Reducible LOC total: N`, the sum of the numeric rows. Then write `Cleanup level: P%` where `P` = that total / scoped LOC, plus `50% target: met` or `not met` and `75% target: met` or `not met`. If the total is unknown, write `Cleanup level: unknown` and mark both targets `not met`. Stop. Implement only if the user asked. Optional saved report: `docs/reports/YYYY-MM-DD_codebase-minimalism-audit_<topic>.md` with a slug matching `^[a-z0-9]+(-[a-z0-9]+)*$`.

## Gotchas

- Greedy DRY: identical lines in different bounded contexts with different reasons to change stay separate.
- Dead-code candidates are Python-only and are not proof a public symbol is unused.
- Non-Python harvest is regex-approximate. Confirm before collapsing.
- Enum replacements must preserve external default values.

## Related Skills

- Use **code-minimalism** when the finding is "do not write this helper" on a new path.
- Use **deprecation-migration** when the canonical replacement is a public or facade symbol.
- Use **python-testing** to lock inputs and outputs before any edit.
- Use **verify-and-stop** after the table is written unless the user asked to implement.

## Final Checklist

- [ ] Extractor ran; summary read; no full-symbol dump unless needed
- [ ] Alerts clustered by domain; each kept alert confirmed in source
- [ ] Targets `50%` and `75%` were written before the harvest
- [ ] `Legacy -> Canonical` table produced for one bounded context, with `Reducible LOC`, a total, and a cleanup level against both targets
- [ ] No edit unless requested; handoffs named when an edit is requested
- [ ] Greedy DRY and public-surface checks applied
