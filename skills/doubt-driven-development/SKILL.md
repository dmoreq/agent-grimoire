---
name: doubt-driven-development
description: >-
  Adversarial review of a non-trivial decision before it hardens (assumptions, edges, blast radius).
  Not for mechanical edits, exploratory research notes, or merge review.
risk: safe
source: local
date_added: "2026-08-23"
---

# Doubt-Driven Development Skill

Subject non-trivial decisions to adversarial review before they harden.

- Load `references/goldfish-review-lenses.md` for the five-lens multi-agent review of a saved spec or plan.

## When to Use
- Architectural or design choices under uncertainty
- Branching logic, cross-module contracts, concurrency, or security-sensitive behavior
- Claims not fully enforced by types/compiler/tests yet
- High blast-radius changes: public API, data migration, production-critical paths
- Unfamiliar code where confidence may be false
- Research outputs that are about to harden into an implementation decision

## When Not to Use
- Mechanical edits: rename, format, move files
- Obvious one-line fixes
- User explicitly prioritizes speed over verification
- Pure summary/research with no decision being locked in
- Intermediate research notes that are still exploratory

## Non-Trivial Test
Use this skill if at least one is true:
- Introduces or changes branching/state transitions
- Crosses module or service boundaries
- Asserts invariants not yet protected by tests/types
- Is expensive or hard to reverse
- Converts research findings into a concrete adoption/rejection decision

## Research Decisions
Use this skill on research outputs only when they harden into a decision.

Examples:
- Adopting a library, model, or approach
- Rejecting alternatives with material trade-offs
- Recommendations that will drive implementation

For research decisions:
- **Artifact** = recommendation + evidence summary
- **Contract** = project constraints and success criteria

Challenge:
- Weak or selective evidence
- Missing baselines
- Overconfident SOTA claims
- Recommendations not tied to constraints
- Confusion between "trending" and "battle-tested"

Do not use this skill to adversarially review every research report by default.

## Goldfish Multi-Lens Review

Use this mode for a saved spec or implementation plan. Five read-only lenses run in isolated contexts. The copy-ready prompt cards live in `references/goldfish-review-lenses.md`.

### Semantic Split
Find one boundary header: `## Detailed Implementation Plan`, `## Implementation Plan`, `## Work Breakdown`, or `## Implementation Steps`.

- `FeatureRange` = line 1 through the line before the boundary.
- `DetailedRange` = boundary header through the end.
- No boundary: `FeatureRange` covers the full document, `DetailedRange` is `N/A`, and the missing split is a Major finding.

### Lenses and Scope

| Lens | Scope | Primary Focus |
| :--- | :--- | :--- |
| Zoom-Out | Full document | Simplicity, YAGNI, macro reuse, altitude control |
| Comprehension | Full document | Undefined terms, assumed knowledge, clarity |
| Design Critic | `FeatureRange` | Architecture, scalability, unmitigated risk |
| Implementation Readiness | `DetailedRange` | Zero-Decision Rule, data & schema migration, test plan |
| Codebase Details | `DetailedRange` | Document versus code, stale references, drift |

### Plan Scope Tiering
- **Fast Plan Tier** (< 100 plan lines, single-module scope): Dispatches 3 lenses: `Comprehension`, `Implementation Readiness`, `Codebase Details`.
- **Full Architecture Tier** (>= 100 plan lines, multi-module, schema, or system change): Dispatches all 5 lenses.

### Dispatch
- Tier 1, native parallel subagents: Antigravity `invoke_subagent`, Codex `spawn_agent`, OpenCode `Task`.
- Tier 2, sequential cold read: save the artifact, then run each lens card in order.

Pass only the lens card, artifact path, line range, and readable source paths. Never pass conversation history or a prior verdict.

### Consolidated Report
Deduplicate findings across lenses. Group by `Critical`, `Important`, `Suggestion`, and `Nit`. Write `docs/reports/YYYY-MM-DD_goldfish-review_<topic>.md`. Allow one re-audit per stage and follow the spec/design review bound in `rules/AGENTS.md` §1. Topic slugs follow the artifact slug and containment rule in `rules/AGENTS.md` §4.

## Process

### 1. CLAIM
State the decision in 2–3 lines and why it matters.

### 2. EXTRACT
Isolate the smallest reviewable artifact + contract. Strip prior reasoning.

### 3. DOUBT
Review adversarially to find issues, not to approve.

Use this prompt shape:

```text
Find what is wrong with this artifact.
Assume the author is overconfident.
Look for unstated assumptions, missing edge cases, hidden coupling,
contract violations, and failure modes.
Do not validate. Do not summarize.
List concrete issues, or state that none were found.

ARTIFACT:
CONTRACT:
```

### 4. RECONCILE
Classify each finding:
- **PROPOSE FIX**: Valid finding. State the exact replacement or structural correction.
- **CONTEST**: Inaccurate finding. Cite evidence the reviewer could read: a file and symbol, a spec clause, or command output. "This was intentional" is not evidence.
- **ESCALATE**: The finding cannot be resolved with readable evidence. Hand it to the owner with the missing context stated.
- **DECLINE**: Valid Nit with no worthwhile fix. Record it and move on.

Rules:
- A contest must be checkable under `rules/AGENTS.md` §1. If it is not, use ESCALATE or PROPOSE FIX.
- Never change a severity while contesting. State the reason and let the owner decide.
- Do not contest a comprehension gap. If a fresh reader cannot follow the document, the document is missing context.
- Do not add context only to satisfy a reviewer. Add it when a human reader needs it.

Re-read the artifact before accepting findings.

### 5. STOP
Stop when:
- Findings are trivial/noise, or
- The spec/design review bound in `rules/AGENTS.md` §1 is reached, or
- Residual risk is explicitly accepted by the user

## Rules
- Pass artifact + contract only; do not pass the claim as a conclusion.
- Prefer disproof over approval.
- Do not loop past the spec/design review bound in `rules/AGENTS.md` §1; escalate instead.
- This is in-flight checking, not a replacement for final review.
- For research, challenge the decision — not every intermediate survey.

## Reviewing a written plan before execution

A plan that names exact expected outputs is an artifact worth doubting, because every
prediction in it will be treated as ground truth by whoever executes it. Check each claim
for whether it was *observed* or *assumed*:

- **Predicted command output** ("expect 2 failed", "expect `All checks passed!`", "this case
  may already pass") — run the command first if it is cheap, or delete the prediction. A wrong
  expectation sends the implementer debugging correct code, and a hedged one ("may already
  pass") is worse than none because it licenses ignoring the result.
- **Predicted failure reason** — verify the exception type and message actually match. "This
  will fail because the constructor accepts invalid input" and "this will fail because a
  validation message is wrong" lead to opposite fixes.
- **Predicted magnitude** ("recover ~12 tokens", "about 2x faster") — either cite the run that
  produced the number or label it an estimate that must be replaced by measurement.
- **Ordering dependencies between steps** — when step N+1 rewrites what step N tested, say
  explicitly that step N's test is re-run as a regression check, not a formality. Otherwise a
  later step silently invalidates an earlier green.
- **Decision tables with pre-committed thresholds** — a plan that states "if the delta is below
  X, keep the old default" is stronger than one that leaves the call to judgement after seeing
  results. Prefer the former; flag the latter as a gap.

Everything the plan asserts about current state ("file X is tracked", "function Y has no
callers", "the tree is clean") is a probe, not a premise. Re-verify with a command and record
what it returned.

## Related Skills
- Use **spec-driven-design** to produce the spec that this review audits.
- Use **tech-research** when alternatives or evidence are missing; hand off here only when a decision is being locked.
- Use **code-minimalism** when a finding is over-engineering rather than a defect.
- Use **python-patterns** when the doubt is a framework, layout, or boundary decision.
- Use **python-testing** (or crate tests) to turn important doubts into regression tests.
- Use **deprecation-migration** when the decision is a sunset or cutover.
- Use **code-review** for the final diff and merge-quality gate.
- Use **ux-critic** when the decision is a rendered-UI design critique.
- Use **codebase-contracts** when the finding depends on whether the code matches a documented contract.

## Final Checklist
- [ ] Decision is actually non-trivial
- [ ] Claim and stakes are explicit
- [ ] Artifact and contract are isolated
- [ ] Review prompt is adversarial
- [ ] Findings are classified, not rubber-stamped
- [ ] Actionable issues are fixed or explicitly deferred
- [ ] Stop condition is reached (see `rules/AGENTS.md` §1).
- [ ] Important residual risks are visible to the user
- [ ] If research-derived, recommendation is tied to constraints and evidence quality was challenged
