---
name: data-storytelling
description: >-
  Turn already-validated metrics into a stakeholder decision narrative (Hook -> Ask)
  using Zen Minimalism wording, Kanso essentialism, and Ma paragraph rhythm.
  Not for analysis, Plotly construction, or saved engineering markdown.
risk: safe
source: local
date_added: "2026-02-27"
---

# Data Storytelling Skill

Transform validated analysis into a calm, authoritative, decision-ready narrative for stakeholders using **Zen Minimalism** prose principles.

## When to Use
- Presenting insights to executives or non-technical audiences
- QBRs or business recommendations that need a clear "so what"
- Turning statistical or ML findings into an actionable ask

## When Not to Use
- Numbers are not yet validated (`data-science` first)
- Pure exploratory analysis still in progress
- Technical deep-dives for other data scientists (`technical-reporting` if a file is requested)
- Simple metric dump with no decision

## Related Skills
- **Required:** base the story on validated findings from **data-science**. Do not invent numbers.
- Use **data-visualization** for supporting charts (layout and overlap live there).
- Use **technical-reporting** only when the user asked to save a formal technical file.
- Use **html-report** when the validated narrative must become a stakeholder-facing HTML brief. Follow the locked composition.

## Core Structure (Architectural Chapters 01-06)
1. **01 · Hook (The Thesis)** - Open with one declarative sentence naming the core metric, exact delta, and operational consequence.
2. **02 · Context (The Baseline)** - State the cohort scope, baseline number, and why the threshold matters in 1-2 sentences.
3. **03 · Insight (The Evidence)** - Present the primary quantitative contrast via a clean comparison table or focal delta chart.
4. **04 · Implication (The Stakes)** - Translate the metric shift into user, revenue, latency, or reliability outcomes.
5. **05 · Recommendation (The Path)** - Propose concrete actions paired with expected impact ranges.
6. **06 · Ask (The Decision)** - Close with the single explicit approval or resource decision required from stakeholders.

## Zen Minimalism Wording & Paragraphing Rules
1. **Kanso (Simplicity & Essentialism in Wording)**:
   - Eliminate throat-clearing preambles ("In order to evaluate...", "It is interesting to note that...").
   - Cut decorative adjectives and corporate buzzwords ("synergistic", "paradigm", "massive game-changer").
   - Start sentences with the subject or the metric: *"PlaceSearch lifts Top-1 accuracy by +8.36pp (78.52% vs 70.16%) across 4.37M converted queries."*
   - Target <= 20 words per sentence so every clause carries high signal.
2. **Ma (Negative Space in Paragraphing)**:
   - Cap every paragraph at **2-3 sentences** (`<= 60 words`, 60ch-70ch measure, target 66ch).
   - Never stack more than two paragraphs without a structural break (a compact table, a bulleted takeaway, or a numbered section header).
   - Give each paragraph exactly one job: either state the claim, explain the mechanism, or quantify the consequence.
3. **Shibumi (Understated Authority)**:
   - Let exact numbers, sample sizes (`N = ...`), and percentage-point deltas (`+8.36pp`) speak for themselves without exclamation marks or hype.
   - Pair every positive gain with its honest boundary condition or trade-off in the same calm register (e.g., *"Hit@1 rises +8.36pp while deep-tail Hit@10 narrows -5.21pp due to candidate pruning"*).
4. **Parallel Rhythm in Lists**:
   - Begin every bullet in a group with the exact same grammatical form (all bold noun labels or all active imperative verbs).
   - Keep bullet items to 1-2 lines so the eye scans vertically without horizontal fatigue.

## Output Expectations
- Open immediately with the **Thesis Callout** (1-2 sentences containing the primary metric, delta, and decision).
- Precede every data table or chart with a single-sentence **Chapter Lead** (`<= 25 words`) stating what pattern the reader should see.
- Separate empirical findings (`FACT`) from strategic recommendations (`RECOMMENDATION`) and explicit stakeholder decisions (`ASK`).

## Final Checklist
- [ ] Insights come from validated `data-science` output
- [ ] Hook / TL;DR states the core number and delta in the opening sentence
- [ ] Flow follows numbered chapters: Hook -> Context -> Insight -> Implication -> Recommendation -> Ask
- [ ] Every paragraph is 2-3 sentences and <= 60 words (*Ma* breathing room)
- [ ] Zero filler phrases, buzzwords, or ungrounded superlatives (*Kanso* discipline)
- [ ] Limitations and trade-offs are stated calmly alongside gains (*Shibumi* honesty)
- [ ] Every number serves the narrative; simple deltas beat complex charts
- [ ] Language matches the audience and ends with one concrete ask
