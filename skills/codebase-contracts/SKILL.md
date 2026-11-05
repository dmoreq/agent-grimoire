---
name: codebase-contracts
description: >-
  Generate and audit directory README contracts: Peanuts/Hay bootstrap from code,
  then drift detection between specs, READMEs, and the live codebase.
  Not for implementing features or reviewing pull request diffs.
risk: safe
source: local
date_added: "2026-10-28"
---

# Codebase Contracts Skill

Keep the written architecture and the running code in agreement. Use bottom-up generation to publish contracts, and top-down audit to find drift.

## When to Use
- A repository subtree has no README contracts, or existing ones are stale.
- A new contributor or agent needs interface, invariant, and side-effect facts per directory.
- A spec or README claims behavior that must be checked against the code.
- A migration or refactor needs proof that documented contracts still hold.

## When Not to Use
- Writing or refactoring functional code.
- Reviewing a pull request diff (`code-review`).
- Drafting a new feature spec (`spec-driven-design`).
- The documentation covers a single file with no directory boundary.

## Modes

| Mode | Direction | Primary Output |
| :--- | :--- | :--- |
| Bootstrap | Code to README | Peanuts component contracts and Hay blueprints |
| Drift audit | README or spec to code | Drift report with divergences only |

## Mode 1: Bootstrap (Peanuts and Hay)

Run `references/peanuts-and-hay-templates.md` for the templates and the worker schema.

### Step 1: Discover Verification Command
Read the root manifest and record `VerificationCommand`: `package.json` to `npm test`, `Cargo.toml` to `cargo test`, `go.mod` to `go test ./...`, `pyproject.toml` to `pytest`, `Makefile` to `make test`.

### Step 2: Scope the Tree
1. Walk breadth-first, one directory level at a time. Never run recursive `find` or `ls -R`.
2. Skip symbolic links, hidden directories, `node_modules`, virtual environments, `dist`, `build`, and patterns from `.gitignore` and `.egmignore`.
3. Keep manifests for verification lookup.
4. **Safety gate**: if discovered directories exceed 15, stop and ask the owner before continuing.
5. Prune bottom-up. Keep directories that contain source, schema, IDL, or infrastructure files. Drop test-only and non-code directories.

### Step 3: Choose Execution Strategy
- Five or fewer directories: process in the current thread.
- More than five: partition the tree into three to five subtrees and spawn one read-only worker per subtree. Requires owner approval from the safety gate.

### Step 4: Generate Contracts Bottom-Up
For each directory, in post-order:
1. Spawn a read-only scout. Cap reads at 50,000 bytes per directory and 300 lines per file. Ignore test files.
2. Read implementation and schema files first, then entry points, then remaining source.
3. Classify the directory:
   - Peanut: contains direct source files.
   - Hay: contains only child directories with code.
4. Write or update the contract. If the file exists, preserve developer notes and correct only the contract sections.
5. For a Hay directory, roll up child interface summaries and link only to child files that exist.

### Step 5: Verify
Read every created or modified contract. Confirm the Interface, Invariants, and Side Effects sections are populated, links resolve on disk, and the verification command matches the manifest.

## Mode 2: Drift Audit

Run the audit against a directory of specs or READMEs.

1. **List** every target document. Read each one for intent and named files, symbols, and endpoints.
2. **Locate** the source for each claim with `git grep` or a symbol probe. Ask the owner to add missing links when a claim cannot be located.
3. **Verify** against current code. Read the files; do not rely on memory.
4. **Classify** each divergence with the six vectors in the reference:
   - Missing behavior
   - Incomplete data model
   - Logic shortcut
   - Architectural divergence
   - Undocumented implemented behavior
   - Stale reference
5. **Report only divergences**. A clean document gets one line: `No drift detected`.
6. Write `docs/reports/YYYY-MM-DD_drift-report_<topic>.md`. Process documents sequentially to bound output. Topic slugs follow the artifact slug and containment rule in `rules/AGENTS.md` §4.

## Rules
- Documentation only. Never create, modify, or refactor functional source.
- Do not run `git add`, `git commit`, or any VCS mutation.
- A proposed file is not drift. Apply stale-reference checks only to items the document says exist now.
- A plan that lists files without Create, Modify, or Delete markers is one Major finding, not one finding per path.
- Bounded reads only. Stop a scout that exceeds the byte or line cap and mark the contract incomplete.

## Related Skills
- Use **spec-driven-design** to draft the spec that contracts should implement.
- Use **code-review** to inspect code diffs and verify that documented APIs exist.
- Use **doubt-driven-development** when contract drift challenges an approved design decision.
- Use **verify-and-stop** to run the decisive verification once and terminate.

## Final Checklist
- [ ] Verification command discovered from the root manifest
- [ ] Tree walked breadth-first without recursive search
- [ ] Safety gate honored above 15 directories
- [ ] Every contract has Interface, Invariants, and Side Effects
- [ ] Every relative link resolves on disk
- [ ] Drift report contains divergences only and uses an ISO-dated path
- [ ] No source code and no VCS mutation
