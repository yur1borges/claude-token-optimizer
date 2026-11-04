# My setup — how I organize skills, hooks and settings

Real, sanitized snapshot of my `~/.claude`. Goal: spend fewer tokens per session.

## 1. Skills: few visible, rest hidden

Every visible skill costs tokens in the listing at each session start. So:

| Where | What | Effect |
|---|---|---|
| `~/.claude/skills/` | ~37 skills I actually use (engineering + my own projects) | listed |
| `~/.claude/skills_desligadas/` | unused skills (symlinks to `~/.agents/skills/`) | not loaded |
| `~/.claude/skills_arquivadas/` | old/retired skills | not loaded |
| `skillOverrides` in settings | plugin skills set to `user-invocable-only` or `off` (128 entries) | only on explicit `/name` |
| `skillListingMaxDescChars: 150` | truncates each description | smaller listing |
| `skillListingBudgetFraction: 0.002` | caps listing share of context | hard ceiling |

Rules:
- Descriptions are one line, start with "Use when/ao ...", no examples. Long reference text goes in `references/` inside the skill, loaded only when needed.
- Backups (`SKILL.md.bak`) stay outside the skills dir.
- Public skills live in `skills/<bucket>/` of this repo; private ones (research, personal apps) are kept out (see [SCOPE](../../SCOPE.md)).

## 2. Plugins: only the terse ones on

`enabledPlugins`: only `caveman` (terse output) and `ponytail` (smallest-diff coding) are on. All other marketplaces are registered in `extraKnownMarketplaces` but `false`, so I can enable one for a task and turn it off again.

## 3. Hooks

| Hook | Purpose |
|---|---|
| `PreToolUse` (Bash) → `rtk hook claude` | [rtk](https://github.com/rtk-ai/rtk) condenses command output before it enters context |
| `PreCompact` → [`hooks/pre-compact.py`](hooks/pre-compact.py) | tells compaction what to KEEP/DROP; summary stays ~6000 chars |
| `SessionStart` | starts a watchdog for remote control (personal, not included) |

Hooks that were not worth their cost are moved to `hooks/_arquivados/` instead of deleted.

## 4. Settings that save tokens

See [`settings.example.json`](settings.example.json):
- `bashOutputMaxChars: 10000` — cap on tool output
- `autoCompactWindow: 180000` + `autoCompactEnabled` — compact before the window overflows
- `promptCacheTtl: "1h"` — keep the cache warm across pauses
- `alwaysThinkingEnabled: false` and `effortLevel: low` for every model — raise effort only when needed
- `CLAUDE_CODE_SUBAGENT_MODEL=claude-sonnet-4-6` — subagents on a cheaper model
- `includeGitInstructions: false` — drops built-in git prompt text

## 5. Global CLAUDE.md habits

- Short, imperative rules; one language rule; skills are called by the agent itself per task type.
- Subagents only when asked or for big parallel work (each starts cold = expensive).
- Subagent results are graded (good / acceptable / bad); bad ones are redone once, with a more detailed prompt.
