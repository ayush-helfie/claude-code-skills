---
name: pair-pr-reviewer
description: Use when the user wants to pair on or review a pull request together, group by group, choosing which review comments get posted, or shares a PR link asking to "pair and review".
---

# Pair PR reviewer

Review a PR with the user one group of files at a time. You bring verified findings; the user picks what gets posted.

## Setup (in parallel)
1. `gh pr view <n> --json id,title,body,files,commits,reviews,headRefOid` and save `gh pr diff` to the scratchpad. Read from a local checkout at the PR head if one exists.
2. Subagent (sonnet): the HD tickets in the PR body (Atlassian MCP, products-helfie.atlassian.net), their parent and linked issues, and linked or searched Confluence pages → ACs, requirement edge cases, open questions.
3. Subagent (opus, background): review every test file against the code it tests → severity table. Hold the result until the end.
4. Read the existing review comments (`gh api repos/<o>/<r>/pulls/<n>/comments`). Don't raise anything they already cover.
5. Split the production files into groups, bottom-up (storage/ports → domain → orchestration → UI → integration → build/docs). Wait for step 2 to finish, then show the requirement checks and the groups as tables and start group 1.

## Each group
Read the code yourself and check it against the requirements. Always present issues as a table:

| # | Sev | file:line | Observation + suggested fix |
|---|---|---|---|

- Sev is High, Med, Low or Nit. Add `(question)` when the answer depends on the author or the product.
- Add ✅ rows for things you checked that are correct.
- Verify every High yourself before reporting it, including ones a subagent found.
- End with "Which should I post?" and stop.

## Posting
1. Post only the numbers the user picks, merged the way they say. Send one review per group: `gh api -X POST repos/<o>/<r>/pulls/<n>/reviews --input review.json` with `commit_id` = head SHA, `event: COMMENT` and inline `comments` (`path`, `line`, `side: RIGHT`).
2. Write each comment as problem → why it matters → concrete fix.
3. Mark every file in the group as viewed: `gh api graphql -f query='mutation($id:ID!,$p:String!){markFileAsViewed(input:{pullRequestId:$id,path:$p}){clientMutationId}}' -f id=<PR node id> -f p=<path>`.
4. Give the review link, then present the next group.

## Finish
1. After the last production group, present the test findings as a table with a post/skip recommendation for each. Post what the user approves and mark the test files as viewed.
2. Summary: a table of the comments posted per group, then a must-fix-first list.
