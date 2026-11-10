---
name: task-observer
description: "Monitors task execution for skill improvement opportunities: logs patterns, user corrections and methodology worth preserving to the workspace, turns them into skill updates in a weekly review, and flags repeating work as new skills. Use during ANY multi-step task, agentic workflow, or work session."
---

# Task Observer

Monitors multi-step task execution to improve skills.

## Trigger

Auto-invoked on tasks with > 3 steps. Or user-invoked: "observe this task".

## When to reach for it

- Complex workflows
- Debugging skills
- Process optimization

## What it does

Records: steps, tools used, time, errors, decisions. Generates a report at the end with patterns and skill suggestions.

## Common questions

**Q: Does it save sensitive data?**
No. Only execution metadata.

**Q: Where is the report?**
`.claude/task-observer/` in the project.

## It's working if

Report generated with > 3 actionable insights.