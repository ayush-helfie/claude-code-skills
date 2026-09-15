# Phase 5 — Synthesis, verification & severity

Nine lenses have handed you raw findings. **You are responsible for the correctness of the final
review, not for faithfully aggregating what they produced.**

Some of those findings are wrong. A lens agent reasoning over a large diff will occasionally invent
an API, misread a lifecycle, or flag a pattern the repository deliberately uses. Passing those
through unverified is worse than missing something: it sends the author to change working code, and
it teaches them to discount the findings that were real.

## Cross-lens verification

Work through these in order:

1. **Deduplicate.** Several lenses will hit the same code from different angles.
2. **Identify disagreements.** Where two lenses contradict each other, at least one is wrong — resolve
   it, don't report both.
3. **Verify disputed findings against the actual repository.** Go read the code yourself.
4. **Re-read relevant code** wherever a finding's claim isn't obviously supported by its evidence.
5. **Verify API and library claims against current documentation.** If the docs contradict the
   finding, drop it (see `documentation-research.md`).
6. **Reject findings based on assumptions.** If the evidence section says "this appears to" or
   "likely", either establish it or cut it.
7. **Lower severity** where impact is overstated. Lens agents inflate; it's a predictable bias.
8. **Raise severity** where multiple independent lenses found the same underlying problem. Convergence
   from different angles is real signal — it usually means a root cause rather than a symptom.
9. **Combine related findings** that are one root issue seen from several places. Three symptoms of
   one misplaced responsibility should be one finding with three locations, not three findings.

A finding survives only if you can state: what the code does, why that's a problem, and the specific
evidence — file, line, caller, test, or documentation URL — that establishes it.

## Severity model

- **P0 — Critical/blocking.** A severe correctness, security, data-loss, crash, or
  production-impacting problem.
- **P1 — Important.** A meaningful bug, architectural problem, maintainability problem, performance
  issue, or scope problem that should be addressed before merging.
- **P2 — Moderate.** A real improvement to correctness, readability, architecture, testability, or
  maintainability, but not necessarily merge-blocking.
- **P3 — Minor.** Small cleanup, naming, style, or low-impact optimization.

**By default, do not report P3 issues.**

Report one only when it is unusually clear, systematically repeated across the PR, creates meaningful
future maintenance cost, or reveals a broader design problem.

Be selective. The review should have a high signal-to-noise ratio. **If there are fifteen possible
issues but only four materially matter, report the four.** A long list dilutes the important findings
until the author skims past them — the practical effect of reporting everything is that nothing gets
read.

## Priority ordering

Order findings roughly by:

1. correctness and bugs
2. security and data integrity
3. lifecycle and concurrency problems
4. architectural problems
5. unnecessary duplication and parallel implementations
6. meaningful performance problems
7. significant readability and maintainability problems
8. naming problems
9. minor cleanup

## Distinguish fact from recommendation

For every surviving finding, keep these separate and explicit:

- **what the code currently does** — observable fact
- **why that is a problem** — the impact
- **evidence** — from the repository or documentation
- **what should change** — your recommendation
- **whether it is required or optional**

Never present a subjective preference as a defect. This is what makes a review arguable in a
productive way: the author can accept your facts and still disagree with your recommendation, and
that conversation is useful. A preference stated as a bug just produces a fight about the premise.

**Weak:**

> "Use a repository here because Clean Architecture requires it."

**Strong:**

> "This ViewModel directly performs database access, while all other database access in this feature
> goes through `XRepository`. This introduces a second access pattern and makes the ViewModel
> responsible for data-layer concerns. Reusing `XRepository` would keep the existing dependency
> boundary."

The second states what the code does, what the codebase does elsewhere, what that costs, and what
would fix it — with no appeal to authority anywhere.

## Return to the human

Before writing the report, take back to the user any surviving conclusion that depends on product
intent, an undocumented constraint, or an architectural decision you cannot establish from repository
evidence.

Findings you still can't resolve go into **"What I could not verify"** in the report, not into the
findings list with a hedge attached.
