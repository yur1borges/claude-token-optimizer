<p>
  <a href="https://www.aihero.dev/s/skills-newsletter">
    <picture>
      <source media="(prefers-color-scheme: dark)" srcset="https://res.cloudinary.com/total-typescript/image/upload/v1777382277/skills-repo-dark_2x.png">
      <source media="(prefers-color-scheme: light)" srcset="https://res.cloudinary.com/total-typescript/image/upload/v1777382277/skill-repo-light_2x.png">
      <img alt="Skills" src="https://res.cloudinary.com/total-typescript/image/upload/v1777382277/skill-repo-light_2x.png" width="369">
    </picture>
  </a>
</p>

# Skills For Real Engineers

[![skills.sh](https://skills.sh/b/mattpocock/skills)](https://skills.sh/mattpocock/skills)

My agent skills that I use every day to do real engineering — not vibe coding.

Developing real applications is hard. Approaches like GSD, BMAD, and Spec-Kit try to help by owning the process. But while doing so, they take away your control and make bugs in the process hard to resolve.

These skills are designed to be small, easy to adapt, and composable. They work with any model. They're based on decades of engineering experience. Hack around with them. Make them your own. Enjoy.

If you want to keep up with changes to these skills, and any new ones I create, you can join ~60,000 other devs on my newsletter:

[Sign Up To The Newsletter](https://www.aihero.dev/s/skills-newsletter)

## Installation (30-second setup)

A plugin updates itself. [skills.sh](https://skills.sh/mattpocock/skills) copies editable files into your project, and you update them by hand. Pick one per agent, because installing both gives you every skill twice.

### 1. Get the skills

<details>
<summary><strong>Claude Code</strong></summary>

```bash
claude plugin install mattpocock-skills@claude-plugins-official
```

Updates itself by default.

</details>

<details>
<summary><strong>Codex</strong></summary>

```bash
codex plugin marketplace add mattpocock/skills
codex plugin add mattpocock-skills@mattpocock
```

Updates itself at startup.

</details>

## Skills

Skills are organized into bucket folders under `skills/`:

- `engineering/`: daily code work
- `productivity/`: daily non-code workflow tools
- `misc/`: kept around but rarely used, not promoted
- `in-progress/`: beta: public on purpose, feedback wanted, not shipped in the plugin
- `deprecated/`: no longer used

### Engineering

#### User-invoked

- [brainstorming](./skills/engineering/brainstorming/SKILL.md) — Prerequisite for creative work
- [find-skills](./skills/engineering/find-skills/SKILL.md) — Discover and install skills
- [graphify](./skills/engineering/graphify/SKILL.md) — Code knowledge graph
- [humanizer](./skills/engineering/humanizer/SKILL.md) — Remove AI writing patterns
- [impeccable](./skills/engineering/impeccable/SKILL.md) — High-end frontend design
- [llm-council](./skills/engineering/llm-council/SKILL.md) — 5-advisor council for hard decisions
- [systematic-debugging](./skills/engineering/systematic-debugging/SKILL.md) — Root-cause-first debugging
- [task-observer](./skills/engineering/task-observer/SKILL.md) — Monitor multi-step task execution
- [taste-skill](./skills/engineering/taste-skill/SKILL.md) — Anti-slop frontend design
- [test-driven-development](./skills/engineering/test-driven-development/SKILL.md) — Mandatory TDD
- [teste-leigo](./skills/engineering/teste-leigo/SKILL.md) — Layperson testing for desktop apps
- [ui-ux-pro-max](./skills/engineering/ui-ux-pro-max/SKILL.md) — Design intelligence (79 styles, 192 palettes)
- [verification-before-completion](./skills/engineering/verification-before-completion/SKILL.md) — Evidence before claims
- [writing-plans](./skills/engineering/writing-plans/SKILL.md) — Implementation plans for multi-step tasks

#### Model-invoked

(none currently)

### Productivity

#### User-invoked

- [caveman](./skills/productivity/caveman/SKILL.md) — Terse, smart mode
- [ponytail](./skills/productivity/ponytail/SKILL.md) — Lazy senior developer

#### Model-invoked

(none currently)

### Misc

(none currently)

### In Progress

(none currently)

### Deprecated

(none currently)

## Agents

See [AGENTS.md](./AGENTS.md) for available agent types and routing configuration.

## Documentation

Human-facing docs for promoted skills live under `docs/`:

- [Engineering skills](./docs/engineering/)
- [Productivity skills](./docs/productivity/)

## Contributing

See [CONTRIBUTING.md](./CONTRIBUTING.md).

## License

MIT — see [LICENSE](./LICENSE).