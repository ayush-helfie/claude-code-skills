# Lens: Tests

**Model: sonnet.**

Your question: **if this behavior broke six months from now, would anything catch it?**

## Review

- Do tests exist for the changed behavior?
- Do *existing* tests already cover it? (Check before asking for new ones — the coverage may be there
  a layer up.)
- Are new tests necessary?
- Do the tests validate **behavior** rather than implementation details?
- Are edge cases covered?
- Are failure cases covered?
- Are concurrency and lifecycle cases covered where relevant?
- Is there regression protection for the specific bug this PR fixes?

## Find the tests before concluding anything

```bash
fd -e kt . src/test src/androidTest 2>/dev/null | rg -i '<changed class name>'
rg -t kotlin -l '<ChangedClass>' src/test src/androidTest
rg -t kotlin -l 'class <ChangedClass>Test|<ChangedClass>Test'
```

Also check where this project *puts* its tests and what it normally tests at each level — a repo that
tests behavior through ViewModel tests and doesn't unit-test repositories is making a deliberate
choice, and asking for repository unit tests fights that choice for no gain. See
`duplication-and-patterns.md`.

## Behavior versus implementation

The most valuable test finding is usually not "there are no tests" — it's "these tests will pass
while the feature is broken."

Tests coupled to implementation break on every refactor and pass through real regressions. Watch for:

- asserting that a mock was called rather than that the outcome happened
- mocking the thing under test
- asserting on internal state instead of observable behavior
- tests that mirror the implementation's structure step for step
- a test that would still pass if the function body were replaced with its happy path

## Proportionality

**Do not demand tests for trivial changes where they add no meaningful value.** A test for a renamed
constant or a one-line string change is ceremony, and asking for it trains authors to write
low-value tests to satisfy reviewers.

Weight your asks by what breaking would cost:

- a bug fix with no regression test — nearly always worth asking for; this is the highest-value test
  request in review, because the bug already demonstrated the gap is real
- new business logic, state machines, mappers, validation — worth testing
- a new branch in existing logic — worth covering
- pure UI wiring with no logic — usually not
- a rename, a constant, a formatting change — no

## What to report

Identify **important behavior that currently has no regression protection**, and be specific about
what a test would need to assert. "Add tests" is not actionable; "there's no test that a cancelled
sync leaves the pending-writes queue intact, which is the failure this PR fixes" is.

Where existing tests exist but are weak, say what they'd let through.

End with a **Could not verify** list — including tests you couldn't locate but suspect exist.
