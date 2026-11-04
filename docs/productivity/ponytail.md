# Ponytail

## What it does

Asks: "Need to exist?" → use existing → stdlib → dependency → one-liner → minimum that works. Delete > add. Finish callers, tests, fixtures.

## When to reach for it

- Any code task
- Want minimal, correct solution
- Avoid over-engineering

## Common questions

**Does it skip validation?**
Never. Validation at trust boundaries is mandatory.

**Works for new features?**
Yes. Smallest version that does core job.

## It's working if

Diff smaller than obvious alternative. Zero "for later" code. Callers/tests/fixtures ok.