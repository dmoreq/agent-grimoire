---
name: code-index
description: >-
  Local code knowledge index via the kg CLI. Answers who-calls-this, what-does-this-call,
  and what-is-impacted-by-this-file in one query instead of grep loops. Consultative only:
  no hooks, no daemon, no network, writes confined to .kg/.
risk: safe
source: local
date_added: "2026-10-31"
---

# code-index — kg CLI wrapper

Use `kg` when a navigation question needs call-graph knowledge. Fall back to
grep when the question is textual (string search, comments, config).

## When to use

- "Who calls X?" / "Find every call site of X outside tests" -> `kg callers`
- "What does X invoke, directly or N hops deep?" -> `kg callees --depth N`
- "If this file changes, what must be updated?" -> `kg impact <file>`
- Architecture trace ("which stages run in order?") -> `kg callees <entry> --depth 3`

## Commands

```bash
kg build                       # once per session after pulling changes; ~1-2s on 100k LOC
kg callers Widget.render       # -> path:line pointers, capped at 50 (--limit N)
kg callees parse --depth 3     # transitive call closure
kg impact app.py               # files that call into app.py
kg stats                       # index totals
kg hotspots --limit 10         # pain-ranking: cyclomatic + LOC + churn-90d + fix-density
kg report                      # 4-section architecture report
kg doctor [--invalidate]       # health check; --invalidate deletes the index
```

## Contract

- Pointers: `path:line [ambiguous]`, 1-based, capped at 50 by default.
- Staleness: kg prints `kg: K of N result files changed since build — run kg build`
  when result files changed after the build. Re-run `kg build` when you see it.
  kg never rebuilds on its own.
- Exit 2 + a candidate list on stdout = ambiguous name; re-query with the
  `Class.method` qualname shown in the list.
- Empty result (exit 1) with "dynamic dispatch possible" -> use grep for that
  symbol; do not retry kg blindly.

## Caveats

- `stats`/`hotspots`/`report` read the build-time file set: files created or
  deleted after `kg build` are invisible or skipped until the next build.
  Re-run `kg build` before trusting them on a changed tree.

## Rules

1. `kg build` writes only under `.kg/`. Never pass `--force` unless a rebuild
   is explicitly needed (it re-parses everything).
2. If `kg` is not installed, say so and use grep; do not install it unprompted.
3. Read the pointed-to lines before claiming a caller relationship; kg gives
   static resolution, dynamic dispatch can still hide callers.
