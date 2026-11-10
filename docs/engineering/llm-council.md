# llm-council (disabled)

**Status:** out of the setup. The code is in [skills/deprecated/llm-council](../../skills/deprecated/llm-council/SKILL.md) and on my PC it sits in `~/.claude/skills_desligadas/`.

## What it did

Five "advisors" with different points of view debate a decision and a judge consolidates.

## Why it left

Each decision cost about five times a normal answer. For the decisions I make, a direct recommendation from the model with the pros and cons is enough.

## How to bring it back

Move the folder back to `~/.claude/skills/` and remove the `"llm-council": "off"` entry from `skillOverrides`.
