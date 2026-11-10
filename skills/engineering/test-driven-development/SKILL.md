---
name: test-driven-development
description: "Use when implementing any feature or bugfix, before writing implementation code"
---

# Test Driven Development

Mandatory TDD. Red → Green → Refactor for features, bugfixes, refactoring.

## Trigger

User-invoked. "tdd this" before writing production code.

## When to reach for it

- New feature
- Bugfix (regression test first)
- Refactoring (existing tests pass)

## What it does

Forces the cycle: test fails → minimal code passes → refactor. Does not write production code without a failing test first.

## Common questions

**Q: What about legacy code without tests?**
It writes a characterization test first.

**Q: Integration vs unit?**
Starts with unit. Integration if needed.

## It's working if

Coverage > 80% on new code. Zero commented-out tests.