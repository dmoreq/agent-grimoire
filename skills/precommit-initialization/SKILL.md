---
name: precommit-initialization
description: >-
  Initialize, standardize, and maintain pre-commit hooks, multi-stage pipelines
  (pre-commit, pre-push), and security hygiene gates across Python, Rust, and polyglot repositories.
risk: safe
date_added: "2026-11-09"
---

# Pre-Commit Initialization & Git Hook Discipline

Standardize Git hook pipelines to catch errors locally before they reach CI or pull requests. Enforce a two-stage architecture: fast formatters, linters, and hygiene checks on `pre-commit`, with full test suites or locked builds deferred to `pre-push`.

- Load `references/universal-stack.yaml` for language-agnostic file hygiene, secret scanning, and merge conflict checks.
- Load `references/python-stack.yaml` for modern Python projects using Ruff, Bandit, and `pyproject.toml` validation.
- Load `references/rust-stack.yaml` for Rust repositories with typos check, `cargo fmt`, Clippy, and pre-push test gates.
- Load `references/hygiene-gate-scripts.md` for reusable bash gate scripts (leakage detection, code smell thresholds, allowlists).

## When to Use
- Bootstrapping pre-commit hooks in a new or unconfigured repository.
- Standardizing disparate hook configs across Python, Rust, or polyglot codebases.
- Adding pre-push safety gates for slow test suites (`pytest`, `cargo test --locked`).
- Configuring security leakage gates (private paths, access keys, sensitive tokens).
- Automating git diff whitespace and formatting hygiene.

## When Not to Use
- Running full repository test suites or linters during minor feature edits (use targeted commands instead).
- Bypassing pre-commit checks with `git commit --no-verify` (fix the underlying violation).
- Writing framework-specific application logic or tests.

## Related Skills
- Use **python-pro** to configure Ruff, Pyright, and Python packaging standards enforced by pre-commit.
- Use **rust-pro** to configure Cargo formatting, Clippy rules, and Rust compiler invariants.
- Use **code-review** to inspect code diffs and audit pre-commit quality gates before merge.
- Use **verify-and-stop** to run targeted pre-commit checks on modified files and terminate cleanly.

## 1. Quickstart & Installation

Install `pre-commit` into the developer toolchain:

```bash
# Python / UV (Preferred)
uv tool install pre-commit
# or add to project dev dependencies
uv add --dev pre-commit

# Homebrew (macOS)
brew install pre-commit

# Python pip
pip install --user pre-commit
```

### Install Git Hook Handlers
Always install both `pre-commit` and `pre-push` hook stages:
```bash
pre-commit install --hook-type pre-commit --hook-type pre-push
```

Verify installed hooks in `.git/hooks/`:
```bash
ls -la .git/hooks/pre-commit .git/hooks/pre-push
```

## 2. Multi-Stage Pipeline Architecture

Split hooks across stages to maintain sub-second commit latency while preventing broken builds on push:

| Stage | Trigger | Latency Target | Permitted Operations |
|---|---|---|---|
| `pre-commit` | `git commit` | < 1 second | Whitespace, EOF, YAML/TOML/JSON syntax, merge conflict markers, secret detection, fast linter fixes (`ruff`, `cargo fmt`). |
| `pre-push` | `git push` | < 15 seconds | Integration tests (`pytest -n 4`, `cargo test --locked`), structural invariant checks, lockfile allowlists. |
| `manual` | On demand / CI | Unbounded | Deep static analysis, full security audits, benchmark baselines. |

## 3. Presets & Stack Configurations

Select the matching configuration template from `references/`:

### Universal Baseline (`references/universal-stack.yaml`)
Include these hooks in every project regardless of language:
1. `check-merge-conflict`: Blocks unresolved merge conflict markers.
2. `trailing-whitespace`: Trims trailing spaces (exclude docs and test fixtures).
3. `end-of-file-fixer`: Ensures files end in a newline.
4. `check-yaml` / `check-toml` / `check-json`: Validates configuration syntax.
5. `check-case-conflict`: Prevents case-sensitivity filesystem collisions.
6. `detect-private-key`: Blocks accidental commitment of RSA, SSH, or PEM private keys.
7. `mixed-line-ending`: Normalizes line endings to LF.

### Python Stack (`references/python-stack.yaml`)
1. **Ruff Linter & Formatter**: Replace flake8, black, isort, and autoflake:
   ```yaml
   - repo: https://github.com/astral-sh/ruff-pre-commit
     rev: v0.9.10
     hooks:
       - id: ruff
         args: [--fix, --exit-non-zero-on-fix]
       - id: ruff-format
   ```
2. **Bandit Security Audit**: Static AST vulnerability scanning.
3. **Pyproject Validation**: Validate `pyproject.toml` schema integrity with `validate-pyproject`.

### Rust Stack (`references/rust-stack.yaml`)
1. **Typos Spellcheck**: Fast source code spellchecking via `crate-ci/typos`.
2. **Cargo Fmt**: `cargo fmt --all -- --check`.
3. **Cargo Clippy**: `cargo clippy --all-targets -- -D warnings`.
4. **Pre-Push Gate**: `cargo test --locked` on `stages: [pre-push]`.

## 4. Local Custom Hygiene Gates

Add project-specific enforcement gates using `repo: local` in `.pre-commit-config.yaml`:

```yaml
- repo: local
  hooks:
    - id: git-diff-check
      name: git diff whitespace check
      entry: git diff --cached --check
      language: system
      pass_filenames: false
      always_run: true

    - id: hygiene-check
      name: private leakage and hygiene gate
      entry: bash tests/scripts/hygiene_check.sh
      language: system
      types: [text]
```

### Critical Gate Rules
- **Zero Private Path Leakage**: Fail if files contain `/Users/`, `/home/<user>/`, or user workspace paths.
- **Zero Token Leakage**: Scan for AWS keys (`AKIA...`), GitHub PATs (`ghp_...`), or Bearer tokens.
- **Structural Limits**: Reject source files exceeding hard LOC limits (e.g. > 500 lines).

## 5. Agent Execution Discipline

When working in an agent session, follow these strict execution rules:
- **Never Run Full Runs Unprompted**: Do not execute `pre-commit run --all-files` during normal tasks or feature edits. Full runs rewrite unrelated code and bloat diffs.
- **Run Targeted Checks Only**: Run `pre-commit run --files <changed_files>` targeting only modified files.
- **Prefer Fast Direct Linters**: Prefer running `ruff check <files>` directly for fast feedback loops during iteration.
- **Skip Non-Executable Diffs**: Skip running pre-commit when diffs only touch documentation, markdown files, or notes.
- **Handle Auto-Fixes**: If a hook formats a file, re-stage the modified file once: `git add <file>` and re-run.

## 6. Makefile & Build Integration

Provide standardized helper targets in project `Makefile`:

```makefile
pre-commit-install:
	pre-commit install --hook-type pre-commit --hook-type pre-push

pre-commit-run:
	pre-commit run --files $$(git diff --name-only --cached)
```

## 7. Maintenance & Updates

- **Update Hook Versions**: Run `pre-commit autoupdate` periodically to update repo revisions to current stable tags.
- **Clean Cache**: If hook environments become corrupted, run `pre-commit clean` and reinstall.
- **CI Sync**: Run `pre-commit/action` in GitHub Actions workflows to ensure identical enforcement on PRs.
