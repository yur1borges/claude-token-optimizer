# AGENTS.md

This file documents the agent types available in this skills repository.

## Agent Types

| Agent | Description | Model | Effort |
|-------|-------------|-------|--------|
| caveman:cavecrew-builder | Surgical 1-2 file edits | Haiku | low |
| caveman:cavecrew-investigator | Read-only code locator | Haiku | low |
| caveman:cavecrew-reviewer | Diff/branch/file reviewer | Haiku | low |
| claude | Catch-all general agent | Sonnet 4.6 | low |
| claude-code-guide | Claude Code/SDK/API questions | Haiku | low |
| design | Interface, colors, icons, layout | Sonnet 4.6 | low |
| devops | Infra, deploy, Docker, CI/CD | Sonnet 4.6 | low |
| documentador | Docs, notes, reports | Sonnet 4.6 | low |
| especialista | Hard/critical/architecture tasks | Opus 5.5 | low |
| Explore | Broad read-only search | Sonnet 4.6 | low |
| fisico | Physics/numerical analysis | Sonnet 4.6 | low |
| general-purpose | Complex research, multi-step | Sonnet 4.6 | low |
| pesquisador | Research, long reasoning, analysis | Sonnet 4.6 | low |
| Plan | Software architect (plans) | Sonnet 4.6 | low |
| programador | Write/edit/refactor/debug code | Sonnet 4.6 | low |
| revisor | Review code, diffs, texts | Sonnet 4.6 | low |
| seguranca | Security review, audit, secrets | Sonnet 4.6 | low |
| statusline-setup | Configure status line | Haiku | low |
| testador | Tests, verification | Sonnet 4.6 | low |
| teste | Run test suites | Sonnet 4.6 | low |

## Routing by Task (Combos)

| Category | Subagent | Combo |
|----------|----------|-------|
| Code/scripts | programador | combo/programacao |
| Tests/verification | testador | combo/testes |
| Code/text review | revisor | combo/revisao |
| Research/reasoning/analysis | pesquisador | combo/pesquisa |
| Security/audit | seguranca | combo/seguranca |
| Infra/deploy/Docker/CI | devops | combo/devops |
| Hard/critical/architecture | especialista | combo/especialistas |
| Simple questions/quick reads | Main session | combo/modelos gratuitos |

## Skill Invocation Rules

- Agents invoke relevant skills before starting tasks
- User-invoked skills: `disable-model-invocation: true`
- Model-invoked skills: reachable by model or user
- See `.agents/invocation.md` for details