# Contributing

## Adding a Skill

1. Create skill directory under `skills/engineering/` or `skills/productivity/`
2. Add `SKILL.md` with trigger, description, when to use, common questions, success criteria
3. Add docs page under `docs/engineering/` or `docs/productivity/`
4. Update bucket `README.md` and top-level `README.md`
5. Add entry to `.claude-plugin/plugin.json` skills array
6. Run `claude plugin validate . --strict`
7. Run `scripts/link-skills.sh` to install locally

## Skill Requirements

- No em dashes in any prose
- Four doc sections: What it does, When to reach for it, Common questions, It's working if
- User-invoked or model-invoked (not both)
- `disable-model-invocation: true` for user-invoked

## Updating a Skill

1. Edit `SKILL.md` and docs page together
2. Update `ask-matt` router if user-reachable skill changed
3. Validate and link

## Removing a Promoted Skill

1. Move to `skills/deprecated/`
2. Mark docs page as archived (see `.agents/writing-docs.md`)
3. Remove from READMEs and plugin.json
4. Validate and link