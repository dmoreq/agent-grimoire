---
name: code-index
description: >-
  Local code knowledge index via kg. Answers who-calls, what-calls, impact,
  implementations, test reach, and public-surface questions without grep loops.
  Consultative only: no hooks, daemon, network, or writes outside .kg/.
risk: safe
source: local
date_added: "2026-10-31"
---

# code-index — kg CLI wrapper

Use `kg` for structural navigation; use grep for text.

## Decision table

```bash
kg build                     # once per session after pulling changes
kg callers X                 # who calls X? path:line pointers, cap 50
kg callees X --depth 3       # what does X invoke, N hops?
kg path A B                  # shortest call route between symbols
kg context X                 # definition + direct callers + callees
kg implementers X            # who inherits/implements X? resolved inherits only
kg imports file              # what does this file import (outbound)?
kg tests X                   # which tests reach X? static candidates
kg impact file               # files that call into file; --edges/--depth for deps
kg symbols file|dir --outline  # structure + signatures
kg symbols file --metrics    # cyclomatic/branches/nesting/effective LOC
kg search terms              # bm25 lookup; --kind/--path/--exact
kg complexity --min-cyc 11   # functions over the ceiling
kg api file|dir              # public/exported symbol inventory
kg files --path dir          # indexed file inventory (symbols/bytes/generated)
kg clones / dead --exclude-tests  # duplicate/dead candidates, never proof
kg unresolved [--names]      # resolution gaps; --names gives path:line kind name
kg stats / hotspots / report # totals, pain ranking, architecture
```

## Do NOT use for

- Content search in bodies, strings, comments, config -> grep/rg. `kg search`
  matches identifier, path, and signature tokens; bodies are not indexed.
- Git history/blame -> git. Cross-repo -> the index is per-repo.

## Contract

- Pointers: `path:line`, 1-based, cap 50 (`--limit N`, max 10000).
- Rebuild when `kg: K of N result files changed since build`.
- Exit 2 + candidates = ambiguous name; re-query with `Class.method`.
- Exit 1 = no result or no index; read the reason line, then grep.

## Caveats

- `implementers`, `imports`, `tests`, `api`, `complexity` are static; import/
  inherit coverage is unmeasured, and `tests` misses non-`test_*` Rust
  `#[test]` names and TS `describe`/`it` callbacks.
- `dead`/`clones` are candidates, not proof.
- `stats`/`files`/`hotspots`/`report` are build-time snapshots.

## Rules

1. `kg build` writes only under `.kg/`; avoid `--force` unless needed.
2. If `kg` is missing, use grep; do not install unprompted.

## Related Skills

- Use **codebase-contracts** to keep skill claims in sync with the binary.
- Use **doubt-driven-development** when a pointer looks wrong.
- Use **verify-and-stop** once the pointer answers the question.
