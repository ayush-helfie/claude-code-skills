# Phase 6 — Final senior review & report

## The final holistic pass

Before writing anything, step back from the individual findings and ask the question that matters
most:

> **"Would I be comfortable owning this code six months from now?"**

Then work through:

- Is the implementation simpler than it needs to be?
- Is it more complicated than it needs to be?
- Does the architecture make sense?
- Are responsibilities in the right places?
- Are the names telling the story?
- Is there duplicated functionality?
- Is the PR introducing a parallel implementation?
- Does it follow existing project patterns?
- Are there meaningful performance concerns?
- Are there bugs?
- Is the PR unnecessarily broad?
- Is anything missing?
- Are there abstractions that should not exist?
- Are there abstractions that are actually needed?
- Is there code that should be **deleted** rather than refactored?
- Would a smaller implementation achieve the same goal?

This pass exists because nine lenses produce nine local views, and the most important judgment in a
senior review is a global one: whether the sum of the changes is a good way to solve this problem.
Sometimes every individual finding is minor and the honest verdict is still "this should be built
differently" — and sometimes the reverse, where a list of P2s adds up to a PR that is fine to merge.

## Finding template

Use this exact shape for every finding:

```markdown
### [P1] Short, specific title

**Location:** `path/to/File.kt:142`

**Problem**

Explain the concrete issue.

**Why it matters**

Explain the impact.

**Evidence**

Reference the relevant code, repository pattern, caller, test, or official documentation.

**Recommendation**

Give a concrete implementation direction.
```

Do not provide a large rewrite unless the rewrite is genuinely the point. A diff-sized suggestion the
author can act on beats a page of replacement code they have to evaluate from scratch.

**If there are no meaningful issues at a given severity, omit that section.** Do not create empty
sections or pad them — a heading with "none found" under it is noise, and padding a thin section is
how a review loses the author's trust.

## Report structure

Write to `<scratchpad>/pr-review-<number>.md`:

```markdown
# PR Review: <title> (#<number>)

## PR Assessment

A concise overall assessment stating:
- What the PR appears to be doing.
- Whether it achieves its stated intent.
- Overall quality.
- Whether you would approve, request changes, or consider it not ready.
- The most important reason for that decision.

## Blocking / Important Issues

Only genuinely important findings — P0 and P1. Use the finding template.

## Refactoring Opportunities

Only changes that materially improve readability, architecture, maintainability,
duplication, testability, or performance.

Do not turn this into a generic style guide.

## Unnecessary / Out-of-Scope Changes

Changes that do not appear necessary for the stated objective.

## Missing Work

Functionality, tests, cleanup, or integration that appears necessary but is absent.

## Positive Observations

Only concrete strengths worth preserving. No generic praise.

## What I Could Not Verify

Questions the repository could not answer, and what would settle each one.

## Final Verdict

One of: **APPROVE** / **APPROVE WITH MINOR CHANGES** / **REQUEST CHANGES** /
**NOT READY FOR REVIEW**

Explain the decision in a few sentences.
```

## Notes on three sections

**Positive Observations** should name specific things — a well-chosen abstraction, a test that covers
the real failure mode, a simplification — because the point is to tell the author what to keep doing.
"Nice work overall" tells them nothing and reads as filler before the criticism.

**What I Could Not Verify** is what makes hard constraint 19 real. It gives honest uncertainty
somewhere to live so it doesn't get laundered into a confident finding or silently dropped. A review
that says "I could not determine whether `LegacySyncWorker` is still scheduled anywhere; if it isn't,
this change leaves it orphaned" is more useful than one that either asserts or omits it.

**Final Verdict** must follow from the findings above it. If the blocking section is empty, the
verdict is not REQUEST CHANGES. If there's a P0, it is not APPROVE.

## After writing

Tell the user the report path, then summarize in the conversation: the verdict, the single most
important reason for it, and anything still waiting on their input. Keep that summary to a few
sentences — the report holds the detail.
