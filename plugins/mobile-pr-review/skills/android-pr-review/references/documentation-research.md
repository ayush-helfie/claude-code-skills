# Phase 3 — Research the technical context

Before the detailed review, do a small research pass to establish technical context. Research **only
what is relevant to this PR** — this is a targeted lookup, not a survey of Android.

## Why

Android and Kotlin APIs move, and model memory of them ages badly. Recollections of lifecycle
semantics, Compose APIs, Flow operator behavior, and "the recommended approach" go stale within a
release or two, and a confident finding built on a stale recollection is worse than no finding: it
sends the author to change working code.

So the rule is simple — **do not rely on memory when an authoritative source is available.**

## Prefer primary sources

- Android Developers (developer.android.com)
- Kotlin documentation (kotlinlang.org)
- JetBrains documentation
- Official AndroidX documentation and release notes
- The official documentation of whichever library the PR touches
- Official API reference for the specific class or function

Blog posts and Stack Overflow answers can point you at the right question but should not settle it.

## What to verify

Look up the behavior the implementation actually depends on:

- API behavior and contracts
- lifecycle semantics
- threading guarantees
- coroutine behavior, especially cancellation and exception propagation
- Compose behavior — recomposition, state, effect APIs, stability
- `Flow` / `StateFlow` / `SharedFlow` semantics — operator behavior, buffering, conflation, replay
- Room behavior — transactions, migrations, query threading, `Flow` emissions
- WorkManager behavior — constraints, uniqueness, retry and backoff, expedited work
- Navigation behavior — back stack, arguments, deep links, state restoration
- dependency injection library behavior and scoping
- serialization library behavior
- networking library behavior
- deprecated versus currently recommended approaches
- performance characteristics
- platform constraints and API-level differences

## Check what the project is actually on

An API's current documentation is irrelevant if the project is three major versions behind. Before
citing docs, check what's in use:

```bash
cat gradle/libs.versions.toml 2>/dev/null
rg 'compileSdk|minSdk|targetSdk' --glob '*.gradle*'
rg 'kotlin.*version|composeBom|lifecycle-|room-|work-' --glob '*.gradle*' --glob '*.toml'
```

Then verify against the documentation *for those versions*.

## Hold findings to this standard

This phase runs again, implicitly, during synthesis:

- If documentation contradicts a lens agent's assumption, **discard the finding.** Don't soften it —
  drop it. A finding that survived only because nobody checked is not a finding.
- If documentation confirms a suspected bug, cite the specific source in the finding's **Evidence**.
  A finding that cites the coroutines guide on cancellation semantics is one the author can act on;
  the same finding without the citation is an argument.
- If documentation is ambiguous or doesn't cover the case, say so rather than resolving it in
  whichever direction supports your finding.

## Don't over-apply it

Do not blindly apply generic "best practices" when the official documentation or the project's actual
architecture indicates otherwise. Documentation describes what an API does; it does not decide what
this codebase should do. Where the two conflict, the project's deliberate, consistent choice usually
wins — see `scope-and-evidence.md`.

Write what you find to `<scratchpad>/pr-<number>/research-notes.md`, with a source URL per claim, and
pass it to the lens subagents alongside the scope brief so they aren't each re-researching the same
API.
