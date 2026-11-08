"""Regression tests for the code-smells scanner."""
from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

SCRIPT = (
    Path(__file__).resolve().parent.parent
    / "skills"
    / "code-smells"
    / "scripts"
    / "smell_scan.py"
)
SPEC = importlib.util.spec_from_file_location("smell_scan", SCRIPT)
assert SPEC and SPEC.loader
scanner = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = scanner
SPEC.loader.exec_module(scanner)


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _run(root: Path, out_dir: Path) -> dict:
    code = scanner.main([str(root), "--out-dir", str(out_dir)])
    assert code == 0
    return json.loads((out_dir / "smell_manifest.json").read_text(encoding="utf-8"))


def _smells(payload: dict) -> set[str]:
    return {row["smell"] for row in payload["findings"]}


def test_long_method_and_parameter_list(tmp_path: Path) -> None:
    body = "\n".join(f"    value_{index} = {index}" for index in range(60))
    params = ", ".join(f"p{index}" for index in range(5))
    _write(tmp_path / "long.py", f"def long_one():\n{body}\n\ndef wide({params}):\n    return p0\n")
    payload = _run(tmp_path, tmp_path / "out")
    assert "Long Method" in _smells(payload)
    assert "Long Parameter List" in _smells(payload)


def test_elif_chain_and_message_chain(tmp_path: Path) -> None:
    _write(
        tmp_path / "branch.py",
        "def choose(kind):\n"
        "    if kind == 'a':\n        return 1\n"
        "    elif kind == 'b':\n        return 2\n"
        "    elif kind == 'c':\n        return 3\n"
        "    elif kind == 'd':\n        return 4\n"
        "    elif kind == 'e':\n        return 5\n"
        "    return 0\n"
        "def chained(root):\n"
        "    return root.a.b.c\n",
    )
    payload = _run(tmp_path, tmp_path / "out")
    assert "Switch Statements" in _smells(payload)
    assert "Message Chains" in _smells(payload)


def test_data_clump(tmp_path: Path) -> None:
    header = "user_id, org_id, tenant_id"
    text = "\n".join(f"def use_{index}({header}):\n    return user_id\n" for index in range(3))
    _write(tmp_path / "clump.py", text)
    payload = _run(tmp_path, tmp_path / "out")
    assert "Data Clumps" in _smells(payload)


def test_feature_envy_and_temporary_field(tmp_path: Path) -> None:
    _write(
        tmp_path / "envy.py",
        "class Box:\n"
        "    def leak(self, order):\n"
        "        return order.total + order.tax + order.tip\n"
        "    def scratch(self):\n"
        "        self.temp = 1\n"
        "        return self.temp\n"
        "    def other(self):\n"
        "        return 1\n",
    )
    payload = _run(tmp_path, tmp_path / "out")
    assert "Feature Envy" in _smells(payload)
    assert "Temporary Field" in _smells(payload)


def test_summary_has_no_emoji_and_escape_fails(tmp_path: Path) -> None:
    _write(tmp_path / "ok.py", "def ping():\n    return 1\n")
    out_dir = tmp_path / "out"
    payload = _run(tmp_path, out_dir)
    assert payload["summary"]["functions"] == 1
    summary = (out_dir / "smell_summary.md").read_text(encoding="utf-8")
    for emoji in ("🚨", "✅", "⚠️"):
        assert emoji not in summary
    code = scanner.main(
        [str(tmp_path), "--out-dir", str(out_dir), "--output", str(tmp_path / "escaped.json")]
    )
    assert code == 2
