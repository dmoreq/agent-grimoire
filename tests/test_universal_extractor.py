"""Regression tests for the codebase-minimalism universal extractor."""
from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

import pytest

SCRIPT = (
    Path(__file__).resolve().parent.parent
    / "skills"
    / "codebase-minimalism"
    / "scripts"
    / "universal_extractor.py"
)
SPEC = importlib.util.spec_from_file_location("universal_extractor", SCRIPT)
assert SPEC and SPEC.loader
extractor = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = extractor
SPEC.loader.exec_module(extractor)


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _alert_types(payload: dict) -> list[str]:
    return [row["duplication_type"] for row in payload["alerts"]]


def _run(root: Path, out_dir: Path, extra: list[str] | None = None) -> dict:
    argv = [str(root), "--out-dir", str(out_dir), *(extra or [])]
    code = extractor.main(argv)
    assert code == 0
    return json.loads((out_dir / "universal_manifest.json").read_text(encoding="utf-8"))


def test_shadow_flag_vs_enum(tmp_path: Path) -> None:
    _write(
        tmp_path / "status.py",
        "from enum import Enum\n"
        "class Status(Enum):\n"
        "    DONE = 1\n"
        "    PENDING = 2\n"
        "\n"
        "def check_item(is_done: bool) -> None:\n"
        "    return None\n",
    )
    payload = _run(tmp_path, tmp_path / "out")
    assert "variable/variable" in _alert_types(payload)
    shadow = payload["alerts"][0]["shadow_entity"]
    assert "is_done" in shadow


def test_function_function_across_files(tmp_path: Path) -> None:
    _write(tmp_path / "a.py", "def validate_email_address(value: str) -> str:\n    return value\n")
    _write(tmp_path / "b.py", "def validate_email_format(value: str) -> str:\n    return value\n")
    payload = _run(tmp_path, tmp_path / "out")
    assert "function/function" in _alert_types(payload)


def test_same_file_helpers_are_not_function_duplicates(tmp_path: Path) -> None:
    _write(
        tmp_path / "same.py",
        "def validate_email_address(value: str) -> str:\n    return value\n"
        "def validate_email_format(value: str) -> str:\n    return value\n",
    )
    payload = _run(tmp_path, tmp_path / "out")
    assert "function/function" not in _alert_types(payload)


def test_type_type_dto_clone(tmp_path: Path) -> None:
    _write(tmp_path / "models.py", "class UserProfile:\n    name: str\n")
    _write(tmp_path / "dto.py", "class UserProfileDto:\n    name: str\n")
    payload = _run(tmp_path, tmp_path / "out")
    assert "type/type" in _alert_types(payload)


def test_wrapper_candidate(tmp_path: Path) -> None:
    _write(
        tmp_path / "wrap.py",
        "def inner(x: int) -> int:\n    return x\n"
        "def outer(x: int) -> int:\n    return inner(x)\n",
    )
    payload = _run(tmp_path, tmp_path / "out")
    names = [row["function"] for row in payload["redundant_wrappers"]]
    assert "outer" in names


def test_dead_code_skips_private_and_routes(tmp_path: Path) -> None:
    _write(
        tmp_path / "dead.py",
        "def unused_helper() -> int:\n    return 1\n"
        "def _private() -> int:\n    return 2\n"
        "def handler() -> int:\n    return 3\n"
        "def app_get() -> None:\n    return None\n"
        "app_get = app_get\n",
    )
    _write(
        tmp_path / "routes.py",
        "def get(path):\n    def deco(fn):\n        return fn\n    return deco\n"
        "class App:\n    get = staticmethod(get)\n"
        "app = App()\n"
        "@app.get('/x')\n"
        "def live_route() -> str:\n    return 'ok'\n",
    )
    payload = _run(tmp_path, tmp_path / "out")
    dead_names = {row["name"] for row in payload["dead_code_candidates"]}
    assert "unused_helper" in dead_names
    assert "_private" not in dead_names
    assert "handler" not in dead_names
    assert "live_route" not in dead_names


def test_function_module_raw_http_with_client(tmp_path: Path) -> None:
    _write(
        tmp_path / "client.py",
        "class ApiClient:\n    def fetch(self) -> None:\n        return None\n",
    )
    _write(
        tmp_path / "bypass.py",
        "import requests\n"
        "def load_remote() -> None:\n"
        "    requests.post('https://example.invalid')\n",
    )
    payload = _run(tmp_path, tmp_path / "out")
    assert "function/module" in _alert_types(payload)


def test_cli_omits_symbols_until_flag(tmp_path: Path) -> None:
    _write(tmp_path / "mod.py", "def ping() -> str:\n    return 'pong'\n")
    out_dir = tmp_path / "out"
    payload = _run(tmp_path, out_dir)
    assert "symbols" not in payload
    summary = (out_dir / "universal_summary.md").read_text(encoding="utf-8")
    for emoji in ("🚨", "🔄", "⚰️", "❌", "✅", "⚠️", "🚀"):
        assert emoji not in summary
    full = _run(tmp_path, tmp_path / "full", ["--full-symbols"])
    assert "symbols" in full


def test_skips_files_over_size_cap(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(extractor, "MAX_FILE_BYTES", 8)
    big = tmp_path / "big.py"
    _write(big, "def huge_helper_name() -> int:\n    return 1\n")
    assert big.stat().st_size > 8
    payload = _run(tmp_path, tmp_path / "out")
    assert payload["summary"]["total_functions"] == 0


def test_missing_root_exits_one(tmp_path: Path) -> None:
    code = extractor.main([str(tmp_path / "missing"), "--out-dir", str(tmp_path / "out")])
    assert code == 1


def test_screaming_snake_constant_overlaps_calculator(tmp_path: Path) -> None:
    _write(
        tmp_path / "retry.py",
        "MAX_RETRY_COUNT = 3\n"
        "ISSUE_REPORT_ID = 'x'\n"
        "def get_max_retry_count() -> int:\n    return MAX_RETRY_COUNT\n"
        "def issue_report() -> str:\n    return ISSUE_REPORT_ID\n",
    )
    payload = _run(tmp_path, tmp_path / "out")
    pairs = {(row["primary_entity"], row["shadow_entity"]) for row in payload["alerts"] if row["duplication_type"] == "function/variable"}
    assert any("MAX_RETRY_COUNT" in primary and "get_max_retry_count" in shadow for primary, shadow in pairs)
    assert not any("issue_report" in shadow for _, shadow in pairs)


def test_dead_code_module_self_and_attr_calls(tmp_path: Path) -> None:
    _write(
        tmp_path / "boot.py",
        "def bootstrap() -> None:\n    return None\n"
        "def unused_recursive(n: int) -> int:\n    return unused_recursive(n - 1)\n"
        "def save() -> None:\n    return None\n"
        "def persist() -> None:\n    db.save()\n"
        "bootstrap()\n"
        "if __name__ == '__main__':\n    build_app()\n"
        "def build_app() -> None:\n    return None\n",
    )
    payload = _run(tmp_path, tmp_path / "out")
    dead_names = {row["name"] for row in payload["dead_code_candidates"]}
    assert "bootstrap" not in dead_names
    assert "build_app" not in dead_names
    assert "unused_recursive" in dead_names
    assert "save" in dead_names


def test_dead_code_does_not_skip_computed_field(tmp_path: Path) -> None:
    _write(
        tmp_path / "fields.py",
        "def computed_field(fn):\n    return fn\n"
        "def singledispatch(fn):\n    return fn\n"
        "@computed_field\n"
        "def output() -> int:\n    return 1\n"
        "@singledispatch\n"
        "def dispatch(x: int) -> int:\n    return x\n",
    )
    payload = _run(tmp_path, tmp_path / "out")
    dead_names = {row["name"] for row in payload["dead_code_candidates"]}
    assert "output" in dead_names
    assert "dispatch" in dead_names


def test_typescript_type_alias_is_not_enum(tmp_path: Path) -> None:
    _write(
        tmp_path / "alias.ts",
        "export type TaskState = { done: boolean }\n"
        "export function checkItem(isDone: boolean) { return isDone }\n",
    )
    payload = _run(tmp_path, tmp_path / "out")
    assert "variable/variable" not in _alert_types(payload)


def test_typescript_enum_still_flags_boolean(tmp_path: Path) -> None:
    _write(
        tmp_path / "state.ts",
        "export enum TaskState { Done, Pending }\n"
        "export function checkItem(isDone: boolean) { return isDone }\n",
    )
    payload = _run(tmp_path, tmp_path / "out")
    assert "variable/variable" in _alert_types(payload)


def test_python_flag_is_enum_enumeration_is_not(tmp_path: Path) -> None:
    _write(
        tmp_path / "flags.py",
        "from enum import Flag\n"
        "class Status(Flag):\n    DONE = 1\n"
        "def check_item(is_done: bool) -> None:\n    return None\n",
    )
    _write(
        tmp_path / "enumeration.py",
        "class Enumeration:\n    pass\n"
        "class Kind(Enumeration):\n    DONE = 1\n"
        "def check_kind(is_done: bool) -> None:\n    return None\n",
    )
    payload = _run(tmp_path, tmp_path / "out")
    shadows = [row for row in payload["alerts"] if row["duplication_type"] == "variable/variable"]
    assert any("Status" in row["primary_entity"] for row in shadows)
    assert not any("Kind" in row["primary_entity"] or "Enumeration" in row["primary_entity"] for row in shadows)


def test_urllib_parse_is_not_http_bypass(tmp_path: Path) -> None:
    _write(tmp_path / "client.py", "class ApiClient:\n    pass\n")
    _write(
        tmp_path / "parse.py",
        "import urllib.parse\n"
        "def load_path(url: str) -> str:\n    return urllib.parse.urlparse(url).path\n",
    )
    payload = _run(tmp_path, tmp_path / "out")
    assert "function/module" not in _alert_types(payload)


def test_go_http_get_is_bypass(tmp_path: Path) -> None:
    _write(tmp_path / "client.go", "type ApiClient struct {}\n")
    _write(
        tmp_path / "remote.go",
        "package p\nfunc loadRemote() {\n    http.Get(\"https://example.invalid\")\n}\n",
    )
    payload = _run(tmp_path, tmp_path / "out")
    assert "function/module" in _alert_types(payload)
    row = next(a for a in payload["alerts"] if a["duplication_type"] == "function/module")
    assert row["primary_file"] == "client.go"


def test_keyword_only_flag_param(tmp_path: Path) -> None:
    _write(
        tmp_path / "status.py",
        "from enum import Enum\n"
        "class Status(Enum):\n    DONE = 1\n"
        "def check_kw(*, is_done: bool) -> None:\n    return None\n"
        "def check_pos(is_done: bool, /) -> None:\n    return None\n",
    )
    payload = _run(tmp_path, tmp_path / "out")
    shadows = " ".join(row["shadow_entity"] for row in payload["alerts"] if row["duplication_type"] == "variable/variable")
    assert "check_kw" in shadows
    assert "check_pos" in shadows


def test_user_data_vs_user_info_is_not_dto_clone(tmp_path: Path) -> None:
    _write(tmp_path / "a.py", "class UserData:\n    name: str\n")
    _write(tmp_path / "b.py", "class UserInfo:\n    name: str\n")
    payload = _run(tmp_path, tmp_path / "out")
    assert "type/type" not in _alert_types(payload)


def test_dart_function_function_across_files(tmp_path: Path) -> None:
    _write(
        tmp_path / "a.dart",
        "String validateEmailAddress(String value) {\n  return value;\n}\n",
    )
    _write(
        tmp_path / "b.dart",
        "String validateEmailFormat(String value) {\n  return value;\n}\n",
    )
    payload = _run(tmp_path, tmp_path / "out")
    assert "function/function" in _alert_types(payload)


def test_output_escape_exits_two(tmp_path: Path) -> None:
    _write(tmp_path / "mod.py", "def ping() -> str:\n    return 'pong'\n")
    code = extractor.main(
        [
            str(tmp_path),
            "--out-dir",
            str(tmp_path / "out"),
            "--output",
            str(tmp_path / "escaped.json"),
        ]
    )
    assert code == 2
