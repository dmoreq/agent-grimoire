---
name: code-minimalism
description: >-
  Forces the simplest, shortest, most minimal solution (YAGNI). Reaches for
  stdlib before custom code, platform features before dependencies, one line before fifty.
  Use for /minimal, /ponytail, "be lazy", "simplest solution", "zero bloat", "yagni",
  or auditing generalized mechanisms versus ad-hoc copies.
  Not for repo-wide semantic duplication harvest (codebase-minimalism).
risk: safe
source: local
date_added: "2026-09-22"
---

# Code Minimalism Skill

Channels a pragmatic senior engineer: the best code is the code never written. Question whether a speculative abstraction needs to exist, reach for the standard library before custom code, native platform features before dependencies, and one clear line before fifty.

- Load `references/generalization-and-export-audits.md` when auditing a codebase for ad-hoc dialect copies, regex/lexer duplication, or vocabulary/export consolidation.
- Load `references/gitignore-optimization.md` when pruning or auditing `.gitignore` and exclusion rules.

## When to Use
- User asks for the "simplest solution", "minimal code", "be lazy", "zero bloat", or "yagni"
- Explicit slash commands: `/minimal`, `/ponytail [lite|full|ultra]`
- User complains about over-engineering, boilerplate, or unnecessary dependencies
- Refactoring speculative abstractions down to bare essentials
- Auditing generalized mechanisms versus domain heuristics and ad-hoc edge-case rules

## When Not to Use
- Non-coding requests (general prose, translation, stakeholder narratives)
- Broad architectural redesigns requiring multi-system migrations (`deprecation-migration`)
- Repo-wide semantic duplication harvest of shadow flags, DTO clones, or reinvented utilities (`codebase-minimalism`)
- Naming a Fowler smell or measuring function length and branch count (`code-smells`)
- When the user explicitly requests full enterprise scaffolding

## Related Skills
- Use **aw-first** to discover canonical existing helpers and interfaces (`aw search`) before implementing new types or utilities.
- Use **python-pro** to implement the minimal design in typed, tested Python.
- Use **code-simplification** to clean up messy control flow in existing code without changing behavior.
- Use **code-review** to verify that a pull request respects YAGNI and complexity budgets.
- Use **codebase-minimalism** for slim, debloat, reduce LOC, or a repo-wide harvest of shadow flags, DTO clones, or reinvented utilities.
- Use **code-smells** to name a structural smell or measure function length and branch count. Do not restate those thresholds here.
- Use **verify-and-stop** to confirm minimal acceptance criteria and terminate cleanly.

## 1. Concrete Anti-Bloat Heuristics

Follow the Code Generation Ladder defined in `rules/AGENTS.md` §2. In this skill, apply these concrete heuristics to enforce minimalism:

| Pattern | Bloat Anti-Pattern | Minimal Replacement |
| :--- | :--- | :--- |
| **Data modeling** | Abstract base class + 1 concrete class | Single standard class or `@dataclass(slots=True)` |
| **Configuration** | Dynamic JSON/YAML loader for 3 static flags | Module-level constant dict or dataclass |
| **Control flow** | Strategy pattern with registry for 2 branches | Plain `if/else` or match statement |
| **Dependencies** | External package for simple task | Python stdlib (`pathlib`, `itertools`, `functools`) |
| **Validation** | Custom metaclass validator | Standard assertions or schema at trust boundary |

**Equal-size tiebreak**: between two options of equal size, take the one correct on edge cases.

## 2. Generalization & Bloat Audit Principles

When auditing an existing module for bloat, duplicate dialect branches, or export sprawl (see `references/generalization-and-export-audits.md` for the full 10-step protocol):
1. **Verify Live Execution Paths First**: Grep the production entry point before calling a class "the architecture" or "dead". Exported stage classes used only by tests are false generalizations; symbols imported by sibling packages are live contracts even if omitted from `__all__`.
2. **Separate General Mechanisms, Domain Heuristics, and Entity Exceptions**: Do not equate moving hardcoded rules into a JSON file or a generic rules engine with generalization—a rules framework only relocates exceptions without validating their assumptions.
3. **Structural hotspots**: Do not re-measure function length or branch count here. Take those rows from **code-smells**. Follow `rules/AGENTS.md` §3 for the canonical thresholds. This step only counts duplicate regex or keyword decision sites across the package.
4. **Lock Public Outputs Before Collapsing Copies**: Run the production entry point on representative inputs and lock public return fields before merging duplicate branches or deleting shims. Separate copy elimination from control-flow reordering into distinct commits.
5. **Keep Commit Slices Import- and Typecheck-Clean**: Dropping a re-export shim and retargeting its callers must land in the same commit so `pre-commit` / `pyright` never sees a broken intermediate tree.

## 3. Intensity Levels

| Level | Behavior |
| :--- | :--- |
| **lite** | Build what was requested, and note the simpler stdlib/minimal alternative in one sentence. |
| **full** (default) | Enforce the YAGNI ladder. Stdlib and platform native first; shortest working diff and explanation. |
| **ultra** | YAGNI extremist. Deletion before addition; challenge unnecessary abstractions immediately. |

## 4. Trust Boundaries & Ceiling Markers
- **Non-Negotiables**: Never simplify away trust boundaries, security checks, accessibility, or error handling that prevents data loss (`rules/AGENTS.md` §2).
- **Root Cause vs. Local Band-Aid**: Grep every caller of the target function before editing. One guard at the root cause is a smaller, safer diff than patching five callers. If the root fix is blocked, record the blocker and keep the workaround confined to one layer.
- **Ceiling Markers**: When shipping a deliberate simplification with a known scaling threshold (e.g., in-memory dict, global lock, linear scan), document the ceiling inline:
  ```python
  # ponytail: linear scan over <=500 rules; switch to Aho-Corasick trie if rule count exceeds 5,000
  ```

## 5. Anti-Weeds (Altitude Control)
When the artifact is a design or plan rather than code:
- Keep high-level sections at architecture, interfaces, and data flow.
- Flag helper functions, loop variables, and pseudocode that belong in the implementation range.
- Prefer a structural fix in the owning component over a local workaround.
- Give each behavior one home. Duplicating it across layers is a coupling smell, not reuse.
- A proposed abstraction with one caller is a weed. Delete it or name the second caller.

## Final Checklist
- [ ] Stopped at the highest applicable rung of `rules/AGENTS.md` §2 Code Generation Ladder
- [ ] Zero single-implementation interfaces, speculative configs, or unrequested dependencies
- [ ] Public outputs locked before collapsing duplicate branches or exports
- [ ] Deliberate scaling shortcuts annotated with `# ponytail:` ceiling markers
- [ ] New non-trivial logic (branch, loop, parser, money, security, new script) ships with one small test or assert-based self-check
- [ ] Reply ends with one line: what was skipped or not checked, and the risk the user must know
