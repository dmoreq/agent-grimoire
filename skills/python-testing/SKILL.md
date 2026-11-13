---
name: python-testing
description: >-
  Write or fix pytest suites: fixtures, boundary mocks, property-based tests, async tests, flaky tests, and golden-set audits.
  Not for implementing features or load/performance benchmarks.
risk: safe
source: local
date_added: "2026-02-27"
---

# Python Testing Skill

Design and maintain fast, deterministic, high-signal Python test suites with `pytest`.

- Load `references/implementation-playbook.md` **only** for concrete pytest snippets (fixtures, parametrize, mock, async).
- Load `references/golden-set-audits.md` when auditing golden-set fixtures, oracle sensitivity, mutation probes, or snapshot drift.

## When to Use
- Unit, integration, property-based, or API tests in Python
- `pytest` configuration, fixture design, and TDD workflows
- Mocking external boundaries (HTTP, DB, time, randomness)
- Debugging async tests, flaky tests, or `PYTHONPATH` environment contamination
- Auditing golden-set fixtures and assertion strength

## When Not to Use
- Non-Python testing (use Rust crate tests or `dash_duo` as appropriate)
- Feature implementation with no test scope (`python-pro`)
- Runtime latency or memory benchmarks (`python-performance`)

## Related Skills
- Required for **Python** behavior changes before **code-review**.
- Use **debugging-and-error-recovery** when a failure is not yet localized.
- Use **verify-and-stop** to run the decisive test check once and terminate cleanly.

## 1. Core Testing Invariants
1. **Test Behavior and Public Contracts, Not Private Implementation**: Assert public return fields and observable side effects, never private `_stage` names scheduled for refactoring.
2. **Targeted & Parallel Execution First**:
   - Run only affected test files/functions during iteration (`pytest -n 4 path/to/test.py -k test_name`).
   - Run full suites at most once at the final pre-merge gate.
   - Do not invent arbitrary coverage percentage gates.
3. **Clean Interpreter Invocation**:
   - When virtualenvs or sibling packages exist, strip leaked environment variables (`env -u PYTHONPATH -u PYTHONHOME /abs/path/.venv/bin/python -m pytest ...`) so third-party C-extensions (`pydantic_core`, `pyarrow`) never resolve from a mismatched Python version.
4. **Verify Actual Exit Codes**:
   - Piping test commands through `| tail` or `| grep` without `set -o pipefail` masks non-zero exit codes. Always verify the test runner's own exit status and summary line.

## 2. Test Layer Strategy

| Layer | Purpose | Typical Tools |
| :--- | :--- | :--- |
| **Unit** | Pure business logic, edge cases, branches | `pytest`, `@pytest.mark.parametrize` |
| **Property-Based** | Parsers, serializers, round-trip invariants | `hypothesis` (`@given(...)`) |
| **Integration** | HTTP routes, DB queries, filesystem contracts | `pytest` + `httpx` / `TestClient`, SQLite/containers |
| **Characterization / Golden** | Locking live outputs before refactoring/migration | `references/golden-set-audits.md` |

## 3. Pytest Configuration & Determinism Guardrails
- Standard `pyproject.toml` configuration:
  ```toml
  [tool.pytest.ini_options]
  addopts = "--strict-markers --strict-config -ra -n 4 --dist=loadscope"
  testpaths = ["tests"]
  ```
- **Hash-Seed Stability**: Verify new tests do not depend on dict/set iteration order by running the targeted file with `PYTHONHASHSEED=random pytest path/to/test_file.py -k test_name`.
- **Time & Randomness**: Freeze time with `time-machine` (or `freezegun`) and seed RNGs (`random.seed(42)`). Never use `time.sleep()` or `asyncio.sleep()` for synchronization when an `asyncio.Event` works.
- **Boundary Mocking Only**: Mock external HTTP, cloud APIs, and clocks; never mock the pure function or internal class under test.

## 4. Untracked / Gitignored Dependencies & Cross-Package Locks
- **Gating Tests That Import Gitignored Trees**:
  - A module-level `pytestmark = pytest.mark.skipif(...)` runs *after* top-level `import` statements, so missing gitignored modules fail during collection.
  - Gate optional/gitignored imports inside `conftest.py` using `collect_ignore = [...]` (and print a notice to `sys.stderr`), and convert fixture file checks (`assert DATA.is_file()`) to `pytest.skip(f"missing {DATA}")`.
  - Verify both the populated working copy and a clean `git archive HEAD` extraction when untracking files.
- **Cross-Package Lock Placement**:
  - Place characterization lock tests inside the package that **owns** the symbol under test; a lower-layer library must never import a higher-layer consumer package solely to run tests.

## 5. Bug-Fixing Loop
1. **Discover the runner** from the repo config (`pyproject.toml`, `package.json`, `Makefile`). Do not assume `pytest` when another command is the project runner.
2. **Prove-It.** Commit the minimal failing test before the fix (`RED`).
3. **Isolate** the root cause. If it is not local, hand off to **debugging-and-error-recovery**.
4. **Fix** the code with the smallest clean diff (`GREEN`).
5. **Guard** by keeping the regression test in the suite.
6. After a clean pass and no code change, do not run the same command again. Reuse that proof.

## Final Checklist
- [ ] Tests assert public behavior and contracts, not private internals
- [ ] Targeted suite passes under `PYTHONHASHSEED=random` and `-n 4`
- [ ] Strict markers and config enabled in `pyproject.toml`
- [ ] External boundaries mocked cleanly; zero `sleep`-based flaky waits
- [ ] Optional/gitignored datasets skip cleanly via `conftest.py` or `pytest.skip`
