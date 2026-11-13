# Definition of Done vs Acceptance Criteria

**Acceptance criteria** are the task contract: the check that proves this request.

**Definition of Done** is the standing bar for a behavior change:

- The cause is fixed, not silenced.
- A regression check exists for the failure.
- The decisive verification passed once. Do not re-run it when no code changed.
- Trust-boundary checks and accessibility were not removed to go green.

A single green run is not Done when the task also required a guard or a documented revert.
