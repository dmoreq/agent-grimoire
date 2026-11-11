#!/usr/bin/env python3
"""Validate structural invariants of a single-file HTML report."""
from __future__ import annotations

import argparse
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit
import re
import sys

MAX_BYTES = 1_000_000
PRESETS = (
    "dossier",
    "zen-garden",
    "chronicle",
    "sumi-ink",
    "shoji-grid",
    "aizome-indigo",
    "yugen-noir",
    "simple-white",
    "plotly-white",
    "ggplot2-grammar",
    "apple-hig",
    "material-you",
    "geist-zinc",
)
LAYOUTS = ("L1", "L2", "L3", "L4", "L5", "L6")
VOICES = ("V1", "V2", "V3", "V4")
FONT_STYLE_HOST = "fonts.googleapis.com"
FONT_FILE_HOST = "fonts.gstatic.com"
CHART_HOST = "cdn.jsdelivr.net"
CHART_PATH_PREFIX = "/npm/chart.js@"
ASSET_ATTRIBUTES = {
    "img": "src",
    "iframe": "src",
    "object": "data",
    "embed": "src",
    "source": "src",
    "video": "src",
    "audio": "src",
    "track": "src",
}
CSS_MARKERS = (
    "prefers-color-scheme",
    "prefers-reduced-motion",
    "@media print",
    "@page",
    "tabular-nums",
    "focus-visible",
    "font-optical-sizing",
)
CHART_MARKERS = (
    "chart-tooltip",
    "data-chart-point",
    "data-label",
    'role="status"',
    'aria-hidden="true"',
    'pointer-events="none"',
)
NETWORK_PATTERNS = (
    ("fetch", re.compile(r"\bfetch\s*\(", re.IGNORECASE)),
    ("xmlhttprequest", re.compile(r"\bXMLHttpRequest\b", re.IGNORECASE)),
    ("sendbeacon", re.compile(r"\bsendBeacon\s*\(", re.IGNORECASE)),
    ("websocket", re.compile(r"\bWebSocket\b", re.IGNORECASE)),
    ("eventsource", re.compile(r"\bEventSource\b", re.IGNORECASE)),
    ("dynamic-import", re.compile(r"\bimport\s*\(", re.IGNORECASE)),
    ("new-image", re.compile(r"\bnew\s+Image\b", re.IGNORECASE)),
    ("location", re.compile(r"\blocation\.(?:href|assign|replace)\b", re.IGNORECASE)),
)
SECRET_PATTERNS = (
    ("private-key", re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----")),
    ("aws-access-key", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
    ("github-token", re.compile(r"\bgh[pousr]_[A-Za-z0-9]{36,}\b")),
    ("openai-key", re.compile(r"\bsk-(?:proj-)?[A-Za-z0-9_-]{20,}\b")),
    ("bearer-token", re.compile(r"\bAuthorization\s*:\s*Bearer\s+[A-Za-z0-9._-]{20,}", re.IGNORECASE)),
)
CSP_REQUIRED_NONE = ("default-src", "connect-src", "object-src", "base-uri", "form-action")
TOKEN_BLOCK = re.compile(
    r":root(?:\s*,\s*:root\s*\[\s*data-preset\s*=\s*['\"]([^'\"]+)['\"]\s*\]"
    r"|\s*\[\s*data-preset\s*=\s*['\"]([^'\"]+)['\"]\s*\])\s*\{",
    re.IGNORECASE,
)
CSS_URL = re.compile(r"(?:url\(\s*|@import\s+(?:url\(\s*)?)['\"]?([^)'\";]+)", re.IGNORECASE)


class ReportParser(HTMLParser):
    """Collect the structural facts the validator needs from one HTML file."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.doctype = False
        self.html_attrs: dict[str, str] = {}
        self.meta_charset = False
        self.meta_viewport = False
        self.has_theme_toggle = False
        self.has_font_stylesheet = False
        self.font_display_swap = False
        self.has_chart_script = False
        self.csp_content = ""
        self.has_chart = False
        self.preset_switches: list[str] = []
        self.inline_handlers: list[str] = []
        self.external_assets: list[str] = []
        self.inline_network_terms: list[str] = []
        self.ids: list[str] = []
        self.duplicate_ids: set[str] = set()
        self.h1_count = 0
        self.last_heading = 0
        self.heading_jumps: list[str] = []
        self.tables_without_head = 0
        self.th_without_scope = 0
        self.buttons_without_type: list[str] = []
        self.has_details = False
        self._table_stack: list[bool] = []
        self._in_script = False
        self._script_type = ""
        self._script_text: list[str] = []

    def handle_decl(self, decl: str) -> None:
        if decl.strip().lower() == "doctype html":
            self.doctype = True

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attributes = {name.lower(): (value or "") for name, value in attrs}
        if tag == "html":
            self.html_attrs = attributes
        if tag == "meta":
            self._read_meta(attributes)
        self._read_preset_switch(attributes)
        self._read_heading(tag)
        self._read_structure(tag, attributes)
        self._read_asset(tag, attributes)
        self._read_id(attributes)
        self._read_interactions(tag, attributes)

    def handle_endtag(self, tag: str) -> None:
        if tag == "script" and self._in_script:
            self._close_script()
        if tag == "table" and self._table_stack:
            if not self._table_stack.pop():
                self.tables_without_head += 1

    def handle_data(self, data: str) -> None:
        if self._in_script:
            self._script_text.append(data)

    def _read_meta(self, attributes: dict[str, str]) -> None:
        if attributes.get("charset", "").lower() == "utf-8":
            self.meta_charset = True
        name = attributes.get("name", "").lower()
        content = attributes.get("content", "")
        if name == "viewport" and "width=device-width" in content.lower():
            self.meta_viewport = True
        http_equiv = attributes.get("http-equiv", "").lower()
        if http_equiv == "content-security-policy":
            self.csp_content = content
        if http_equiv == "refresh":
            self.external_assets.append("<meta http-equiv=refresh>")

    def _read_preset_switch(self, attributes: dict[str, str]) -> None:
        classes = attributes.get("class", "").lower()
        is_switch = (
            "data-preset-val" in attributes
            or "preset-btn" in classes
            or "preset-group" in classes
        )
        if is_switch:
            self.preset_switches.append(attributes.get("id") or classes or "preset control")

    def _read_heading(self, tag: str) -> None:
        if len(tag) != 2 or tag[0] != "h" or tag[1] not in "123456":
            return
        level = int(tag[1])
        if self.last_heading and level > self.last_heading + 1:
            self.heading_jumps.append(f"h{self.last_heading} to h{level}")
        self.last_heading = level

    def _read_structure(self, tag: str, attributes: dict[str, str]) -> None:
        if tag == "h1":
            self.h1_count += 1
        if tag == "table":
            self._table_stack.append(False)
        if tag == "details":
            self.has_details = True
        if tag == "thead" and self._table_stack:
            self._table_stack[-1] = True
        if tag == "th" and "scope" not in attributes and "role" not in attributes:
            self.th_without_scope += 1
        if tag == "button" and attributes.get("type", "").lower() != "button":
            self.buttons_without_type.append(attributes.get("id") or "unnamed")
        if attributes.get("id") == "theme-toggle":
            self.has_theme_toggle = True
        if "data-chart-point" in attributes or attributes.get("id") == "chart-tooltip":
            self.has_chart = True

    def _read_asset(self, tag: str, attributes: dict[str, str]) -> None:
        if tag == "link":
            self._read_link(attributes)
            return
        if tag == "script":
            self._read_script_asset(attributes)
            return
        if tag in {"a", "area"}:
            self._read_anchor(attributes)
            return
        if tag == "base":
            if attributes.get("href"):
                self.external_assets.append("<base href>")
            return
        if tag == "form":
            if attributes.get("action"):
                self.external_assets.append(f"<form action={attributes['action'][:80]}>")
            return
        if tag in {"input", "button"}:
            if attributes.get("formaction"):
                self.external_assets.append(f"<{tag} formaction={attributes['formaction'][:80]}>")
            return
        attribute = ASSET_ATTRIBUTES.get(tag)
        if attribute:
            self._record_url(tag, attribute, attributes.get(attribute, ""))
        if tag == "video" and attributes.get("poster"):
            self._record_url(tag, "poster", attributes["poster"])
        if tag in {"img", "source"} and attributes.get("srcset"):
            self._read_srcset(tag, attributes["srcset"])

    def _read_link(self, attributes: dict[str, str]) -> None:
        value = attributes.get("href", "").strip()
        if not value:
            return
        parts = urlsplit(value)
        rel = attributes.get("rel", "").lower()
        if parts.scheme == "https" and parts.hostname == FONT_STYLE_HOST and parts.path.startswith("/css"):
            self.has_font_stylesheet = True
            if "display=swap" in parts.query:
                self.font_display_swap = True
            return
        if (
            parts.scheme == "https"
            and parts.hostname in {FONT_STYLE_HOST, FONT_FILE_HOST}
            and "preconnect" in rel
        ):
            return
        self.external_assets.append(f"<link href={value[:80]}>")

    def _read_script_asset(self, attributes: dict[str, str]) -> None:
        value = attributes.get("src", "").strip()
        if not value:
            return
        parts = urlsplit(value)
        integrity = attributes.get("integrity", "")
        approved = (
            parts.scheme == "https"
            and parts.hostname == CHART_HOST
            and parts.path.startswith(CHART_PATH_PREFIX)
            and re.fullmatch(r"sha384-[A-Za-z0-9+/]+={0,2}", integrity) is not None
            and attributes.get("crossorigin") == "anonymous"
        )
        if not approved:
            self.external_assets.append(f"<script src={value[:80]}>")
        else:
            self.has_chart_script = True

    def _read_anchor(self, attributes: dict[str, str]) -> None:
        value = attributes.get("href", "").strip()
        if not value or value.startswith("#"):
            return
        lowered = value.lower()
        if lowered.startswith(("javascript:", "vbscript:")):
            self.inline_handlers.append("anchor href scheme")
            return
        parts = urlsplit(value)
        if parts.scheme in {"http", "https", "mailto", "tel"}:
            return
        self.external_assets.append(f"<a href={value[:80]}>")

    def _read_srcset(self, tag: str, value: str) -> None:
        for candidate in value.split(","):
            url = candidate.strip().split()[0] if candidate.strip() else ""
            if url:
                self._record_url(tag, "srcset", url)

    def _record_url(self, tag: str, attribute: str, value: str) -> None:
        value = value.strip()
        if not value or value.startswith("#"):
            return
        lowered = value.lower()
        if lowered.startswith(("javascript:", "vbscript:")):
            self.inline_handlers.append(f"{tag} {attribute} scheme")
            return
        if lowered.startswith("data:"):
            if tag in {"img", "source"}:
                return
            self.external_assets.append(f"<{tag} {attribute}=data:...>")
            return
        parts = urlsplit(value)
        if parts.scheme in {"http", "https"}:
            self.external_assets.append(f"<{tag} {attribute}={value[:80]}>")
            return
        self.external_assets.append(f"<{tag} {attribute}={value[:80]}>")

    def _read_id(self, attributes: dict[str, str]) -> None:
        value = attributes.get("id", "")
        if not value:
            return
        if value in self.ids:
            self.duplicate_ids.add(value)
        self.ids.append(value)

    def _read_interactions(self, tag: str, attributes: dict[str, str]) -> None:
        if tag == "script":
            self._in_script = True
            self._script_type = attributes.get("type", "").lower()
            self._script_text = []
        for name in attributes:
            if name.startswith("on"):
                self.inline_handlers.append(name)

    def _close_script(self) -> None:
        text = "".join(self._script_text)
        if self._script_type not in {"application/json", "application/ld+json", "text/template"}:
            for name, pattern in NETWORK_PATTERNS:
                if pattern.search(text):
                    self.inline_network_terms.append(name)
        self._in_script = False
        self._script_text = []


def _csp_failures(parser: ReportParser) -> list[str]:
    if not parser.csp_content:
        return ["missing Content-Security-Policy meta"]
    directives: dict[str, list[str]] = {}
    for chunk in parser.csp_content.split(";"):
        tokens = chunk.strip().split()
        if tokens:
            directives[tokens[0].lower()] = tokens[1:]
    failures: list[str] = []
    for name in CSP_REQUIRED_NONE:
        if directives.get(name) != ["'none'"]:
            failures.append(f"CSP {name} must be 'none'")
    expected = {
        "style-src": {"'unsafe-inline'", "https://fonts.googleapis.com"},
        "font-src": {"https://fonts.gstatic.com"},
        "img-src": {"data:"},
        "script-src": {"'unsafe-inline'", "https://cdn.jsdelivr.net"},
    }
    required = {
        "style-src": {"'unsafe-inline'", "https://fonts.googleapis.com"},
        "font-src": {"https://fonts.gstatic.com"},
        "img-src": {"data:"},
        "script-src": {"'unsafe-inline'"},
    }
    for name, allowed in expected.items():
        tokens = set(directives.get(name, []))
        if tokens - allowed:
            failures.append(f"CSP {name} has disallowed tokens: {sorted(tokens - allowed)}")
        if not required[name] <= tokens:
            failures.append(f"CSP {name} is missing required tokens: {sorted(required[name] - tokens)}")
    if parser.has_chart_script and "https://cdn.jsdelivr.net" not in directives.get("script-src", []):
        failures.append("CSP script-src must allow https://cdn.jsdelivr.net for Chart.js")
    return failures


def _axis_failures(attrs: dict[str, str]) -> list[str]:
    failures: list[str] = []
    layout = attrs.get("data-layout", "")
    voice = attrs.get("data-voice", "")
    if layout and layout not in LAYOUTS:
        failures.append(f"data-layout must be one of {LAYOUTS}, found '{layout}'")
    if voice and voice not in VOICES:
        failures.append(f"data-voice must be one of {VOICES}, found '{voice}'")
    return failures


def _parser_failures(parser: ReportParser) -> list[str]:
    preset = parser.html_attrs.get("data-preset", "")
    checks = (
        (parser.doctype, "missing <!DOCTYPE html>"),
        (parser.meta_charset, 'missing <meta charset="utf-8">'),
        (parser.meta_viewport, "missing viewport meta with width=device-width"),
        (bool(parser.html_attrs.get("lang")), "missing <html lang>"),
        (preset in PRESETS, f"data-preset must be one of {PRESETS}, found '{preset}'"),
        (bool(parser.html_attrs.get("data-theme")), "missing data-theme on <html>"),
        (parser.has_theme_toggle, 'missing id="theme-toggle" control'),
        (parser.has_font_stylesheet, "missing Google Fonts stylesheet link"),
        (parser.font_display_swap, "missing display=swap on the font stylesheet"),
        (not parser.preset_switches, f"preset switcher is not allowed: {parser.preset_switches}"),
        (parser.h1_count == 1, f"expected one <h1>, found {parser.h1_count}"),
        (not parser.heading_jumps, f"heading level jumps: {parser.heading_jumps}"),
        (not parser.duplicate_ids, f"duplicate ids: {sorted(parser.duplicate_ids)}"),
        (not parser.inline_handlers, f"inline event handlers: {sorted(set(parser.inline_handlers))}"),
        (not parser.external_assets, f"external or sidecar assets: {parser.external_assets}"),
        (
            not parser.inline_network_terms,
            f"inline script network calls: {sorted(set(parser.inline_network_terms))}",
        ),
        (parser.tables_without_head == 0, f"{parser.tables_without_head} table(s) without <thead>"),
        (parser.th_without_scope == 0, f"{parser.th_without_scope} <th> without scope or role"),
        (
            not parser.buttons_without_type,
            f"buttons without type=button: {parser.buttons_without_type}",
        ),
    )
    failures = [message for passed, message in checks if not passed]
    failures.extend(_axis_failures(parser.html_attrs))
    return failures


def _strip_comments(text: str) -> str:
    text = re.sub(r"<!--.*?-->", "", text, flags=re.DOTALL)
    return re.sub(r"/\*.*?\*/", "", text, flags=re.DOTALL)


def _style_text(text: str) -> str:
    blocks = re.findall(r"<style\b[^>]*>(.*?)</style>", text, flags=re.IGNORECASE | re.DOTALL)
    return "\n".join(blocks)


def _preset_blocks(text: str) -> list[str]:
    blocks: list[str] = []
    for first, second in TOKEN_BLOCK.findall(_style_text(_strip_comments(text))):
        blocks.append(first or second)
    return blocks


def _external_css_urls(text: str) -> list[str]:
    failures: list[str] = []
    for candidate in CSS_URL.findall(text):
        value = candidate.strip()
        if not value or value.startswith(("#", "data:")):
            continue
        parts = urlsplit(value)
        if parts.scheme == "https" and parts.hostname in {FONT_STYLE_HOST, FONT_FILE_HOST}:
            continue
        failures.append(value[:80])
    return failures


def _secret_failures(text: str) -> list[str]:
    return [name for name, pattern in SECRET_PATTERNS if pattern.search(text)]


def _text_failures(text: str, chosen_preset: str) -> list[str]:
    clean = _strip_comments(text)
    lowered = clean.lower()
    failures = [f"missing CSS marker: {marker}" for marker in CSS_MARKERS if marker not in lowered]
    blocks = _preset_blocks(clean)
    counts = Counter(blocks)
    if not blocks:
        failures.append("missing preset token block")
    for preset, count in counts.items():
        if preset not in PRESETS:
            failures.append(f"unknown preset: {preset}")
        if count > 1:
            failures.append(f"duplicate preset token block: {preset}")
    if len(counts) > 1:
        failures.append(f"multiple preset blocks: {sorted(counts)}")
    if chosen_preset and chosen_preset not in counts:
        failures.append(f"missing token block for chosen preset: {chosen_preset}")
    for theme in ("light", "dark"):
        if not re.search(rf"data-theme\s*=\s*['\"]?{theme}['\"]?", clean, re.IGNORECASE):
            failures.append(f"missing theme selector: {theme}")
    if "cdn.tailwindcss.com" in lowered:
        failures.append("Tailwind CDN is not allowed")
    if "replace_with" in lowered:
        failures.append("unresolved REPLACE_WITH placeholder")
    failures += [f"external CSS request is not allowed: {url}" for url in _external_css_urls(clean)]
    failures += [f"credential-shaped string detected: {name}" for name in _secret_failures(text)]
    return failures


def validate(path: Path) -> list[str]:
    if not path.is_file():
        return [f"not a regular file: {path}"]
    try:
        size = path.stat().st_size
        if size >= MAX_BYTES:
            return [f"file is {size} bytes; limit is {MAX_BYTES} (exclusive)"]
        data = path.read_bytes()
    except OSError as error:
        return [f"cannot read file: {error}"]
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError as error:
        return [f"file is not UTF-8: {error}"]
    parser = ReportParser()
    parser.feed(text)
    failures = _parser_failures(parser) + _csp_failures(parser)
    failures += _text_failures(text, parser.html_attrs.get("data-preset", ""))
    if parser.has_details and "details:not([open])" not in text.lower():
        failures.append("details present but print CSS does not expand closed details")
    if parser.has_chart:
        failures += [
            f"chart interaction marker missing: {marker}"
            for marker in CHART_MARKERS
            if marker not in text.lower()
        ]
    return failures


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("report", type=Path, help="Path to the generated HTML report")
    args = parser.parse_args()
    failures = validate(args.report)
    if failures:
        print(f"FAIL: {args.report}")
        for failure in failures:
            print(f"  - {failure}")
        return 1
    print(f"PASS: {args.report}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
