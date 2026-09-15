# Phase 1 — Interview the human

Before any substantive review, interview the user about what you cannot establish from the repository.

## Why this gate exists

A reviewer who guesses at intent produces confident findings about a premise the author never held.
The author then spends a round-trip correcting your assumption instead of fixing real problems, and
learns to discount your next review. The cost of asking is one question; the cost of guessing is the
credibility of everything else you say.

There is a second, subtler reason. Many of the most valuable review findings — "this abstraction has
no second implementation and probably shouldn't exist", "this retry loop will hammer the API" —
flip completely depending on a constraint you can't see from the code. Asking is how you find out
which findings are real.

## Never assume

Ask rather than assume any of these:

- why a particular implementation was chosen
- whether a seemingly unusual pattern is intentional
- whether backwards compatibility is required
- whether a behavior is product-required
- whether a TODO is intentional
- whether an apparently unused abstraction has future requirements
- whether a performance tradeoff is acceptable
- whether a particular architecture is mandated by the project
- whether a dependency or API can be changed
- whether a seemingly unnecessary change is required by some external constraint

If the PR's intent or scope is unclear at all, **stop and clarify before reviewing implementation
details**. Reviewing first and asking later means redoing the review.

## How to ask

Use `AskUserQuestion`. Batch your questions — one round of three or four focused questions beats four
separate interruptions.

Ask only what actually blocks or changes the review. A question whose answer wouldn't alter any
finding is noise, and asking a pile of them makes the user stop reading your questions carefully.

Good questions are specific and grounded in something you observed:

- *"`SyncScheduler` wraps `WorkManager` with a single implementation and no interface. Is that
  wrapper there for a planned second backend, or is it incidental?"*
- *"The PR changes the DB schema without a migration. Is this table still pre-release, or is a
  migration missing?"*
- *"`RetryPolicy` uses a fixed 1s delay with no backoff. Is that a product requirement, or the
  default that happened to be there?"*

Weak questions are generic and could have been asked of any PR:

- *"Are there any constraints I should know about?"*
- *"Is this the architecture you want?"*

## Opening questions

If the user gave you a PR link with little context, open with these before anything else:

1. **What is this PR supposed to do**, in your words? (The stated outcome — authoritative for intent,
   not for behavior.)
2. **Is anything here constrained from outside** — a deadline, an API you don't control, a pattern
   another team mandated, a change you were told to make?
3. **Is there anything you already know is rough** and want focused attention on, or deliberately
   left for a follow-up PR?

Question 3 is worth asking every time. It surfaces intentional debt so you don't spend the review
reporting things the author already knows, and it points you at where they actually want eyes.

## Later checkpoints

The interview is not only Phase 1. Come back to the user during synthesis (Phase 5) whenever a
surviving finding depends on product intent, an undocumented constraint, or an architectural decision
you cannot establish from repository evidence.

When you do, present it as a question with your reasoning attached, not as a finding with a hedge:

> *"`UserPrefsRepository` and `SettingsStore` both persist the same three fields. The PR writes to
> `SettingsStore` only, so the two can now diverge. Is `UserPrefsRepository` being retired, or should
> this write through it?"*

Do not manufacture certainty when the user has not given you the context to be certain. "I could not
verify this" is a legitimate and useful thing for a review to say — see `report-format.md`.
