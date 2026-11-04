# Writing Plans

## What it does

Generates plan: objective, ordered steps, affected files, risks, tests, rollback. Format: markdown with checkboxes.

## When to reach for it

- Features > 3 files
- Cross-cutting refactoring
- Migration
- Any task with dependencies

## Common questions

**Does the model follow the plan?**
Should. Deviation = new plan.

**Too much detail?**
Level: file + function. Not line.

## It's working if

Plan exists before code. Execution follows plan or documents deviation.