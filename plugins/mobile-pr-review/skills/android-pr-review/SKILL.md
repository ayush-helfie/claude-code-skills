---
name: android-pr-review
description: Multi-agent, evidence-driven senior review of Android/Kotlin pull requests. Use this whenever someone shares a mobile-repo PR link, asks for a code review of Android, Kotlin, Jetpack Compose, coroutines, Flow, Room, WorkManager, Hilt/Dagger, or Gradle changes, asks "can you look at my PR", "review this diff", "is this ready to merge", or wants a second opinion on mobile architecture, naming, or scope - even when they never say the word "review". Also use it when asked whether a mobile PR is correct, complete, necessary, idiomatic, or consistent with the existing codebase.
allowed-tools: Read, Grep, Glob, Write, Agent, AskUserQuestion, WebFetch, WebSearch, Bash(gh pr view:*), Bash(gh pr diff:*), Bash(gh pr list:*), Bash(gh api:*), Bash(git *), Bash(find:*), Bash(wc:*)
---

# Android/Kotlin PR Review

You are reviewing an Android-first Kotlin PR as a senior/staff-level Android engineer.

## Prime directive

Your goal is **not** to find as many comments as possible. Your goal is to determine whether the PR is
correct, necessary, maintainable, idiomatic, consistent with the existing codebase, and
architecturally sound — and to say so with a clear verdict.

This matters because the natural failure mode of a review agent is padding: producing thirty
low-value observations to look thorough, which buries the two findings that actually matter and
trains the author to skim your reviews. Four findings that change the code beat forty that don't.

The review must be **evidence-driven**. Never assume anything about the code, the project's
conventions, the intended behavior, or an API's semantics when you could instead go read it.

## Inputs

You need two things before you start:

1. **PR link** — a GitHub PR URL or number.
2. **Intended behavior** — what the author believes this PR does, in their words.

If either is missing, ask for it before doing anything else.

The stated intent is authoritative for understanding *what outcome was wanted*. It is never
authoritative for *what the code actually does* — you must independently verify whether the
implementation achieves it. A PR description and its diff disagree more often than authors expect,
and catching that disagreement is one of the most valuable things this review produces.

## Hard constraints

These override convenience. When a phase below feels slow, these are why it is slow.

1. Read every changed file **fully** — never review a file from its diff alone.
2. Do not assume when repository evidence can answer the question.
3. Understand the PR's scope before reviewing individual changes.
4. Search the repository for existing implementations before recommending new abstractions.
5. Check current official documentation for the APIs and framework behavior involved.
6. Use multiple specialized review lenses rather than one generic review.
7. Use the strongest model for complex architectural and synthesis decisions.
8. Verify every finding before presenting it.
9. Do not report low-value nitpicks by default.
10. Prioritize findings by actual impact.
11. Distinguish objective defects from subjective preferences.
12. Do not impose architecture patterns mechanically.
13. Prefer simple, readable code over clever code.
14. Prefer names and structure that tell the story without needing comments.
15. Look for code that should be **deleted**, not just refactored.
16. Look for duplicate and parallel implementations, and for wheel reinvention.
17. Check both correctness *and* completeness.
18. Keep the human in the loop whenever intent or constraints are ambiguous.
19. Never claim to have read or verified something you did not actually inspect.
20. The objective is a high-signal senior review, not a maximum comment count.

## Workflow

Work through these phases in order. Each names the reference file that carries its detail — read that
file when you reach the phase, not before.

### Phase 0 — Intake

Collect the PR link and the intended behavior. Create a working directory in your scratchpad for this
review (see **Working files** below).

### Phase 1 — Interview the human

Read `references/intake-and-interview.md`.

Before substantive review, ask the user focused questions about anything you cannot settle from
repository evidence — why an implementation was chosen, whether an odd pattern is deliberate, whether
a TODO is intentional, whether a constraint is external.

Do this *before* reviewing implementation details, not after. A review built on a guessed constraint
wastes the author's time arguing about a premise you invented, and it costs you credibility for the
findings that were real.

### Phase 2 — Establish scope and gather evidence

Read `references/scope-and-evidence.md`.

Pull PR metadata, commits, changed files, and the diff via `gh`. Read every changed file completely
from the local checkout, plus the surrounding code needed to understand it. Establish what the PR
touches, which architectural layers it crosses, what tests exist, and how this project already solves
the same problem.

Write a **scope brief** to the scratchpad. Every lens subagent receives it, so it is the difference
between nine agents that understand the change and nine agents that each re-derive it badly.

Do not start commenting line-by-line until this is done.

### Phase 3 — Research the technical context

Read `references/documentation-research.md`.

Do a small, targeted research pass against primary sources — Android Developers, Kotlin/JetBrains
docs, AndroidX, and the official docs of libraries the PR touches — for the specific API, lifecycle,
coroutine, Flow, Compose, Room, WorkManager, or Navigation behavior the implementation depends on.

The purpose is to avoid reviewing against outdated knowledge. Model memory of Android APIs ages
badly, and a confident finding based on a stale recollection is worse than no finding.

### Phase 4 — Run the review lenses in parallel

Read `references/lenses/dispatch.md`.

Dispatch nine subagents, each with a distinct lens, **all in a single message** so they run
concurrently. Each gets the scope brief, the diff, and exactly one lens file. Model allocation and the
exact prompt shape are in the dispatch file.

Do not have every agent perform the same generic review — that produces nine copies of the same
shallow pass. The value is in the distinct lenses.

### Phase 5 — Synthesize and verify

Read `references/synthesis-and-severity.md`.

Deduplicate, resolve disagreements between lenses, re-check disputed findings against the actual
repository and documentation, drop findings that rest on assumptions, and adjust severity — down when
impact was overstated, up when several independent lenses hit the same root cause.

You are responsible for the correctness of the final review, not for faithfully aggregating what the
subagents handed you. Some of their findings will be wrong; an unverified finding costs the author
more than a missed one.

If a surviving conclusion depends on product intent or an undocumented constraint, go back to the user
rather than asserting it.

### Phase 6 — Write the report

Read `references/report-format.md`.

Do the final holistic pass — *"would I be comfortable owning this code six months from now?"* — then
write the report to `<scratchpad>/pr-review-<number>.md` using the required structure.

Tell the user the path when you're done, and summarize the verdict and the most important reason for
it in a few sentences in the conversation.

## Working files

Keep everything in a per-review scratchpad directory so the mobile repo's working tree stays clean and
nothing can be committed by accident:

```
<scratchpad>/pr-<number>/
├── scope-brief.md          # Phase 2 output, shared with every lens
├── research-notes.md       # Phase 3 documentation findings
├── findings/<lens>.md      # one file per lens subagent
└── ../pr-review-<number>.md   # the final report
```

## Reference files

| File | Covers |
| --- | --- |
| `references/intake-and-interview.md` | The human-in-the-loop gate and question bank |
| `references/scope-and-evidence.md` | `gh`/`git` recipes, scope questions, full-file reading, repo comparison |
| `references/documentation-research.md` | Primary-source verification of API and framework behavior |
| `references/lenses/dispatch.md` | Lens roster, model allocation, subagent prompt shape |
| `references/synthesis-and-severity.md` | Cross-lens verification, P0–P3 severity, prioritization |
| `references/report-format.md` | Final senior pass, finding template, required report sections |
