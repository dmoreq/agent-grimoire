#!/usr/bin/env python3
"""Harvest symbols and emit semantic-duplication alerts. Stdlib only."""
from __future__ import annotations

import argparse
import ast
import json
import logging
import os
import re
import sys
import time
from collections import defaultdict
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Iterator

MAX_FILE_BYTES = 1 * 1024 * 1024
ALERT_CAP = 200
SUMMARY_ROWS = 25
PROGRESS_INTERVAL_S = 5.0
DEFAULT_OUT_DIR = Path(".tmp") / "codebase-minimalism"

IGNORE_DIRS = {
    ".git",
    "__pycache__",
    "venv",
    ".venv",
    "env",
    "node_modules",
    ".dart_tool",
    "build",
    "dist",
    "target",
    ".tox",
    ".idea",
    ".vscode",
    ".tmp",
    ".mypy_cache",
    ".pytest_cache",
    "coverage",
    "htmlcov",
    ".eggs",
}
EXTENSION_MAP = {
    ".py": "python",
    ".dart": "dart",
    ".ts": "typescript",
    ".tsx": "typescript",
    ".js": "javascript",
    ".jsx": "javascript",
    ".go": "go",
    ".rs": "rust",
}
STOPWORDS = {"get", "set", "def", "for", "the", "and", "data", "info", "func"}
FLAG_PREFIXES = ("is_", "has_", "can_", "enable_", "use_")
CALC_PREFIXES = ("get", "calc", "check", "is")
DEAD_SKIP_NAMES = frozenset({"main", "run", "handler"})
ROUTE_DECORATOR_MARKS = ("route", "fixture", "get", "post", "put", "patch", "delete")
BYPASS_PREFIXES = (
    "requests.",
    "urllib.",
    "http.client",
    "http.Get",
    "http.Client",
)
BYPASS_NAMES = frozenset({"fetch", "axios", "reqwest", "dio", "requests"})
CLIENT_MARKS = ("client", "sdk")

LOGGER = logging.getLogger("codebase-minimalism")


@dataclass
class Symbol:
    name: str
    kind: str
    file: str
    line: int
    language: str
    parameters: list[dict[str, str]] = field(default_factory=list)
    members: list[str] = field(default_factory=list)
    calls: list[str] = field(default_factory=list)
    decorators: list[str] = field(default_factory=list)
    qualified_name: str = ""
    loc: int = 1
    is_wrapper: bool = False
    forward_target: str | None = None


@dataclass
class Alert:
    duplication_type: str
    primary_entity: str
    primary_file: str
    shadow_entity: str
    shadow_file: str
    reason: str
    confidence: str


def tokenize_name(name: str) -> set[str]:
    cleaned = re.sub(r"[^a-zA-Z0-9_]", " ", name)
    words = re.findall(r"[A-Z]?[a-z]+|[A-Z]+(?=[A-Z][a-z]|\d|\W|$|\d+)", cleaned)
    if not words:
        words = cleaned.split("_")
    tokens: set[str] = set()
    for word in words:
        clean = word.lower().strip("_")
        if len(clean) > 2 and clean not in STOPWORDS:
            tokens.add(clean)
    return tokens


def expand_tokens(tokens: set[str], synonyms: dict[str, str]) -> set[str]:
    extra = {synonyms[token] for token in tokens if token in synonyms}
    return tokens | extra


def _expr_name(node: ast.AST) -> str:
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        return f"{_expr_name(node.value)}.{node.attr}"
    if isinstance(node, ast.Call):
        return _expr_name(node.func)
    return ast.unparse(node)


def _is_docstring(stmt: ast.stmt) -> bool:
    return isinstance(stmt, ast.Expr) and isinstance(stmt.value, ast.Constant)


def _call_from_stmt(stmt: ast.stmt) -> ast.Call | None:
    if isinstance(stmt, ast.Return) and isinstance(stmt.value, ast.Call):
        return stmt.value
    if isinstance(stmt, ast.Expr) and isinstance(stmt.value, ast.Call):
        return stmt.value
    return None


def _class_members(node: ast.ClassDef) -> list[str]:
    members: list[str] = []
    for item in node.body:
        if isinstance(item, ast.Assign):
            members.extend(t.id for t in item.targets if isinstance(t, ast.Name))
        elif isinstance(item, ast.AnnAssign) and isinstance(item.target, ast.Name):
            members.append(item.target.id)
    return members


def _walk_calls(node: ast.AST) -> list[str]:
    calls: list[str] = []
    for child in ast.walk(node):
        if not isinstance(child, ast.Call):
            continue
        name = _expr_name(child.func)
        if name and name not in calls:
            calls.append(name)
    return calls


class PythonCollector(ast.NodeVisitor):
    def __init__(self, rel_path: str) -> None:
        self.rel_path = rel_path
        self.symbols: list[Symbol] = []
        self.class_stack: list[str] = []

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        bases = [_expr_name(base) for base in node.bases]
        kind = "enum" if any("Enum" in base for base in bases) else "model"
        self.symbols.append(
            Symbol(
                name=node.name,
                kind=kind,
                file=self.rel_path,
                line=node.lineno,
                language="python",
                members=_class_members(node),
                qualified_name=node.name,
            )
        )
        self.class_stack.append(node.name)
        self.generic_visit(node)
        self.class_stack.pop()

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        self._add_function(node)

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
        self._add_function(node)

    def visit_Assign(self, node: ast.Assign) -> None:
        if self.class_stack:
            self.generic_visit(node)
            return
        for target in node.targets:
            if isinstance(target, ast.Name) and target.id.isupper() and len(target.id) > 2:
                self.symbols.append(
                    Symbol(
                        name=target.id,
                        kind="constant",
                        file=self.rel_path,
                        line=node.lineno,
                        language="python",
                        qualified_name=target.id,
                    )
                )
        self.generic_visit(node)

    def _add_function(self, node: ast.FunctionDef | ast.AsyncFunctionDef) -> None:
        parent = self.class_stack[-1] if self.class_stack else None
        qualified = f"{parent}.{node.name}" if parent else node.name
        params = [
            {"name": arg.arg, "type": ast.unparse(arg.annotation) if arg.annotation else ""}
            for arg in node.args.args
            if arg.arg not in ("self", "cls")
        ]
        body = [stmt for stmt in node.body if not _is_docstring(stmt)]
        call_node = _call_from_stmt(body[0]) if len(body) == 1 else None
        calls = _walk_calls(node)
        loc = (node.end_lineno or node.lineno) - node.lineno + 1
        self.symbols.append(
            Symbol(
                name=node.name,
                kind="function",
                file=self.rel_path,
                line=node.lineno,
                language="python",
                parameters=params,
                calls=calls,
                decorators=[_expr_name(dec) for dec in node.decorator_list],
                qualified_name=qualified,
                loc=loc,
                is_wrapper=call_node is not None,
                forward_target=_expr_name(call_node.func) if call_node else None,
            )
        )
        self.generic_visit(node)


def parse_python(rel_path: str, content: str) -> list[Symbol]:
    try:
        tree = ast.parse(content, filename=rel_path)
    except SyntaxError as exc:
        LOGGER.warning("Could not parse %s: %s", rel_path, exc)
        return []
    collector = PythonCollector(rel_path)
    collector.visit(tree)
    return collector.symbols


def _line_of(content: str, index: int) -> int:
    return content[:index].count("\n") + 1


def _parse_parameter(raw: str, lang: str) -> dict[str, str] | None:
    piece = raw.strip()
    if not piece or piece in ("self", "cls", "_"):
        return None
    if ":" in piece:
        name, typ = piece.split(":", 1)
        return {"name": name.strip().lstrip("*"), "type": typ.strip()}
    tokens = piece.split()
    if lang == "go" and len(tokens) >= 2:
        return {"name": tokens[0], "type": " ".join(tokens[1:])}
    if lang in {"dart"} and len(tokens) >= 2:
        return {"name": tokens[-1], "type": " ".join(tokens[:-1])}
    return {"name": tokens[0].lstrip("*"), "type": tokens[1] if len(tokens) > 1 else ""}


def parse_regex_enums(rel_path: str, content: str, lang: str) -> list[Symbol]:
    symbols: list[Symbol] = []
    pattern = re.compile(r"\b(?:enum|type)\s+([A-Za-z0-9_]+)\s*(?:=\s*)?\{([^}]+)\}", re.MULTILINE)
    for match in pattern.finditer(content):
        members = [w for w in re.findall(r"\b([A-Za-z0-9_]+)\b", match.group(2)) if not w.isdigit()]
        symbols.append(
            Symbol(
                name=match.group(1),
                kind="enum",
                file=rel_path,
                line=_line_of(content, match.start()),
                language=lang,
                members=members[:30],
                qualified_name=match.group(1),
            )
        )
    return symbols


def parse_regex_models(rel_path: str, content: str, lang: str) -> list[Symbol]:
    symbols: list[Symbol] = []
    pattern = re.compile(
        r"\b(?:export\s+)?(?:class|interface|struct|type)\s+([A-Za-z0-9_]+)",
        re.MULTILINE,
    )
    for match in pattern.finditer(content):
        symbols.append(
            Symbol(
                name=match.group(1),
                kind="model",
                file=rel_path,
                line=_line_of(content, match.start()),
                language=lang,
                qualified_name=match.group(1),
            )
        )
    return symbols


_FN_PATTERNS = (
    re.compile(r"\b(?:export\s+)?(?:default\s+)?(?:async\s+)?function(?:\s+([A-Za-z0-9_]+))?\s*\(([^)]*)\)"),
    re.compile(r"func\s+(?:\([^)]+\)\s+)?([A-Za-z0-9_]+)\s*\(([^)]*)\)"),
    re.compile(r"(?:pub\s+)?(?:async\s+)?fn\s+([A-Za-z0-9_]+)\s*(?:<[^>]+>)?\s*\(([^)]*)\)"),
    re.compile(r"\b(?:export\s+)?(?:const|let|var)\s+([A-Za-z0-9_]+)\s*=\s*(?:async\s*)?\(([^)]*)\)\s*=>"),
)


def parse_regex_functions(rel_path: str, content: str, lang: str) -> list[Symbol]:
    symbols: list[Symbol] = []
    seen_lines: set[int] = set()
    skip = {"if", "while", "for", "switch", "catch", "return", "constructor"}
    for pattern in _FN_PATTERNS:
        for match in pattern.finditer(content):
            name = match.group(1)
            lineno = _line_of(content, match.start())
            if not name or name in skip or lineno in seen_lines:
                continue
            seen_lines.add(lineno)
            raw = match.group(2) or ""
            params = [p for p in (_parse_parameter(part, lang) for part in raw.split(",")) if p]
            symbols.append(
                Symbol(
                    name=name,
                    kind="function",
                    file=rel_path,
                    line=lineno,
                    language=lang,
                    parameters=params,
                    qualified_name=name,
                )
            )
    return symbols


def parse_regex_constants(rel_path: str, content: str, lang: str) -> list[Symbol]:
    symbols: list[Symbol] = []
    pattern = re.compile(r"\b(?:const|final|static\s+const)\s+(?:[A-Za-z0-9_<>,]+\s+)?([A-Z0-9_]{3,})\b\s*=")
    for match in pattern.finditer(content):
        symbols.append(
            Symbol(
                name=match.group(1),
                kind="constant",
                file=rel_path,
                line=_line_of(content, match.start()),
                language=lang,
                qualified_name=match.group(1),
            )
        )
    return symbols


def parse_regex_file(rel_path: str, content: str, lang: str) -> list[Symbol]:
    symbols = parse_regex_enums(rel_path, content, lang)
    symbols.extend(parse_regex_models(rel_path, content, lang))
    symbols.extend(parse_regex_functions(rel_path, content, lang))
    symbols.extend(parse_regex_constants(rel_path, content, lang))
    return symbols


def iter_source_files(root: Path) -> Iterator[tuple[Path, str, str]]:
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [name for name in dirnames if name not in IGNORE_DIRS and not name.startswith(".")]
        for filename in filenames:
            ext = Path(filename).suffix.lower()
            if ext not in EXTENSION_MAP:
                continue
            full = Path(dirpath) / filename
            yield full, os.path.relpath(full, root), EXTENSION_MAP[ext]


def parse_file(full: Path, rel_path: str, lang: str) -> list[Symbol]:
    size = full.stat().st_size
    if size > MAX_FILE_BYTES:
        LOGGER.warning("Skipping %s (%s bytes > %s)", rel_path, size, MAX_FILE_BYTES)
        return []
    content = full.read_text(encoding="utf-8", errors="ignore")
    if lang == "python":
        return parse_python(rel_path, content)
    return parse_regex_file(rel_path, content, lang)


def harvest(root: Path) -> list[Symbol]:
    symbols: list[Symbol] = []
    started = time.monotonic()
    last_log = started
    scanned = 0
    for full, rel_path, lang in iter_source_files(root):
        scanned += 1
        try:
            symbols.extend(parse_file(full, rel_path, lang))
        except OSError as exc:
            LOGGER.warning("Failed to read %s: %s", rel_path, exc)
        now = time.monotonic()
        if now - last_log >= PROGRESS_INTERVAL_S:
            rate = scanned / max(now - started, 0.001)
            LOGGER.info("scanned %s files (%.1f files/s)", scanned, rate)
            last_log = now
    LOGGER.info("scanned %s files in %.1fs", scanned, time.monotonic() - started)
    return symbols


def _is_flag_param(param: dict[str, str]) -> bool:
    name = param.get("name", "")
    typ = param.get("type", "")
    return name.startswith(FLAG_PREFIXES) or typ == "bool"


def detect_variable_variable(symbols: list[Symbol], synonyms: dict[str, str]) -> list[Alert]:
    alerts: list[Alert] = []
    enums = [s for s in symbols if s.kind == "enum"]
    functions = [s for s in symbols if s.kind == "function"]
    for enum in enums:
        enum_tokens = expand_tokens(tokenize_name(enum.name), synonyms)
        for member in enum.members:
            enum_tokens |= expand_tokens(tokenize_name(member), synonyms)
        for fn in functions:
            alerts.extend(_flag_overlaps(enum, enum_tokens, fn, synonyms))
    return alerts


def _flag_overlaps(
    enum: Symbol, enum_tokens: set[str], fn: Symbol, synonyms: dict[str, str]
) -> list[Alert]:
    alerts: list[Alert] = []
    for param in fn.parameters:
        if not _is_flag_param(param):
            continue
        overlap = expand_tokens(tokenize_name(param["name"]), synonyms) & enum_tokens
        if not overlap:
            continue
        alerts.append(
            Alert(
                duplication_type="variable/variable",
                primary_entity=f"Enum {enum.name}",
                primary_file=enum.file,
                shadow_entity=f"Parameter '{param['name']}' in `{fn.qualified_name or fn.name}()`",
                shadow_file=fn.file,
                reason=f"Boolean flag '{param['name']}' shadows Enum '{enum.name}'. Matched: {sorted(overlap)}.",
                confidence="HIGH",
            )
        )
    return alerts


def _token_index(functions: list[Symbol], synonyms: dict[str, str]) -> dict[str, list[int]]:
    index: dict[str, list[int]] = defaultdict(list)
    for i, fn in enumerate(functions):
        for token in expand_tokens(tokenize_name(fn.name), synonyms):
            index[token].append(i)
    return index


def detect_function_function(symbols: list[Symbol], synonyms: dict[str, str], cap: int) -> list[Alert]:
    functions = [s for s in symbols if s.kind == "function"]
    index = _token_index(functions, synonyms)
    seen: set[tuple[int, int]] = set()
    alerts: list[Alert] = []
    for i, fn_a in enumerate(functions):
        tokens_a = expand_tokens(tokenize_name(fn_a.name), synonyms)
        if len(tokens_a) < 2:
            continue
        candidates = {j for token in tokens_a for j in index[token] if j > i}
        for j in candidates:
            pair = _fn_pair_alert(fn_a, functions[j], tokens_a, synonyms)
            if pair is None:
                continue
            key = (i, j)
            if key in seen:
                continue
            seen.add(key)
            alerts.append(pair)
    alerts.sort(key=lambda a: (a.primary_file, a.shadow_file, a.primary_entity))
    return alerts[:cap]


def _fn_pair_alert(
    fn_a: Symbol, fn_b: Symbol, tokens_a: set[str], synonyms: dict[str, str]
) -> Alert | None:
    if fn_a.file == fn_b.file:
        return None
    tokens_b = expand_tokens(tokenize_name(fn_b.name), synonyms)
    if len(tokens_b) < 2:
        return None
    intersection = tokens_a & tokens_b
    union = tokens_a | tokens_b
    jaccard = len(intersection) / len(union) if union else 0.0
    if len(intersection) < 2 or jaccard < 0.5:
        return None
    return Alert(
        duplication_type="function/function",
        primary_entity=f"Function `{fn_a.name}()`",
        primary_file=fn_a.file,
        shadow_entity=f"Function `{fn_b.name}()`",
        shadow_file=fn_b.file,
        reason=f"Functions share {sorted(intersection)} (Jaccard {jaccard:.2f}).",
        confidence="HIGH" if jaccard >= 0.7 else "MEDIUM",
    )


def detect_function_variable(symbols: list[Symbol], synonyms: dict[str, str]) -> list[Alert]:
    alerts: list[Alert] = []
    constants = [s for s in symbols if s.kind == "constant"]
    functions = [s for s in symbols if s.kind == "function"]
    for const in constants:
        const_tokens = expand_tokens(tokenize_name(const.name), synonyms)
        for fn in functions:
            if not fn.name.lower().startswith(CALC_PREFIXES):
                continue
            overlap = const_tokens & expand_tokens(tokenize_name(fn.name), synonyms)
            if len(overlap) < 2:
                continue
            alerts.append(
                Alert(
                    duplication_type="function/variable",
                    primary_entity=f"Constant `{const.name}`",
                    primary_file=const.file,
                    shadow_entity=f"Function `{fn.name}()`",
                    shadow_file=fn.file,
                    reason=f"Function `{fn.name}` overlaps constant `{const.name}`: {sorted(overlap)}.",
                    confidence="MEDIUM",
                )
            )
    return alerts


def _is_bypass_call(call: str) -> bool:
    if call in BYPASS_NAMES:
        return True
    return any(call.startswith(prefix) for prefix in BYPASS_PREFIXES)


def _has_client_symbol(symbols: list[Symbol]) -> bool:
    for symbol in symbols:
        lower = symbol.name.lower()
        if any(mark in lower for mark in CLIENT_MARKS):
            return True
    return False


def detect_function_module(symbols: list[Symbol]) -> list[Alert]:
    if not _has_client_symbol(symbols):
        return []
    alerts: list[Alert] = []
    for fn in symbols:
        if fn.kind != "function":
            continue
        hits = [call for call in fn.calls if _is_bypass_call(call)]
        if not hits:
            continue
        alerts.append(
            Alert(
                duplication_type="function/module",
                primary_entity="Project client/SDK symbol",
                primary_file="",
                shadow_entity=f"Function `{fn.qualified_name or fn.name}()`",
                shadow_file=fn.file,
                reason=f"Raw HTTP/client call {hits} bypasses an existing client/SDK symbol.",
                confidence="MEDIUM",
            )
        )
    return alerts


def detect_type_type(symbols: list[Symbol], synonyms: dict[str, str], cap: int) -> list[Alert]:
    models = [s for s in symbols if s.kind == "model"]
    alerts: list[Alert] = []
    for i, model_a in enumerate(models):
        tokens_a = expand_tokens(tokenize_name(model_a.name), synonyms)
        if not tokens_a:
            continue
        for model_b in models[i + 1 :]:
            if model_a.file == model_b.file:
                continue
            tokens_b = expand_tokens(tokenize_name(model_b.name), synonyms)
            intersection = tokens_a & tokens_b
            if len(intersection) < 2 and tokens_a != tokens_b:
                continue
            if not intersection:
                continue
            alerts.append(
                Alert(
                    duplication_type="type/type",
                    primary_entity=f"Model `{model_a.name}`",
                    primary_file=model_a.file,
                    shadow_entity=f"Model `{model_b.name}`",
                    shadow_file=model_b.file,
                    reason=f"Models share {sorted(intersection)} across files.",
                    confidence="MEDIUM",
                )
            )
    alerts.sort(key=lambda a: (a.primary_file, a.shadow_file, a.primary_entity))
    return alerts[:cap]


def wrapper_candidates(symbols: list[Symbol]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for fn in symbols:
        if fn.kind != "function" or not fn.is_wrapper or not fn.forward_target:
            continue
        rows.append(
            {
                "function": fn.qualified_name or fn.name,
                "file": fn.file,
                "line": fn.line,
                "wrapped_target": fn.forward_target,
                "loc": fn.loc,
            }
        )
    return rows


def _is_route(fn: Symbol) -> bool:
    for decorator in fn.decorators:
        low = decorator.lower()
        if any(mark in low for mark in ROUTE_DECORATOR_MARKS):
            return True
    return False


def dead_code_candidates(symbols: list[Symbol]) -> list[dict[str, Any]]:
    functions = [s for s in symbols if s.kind == "function" and s.language == "python"]
    counts: dict[str, int] = defaultdict(int)
    for fn in functions:
        for call in fn.calls:
            counts[call] += 1
            counts[call.split(".")[-1]] += 1
    rows: list[dict[str, Any]] = []
    for fn in functions:
        if fn.name.startswith("_") or fn.name in DEAD_SKIP_NAMES or _is_route(fn):
            continue
        received = counts[fn.name] + counts[fn.qualified_name]
        if received != 0:
            continue
        rows.append({"name": fn.qualified_name or fn.name, "file": fn.file, "line": fn.line, "loc": fn.loc})
    return rows


def collect_alerts(
    symbols: list[Symbol], synonyms: dict[str, str], cap: int
) -> tuple[list[Alert], list[dict[str, Any]], list[dict[str, Any]]]:
    alerts: list[Alert] = []
    alerts.extend(detect_variable_variable(symbols, synonyms))
    alerts.extend(detect_function_function(symbols, synonyms, cap))
    alerts.extend(detect_function_variable(symbols, synonyms))
    alerts.extend(detect_function_module(symbols))
    alerts.extend(detect_type_type(symbols, synonyms, cap))
    return alerts[:cap], wrapper_candidates(symbols), dead_code_candidates(symbols)


def summarize(symbols: list[Symbol], alerts: list[Alert]) -> dict[str, int]:
    return {
        "total_symbols": len(symbols),
        "total_functions": sum(1 for s in symbols if s.kind == "function"),
        "total_enums": sum(1 for s in symbols if s.kind == "enum"),
        "total_models": sum(1 for s in symbols if s.kind == "model"),
        "total_constants": sum(1 for s in symbols if s.kind == "constant"),
        "semantic_duplication_alerts": len(alerts),
    }


def _md_cell(value: str) -> str:
    return value.replace("|", "\\|").replace("\n", " ")


def write_summary(
    path: Path,
    summary: dict[str, int],
    alerts: list[Alert],
    wrappers: list[dict[str, Any]],
    dead: list[dict[str, Any]],
) -> None:
    lines = [
        "# Universal Codebase Semantic Audit Summary",
        "",
        f"- **Total Symbols Indexed**: {summary['total_symbols']}",
        f"- **Functions**: {summary['total_functions']}",
        f"- **Enums**: {summary['total_enums']}",
        f"- **Models/Interfaces**: {summary['total_models']}",
        f"- **Constants**: {summary['total_constants']}",
        f"- **Semantic Duplication Alerts**: {summary['semantic_duplication_alerts']}",
        f"- **Pass-through Wrappers (candidates)**: {len(wrappers)}",
        f"- **Dead Code (Python candidates, 0 callers)**: {len(dead)}",
        "",
        "## Detected Semantic Duplications",
        "",
        "| Category | Primary Entity | Shadow Entity | Location | Details |",
        "| :--- | :--- | :--- | :--- | :--- |",
    ]
    for alert in alerts[:SUMMARY_ROWS]:
        location = f"{alert.primary_file} <-> {alert.shadow_file}"
        lines.append(
            f"| `{alert.duplication_type}` | `{_md_cell(alert.primary_entity)}` | "
            f"`{_md_cell(alert.shadow_entity)}` | `{_md_cell(location)}` | {_md_cell(alert.reason)} |"
        )
    _append_candidate_tables(lines, wrappers, dead)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _append_candidate_tables(
    lines: list[str], wrappers: list[dict[str, Any]], dead: list[dict[str, Any]]
) -> None:
    lines.extend(["", "## Pass-through Wrappers (candidates)", ""])
    lines.extend(["| Function | Forwards To | File:Line | LOC |", "| :--- | :--- | :--- | :--- |"])
    for row in wrappers[:SUMMARY_ROWS]:
        lines.append(f"| `{row['function']}` | `{row['wrapped_target']}` | `{row['file']}:{row['line']}` | {row['loc']} |")
    lines.extend(["", "## Dead Code Candidates (Python, 0 callers)", ""])
    lines.extend(["| Function | File:Line | LOC |", "| :--- | :--- | :--- |"])
    for row in dead[:SUMMARY_ROWS]:
        lines.append(f"| `{row['name']}` | `{row['file']}:{row['line']}` | {row['loc']} |")


def write_manifest(
    path: Path,
    summary: dict[str, int],
    alerts: list[Alert],
    wrappers: list[dict[str, Any]],
    dead: list[dict[str, Any]],
    symbols: list[Symbol],
    full_symbols: bool,
) -> None:
    payload: dict[str, Any] = {
        "summary": summary,
        "alerts": [asdict(alert) for alert in alerts],
        "redundant_wrappers": wrappers,
        "dead_code_candidates": dead,
    }
    if full_symbols:
        payload["symbols"] = [asdict(symbol) for symbol in symbols]
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")


def contained_in(path: Path, root: Path) -> bool:
    resolved = path.resolve()
    base = root.resolve()
    return resolved == base or base in resolved.parents


def resolve_outputs(out_dir: Path, output: Path | None, summary: Path | None) -> tuple[Path, Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    manifest = (output or (out_dir / "universal_manifest.json")).resolve()
    summary_path = (summary or (out_dir / "universal_summary.md")).resolve()
    if not contained_in(manifest, out_dir) or not contained_in(summary_path, out_dir):
        raise ValueError(f"output paths must stay inside {out_dir.resolve()}")
    return manifest, summary_path


def load_synonyms(path: Path | None) -> dict[str, str]:
    if path is None:
        return {}
    raw = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise ValueError("synonyms file must be a JSON object of token -> token")
    return {str(key).lower(): str(value).lower() for key, value in raw.items()}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Harvest symbols and detect semantic duplication.")
    parser.add_argument("root", type=Path, help="Codebase directory to scan")
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_OUT_DIR)
    parser.add_argument("--output", type=Path, default=None)
    parser.add_argument("--summary", type=Path, default=None)
    parser.add_argument("--full-symbols", action="store_true")
    parser.add_argument("--synonyms", type=Path, default=None)
    parser.add_argument("--alert-cap", type=int, default=ALERT_CAP)
    return parser


def run_audit(
    root: Path,
    out_dir: Path,
    output: Path | None,
    summary: Path | None,
    full_symbols: bool,
    synonyms_path: Path | None,
    alert_cap: int,
) -> int:
    if not root.is_dir():
        print(f"root does not exist: {root}", file=sys.stderr)
        return 1
    try:
        manifest_path, summary_path = resolve_outputs(out_dir, output, summary)
        synonyms = load_synonyms(synonyms_path)
    except (ValueError, OSError, json.JSONDecodeError) as exc:
        print(str(exc), file=sys.stderr)
        return 2
    symbols = harvest(root)
    alerts, wrappers, dead = collect_alerts(symbols, synonyms, alert_cap)
    summary_counts = summarize(symbols, alerts)
    write_manifest(manifest_path, summary_counts, alerts, wrappers, dead, symbols, full_symbols)
    write_summary(summary_path, summary_counts, alerts, wrappers, dead)
    print(f"Manifest written to {manifest_path}")
    print(f"Summary written to {summary_path}")
    return 0


def main(argv: list[str] | None = None) -> int:
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    args = build_parser().parse_args(argv)
    return run_audit(
        root=args.root,
        out_dir=args.out_dir,
        output=args.output,
        summary=args.summary,
        full_symbols=args.full_symbols,
        synonyms_path=args.synonyms,
        alert_cap=args.alert_cap,
    )


if __name__ == "__main__":
    sys.exit(main())
