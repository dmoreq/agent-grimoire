#!/usr/bin/env bash
set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TMP="$(mktemp -d "${TMPDIR:-/tmp}/precept-test.XXXXXX")"
cleanup() {
    rm -rf -- "$TMP"
    rm -f "$REPO_DIR/.zcode/secret.md" "$REPO_DIR/docs/reports/secret.html"
}
trap cleanup EXIT

echo "==> Running test_package_script.sh"

fail() {
    echo "FAIL: $*" >&2
    exit 1
}

assert_contains() {
    local haystack="$1" needle="$2" message="$3"
    printf '%s' "$haystack" | grep -Fq "$needle" || fail "$message"
}

# Untracked sentinels must never enter a git-archive bundle.
mkdir -p "$REPO_DIR/.zcode" "$REPO_DIR/docs/reports"
printf 'private plan\n' > "$REPO_DIR/.zcode/secret.md"
printf '<html>private</html>\n' > "$REPO_DIR/docs/reports/secret.html"

DIST="$TMP/dist"
mkdir -p "$DIST"
DIST_DIR="$DIST" "$REPO_DIR/package.sh" --bundle-only >/dev/null

[[ -f "$DIST/precept.tar.gz" ]] || fail "bundle tar was not created"
[[ -f "$DIST/precept.zip" ]] || fail "bundle zip was not created"
[[ ! -e "$DIST/skills.tar.gz" ]] || fail "--bundle-only created a skills archive"

TAR_LIST="$(tar -tzf "$DIST/precept.tar.gz")"
ZIP_LIST="$(unzip -Z1 "$DIST/precept.zip")"
for forbidden in '.zcode' 'docs/' '.env'; do
    if printf '%s' "$TAR_LIST" | grep -Fq "$forbidden"; then
        fail "bundle tar contains $forbidden"
    fi
    if printf '%s' "$ZIP_LIST" | grep -Fq "$forbidden"; then
        fail "bundle zip contains $forbidden"
    fi
done
assert_contains "$TAR_LIST" "precept/skills/html-report/SKILL.md" "bundle is missing a skill"
assert_contains "$TAR_LIST" "precept/rules/AGENTS.md" "bundle is missing rules"
assert_contains "$TAR_LIST" "precept/setup.sh" "bundle is missing setup.sh"
echo "  Bundle contains tracked content and excludes local state"

DIST2="$TMP/dist2"
mkdir -p "$DIST2"
DIST_DIR="$DIST2" "$REPO_DIR/package.sh" --skills-only >/dev/null
[[ -f "$DIST2/skills.tar.gz" ]] || fail "skills tar was not created"
[[ -f "$DIST2/skills.zip" ]] || fail "skills zip was not created"
[[ ! -e "$DIST2/precept.tar.gz" ]] || fail "--skills-only created a bundle archive"
assert_contains "$(tar -tzf "$DIST2/skills.tar.gz")" "html-report/SKILL.md" "skills archive is missing html-report"
echo "  Skills-only mode creates only skill archives"

if DIST_DIR="$TMP/dist3" "$REPO_DIR/package.sh" --bogus >/dev/null 2>&1; then
    fail "unknown package flag was accepted"
fi
if DIST_DIR="$TMP/dist3" "$REPO_DIR/package.sh" --skills-only --bundle-only >/dev/null 2>&1; then
    fail "mutually exclusive package modes were accepted"
fi
echo "  Unknown and conflicting flags are rejected"

# A failed zip build must not destroy the previous bundle tar.
OLD="$TMP/dist4"
mkdir -p "$OLD"
printf 'old archive\n' > "$OLD/precept.tar.gz"
REAL_GIT="$(command -v git)"
mkdir -p "$TMP/bin"
cat > "$TMP/bin/git" <<EOF
#!/usr/bin/env bash
for arg in "\$@"; do
    if [[ "\$arg" == "--format=zip" ]]; then
        echo "simulated zip failure" >&2
        exit 1
    fi
done
exec "$REAL_GIT" "\$@"
EOF
chmod +x "$TMP/bin/git"
if PATH="$TMP/bin:$PATH" DIST_DIR="$OLD" "$REPO_DIR/package.sh" --bundle-only >/dev/null 2>&1; then
    fail "package.sh succeeded despite a simulated zip failure"
fi
assert_contains "$(cat "$OLD/precept.tar.gz")" "old archive" "failed build destroyed the previous archive"
echo "  Failed build preserves the previous archive"

echo "==> All package script tests passed!"
