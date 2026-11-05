"""G15 skill-contract drift gate for code-index consumers (kg Amendment 12).

Checks every `kg` command in inline backticks and fenced code blocks of
`skills/*/SKILL.md` against the binary at `$KG_BIN`. Without `$KG_BIN`, it
validates against the checked-in `tests/kg_contract_manifest.txt` instead of
skipping, and it fails when a supplied binary disagrees with that manifest.
Consumer skills are scanned too, so a stale pointer in another skill fails the
gate.
"""

from __future__ import annotations

import os
import re
import subprocess
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SKILLS = REPO / "skills"
SKILL = SKILLS / "code-index" / "SKILL.md"
MANIFEST = REPO / "tests" / "kg_contract_manifest.txt"
BUDGET_BYTES = 3000
GLOBAL_FLAGS = {"--root", "--no-journal", "--help"}


def _fail(messages: list[str]) -> int:
    for message in messages:
        print(f"DRIFT: {message}")
    print(f"FAIL: {len(messages)} drift finding(s)")
    return 1


def _parse_manifest(path: Path) -> dict[str, set[str]]:
    contract: dict[str, set[str]] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        name, _, flags = line.partition(":")
        contract[name.strip()] = set(flags.split())
    return contract


def _dynamic_contract(kg: str, messages: list[str]) -> dict[str, set[str]]:
    top = subprocess.run([kg, "--help"], capture_output=True, text=True, check=False)
    if top.returncode != 0:
        messages.append(f"'kg --help' exited {top.returncode}")
        return {}
    subs = re.findall(r"^  (\w[\w-]*)\s{2,}", top.stdout, re.M)
    contract = {"global": set(GLOBAL_FLAGS)}
    for sub in [s for s in subs if s != "help"]:
        result = subprocess.run(
            [kg, sub, "--help"], capture_output=True, text=True, check=False
        )
        if result.returncode != 0:
            messages.append(f"'kg {sub} --help' exited {result.returncode}")
            continue
        contract[sub] = set(GLOBAL_FLAGS) | set(re.findall(r"(--[\w-]+)", result.stdout))
    return contract


def _extract_commands(text: str) -> list[str]:
    commands = list(re.findall(r"`([^`]+)`", text))
    in_fence = False
    for raw in text.splitlines():
        line = raw.strip()
        if line.startswith("```"):
            in_fence = not in_fence
            continue
        if not in_fence:
            continue
        line = line.split("#", 1)[0].strip()
        if line.startswith("kg ") or line == "kg":
            commands.append(line)
    return commands


def _check_commands(
    path: Path, text: str, contract: dict[str, set[str]], messages: list[str]
) -> int:
    checked = 0
    for span in _extract_commands(text):
        span = span.strip()
        if " / " in span:  # compound examples are prose, not one invocation
            continue
        match = re.match(r"kg(?:\s+(\w[\w-]*))?", span)
        if match is None:
            continue
        checked += 1
        subcommand = match.group(1)
        flags = set(re.findall(r"(--\w[\w-]*)", span))
        if subcommand is None:
            unknown = flags - GLOBAL_FLAGS
            if unknown:
                messages.append(
                    f"{path.name}: flags {sorted(unknown)} used without a subcommand"
                )
            continue
        if subcommand not in contract:
            messages.append(f"{path.name}: subcommand '{subcommand}' not in contract")
            continue
        unknown = flags - contract[subcommand]
        if unknown:
            messages.append(
                f"{path.name}: flags {sorted(unknown)} not in 'kg {subcommand} --help'"
            )
    return checked


def main() -> int:
    if not SKILL.exists():
        return _fail([f"skill file not found: {SKILL}"])
    if not MANIFEST.exists():
        return _fail([f"manifest not found: {MANIFEST}"])

    text = SKILL.read_text(encoding="utf-8")
    size = len(text.encode("utf-8"))
    if size > BUDGET_BYTES:
        return _fail([f"{SKILL} is {size} bytes > {BUDGET_BYTES} budget"])

    messages: list[str] = []
    manifest = _parse_manifest(MANIFEST)
    kg = os.environ.get("KG_BIN", "").strip()
    if kg:
        contract = _dynamic_contract(kg, messages)
        if manifest != contract:
            only_manifest = sorted(set(manifest) - set(contract))
            only_binary = sorted(set(contract) - set(manifest))
            messages.append(
                "static manifest is stale: "
                f"manifest-only={only_manifest}, binary-only={only_binary}"
            )
        source = "kg --help"
    else:
        contract = manifest
        source = f"static manifest {MANIFEST.name}"

    checked = 0
    consumer_lines = 0
    for path in sorted(SKILLS.glob("*/SKILL.md")):
        body = path.read_text(encoding="utf-8")
        checked += _check_commands(path, body, contract, messages)
        if path != SKILL and "code-index" in body:
            consumer_lines += 1

    if messages:
        return _fail(messages)
    print(
        f"OK: {SKILL.name} ({size} bytes), {checked} command(s), "
        f"{consumer_lines} consumer skill(s), contract from {source}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
