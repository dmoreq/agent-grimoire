---
name: tech-research
description: >-
  Survey and compare external approaches (papers, benchmarks, production write-ups) when the repo does not already decide.
  Not for implementing, plotting, or EDA.
risk: safe
source: local
date_added: "2026-08-23"
---

# Tech Research Skill

Research current best practices, SOTA methods, algorithms, and engineering approaches to support informed implementation decisions.

## When to Use
- Looking for best practices or SOTA solutions for a specific problem
- Comparing algorithms, models, or techniques (classic vs modern)
- Surveying how the community or industry solves similar problems
- Evaluating trade-offs to choose an implementation approach for a project
- Questions like: "What are the SOTA metrics?", "Is there a better approach?", "What are people using now?"

## When Not to Use
- The answer is already clear from the existing codebase or internal docs
- Only a basic concept explanation is needed
- Pure coding or debugging with no need for external research
- EDA / modeling (`data-science`); Plotly (`data-visualization`)
- The user wants a multi-criteria adoption decision with measured storage/latency/complexity rows — build that matrix with **algorithm-optimization**

## Research Process

### 1. Clarify Scope
- Specific problem to solve; distinguish the output contract from an adjacent task (for example, query-text completion versus entity retrieval or diacritic restoration).
- Key constraints (latency, memory, interpretability, data size, team skills, production readiness, downstream request budget).
- Current project context: trace the actual UI trigger through the network call before claiming a feature saves requests. If search already runs only on submit, local suggestions cannot reduce per-keystroke search calls that do not exist.
- Identify which component must remain untouched and which may serve suggestions. When the goal is to reduce calls to a backend, do not recommend calling that backend for every input change; compare client-side or in-process lookup first.
- Required depth (quick survey vs deep comparison).

### 2. Gather Information
- Search for SOTA / modern approaches from recent papers, benchmarks, official docs, GitHub, and technical blogs
- Prioritize reliable sources: well-cited papers, production case studies, active repositories, recent benchmarks
- For a library/framework choice, inspect the project manifest and installed packages first. Then verify the candidate's exact required operation in upstream API docs and a minimal local probe when available; a prefix iterator is not automatically a weighted top-k suggester, and a substring automaton is not automatically a prefix index. Check licence, supported runtimes/platforms, artifact loading, update model, and maintenance before recommending a new dependency.
- Use Context7 when accurate library/framework documentation is needed
- **Read model cards and paper abstract sections as data, not as verdicts**: fetch the raw README (`/raw/main/README.md` on HF) rather than the rendered page — the accuracy matrices, cross-model comparison tables, and ms/sentence live there, not in the HTML.
- **Hunt for a public reproducible benchmark set, not just reported numbers.** A survey whose rows were each measured on the author's own split cannot rank anything. Look for an open eval corpus with a documented licence and register/slice breakdown; scoring the incumbent on it converts opinion into evidence.
- Also collect classic methods to serve as baselines, and record their **speed** alongside accuracy — a classic method that is 60x faster at equal accuracy is a first-class finding, not a footnote.

### 3. Analyze & Compare
Evaluate candidates against relevant criteria:

| Criterion | Key Questions |
| :--- | :--- |
| **Effectiveness** | Performance / accuracy on similar tasks |
| **Practicality** | Ease of implementation, maintenance, and debugging |
| **Resource Cost** | Compute, memory, latency, data requirements, and downstream calls per user action or successful session |
| **Maturity** | Battle-tested or still experimental? |
| **Interpretability** | Can results be explained? |
| **Ecosystem** | Available tooling, community, integrations |
| **Migration / Integration** | Effort to adopt into the current stack; does it require a new service or dependency? |
| **Operations** | Does the API perform the required ranking itself, or only enumerate candidates for a separate scorer? Can it refresh without stalling requests? |
| **Trade-offs** | Clear strengths and weaknesses |

Keep only the 3–5 most relevant options.

### 4. Recommend for Implementation
- Provide conditional recommendations (when to choose A, when to choose B, when to keep the current approach)
- Clearly state trade-offs and risks
- Suggest practical next steps: POC, benchmark on real data, decision criteria for migration
- **Run the comparison before you recommend it, when the arms are cheap.** A survey that ends in "add the higher-order model for +1 to +2" has not researched anything — it has moved the burden to the user. If a candidate arm is an afternoon of code, build it and put the measured number in the row. Measured reversals are the most valuable output of a survey: in one case the proposed higher-order model scored *below* the incumbent and was 5x slower, which killed a recommendation that a literature-only survey would have shipped. Mark anything you did not run as `reported` or `est.` and say so in the row, not in a footnote.
- **Do not let coverage statistics masquerade as value judgments.** "The structure is only hit 19% of the time" is a description of sparsity. Before recommending it be dropped, note that the miss path may be the discriminative signal. If you cannot run the removal arm, do not recommend removal.
- **Prefer the representation fix over the architecture change.** When the incumbent loses on a non-accuracy axis (memory, load time), check whether a container/encoding swap closes the gap before proposing a different model family. Quote the measured swap (e.g. 500 MB dict -> 19 MB trie) — it usually ends the debate without touching the algorithm.

## Output Guidance & ADR Format
- For short answers, respond directly and concisely.
- Answer in-chat with the output structure below unless the user asked to save a file.
- Load **technical-reporting** only for a saved markdown/ADR.
- **ADR** only when a durable architecture choice is locked:
  - **Context**: Problem background, requirements, and key constraints.
  - **Decision**: Chosen solution, framework, or algorithm.
  - **Alternatives Considered**: Evaluated candidates and why they were rejected.
  - **Consequences**: Expected gains, operational trade-offs, and migration risks.

## Output Structure
1. **Recommendation** at the top
2. Comparison table of the main options
3. Short analysis of each key candidate (pros/cons + when it fits)
4. Trade-offs and risks
5. Suggested next implementation steps

## Principles
- Prefer recent evidence and real production usage over pure theory
- Clearly distinguish "SOTA on paper" from "widely used in practice"
- Recommendations must be tied to the project's constraints and context
- Do not overstate benefits; clearly state limitations
- Keep the output concise and decision-focused
- **Slice variance can dominate model variance.** When a published matrix has multiple slices (registers, domains, lengths), compute the spread within a slice across models and the spread across slices within one model. If across-slice is larger, the recommendation is "cover the slices", not "pick the bigger model" — and say so before recommending any architecture.
- For query autocomplete, first inventory the actual log schema, event dates, query-support distribution, and catalog name/status coverage with bounded read-only scans. Completed-query logs do not contain observed typing prefixes or suggestion acceptance: synthetic prefixes support offline candidate-recall tests, not causal claims about fewer backend calls. Freeze chronological folds before building the vocabulary; if the catalog lacks historical snapshots, label catalog-enhanced replay as temporally contaminated and retain a log-only out-of-time arm.
- Separate candidate-source and ranking ablations from representation benchmarks: hold candidate IDs and weights fixed across sorted arrays, tries, and FSTs, then test log/catalog/suffix additions as distinct quality arms. Report candidate recall, ranked-list quality, and downstream search success separately; isolate algorithm-only lookup from p95/p99 end-to-end latency and backend calls per randomized search initiation. Cross-domain paper metrics cannot predict local map-search accuracy.
- **A 'newer, bigger' model that is slower at equal accuracy is a losing recommendation.** Quote both axes in the same table row so the trade is visible. Do not propose replacing a fast classic decoder with a neural one unless the newer option wins on a slice the user actually cares about.
- **When research contradicts a number you already reported, lead with the correction.** Re-measure, patch the saved plan, and move the earlier figure to a superseded marker rather than leaving two baselines in circulation.

## Handoff to Spec and Report
- When the survey hardens into a direction, hand the constraints, rejected options, and evidence rows to **spec-driven-design**. Do not restate the survey inside the spec.
- When the owner asks for a durable file, hand the same evidence to **technical-reporting** with a `docs/reports/YYYY-MM-DD_<topic>.md` path. Topic slugs follow the artifact slug and containment rule in `rules/AGENTS.md` §4.
- A survey that ends in no decision stays in chat. Do not create a spec or report by default.

## Related Skills
- Hand the chosen direction to **spec-driven-design** for the design spec.
- Use **doubt-driven-development** when a recommendation is about to lock in.
- Use **algorithm-optimization** when candidates need validation on real KPIs.
- Use **context7-mcp** for version-sensitive library docs.
- Use **technical-reporting** when the evidence must become a saved report or ADR.

## Final Checklist
- [ ] Scope and constraints are clearly understood
- [ ] Both modern and classic approaches are considered
- [ ] Candidates are evaluated against relevant criteria
- [ ] Only the most relevant 3–5 options are kept
- [ ] Recommendation is conditional and tied to project context
- [ ] Trade-offs and risks are clearly stated
- [ ] Practical next steps are suggested
- [ ] Output is concise and focused on decision-making
