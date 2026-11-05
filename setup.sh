#!/usr/bin/env bash
# Sync Global Agent Rules + Skills to Antigravity, Grok Build, OpenCode, Codex, Zed, and ZCode.
# Default: user-global, skips Rust skills. See --help.
set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
RULES_FILE="$REPO_DIR/rules/AGENTS.md"
SKILLS_DIR="$REPO_DIR/skills"

SCOPE="user"          # user | project
MODE="copy"           # copy | link
DRY_RUN=false
FORCE=false
MIRROR_NATIVE=false   # also copy skills into native host dirs (duplicates ~/.agents)
HOSTS_FILTER=""       # empty = auto-detect
HOSTS_FILTER_SET=false
SUPPORTED_HOSTS=("portable" "antigravity" "grok" "opencode" "codex" "zed" "zcode")
WITH_RUST=false       # skip Rust skills by default
WITH_FLUTTER=false    # skip Flutter/Dart skills by default

# Rust skills skipped by default unless --with-rust is passed
RUST_SKILLS=("rust-pro" "rust-async-patterns" "pyo3-maturin")

# Flutter/Dart skills skipped by default unless --with-flutter is passed
FLUTTER_SKILLS=(
    "dart-modern-idioms"
    "flutter-architecture-data"
    "flutter-codegen-release"
    "flutter-navigation-routing"
    "flutter-performance-optimization"
    "flutter-state-management"
    "flutter-testing-verification"
    "flutter-ui-responsive-a11y"
)

usage() {
    cat <<'EOF'
Usage: ./setup.sh [options]

Install this repo's rules (AGENTS.md) and skills to coding agents.

Options:
  --project          Install into the current directory (.agents/skills, AGENTS.md)
  --user             Install user-global (default)
  --host LIST        Comma-separated: antigravity,grok,opencode,codex,zed,zcode,portable
                     Default: portable + antigravity always; grok/opencode/codex/zed/zcode if detected
  --with-rust        Include Rust skills (rust-pro, rust-async-patterns, pyo3-maturin). Default: skipped.
  --without-rust     Skip Rust skills (default).
  --with-flutter     Include Flutter/Dart skills. Default: skipped.
  --without-flutter  Skip Flutter/Dart skills (default).
  --all              Include both Rust and Flutter/Dart skills (all 38). The default already targets every detected host.
  --link             Symlink skill folders from this repo (dev). Default is copy.
  --mirror-native    Also copy skills into native host dirs (duplicates ~/.agents/skills; for old hosts)
  --force            Replace unmanaged same-name skill dirs and create host dirs even if the product is not detected
  --dry-run          Print destinations; do not write
  -h, --help         Show this help

Canonical skill path (all modern hosts scan it):
  ~/.agents/skills/<name>/SKILL.md

Native extras (hosts that do not reliably use ~/.agents/skills):
  Antigravity IDE    ~/.gemini/config/skills
  Antigravity CLI    ~/.gemini/antigravity-cli/skills
  ZCode Desktop      ~/.zcode/skills (rules: ~/.zcode/AGENTS.md)
EOF
}

log() { printf '%s\n' "$*"; }

have_cmd() { command -v "$1" >/dev/null 2>&1; }

detected_antigravity() {
    [[ -d "$HOME/.gemini" ]] || have_cmd agy || have_cmd gemini || have_cmd antigravity
}

detected_grok() {
    [[ -d "$HOME/.grok" ]] || have_cmd grok
}

detected_opencode() {
    [[ -d "$HOME/.config/opencode" ]] || [[ -d "$HOME/.opencode" ]] || have_cmd opencode
}

detected_codex() {
    [[ -d "$HOME/.codex" ]] || have_cmd codex || [[ -d "/Applications/ChatGPT.app/Contents/Resources/codex-cli" ]]
}

detected_zed() {
    [[ -d "$HOME/.config/zed" ]] || have_cmd zed || [[ -d "/Applications/Zed.app" ]]
}

detected_zcode() {
    [[ -d "$HOME/.zcode" ]] || [[ -d "/Applications/ZCode.app" ]]
}

is_rust_skill() {
    local name="$1"
    for r in "${RUST_SKILLS[@]}"; do
        [[ "$name" == "$r" ]] && return 0
    done
    return 1
}

is_flutter_skill() {
    local name="$1"
    for f in "${FLUTTER_SKILLS[@]}"; do
        [[ "$name" == "$f" ]] && return 0
    done
    return 1
}

should_skip_skill() {
    local name="$1"
    if ! $WITH_RUST && is_rust_skill "$name"; then
        return 0
    fi
    if ! $WITH_FLUTTER && is_flutter_skill "$name"; then
        return 0
    fi
    return 1
}

host_wanted() {
    local name="$1"
    if $HOSTS_FILTER_SET; then
        case ",$HOSTS_FILTER," in
            *",$name,"*) return 0 ;;
        esac
        # These hosts read ~/.agents/skills and have no native skill root.
        if [[ "$name" == "portable" ]]; then
            case ",$HOSTS_FILTER," in
                *",grok,"*|*",opencode,"*|*",codex,"*|*",zed,"*) return 0 ;;
            esac
        fi
        return 1
    fi
    case "$name" in
        portable|antigravity) return 0 ;;
        grok)     detected_grok || $FORCE ;;
        opencode) detected_opencode || $FORCE ;;
        codex)    detected_codex || $FORCE ;;
        zed)      detected_zed || $FORCE ;;
        zcode)    detected_zcode || $FORCE ;;
        *)        return 1 ;;
    esac
}

# Resolve a path, including a symlink target, without requiring the file to exist.
resolve_path() {
    local path="$1"
    if [[ -e "$path" || -L "$path" ]]; then
        python3 - "$path" <<'PY'
import pathlib, sys
print(pathlib.Path(sys.argv[1]).resolve())
PY
        return 0
    fi
    local parent
    parent="$(dirname "$path")"
    if [[ -d "$parent" ]]; then
        printf '%s/%s\n' "$(cd "$parent" && pwd -P)" "$(basename "$path")"
    else
        printf '%s\n' "$path"
    fi
}

assert_not_source_tree() {
    local dest="$1"
    [[ -e "$dest" || -L "$dest" ]] || return 0
    local dest_real repo_real
    dest_real="$(resolve_path "$dest")"
    repo_real="$(cd "$SKILLS_DIR" && pwd -P)"
    case "$dest_real/" in
        "$repo_real"/*)
            log "ERROR: refusing to write into the source tree: $dest_real"
            exit 1
            ;;
    esac
}

manifest_has() {
    local manifest="$1" name="$2"
    [[ -f "$manifest" ]] && grep -qxF "$name" "$manifest"
}

# True when an existing skill dir is an unmodified copy from this repo.
is_managed_copy() {
    local skill="$1" dest_skill="$2"
    [[ -f "$dest_skill/SKILL.md" ]] && cmp -s "$skill/SKILL.md" "$dest_skill/SKILL.md"
}

# Remove this repo's skill names from a dest (keeps unrelated user skills).
prune_our_skills() {
    local dest="$1"
    [[ -d "$dest" ]] || return 0
    assert_not_source_tree "$dest"
    local manifest="$dest/.agent-skills-managed"
    local skill name dest_skill
    for skill in "$SKILLS_DIR"/*; do
        [[ -d "$skill" ]] || continue
        name="$(basename "$skill")"
        dest_skill="$dest/$name"
        [[ -e "$dest_skill" || -L "$dest_skill" ]] || continue
        if manifest_has "$manifest" "$name" || is_managed_copy "$skill" "$dest_skill" || $FORCE; then
            if $DRY_RUN; then
                log "  prune $dest_skill"
            else
                rm -rf -- "$dest_skill"
            fi
        else
            log "  skip unmanaged $dest_skill (not installed by this repo; use --force)"
        fi
    done
    if ! $DRY_RUN && [[ -f "$manifest" ]]; then
        local tmp="$manifest.tmp.$$"
        : > "$tmp"
        while IFS= read -r name; do
            [[ -e "$dest/$name" || -L "$dest/$name" ]] && printf '%s\n' "$name" >> "$tmp"
        done < "$manifest"
        sort -u "$tmp" -o "$tmp"
        mv -f "$tmp" "$manifest"
    fi
}

# Overwrite only skill folders shipped by this repo. Other skills stay.
sync_skills() {
    local dest="$1"
    assert_not_source_tree "$dest"
    if ! $DRY_RUN; then
        mkdir -p "$dest"
    fi
    local manifest="$dest/.agent-skills-managed"
    local manifest_tmp="$dest/.agent-skills-managed.tmp.$$"
    if ! $DRY_RUN; then
        : > "$manifest_tmp"
    fi
    local skill name dest_skill stage
    for skill in "$SKILLS_DIR"/*; do
        [[ -d "$skill" ]] || continue
        name="$(basename "$skill")"
        dest_skill="$dest/$name"

        if should_skip_skill "$name"; then
            if [[ -e "$dest_skill" || -L "$dest_skill" ]]; then
                if manifest_has "$manifest" "$name" || is_managed_copy "$skill" "$dest_skill" || $FORCE; then
                    if $DRY_RUN; then
                        log "  prune skipped optional skill $name from $dest"
                    else
                        rm -rf -- "$dest_skill"
                    fi
                fi
            fi
            continue
        fi

        if [[ -e "$dest_skill" || -L "$dest_skill" ]]; then
            if ! manifest_has "$manifest" "$name" && ! is_managed_copy "$skill" "$dest_skill" && ! $FORCE; then
                log "  skip unmanaged $dest_skill (not installed by this repo; use --force)"
                continue
            fi
        fi

        if $DRY_RUN; then
            log "  skill $name -> $dest_skill"
            continue
        fi

        stage="$dest/.$name.tmp.$$"
        rm -rf -- "$stage"
        if [[ "$MODE" == "link" ]]; then
            ln -s "$skill" "$stage" || { rm -rf -- "$stage"; exit 1; }
        else
            cp -R "$skill" "$stage" || { rm -rf -- "$stage"; exit 1; }
        fi
        rm -rf -- "$dest_skill"
        mv "$stage" "$dest_skill"
        printf '%s\n' "$name" >> "$manifest_tmp"
    done
    if ! $DRY_RUN; then
        sort -u "$manifest_tmp" -o "$manifest_tmp"
        mv -f "$manifest_tmp" "$manifest"
    fi
}

install_rules_file() {
    local dest="$1"
    local src="$2"
    if $DRY_RUN; then
        log "  file -> $dest"
        return 0
    fi
    mkdir -p "$(dirname "$dest")"
    local target
    target="$(resolve_path "$dest")"
    local custom=""
    if [[ -f "$target" ]]; then
        custom="$(awk 'NR==FNR { if ($0 ~ /^## /) seen[$0]=1; next } /^## / { keep = !($0 in seen) } keep' "$src" "$target")"
    fi
    local tmp
    tmp="$(mktemp "${target}.tmp.XXXXXX")"
    if ! cat "$src" > "$tmp"; then
        rm -f "$tmp"
        return 1
    fi
    if [[ -n "$custom" ]]; then
        printf '\n%s\n' "$custom" >> "$tmp"
    fi
    if [[ -f "$target" ]] && cmp -s "$target" "$tmp"; then
        rm -f "$tmp"
        return 0
    fi
    if [[ -f "$target" ]]; then
        local backup="$target.bak.$(date +%Y%m%d%H%M%S).$$"
        cp -p "$target" "$backup"
        log "    backup -> $backup"
    fi
    chmod 644 "$tmp"
    mv -f "$tmp" "$target"
}

write_opencode_rules() {
    local rules_path="$HOME/.config/opencode/AGENTS.md"
    local config_file="$HOME/.config/opencode/opencode.json"
    if $DRY_RUN; then
        log "  file -> $rules_path"
        [[ -f "$config_file" ]] && log "  config -> $config_file"
        return 0
    fi
    if [[ -f "$config_file" ]]; then
        if ! python3 - "$config_file" "$rules_path" <<'PY'
import json, pathlib, sys
config_path = pathlib.Path(sys.argv[1])
rule_str = sys.argv[2]
try:
    data = json.loads(config_path.read_text(encoding="utf-8"))
except Exception as error:
    sys.exit(f"{config_path}: invalid JSON ({error})")
instructions = data.get("instructions", [])
if not isinstance(instructions, list):
    sys.exit(f"{config_path}: 'instructions' must be a list")
cleaned = [
    item for item in instructions
    if not (isinstance(item, str) and item.endswith("/opencode/AGENTS.md"))
]
if rule_str not in cleaned:
    cleaned.append(rule_str)
data["instructions"] = cleaned
backup = config_path.with_name(config_path.name + ".bak")
if not backup.exists():
    backup.write_bytes(config_path.read_bytes())
tmp = config_path.with_name(config_path.name + ".tmp")
tmp.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
tmp.replace(config_path)
PY
        then
            log "ERROR: cannot update $config_file; fix it manually and rerun."
            exit 1
        fi
    fi
    install_rules_file "$rules_path" "$RULES_FILE"
}

skill_count() {
    local n=0
    local d name
    for d in "$SKILLS_DIR"/*; do
        [[ -d "$d" ]] || continue
        name="$(basename "$d")"
        if should_skip_skill "$name"; then
            continue
        fi
        n=$((n + 1))
    done
    printf '%s' "$n"
}

# --- args ---
while [[ $# -gt 0 ]]; do
    case "$1" in
        --project) SCOPE="project"; shift ;;
        --user)    SCOPE="user"; shift ;;
        --host)
            if [[ $# -lt 2 || -z "$2" || "$2" == -* ]]; then
                log "ERROR: --host requires a comma-separated host list."
                usage
                exit 2
            fi
            HOSTS_FILTER="$2"
            HOSTS_FILTER_SET=true
            shift 2
            ;;
        --host=*)
            HOSTS_FILTER="${1#--host=}"
            if [[ -z "$HOSTS_FILTER" ]]; then
                log "ERROR: --host requires a comma-separated host list."
                usage
                exit 2
            fi
            HOSTS_FILTER_SET=true
            shift
            ;;
        --with-rust) WITH_RUST=true; shift ;;
        --without-rust) WITH_RUST=false; shift ;;
        --with-flutter) WITH_FLUTTER=true; shift ;;
        --without-flutter) WITH_FLUTTER=false; shift ;;
        --all)     WITH_RUST=true; WITH_FLUTTER=true; shift ;;
        --link)    MODE="link"; shift ;;
        --mirror-native) MIRROR_NATIVE=true; shift ;;
        --force)   FORCE=true; shift ;;
        --dry-run) DRY_RUN=true; shift ;;
        -h|--help) usage; exit 0 ;;
        *)
            log "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

HOSTS_FILTER="$(printf '%s' "$HOSTS_FILTER" | tr 'A-Z' 'a-z' | tr -d ' ')"
if $HOSTS_FILTER_SET; then
    IFS=',' read -r -a _requested_hosts <<< "$HOSTS_FILTER"
    for _host in "${_requested_hosts[@]}"; do
        if [[ -z "$_host" ]]; then
            log "ERROR: --host contains an empty value."
            exit 2
        fi
        if [[ " ${SUPPORTED_HOSTS[*]} " != *" $_host "* ]]; then
            log "ERROR: unknown --host value: $_host"
            exit 2
        fi
    done
fi

if [[ ! -f "$RULES_FILE" ]]; then
    log "Missing $RULES_FILE"
    exit 1
fi
if [[ ! -d "$SKILLS_DIR" ]]; then
    log "Missing $SKILLS_DIR"
    exit 1
fi

N_SKILLS="$(skill_count)"

log "========================================================"
log "==> Agent Skills Setup"
log "    repo:        $REPO_DIR"
log "    scope:       $SCOPE"
log "    mode:        $MODE"
log "    skills:      $N_SKILLS"
if $WITH_RUST; then
    log "    rust skills: enabled (rust-pro, rust-async-patterns, pyo3-maturin)"
else
    log "    rust skills: skipped by default (pass --with-rust to enable)"
fi
if $WITH_FLUTTER; then
    log "    flutter skills: enabled (8 Dart/Flutter skills)"
else
    log "    flutter skills: skipped by default (pass --with-flutter to enable)"
fi
$DRY_RUN && log "    dry-run:     yes"
log "========================================================"

INSTALLED=()

if [[ "$SCOPE" == "project" ]]; then
    PROJECT_SKILLS="$PWD/.agents/skills"
    PROJECT_AGENTS="$PWD/AGENTS.md"
    log "==> Project scope ($PWD)"
    log "    skills -> $PROJECT_SKILLS"
    log "    rules  -> $PROJECT_AGENTS"
    if ! $DRY_RUN; then
        mkdir -p "$PROJECT_SKILLS"
    fi
    sync_skills "$PROJECT_SKILLS"
    install_rules_file "$PROJECT_AGENTS" "$RULES_FILE"
    INSTALLED+=("project|$PROJECT_AGENTS|$PROJECT_SKILLS")
else
    # Portable Agent Skills root scanned by Grok, Codex, Zed, and other Agent Skills hosts.
    if host_wanted portable; then
        DEST="$HOME/.agents/skills"
        log "==> [portable] ~/.agents/skills"
        sync_skills "$DEST"
        INSTALLED+=("portable|-|$DEST")
    fi

    if host_wanted antigravity; then
        log "==> [antigravity] IDE + CLI"
        install_rules_file "$HOME/.gemini/GEMINI.md" "$RULES_FILE"
        sync_skills "$HOME/.gemini/config/skills"
        sync_skills "$HOME/.gemini/antigravity-cli/skills"
        INSTALLED+=("antigravity|$HOME/.gemini/GEMINI.md|$HOME/.gemini/config/skills + ~/.gemini/antigravity-cli/skills")
    elif [[ -z "$HOSTS_FILTER" ]]; then
        log "==> [antigravity] skipped (no ~/.gemini, agy, or gemini; pass --force or --host antigravity)"
    fi

    if host_wanted grok; then
        log "==> [grok] ~/.grok/AGENTS.md (skills via ~/.agents/skills)"
        install_rules_file "$HOME/.grok/AGENTS.md" "$RULES_FILE"
        if $MIRROR_NATIVE; then
            sync_skills "$HOME/.grok/skills"
            INSTALLED+=("grok|$HOME/.grok/AGENTS.md|$HOME/.grok/skills + ~/.agents/skills")
        else
            prune_our_skills "$HOME/.grok/skills"
            INSTALLED+=("grok|$HOME/.grok/AGENTS.md|~/.agents/skills")
        fi
    elif [[ -z "$HOSTS_FILTER" ]]; then
        log "==> [grok] skipped (Grok not detected)"
    fi

    if host_wanted opencode; then
        log "==> [opencode] ~/.config/opencode/AGENTS.md (skills via ~/.agents/skills)"
        write_opencode_rules
        INSTALLED+=("opencode|$HOME/.config/opencode/AGENTS.md|~/.agents/skills")
    elif [[ -z "$HOSTS_FILTER" ]]; then
        log "==> [opencode] skipped (OpenCode not detected)"
    fi

    if host_wanted codex; then
        log "==> [codex] ~/.codex/AGENTS.md (skills via ~/.agents/skills)"
        install_rules_file "$HOME/.codex/AGENTS.md" "$RULES_FILE"
        if $MIRROR_NATIVE; then
            sync_skills "$HOME/.codex/skills"
            INSTALLED+=("codex|$HOME/.codex/AGENTS.md|$HOME/.codex/skills + ~/.agents/skills")
        else
            prune_our_skills "$HOME/.codex/skills"
            INSTALLED+=("codex|$HOME/.codex/AGENTS.md|~/.agents/skills")
        fi
    elif [[ -z "$HOSTS_FILTER" ]]; then
        log "==> [codex] skipped (Codex not detected)"
    fi

    if host_wanted zed; then
        log "==> [zed] ~/.config/zed/AGENTS.md (skills via ~/.agents/skills)"
        install_rules_file "$HOME/.config/zed/AGENTS.md" "$RULES_FILE"
        INSTALLED+=("zed|$HOME/.config/zed/AGENTS.md|~/.agents/skills")
    elif [[ -z "$HOSTS_FILTER" ]]; then
        log "==> [zed] skipped (Zed not detected; pass --force or --host zed)"
    fi

    if host_wanted zcode; then
        log "==> [zcode] ~/.zcode/AGENTS.md + native skills root"
        install_rules_file "$HOME/.zcode/AGENTS.md" "$RULES_FILE"
        sync_skills "$HOME/.zcode/skills"
        INSTALLED+=("zcode|$HOME/.zcode/AGENTS.md|$HOME/.zcode/skills")
    elif [[ -z "$HOSTS_FILTER" ]]; then
        log "==> [zcode] skipped (ZCode not detected; pass --force or --host zcode)"
    fi
fi

log "========================================================"
if [[ ${#INSTALLED[@]} -eq 0 ]]; then
    log "Nothing installed. Use --force or --host antigravity,grok,opencode,codex,zed,zcode,portable"
    exit 1
fi
log "Done. Restart each agent session so it re-scans skills."
log ""
log "Host         Rules                                      Skills"
for row in "${INSTALLED[@]}"; do
    IFS='|' read -r host rules skills <<<"$row"
    printf '  %-12s %-43s %s\n' "$host" "$rules" "$skills"
done
log "========================================================"
log "Verify:"
log "  Antigravity: ask which skills are available, or /skills"
log "  Codex:       ask which skills are available, /skills, or codex exec 'What skills are installed?'"
log "  Grok Build:  grok inspect"
log "  Zed:         ask which skills are available in the Agent Panel, or /skills"
log "  OpenCode:    opencode debug config"
log "  ZCode:       Settings → Skills, or ask which skills are available"
log "========================================================"
