---
name: addressing-review-comments
description: Use when the user shares a pull request whose review comments they want to work through or fix ("check the comments", "let's plan the fixes"), especially when the code is a shared module that other apps or repos consume.
---

# Addressing review comments

Turn review feedback into evidence-backed decisions, made one at a time, then a plan, then fixes and replies. Change no code and post nothing without approval.

## 1. Gather
- Run `gh api --paginate` to fetch inline comments, review bodies and issue comments, and save them to the scratchpad. Count them, including the bullets inside summary reviews.
- If the user hasn't said, ask which consumer branches or PRs wire this code.

## 2. Verify (parallel subagents, grouped by area)
For each comment, record: **Real / Partly / Not real**, `file:line` evidence, the root cause, and the comments that share it.
- **Read the consumers' code before deciding.** Actual usage often flips a verdict, or explains odd code. For example, a gate that looks pointless may be preventing a logout.
- **Test the reviewer's fix against their own scenario.** It often doesn't fix the case they describe.
- **Look for a repo precedent** for the fix shape.
- **Back every claim with a source**: library source or docs, a compile, or existing code. If the user challenges a claim, verify it. Don't defend it.

## 3. Decide non-test comments, one per message
Send this card, then wait for the answer:

```
## N · <title> (#ids)
**Problem**
**What consumers do**: table, with file:line
**Root cause**: one line
**Options**: | | Change | Pros | Cons |, recommended first
**Recommendation** + the one decision needed
```

Answer factual questions from the code. Ask the user only for decisions.

## 4. Decide test comments, all in one table
Prefer deleting, renaming or modifying existing tests. Add a new test only when it pins behaviour that this round changes, or a core invariant. Give a reason for every skipped gap; that reason becomes its reply.

## 5. Plan
Use superpowers:writing-plans.
- Order moves and renames first.
- Mark any task that deviates from a decision, and confirm it before executing.
- Include a consumer **integration guide**: what changed, and the app file each change touches.
- Include a task for the thread replies and the PR description.

## 6. After the fixes (show drafts first)
- Reply in each thread with what changed, the commit, and why. Where you pushed back, include the evidence.
- Resolve the threads.
- Update the PR description from base to tip, with the integration guide.

## Common mistakes
| Mistake | Instead |
|---|---|
| Deciding in batches by group | One card per non-test comment |
| Adopting a well-specified fix unchecked | Check that it fixes the reviewer's scenario |
| A new test for every gap | Minimal tests, plus a reason for each skip |
| Asking the user for facts | Read the consumers' code |
