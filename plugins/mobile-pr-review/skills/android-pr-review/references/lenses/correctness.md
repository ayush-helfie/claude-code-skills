# Lens: Scope & correctness

**Model: opus.** Subtle concurrency and lifecycle reasoning is where a weaker pass produces
confident, plausible, wrong answers.

Your question: **does this actually work, and does it do what the PR says it does?**

## Start with intent

1. Does the PR accomplish its stated goal? Trace the change end to end and confirm it, rather than
   assuming the author's description matches the diff — that mismatch is one of the most valuable
   things this review can catch.
2. Is the implementation logically correct?
3. Are there missing cases?
4. Are there unintended behavioral changes — things that now behave differently and weren't meant to?
5. Are edge cases handled?
6. Is error handling correct?
7. Are lifecycle and state transitions correct?
8. Does it behave correctly under realistic Android conditions — rotation, process death, no network,
   slow network, backgrounding mid-operation, rapid repeated taps?

## Defect catalog

Work through these deliberately. Most are invisible in a diff hunk and only appear once you've read
the whole file and its callers.

**Logic and data**
- incorrect conditions — inverted comparisons, wrong boundary, `&&`/`||` mixups
- incorrect null handling — `!!`, unsafe platform types from Java interop, nullable lost in mapping
- incorrect equality/identity assumptions — `data class` with array fields, `==` on instances that
  should be compared by id, `equals`/`hashCode` not updated alongside a new property
- incorrect serialization — missing `@Serializable`, renamed fields breaking persisted payloads,
  default values masking absent fields, enum values that won't round-trip
- incorrect caching — stale reads, cache not invalidated on write, key collisions
- incorrect API assumptions — verify the contract in the docs before asserting

**Concurrency**
- race conditions — check-then-act on shared state, concurrent mutation of a collection
- coroutine cancellation problems — work that should be cancelled isn't, or `CancellationException`
  swallowed by a broad `catch (e: Exception)`
- structured concurrency violations — `GlobalScope`, a scope that outlives its owner, a job launched
  where nothing awaits or cancels it
- incorrect threading — main-thread I/O, or the wrong dispatcher for the work
- suspend functions that block instead of suspending

**Lifecycle and state**
- lifecycle bugs — collection that isn't lifecycle-aware, work continuing after the owner is gone
- stale state — state read once that should be observed, or a snapshot that outlives its validity
- incorrect state restoration — `SavedStateHandle` not used where process death matters
- memory leaks — a retained `Context`, `Activity`, or `View`; a listener never removed; a long-lived
  scope holding a short-lived reference
- resource leaks — `Cursor`, `InputStream`, `Closeable` not closed on the error path

**Events and flows**
- duplicate events — a one-shot event replayed on reconfiguration, or a `SharedFlow` with replay
  where it shouldn't have one
- lost events — emitted to a flow with no active collector, or a buffer that drops silently
- incorrect retry behavior — retrying non-retryable errors, no backoff, no cap, retry that ignores
  cancellation

**Persistence and navigation**
- database consistency problems — missing transaction around multi-step writes, missing migration,
  a schema change with no migration path
- incorrect navigation — wrong back-stack behavior, args not passed, deep link broken, navigation
  from a destroyed destination

**Compose**
- incorrect Compose state — state read outside composition, `mutableStateOf` not remembered,
  a `LaunchedEffect` keyed wrong so it re-runs or never re-runs, `derivedStateOf` missing where it
  matters, mutation during composition

**Empty, loading, error**
- edge cases around empty, loading, and error states — the three that get skipped most, and the three
  users hit first

## Verify before you report

Verify every suspected bug against callers, the API's documentation, and the actual code path before
reporting it. A confidently-reported bug that doesn't exist costs the author more time than a bug you
missed, and it's the fastest way to make your real findings get skimmed.

For each candidate finding, be able to answer: what input or state produces the wrong behavior, and
what goes wrong? If you can't construct that scenario concretely, either keep digging or mark it
low-confidence and put it in "Could not verify".

End your report with a **Could not verify** list — suspicions you couldn't settle from the repository,
with what would settle them.
