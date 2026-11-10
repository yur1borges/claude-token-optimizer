---
name: systematic-debugging
description: "Use when encountering any bug, test failure, or unexpected behavior, before proposing fixes"
---

# Systematic Debugging

Systematic debugging (root cause first). For any bug/failure.

## Trigger

User-invoked. "debug this" or "systematic debugging" when you hit a bug.

## When to reach for it

- Failing tests
- Unexpected behavior
- Crash/exception
- Performance degradation

## What it does

Processo: reproduce → isolate → hypothesize → test hypothesis → fix → verify → prevent regression. Does not skip steps.

## Common questions

**Q: Does it work for production bugs?**
Yes. Same process, more care with data.

**Q: Does it need tests?**
It creates a regression test if none exists.

## It's working if

Root cause identified, minimal fix, regression test passing.