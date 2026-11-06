# Refactor Blueprint

Load this reference after clustering harvest alerts. Produce a table. Do not edit code unless the user asked.

## Canonical lexicon

| Legacy symbol | File | Canonical symbol | File | Dimension | Action |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `is_done` | `mod.py` | `Status.DONE` | `status.py` | variable/variable | Replace flag with Enum |

One bounded context per table. Stop after one context unless the user asked for more.

## Handoffs

1. Lock inputs and outputs with tests before any edit (`python-testing`).
2. If the canonical symbol is a public or facade name, migrate with `deprecation-migration`.
3. After callers point at the canonical symbol, local nesting cleanup is `code-simplification`.
4. If two live symbols both look canonical, lock the choice with `doubt-driven-development`.
5. Claimed hot-path cost needs a measured profile (`python-performance`). Do not invent latency numbers.
6. Merge through `code-review`. Stop with `verify-and-stop`.

## Greedy DRY

Identical lines in different bounded contexts with different reasons to change stay separate. That rule lives only in this skill.

## Deletion

Do not delete from the dead-code candidate list. Confirm public surface, dynamic invocation, reflection, and webhook entrypoints first. Enum replacements must keep external default values compatible.
