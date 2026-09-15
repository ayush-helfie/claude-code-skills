# Phase 4 — Dispatch the review lenses

Nine subagents, nine distinct lenses, launched **in a single message** so they run concurrently.

## Why distinct lenses

Running the same generic review nine times produces nine copies of the same shallow pass, with the
same blind spots, and gives you false confidence because they agree. The value comes from the lenses
being genuinely different: the agent hunting for duplicate implementations is in a different mental
mode from the one tracing coroutine cancellation, and neither would find the other's results.

Give each agent one lens and one lens file. An agent handed all nine lenses will do the two it finds
easiest and gesture at the rest.

## The roster

| Lens | File | Model | Mandate |
| --- | --- | --- | --- |
| Correctness | `correctness.md` | opus | Does it work? Bugs, edge cases, lifecycle, concurrency |
| Architecture | `architecture.md` | opus | Layers, boundaries, SOLID where it earns its place, abstractions |
| Necessity & placement | `necessity-and-placement.md` | sonnet | What does it do, does it belong here, is it needed at all |
| Clean code | `clean-code.md` | sonnet | Naming, readability, complexity, cohesion, comments |
| Android/Kotlin idiom | `android-kotlin.md` | sonnet | Kotlin and Android idiomaticity as a practitioner |
| Performance | `performance.md` | sonnet | Meaningful performance problems, not micro-optimizations |
| Duplication & patterns | `duplication-and-patterns.md` | sonnet | Wheel reinvention; consistency with how this repo works |
| Tests | `tests.md` | sonnet | Coverage of the affected behavior, test quality |
| Completeness | `completeness.md` | sonnet | What's *missing* — wiring, call sites, cleanup, migrations |

## Model allocation

Use models deliberately. **Opus** goes to complex architectural analysis and subtle
concurrency/lifecycle reasoning — the two places where a weaker pass produces plausible-sounding
wrong answers. **Sonnet** handles the focused, more mechanical lenses, which is most of them.

Don't spend the strongest model on repetitive inspection, and don't put subtle concurrency analysis
on a model that will pattern-match its way to a confident wrong conclusion.

The main agent — on the strongest model — does the synthesis in Phase 5. That's the other place where
judgment matters most: deciding which findings are real and which are noise.

## Prompt shape

Give every subagent the same scaffolding, varying only the lens:

```
You are reviewing an Android/Kotlin PR through ONE lens: <lens name>.

Read your lens file first: <abs path to lens file>
Read the scope brief:      <scratchpad>/pr-<n>/scope-brief.md
Read the research notes:   <scratchpad>/pr-<n>/research-notes.md

The PR is checked out locally at <repo path> on branch pr-<n>.
Base branch: <base>. Diff: `git diff $(git merge-base HEAD origin/<base>)..HEAD`

Rules that override everything else:
- Read every changed file IN FULL. Never review from the diff alone.
- If a finding depends on code outside the changed file, read that code first.
- Never report a finding you have not verified against actual code.
- Cite file:line for every finding, and state what you actually inspected.
- Report only what your lens covers. Another agent has the others.
- Default to NOT reporting P3/minor issues (see the severity model).
- Prefer four findings that matter to forty that don't.

Write findings to <scratchpad>/pr-<n>/findings/<lens>.md in the required shape,
then return a short summary of what you found and what you could not verify.
```

## Required finding shape

Every lens writes findings in this shape. Synthesis depends on it — a finding without evidence and a
confidence level cannot be verified or ranked, and will be dropped.

```markdown
## [P1] Short, specific title

**Location:** `path/to/File.kt:142`
**Confidence:** high | medium | low

**Problem**
What the code currently does, concretely.

**Why it matters**
The actual impact. If you can't state one, this isn't a finding.

**Evidence**
What you inspected: files read, callers found, tests checked, docs cited (with URL).
Quote the relevant lines.

**Recommendation**
A concrete direction. Not a full rewrite unless the rewrite is the point.

**Required or optional:** required | optional
```

Each lens file also asks its agent to end with a **"Could not verify"** list. That list is how
uncertainty reaches the report honestly instead of being laundered into a confident finding.

## Severity, briefly

Lenses assign a provisional severity; synthesis adjusts it. The full model is in
`../synthesis-and-severity.md`, but every lens agent needs the short version:

- **P0** — critical: correctness, security, data loss, crash, production impact
- **P1** — important: a real bug, architectural problem, or scope problem to fix before merge
- **P2** — moderate: a real improvement, not merge-blocking
- **P3** — minor: small cleanup, stylistic, low impact — **suppressed by default**

Report a P3 only when it is unusually clear, systematically repeated, creates meaningful future
maintenance cost, or reveals a broader design problem.
