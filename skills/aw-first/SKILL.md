---
name: aw-first
description: >-
  Routing policy for code agents with the aw code index available. Query aw
  (CLI or MCP agent-weave) first for callers, callees, impact, call paths,
  symbol surroundings, imports, helper search, duplicate detection, and memory.
risk: safe
source: "external: /Users/quy.doan/Workspace/kg"
date_added: "2026-11-08"
---

# aw-first Routing Policy

`aw` indexes supported source files' symbols and static relationships into `.aw/index.db`. Results describe the indexed, resolved subset rather than every dynamic runtime relationship. Query `aw` (CLI or MCP `agent-weave`) before reading entire files or running broad codebase greps.

## When to Use
- Locating callers, callees, or transitive reverse call closures for a symbol.
- Tracing shortest static call paths between two functions or methods.
- Inspecting a symbol's definition range, signature, and surroundings (`aw context`).
- Mapping blast radius and dependency impacts of a changed file (`aw impact`).
- Discovering existing canonical helpers before writing new code (`aw search`).
- Detecting duplicate functions, client bypasses, and 1-caller wrappers (`aw reuse`).
- Querying durable project memories, architectural decisions, and developer preferences (`aw mem query`).

## When Not to Use
- Pure semantic questions without known identifiers or syntax terms (use grep/source reads).
- Resolving dynamic runtime dispatch, untyped monkey-patching, or external untyped libraries.
- Investigating code located outside the current indexed workspace repository.
- Replacing required source line reads when establishing behavioral correctness or safety.

## Related Skills
- Use **code-minimalism** to search canonical existing helpers (`aw search`) before creating new types.
- Use **codebase-minimalism** to detect semantic duplicates, callee footprints, and 1-caller wrappers (`aw reuse`).
- Use **code-review** to audit blast radius and reverse call closures (`aw callers`, `aw impact`).
- Use **algorithm-optimization** to trace execution paths and call hierarchies (`aw path`, `aw callers`).
- Use **python-performance** to inspect callers and surroundings around profiled hotspots (`aw context`).
- Use **python-pro** or **rust-pro** to implement verified modifications after navigation.
- Use **verify-and-stop** to verify criteria on pointed source lines and terminate cleanly.

## Binding Routing

For these questions, **query aw first** before running general grep searches or dumping full source files. Read pointed source lines before making behavioral claims or edits; the index points to lines but does not replace source evidence.

| Question / Intent | Command / Tool | Purpose & Usage |
|---|---|---|
| Index currency | `aw build` | Rebuild after source edits before trusting pointers (~0.02s incremental rebuild). |
| Who calls this symbol | `aw callers <name>` | Pointer list `path:line qualname`; add `--depth N` for transitive reverse call closure. |
| What does this call (transitive) | `aw callees <name> --depth N` | Outgoing call closure over resolved static edges. |
| Does A reach B, via which call sites | `aw path <from> <to>` | Shortest route over resolved call edges. Swap arguments for reverse query. |
| Symbol surroundings | `aw context <name>` | Definition range + signature + direct callers + direct callees in one call. |
| Which files depend on a file | `aw impact <file>` | Files that call into target; add `--edges calls,imports,inherits --depth N`. |
| What does this file import | `aw imports <file>` | Outbound resolved imports for an indexed file. |
| Discover canonical helper (Pre-Write) | `aw search '<terms>'` | Concise Interface Cards (`path:line kind qualname signature [callers=N]`). Prioritize high caller counts. |
| Detect duplicate functions (Post-Edit) | `aw reuse [paths...]` | Four calibrated detectors: callee footprint, interface similarity, client bypass, 1-caller wrappers. |
| Session handoff & developer preferences | `aw mem query [terms]` | Retrieve prior decisions, handoffs, and developer preferences from `.aw/memory.db`. |
| Session & global telemetry | `aw usage [--global] [--quality]` | Review query counts, p50/p95 latency, error rates, and token savings. |

Avoid repeating a complete lookup with grep when a current, unambiguous `aw` result already answers it. Use source reads or targeted grep for focused verification, missing relationships, or conflicting evidence.

## Trust Contract

Treat resolved navigation rows as candidates. Static resolution can produce both false positives and missing relationships.
Verify with source reads or grep when:
- The output is explicitly marked as candidates only (`aw reuse`, `aw unresolved`).
- The result is capped (`showing N of M`), stale, ambiguous, or empty.
- The question asks for a behavioral field the static index does not carry.
- You require behavioral, safety, or review evidence.
- A row conflicts with the current source file on disk.

Commands returning resolved navigation rows: `callers`, `callees`, `context`, `imports`, `impact`, `path`, `symbols`, `search`.
Commands whose output is candidates: `reuse`, `unresolved`, `mem query`, `mem get`.

## Secondary & Maintenance Tools

- `aw symbols <file> [--outline]`: Deterministic definition inventory and signatures of one indexed file.
- `aw symbols <dir> --outline`: Definition inventory across a directory prefix.
- `aw unresolved`: Summaries of unindexed or ambiguous resolution sites (`aw unresolved --names`).
- `aw stats [--path <dir>]`: Build-time index summary.

## Project Memory Operations

`aw` persists agent-authored notes in `.aw/memory.db` (local) and developer preferences in `~/.aw/memory.db` (global):
- **Write**: `aw mem write <key> --body <prose> --kind decision|gotcha|fact|task [--tags ...] [--refs ...] [--global]`. Record settled decisions, gotchas, or task summaries.
- **Query**: `aw mem query <terms>`. Queries seamlessly search both local and global stores; local notes take precedence.
- **Maintain**: Rewrite under the same key to update revisions; use `--supersedes <key>` for cross-key replacement; use `--scope session` for transient scratch.

## Contract Behaviors & Staleness Discipline

1. **Exit 2 (Ambiguous Name)**: A bare name matched multiple symbols. Re-query with the fully qualified name (`Class.method` or `module.function`).
2. **Result Caps**: When `showing N of M` appears (N < M), re-run with `--limit <M>` (max 10000) or narrow file filters.
3. **Staleness Check**: After editing code, run `aw build` before further navigation queries. If `aw: K of N result files changed since build` appears, rebuild immediately.

## Context Hygiene

- Pointers lead with `path:line`; open only the targeted line range via editor tools, never dumping whole files into context.
- `aw symbols <file> --outline` replaces reading whole source files when you only need definition inventories and signatures.

## Fallback When aw is Unavailable

When neither `aw` CLI nor MCP `agent-weave` is available in the environment:
- **Callers & References**: Run targeted regex searches (`rg -n --column "\b<symbol>\b"` or `git grep -n "\b<symbol>\b"`) constrained to relevant directories and file extensions.
- **Bounded Line Reads**: Read only target line intervals (`read_file` with `StartLine`/`EndLine` or `sed -n 'L1,L2p'`). Never dump unbounded source files into context.
- **Surroundings & Signatures**: Use compiler diagnostics, language servers, or focused grep for signatures rather than loading full modules.
- **Dependency Impact**: Inspect top-of-file `import` / `use` statements and module manifests directly instead of crawling arbitrary directories.
