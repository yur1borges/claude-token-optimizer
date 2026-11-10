# Contributing

## Before adding a Skill

Answer three questions. If any answer is no, do not add it:

1. Will it be used every week?
2. Is there no installed skill doing the same thing?
3. Does it save more tokens than its line in the listing costs?

## Adding a Skill

1. Create skill directory under `skills/engineering/` or `skills/productivity/`
2. Add `SKILL.md` with trigger, description, when to use, common questions, success criteria
3. Add docs page under `docs/engineering/` or `docs/productivity/`, including a `## Why it is in the setup` section
4. Update bucket `README.md` and top-level `README.md`
5. Run `scripts/link-skills.sh` to install locally

## Skill Requirements

- No em dashes in any prose
- Four doc sections: What it does, When to reach for it, Common questions, It's working if
- User-invoked or model-invoked (not both)
- `disable-model-invocation: true` for user-invoked

## Updating a Skill

1. Edit `SKILL.md` and docs page together
2. Validate and link

## Removing a Promoted Skill

1. Move to `skills/deprecated/`
2. Mark docs page as archived (see `.agents/writing-docs.md`)
3. Remove from READMEs
4. Validate and link