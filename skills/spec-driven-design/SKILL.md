---
name: spec-driven-design
description: >-
  Turn a half-formed idea into an approved design spec: multi-turn clarification,
  six-lens parallel brainstorm, and a Zero-Decision draft split into FeatureRange
  and DetailedRange. Not for implementation, code review, or research surveys.
risk: safe
source: local
date_added: "2026-10-28"
---

# Spec-Driven Design Skill

Move from an unproven idea to an owner-approved design spec before code exists.

## When to Use
- A feature request is vague, under-specified, or architecturally open.
- Several defensible designs exist and the owner must choose.
- The work needs a saved spec that a fresh implementer can execute without guessing.
- A concept needs adversarial review before it becomes a commitment.

## When Not to Use
- The change is mechanical, local, and fully specified.
- The work is implementation (`python-pro`, `rust-pro`) or merge review (`code-review`).
- The question is an external approach survey (`tech-research`).
- Codebase facts are unknown; ground them first with `codebase-contracts`.

## Artifact Paths
- Concepts brief: `docs/designs/YYYY-MM-DD_concepts-brief_<topic>.md`. Topic and feature slugs follow the artifact slug and containment rule in `rules/AGENTS.md` §4.
- Approved spec: `docs/designs/YYYY-MM-DD_<feature>.md`.
- Session fallback: the host artifact directory, or `.tmp/`, with the same date prefix.
- Never write an undated file at the repository root.
- If that path already holds an incomplete brief or spec, do not overwrite it. Continue that file, or ask which path to use.

## Workflow

### 0. Intake
Read the predecessor artifact in this order: explicit path, concepts brief, discussion summary, then interactive chat. Confirm the parsed context with the owner before drafting.

### 0a. Phase 0 capability map
When one request bundles independently testable capabilities, write a map before Gate 1: module id, dependency, and build order. The owner approves the map before any module spec.

### 1. Gate 1: Requirements and Architecture Lock
1. Drill the problem with one open-ended question per turn. Attach a one-sentence guess and a confidence percent. Ask again until the problem statement, consumers, hard constraints, and out-of-scope boundaries are clear.
2. Stop asking when you can predict the owner's reaction to the next three questions. Otherwise ask again or step back.
3. Accept only an explicit yes. "Sounds good", silence, and "whatever you think" do not confirm.
4. After that yes, state the intent and end the turn. Do not draft the spec and do not call tools in that turn.
5. Stop on contradictory requests under the Contradiction Halt rule in `rules/AGENTS.md` §2.
6. When architectures diverge, apply Architecture Ownership: up to three options, no ranking, owner decides. Do not use structured question tools for open-ended exploration.
7. Summarize the anchored hypothesis in 2-3 sentences. Wait for explicit readiness confirmation before spawning reviewers.

### 2. Multi-Lens Brainstorm Fan-Out
Dispatch read-only Goldfish subagents per lens using risk-based tiering. Prompt cards live in `references/spec-templates-and-standards.md`.

| Tier | Concept Profile | Lenses Dispatched |
| :--- | :--- | :--- |
| **Core Tier (4 lenses)** | Internal logic, refactor, CLI helper, no external API/DB/auth | `Contrarian/YAGNI`, `UX/Ergonomics`, `Observability/SRE`, `Maintenance/Coupling` |
| **Full Tier (7 lenses)** | Touches public API, auth, database, LLM, or payments | Core 4 lenses + `Cost/Quota/Token`, `Migration/Compatibility`, `Security & Threat Modeling` |
| **Specialist Research** | Novel architecture, SOTA benchmarks, tech selection | On-demand: add `Specialist Lens: SOTA & Industry Prior-Art` |

| Lens | Primary Challenge |
| :--- | :--- |
| Contrarian / YAGNI | Why must this exist? Can reuse solve 90%? |
| Cost / Quota / Token | Peak QPS, memory, storage, token budget |
| UX / Ergonomics | Is the interface intuitive and consistent? |
| Migration / Compatibility | Schema, client, and rollback safety |
| Observability / SRE | Can an on-call engineer debug this at 3 AM? |
| Maintenance / Coupling | Will this be a liability in two years? |
| Security & Threat Modeling | Trust boundaries, prompt injection, abuse, auth bypass |
| SOTA & Industry Prior-Art | Industry consensus, battle-tested OSS alternatives, SOTA benchmarks |

Apply the Arbitration Precedence Standard (`Security > Correctness > Budget > YAGNI > Ergonomics`) when lenses produce conflicting recommendations.

Dispatch by host capability:
- Tier 1, native parallel subagents: Antigravity `invoke_subagent`, Codex `spawn_agent`, OpenCode `Task`.
- Tier 2, sequential cold read: save the hypothesis to disk, then evaluate each lens card in order.

Pass only the lens card, the artifact path, and readable source paths. Never pass conversation history.

### 3. Compile the Concepts Brief
Deduplicate findings, group by severity (`Critical`, `Important`, `Suggestion`, `Nit`), and write the brief. Notify the owner with the path and the 2-3 strongest objections. Iterate until the concept survives review.

### 4. Draft the Spec
Write the spec against the template in `references/spec-templates-and-standards.md`.

- Split semantics: `FeatureRange` covers the problem, goals, architecture, alternatives, and CUJs. `DetailedRange` covers the implementation plan.
- Apply the Zero-Decision Rule on `DetailedRange`: name every file as Create, Modify, or Delete with a rationale, API shape, data flow, and test plan. No code.
- Apply the Alternatives Rule and the Heilmeier questions.
- Fill Critical User Journeys in Given / When / Then form.
- Write to disk. Do not dump the draft into chat.
- After the spec is on disk, end the turn. Owner approval is a later turn.

### 5. Gate 2: Consolidated Review
1. Hand the spec to **doubt-driven-development** and run the five-lens Goldfish review across both ranges.
2. The owner resolves findings with `PROPOSE FIX`, `CONTEST`, `ESCALATE`, or `DECLINE` under the Checkable Contest Invariant.
3. Apply approved fixes, then re-check the semantic split before any later audit.

Default cadence is the two gates above. Pause section by section only when the owner explicitly asks.

## Rules
- One question per turn. Options must be action-oriented, with no `(Recommended)` prefix on architecture choices.
- Do not use narration, a research dump, or a pull-request citation as evidence. Cite a file, a probe, or an owner decision.
- Never present large drafts in chat. Write the artifact and link it.
- Plain English. No promotional adjectives, no flattery, no apologies.
- Reviewers are read-only and stateless. A same-context review is not a Goldfish review.
- Cap re-audits at one per stage and follow the spec/design review bound in `rules/AGENTS.md` §1.

## Related Skills
- Hand off the approved spec to **doubt-driven-development** for the consolidated five-lens review.
- Use **ux-product-shaper** when the approved spec needs information architecture, Surface Mode, and the 8-state contract.
- Use **python-patterns** for framework, layout, and ADR decisions inside the spec.
- Apply **code-minimalism** when the concept can be reduced to a smaller scope.
- Use **tech-research** when the alternatives require external evidence.
- Use **codebase-contracts** to ground the spec in current code and to publish contracts afterward.

## Final Checklist
- [ ] Problem, consumers, constraints, and non-goals are explicit
- [ ] Architecture options were owner-approved, not auto-selected
- [ ] Six brainstorm lenses ran in isolated contexts
- [ ] Concepts brief and spec use ISO-dated paths
- [ ] `FeatureRange` and `DetailedRange` are both complete
- [ ] Zero-Decision Rule holds on the implementation plan
- [ ] Alternatives and risks are documented
- [ ] Owner approved Gate 2
