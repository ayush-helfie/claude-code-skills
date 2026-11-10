---
name: pr-description
description: Use when opening, creating, raising, drafting or pushing a pull request or PR (gh pr create), finishing a branch, "ship it", "send for review", "ready for review", or writing a PR title, description or body, including port or cherry-pick PRs to main or prod-main.
---

# PR description

The Jira key links the PR to the ticket; the body carries what Jira can't.

1. Branch `<type>/HD-<n>-<slug>`, title `<type>(HD-<n>): <user-visible change>`. Ask for the key if none is known.
2. Fetch the ticket (Atlassian MCP `getJiraIssue`). Copy its acceptance criteria, or a bug's Expected Result, into the checklist.
3. If the ticket has no clear ACs, research before asking: its parent, linked issues and comments in Jira, and linked or searched Confluence pages. Draft the ACs from what you find, cite the sources, and confirm them with the user (AskUserQuestion) before writing the body.
4. Fill the body below. It is the org PR template (`Helfie-Platform/.github/pull_request_template.md`, enforced by an automated check) followed by our two sections. Keep every heading, in this order, spelled exactly. Write `None` under an org heading that doesn't apply; never delete it. Acceptance criteria is required. Never leave placeholders or template comments.

```markdown
**Ticket:** [HD-<n>](https://products-helfie.atlassian.net/browse/HD-<n>)

## User-Facing Changes
<What changes for the user, in plain words, or None.>

## Technical Changes
<Root cause for a bug or reason for a feature, then the significant implementation, API or infrastructure changes. For a port: Port of PR #<n> on main / prod-main.>

## Feature Flags
<Flags added, changed or removed, with their intended state, or None.>

## Risks
<Known gaps, limitations, accepted trade-offs, follow-ups, what to review first, or None.>

## Acceptance criteria
- [ ] <one line per AC from the ticket>

## How verified
- [ ] Unit tests: <which>
- [ ] Device or emulator: <env, build>
- [ ] Screenshots or recording for UI changes, also attached to the ticket

Build for QA: <env and version, e.g. Staging 1.0(1.41)>
```
