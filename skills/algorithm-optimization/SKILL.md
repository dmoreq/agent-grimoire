---
name: algorithm-optimization
description: >-
  Improve quality KPIs (accuracy, F1, Hit@K, error rate) on real cases while protecting healthy ones.
  Not for Python runtime/memory profiling or one-off syntax cleanup.
risk: safe
source: local
date_added: "2026-08-23"
---

# Algorithm Optimization Skill

Systematically improve algorithm or ranking quality KPIs on real evaluation cases through root-cause isolation, controlled ablations, and strict regression guardrails.

- Load `references/headline-metric-audit.md` when verifying a repo's reported accuracy, auditing evaluator bugs, or running a 4-cell code/data ablation.
- Load `references/approach-selection-matrix.md` when comparing candidate models/representations across accuracy, storage, latency, and complexity.
- Load `references/search-ranking-evaluation.md` when evaluating search/ranking Hit@K, candidate-pool vs. ranking misses, bounded-demotion guards, or feature-store compression.
- Load `references/query-suggestion-experiments.md` when the arm suggests or completes strings before submission (autocomplete, typeahead, prefix/suffix backoff), or when the log has submitted events only and no keystroke/impression/acceptance columns.

## When to Use
- Optimizing accuracy, F1, Hit@K, MRR, calibration, or error rate on labeled/logged cases
- Diagnosing why specific slices or cohorts underperform
- Auditing whether a regression came from code changes, data/vocabulary rebuilds, or scorer bugs
- Compressing model/lookup artifacts subject to a quality non-inferiority floor

## When Not to Use
- No evaluation dataset or measurable quality metric exists
- Runtime CPU/memory/I/O profiling with unchanged outputs (`python-performance`)
- Exploratory dataset profiling or A/B experiment design (`data-science`)

## Related Skills
- Use **aw-first** to trace execution paths and call hierarchies (`aw path`, `aw callers`, `aw context`).
- Use **data-science** for statistical significance testing and experiment design.
- Use **python-performance** when the bottleneck is latency, CPU, or RAM rather than quality KPIs.
- Use **data-visualization** for before/after KPI charts. Save Markdown via **technical-reporting** or a single-file HTML page via **html-report**.

## Optimization Loop

### Step 1: Pin Contract & Verify Baseline Scorer
1. **Pin the Metric Contract**: Define target/intent filters, whether unlabeled/abandoned cases enter the denominator, and sample design (natural mix vs. stratified quotas). Never substitute an all-cohort score for a focus-cohort goal.
2. **Re-derive Headline Numbers with an Independent Scorer**: Shipped evaluators frequently contain off-by-one counters, length-mismatch skips, or dropped empty records. Score the baseline prediction file with an independent per-item counter and use the verified fair score as the baseline (`references/headline-metric-audit.md`).
3. **Four-Cell Code/Data Ablation**: When both algorithm code and data/vocabulary artifacts changed, run all four combinations (`old-code/old-data`, `old-code/new-data`, `new-code/old-data`, `new-code/new-data`) to isolate whether code or data caused the delta.
4. **Measure the Structural Ceiling**: Compute the candidate/representation ceiling (share of cases where the gold answer exists in the candidate pool) and context-free baseline before proposing a larger model family.
5. **Measure Real Surface Calls**: Verify actual call sites before claiming savings; search-on-submit surfaces incur zero typing calls (`references/query-suggestion-experiments.md`).
6. **Harness Equivalence Gate**: Verify canonical reader predictions match a naive independent scan with identical per-case result lists, not just aggregate metrics.
7. **Scoped Slices First**: Slice metrics by target population (e.g. prefix length, region) and report the scoped slice as primary headline.
8. **Constant Mutability & Reproducibility**: Ensure all gate constants affect outcomes at call time. Require deterministic builds with identical SHA-256 digests.
9. **Single Normalizer / Tokenizer**: Share normalization logic between miner and verifier to prevent drift.

### Step 2: Compute Integer Thresholds & Segment Cases
1. Convert percentage targets into exact integer hit counts: `ceil(target * denominator)` for `>= target`, or `floor(target * denominator) + 1` for `> target`. Subtract current hits to find the required net gain.
2. Segment misses into **rerankable** (target present in candidate pool outside top K), **retrieval/coverage misses** (target indexed/valid but absent from candidate pool), and **unreachable** (target absent from catalog/index or invalid label). Treat each segment's size as an upper bound, never an expected gain.

### Step 3: Isolate Low-Performance & Lock Healthy Guardrails
- Separate failing cases by stage while locking previously passing cases (`Hit@1` and `Rank 2–K`) as a regression guardrail cohort.

### Step 4: Classify Failure Cause
- **Input Data / Label Issue** (noise, stale catalog snapshot, bad gold label): Document and report; never mutate algorithm logic to overfit bad labels. Prove data causes before pruning: attribute error mass, verify candidate tokens across multiple sources, and guard proven valid tokens (`MUST_KEEP`).
- **Retrieval / Candidate Pool Issue** (target filtered out or truncated before scoring): Fix upstream retrieval, normalization, or candidate merging first; reranker tuning cannot rescue absent candidates (`references/search-ranking-evaluation.md`).
- **Scoring / Ranking / Post-Processing Issue**: Proceed to Step 5.

### Step 5: Root-Cause & Ablation Analysis
- Trace the full pipeline path (normalization → retrieval → prior hydration → scoring → priority tiers → deduplication → post-rank refinement).
- Build ablations by patching the real evaluation driver (deep-copying candidate objects if scoring mutates them) rather than writing a simplified replay that drops production stages.
- Before recommending that a sparse lookup table be dropped (e.g., "only 19% hit rate"), measure accuracy **with and without** it on the same scorer—the miss/fallback path often carries the discriminative signal. If dropping it loses accuracy, optimize the **container representation** (e.g., `marisa_trie` or sorted byte arrays) rather than pruning the model (`references/approach-selection-matrix.md`).
- Before proposing a higher-order model (e.g., trigram over bigram), count how many evaluation positions actually have lower-order support in the corpus; near-zero support guarantees near-zero gain.

### Step 6: Plan Bounded, Generalizable Improvements
- Prefer general mechanisms (normalization, candidate window policy, calibrated priors) over per-query or per-entity hardcoded exceptions.
- Never use evaluation labels at inference time.
- When optimizing `Hit@K` under a `Hit@1` floor, evaluate both on the same paired cohort and require positive net validation gain over baseline before touching the one-time holdout set.

### Step 7: Implement, Re-run, and Verify on Holdout
- Write a targeted regression test for the failure mechanism first.
- Enforce chronological/out-of-time splits when feature stores or click priors are involved so future interactions never leak into validation (`references/search-ranking-evaluation.md`).
- For long batch replays, write atomic per-batch checkpoints under an `in_progress` name stamped with source and manifest hashes; promote to `full_verified` only when `completed + failed == input` and unique IDs match.
- Re-evaluate on both **previously failing cases** and **healthy baseline cases**. Roll back or revise if healthy-case regressions exceed the budget.

### Step 8: Report with Explicit Denominators
- Present a baseline-vs-after table showing explicit fractions (`hits / cohort_size = %`) for both the focus cohort and the parent cohort.
- Clearly distinguish `measured` values from `reported` or `est.` figures.

## Final Checklist
- [ ] Baseline re-verified with an independent fair scorer and explicit denominators
- [ ] Four-cell code/data ablation and candidate ceiling checked before model changes
- [ ] Retrieval misses separated from ranking/scoring misses
- [ ] Ablations executed on the real pipeline with deep-copied candidates
- [ ] Healthy-case regression floor and untouched holdout verified
