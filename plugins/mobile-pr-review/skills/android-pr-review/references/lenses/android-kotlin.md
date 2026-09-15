# Lens: Android & Kotlin idiomaticity

**Model: sonnet.**

Review this as an experienced Android/Kotlin engineer would: not "does it compile", but "is this how
someone fluent in this platform would have written it, and does it behave correctly on a real device?"

## Kotlin

- **Nullability** — is null used meaningfully, or is `!!` papering over an unclear contract? Are
  platform types from Java interop handled? Is nullability lost or invented in mapping layers?
- **Sealed classes/interfaces** — is a sealed hierarchy used where the state space is closed? Is
  `when` exhaustive without an `else` that will silently swallow a future case?
- **Data classes** — appropriate use; `copy` not defeating intended immutability; `equals`/`hashCode`
  correct with array or mutable members
- **Extension functions** — do they improve readability, or scatter behavior away from its type?
- **Scope functions** — `let`/`run`/`apply`/`also`/`with` used for clarity, not chained into a puzzle
- **Collection APIs** — idiomatic operations; no manual loop reimplementing `groupBy`; no chain that
  allocates four intermediate lists in a hot path (coordinate with the performance lens)
- **Immutability** — `val` over `var`, read-only collection types at boundaries
- **Visibility** — `internal`/`private` rather than defaulting everything to public API

## Coroutines and Flow

This is where most Android review value lives. Verify semantics against documentation rather than
memory (see `../documentation-research.md`).

- **Structured concurrency** — no `GlobalScope`; every coroutine has an owner that will cancel it
- **Scopes** — `viewModelScope`, `lifecycleScope`, or an injected scope, matching the work's lifetime
- **Dispatchers** — correct dispatcher for the work; injected rather than hardcoded so it's testable;
  no blocking call on `Dispatchers.Main`
- **Cancellation** — cooperative cancellation respected; `CancellationException` not swallowed by a
  broad `catch (e: Exception)`; cleanup in `finally` where needed
- **Exception handling** — understand how exceptions propagate in the scope being used; a
  `CoroutineExceptionHandler` placed where it will actually fire
- **Flow** — cold vs hot understood; operators applied in an order that does what's intended;
  `flowOn` where the upstream context matters
- **StateFlow/SharedFlow** — `StateFlow` for state, `SharedFlow` for events; replay and buffer
  configured deliberately; conflation not dropping something that mattered
- **Collection** — lifecycle-aware collection in UI; no collection that keeps running past the
  owner's death
- **suspend functions** — main-safe by convention, or documented if not

## Compose (where applicable)

- state hoisting; Composables that read state they don't own
- `remember` / `rememberSaveable` used correctly, and `mutableStateOf` always remembered
- `LaunchedEffect` / `DisposableEffect` / `SideEffect` chosen correctly and keyed correctly
- no state mutation during composition
- stability and unnecessary recomposition (coordinate with the performance lens)
- `derivedStateOf` where a derived value would otherwise recompose the world
- previews, modifiers passed and ordered conventionally, `Modifier` parameter first-and-default

## Android platform

- **ViewModel usage** and state ownership — who owns what, and does it survive what it must
- **Lifecycle** — work started and stopped at the right callbacks; nothing leaking past `onDestroy`
- **Configuration changes** — state survives rotation
- **Process death** — `SavedStateHandle` where the state genuinely must survive it
- **Threading** — no main-thread I/O or heavy work
- **Resources** — strings externalized, dimens and themes used per project convention, no hardcoded
  colors where a theme exists
- **Dependency injection** — consistent with the project's Hilt/Dagger/Koin usage and scoping
- **Repository / use-case patterns** — only where the project meaningfully uses them

## Two cautions

**Don't replace clear code with clever Kotlin for its own sake.** A readable `for` loop is not a
finding just because a chain of `fold` and `associateWith` exists. Prefer the simplest implementation
that communicates intent.

**Don't apply generic best practice against the project's deliberate, consistent convention.** If
every feature in this repo does something a particular way, the PR following that way is correct
here, whatever a blog post says. See `../scope-and-evidence.md`.

End with a **Could not verify** list.
