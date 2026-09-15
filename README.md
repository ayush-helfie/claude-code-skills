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
| [mobile-pr-review](./plugins/mobile-pr-review) | `android-pr-review` | Multi-agent, evidence-driven senior review of an Android/Kotlin PR: interviews you first, gathers evidence via `gh`, runs nine specialized review lenses in parallel, verifies every finding against real code and current docs, and writes a prioritized review report with a verdict. |

This table is populated as plugins are added under `plugins/`. See [CLAUDE.md](./CLAUDE.md) for the conventions to follow when adding or updating a plugin/skill.
