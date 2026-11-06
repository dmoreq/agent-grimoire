# Semantic Duplication Matrix

Load this reference when classifying harvest alerts. Do not treat name overlap as proof of a safe merge.

## Dimensions

1. **Variable / Variable** — Boolean or string flags (`is_`, `has_`, `can_`, `enable_`, `use_`) whose tokens overlap an Enum name or member. Canonical home is the Enum.
2. **Function / Function** — Helpers in different files sharing two or more name tokens with Jaccard >= 0.5. Candidate for one shared function. Same-file pairs are ignored.
3. **Function / Variable** — `get_`/`calc_`/`check_`/`is_` (or camelCase `getX`) functions that overlap a CONSTANT on two or more tokens. Prefer the constant or a lookup table.
4. **Function / Module** — Raw HTTP or client calls (`requests`, `urllib.request`, `http.client`, `fetch`, `axios`, `http.Get`, `reqwest`, `dio`) while a `*client*` or `*sdk*` symbol exists. Candidate bypass, not a rewrite.
5. **Type / Type** — Models or interfaces in different files sharing two or more name tokens (DTO clones). One shared token is not enough.

## Python-only candidates

- Pass-through wrappers: body is one call or return-call.
- Dead code: zero inbound call-count. Skip `_` names, `main`/`run`/`handler`, and route/fixture/HTTP-method decorators. This list is not proof of unused public API.

## Confidence

- **HIGH**: token overlap on flags vs Enum; Jaccard >= 0.7 on functions.
- **MEDIUM**: constants vs calculators, DTO clones, HTTP bypass.

Regex harvest for TypeScript, Dart, Go, and Rust is approximate. Confirm each alert by reading the two files before proposing a canonical symbol.

## Optional synonyms

Pass `--synonyms map.json` with `{"token": "canonical-token"}` when a domain uses aliases. The default map is empty.
