# Lens: Duplication & existing project patterns

**Model: sonnet.**

Two closely related questions, both answered by searching the repository rather than reasoning about
the diff:

1. **Does this project already have a mechanism for doing this?**
2. **How does this project normally do things, and does the PR follow that?**

This lens is search-heavy by nature. An agent that reasons instead of searching will find nothing,
because duplication is invisible from the diff — the duplicate is somewhere else by definition.

## Part 1 — Wheel reinvention

Search for existing implementations of the same or similar functionality before concluding the PR
needed to build anything.

Look specifically for duplicate:

- utilities
- repositories
- API clients
- mappers
- validators
- formatters
- state handling
- UI components
- error handling
- business logic
- parallel abstractions
- multiple implementations of the same concept

```bash
rg -t kotlin 'fun \w*(format|parse|validate|map|convert)\w*\(' --no-heading
rg -t kotlin 'class \w*(Repository|DataSource|Client|Mapper|Formatter|Validator)'
rg -t kotlin 'sealed (class|interface) \w*(Result|State|Error|Event)'
fd -e kt | rg -i '<concept the PR introduces>'
```

Search by **concept**, not by name. The duplicate almost never shares a name with the new code — that
is precisely why the author didn't find it. Search for the operation, the domain noun, the library
being wrapped, the string format being produced.

For each hit, determine whether the PR should reuse or extend it rather than adding another
implementation.

**Be especially suspicious of two implementations that solve the same conceptual problem with
slightly different APIs.** These are worse than exact duplicates: they diverge silently, each grows
its own bug fixes, and eventually nobody knows which one is authoritative. When you find a pair,
report it explicitly even if the PR only introduced one side.

## Part 2 — Existing project patterns

Understand the repository's established architecture and conventions, then judge the PR against
*them*.

Determine how this project:

- structures similar features
- decides where similar logic lives
- injects dependencies
- models state
- represents errors
- performs networking and database operations
- structures tests
- names things
- organizes files and classes

```bash
fd -e kt . <a sibling feature dir> | head -40        # how a comparable feature is laid out
rg -t kotlin 'sealed (class|interface) \w*Error' -A6 | head -60
rg -t kotlin '@(Inject|Provides|Binds|HiltViewModel)' -l | head -20
```

**The project is a major source of truth.**

**Do not criticize the PR for violating a generic convention when the repository consistently follows
another deliberate one.** This is the most common way a review wastes everyone's time: importing
habits from a different codebase and calling them standards. If the repo has done it one way in
fourteen places, the fifteenth is not a finding.

Conversely, flag it when the PR introduces a new pattern unnecessarily for a problem the project
already has an established answer to. Prefer consistency when the existing pattern is sound, the new
problem is materially equivalent, and there's no demonstrated reason to diverge. Prefer a new pattern
only when there's a concrete reason — and if the PR has one, that's an interview question for the
user, not an assumption.

## Evidence standard

Every finding in this lens must name the other implementation or the established pattern with a path
and line, and show enough of it to make the comparison checkable.

Weak: *"This duplicates existing functionality."*

Strong: *"`DateRangeFormatter` at `feature/reports/DateRangeFormatter.kt:12` produces the same
`'MMM d – MMM d'` output as `core/ui/DateFormatting.kt:88`'s `formatDateRange()`, which is already
used by five call sites and handles the same-month and cross-year cases this one doesn't."*

End with a **Could not verify** list — including searches that were inconclusive, so synthesis knows
how much weight a "no duplicate found" carries.
