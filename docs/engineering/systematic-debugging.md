# Systematic Debugging

## What it does

Process: reproduce → isolate → hypothesize → test hypothesis → fix → verify → prevent regression. Does not skip steps.

## When to reach for it

- Failing tests
- Unexpected behavior
- Crash/exception
- Performance degradation

## Common questions

**Does it work for production bugs?**
Yes. Same process, more care with data.

**Does it need tests?**
Creates regression test if none exists.

## It's working if

Root cause identified, minimal fix, regression test passing.