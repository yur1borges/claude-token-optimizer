# Test Driven Development

## What it does

Forces cycle: failing test → minimal code passes → refactor. No production code without failing test first.

## When to reach for it

- New feature
- Bugfix (regression test first)
- Refactoring (existing tests pass)

## Common questions

**What about legacy code without tests?**
Writes characterization test first.

**Integration vs unit?**
Starts unit. Integration if needed.

## It's working if

Coverage > 80% on new code. Zero commented-out tests.