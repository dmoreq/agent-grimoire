#!/usr/bin/env bash
set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TEST_HOME="$(mktemp -d)"
trap 'rm -rf -- "$TEST_HOME"' EXIT
export HOME="$TEST_HOME"

echo "==> Running test_setup_script.sh"

fail() {
    echo "FAIL: $*" >&2
    exit 1
}

assert_contains() {
    local haystack="$1" needle="$2" message="$3"
    printf '%s' "$haystack" | grep -Fq "$needle" || fail "$message"
}

assert_not_contains() {
    local haystack="$1" needle="$2" message="$3"
    if printf '%s' "$haystack" | grep -Fq "$needle"; then
        fail "$message"
    fi
}

# Test 1: Default dry-run must skip Rust skills and include core skills.
OUT_DEFAULT="$("$REPO_DIR/setup.sh" --dry-run)"
assert_not_contains "$OUT_DEFAULT" "skill rust-pro ->" "rust-pro was synced by default"
assert_not_contains "$OUT_DEFAULT" "skill rust-async-patterns ->" "rust-async-patterns was synced by default"
assert_not_contains "$OUT_DEFAULT" "skill pyo3-maturin ->" "pyo3-maturin was synced by default"
assert_not_contains "$OUT_DEFAULT" "skill flutter-architecture-data ->" "flutter-architecture-data was synced by default"
assert_not_contains "$OUT_DEFAULT" "skill dart-modern-idioms ->" "dart-modern-idioms was synced by default"
assert_contains "$OUT_DEFAULT" "skill code-minimalism ->" "code-minimalism was not synced"
assert_contains "$OUT_DEFAULT" "skill verify-and-stop ->" "verify-and-stop was not synced"
assert_contains "$OUT_DEFAULT" "skill ux-product-shaper ->" "ux-product-shaper was not synced"
assert_contains "$OUT_DEFAULT" "skill design-system ->" "design-system was not synced"
echo "  Default dry-run skips Rust and includes core skills"

# Test 2: --with-rust includes all Rust skills.
OUT_RUST="$("$REPO_DIR/setup.sh" --dry-run --with-rust)"
assert_contains "$OUT_RUST" "skill rust-pro ->" "rust-pro was not synced with --with-rust"
assert_contains "$OUT_RUST" "skill rust-async-patterns ->" "rust-async-patterns was not synced with --with-rust"
assert_contains "$OUT_RUST" "skill pyo3-maturin ->" "pyo3-maturin was not synced with --with-rust"
assert_not_contains "$OUT_RUST" "skill flutter-architecture-data ->" "flutter skill was synced with --with-rust"
echo "  --with-rust syncs Rust skills"

# Test 2b: --with-flutter includes Dart/Flutter skills and not Rust.
OUT_FLUTTER="$("$REPO_DIR/setup.sh" --dry-run --with-flutter)"
assert_contains "$OUT_FLUTTER" "skill dart-modern-idioms ->" "dart-modern-idioms was not synced with --with-flutter"
assert_contains "$OUT_FLUTTER" "skill flutter-architecture-data ->" "flutter-architecture-data was not synced with --with-flutter"
assert_not_contains "$OUT_FLUTTER" "skill rust-pro ->" "rust-pro was synced with --with-flutter"
echo "  --with-flutter syncs Dart/Flutter skills"

# Test 2c: --all includes both optional groups.
OUT_ALL="$("$REPO_DIR/setup.sh" --dry-run --all)"
assert_contains "$OUT_ALL" "skill rust-pro ->" "--all did not include Rust"
assert_contains "$OUT_ALL" "skill flutter-ui-responsive-a11y ->" "--all did not include Flutter"
echo "  --all syncs both optional groups"

# Test 3: Filtered hosts that read ~/.agents/skills also install portable skills.
for host in codex grok zed; do
    OUT_HOST="$("$REPO_DIR/setup.sh" --dry-run --host "$host")"
    assert_contains "$OUT_HOST" "skill code-minimalism ->" "$host did not target portable skills"
    case "$host" in
        codex) AGENT_PATH=".codex/AGENTS.md" ;;
        grok)  AGENT_PATH=".grok/AGENTS.md" ;;
        zed)   AGENT_PATH=".config/zed/AGENTS.md" ;;
    esac
    assert_contains "$OUT_HOST" "$AGENT_PATH" "$host rules file was not targeted"
    assert_not_contains "$OUT_HOST" "  prune " "$host pruned native skills on a clean sandbox"
done
OUT_CODEX="$("$REPO_DIR/setup.sh" --dry-run --host codex)"
assert_contains "$OUT_CODEX" ".codex/AGENTS.md" "codex was not listed in the summary"
echo "  Filtered hosts install the portable skill root"

# Test 4: Invalid host values are rejected before any write.
for bad in hermes portable,bogus; do
    if OUT_BAD="$("$REPO_DIR/setup.sh" --dry-run --host "$bad" 2>&1)"; then
        fail "--host $bad was accepted"
    fi
    assert_contains "$OUT_BAD" "unknown --host value" "--host $bad did not report an unknown host"
done
if OUT_EMPTY="$("$REPO_DIR/setup.sh" --dry-run --host "" 2>&1)"; then
    fail "--host with an empty value was accepted"
fi
assert_contains "$OUT_EMPTY" "requires a comma-separated host list" "empty --host did not report a usage error"
if OUT_MISSING="$("$REPO_DIR/setup.sh" --dry-run --host 2>&1)"; then
    fail "--host without a value was accepted"
fi
assert_contains "$OUT_MISSING" "requires a comma-separated host list" "missing --host value did not report a usage error"
echo "  Invalid host values are rejected"

# Test 5: Non-dry portable install writes 27 base skills and no optional skills.
INSTALL_HOME="$TEST_HOME/install"
HOME="$INSTALL_HOME" "$REPO_DIR/setup.sh" --host portable >/dev/null
SKILL_COUNT="$(find "$INSTALL_HOME/.agents/skills" -mindepth 1 -maxdepth 1 -type d | wc -l | tr -d ' ')"
[[ "$SKILL_COUNT" == "27" ]] || fail "portable install wrote $SKILL_COUNT skills, expected 27"
[[ -f "$INSTALL_HOME/.agents/skills/.agent-skills-managed" ]] || fail "portable install did not write a manifest"
[[ ! -d "$INSTALL_HOME/.agents/skills/rust-pro" ]] || fail "portable install included rust-pro"
[[ ! -d "$INSTALL_HOME/.agents/skills/flutter-architecture-data" ]] || fail "portable install included Flutter by default"
echo "  Non-dry portable install writes 27 base skills and a manifest"

# Test 5b: --with-flutter installs 35 skills including Dart/Flutter.
FLUTTER_HOME="$TEST_HOME/flutter"
HOME="$FLUTTER_HOME" "$REPO_DIR/setup.sh" --host portable --with-flutter >/dev/null
FLUTTER_COUNT="$(find "$FLUTTER_HOME/.agents/skills" -mindepth 1 -maxdepth 1 -type d | wc -l | tr -d ' ')"
[[ "$FLUTTER_COUNT" == "35" ]] || fail "flutter install wrote $FLUTTER_COUNT skills, expected 35"
[[ -f "$FLUTTER_HOME/.agents/skills/flutter-architecture-data/SKILL.md" ]] || fail "flutter install missing flutter-architecture-data"
[[ -f "$FLUTTER_HOME/.agents/skills/dart-modern-idioms/SKILL.md" ]] || fail "flutter install missing dart-modern-idioms"
[[ ! -d "$FLUTTER_HOME/.agents/skills/rust-pro" ]] || fail "flutter install included rust-pro"
echo "  --with-flutter installs 35 skills including Dart/Flutter"

# Test 5c: running without Flutter removes previously installed Flutter skills.
HOME="$FLUTTER_HOME" "$REPO_DIR/setup.sh" --host portable >/dev/null
REVOKED_COUNT="$(find "$FLUTTER_HOME/.agents/skills" -mindepth 1 -maxdepth 1 -type d | wc -l | tr -d ' ')"
[[ "$REVOKED_COUNT" == "27" ]] || fail "revoke left $REVOKED_COUNT skills, expected 27"
[[ ! -e "$FLUTTER_HOME/.agents/skills/flutter-architecture-data" ]] || fail "revoke kept flutter-architecture-data"
[[ ! -e "$FLUTTER_HOME/.agents/skills/dart-modern-idioms" ]] || fail "revoke kept dart-modern-idioms"
[[ -f "$FLUTTER_HOME/.agents/skills/code-review/SKILL.md" ]] || fail "revoke removed a base skill"
echo "  Running without Flutter revokes Dart/Flutter skills"

# Test 6: --host codex installs portable skills and does not create native skills.
CODEX_HOME="$TEST_HOME/codex"
HOME="$CODEX_HOME" "$REPO_DIR/setup.sh" --host codex >/dev/null
[[ -f "$CODEX_HOME/.agents/skills/code-review/SKILL.md" ]] || fail "codex did not install portable skills"
[[ -f "$CODEX_HOME/.codex/AGENTS.md" ]] || fail "codex rules file was not written"
[[ ! -e "$CODEX_HOME/.codex/skills/code-review" ]] || fail "codex created a native skill copy"
echo "  --host codex installs portable skills and codex rules"

# Test 7: Project install preserves custom sections and is idempotent.
PROJECT="$TEST_HOME/project"
mkdir -p "$PROJECT"
printf '## My Team\nKeep this section.\n' > "$PROJECT/AGENTS.md"
(cd "$PROJECT" && HOME="$INSTALL_HOME" "$REPO_DIR/setup.sh" --project >/dev/null)
grep -Fq "## My Team" "$PROJECT/AGENTS.md" || fail "project install lost a custom section"
grep -Fq "Keep this section." "$PROJECT/AGENTS.md" || fail "project install lost custom section content"
BACKUPS_BEFORE="$(find "$PROJECT" -maxdepth 1 -name 'AGENTS.md.bak.*' | wc -l | tr -d ' ')"
[[ "$BACKUPS_BEFORE" == "1" ]] || fail "project install created $BACKUPS_BEFORE backups, expected 1"
(cd "$PROJECT" && HOME="$INSTALL_HOME" "$REPO_DIR/setup.sh" --project >/dev/null)
BACKUPS_AFTER="$(find "$PROJECT" -maxdepth 1 -name 'AGENTS.md.bak.*' | wc -l | tr -d ' ')"
[[ "$BACKUPS_AFTER" == "1" ]] || fail "idempotent project install created another backup"
echo "  Project install preserves custom sections and is idempotent"

# Test 8: Invalid OpenCode JSON fails before writing rules.
OC_BAD_HOME="$TEST_HOME/opencode-bad"
mkdir -p "$OC_BAD_HOME/.config/opencode"
printf '{,}\n' > "$OC_BAD_HOME/.config/opencode/opencode.json"
if HOME="$OC_BAD_HOME" "$REPO_DIR/setup.sh" --host opencode >/tmp/opencode-bad.out 2>&1; then
    fail "invalid OpenCode JSON was accepted"
fi
[[ ! -f "$OC_BAD_HOME/.config/opencode/AGENTS.md" ]] || fail "rules were written despite invalid OpenCode JSON"
echo "  Invalid OpenCode JSON fails before writing rules"

# Test 9: A symlinked skill root pointing at the source tree is refused.
LINK_HOME="$TEST_HOME/link"
mkdir -p "$LINK_HOME/.agents"
ln -s "$REPO_DIR/skills" "$LINK_HOME/.agents/skills"
if HOME="$LINK_HOME" "$REPO_DIR/setup.sh" --host portable >/tmp/symlink.out 2>&1; then
    fail "setup.sh wrote through a symlink into the source tree"
fi
[[ -f "$REPO_DIR/skills/html-report/SKILL.md" ]] || fail "setup.sh deleted a source skill"
echo "  Symlinked source-tree root is refused"

# Test 10: Dry-run did not write into the isolated HOME for the earlier tests.
[[ -d "$INSTALL_HOME/.agents/skills" ]] || fail "non-dry install did not create the expected root"
echo "  Tests used an isolated HOME"

echo "==> All setup script tests passed!"
