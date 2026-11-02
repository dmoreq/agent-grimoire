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

Use `kg` for call-graph navigation questions. For textual questions use
grep.

## Decision table

```bash
kg build                  # run once per session after pulling changes
kg callers X              # "who calls X?" — path:line pointers, capped at 50 (--limit N)
kg callees X --depth 3    # "what does X invoke, N hops deep?"
kg impact file.py         # "what breaks if this file changes?" — files calling into it
kg symbols file.py        # "what is in this file?" --outline + signatures
kg search terms           # "where is X handled?" — bm25 symbol lookup
kg clones                 # copy-pasted blocks — candidates, never proof
kg dead --limit 10        # "what is unused?" — candidates, never proof
kg unresolved             # "where is resolution incomplete?"
kg stats                  # index totals
kg hotspots --limit 10    # cyclomatic + LOC + churn-90d + fix-density
kg report                 # 4-section architecture report
kg usage                  # journal summary (calls, latency, stale/empty rates)
kg doctor [--invalidate]  # health check; --invalidate deletes the index
kg mcp                    # JSON-RPC stdio server for MCP hosts (no doctor tool)
```

## Do NOT use for

- Content search inside file bodies (strings, comments, config) -> grep/rg;
  `kg search` matches identifier names only.
- Git history, blame, authorship -> git.

## Contract

- Pointers: `path:line [ambiguous]`, 1-based, capped at 50 by default.
- Staleness: kg prints `kg: K of N result files changed since build — run kg build`
  when result files changed after the build; rebuild then (kg never
  rebuilds itself).
- Exit 2 + a candidate list = ambiguous name; re-query with the
  `Class.method` qualname from the list.
- Empty result (exit 1) with "dynamic dispatch possible" -> use grep for
  that symbol; do not retry kg blindly.

## Caveats

- `stats`/`hotspots`/`report` read the build-time file set; files created or
  deleted after `kg build` are invisible until the next build.

## Rules

1. `kg build` writes only under `.kg/`. Never pass `--force` unless a
   rebuild is explicitly needed (re-parses everything).
2. If `kg` is not installed, say so and use grep; do not install unprompted.
3. Read pointed-to lines before claiming a caller relationship; dynamic
   dispatch can still hide callers.

## Related Skills

- Use **codebase-contracts** to keep skill claims in sync with the binary's actual contract.
- Use **doubt-driven-development** when a pointer looks wrong; verify the line before trusting static resolution.
- Use **verify-and-stop** to stop once the pointer answers the navigation question.
