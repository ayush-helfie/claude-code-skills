# Lens: Necessity & placement

**Model: sonnet.**

This lens asks two questions of every changed unit of code, and a third that follows from them:

1. **What does this code do?**
2. **Is it at the right level — does it belong here?**
3. **Is it needed? If it were removed, could the PR's stated goal still be achieved?**

Everything below is in service of those three.

## 1. What does this code do?

Go through each new or modified class, function, and file and state plainly what it does — from the
code, not from its name or the PR description.

If you cannot state it plainly, that is itself a finding. Either the code is doing too many things
(no single sentence covers it), or its name is lying about what it does, or it's genuinely unclear.
All three are worth reporting, and all three are cheaper to fix now than in six months.

Watch for the gap between what a thing is *called* and what it *does* — a `validate()` that also
persists, a `getX()` that mutates, a `Helper` that owns the core business rule. Hidden side effects
behind innocent names are among the most expensive defects in a codebase because nobody re-reads a
function whose name they trust.

## 2. Is it at the right level?

For each piece of new logic: which layer or component *should* own this responsibility, and is that
where it is?

Use the architectural map from `architecture.md` rather than a generic layer diagram — the project's
actual structure decides what "right level" means here.

Common misplacements worth checking:

- business rules in a Composable or Activity
- formatting and presentation concerns inside a domain model or repository
- data-layer concerns (DTOs, HTTP codes, SQL, cursors) surfacing in UI or domain
- validation duplicated at three levels because no level owns it
- a `ViewModel` doing work that belongs in a use case or repository the project already has
- a utility in a shared module that only one feature uses, or a feature-local copy of something shared
- logic in a base class that only one subclass needs

The question isn't "does this match a diagram" — it's *"when this rule changes, will someone find it
where they'd look for it?"*

## 3. Is it needed?

The sharpest test in this lens: **"Would removing this change prevent the stated goal of the PR from
working?"**

Apply it to each changed file, each new abstraction, each new dependency, each refactor bundled in.
If the answer is no, investigate whether it belongs in this PR at all.

This isn't hostility to cleanup — it's that unnecessary changes make a PR harder to review, harder to
revert, and harder to bisect later, and they hide the necessary changes in the noise.

Specifically look for:

- Is every changed file necessary?
- Is every new abstraction necessary? (Cross-check with `architecture.md`'s eight questions.)
- Is every new dependency necessary?
- Are there unrelated refactors, renames, or architecture changes riding along?
- Are there formatting-only changes churning the diff?
- Is existing code being rewritten without a concrete benefit?
- Could the same outcome be achieved with substantially less code?
- Does the PR increase complexity without increasing capability?
- Is the PR solving problems outside its stated scope?

A clean PR makes the smallest reasonable set of changes needed to achieve its objective.

## Look for what should be deleted

Necessity cuts both ways. A PR that adds a new path often leaves the old one standing:

- an implementation the PR has superseded but not removed
- feature flags, branches, or fallbacks now permanently on one side
- dead parameters, unused fields, orphaned resources
- a TODO that the PR itself resolved
- tests for behavior that no longer exists

Deleting code is a legitimate and undervalued review recommendation. Check with the user before
asserting that something is obsolete — a leftover may be deliberate, staged for a follow-up, or
required for a rollback.

## Report carefully

Necessity findings can read as "you did extra work for nothing", so lead with the concrete cost —
review burden, revert risk, a second thing to maintain — and keep the tone factual.

Where a change looks unnecessary but might be externally required, raise it as a question rather than
a finding. Many apparently gratuitous changes turn out to be a lint rule, a build constraint, or a
dependency bump someone else asked for.

End with a **Could not verify** list.
