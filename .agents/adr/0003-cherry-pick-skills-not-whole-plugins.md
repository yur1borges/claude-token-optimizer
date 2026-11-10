# ADR 0003: Cherry-pick skills, do not install whole plugins

## Decision

When a plugin or skill pack has a few useful skills, copy only those skills into `~/.claude/skills/` (and this repo). Keep the plugin itself disabled or uninstalled. A plugin stays enabled only when what it delivers is a hook, not a skill: today that is `caveman` and `ponytail`.

## Why

A plugin is a bundle, and the bundle has costs that the useful skill alone does not have:

1. **Every skill in the bundle enters the listing.** The listing (name and description of each visible skill) is loaded at every session start and is part of the prefix of every turn. A plugin with 15 skills adds 15 descriptions even if I use 2 of them.
2. **Plugins bring hooks that run in every session.** A SessionStart hook injects text before any work. That is fine when the injected text is the whole point (caveman, ponytail). It is waste when it is only a router telling the model to look for skills first.
3. **Bundles overlap with each other.** Most packs ship their own debugging, TDD, review and design skills. Two packs means two versions of the same skill, and the model may load both and try to satisfy both.
4. **Rituals are bundled with the good parts.** Many packs pair a short, useful rule (find root cause, verify before claiming done) with long mandatory processes (brainstorm, formal plan, subagent per task). Installing the pack turns the processes on for every task.
5. **Updates change the setup silently.** A plugin update can add skills or change descriptions. A copied skill changes only when I change it.

## Example: superpowers

`obra/superpowers` is the clearest case. From it I kept:

- `systematic-debugging`: root cause before any fix. Short, used on every bug.
- `verification-before-completion`: no "done" without fresh test output. Short, used on every task.
- `test-driven-development`: kept but `user-invocable-only`, because its own description asks to run on any change.

Left out:

- **The `using-superpowers` SessionStart hook.** It injects a few KB every session and makes the model check for a skill before every reply, even trivial ones.
- **`brainstorming`, `writing-plans`, `executing-plans`.** Design doc and formal plan before code. My tasks are usually 1 to 3 files; the ritual costs more than the task. `brainstorming` and `writing-plans` are in `skills/deprecated/` and can come back with `/name`.
- **`subagent-driven-development`, worktree and code-review flows.** One subagent per task plus review multiplies tokens. My delegation rule is narrower: only large reads, web research, or when asked.

The plugin is not installed at all.

## Same pattern elsewhere

| Pack | State | What I use instead |
|---|---|---|
| `mattpocock-skills` | disabled | `systematic-debugging`, `ponytail` cover the same advice in less text |
| `andrej-karpathy-skills` | disabled | `ponytail` (simplicity rules) |
| `ecc` (everything-claude-code, about 87 skills) | disabled | the 13 skills of this repo |
| `impeccable`, `taste-skill` | plugins disabled | local copies, `user-invocable-only` |
| `context-mode`, `context-optimizer`, `setup-token-savings`, `context-engineering` | disabled | my own hooks (`filtra-testes.py`, `loop-edicao.py`, `pre-compact.py`) and RTK output condensing |
| `cloudflare`, `sentry-skills` | disabled | not used weekly |
| `caveman` | **enabled** | the value is its hook (terse mode every turn); its skill is `user-invocable-only`, its `caveman-commit` is off and its `cavecrew-*` subagents are denied in `permissions.deny` |
| `ponytail` | **enabled** | same: the hook is the value; skills are `user-invocable-only` |

## Trade-off

Copied skills do not get upstream fixes automatically. I accept that: the skills I keep are short and stable, and `find-skills` lets me check for a better version when one is needed. When a pack is truly worth it as a whole (a large new project that benefits from formal plans), the deprecated skills can be brought back for that project only.

## How to apply

Before enabling any plugin, run the three questions in [CONTRIBUTING](../../CONTRIBUTING.md) on each of its skills. Copy the ones that pass. Enable the plugin only if its value is a hook you want in every session.
