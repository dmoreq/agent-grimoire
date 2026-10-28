# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [2.3.0] - 2026-10-28

### Added
- `skills/python-patterns`: Added the functional core / imperative shell boundary, explicit batched hydration, and non-critical graceful degradation rules.
- `skills/python-pro`: Added public facade and private layout, keyword-only boundaries, init-time invariants, semantic naming (units, no stage reuse), and corrected Pydantic immutability guidance.
- `skills/python-testing`: Added Protocol-based in-memory fakes and invariant/resilience test requirements.
- `skills/rust-pro`: Clarified unit-bearing newtypes.
- `rules/AGENTS.md`: Added mandatory **Progress Visibility for Long Tasks** under §4 Safety & Workspace Hygiene. Requires scripts running >5 seconds or >100 iterations to output progress indicators (`tqdm` or structured interval logging with rate and completion estimates).
- `skills/python-pro`: Documented progress visibility and throttling standards for batch iterations and CLI scripts.
- `tests/test_invariants.py`: Added invariant test `test_progress_visibility_rule_invariants` asserting the presence of progress visibility clauses in `rules/AGENTS.md` and `skills/python-pro/SKILL.md`.
- `skills/spec-driven-design` (new): Two-gate spec workflow with multi-turn clarification, six parallel Goldfish brainstorm lenses, `FeatureRange`/`DetailedRange` drafting, and the Zero-Decision Rule.
- `skills/spec-driven-design/references/spec-templates-and-standards.md`: Six brainstorm lens prompt cards, host dispatch tiers, Heilmeier and feature-spec standards, implementation-readiness rules, CUJ format, and the ISO-dated spec template.
- `skills/codebase-contracts` (new): Peanuts/Hay directory README bootstrap with bounded read-only scouts, plus top-down spec and README drift audit.
- `skills/codebase-contracts/references/peanuts-and-hay-templates.md`: Contract templates, link rules, Re-Implementation Zero-Assumption standard, worker JSON schema, and six-vector drift report format.
- `skills/doubt-driven-development/references/goldfish-review-lenses.md`: Five self-contained review lens cards (Zoom-Out, Comprehension, Design Critic, Implementation Readiness, Codebase Details) with dispatch and reconciliation rules.
- `rules/AGENTS.md`: Added the **Checkable Contest Invariant** under §1 and **Architecture Ownership** plus **Contradiction Halt** under §2.
- `tests/test_invariants.py`: Added a 25-skill graph gate (`in_degree >= 2`, `out_degree >= 2`), README catalog coverage, ISO-dated artifact path checks, and a zero Claude/plugin escape-hatch assertion.
- `skills/code-review/references/goldfish-code-review-lenses.md`: Five orthogonal read-only code review personas (`cr-correctness-invariants`, `cr-mechanism-generalization`, `cr-codebase-reuse-and-contracts`, `cr-concurrency-memory-perf`, `cr-security-trust-boundary`) with risk routing, deterministic `git grep`/AST probes, and the checkable reconciliation template.
- `tests/test_invariants.py`: Added `test_code_review_goldfish_lenses_integrity` to lock the five persona IDs, required probe terms, and zero-emoji rule.
- `skills/html-report` (new): Single-file, self-contained HTML report skill with dual-theme tokens, print/PDF rules, client-side filtering, and a controlled Chart.js CDN exception.
- `skills/html-report/references/html-report-scaffold.md`: HTML skeleton, light/dark/manual CSS tokens, print styles, JS interaction patterns, and the offline self-check.
- `tests/test_invariants.py`: Added `test_html_report_skill_integrity` and extended ISO-date path checks to `html-report`.
- `skills/ux-product-shaper` (new): Surface Mode, information architecture, user flows, and the 8-state product brief.
- `skills/ux-product-shaper/references/product-and-state-contracts.md`: Surface Mode table, IA rules, 8-state matrix, and the `PRODUCT.md` template.
- `skills/design-system` (new): Three-tier W3C DTCG tokens, light/dark parity, component specs, responsive layout, and implementation handoff.
- `skills/design-system/references/token-and-component-specs.md`: Token tiers, naming, type/spacing/motion scales, component spec template, and handoff checklist.
- `skills/ui-accessibility` (new): WCAG 2.2 AA audit procedure, keyboard/focus model, ARIA failure patterns, and the audit report template.
- `skills/ui-accessibility/references/wcag-2-2-audit.md`: Checklist, optional Playwright/axe-core commands, severity, and gate rules.
- `skills/ux-critic` (new): Six-dimension heuristic critique, squint test, Nielsen's ten heuristics, and steering vocabulary.
- `skills/ux-critic/references/heuristic-critique.md`: Critique dimensions, severity, steering commands, and the report template.
- `tests/test_invariants.py`: Added `test_ui_ux_family_integrity` and extended ISO-date checks to the UI/UX family.

### Changed
- `skills/doubt-driven-development`: Upgraded from a single-artifact prompt to the five-lens Goldfish review with semantic split, isolated dispatch, consolidated report, and `PROPOSE FIX` / `CONTEST` / `ESCALATE` / `DECLINE` reconciliation.
- `skills/code-minimalism`: Added Anti-Weeds (Altitude Control) and an explicit Root Cause versus Local Band-Aid rule.
- `skills/tech-research`: Added the handoff boundary to `spec-driven-design` and `technical-reporting`.
- `skills/technical-reporting`: Added spec, drift-report, and decision-lock handoffs; related skills raised to six.
- `skills/code-review`: Added the `codebase-contracts` drift check for documented behavior, explicit async-Rust review handoff, risk-based Goldfish dispatch, and the multi-agent reconciliation verdict.
- `skills/technical-reporting`, `data-visualization`, `plotly-dash`, `data-storytelling`, `algorithm-optimization`, and `code-review`: Added `html-report` handoffs and resolved the Markdown/HTML, static/server, and chart/report boundaries.
- `rules/AGENTS.md` and `README.md`: Documented single-file HTML report ownership and routing.
- All 26 skills: Completed the bidirectional `## Related Skills` graph with at least two inbound and two outbound handoffs per skill.
- `README.md`: Added both new skills to the structure tree and catalog, extended the ownership map and relationship table, added the six-invariant spec gate, and raised the `code-review` reference count to three.
- `tests/test_skills_schema.py`: Removed the hardcoded skill count; the README catalog now defines the expected skill set.
- `setup.sh` and `README.md`: Made the 27-of-30 default explicit; the three Rust skills remain opt-in.
- `rules/AGENTS.md` and `README.md`: Added UI/UX ownership, relationship rows, flowchart nodes, and quick-router entries.
- `skills/spec-driven-design`, `html-report`, `plotly-dash`, `deprecation-migration`, `data-visualization`, `code-review`, and `doubt-driven-development`: Added reciprocal UI/UX handoffs.
- `skills/html-report`: Added a risk-based review gate; shared or print reports require `ui-accessibility`, and executive reports require `ux-critic` before `verify-and-stop`.
- `skills/ui-accessibility` and `skills/ux-critic`: Added reciprocal HTML report handoffs and explicit triggers for report review.
- `tests/test_invariants.py`: Extended `test_html_report_skill_integrity` to assert both report-review handoffs and the three review profiles.
- `skills/ux-product-shaper`, `design-system`, `ui-accessibility`, and `ux-critic`: Added Minimalism Art Style and YAGNI doctrine: Monochrome + 1 Accent, typography caps, token/prop diet, Rule of Three, subtraction pass, THE ONE DELETION, and the Lazy, Not Negligent boundary.
- `skills/html-report`: Consumes the minimalism/YAGNI doctrine from `design-system` and forbids unrequested navigation, search, filter, export, or account chrome.
- `rules/AGENTS.md` and `README.md`: Documented the UI minimalism/YAGNI ownership, catalog wording, and quick-router entries.
- `tests/test_invariants.py`: Extended the UI/UX family integrity test with minimalism/YAGNI markers.
- `tests/test_setup_script.sh`: Default install now asserts `ux-product-shaper` and `design-system`.
- `.github/workflows/ci.yml`: Added a CI workflow for pytest and the setup script tests.
- `.gitignore`: Ignored `.zcode/` session state.
- `skills/data-storytelling`, `data-visualization`, `design-system`, `html-report`, `technical-reporting`, `ux-critic`, and `ux-product-shaper`: Applied the Zen Minimalism upgrade (Kanso, Ma, Shibumi) with warm organic palettes, a unified 2-3 sentence paragraph budget, and three curated HTML report presets (`dossier`, `zen-garden`, `chronicle`).
- `skills/html-report/references/html-report-scaffold.md`: Rebuilt the scaffold around the three presets, dual-theme tokens, preset switcher, table filtering, print rules, and an offline self-check.
- `skills/ux-product-shaper/references/product-and-state-contracts.md`: Canonicalized Mode A/Mode B names and added the wording budget.
- `skills/ux-critic/references/heuristic-critique.md`: Documented all six critique dimensions, including YAGNI and signifier honesty.
- `skills/design-system/references/token-and-component-specs.md`: Replaced the cool slate primitive example with a warm stone ramp and declared `--bg-subtle`.

### Fixed
- `skills/html-report`: Restored project-token precedence, the `design-system` YAGNI item, the publish-confirmation rule, the decisive `verify-and-stop` check, and the accessibility/critique checklist gates.
- `skills/html-report`: Aligned preset dimensions with the scaffold (`960px`, `1020px`, `5.25rem`, `1220px`) and replaced the unresolved Chart.js SRI placeholder with a verified SHA-384.
- `skills/data-visualization` and `skills/html-report`: Raised the muted context series to at least 3:1 contrast on every preset surface (`#878079` light, `#746B62` dark).
- `skills/ux-product-shaper`: Resolved the 4-6 versus 4 navigation-cap contradiction by standardizing on 4 items.
- `skills/ux-critic`: Corrected the five-versus-six dimension count and added YAGNI to the report template.
- `skills/technical-reporting` and `skills/data-storytelling`: Unified paragraph budgets and restored the simple-delta and audience principles.
- `tests/test_invariants.py`: Added guards against preset-dimension drift, unresolved SRI placeholders, navigation-cap drift, and prose-budget drift.

### Removed
- Hermes host support: deleted `rules/hermes-preamble.md`, `bots/seven-bots/`, and `tests/verify-profiles.sh`; removed Hermes detection, SOUL composition, host routing, and summary output from `setup.sh`.
- Hermes references from the spec, plan, and code-review dispatch contracts; those skills now use native parallel subagents or a sequential cold read.
- Hermes entries from `README.md` and the active test suite. Historical release notes remain unchanged.

## [2.2.0] - 2026-10-25

### Added
- `rules/AGENTS.md`: Added mandatory **Subprocess & Memory Safety** rules under §4 Safety & Workspace Hygiene. Guards against out-of-memory (OOM) and machine freeze conditions via fail-fast small sampling (100–1,000 rows), line-by-line streaming/chunking, conservative concurrency bounds (`workers <= 4`), and strict execution timeouts.
- `setup.sh`: Added native ZCode Desktop support (`--host zcode`, `~/.zcode/AGENTS.md`, `~/.zcode/skills`).
- `tests/test_invariants.py`: Added automated AST complexity budget checks (`depth <= 3`) for all skill scripts, forbidden emoji/HTML tag detection across skills, and recursive internal reference validation.

### Changed & Hardened
- `skills/data-science/scripts/eda_profile.py`: Hardened bounded reading (stops scanning immediately once `--max-rows` is reached), flattened AST indentation nesting to `<= 2`, handled ragged CSV extra columns without crashing, and escaped pipe/newline characters in Markdown summary tables.
- `skills/verify-and-stop`: Replaced emoji bullets with standard Markdown formatting to enforce `rules/AGENTS.md` §1 (`Zero emojis`).
- `skills/code-minimalism`: Refactored to reference `rules/AGENTS.md` §2 directly and added concrete Anti-Bloat Heuristics table, eliminating micro-kernel rule restatement.
- `skills/code-review`: Fixed corrupted HTML tag and renumbered duplicate section numbers in `references/repo-snapshot-review.md`.
- `package.sh` & `.gitignore`: Cleaned stale zip archives before building, excluded `.ruff_cache/`, `.tmp/`, and `.scratch/` from distribution bundles, and added missing patterns to `.gitignore`.
- `setup.sh`: Extended OpenCode detection to check `~/.config/opencode` (XDG standard) and passed config paths to Python via `sys.argv` instead of inline string interpolation.

### Removed
- `setup.sh` & `README.md`: Safely deprecated and pruned discontinued coding agent host configurations and installation logic: Cursor, Windsurf, Claude Code, Pi Agent, DeepSeek Harness, and Eigent Desktop.

## [2.1.0] - 2026-10-24

### Added
- `setup.sh`: Native Zed Editor integration (`--host zed`) installing global rules to `~/.config/zed/AGENTS.md` and discovering portable skills in `~/.agents/skills`; safely preserves existing user commit message rules.
- `bots`: Added bounded role templates and shared bot contract for agentic teams.
- `algorithm-optimization`: Extracted `references/query-suggestion-experiments.md` for pre-submission autocomplete experiments, synthetic prefix cohorts, and independent scorer parity gates.
- `verify-and-stop`: Added `references/subagent-verification.md` for independent parent-agent verification of delegated multi-stage workflows.
- `tests/test_setup_script.sh`: Added automated host detection and dry-run target validation for Zed Editor.

### Optimized
- `code-review`: Extracted declarative skill-bundle review and scan scope verification into `references/repo-snapshot-review.md`.
- `skills`: Enforced Progressive Disclosure budget constraints (`<= 250` lines and `<= 12 KB`) across all skills including `algorithm-optimization`, `code-review`, and `verify-and-stop`.

## [2.0.0] - 2026-10-23

### Added
- `polars-duckdb`: Dedicated tabular data engineering skill with dataset-size engine routing (`<100 MB` Pandas 2.x PyArrow/CoW vs `100 MB–100 GB` Polars lazy API & DuckDB SQL), mandatory join-grain validation (`validate="m:1"`), and `references/pandas-to-polars-migration.md`.
- `data-science`: Deterministic CLI profiler `scripts/eda_profile.py` for CSV, TSV, JSONL, and Parquet files and `references/ab-testing-and-causal.md` covering Sample Ratio Mismatch (SRM) chi-square gates, CUPED variance reduction, and quasi-experimental causal inference.
- `code-minimalism`: Extracted `references/generalization-and-export-audits.md` for dialect-copy and vocabulary export consolidation audits.
- `deprecation-migration`: Extracted `references/dead-code-and-untracking-audits.md` for runtime dead-code probes and `git archive HEAD` untracking verification.
- `package.sh`: Added `.zip` distribution archive generation (`dist/skills.zip` and `dist/agent-skills.zip`) alongside `.tar.gz` bundles.

### Optimized
- `data-science`: Upgraded with leakage-free `Pipeline`/`ColumnTransformer` rules, structure-matched cross-validation (`StratifiedKFold`, `GroupKFold`, `TimeSeriesSplit`), baselines-first modeling ladder, probability calibration, and slice evaluation; removed duplicated search-ranking replay prose.
- `data-visualization`: Added Form-Before-Library gate, Okabe-Ito colorblind-safe categorical palette defaults, semantic color rules (categorical, sequential, diverging, highlight), and cross-chart color consistency invariants.
- `algorithm-optimization`, `code-minimalism`, `deprecation-migration`, `python-pro`, `python-concurrency`: Enforced strict Progressive Disclosure (`<= 250` lines and `<= 12 KB` per `SKILL.md`), purging session-specific literals while preserving domain playbooks in `references/`.
- `python-performance` & `python-testing`: Standardized `resources/implementation-playbook.md` into `references/implementation-playbook.md` across all skills.
- `tests/test_invariants.py` & `tests/test_skills_schema.py`: Fixed hardcoded skill-tuple blind spot in `test_cross_skill_references_exist`, added file-existence verification for all `references/` and `scripts/` paths, and enforced Progressive Disclosure line/byte caps for the 23-skill catalog.

## [1.5.0] - 2026-10-16

### Optimized
- `rules/AGENTS.md`: Mandatory targeted test execution (`pytest <file> -k <test>`, `cargo test <test>`), prohibiting full-suite repetition during incremental edits.
- `rules/AGENTS.md` & `code-review`: Verification deduplication invariant reusing prior passing test/lint outputs instead of re-running identical suites.
- `code-review`: Scoped pre-flight quality gate to changed files (`pre-commit run --files <changed_files>`) and targeted tests; skipped completely for non-executable diffs.
- `python-pro`: Gated full pre-commit execution (`--all-files`) strictly to one-time repository bootstrapping; switched Makefile `pre-commit-run` to target git diff modified files.
- `verify-and-stop`: Enabled immediate proof reuse from preceding step, preventing redundant post-review test executions.
- `python-testing` & `code-simplification`: Confined flaky-test (`PYTHONHASHSEED=random`) and refactoring test passes strictly to modified modules.
- `rules/AGENTS.md` & `python-testing`: Prioritized 4 parallel workers (`pytest -n 4` via `pytest-xdist`) across global rules and Python skills to accelerate test runs.

### Added
- `setup.sh`: Hermes host writes `~/.hermes/SOUL.md` from `rules/hermes-preamble.md` plus `rules/AGENTS.md`. It does not copy skills into `~/.hermes/skills`.
- `setup.sh`: DeepSeek Harness host integration installing global rules (`$DSH_HOME/AGENTS.md`, default `~/.dsh/AGENTS.md`) and native skills (`~/.dsh/skills`); detects `$DSH_HOME`, the macOS app bundle, or a `dsh` CLI on `PATH`.
- `setup.sh`: OpenAI Codex Desktop and CLI host integration installing global rules (`~/.codex/AGENTS.md`) and discovering skills (`~/.agents/skills` / `~/.codex/skills`).
- `code-review`: Automated quality pre-flight gate running targeted `pre-commit` and tests before semantic review.
- `code-review`: Reviewability budget (diff <= 400 LOC) and blast radius public surface gates.
- `code-review`: Omission checklist (resource cleanup in error paths, observability/logging, negative/edge tests, docs synchronization).
- `code-review`: Performance & Concurrency review gate guarding shared mutable state across async tasks and worker threads.
- `code-review`: Mandatory drop-in code fix diff and failure scenario for all Critical and Important findings.
- `python-testing`: Property-based testing with `hypothesis` for invariant and parser verification.
- `python-testing`: Determinism and flaky-test guards (`PYTHONHASHSEED=random`, `time-machine` for time freezing).
- `python-testing`: Strict pytest configuration (`addopts = "--strict-markers --strict-config -ra"`).
- `python-pro`: PEP 561 `py.typed` packaging invariant for typed Python libraries.
- `python-pro`: PEP 695 native type aliases (`type`) and generic functions (`def fn[T]()`).
- `python-pro`: Boundary distinction between Pydantic v2 (external I/O) and `@dataclass(slots=True)` (internal hot loops).
- `python-concurrency`: Modern `asyncio.TaskGroup` structured concurrency with `except*` composite exception handling (PEP 654).
- `python-concurrency`: Cancellation hygiene prohibiting swallowing `asyncio.CancelledError`, and `asyncio.shield()` for critical cleanup.
- `python-patterns`: Standard `src/` layout recommendation for production Python libraries.
- `python-patterns`: Three-Tier Model separation (Domain `dataclass(slots=True)` vs API Pydantic vs Persistence Entity).
- `python-patterns`: Boundary configuration pattern using `pydantic-settings`.
- `python-performance`: SOTA memory profiler `memray` (Bloomberg) tracking native C and Python heap allocations.
- `python-performance`: Drop-in SIMD and C-extension accelerator catalog (`orjson`, `stringzilla`, `rapidfuzz`, `polars`).
- `python-performance`: Zero-copy buffer slicing via `memoryview`.
- `pyo3-maturin`: PyO3 0.21+ `Bound<'py, T>` smart pointer idioms enforcing compile-time GIL lifetime checks.
- `pyo3-maturin`: Zero-copy memory buffer exchange via Python buffer protocol (`PyBuffer`) and `numpy` array slices.
- `pyo3-maturin`: Native Polars expression plugin pattern via `pyo3-polars`.

## [1.4.0] - 2026-10-03

### Added
- `python-pro`: Canonical `.pre-commit-config.yaml` template with Ruff, Pyright, Bandit, Complexipy ratchet, Vulture, and Pip-audit.
- `python-pro` & `code-review`: Automated code clone and duplication detection via `jscpd` (target threshold <= 3%).
- `python-pro`: Standard Makefile targets (`pre-commit-install`, `pre-commit-run`, `duplication-check`).

## [1.3.0] - 2026-10-02

### Added
- `rules/AGENTS.md`: Quantitative structural complexity thresholds (Nesting Depth <= 3, Cyclomatic Complexity <= 10, Cognitive Complexity <= 15, Function Length <= 50 LOC).
- `code-simplification`: Refactoring recipes for complexity (Invert & Guard, Dispatch Table, Pipeline and Decomposition).
- `code-review`: Complexity review gates (Important for CC > 10, Critical for CC > 20).
- `python-pro`: Ruff complexity rules (`C901`, `PLR0912`, `PLR0915`).
- `rust-pro`: Clippy cognitive complexity thresholds.

## [1.2.0] - 2026-09-23

### Added
- `rules/AGENTS.md`: Micro-kernel rule architecture with YAGNI code generation ladder.
- `verify-and-stop`: Disciplined execution and termination protocol preventing runaway loops.
- `setup.sh`: Selective Rust installation (`--with-rust` flag, skipping Rust skills by default).

## [1.1.0] - 2026-09-15

### Added
- `rules/AGENTS.md`: Subagent parallel planning and independent peer-review protocol.
- `rules/AGENTS.md`: Simplified Technical English (ASD-STE100) and token discipline standards.

## [1.0.0] - 2026-09-14

### Added
- Initial portable multi-agent customization suite (`setup.sh`, `package.sh`).
- Portable `~/.agents/skills` architecture shared across Antigravity, Cursor, Pi, and Grok.
- 16 core skills for Python, Rust, data science, visualization, and code review.
