# Precept Repository Rules

Repository-specific conventions for `precept`. Global agent rules live in `rules/AGENTS.md`.

## Release Checklist
When releasing any new version (`vX.Y.Z` — major, minor, or micro/patch), complete every step below in order:

1. **Update Documentation**:
   - Add the `## [X.Y.Z] - YYYY-MM-DD` section to `CHANGELOG.md`.
   - Update `README.md` whenever skill counts, installer flags, workflows, or documented rules change.
2. **Verify & Package**:
   - Run the full CI check suite:
     - `ruff check tests skills/*/scripts/*.py`
     - `python3 -m pytest -n 4 tests/ -q`
     - `bash tests/test_setup_script.sh`
     - `bash tests/test_package_script.sh`
     - `bash -n setup.sh package.sh tests/*.sh`
   - Commit on branch `release/vX.Y.Z`, create tag `vX.Y.Z`, and run `./package.sh` to refresh `dist/` archives.
3. **Create Pull Request**:
   - Push `release/vX.Y.Z` and tag `vX.Y.Z` to `origin`.
   - Create a PR targeting `main` with `gh pr create --base main --head release/v4.2.1` (substituting the release branch).
4. **Install to All Host Agents**:
   - Run `./setup.sh` (without `--host` filtering) to sync the updated `rules/AGENTS.md` and skills to all detected agents on the host.
