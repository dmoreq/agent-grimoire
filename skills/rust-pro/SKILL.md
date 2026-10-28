---
name: rust-pro
description: >-
  Implement production Rust (Edition 2024, rustc 1.85+): ownership, types, errors, unsafe, clippy.
  Not for Tokio task/channel design (use rust-async-patterns).
risk: safe
source: local
date_added: "2026-09-11"
---

# Production Rust Skill

Senior Rust for services, crates, CLIs, and systems code. Edition 2024 requires **rustc 1.85+**. If MSRV is below 1.85, stay on Edition 2021 and do not claim 2024 features.

## When to Use
- Building Rust services, libraries, CLI tools, or systems components
- Ownership, lifetime, borrowing, or API design
- Performance while preserving memory safety
- Reviewing or refactoring **synchronous** Rust

## When Not to Use
- Tokio tasks, channels, `select!`, shutdown, backpressure → **rust-async-patterns**
- Python-only work
- Basic syntax-only questions
- Scripts where Python/Go is the right tool

## Related Skills
- Use **rust-async-patterns** when the work is Tokio/tasks/channels/streams.
- Use **pyo3-maturin** only when exposing Rust as a Python extension.
- Before merge: **code-review**.

## Core Principles
- Compile-time guarantees over runtime checks
- Explicit error handling — never ignore errors
- Zero-cost abstractions first, then measure
- Message passing over shared mutable state
- Document every `unsafe` block with safety invariants
- Small intentional public API
- Prefer static dispatch; dynamic only when necessary
- Instrument with `tracing` instead of `println!`

## Recommended Stack
- Error: `thiserror` (libraries) + `anyhow` (applications)
- Serialization: serde
- Logging: tracing + tracing-subscriber
- Testing: built-in + proptest + criterion
- Linting: clippy + rustfmt. Pedantic/nursery only if the repo already enables them
- HTTP: axum / tonic (gRPC)
- Async runtime: Tokio — **patterns live in rust-async-patterns**

## Language & Type System
- Ownership, borrowing, lifetimes, NLL
- GATs, const generics, associated types when they simplify the API
- Newtype, PhantomData, ZSTs (use newtypes for numeric units, for example `Milliseconds(u64)`)
- Trait design, object safety, coherence
- Native async trait methods; `async-trait` only when `dyn` is required

## Error Handling
- `Result` + `?` as default
- Custom errors with `thiserror`; context with `anyhow` in apps
- No `.unwrap()` / `.expect()` in non-test production paths

## Performance
- Profile before optimizing (`cargo flamegraph`, criterion)
- Minimize allocations; prefer references and `Cow`
- SIMD and lock-free only when justified by a profile

## Safety
- Minimize `unsafe`; every block has `// SAFETY:`
- Prefer safe abstractions over raw pointers
- Miri when validating unsafe

## Testing & Quality
- Unit + integration + doc tests (target specific tests during iteration: `cargo test <test_name>`; avoid full-workspace test runs on minor edits)
- proptest on invariants; criterion on hot paths
- clippy + `cargo deny` / `cargo audit` as the repo already uses them
- Enforce complexity thresholds in `clippy.toml`: `cognitive-complexity-threshold = 15`
- Warn on excessive complexity or function size: `#![warn(clippy::cognitive_complexity)]`, `#![warn(clippy::too_many_lines)]`

## Response Approach
1. Clarify safety, performance, MSRV, and runtime constraints
2. Simple idiomatic solution first
3. Type-safe APIs with clear error surfaces
4. Tests and edge cases
5. Document unsafe or performance trade-offs

## Checklist
- [ ] MSRV / edition confirmed (2024 ⇒ 1.85+)
- [ ] Error strategy chosen (`thiserror` vs `anyhow`)
- [ ] No `.unwrap()` / `.expect()` in non-test code
- [ ] Lifetimes/ownership are minimal and correct
- [ ] All `unsafe` blocks have `// SAFETY:`
- [ ] Public API is minimal and documented
- [ ] Clippy-clean and complexity within limits (Cognitive <= 15, nesting <= 3)
- [ ] Tests for the behavior change
- [ ] Async work handed to `rust-async-patterns`
