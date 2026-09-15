# Working in this repo

This repo is a Claude Code plugin marketplace. Follow these conventions when adding a new plugin/skill or updating an existing one.

## Layout

- One plugin per logical grouping of skills — don't dump unrelated skills into one plugin.
- Each plugin lives at `plugins/<plugin-name>/`:
  ```
  plugins/<plugin-name>/
  ├── .claude-plugin/
  │   └── plugin.json
  └── skills/
      └── <skill-name>/
          └── SKILL.md
  ```
- If a plugin has exactly one skill, `SKILL.md` may live at the plugin root instead of `skills/<skill-name>/SKILL.md`.
- Plugin and skill names are kebab-case.

## `plugin.json`

Only `name` is required; also set `description` and `version`:

```json
{
  "name": "my-plugin",
  "description": "What this plugin does",
  "version": "1.0.0"
}
```

## `SKILL.md` frontmatter

- `name` — the skill's identifier.
- `description` — what it does and when it should trigger. This is what Claude uses to decide whether to auto-invoke the skill, so be specific about the trigger conditions, not just the capability.
- `disable-model-invocation: true` — set if the skill should only ever be run explicitly by a user (e.g. `/skill-name`), never auto-invoked.
- `user-invocable: false` — set if the skill should only be invoked by Claude, never directly by a user command.
- `allowed-tools` — pre-approve specific tool calls the skill needs (e.g. `Bash(git *)`).
- `context: fork` — set if the skill should run in an isolated subagent rather than the main conversation.

Use the `superpowers:writing-skills` skill for guidance on authoring a good SKILL.md (structure, checklist, testing before deployment) when working in a session that has it available.

## Required when adding or updating a plugin

1. Validate it: `claude plugin validate ./plugins/<plugin-name>`.
2. Register/update its entry in `.claude-plugin/marketplace.json`'s `plugins` array:
   ```json
   { "name": "<plugin-name>", "source": "./plugins/<plugin-name>", "description": "..." }
   ```
3. Update the **Available skills** table in `README.md` to list every skill the plugin provides.

A plugin is not done until all three steps above are complete — a plugin directory that isn't registered in `marketplace.json` won't be installable, and one missing from the README won't be discoverable.
