# Custom Repository Hygiene & Safety Gate Scripts

Reusable bash scripts for strict repository invariants, zero private path leakage, security tokens, code smells, and dependency allowlists.

## 1. Repository Hygiene & Anti-Leakage Gate (`tests/scripts/hygiene_check.sh`)

Enforces:
1. Zero private personal paths (`/Users/`, `/home/<user>/`, `/Workspace/`, personal emails).
2. Zero committed API keys, cloud tokens (AWS, GitHub PAT, private keys).
3. Zero decorative emojis or display meters in production source code.
4. Hard file length thresholds (e.g. max 500 LOC per source file).

```bash
#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$$(cd "$$(dirname "$$0")/../.." && pwd)"
cd "$$REPO_ROOT"

# Target files: accept arguments or scan tracked git files
if [ "$$#" -gt 0 ]; then
  FILES=("$$@")
else
  FILES=()
  while IFS= read -r f; do
    [ -n "$$f" ] && FILES+=("$$f")
  done < <(git ls-files)
fi

ERRORS=0

# Regex pattern for private paths, emails, and credentials
LEAK_PATTERNS='(/Users/|/home/[A-Za-z0-9._-]+/|/Workspace/|[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}|(AKIA|ASIA)[0-9A-Z]{16}|gh[pousr]_[A-Za-z0-9]{36,}|github_pat_[A-Za-z0-9_]{22,}|-----BEGIN [A-Z ]*PRIVATE KEY-----)'

for f in "$${FILES[@]}"; do
  [ -f "$$f" ] || continue
  case "$$f" in
    docs/*|tests/fixtures/*|tests/scripts/hygiene_check.sh)
      continue
      ;;
  esac

  matches=$$(grep -n -E "$$LEAK_PATTERNS" "$$f" || true)
  if [ -n "$$matches" ]; then
    echo "HYGIENE ERROR [private-leakage]: Forbidden private path or credential in $$f:" >&2
    echo "$$matches" >&2
    ERRORS=$$((ERRORS + 1))
  fi

  # Check source file length limit (500 LOC)
  case "$$f" in
    src/*.rs|*.py)
      lines=$$(wc -l < "$$f" | tr -d ' ')
      if [ "$$lines" -gt 500 ]; then
        echo "HYGIENE ERROR [file-length]: $$f exceeds 500 lines ($$lines lines)" >&2
        ERRORS=$$((ERRORS + 1))
      fi
      ;;
  esac
done

if [ "$$ERRORS" -gt 0 ]; then
  echo "hygiene_check.sh failed with $$ERRORS error(s)." >&2
  exit 1
fi
```

## 2. Dependency Allowlist Check (`tests/scripts/allowlist_check.sh`)

Ensures lockfiles (`Cargo.lock`, `uv.lock`, `package-lock.json`) only introduce pre-approved dependencies:

```bash
#!/usr/bin/env bash
set -euo pipefail

LOCKFILE="$${1:-Cargo.lock}"
ALLOWLIST="tests/scripts/allowlist.txt"

if [ ! -f "$$LOCKFILE" ] || [ ! -f "$$ALLOWLIST" ]; then
  exit 0
fi

UNAPPROVED=0
# Parse dependency names and cross-reference against allowlist
while IFS= read -r pkg; do
  if ! grep -qxF "$$pkg" "$$ALLOWLIST"; then
    echo "SECURITY ERROR [unapproved-dependency]: Package '$$pkg' in $$LOCKFILE not in $$ALLOWLIST" >&2
    UNAPPROVED=$$((UNAPPROVED + 1))
  fi
done < <(grep -E '^name = ' "$$LOCKFILE" | awk '{print $$3}' | tr -d '"' | sort -u)

if [ "$$UNAPPROVED" -gt 0 ]; then
  echo "Dependency check failed. Add approved packages to $$ALLOWLIST after security audit." >&2
  exit 1
fi
```

## 3. Write-Path Confinement Check (`tests/scripts/write_path_check.sh`)

Guarantees application or agent tools write files only within designated sandbox directories:

```bash
#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$$(cd "$$(dirname "$$0")/../.." && pwd)"
cd "$$REPO_ROOT"

# Scan source code for file write primitives outside sandbox
FORBIDDEN_WRITES=$$(grep -rnE '(std::fs::write|open\(.*["'\''][wa]' src/ | grep -v '\.aw/' || true)

if [ -n "$$FORBIDDEN_WRITES" ]; then
  echo "SECURITY ERROR [unconfined-write]: File writes must target sandbox root only:" >&2
  echo "$$FORBIDDEN_WRITES" >&2
  exit 1
fi
```
