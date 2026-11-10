---
name: writing-plans
description: "Use when you have a spec or requirements for a multi-step task, before touching code"
---

# Writing Plans

Implementation plans for multi-step tasks.

## Trigger

User-invoked. "plan this" or "write plan" before a complex task.

## When to reach for it

- Features touching > 3 files
- Cross-cutting refactoring
- Migration
- Any task with dependencies

## What it does

Generates a plan: goal, ordered steps, affected files, risks, tests, rollback. Format: markdown with checkboxes.

## Common questions

**Q: Does the model follow the plan?**
It should. Deviation = new plan.

**Q: Too much detail?**
Level: file + function. Not line.

## It's working if

The plan exists before the code. Execution follows the plan or documents the deviation.