#!/usr/bin/env bash
set -euo pipefail

# Prevent macOS AppleDouble (._*) files from being added to archives
export COPYFILE_DISABLE=1

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DIST_DIR="${DIST_DIR:-$REPO_DIR/dist}"

usage() {
    cat <<'EOF'
Usage: ./package.sh [--skills-only | --bundle-only]

Build offline archives from tracked repository content.

Options:
  --skills-only   Package only skills.tar.gz and skills.zip
  --bundle-only   Package only agent-grimoire.tar.gz and agent-grimoire.zip
  --help          Show this help

Environment:
  DIST_DIR        Output directory (default: <repo>/dist)

The bundle is built from `git archive HEAD`, so untracked and ignored files
(.zcode/, docs/, .env, caches) are never included.
EOF
}

BUILD_SKILLS=true
BUILD_BUNDLE=true

case "${1:-}" in
    "")
        ;;
    --skills-only)
        BUILD_BUNDLE=false
        ;;
    --bundle-only)
        BUILD_SKILLS=false
        ;;
    -h|--help)
        usage
        exit 0
        ;;
    *)
        echo "ERROR: unknown option: $1" >&2
        usage >&2
        exit 2
        ;;
esac
if [[ $# -gt 1 ]]; then
    echo "ERROR: pass only one packaging mode." >&2
    usage >&2
    exit 2
fi

mkdir -p "$DIST_DIR"
STAGE="$(mktemp -d "$DIST_DIR/.stage.XXXXXX")"
trap 'rm -rf -- "$STAGE"' EXIT

BUNDLE_PREFIX="agent-grimoire"
BUILT=()

if $BUILD_SKILLS; then
    echo "==> Creating skills-only packages"
    git -C "$REPO_DIR" archive --format=tar.gz -o "$STAGE/skills.tar.gz" HEAD:skills
    git -C "$REPO_DIR" archive --format=zip -o "$STAGE/skills.zip" HEAD:skills
    BUILT+=("$STAGE/skills.tar.gz" "$STAGE/skills.zip")
fi

if $BUILD_BUNDLE; then
    echo "==> Creating full offline bundles from tracked content"
    git -C "$REPO_DIR" archive --format=tar.gz --prefix="$BUNDLE_PREFIX/" \
        -o "$STAGE/$BUNDLE_PREFIX.tar.gz" HEAD
    git -C "$REPO_DIR" archive --format=zip --prefix="$BUNDLE_PREFIX/" \
        -o "$STAGE/$BUNDLE_PREFIX.zip" HEAD
    BUILT+=("$STAGE/$BUNDLE_PREFIX.tar.gz" "$STAGE/$BUNDLE_PREFIX.zip")
fi

# Verify every archive before publishing. A failed build leaves the previous
# archives in DIST_DIR untouched.
for archive in "${BUILT[@]}"; do
    case "$archive" in
        *.tar.gz) tar -tzf "$archive" >/dev/null ;;
        *.zip)    unzip -t "$archive" >/dev/null ;;
    esac
done

if $BUILD_BUNDLE; then
    TAR_LIST="$(tar -tzf "$STAGE/$BUNDLE_PREFIX.tar.gz")"
    ZIP_LIST="$(unzip -Z1 "$STAGE/$BUNDLE_PREFIX.zip")"
    for forbidden in '/.zcode/' '/docs/' '/.git/' '/.env' '/.tmp/' '/dist/'; do
        if [[ "$TAR_LIST" == *"$forbidden"* ]]; then
            matches="$(printf '%s\n' "$TAR_LIST" | grep -F "$forbidden" | head -3 | tr '\n' ' ')"
            echo "ERROR: bundle contains forbidden path: $forbidden ($matches)" >&2
            exit 1
        fi
        if [[ "$ZIP_LIST" == *"$forbidden"* ]]; then
            echo "ERROR: bundle contains forbidden path: $forbidden" >&2
            exit 1
        fi
    done
    for required in "$BUNDLE_PREFIX/skills/html-report/SKILL.md" "$BUNDLE_PREFIX/rules/AGENTS.md" "$BUNDLE_PREFIX/setup.sh" "$BUNDLE_PREFIX/README.md"; do
        if ! grep -Fqx "$required" <<< "$TAR_LIST"; then
            echo "ERROR: bundle is missing required path: $required" >&2
            exit 1
        fi
    done
fi

# Publish only after every requested archive has been built and verified.
for archive in "${BUILT[@]}"; do
    mv -f "$archive" "$DIST_DIR/"
done

echo "========================================================"
echo "==> Summary of Generated Packages in $DIST_DIR:"
ls -lh "$DIST_DIR"/*.tar.gz "$DIST_DIR"/*.zip 2>/dev/null || true
echo "========================================================"
