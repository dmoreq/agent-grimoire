---
name: python-patterns
description: >-
  Architecture-time choices: framework, project layout, and ADRs.
  Not for asyncio vs process-pool selection, pytest recipes, or line-by-line implementation.
risk: safe
source: local
date_added: "2026-02-27"
---

# Python Patterns Skill

Decision-making for Python architecture: framework, project structure, and trade-offs. Think; do not copy patterns.

## When to Use
- Choosing a Python framework or service shape
- Structuring a new or growing Python project
- Recording an ADR for a durable architecture choice
- Assessing an existing Python subsystem's design, generalization, and architectural trade-offs

## When Not to Use
- Executor choice (asyncio / threads / processes) → **python-concurrency**
- Implementing modules → **python-pro**
- Writing tests → **python-testing**
- Basic syntax or non-Python stacks
- One-off scripts with no architectural decision

## Related Skills
- Use **spec-driven-design** when the architecture decision still needs an owner-approved spec.
- Use **doubt-driven-development** to stress-test a boundary or layout choice before it hardens.
- Use **python-pro** once the architecture decision is made.
- Use **python-concurrency** when the remaining question is I/O versus CPU execution model.
- Use **python-performance** when the architecture claim depends on a measured runtime fact.

## Existing Subsystem Assessment

1. Read module boundaries, public exports, dependency manifests, representative callers, and behavioral tests before judging the design.
2. Separate four questions: architectural cohesion, behavioral correctness, domain generalization, and measured efficiency. Evidence for one does not establish the others.
3. Trace suspected defects through callers. Distinguish an internal component's documented input contract from an end-to-end failure.
4. Audit evaluation assertions before trusting benchmark labels. Compare fixture fields with fields actually checked; confidence and quality scores are not substitutes for output correctness.
5. Run targeted verification and bounded probes. Report failures without silently fixing snapshots or production code during a read-only assessment. A failing baseline limits confidence but does not prevent an explicitly qualified architecture review.
6. Present a verdict by dimension, concrete findings with `path:line` and observed outputs, strengths, evidence limitations, and prioritized minimal changes. Avoid unsupported numerical design scores.

For grammar, lexer, or normalization subsystems, load `references/parser-generalization.md`. Use **python-performance** for measured runtime analysis rather than inferring optimization from algorithm names.

### Unifying existing workflows without speculative abstractions

1. Name workflows by functionality rather than customer segment or input source. Separate workflow, intent, execution target, storage schema, and transport as independent dimensions.
2. Build an explicit supported workflow/schema matrix before proposing interfaces. Select concrete implementations at construction and reject unsupported combinations before I/O; future combinations justify a seam, not empty implementations or a plugin registry.
3. Trace the complete observable stage sequence through callers, not just the nominal component. Retrieval may hydrate candidates from priors; ranking may continue through deduplication, target refinement, and personalization outside the scorer.
4. Put DSL, fallback queries, projections, nested semantics, and decoding under schema ownership. Inventory raw-document reads in ranking before claiming schema independence; normalize only consumed evidence rather than forcing a universal candidate model.
5. Preserve distinct result and score semantics. Share dependency wiring and genuinely identical utilities, not algorithms whose apparent similarity hides different domain contracts.
6. Lock stage order, mutation ownership, early stops, batching, candidate budgets, identity changes, and consumer compatibility before extraction. Wrapping a concrete client can disable type-based batching and regress latency without changing output tests.
7. Require paired per-case parity for mechanical migration, plus separate performance measurements. Audit cohort exclusions, grouped versus primary identity metrics, fixture skips, and stage timers before treating existing thresholds as accuracy or latency proof.
8. Introduce functional aliases first, extract boundaries next, and move package layout last. Keep compatibility adapters thin and defer removal until actual consumers migrate.

## 1. Framework Selection
Choose based on context, not habit.

- **API / microservices / AI serving** → FastAPI
- **Full-stack / CMS / admin-heavy** → Django
- **Simple service or learning** → Flask
- **Background workers** → Celery, ARQ, or equivalent (with any web framework)

Ask: API-only or full-stack? Need built-in admin? Team async-ready? Existing constraints?

## 2. Typing & Configuration Strategy
Always type function parameters/returns, public APIs, and class attributes that matter. Can be lighter on obvious locals, one-off scripts, and some tests. Prefer `list[str]`, `str | None` when the version allows.
- **External Configuration**: Use `pydantic-settings` (`BaseSettings`) to validate environment variables at the trust boundary.
- **API Payloads**: Use Pydantic v2 schemas for request and response serialization.

## 3. Project Structure & Layout
- **Production Libraries & Services**: Use the `src/` layout (`src/<package_name>/`).
  *Reduces accidental working-tree imports. Verify the built wheel outside the checkout; `src/` alone does not guarantee installed-package testing when editable installs or path overrides are active. For existing projects, isolate layout migration from behavioral refactoring.*
- **Small CLI or Utilities**: Flat layout or single module if under 300 LOC.
- **Service Layers**:
  - `routes/` / `api/`: Thin HTTP adapters; parameter parsing and status codes only.
  - `services/`: Core business logic; framework-agnostic.
  - `models/`: Three-tier model separation:
    1. **Domain Model**: `@dataclass(slots=True)` containing pure domain rules (no ORM or Pydantic base classes).
    2. **API Schema**: `pydantic.BaseModel` for external I/O validation.
    3. **Persistence Entity**: ORM or raw SQL mapping.
    *Invariant*: Never leak database ORM objects directly out of API routes.

### Functional Core, Imperative Shell

- **Shell (I/O)**: routes, adapters, and repositories parse inputs, hydrate context, call the core, and persist results.
- **Core (computation)**: pure functions and immutable value objects. No network, database, filesystem, clock, randomness, or global state. The same input returns the same output and is testable without fakes.
- **Explicit hydration**: accept identifiers at the shell, then fetch in one batched or bounded-concurrent step (`python-concurrency`). Never hide a per-item fetch inside a loop or inside a core function that takes only an ID.
- **Graceful degradation**: apply it only to non-critical enrichment. Decision-critical data fails closed. A safe default must be explicit, logged or metricized, and must not silently change scoring or ranking semantics (`algorithm-optimization`).

## 4. Error Handling
- Domain exceptions in services
- Convert at the API boundary (exception handlers)
- Consistent error shape (code, message, details)
- Never expose internal tracebacks or SQL queries to clients

## 5. Background Tasks
- Simple fire-and-forget → framework background tasks
- Long-running / retry / distributed → Celery, ARQ, or equivalent
- Choose from persistence, retry, and scale needs

## Design Principles
Apply pragmatically: clear names, focused modules, composition over deep inheritance, tests for critical behavior. DRY only when the abstraction is cheaper than repetition.

## Optional ADR
For significant choices (framework, ORM vs SQL, sync vs async *at the service boundary*):
- **Context**: constraints and drivers
- **Decision**: chosen pattern
- **Consequences**: trade-offs

If the open question is which executor to use, stop and load **python-concurrency**.

## Core Decision Checklist
- [ ] Framework chosen from context, not habit
- [ ] Structure matches current scale
- [ ] Error handling is consistent at the boundary
- [ ] Background work has the right tool
- [ ] Trade-offs understood before implementing

## Anti-Patterns
- Defaulting to one framework for every project
- Putting business logic in routes/views
- Skipping types on public APIs
- Over-engineering small projects
