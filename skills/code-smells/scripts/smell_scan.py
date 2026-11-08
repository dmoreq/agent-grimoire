#!/usr/bin/env python3
"""Report structural Fowler smell candidates for a Python tree. Stdlib only."""
from __future__ import annotations

import argparse
import ast
import logging
import os
import sys
import time
from collections import defaultdict
from dataclasses import asdict, dataclass, field
from pathlib import Path

MAX_FILE_BYTES = 1 * 1024 * 1024
LONG_METHOD_LINES = 50
LARGE_CLASS_METHODS = 15
LONG_PARAM_COUNT = 5
CLUMP_SIZE = 3
CLUMP_MIN_FUNCTIONS = 3
ELIF_MIN = 4
CHAIN_HOPS = 4
MIDDLE_MAN_METHODS = 3
MIDDLE_MAN_RATIO = 0.7
LAZY_CLASS_LINES = 12
ENVY_FOREIGN_MIN = 3
PROGRESS_INTERVAL_S = 5.0
SUMMARY_ROWS = 25
DEFAULT_OUT_DIR = Path(".tmp") / "code-smells"
IGNORE_DIRS = {
    ".git",
    "__pycache__",
    "venv",
    ".venv",
    "node_modules",
    "build",
    "dist",
    ".tmp",
    ".mypy_cache",
    ".pytest_cache",
}
LOGGER = logging.getLogger("code-smells")


@dataclass
class Finding:
    smell: str
    symbol: str
    file: str
    line: int
    detail: str


@dataclass
class FuncInfo:
    name: str
    qual: str
    file: str
    line: int
    loc: int
    params: list[str]
    elifs: int
    chain: int
    self_attrs: int
    foreign_attrs: int
    is_wrapper: bool
    is_accessor: bool
    assigns: set[str] = field(default_factory=set)
    reads: set[str] = field(default_factory=set)


@dataclass
class ClassInfo:
    name: str
    file: str
    line: int
    loc: int
    bases: list[str]
    fields: list[str]
    methods: list[FuncInfo]
    abstract: bool


def _expr_name(node: ast.AST) -> str:
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        return f"{_expr_name(node.value)}.{node.attr}"
    if isinstance(node, ast.Call):
        return _expr_name(node.func)
    return ""


def _elif_count(node: ast.If) -> int:
    count = 0
    current = node
    while len(current.orelse) == 1 and isinstance(current.orelse[0], ast.If):
        count += 1
        current = current.orelse[0]
    return count


def _chain_hops(node: ast.AST) -> int:
    if isinstance(node, ast.Name):
        return 1
    if isinstance(node, ast.Attribute):
        return 1 + _chain_hops(node.value)
    if isinstance(node, ast.Call):
        return _chain_hops(node.func)
    return 0


def _max_chain(node: ast.AST) -> int:
    best = 0
    for child in ast.walk(node):
        if isinstance(child, (ast.Attribute, ast.Call)):
            best = max(best, _chain_hops(child))
    return best


def _max_elifs(node: ast.AST) -> int:
    best = 0
    for child in ast.walk(node):
        if isinstance(child, ast.If):
            best = max(best, _elif_count(child))
    return best


def _attr_counts(node: ast.AST) -> tuple[int, int, set[str], set[str]]:
    self_reads = 0
    foreign = 0
    assigns: set[str] = set()
    reads: set[str] = set()
    for child in ast.walk(node):
        if not isinstance(child, ast.Attribute) or not isinstance(child.value, ast.Name):
            continue
        if child.value.id != "self":
            foreign += 1
            continue
        if isinstance(child.ctx, ast.Store):
            assigns.add(child.attr)
            continue
        reads.add(child.attr)
        self_reads += 1
    return self_reads, foreign, assigns, reads


def _is_docstring(stmt: ast.stmt) -> bool:
    return isinstance(stmt, ast.Expr) and isinstance(stmt.value, ast.Constant)


def _is_wrapper(node: ast.FunctionDef | ast.AsyncFunctionDef) -> bool:
    body = [stmt for stmt in node.body if not _is_docstring(stmt)]
    if len(body) != 1:
        return False
    stmt = body[0]
    if isinstance(stmt, ast.Return) and isinstance(stmt.value, ast.Call):
        return True
    return isinstance(stmt, ast.Expr) and isinstance(stmt.value, ast.Call)


def _is_accessor(node: ast.FunctionDef | ast.AsyncFunctionDef) -> bool:
    if node.name.startswith(("get_", "set_")):
        return True
    body = [stmt for stmt in node.body if not _is_docstring(stmt)]
    if len(body) != 1 or not isinstance(body[0], ast.Return):
        return False
    value = body[0].value
    return isinstance(value, ast.Attribute) and isinstance(value.value, ast.Name)


def _params(node: ast.FunctionDef | ast.AsyncFunctionDef) -> list[str]:
    args = [*node.args.posonlyargs, *node.args.args, *node.args.kwonlyargs]
    return [arg.arg for arg in args if arg.arg not in ("self", "cls")]


def _class_fields(node: ast.ClassDef) -> list[str]:
    fields: list[str] = []
    for item in node.body:
        if isinstance(item, ast.AnnAssign) and isinstance(item.target, ast.Name):
            fields.append(item.target.id)
        elif isinstance(item, ast.Assign):
            fields.extend(target.id for target in item.targets if isinstance(target, ast.Name))
    return fields


def _is_abstract(node: ast.ClassDef, bases: list[str]) -> bool:
    if any(base.split(".")[-1] in {"ABC", "ABCMeta"} for base in bases):
        return True
    for item in node.body:
        if not isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        for deco in item.decorator_list:
            if _expr_name(deco).split(".")[-1] == "abstractmethod":
                return True
    return False


class SmellCollector(ast.NodeVisitor):
    def __init__(self, rel_path: str) -> None:
        self.rel_path = rel_path
        self.functions: list[FuncInfo] = []
        self.classes: list[ClassInfo] = []
        self._class: str | None = None

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        bases = [_expr_name(base) for base in node.bases]
        previous = self._class
        self._class = node.name
        start = len(self.functions)
        self.generic_visit(node)
        methods = self.functions[start:]
        self.classes.append(
            ClassInfo(
                name=node.name,
                file=self.rel_path,
                line=node.lineno,
                loc=(node.end_lineno or node.lineno) - node.lineno + 1,
                bases=bases,
                fields=_class_fields(node),
                methods=methods,
                abstract=_is_abstract(node, bases),
            )
        )
        self._class = previous

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        self._add_function(node)

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
        self._add_function(node)

    def _add_function(self, node: ast.FunctionDef | ast.AsyncFunctionDef) -> None:
        self_attrs, foreign, assigns, reads = _attr_counts(node)
        qual = f"{self._class}.{node.name}" if self._class else node.name
        self.functions.append(
            FuncInfo(
                name=node.name,
                qual=qual,
                file=self.rel_path,
                line=node.lineno,
                loc=(node.end_lineno or node.lineno) - node.lineno + 1,
                params=_params(node),
                elifs=_max_elifs(node),
                chain=_max_chain(node),
                self_attrs=self_attrs,
                foreign_attrs=foreign,
                is_wrapper=_is_wrapper(node),
                is_accessor=_is_accessor(node),
                assigns=assigns,
                reads=reads,
            )
        )


def parse_python(rel_path: str, content: str) -> tuple[list[FuncInfo], list[ClassInfo]]:
    try:
        tree = ast.parse(content, filename=rel_path)
    except SyntaxError as exc:
        LOGGER.warning("Could not parse %s: %s", rel_path, exc)
        return [], []
    collector = SmellCollector(rel_path)
    collector.visit(tree)
    return collector.functions, collector.classes


def iter_python_files(root: Path) -> list[tuple[Path, str]]:
    found: list[tuple[Path, str]] = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [name for name in dirnames if name not in IGNORE_DIRS and not name.startswith(".")]
        for filename in filenames:
            if not filename.endswith(".py"):
                continue
            full = Path(dirpath) / filename
            found.append((full, os.path.relpath(full, root)))
    return found


def harvest(root: Path) -> tuple[list[FuncInfo], list[ClassInfo]]:
    functions: list[FuncInfo] = []
    classes: list[ClassInfo] = []
    started = time.monotonic()
    last_log = started
    for index, (full, rel_path) in enumerate(iter_python_files(root), start=1):
        if full.stat().st_size > MAX_FILE_BYTES:
            LOGGER.warning("Skipping %s (over %s bytes)", rel_path, MAX_FILE_BYTES)
            continue
        content = full.read_text(encoding="utf-8", errors="ignore")
        funcs, found_classes = parse_python(rel_path, content)
        functions.extend(funcs)
        classes.extend(found_classes)
        now = time.monotonic()
        if now - last_log >= PROGRESS_INTERVAL_S:
            LOGGER.info("scanned %s files (%.1f files/s)", index, index / max(now - started, 0.001))
            last_log = now
    LOGGER.info("scanned python files in %.1fs", time.monotonic() - started)
    return functions, classes


def _function_findings(functions: list[FuncInfo]) -> list[Finding]:
    findings: list[Finding] = []
    for func in functions:
        if func.loc > LONG_METHOD_LINES:
            findings.append(Finding("Long Method", func.qual, func.file, func.line, f"{func.loc} lines"))
        if len(func.params) >= LONG_PARAM_COUNT:
            findings.append(Finding("Long Parameter List", func.qual, func.file, func.line, f"{len(func.params)} parameters"))
        if func.elifs >= ELIF_MIN:
            findings.append(Finding("Switch Statements", func.qual, func.file, func.line, f"{func.elifs} elif branches"))
        if func.chain >= CHAIN_HOPS:
            findings.append(Finding("Message Chains", func.qual, func.file, func.line, f"{func.chain} hops"))
        if func.foreign_attrs >= ENVY_FOREIGN_MIN and func.foreign_attrs > func.self_attrs:
            findings.append(Finding("Feature Envy", func.qual, func.file, func.line, f"{func.foreign_attrs} foreign attributes"))
    findings.extend(_data_clumps(functions))
    return findings


def _data_clumps(functions: list[FuncInfo]) -> list[Finding]:
    groups: dict[tuple[str, ...], list[FuncInfo]] = defaultdict(list)
    for func in functions:
        if len(func.params) < CLUMP_SIZE:
            continue
        groups[tuple(sorted(func.params))].append(func)
    findings: list[Finding] = []
    for params, members in groups.items():
        if len(members) < CLUMP_MIN_FUNCTIONS:
            continue
        for func in members:
            findings.append(Finding("Data Clumps", func.qual, func.file, func.line, f"shared {', '.join(params)}"))
    return findings


def _class_findings(classes: list[ClassInfo]) -> list[Finding]:
    findings: list[Finding] = []
    subclass_count = _subclass_counts(classes)
    for cls in classes:
        findings.extend(_one_class(cls, subclass_count.get((cls.file, cls.name), 0)))
    return findings


def _subclass_counts(classes: list[ClassInfo]) -> dict[tuple[str, str], int]:
    counts: dict[tuple[str, str], int] = defaultdict(int)
    known = {(cls.file, cls.name) for cls in classes}
    for cls in classes:
        for base in cls.bases:
            key = (cls.file, base.split(".")[-1])
            if key in known and key != (cls.file, cls.name):
                counts[key] += 1
    return counts


def _one_class(cls: ClassInfo, subclasses: int) -> list[Finding]:
    findings: list[Finding] = []
    methods = [method for method in cls.methods if method.qual.startswith(f"{cls.name}.")]
    if len(methods) >= LARGE_CLASS_METHODS:
        findings.append(Finding("Large Class", cls.name, cls.file, cls.line, f"{len(methods)} methods"))
    if _is_middle_man(methods):
        findings.append(Finding("Middle Man", cls.name, cls.file, cls.line, f"{len(methods)} forwarding methods"))
    if _is_data_class(cls, methods):
        findings.append(Finding("Data Class", cls.name, cls.file, cls.line, f"{len(cls.fields)} fields"))
    if _is_lazy(cls, methods):
        findings.append(Finding("Lazy Class", cls.name, cls.file, cls.line, f"{cls.loc} lines"))
    if cls.abstract and subclasses == 1:
        findings.append(Finding("Speculative Generality", cls.name, cls.file, cls.line, "ABC with one subclass"))
    findings.extend(_temporary_fields(cls, methods))
    return findings


def _is_middle_man(methods: list[FuncInfo]) -> bool:
    if len(methods) < MIDDLE_MAN_METHODS:
        return False
    wrappers = sum(1 for method in methods if method.is_wrapper)
    return wrappers / len(methods) >= MIDDLE_MAN_RATIO


def _is_data_class(cls: ClassInfo, methods: list[FuncInfo]) -> bool:
    if len(cls.fields) < 2 or not methods:
        return False
    return all(method.is_accessor for method in methods)


def _is_lazy(cls: ClassInfo, methods: list[FuncInfo]) -> bool:
    if cls.fields or cls.abstract or cls.loc > LAZY_CLASS_LINES:
        return False
    return len(methods) <= 1


def _temporary_fields(cls: ClassInfo, methods: list[FuncInfo]) -> list[Finding]:
    writers: dict[str, set[str]] = defaultdict(set)
    readers: dict[str, set[str]] = defaultdict(set)
    for method in methods:
        for name in method.assigns:
            writers[name].add(method.qual)
        for name in method.reads:
            readers[name].add(method.qual)
    findings: list[Finding] = []
    for name, owners in writers.items():
        if len(owners) == 1 and readers.get(name, owners) <= owners:
            findings.append(Finding("Temporary Field", f"{cls.name}.{name}", cls.file, cls.line, f"used only in {next(iter(owners))}"))
    return findings


def collect_findings(functions: list[FuncInfo], classes: list[ClassInfo]) -> list[Finding]:
    findings = _function_findings(functions)
    findings.extend(_class_findings(classes))
    findings.sort(key=lambda item: (item.smell, item.file, item.line, item.symbol))
    return findings


def write_summary(path: Path, findings: list[Finding], functions: int, classes: int) -> None:
    lines = [
        "# Code Smell Scan",
        "",
        f"- **Functions**: {functions}",
        f"- **Classes**: {classes}",
        f"- **Candidates**: {len(findings)}",
        "",
        "Script rows: Long Method, Large Class, Long Parameter List, Data Clumps, Switch Statements, Message Chains, Middle Man, Data Class, Lazy Class, Feature Envy, Temporary Field, Speculative Generality.",
        "",
        "Manual rows stay in `references/fowler-catalog.md`: Refused Bequest, Inappropriate Intimacy, Parallel Inheritance, Alternative Classes with Different Interfaces, Primitive Obsession, Duplicate Code, Dead Code, Divergent Change, Shotgun Surgery.",
        "",
        "| Smell | Symbol | Location | Detail |",
        "| :--- | :--- | :--- | :--- |",
    ]
    for finding in findings[:SUMMARY_ROWS]:
        detail = finding.detail.replace("|", "\\|")
        lines.append(f"| {finding.smell} | `{finding.symbol}` | `{finding.file}:{finding.line}` | {detail} |")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_manifest(path: Path, findings: list[Finding], functions: int, classes: int) -> None:
    import json

    payload = {
        "summary": {"functions": functions, "classes": classes, "candidates": len(findings)},
        "findings": [asdict(finding) for finding in findings],
    }
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def contained_in(path: Path, root: Path) -> bool:
    resolved = path.resolve()
    base = root.resolve()
    return resolved == base or base in resolved.parents


def resolve_outputs(out_dir: Path, output: Path | None, summary: Path | None) -> tuple[Path, Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    manifest = (output or (out_dir / "smell_manifest.json")).resolve()
    summary_path = (summary or (out_dir / "smell_summary.md")).resolve()
    if not contained_in(manifest, out_dir) or not contained_in(summary_path, out_dir):
        raise ValueError(f"output paths must stay inside {out_dir.resolve()}")
    return manifest, summary_path


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Scan Python files for structural code-smell candidates.")
    parser.add_argument("root", type=Path)
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_OUT_DIR)
    parser.add_argument("--output", type=Path, default=None)
    parser.add_argument("--summary", type=Path, default=None)
    return parser


def main(argv: list[str] | None = None) -> int:
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    args = build_parser().parse_args(argv)
    if not args.root.is_dir():
        print(f"root does not exist: {args.root}", file=sys.stderr)
        return 1
    try:
        manifest, summary = resolve_outputs(args.out_dir, args.output, args.summary)
    except (ValueError, OSError) as exc:
        print(str(exc), file=sys.stderr)
        return 2
    functions, classes = harvest(args.root)
    findings = collect_findings(functions, classes)
    write_manifest(manifest, findings, len(functions), len(classes))
    write_summary(summary, findings, len(functions), len(classes))
    print(f"Manifest written to {manifest}")
    print(f"Summary written to {summary}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
