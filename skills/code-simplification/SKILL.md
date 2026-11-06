---
name: code-simplification
description: >-
  Simplify working code without changing behavior (nesting, names, accidental complexity).
  Not for redesign, performance rewrites, or untested risky edits.
risk: safe
source: local
date_added: "2026-08-23"
---

# Code Simplification Skill

Simplify code for clarity and maintainability without changing behavior. Focus on existing working code.

## When to Use
- Code works but is harder to read, maintain, or extend than it should be
- After a feature/fix when implementation feels heavier than needed
- During review when complexity, nesting, duplication, or unclear naming is flagged
- When cleaning recently modified code

## When Not to Use
- Code is already clear enough
- You do not yet understand the code
- Performance-critical path where simpler form is measurably worse
- Broad redesign or rewrite is the real goal
- The task is to name which Fowler smell applies (`code-smells`)
- No tests and behavior is risky to change without characterization first

## Core Principles
1. **Preserve behavior exactly** — same outputs, errors, side effects, and edge cases.
2. **Clarity over cleverness** — explicit readable code beats dense one-liners.
3. **Follow project conventions** — simplify toward local style, not personal taste.
4. **Scope tightly** — default to recently changed code; avoid drive-by refactors.
5. **Simplify incrementally** — one change at a time; keep tests green.

## Process
1. Understand responsibility, callers, edge cases, and existing tests.
2. Start from confirmed **code-smells** rows. Do not run a second smell detector. Apply the recipe that matches the smell name. Names such as `data`, `temp`, and `result` are still renamed to domain words. Dead code is removed only when **codebase-minimalism** has confirmed it is unused.
3. Apply one simplification at a time.
4. Verify targeted tests/build still pass (`pytest -n 4 path/to/test_module.py`). Do not run full test suites or pre-commit hooks between incremental simplification edits.
5. Stop when a new teammate would understand it faster.

## Refactoring Recipes for Complexity
1. **Invert and Guard (Reduces Cognitive and Nesting Complexity)**:
   - Invert nested conditional branches to return or continue early.
   - Keep maximum indentation depth <= 3.
2. **Dispatch Table or Dictionary Map (Reduces Cyclomatic Complexity)**:
   - Replace long `if/elif/else` ladders with dictionary or match-case lookups for discrete keys.
3. **Pipeline and Decomposition (Reduces Function Volume and Coupling)**:
   - Extract multi-step sequences into private helper functions or generator pipelines.
   - Keep function bodies within the hard length threshold in `rules/AGENTS.md` §3.

## Do Not
- Change behavior to make code "nicer"
- Replace a local pattern with a "similar" shared pattern. Copy the pattern string exactly, then call the shared singleton. A broader keyword set, added flags, or a following collapse/expand step changes matches.
- Do not merge two similar classification ladders by also merging their context. Share the classifier and pass each caller's flags (which text, which branches). The ladders look duplicated because the flags differ.
- Prove "no compile outside the SSOT module" with a source-text search. Walk `ast.Call` nodes whose function is `re.compile` or `regex.compile`. Suggestion strings contain those words and are not compiles.
- Remove error handling, logging, or guards that encode intent
- Optimize solely for fewer lines of code
- Mix simplification with feature work in the same change/commit
- Over-inline helpers that give useful conceptual names

## Related Skills
- Triggered from **code-review** when structural complexity is flagged.
- Use **code-smells** when the code needs a named Fowler smell before a rewrite.
- Use **code-minimalism** if the primary problem is speculative over-engineering or unnecessary libraries.
- Use **python-testing** (or crate tests) to lock behavior before simplifying.
- Before merge: **code-review**.

## Final Checklist
- [ ] Behavior preserved exactly (inputs, outputs, exceptions, side-effects)
- [ ] Scope limited strictly to intended code (no drive-by refactors)
- [ ] Tests still pass without rewriting assertions to fit new behavior
- [ ] Naming, control flow, and structure are genuinely clearer
- [ ] Diff is reviewable, atomic, and free of unrelated changes
