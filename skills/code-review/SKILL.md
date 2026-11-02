---
name: code-review
description: >-
  Review code diffs, audit public APIs, or inspect unpacked repo snapshots for correctness, safety, performance, YAGNI, and test coverage.
  Not the first skill for implementing features from scratch.
risk: safe
source: local
date_added: "2026-09-11"
---

# Code Review Skill

Review concrete diffs or an explicitly scoped existing API surface. Review the code, not the author. Zero findings is valid when evidence supports it.

- Load `references/public-api-audits.md` when auditing all exports, contracts, and consumers of an existing package — including "what legacy is still here" audits. It covers symbol-level deadness, the shipped-wheel inspection step, and decision-ready verdicts.
- Load `references/repo-snapshot-review.md` when reviewing an unpacked code archive, fresh clone, or colleague handoff with no PR diff.
- Load `references/goldfish-code-review-lenses.md` for non-trivial diffs (>= 100 LOC, new helpers/rules, multi-module, concurrency/security/public-API) or parallel Goldfish dispatch.

## When to Use
- Pull requests or local git diffs
- Quality gate before merging behavior or public-API changes
- Looking for bugs, security issues, over-engineering, or missing tests
- Auditing public API exports, contracts, actual consumers, and algorithm suitability
- Reviewing a repo snapshot or declarative skill bundle against its own README claims
- Peer-review step for non-trivial subagent code deliverables (diff + contract only)

## When Not to Use
- No concrete code surface or change to inspect
- Pure design discussion without concrete code (`doubt-driven-development` / `python-patterns`)
- Starting a feature from scratch (implement first via `python-pro` / `rust-pro`, then review)

Keep review-only requests read-only. Implement fixes through the language skill only when requested; an audit backlog is not implementation authorization.

## Verifying Claims and Scans
- Verify scan scopes before reporting "clean" (`git grep` cross-check); classify benign mentions from live references (`references/repo-snapshot-review.md` §6).
- Prove artifact reachability using the loader's true resolution paths rather than flat directory probes.

## Related Skills
- Use **python-pro** to apply the requested fix in the language idiomatic to the codebase.
- Use **code-simplification** when the main issue is structural complexity or nesting in existing code.
- Use **code-minimalism** when the diff contains bloat, unrequested abstractions, or premature dependencies.
- Use **deprecation-migration** when the diff or review surfaces a legacy API that should be sunset.
- Use **codebase-contracts** when a directory README or spec documents the changed behavior.
- Use **python-testing** or crate tests when behavior changed without tests.
- Use **rust-async-patterns** when reviewing async Rust task, channel, or cancellation code.
- Use **ui-accessibility** for UI and WCAG review.
- Use **technical-reporting** for a Markdown audit handoff, or **html-report** for a single-file HTML audit page.

- Use **dart-modern-idioms** when reviewing a Dart or Flutter diff for idiom, exhaustiveness, or async-safety compliance.
- Use **flutter-testing-verification** when a Flutter diff changed behavior without widget or integration tests.
## Review Workflow & Gates

Select the review mode first: diff review (below), package export audit (`references/public-api-audits.md`), repo snapshot review (`references/repo-snapshot-review.md`), or declarative skill-bundle review (`references/repo-snapshot-review.md` §5).

For all modes:
- Capture git revision and dirty-tree scope; recheck before finalizing if concurrent edits occur.
- Separate static observations, independently executed failures, and proposed fixes. Never present an untested correction as a validated patch.
- Reproduce important delegated findings through the actual consumer when possible.
- Resolve every method and class a README or spec advertises against the built artifact; a documented API absent from the code is a **Critical** finding.
- When reviewing a refactor or deletion plan, verify that old and new paths were executed on identical inputs with matching observable outputs.

For diff reviews, execute automated and structural gates before manual semantic review:
1. **Automated Quality Pre-Flight Gate (Targeted & Deduplicated)**:
   - **Skip Gate for Non-Executable Changes**: If the diff contains only documentation, markdown, or static non-code assets, skip pre-commit and test execution entirely.
   - **Reuse Verified Proof**: If the authoring agent or subagent already provided passing test and lint outputs for this exact diff, do not re-run them.
   - **Targeted Pre-commit Only**: Run only against modified files: `pre-commit run --files <changed_files>` or fast direct checks (`ruff check <files>`, `pyright <files>`). Never run `--all-files` during routine diff reviews.
   - **Targeted Tests**: Run only tests relevant to the modified modules (`pytest -n 4 path/to/changed_test.py` or `cargo test <module>`).
   - If pre-commit or tests fail: halt deep review immediately and report failures as a **Critical** blocker.
2. **Risk-Based Multi-Lens Goldfish Dispatch (3-Tier)**:
   - **Fast path** (< 100 effective LOC, one module, no new helper, no async/security/crypto/public-API change): run the checklist in-thread. Spawn no subagent.
   - **Specialist escalation** (< 100 LOC touching async, security, auth, crypto, or public-API): dispatch `cr-correctness-invariants` + matching specialist (`cr-security-trust-boundary` or `cr-concurrency-memory-perf`). Run concurrently and reconcile in-thread.
   - **Core 3-lens swarm** (>= 100 LOC, new helpers/rules, multi-module): `cr-correctness-invariants`, `cr-mechanism-generalization`, `cr-codebase-reuse-and-contracts`.
   - **Full 5-lens swarm** (also I/O, async/threads, large data, auth, SQL, or paths): add `cr-concurrency-memory-perf` and `cr-security-trust-boundary`.
   - Keep lens 2 inside the diff (ad-hoc hardcoding, symptom band-aids, YAGNI, complexity) and lens 3 outside it (`git grep` reuse, stdlib, callers, contract drift). Never merge them.
   - Tier 1 native parallel: Antigravity `invoke_subagent`, Codex `spawn_agent`, OpenCode `Task`. Tier 2 sequential cold read for Zed, Grok, ZCode, or a single-thread CLI.
   - Pass only the persona card, diff paths, contract path, and pre-flight confirmation. Never pass author reasoning.
3. **Reviewability & Blast Radius Gate**:
   - **Reviewability Budget**: Diff exceeds 400 effective LOC (excluding lockfiles/fixtures) → **Important** (request splitting into stacked PRs).
   - **Separation of Concerns**: Diff mixes mechanical refactoring with behavioral logic → **Important** (request isolating refactors).
   - **Public Surface**: Public signature changed without backward compatibility or version bump → **Critical**.
4. **Omission Checklist (Verify What Is Missing)**:
   - **Error Path Cleanup**: Are open resources (files, sockets, DB transactions) released in failure branches?
   - **Callers of Deleted Symbols & Dangling References**: Confirm every reference—code importer, sibling script, and non-code config/docs—was retargeted in the same commit. Grep the whole tree (`git grep -nw '<name>' <rev> -- .`), never hand-written globs that risk missing files at different depths. A deleted target still referenced is a **Critical** dangling reference.
   - **Observability**: Are new error states logged with contextual parameters?
   - **Negative & Edge Tests**: Are empty collections, `None` inputs, and timeouts tested?
   - **Documentation Sync**: Are `CHANGELOG.md`, `__all__`, or `README.md` updated for public changes? If a directory README or spec documents the changed behavior, run a **codebase-contracts** drift check instead of guessing.
   - **Commit-Message Claims vs Artifact**: Verify each concrete claim in the commit message against the tree, not the intent. A message asserting a cleanup ("no longer references X", "removes Y") is a testable statement; if the tree still violates it, that is a finding, and the message itself becomes misleading evidence for downstream reviewers.

When re-reviewing an amended commit: verify the delta directly (`git diff <old> <new> --name-only`) to confirm it contains ONLY requested changes. Re-run the original check against the new revision to verify closure.
5. **Semantic & Architectural Review**:
   - **Correctness**: Does what it claims; edge and error paths; no obvious race conditions.
   - **Safety & Security**: Inputs validated; parameterized queries; no hardcoded or leaked secrets.
   - **Performance & Concurrency**: No extra work on hot paths; no shared mutable state across async tasks/threads without locks.
   - **Maintainability & Complexity**:
     - Cyclomatic Complexity > 10, Cognitive Complexity > 15, or Nesting Depth >= 4 → **Important** (hand off to `code-simplification`).
     - Cyclomatic Complexity > 20 or Cognitive Complexity > 20 without justification → **Critical**.
     - Unjustified code duplication (> 15 identical lines) → **Important**.
   - **Over-Engineering & YAGNI**: No single-implementation interfaces, unrequested dependencies, or speculative abstractions; deliberate shortcuts annotated with `# ponytail: <limit>`.

## Severity Levels (Text Only — No Emoji)
- **Critical** — must fix before merge (bugs, security flaws, data loss, test/lint failures, breaking API shifts)
- **Important** — should fix (complexity violations, missing error handling/tests, diff > 400 LOC)
- **Suggestion** — cleaner alternative with clear technical trade-off
- **Nit** — non-blocking style preference (<= 2 per review; never block merge)

Calibrate severity by reachability. A latent defect unreachable by current paths is **Suggestion**, not **Important**—state the reachability rationale explicitly. Escalate minor flaws that are reachable on common paths. When a contract clause lacks an automated enforcement hook, report it as an unverified limitation rather than a defect or guarantee.

## Output Format
1. **Summary** — 1–3 sentences stating diff scope, pre-flight gate status, and overall verdict.
2. **Findings** — Ordered by severity (`Critical` → `Nit`). Every `Critical` and `Important` finding MUST include:
   - **Location**: `path/to/file.py#L42-L46`
   - **Failure Scenario**: Concrete input or race condition that triggers the defect.
   - **Correction & Acceptance**: Smallest fix direction, drop-in replacement diff when helpful, and regression test criteria.
   - **Rationale**: Operational, security, or data integrity impact.
3. **Positive Notes** — Highlight clean patterns or effective tests (if any).
4. **Questions** — Clarify ambiguous architectural assumptions (if any).
5. **Reconciliation Verdict** (multi-agent review only) — Record `PROPOSE FIX`, `CONTEST`, `ESCALATE`, or `DECLINE` per finding. `CONTEST` requires a file and symbol, spec clause, or command output. Never change severity while contesting. `ESCALATE` when the proof is outside every readable artifact.
