# claude-token-optimizer

Agent skills for Claude Code: organized, documented, ready to use.

Skills are small, composable, and work with any model. Based on real engineering workflows. Hack them. Make them yours.

## Installation

```bash
git clone https://github.com/yur1borges/claude-token-optimizer
cd claude-token-optimizer
bash scripts/link-skills.sh
```

Symlinks each promoted skill into `~/.claude/skills` and `~/.agents/skills` (works for Claude Code and Codex). Re-run after `git pull`.

Check the repo (frontmatter, links, em dashes): `bash scripts/check.sh`

## My setup

How I organize skills, hooks and settings to save tokens: [docs/setup](./docs/setup/README.md).

## Skills

Organized into buckets under `skills/`:

- `engineering/`: daily code work
- `productivity/`: daily non-code workflow tools
- `misc/`: kept around, rarely used, not promoted
- `in-progress/`: beta, feedback wanted, not in plugin
- `deprecated/`: no longer used

### Engineering (User-invoked)

- [brainstorming](./skills/engineering/brainstorming/SKILL.md): Prerequisite for creative work
- [find-skills](./skills/engineering/find-skills/SKILL.md): Discover and install skills
- [graphify](./skills/engineering/graphify/SKILL.md): Code knowledge graph
- [humanizer](./skills/engineering/humanizer/SKILL.md): Remove AI writing patterns
- [impeccable](./skills/engineering/impeccable/SKILL.md): High-end frontend design
- [llm-council](./skills/engineering/llm-council/SKILL.md): 5-advisor council for hard decisions
- [systematic-debugging](./skills/engineering/systematic-debugging/SKILL.md): Root-cause-first debugging
- [task-observer](./skills/engineering/task-observer/SKILL.md): Monitor multi-step task execution
- [taste-skill](./skills/engineering/taste-skill/SKILL.md): Anti-slop frontend design
- [test-driven-development](./skills/engineering/test-driven-development/SKILL.md): Mandatory TDD
- [teste-leigo](./skills/engineering/teste-leigo/SKILL.md): Layperson testing for desktop apps
- [ui-ux-pro-max](./skills/engineering/ui-ux-pro-max/SKILL.md): Design intelligence (79 styles, 192 palettes)
- [verification-before-completion](./skills/engineering/verification-before-completion/SKILL.md): Evidence before claims
- [writing-plans](./skills/engineering/writing-plans/SKILL.md): Implementation plans for multi-step tasks

### Productivity (User-invoked)

- [caveman](./skills/productivity/caveman/SKILL.md): Terse, smart mode
- [ponytail](./skills/productivity/ponytail/SKILL.md): Lazy senior developer

### Misc / In Progress / Deprecated

(None currently)

## Agents

See [AGENTS.md](./AGENTS.md) for agent types and routing configuration.

## Documentation

Human-facing docs for promoted skills under `docs/`:

- [Engineering skills](./docs/engineering/)
- [Productivity skills](./docs/productivity/)

## Contributing

See [CONTRIBUTING.md](./CONTRIBUTING.md).

