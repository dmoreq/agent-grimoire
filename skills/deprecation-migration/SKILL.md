---
name: deprecation-migration
description: >-
  Safely sunset or replace legacy APIs, modules, and systems (strangler, adapter, namespace shims) without breaking consumers.
  Not for local dead-code cleanup or readability-only refactors.
risk: safe
source: local
date_added: "2026-08-23"
---

# Deprecation & Migration Skill

Plan and execute safe replacement, consolidation, or removal of legacy APIs, modules, and data artifacts without breaking downstream consumers.

- Load `references/dead-code-and-untracking-audits.md` when proving whether legacy symbols, `**kwargs` shims, duplicate data stores, or git-tracked directories are safe to remove.
- Load `references/ignore-rule-audit.md` when auditing `.gitignore`, `.dockerignore`, or `MANIFEST.in` exclusion rules.

## When to Use
- Replacing an old API, library, service, or pipeline stage
- Consolidating duplicate implementations across modules or packages
- Sunsetting legacy features or shrinking a package's top-level public exports
- Auditing whether "unused" symbols, shims, or data artifacts have hidden consumers

## When Not to Use
- Trivial local dead-code cleanup inside a single private function (`code-simplification`)
- Pure readability refactoring with no contract or import change (`code-simplification`)
- Initial greenfield architecture selection (`python-patterns`)

## Related Skills
- Use **design-system** when retiring tokens or components that still have consumers.
- Use **tech-research** when surveying replacement libraries or architectures.
- Use **doubt-driven-development** to stress-test high-risk cutover plans.
- Use **codebase-contracts** to record the legacy contract and the replacement contract.
- Use **python-testing** to lock parity and compatibility before deleting legacy paths.
- Use **verify-and-stop** to group import-consistent commits and verify clean-archive builds.
- Use **dart-modern-idioms** when migrating legacy Dart 2 patterns to Dart 3.x sealed classes, switch expressions, or class modifiers.

## 1. Decision Checklist
1. Does the legacy path still perform unique work that the replacement cannot express?
2. Who depends on it (internal callers, `__all__` facades, sibling repos, external API/UI consumers)?
3. Is the replacement proven equivalent on frozen production inputs?
4. What is the incremental migration path (Adapter, Namespace Shim, Strangler, or Feature Flag)?
5. Is the deprecation compulsory (break at a named version) or advisory (warning only)?
6. Is this zombie code: reachable, unowned, and kept only because removal feels risky? Name an owner or schedule removal.

## 2. Core Equivalence & Migration Rules

1. **Prove Equivalence in Tests Before Deleting**:
   - Never delete old code first and rewrite tests afterward—green-after-deletion cannot distinguish equivalence from weakened assertions.
   - Point consumer tests at the replacement while the old symbol still exists, verify parity (`old is not new` to prevent self-comparison), and only then delete the legacy implementation.
2. **Test Whether the Replacement Covers the Input Domain**:
   - Before claiming "the new schema/stage already handles this", test an input the new representation cannot express (e.g., merging two independent root records vs. attaching children to one root). If the old step is the only implementer of that invariant, rename/document it rather than deleting it.
3. **Separate Duplicate Consolidation from Control-Flow Reordering**:
   - Collapse duplicate decision sites onto a shared function first while preserving exact caller flags and stage order. Move any execution-order change to a separate, independently benchmarked commit.
4. **Use Python Namespace Shims (`__getattr__`) When Shrinking Top-Level Exports**:
   - Removing a symbol from `pkg/__init__.py` while keeping it in `pkg/submodule.py` is a facade deprecation, not a full deletion. Keep removed top-level names importable via module-level `__getattr__` that emits `DeprecationWarning` and forwards to the owning submodule until the major version bump.
5. **Audit Hidden Consumers & Silent Compatibility Traps**:
   - Grep across the entire repository and sibling checkouts (including accessor patterns like `for_x`, `<x>_pipeline`, and registry tables) before declaring a symbol dead.
   - Check constructors for pass-through `**legacy_kwargs` that silently swallow renamed or misspelled arguments, and check parity tests to ensure they do not import the same module under two aliases (`assert old_mod is not new_mod`).
   - See `references/dead-code-and-untracking-audits.md` for runtime probe recipes and git-untracking checks.

## 3. Standard Migration Workflow
1. **Characterize & Lock**: Capture live outputs of the legacy path on representative cases and assert `old is not new` in parity tests.
2. **Introduce Adapter / Namespace Shim**: Route callers through the new implementation while preserving legacy import paths and return contracts.
3. **Migrate Consumers Incrementally**: Retarget internal and sibling callers in import-consistent commits (dropping a shim and updating its callers in the same commit).
4. **Verify Clean Clone & Package Artifact**: When untracking directories (`git rm -r --cached`) or deleting modules, extract `git archive HEAD` to a temp directory and run `pytest --collect-only` and wheel smoke tests there.
5. **Final Sunset**: Remove shims, dead fixtures, and stale documentation once active usage reaches zero.

## Final Checklist
- [ ] Replacement proven equivalent on live inputs before legacy deletion (`old is not new` verified)
- [ ] All internal, facade (`__all__`), and sibling-repo consumers audited
- [ ] Copy consolidation separated from stage-order changes
- [ ] Clean `git archive HEAD` clone and built wheel verified when untracking or removing modules
- [ ] `CHANGELOG.md` and public docs updated accurately ("removed from facade" vs. "removed from package")
