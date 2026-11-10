# brainstorming (disabled)

**Status:** out of the setup. The code is in [skills/deprecated/brainstorming](../../skills/deprecated/brainstorming/SKILL.md) and on my PC it sits in `~/.claude/skills_desligadas/`.

## What it did

A mandatory ideas session before any creative work or new feature, with questions, alternatives and a design document before the code.

## Why it left

Its description said "use before any creative work", so it fired on almost every task. For changes touching 1 to 3 files, the ideas conversation cost more tokens than the task itself.

## How to bring it back

Move the folder back to `~/.claude/skills/` and remove the `"brainstorming": "off"` entry from `skillOverrides`.
