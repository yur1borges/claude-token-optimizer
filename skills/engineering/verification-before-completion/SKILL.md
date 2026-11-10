---
name: verification-before-completion
description: "Use when about to claim work is complete, fixed, or passing, before committing or creating PRs - requires running verification commands and confirming output before making any success claims; evidence before assertions always"
---

# Verification Before Completion

Evidence before claims. "complete", "fixed", "passing" require proof.

## Trigger

Auto-invoked when the agent says "done", "fixed", "complete", "passing".

## When to reach for it

- Always. It is a mandatory guardrail.

## What it does

Blocks claims without evidence: test output, build log, screenshot, diff. Forces: "tests pass: [output]", not "tests pass".

## Common questions

**Q: For non-code tasks?**
Yes. Evidence = relevant output (file created, command ran, etc.)

**Q: Can it be turned off?**
No. Hard rule in CLAUDE.md.

## It's working if

Zero claims without evidence in the history.