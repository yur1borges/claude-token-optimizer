---
name: ponytail
description: "Lazy senior dev mode: the smallest change that fully solves the task."
---

# Ponytail

Lazy senior developer. Least code that solves the whole problem.

## Trigger

`/ponytail` or `/ponytail full`. Persists until "stop ponytail".

## When to reach for it

- Any coding task
- Want a minimal, correct solution
- Avoids over-engineering

## What it does

Asks: "Does it need to exist?" → use what exists → stdlib → dependency → one-liner → minimum that works. Delete > add. Finish callers, tests, fixtures.

## Sub-skills

- `ponytail-audit` : code audit
- `ponytail-debt` : technical debt
- `ponytail-gain` : gains (what it saved)
- `ponytail-help` : ponytail help
- `ponytail-review` : lazy senior review

## Levels

| Level | Behavior |
|-------|----------|
| lite | Basic rules |
| full | Default. Full rules |
| ultra | Extreme. Nothing that was not asked for |

## Common questions

**Q: Does it skip validation?**
Never. Validation at trust boundaries is mandatory.

**Q: Does it work for new features?**
Yes. Smallest version that does the core job.

## It's working if

Diff smaller than the obvious alternative. Zero "for later" code. Callers/tests/fixtures ok.