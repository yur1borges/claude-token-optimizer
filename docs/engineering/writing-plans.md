# writing-plans (disabled)

**Status:** out of the setup. The code is in [skills/deprecated/writing-plans](../../skills/deprecated/writing-plans/SKILL.md) and on my PC it sits in `~/.claude/skills_desligadas/`.

## What it did

A formal, step-by-step implementation plan, written to a file before touching the code.

## Why it left

It generated long plans for short tasks. I replaced it with a cheaper rule: a short plan in `~/.claude/planos/` only when the task has more than 3 steps.

## How to bring it back

Move the folder back to `~/.claude/skills/` and remove the `"writing-plans": "off"` entry from `skillOverrides`.
