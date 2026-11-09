---
name: python-pro
description: >-
  Implement or modernize Python modules with typing, uv, ruff, pyright, and pyproject.toml.
  Not for framework choice, concurrency model, runtime profiling, or PR review.
risk: safe
source: local
date_added: "2026-02-27"
---

# Modern Python Skill

Write clean, typed, idiomatic Python. Prefer Python 3.12+ when the runtime allows.

Load `references/standalone-distribution.md` when packaging a library into a standalone wheel/sdist, auditing `pyproject.toml` dependencies, or adapting domain schemas across package boundaries.

## When to Use
- Writing or modernizing Python modules and packages
- Setting up a Python project (`uv`, `ruff`, `pyright`, `pyproject.toml`, `.pre-commit-config.yaml`)
- Implementing production libraries, APIs, CLI tools, or data models

## When Not to Use
- Choosing FastAPI vs Django vs project layout (`python-patterns`)
- Choosing asyncio vs threads vs processes (`python-concurrency`)
- Profiling latency/CPU/memory (`python-performance`)
- Tabular Polars/DuckDB data wrangling (`polars-duckdb`)
- Reviewing a diff (`code-review`)

## Related Skills
- Use **python-patterns** when architecture (framework/layout/ADR) is still open.
- Use **context7-mcp** when a library or framework API is version-sensitive.
- Use **python-testing** to protect behavior with targeted `pytest` suites.
- Use **precommit-initialization** to install and configure pre-commit hooks and Ruff/Bandit verification gates.
- Before merge: **code-review**.
- Use **verify-and-stop** to confirm the decisive check and terminate cleanly.

## 1. Version Handling
Confirm the target Python version from `pyproject.toml` or `.python-version` first:
- **Python 3.12+ (Preferred)**: Use PEP 695 `type Alias = ...` statements, native generic syntax `def first[T](items: list[T]) -> T:`, and `@override` (`from typing import override`).
- **Python 3.10–3.11**: Use `X | Y` unions, builtin generic types (`list[str]`, `dict[str, Any]`), and `typing_extensions` (`Self`, `Protocol`, `ParamSpec`, `TypeGuard`) where supported.
- **Python <= 3.9**: Legacy maintenance only; keep changes minimal.

## 2. Core Engineering Principles
- **Model Boundary Separation**:
  - **Untrusted I/O Boundaries** (HTTP payloads, CLI args, external configs): Use Pydantic v2 (`model_validate`, `model_dump(mode="json")`, `by_alias=True`). Distinguish confirmed empty config (`[]`) from unavailable/unreadable config (`None` or explicit error).
  - **Internal Domain Logic & Hot Loops**: Use `@dataclass(slots=True)` (or `frozen=True, slots=True`) for 5x–10x faster instantiation and 60% lower RAM.
- **Explicit Public Surface & Typing**:
  - Declare `__all__` explicitly in public modules; prefix internal helpers with `_`.
  - Include a PEP 561 `py.typed` marker file in every typed library package.
  - Re-export `Final` constants with `from module import NAME` (never `NAME as NAME`, which Pyright flags as a `Final` reassignment).
  - Prefer `typing.Protocol` (structural subtyping) over deep `abc.ABC` inheritance hierarchies.
- **Zero Import-Time Side Effects**: Never execute network I/O, database connections, or heavy file loads at module import time.
- **Long-Running Iterations & Progress Visibility**: Add `tqdm` or structured logging with elapsed time, processed counts, and rates for loops and batch jobs exceeding 5 seconds (or >100 iterations). Throttle update intervals to avoid stdout flooding.
- **Standalone Packaging Hygiene**: Never read checkout-relative paths (`Path(__file__).parents[N] / "data"`) at runtime in a distributable package; restrict `package-data` to explicit extensions and verify built wheels in a clean venv (`references/standalone-distribution.md`).

## 3. Recommended Tooling & Quality Thresholds
- **Environment & Packaging**: `uv` + `pyproject.toml`
- **Lint & Format**: `ruff` (`C901` max-complexity = 10, `PLR0912` max-branches = 12, `PLR0915` max-statements = 50)
- **Cognitive Complexity**: `complexipy` (`<= 15` per function)
- **Code Duplication**: `jscpd` (`<= 3%` clone threshold, min-lines = 15, min-tokens = 60)
- **Type Checking**: `pyright` (or `mypy`)
- **Tests**: `pytest -n 4` (`python-testing`)

## 4. Working Approach
1. Confirm Python version, runtime, and repository conventions.
2. Define module boundaries, `__all__`, and data contracts (`Pydantic` at boundaries, `@dataclass(slots=True)` internally).
3. Implement with complete type annotations, explicit error handling, and complexity within caps (`CC <= 10`, `Cognitive <= 15`, `Nesting <= 3`).
4. Add targeted unit/property tests (`python-testing`).
5. Run fast targeted checks on modified files only: `ruff check <files>`, `pyright <files>`, `pytest -n 4 <test_file>`.
6. When a pre-commit hook rewrites a file (formatter or complexity snapshot), stage the updated file and re-commit cleanly without `--no-verify`.

## 5. Pre-commit & Repository Quality Gate Setup (Project Bootstrap Only)
Provision `.pre-commit-config.yaml` and `Makefile` targets **only** when initializing or modernizing repository infrastructure (never run `pre-commit run --all-files` during routine feature edits):

```yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.6.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
        exclude: ^complexipy-snapshot\.json$
      - id: check-yaml
      - id: check-toml
      - id: check-json
      - id: check-added-large-files
        args: ['--maxkb=4000']
      - id: check-merge-conflict
      - id: debug-statements
      - id: detect-private-key

  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.16.10
    hooks:
      - id: ruff-check
        args: [--fix, --exit-non-zero-on-fix]
      - id: ruff-format

  - repo: local
    hooks:
      - id: pyright
        name: pyright
        entry: pyright
        language: system
        types: [python]
        pass_filenames: false

  - repo: https://github.com/PyCQA/bandit
    rev: 1.7.10
    hooks:
      - id: bandit
        args: ["-c", "pyproject.toml"]
        additional_dependencies: ["bandit[toml]"]
        exclude: ^(tests/|eval/)

  - repo: https://github.com/rohaquinlop/complexipy-pre-commit
    rev: v8.0.1
    hooks:
      - id: complexipy
        args: [--max-complexity-allowed=15, <target_packages>]
        pass_filenames: false

  - repo: https://github.com/jendrikseipp/vulture
    rev: v2.16
    hooks:
      - id: vulture
        args: [--min-confidence=80, <target_packages>]
        pass_filenames: false

  - repo: https://github.com/kucherenko/jscpd
    rev: v5.4.0
    hooks:
      - id: jscpd
        args: ["--min-lines", "15", "--min-tokens", "60", "--threshold", "3", "--ignore", "tests/**,**/fixtures/**,**/*.json,**/*.xz"]
        pass_filenames: false
```

Standard `Makefile` targets:
```makefile
pre-commit-install:
	pre-commit install

pre-commit-run:
	pre-commit run --files $$(git diff --name-only HEAD)

pre-commit-all:
	pre-commit run --all-files  # One-time baseline / CI only
```

## Final Checklist
- [ ] Target Python version confirmed and modern syntax applied appropriately
- [ ] Pydantic v2 at I/O boundaries; `@dataclass(slots=True)` for internal models
- [ ] Public surface (`__all__`) and `py.typed` marker explicit; zero import-time I/O
- [ ] Complexity (`CC <= 10`, `Cognitive <= 15`, `Nesting <= 3`) and duplication (`<= 3%`) respected
- [ ] Targeted `ruff`, `pyright`, and `pytest -n 4` checks passing on modified files
