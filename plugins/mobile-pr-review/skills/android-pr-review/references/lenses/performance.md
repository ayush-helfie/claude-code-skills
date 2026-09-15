# Lens: Performance

**Model: sonnet.**

Look for performance problems that would actually be felt on a real device by a real user. This lens
has the worst noise-to-signal ratio if run carelessly, so the discipline below matters more than the
checklist.

## Classify every candidate

Before reporting anything, put it in one of three buckets:

1. **Actual performance problem** — measurable impact users would notice: jank, ANR, main-thread
   blocking, a query in a scroll listener, work that grows with data size in a hot path.
2. **Likely performance risk** — fine at today's data volumes, bad at plausible future ones, or on a
   low-end device. Worth raising with the scaling condition stated.
3. **Negligible micro-optimization** — theoretically wasteful, practically irrelevant.

Report bucket 1 and bucket 2. **Report bucket 3 only when there's a compelling reason** — it's in a
genuinely hot path, or it's a systematic pattern repeated across the PR.

Do not report theoretical micro-optimizations with no meaningful impact. An allocation in a function
called once at startup is not a finding, and reporting it makes the author discount your real ones.

## What to look for

**Work and allocation**
- unnecessary allocations, especially in loops, `onBind`, or recomposition
- repeated work that could be computed once
- redundant recomputation of a derived value
- inefficient collection operations — nested iteration where a map lookup would do; a chain building
  four intermediate lists over a large collection
- unnecessary copying of large structures
- excessive object creation in hot paths
- inefficient serialization/deserialization, or parsing the same payload twice

**I/O**
- repeated database queries, especially N+1 in a loop or per list item
- unnecessary network calls; a call that could be cached, batched, or deduplicated
- a query or request on the main thread

**Threading**
- incorrect coroutine dispatchers for the kind of work
- blocking calls inside suspend functions
- main-thread work — I/O, parsing, image decoding, large sorts, DB access

**Compose**
- unnecessary recomposition — unstable parameters, lambdas recreated each composition, reading state
  at too high a level in the tree
- inefficient Compose state handling; missing `derivedStateOf` where a hot derived value recomputes
  the subtree
- expensive work inside a Composable body rather than in an effect or `remember`
- `LazyColumn` items without stable keys

**Memory**
- memory retention beyond a component's useful life
- leaks — retained `Context`, `Activity`, `View`, or a listener never removed
- caches with no bound or eviction

**Lifecycle**
- work that continues while backgrounded and shouldn't
- work restarted on every configuration change that should have survived it

## Evidence standard

A performance finding needs a mechanism and a magnitude, not a vibe.

Weak: *"This could be slow."*

Strong: *"`loadOrders()` at `OrderRepository.kt:71` issues one `getCustomer()` query per order inside
the `map`, so a 200-order page runs 201 queries. It's called from `OrderListViewModel.init`, so it's
on the path to first render. `OrderDao` already has `getCustomersByIds()` at `OrderDao.kt:44`."*

State where in the call path it sits and what data volume makes it matter. If you can't establish
that the code is on a hot path, say so and mark the finding low-confidence rather than asserting
impact you haven't traced.

End with a **Could not verify** list.
