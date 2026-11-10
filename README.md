# claude-token-optimizer

The set of skills, plugins, hooks and settings I use in Claude Code to **spend fewer tokens without losing quality**. It is not a large collection of skills: it is a small, deliberate selection, with the reason for each piece and for each thing that was left out.

State as of November 2026. The full setup, with every setting and hook explained, is in [docs/setup](./docs/setup/README.md).

## Why so few skills

Installing skills is easy; each one looks free. It is not. I kept only 13 (11 engineering and 2 productivity) for four reasons:

1. **Every visible skill is charged in every session.** The name and description of each skill go into the listing at the start, which is part of the prefix of every turn. 100 skills with 150-character descriptions are ~15 thousand characters (about 4 thousand tokens) paid before any question, even if none is used.
2. **Too many skills confuse the choice.** With dozens of similar descriptions ("design", "frontend", "UI"), the model calls the wrong one, calls two, or calls none. With one skill per type of task, the trigger is clear: a bug calls `systematic-debugging`, an interface calls `ui-ux-pro-max`.
3. **Overlapping skills fight each other.** Three design guides or two "short answer" modes give different instructions for the same thing. The result is longer text (the model tries to satisfy both) and less consistency.
4. **Rituals cost more than they save.** Skills that require a long process before every task (brainstorming, formal plan, 5-model council) make sense in a large, new project. Day to day, with tasks of 1 to 3 files, they spend more tokens than they save in rework.

The rule that remains: **a skill gets in only if I use it every week, if no other does the same thing, and if it saves more than it costs in the listing.** The rest stays off (moved to `~/.claude/skills_desligadas/`, not deleted) and comes back with a `mv` when I need it.

## The skills and why each one

### Engineering: `skills/engineering/`

| Skill | What it does | Why this one and not another |
|---|---|---|
| [systematic-debugging](./skills/engineering/systematic-debugging/SKILL.md) | finds the root cause before proposing a fix | avoids the "try, fail, try" cycle, which is the biggest waste of tokens in a bug. Beat `diagnosing-bugs` (mattpocock) for being shorter |
| [verification-before-completion](./skills/engineering/verification-before-completion/SKILL.md) | forces running the test and seeing the output before saying "done" | a false "done" costs a whole session back. Cheap and always useful |
| [test-driven-development](./skills/engineering/test-driven-development/SKILL.md) | writes the test before the code | `user-invocable-only`: useful for new logic, too expensive if it fires on every edit |
| [ui-ux-pro-max](./skills/engineering/ui-ux-pro-max/SKILL.md) | interface guide (layout, color, typography, accessibility) | the **only** design skill called automatically. Covers web and desktop (my apps are PyQt), which the others do not |
| [impeccable](./skills/engineering/impeccable/SKILL.md) | fine polish for web frontend | only under `/impeccable`: good for a carefully made web page, redundant with ui-ux-pro-max otherwise |
| [taste-skill](./skills/engineering/taste-skill/SKILL.md) | "anti-generic" art direction for websites | on demand only, for the same reason. Kept because it gives a different visual result when I want it |
| [teste-leigo](./skills/engineering/teste-leigo/SKILL.md) | tests a desktop app like an impatient user | written by me; no public skill tests a desktop GUI like this |
| [graphify](./skills/engineering/graphify/SKILL.md) | graph of the code's files and calls | only to **locate** files in a large repo; reading the whole graph would cost more than a grep |
| [humanizer](./skills/engineering/humanizer/SKILL.md) | removes AI text patterns | on demand only, for texts that go to people (email, report) |
| [find-skills](./skills/engineering/find-skills/SKILL.md) | searches for and installs a skill when one is missing | avoids installing large packages "just in case": I look for the skill when I need it |
| [task-observer](./skills/engineering/task-observer/SKILL.md) | records corrections and patterns to improve the skills | `user-invocable-only`: the original description asks to run in every session, which would be expensive |

### Productivity: `skills/productivity/`

| Skill | What it does | Why |
|---|---|---|
| [caveman](./skills/productivity/caveman/SKILL.md) | terse answers, no ceremony, every technical fact kept | output is the most expensive token; cuts 40 to 60% of the text. Beat `token-diet`, which did the same and more things I did not want |
| [ponytail](./skills/productivity/ponytail/SKILL.md) | smallest change that solves the whole task | less code written means less output, less review and fewer bugs. Replaced `mattpocock-skills` and `andrej-karpathy-skills`, which gave similar advice in more text |

Both run by hook at session start. That is why they are `user-invocable-only`: they are already active and do not need to take up space in the listing.

### Disabled: `skills/deprecated/`

| Skill | Why it left |
|---|---|
| [brainstorming](./skills/deprecated/brainstorming/SKILL.md) | required an ideas session before any creative task; expensive and almost always unnecessary |
| [writing-plans](./skills/deprecated/writing-plans/SKILL.md) | long formal plan; replaced by a short plan in a file only when the task has more than 3 steps |
| [llm-council](./skills/deprecated/llm-council/SKILL.md) | 5 "advisors" per decision multiply the cost by 5 |

## How the repo is organized

```
skills/
  engineering/    daily use on code (promoted: go to ~/.claude/skills)
  productivity/   way of working, outside code (promoted)
  misc/           stored, rare use, not installed
  in-progress/    under test, not installed
  deprecated/     disabled, kept as reference
docs/
  engineering/    one page per skill: what it does, when to use it, why it is here
  productivity/
  setup/          my real setup: settings, hooks, agents, MCPs, with the why
.agents/          rules for whoever edits the repo and recorded decisions (ADRs)
scripts/          installation (link-skills.sh) and checking (check.sh)
```

**Why buckets:** separating "promoted" from "stored" makes it clear what goes into the context. Only `engineering/` and `productivity/` are installed; removing a skill from the setup is moving it to another folder, without losing history.

**Why skill and doc separate:** `SKILL.md` is read by the model and must be short. The page in `docs/` is for people and can explain the context without costing tokens.

**What is not here:** personal skills (my research software, Lattes, XRD, DEM) and configurations with paths and keys. See [SCOPE.md](./SCOPE.md).

## Installation

```bash
git clone https://github.com/yur1borges/claude-token-optimizer
cd claude-token-optimizer
bash scripts/link-skills.sh
```

Creates links for each promoted skill in `~/.claude/skills` and `~/.agents/skills` (works for Claude Code and Codex). Run again after `git pull`.

Check (frontmatter, links, em dashes): `bash scripts/check.sh`

## More

- [docs/setup](./docs/setup/README.md): settings, plugins, hooks, subagents and MCPs, with the why of each one
- [AGENTS.md](./AGENTS.md): subagents and when to delegate
- [CONTRIBUTING.md](./CONTRIBUTING.md): how to add or retire a skill
