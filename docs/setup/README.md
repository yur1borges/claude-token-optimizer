# My Claude Code setup (state as of November 2026)

A real snapshot, without personal data, of my `~/.claude`. The goal of everything here is to spend fewer tokens per session without losing quality. Each item says **what it is**, **why it is here** and, when it was removed, **why it left**.

Machine: Windows 11 laptop, 7.6 GB of RAM, VS Code + Claude Code. This weighs on several choices (little RAM, one heavy process at a time).

## Overview: where the cost comes from

A session pays tokens in four places. Each layer of the setup attacks one of them:

| Cost | What generates it | What I use against it |
|---|---|---|
| Fixed prefix (every turn) | list of skills, plugins, MCPs, CLAUDE.md | few visible skills, plugins off, no global MCP |
| Tool input | output of commands, tests, files read | rtk, `filtra-testes.py`, `bashOutputMaxChars`, reading by range |
| Model output | text of the answers, thinking | caveman, ponytail, `effortLevel: low`, thinking off |
| Repetition | rereads, error loops, stale context | 1 h cache, `loop-edicao.py`, guided compaction, `/clear` per topic |

## 1. Skills: few visible, the rest hidden

Every visible skill goes into the listing at the start of each session. Therefore:

| Where | What | Effect |
|---|---|---|
| `~/.claude/skills/` | ~24 skills I actually use | listed |
| `~/.claude/skills_desligadas/` | 26 skills out of use (Maestri, reverse engineering, brainstorming, llm-council, writing-plans etc.) | not loaded; I bring them back with a `mv` |
| `skillOverrides` | plugin skills set to `user-invocable-only` or `off` (~55 entries) | only with an explicit `/name` |
| `skillListingMaxDescChars: 150` | truncates each description | smaller listing |
| `skillListingBudgetFraction: 0.002` | cap of the listing in the context | hard limit |

Rules for skills:
- One-line description, starting with "Use when ...", no examples. Long text goes to `references/` inside the skill and only loads when needed.
- `user-invocable-only` when the skill is useful but should not fire on its own (caveman, ponytail, graphify, humanizer, TDD). `off` when I no longer use it.
- Disabling is moving to `skills_desligadas/`, never deleting. It comes back easily and the work is not lost.
- Personal skills (TriboDEM, DA, XRD, Lattes, my apps) do not go in this repo; see [SCOPE](../../SCOPE.md).

Which ones the model calls on its own, by type of task (rule in the global CLAUDE.md):

| Task | Skill |
|---|---|
| bug | systematic-debugging |
| review | code-review (native) |
| before saying "done" | verification-before-completion |
| interface | ui-ux-pro-max |
| page/Artifact | artifact-design (native) |
| broad research | deep-research (native) |
| test a desktop app as a lay user | teste-leigo |

**Why they left:**
- `brainstorming`, `writing-plans`, `llm-council`: long ritual before every task. They spent more tokens than they saved in day-to-day tasks. A short plan goes in `~/.claude/planos/` only if there are more than 3 steps.
- Maestri (7 skills) and `orca-cli`: external orchestration I stopped using. Archived, not deleted.
- Reverse engineering skills: rare use; they stay off and I turn them on when needed.
- `impeccable` and `taste-skill` as a plugin: duplicated the versions in `~/.claude/skills/`. The local copy stayed in `user-invocable-only`, and `ui-ux-pro-max` is the default for interfaces (just one, so as not to load three design guides).

## 2. Plugins: only the ones that shorten the output

On:
- **caveman**: terse answers (fragments, no ceremony). Cuts the output, which is the most expensive token. I use the `ultracave` level.
- **ponytail**: "lazy senior dev", the smallest diff that solves it. Less code written means less output and less review.

Both run by `SessionStart` hook, so their skills are `user-invocable-only` (already active, they do not need to appear in the listing).

Registered in `extraKnownMarketplaces` but `false` (I turn one on for a task and off afterwards):

| Plugin | Why it is off |
|---|---|
| `ecc` (everything-claude-code) | heavy: ~87 skills and the GateGuard, which forced extra text before acting |
| `context-mode` | large start-up text, an MCP server along with it and a Bash compressor that duplicated rtk |
| `context-optimizer` (cco) | redundant with rtk + guided compaction |
| `mattpocock-skills`, `andrej-karpathy-skills` | redundant with ponytail/caveman; they took about 5 to 10 thousand fixed tokens (estimate, not measured) |
| `sentry-skills`, `cloudflare` | only useful for those services, which I do not use day to day |
| `impeccable`, `taste-skill` | duplicated the local copies (see section 1) |
| `setup-token-savings`, `context-engineering` | tested; what was useful in them is already in my settings and hooks |

I also deny the `caveman:cavecrew-*` subagents (Haiku) in `permissions.deny`: they were called without my asking and the return was weak for my kind of work. I use my own `triage` instead (section 5).

## 3. Hooks

| Hook | Event | Why |
|---|---|---|
| `rtk hook claude` (via `filtra-testes.py`) | `PreToolUse` Bash | [rtk](https://github.com/rtk-ai/rtk) condenses command output before it enters the context |
| [`filtra-testes.py`](hooks/filtra-testes.py) | `PreToolUse` Bash | test command: runs once, saves the log and returns only failures (traceback with `-A 15`) + summary. If it passed, returns only the tail |
| [`loop-edicao.py`](hooks/loop-edicao.py) | `PostToolUse` Edit/Write/Bash/PowerShell | 5 edits to the same file without running a test: warns the agent. Avoids the "edit, fail, edit" loop that burns tokens |
| [`pre-compact.py`](hooks/pre-compact.py) | `PreCompact` | tells the compaction what to KEEP (literal requests, decisions, files, numbers) and what to DISCARD (logs, dead attempts). Summary up to ~800 words. Also writes `HANDOFF.md` in the project so a new session can resume by reading only it |
| `troca-assunto.py` (personal, not included) | `UserPromptSubmit` + `SessionStart` | detects a project switch in the prompt (TriboDEM, DA etc.), suggests `/clear` and, after the `/clear`, reruns the request by itself. One project's context does not contaminate the other |
| Remote Control watchdog (personal) | `SessionStart` | reconnects Remote Control when the internet returns |
| Orca and Codenotch (personal) | various | desktop status and notifications; they do not affect tokens |

**Why they left** (they stay in `hooks/_arquivados/`, not deleted):
- `laya-gate.mjs`: thinking filter. It loaded an ONNX model on every prompt and cost ~35 tokens per turn; with thinking off and effort `low`, it was not worth it.
- `context-mode-cache-heal.mjs`: only existed because of the context-mode plugin, which I turned off.
- `autoclear.ps1`: cleared on its own; replaced by `troca-assunto.py`, which asks first and does not lose the request.
- `caveman-statusline.ps1`, `start_orchestrator.ps1`, `erros_softwares.py`: replaced by Orca's statusline or unused.

## 4. Settings that save

See [`settings.example.json`](settings.example.json).

| Setting | Why |
|---|---|
| `model: opus` + `effortLevel: low` on all models | strong model, short reasoning by default; I raise the effort only when the task asks for it |
| `alwaysThinkingEnabled: false`, `showThinkingSummaries: false` | thinking is paid output; off by default |
| `promptCacheTtl: "1h"` | cache survives long pauses; the fixed prefix is billed cheaply |
| `autoCompactWindow: 200000` + `precomputeCompactionEnabled` | compacts before overflowing, with the summary already precomputed |
| `bashOutputMaxChars: 10000` | cap for tool output |
| `includeGitInstructions: false` | removes the git text embedded in the prompt |
| `promptSuggestionEnabled`, `awaySummaryEnabled`, `autoMemoryEnabled: false` | each one generates extra calls or context that I do not use |
| `disableClaudeAiConnectors`, `syncClaudeAiPlugins: false` | claude.ai connectors become MCPs in the prefix; turned off |
| `CLAUDE_CODE_GOAL_CHECKIN_MINUTES=0` | no automatic periodic check-in |

**Why I do not use** a global `CLAUDE_CODE_SUBAGENT_MODEL` (I used to): each agent now declares its own `model` in the frontmatter (section 5), which is more precise.

## 5. Subagents

Rule: delegate only large reads (more than ~5 files or large logs), web research, or when I ask. Each subagent starts from zero and rereads context, so a small task is done directly.

| Agent | Model | What for |
|---|---|---|
| `triage` ([example](agents/triage.md)) | Haiku | cheap lookup: file, symbol, config, error. Answer in up to 120 tokens |
| `programador`, `design`, `documentador`, `teste` | Sonnet, effort low, `maxTurns: 50` | implement, UI, docs, run tests |
| `revisor` ([example](agents/revisor.md)) | Sonnet | reviews a diff without editing |
| `pesquisador`, `fisico` | Sonnet + WebSearch | literature and numerical analysis |
| `Explore` | Sonnet | read-only sweep |

- All read `~/.claude/regras_agentes.md` (common rules: pt-BR, do not delete data, long process in background, deliver with evidence). It lives in a single file so as not to repeat it in each agent.
- Narrow question with a fixed output format.
- Return graded: BOM, ACEITÁVEL or RUIM. RUIM goes back once with a more detailed prompt; if it is still bad, I do it myself.

## 6. Habits from the global CLAUDE.md

- Short, imperative rules: language, autonomy, git, tokens, skills, subagents.
- Read a file by range or grep, never whole unless needed. Large output goes to a log on disk and I read it with `grep -A 15 -E 'ERROR|FAIL|Traceback'` + `head`.
- Changed topic or came back after more than 1 h: `/clear` (with `/rename`). `/compact` only at the end of a phase.
- **Stable prefix**: do not change model, MCPs, skills or CLAUDE.md mid-session. Any change invalidates the cache and the whole prefix is billed again.
- Commit and push once a month (less noise and fewer turns spent on git).

## 7. MCPs

No global MCP. The claude.ai connectors are off and the only MCP lives in the scope of one specific project. **Why:** each MCP puts the description of all its tools in the prefix of every session. Browser tools and the like come in as "deferred" (only the name appears) and I load them with `ToolSearch` when needed.

## 8. Related projects

| Project | Idea | Status |
|---|---|---|
| [JuliusBrussee/caveman](https://github.com/JuliusBrussee/caveman) | terse voice | in use |
| [DietrichGebert/ponytail](https://github.com/DietrichGebert/ponytail) | smallest diff | in use |
| [rtk-ai/rtk](https://github.com/rtk-ai/rtk) | condenses command output | in use (v1.1.0) |
| [Kulaxyz/token-diet](https://github.com/Kulaxyz/token-diet) | always-on skill for short answers | overlaps caveman + ponytail; not installed |
| [nidhinjs/prompt-master](https://github.com/nidhinjs/prompt-master) | rewrites prompts to get it right the first time | on-demand candidate |
| [foryourhealth111-pixel/Vibe-Skills](https://github.com/foryourhealth111-pixel/Vibe-Skills) | routes among ~195 skills | heavy; my solution is to have fewer visible skills |
