# AGENTS.md

Subagents I use today (`~/.claude/agents/`). The reasoning behind each choice is in [docs/setup](./docs/setup/README.md), section 5.

## Own agents

| Agent | Model | Effort | Tools | Use |
|---|---|---|---|---|
| triage | Haiku | default | Read, Grep, Glob | cheap lookup: file, symbol, config, error (up to 120 tokens) |
| programador | Sonnet | low | Read, Write, Edit, Grep, Glob, Bash, Skill | implement and fix code, launch tests/batches |
| design | Sonnet | low | Read, Write, Edit, Grep, Glob, Bash, Skill | interface, colors, icons, layout |
| documentador | Sonnet | low | Read, Write, Edit, Grep, Glob, Bash | notes, docs, reports |
| teste | Sonnet | low | Read, Grep, Glob, Bash, Skill | run suites and report pass/fail |
| revisor | Sonnet | low | Read, Grep, Glob, Bash | review a diff without editing |
| pesquisador | Sonnet | low | + WebSearch, WebFetch | literature and data on the web |
| fisico | Sonnet | low | + WebSearch, WebFetch | physical/numerical analysis of results |
| Explore | Sonnet | low | Read, Grep, Glob, Bash | read-only sweep |

All with `maxTurns: 50` (except triage and Explore) and all read `~/.claude/regras_agentes.md` before starting.

## Native ones used

`general-purpose`, `Plan`, `claude-code-guide`, `statusline-setup`.

## Removed and why

- `caveman:cavecrew-builder/investigator/reviewer`: denied in `permissions.deny`; they fired without being asked and the return was weak. `triage` covers cheap lookup.
- `especialista` (Opus), `seguranca`, `devops`, `testador`: overlapped with the main session (already on Opus) and with `teste`/`revisor`.
- Routing by proxy combos (`combo/programacao` etc.): outside this repo; each agent declares its model in the frontmatter.

## Rules

- Delegate only large reads (more than ~5 files or large logs), web research, or when asked.
- Narrow question, fixed output format.
- Return graded: BOM, ACEITÁVEL or RUIM; RUIM goes back once with a more detailed prompt.
- Skills: `disable-model-invocation: true` for user-only ones. See `.agents/invocation.md`.
