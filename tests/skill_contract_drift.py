"""G15 skill-contract drift gate for the code-index skill (kg Amendment 12).

Renders ``kg --help`` and each subcommand's ``--help`` via the binary at
``$KG_BIN`` and asserts every subcommand and flag mentioned in backticked
spans of ``skills/code-index/SKILL.md`` exists in the binary's help output.

Skips (exit 0) when ``KG_BIN`` is unset: the agent-skills CI cannot build the
private kg repo, so enforcement is the owner's local pre-commit check when
editing the skill (kg repo spec, Amendment 12 / gate G15).
"""

from __future__ import annotations

import os
import re
import subprocess
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SKILL = REPO / "skills" / "code-index" / "SKILL.md"
BUDGET_BYTES = 3000
GLOBAL_FLAGS = {"--root", "--no-journal", "--help"}


def _fail(messages: list[str]) -> int:
    for message in messages:
        print(f"DRIFT: {message}")
    print(f"FAIL: {len(messages)} drift finding(s) in {SKILL}")
    return 1


def _help_of(kg: str, args: list[str], messages: list[str]) -> str:
    result = subprocess.run(
        [kg, *args, "--help"], capture_output=True, text=True, check=False
    )
    if result.returncode != 0:
        messages.append(f"'kg {' '.join(args)} --help' exited {result.returncode}")
        return ""
    return result.stdout


def main() -> int:
    if not SKILL.exists():
        return _fail([f"skill file not found: {SKILL}"])

    text = SKILL.read_text(encoding="utf-8")
    size = len(text.encode("utf-8"))
    if size > BUDGET_BYTES:
        return _fail([f"skill is {size} bytes > {BUDGET_BYTES} budget"])

    kg = os.environ.get("KG_BIN", "").strip()
    if not kg:
        print(
            "SKIP: KG_BIN not set — run locally with KG_BIN=<path-to-kg> "
            "python3 tests/skill_contract_drift.py"
        )
        return 0

    messages: list[str] = []
    top_help = _help_of(kg, [], messages)
    subcommands = set(re.findall(r"^  (\w[\w-]*)\s{2,}", top_help, re.M))

    for span in re.findall(r"`([^`]+)`", text):
        match = re.match(r"kg(?:\s+(\w[\w-]*))?", span.strip())
        if match is None:
            continue
        subcommand = match.group(1)
        flags = set(re.findall(r"(--\w[\w-]*)", span))
        if subcommand is None:
            unknown = flags - GLOBAL_FLAGS
            if unknown:
                messages.append(
                    f"flags {sorted(unknown)} used without a subcommand "
                    f"(global flags: {sorted(GLOBAL_FLAGS)})"
                )
            continue
        if subcommand not in subcommands:
            messages.append(f"subcommand '{subcommand}' not in 'kg --help'")
            continue
        sub_help = _help_of(kg, [subcommand], messages)
        unknown = flags - GLOBAL_FLAGS - set(re.findall(r"(--\w[\w-]*)", sub_help))
        if unknown:
            messages.append(
                f"flags {sorted(unknown)} not in 'kg {subcommand} --help'"
            )

    if messages:
        return _fail(messages)
    print(f"OK: {SKILL.name} ({size} bytes) matches 'kg --help' contract")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
