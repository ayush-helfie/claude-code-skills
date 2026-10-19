# claude-code-skills

A [Claude Code](https://claude.com/claude-code) plugin marketplace: a collection of installable plugins, each providing one or more skills.

## Adding this marketplace

```
/plugin marketplace add ayush-helfie/claude-code-skills
```

## Installing a plugin

```
/plugin install <plugin-name>@claude-code-skills
```

## Available skills

| Plugin | Skill | Description |
| --- | --- | --- |
| [pr-helper](./plugins/pr-helper) | `pr-description` | Writes PR titles and bodies that stay in sync with the Jira ticket: HD key, the ticket's ACs as a checklist (researched in Jira/Confluence and confirmed with you when unclear), verification and build for QA. A hook blocks `gh pr create` until the body has acceptance criteria. |
| [pair-pr-reviewer](./plugins/pair-pr-reviewer) | `pair-pr-reviewer` | Pair-reviews a PR with you group by group: gathers Jira/Confluence context, shows findings as tables, posts only the comments you pick as inline reviews, marks each reviewed group's files as viewed, and reviews the tests last. |
| [review-responder](./plugins/review-responder) | `addressing-review-comments` | Works through review comments on your PR: verifies each against the code and the apps that consume it, decides non-test comments with you one at a time, batches test comments with minimal new tests, plans the fixes with a consumer integration guide, then replies to and resolves threads and updates the PR description. |

This table is populated as plugins are added under `plugins/`. See [CLAUDE.md](./CLAUDE.md) for the conventions to follow when adding or updating a plugin/skill.
