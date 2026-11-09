---
name: verify-and-stop
description: >-
  Disciplined execution and termination protocol. Verifies minimal acceptance criteria
  with a single decisive check, presents proof, and stops immediately without runaway loops.
risk: safe
source: local
date_added: "2026-09-22"
---

# Verify-and-Stop Skill

Enforces strict termination discipline for coding agents. Complete the requested task, verify the acceptance criteria with a decisive command, present the proof, and stop. Never continue into unprompted refactoring, speculative cleanup, or endless loop cycles.

- Load `references/subagent-verification.md` when coordinating multi-stage delegated agent workflows or reviewing parent/child verification chains.

## When to Use
- Implementation or fix is complete and requires definitive validation
- Guarding against agent runaways, over-refactoring, or perpetual tool calls
- Finishing a subagent delegation stream cleanly

## When Not to Use
- Active debugging when the cause of a test failure is not yet identified
- Initial design or research phases where code has not been written

## The 4-Step Termination Protocol

1. **Check Acceptance Criteria**:
   Compare the current state strictly against what was requested. Ask: did we satisfy the exact prompt contract?
2. **Execute One Decisive Verification (or Reuse Prior Proof)**:
   - **Reuse Prior Proof**: If the immediately preceding step or tool call already executed a verification command that proved correctness with clean passing output, **do NOT re-run it**. Reuse that output as proof.
   - Otherwise, run the smallest runnable command that proves correctness:
     - Python: `pytest -n 4 path/to/test.py -k test_name`
     - Rust: `cargo test test_name`
     - Build / Lint: targeted linter check (`ruff check <files>`). When deleting packaged modules, verify the built wheel/archive contents from a clean staging tree, not just the build exit code: cached `build/bdist` files can ship deleted modules. Smoke-import the clean artifact outside the source checkout.
     - Installers: run against isolated `HOME` and project working directories. Count installed entries, rerun for idempotence, and assert a conflicting pre-existing entry remains unchanged after rejection. This proves filesystem behavior without mutating the user's real installation; report CLI discovery separately if the CLI was not exercised.
3. **Present Decisive Proof**:
   Output the result concisely:
   - Status (PASS / FAIL)
   - Scope touched (files and delta LOC)
   - Verification evidence (command output or reused proof from immediate prior step)
   - Zero speculative commentary

   **A background run is not a reusable proof.** When a test command was launched with `background=true` and its completion arrives later, its output describes the tree at launch time. If you edited files after launching it, reconcile before reporting: re-run the suite in the foreground against the current tree, or state plainly that the result is stale and what changed since. Do not present a delayed green or red as the state of the code — a stale red in particular invites debugging a failure you already fixed. If a final full suite fails only on changed-contract fixtures, audit every changed snapshot for ID removal, added rows, and shared-score drift before regenerating it. Run the affected modules after updating fixtures; report the original full-suite failure and targeted repair honestly, not as a full-suite pass.
4. **STOP**:
   Call no more tools. Do not initiate drive-by refactoring, extra cleanup, or tangential improvements. State completion directly.

## Git Branch and Commit Verification

When a task includes branch creation, rebasing, conflict resolution, or a commit, verify those outcomes explicitly before stopping:
1. Inspect `git status --short --branch` before changing branches. Preserve existing edits and leave unrelated untracked files unstaged.
2. Identify the intended rebase target from the requested integration target (usually the repository's default branch for a new feature branch), not just the feature branch's tracking configuration. Fetch that target and confirm its remote-tracking ref is current.
3. Rebase onto the confirmed integration target. If the user asks to catch up a branch for an MR and no target is specified, inspect the repository's default branch and MR context; use that base rather than the source branch's own remote ref. Ask only when the target remains ambiguous.
4. For dirty worktrees, preserve tracked edits before rebasing. Resolve conflicts by combining the intended feature change with upstream content, not by choosing an entire side blindly. After resolving an autostash conflict, confirm the stash-applied feature edits are present before committing.
5. Verify `git status --short --branch`, `git show --stat --oneline HEAD`, `git show --check HEAD`, and the commit count against the chosen base.
6. If the rebased branch was already pushed, update it with `git push --force-with-lease <remote> <branch>`, never plain force. Confirm the remote branch points to the rebased commit and the local branch is no longer behind its remote.
7. When splitting a finished change into several conventional commits under a pre-commit hook suite: format the full set first; stage and commit only slices that leave the tree importable and typecheck-clean on their own (re-export removal + consumer retarget = one commit). Commit each git root separately. Leave handoff-listed unrelated dirty paths unstaged. If a hook rewrites files and rolls back, re-stage the rewritten content and retry that slice once — do not `--no-verify`.

Keep existing untracked files untouched and out of the commit unless the user explicitly includes them.

## Anti-Patterns
- Reporting a number, then discovering the harness was wrong, then reporting a fresh number, then discovering the metric definition was wrong — across successive turns. Two mid-series corrections on the same claim means the measurement protocol is unvalidated, not that the third number is the good one. Stop publishing deltas; validate the harness against a known-good figure and fix the metric definition first, then report once.
- Reusing an assumption that a prior turn already falsified. If `prod_ids` was shown to mix two id sources, do not later reason "ids in `prod_ids` are children". Carry the correction forward explicitly, or the next measurement inherits the same defect and produces the same retracted result.
- Continuing to edit unrelated files after the requested test passes.
- Running multiple redundant test commands that check the same thing.
- Re-running tests or pre-commit when the previous step already verified the exact same code with passing output.
- Running full repository test suites or `pre-commit run --all-files` when targeted checks suffice.
- Asking the user "Would you like me to also refactor X, Y, and Z?" when not requested.
- Treating a delayed background test result as proof of the current tree. Launch a background suite only for work you will not edit while it runs; otherwise run it in the foreground.
- Re-answering a replayed background job completion that was already processed.
- Re-running a long measurement because a delayed notification showed an older configuration's numbers.
- Reporting a suite as green from the working copy when changed code was not yet committed (`git archive HEAD` probe).
- Running `pytest` with a shell whose `PYTHONPATH`/`PYTHONHOME` leaked from an external toolchain.
- Writing heredocs to filesystem root paths (`cat > /probe.py`). Anchor scratch scripts under `.scratch/` or conversation scratch dirs.
- Accepting a subagent's self-reported acceptance table as proof without independently re-running cheap invariant checks.
- Publishing metrics from a derived artifact whose regeneration has not been proven reproducible. Hash the artifact, regenerate from the same inputs in the same process, and require an identical digest before quoting any accuracy number. A miner reading a `defaultdict` or a persisted file can yield a different key population on the next run, which silently redefines every denominator downstream.
- Looping on an operation that is structurally blocked by the state it is running in, and retrying variations hoping the guard stops firing. A restart issued from inside the process being restarted will never complete — the drain waits on the turn that issued it. Two refusals with the SAME reason is a wall, not a flaky check: stop, name the deadlock in one sentence, and hand the command to the user to run in their own shell. Changing `restart` → `restart --yes` → `launchctl` → a detached wrapper is a loop wearing different commands.
- Reporting a background run as a failure because your `terminal` call hit its own timeout. The child process keeps working after the wait expires; read its session store (`sqlite3 <profile>/state.db "SELECT message_count, tool_call_count ..."`) or its output file before concluding anything. The correct finding may be "still running, 12 tool calls in, behaving correctly" — which is a result, not a retry prompt.
- Leaving the shell in a directory you then delete. Every later `cd` in that session fails with `getcwd: cannot access parent directories`. Run scratch work under a directory you keep, and if the shell is already wedged, recover by passing an explicit `workdir` rather than chaining `cd`.

## Verifying Subagent Chains
- When a task runs across implement → review → fix cycles, the parent agent owns the official record and must run acceptance checks independently (`references/subagent-verification.md`).
- Pass the reviewer the exact revision you will ship, compare verdict commit SHAs against HEAD, and confirm arrival before acting.

## Related Skills
- Use **python-testing** to write or debug targeted test assertions.
- Use **code-review** for pre-merge multi-axis inspection.
- Use **precommit-initialization** to configure targeted git hook gates.
- Use **code-minimalism** to ensure the verified solution remains minimal.
