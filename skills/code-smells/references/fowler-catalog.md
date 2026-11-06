# Fowler Smell Catalog

21 types from Fowler's *Refactoring*, excluding "Comments". A comment that explains why is not a smell (`rules/AGENTS.md` §3).

95% of types means at least 20 of these 21 rows are either an automated candidate or a named manual check. This is not 95% of smell instances and not 95% precision.

Thresholds for function length, nesting, and cyclomatic complexity stay in `rules/AGENTS.md` §3. Do not copy the numbers into a finding.

| Smell | Signal | Mode | Handoff |
| :--- | :--- | :--- | :--- |
| Long Method | Function span above the hard length in `AGENTS.md` §3 | Script | `code-simplification` |
| Large Class | 15 or more methods on one class | Script | `code-simplification` |
| Long Parameter List | 5 or more parameters after `self` and `cls` | Script | `code-simplification` |
| Data Clumps | The same parameter set of 3 or more names on 3 or more functions | Script | `code-simplification` |
| Switch Statements | One `if`/`elif` chain with 4 or more `elif` branches | Script | `code-simplification` |
| Message Chains | Attribute or call chain of 4 or more hops (`a.b.c.d`) | Script | `code-simplification` |
| Middle Man | At least 3 methods and at least 70% only forward one call | Script | `code-simplification` |
| Data Class | At least 2 fields and every method is a getter or setter | Script | `code-simplification` |
| Lazy Class | Class span of 12 lines or fewer, at most one method, no fields | Script | `code-simplification` |
| Feature Envy | One method touches another object's attributes more often than `self`, and at least 3 times | Script | `code-simplification` |
| Temporary Field | A `self` field is written and read in only one method | Script | `code-simplification` |
| Speculative Generality | An `ABC` with abstract methods and exactly one subclass in the scan | Script | `code-minimalism` |
| Refused Bequest | Subclass defines 2 or more methods, none call `super()`, and a scanned base has methods the subclass never uses | Manual | `code-simplification` |
| Inappropriate Intimacy | Two classes call each other's `_` methods or read each other's `_` fields | Manual | `code-simplification` |
| Parallel Inheritance | Adding a subclass to one hierarchy forces a subclass in another | Manual | `code-simplification` |
| Alternative Classes with Different Interfaces | Two types serve the same role with different method names | Manual, then `codebase-minimalism` if the names overlap | `codebase-minimalism` |
| Primitive Obsession | Flags, string codes, or loose tuples stand in for a type or Enum | Manual | `codebase-minimalism` |
| Duplicate Code | More than 15 identical lines in one diff, or the same concept under different names across modules | Manual | `codebase-minimalism` when the copies span modules |
| Dead Code | No caller, including dynamic and framework entrypoints | Manual | `codebase-minimalism` |
| Divergent Change | One class changes for unrelated reasons | Manual, `git log` only when the user allows history | `code-simplification` |
| Shotgun Surgery | One concept change edits many classes together | Manual, `git log` only when the user allows history | `code-simplification` |

Python is the automated scope. Other languages stay on the manual rows. A missing `git` history is "insufficient data" for the last two rows, not a clean result.

Every script row is a candidate. Confirm it in the named file before proposing an edit.

A hard-threshold breach from `rules/AGENTS.md` §3 is a normal finding. It is extreme when cyclomatic or cognitive complexity is more than double that hard cap and the code has no written justification. `code-review` maps normal to Important and extreme to Critical. Do not copy the cap numbers into the finding.
