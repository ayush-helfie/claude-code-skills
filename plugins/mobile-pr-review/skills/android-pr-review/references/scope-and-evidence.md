# Phase 2 — Establish scope and gather evidence

Understand the whole change before you judge any part of it. A finding written before you understood
the scope is usually a finding about something the next file over already handles.

## Pulling the PR

```bash
# Metadata, description, commits, changed files
gh pr view <PR_URL_OR_NUMBER> --json number,title,body,author,state,baseRefName,headRefName,\
additions,deletions,changedFiles,commits,files,labels,reviews

# The full diff
gh pr diff <PR_URL_OR_NUMBER>

# Per-file stats when the diff is large
gh api repos/{owner}/{repo}/pulls/<n>/files --paginate \
  --jq '.[] | {path: .filename, status: .status, additions, deletions}'

# Existing review conversation - do not repeat points already made
gh api repos/{owner}/{repo}/pulls/<n>/comments --jq '.[] | {path, line, body: .body[0:200]}'
```

## Getting the code locally

Full-file reading needs a checkout. From the mobile repo:

```bash
git fetch origin pull/<n>/head:pr-<n>
git checkout pr-<n>
git merge-base HEAD origin/<baseRefName>      # the true diff base
git diff --stat $(git merge-base HEAD origin/<baseRefName>)..HEAD
```

If the user has no local checkout, fall back to reading file contents through
`gh api repos/{owner}/{repo}/contents/<path>?ref=<headRefName>` — but say so in the report, because
searching the repository for existing implementations is much weaker without a checkout, and that
weakens the duplication and project-patterns lenses.

## The ten scope questions

Answer all of these in the scope brief before reviewing individual changes:

1. What is the PR's **stated** purpose?
2. What is the **actual** scope of the changes?
3. What parts of the application are affected?
4. Which architectural layers are touched?
5. What are the relevant existing implementations surrounding the changed code?
6. What tests exist, and what do they cover for this change?
7. Does the PR contain unrelated changes?
8. Does the PR appear to be solving a larger problem than its stated scope?
9. Is the PR missing changes necessary to actually fulfill its stated purpose?
10. Does the implementation, as far as you can tell so far, achieve the stated intent?

## Read every changed file completely

This is one of the highest-priority rules in the whole review, and the one most likely to be quietly
skipped under time pressure. **Never review a file solely from its diff.**

A diff hunk shows you changed lines with three lines of context. Almost every real Android bug —
a lifecycle mismatch, a scope that outlives its owner, a second write path to the same state, a
`when` that lost its exhaustiveness — lives in the relationship between the changed lines and code
that is nowhere in the hunk. Reviewing hunks finds typos; reviewing files finds bugs.

For every changed file:

1. Read the complete file.
2. Understand its role and responsibilities.
3. Understand the code before and after the change.
4. Search for usages of what changed.
5. Search for related implementations.
6. Search for its tests.
7. Search for interfaces or base classes it participates in.
8. Search for sibling implementations.
9. Search for callers and consumers.

While reading, note: existing abstractions, imports and dependencies, state management, error
handling, lifecycle, concurrency, established patterns, naming conventions, and related tests.

If a finding depends on code outside the changed file, **read that code before reporting the
finding.** Also read surrounding files completely whenever they're needed to understand the change.

Never infer the contents of a file you have not read.

## Language discipline

Never write "this probably…", "this might…", or "it looks like…" when repository evidence can settle
the question. Go settle it. Those phrases are a signal that you stopped one search short.

Hedging is legitimate only where the answer genuinely isn't in the repository — an external API's
runtime behavior, a product requirement, a user's intent. Those go to the user (Phase 1) or into
"What I could not verify" in the report.

## Compare against the repository

For each major implementation decision in the PR, ask: **"How does this project already solve the same
problem?"**

The project itself is a primary source of truth, often outranking generic best practice. Search for
similar functionality before forming an opinion:

```bash
rg -t kotlin 'class \w*Repository' --files-with-matches
rg -t kotlin 'interface \w*(DataSource|Repository|UseCase)'
rg -t kotlin -l 'sealed (class|interface) \w*(State|Result|Error)'
```

Prefer consistency with the existing pattern when it is sound, the new problem is materially
equivalent, and there is no demonstrated reason to diverge.

Prefer a new pattern only when there's a concrete reason for it.

**Do not criticize the PR for violating a generic convention when the repository consistently follows
a different deliberate one.** Conversely, flag it when the PR introduces a new pattern for a problem
the project already has an established answer to. And when you find two implementations solving the
same problem, call that out explicitly — parallel implementations that drift apart are among the most
expensive things a codebase accumulates.

## The scope brief

Write `<scratchpad>/pr-<number>/scope-brief.md` with:

- PR number, title, author, base and head branches
- The author's stated intent, and what they told you in the interview
- Changed files grouped by architectural layer, with a one-line note on each file's role
- The existing implementations and patterns surrounding the change
- Test files that touch the affected behavior
- Your answers to the ten scope questions
- Open questions you could not resolve

Every lens subagent receives this. Nine agents working from a good brief review the change; nine
agents without one each re-derive the context badly and disagree about basic facts.
