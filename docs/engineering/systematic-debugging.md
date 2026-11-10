# systematic-debugging

**Summary:** before fixing any bug, find the root cause. No "try something and see if it works".

## What it does

The skill enforces one core rule, called the "iron law": **no fix without investigating the root cause first**. Fixing the symptom counts as a failure, even on a simple bug.

The work follows four phases, none skipped:

1. **Root cause.** Read the whole error message, reproduce the problem reliably, check what changed recently (git diff, dependencies, configuration) and trace where the wrong value comes from, going back up the call stack to the origin.
2. **Pattern.** Look in the codebase for a similar case that works and compare it with the one that breaks. The difference is often the cause.
3. **Hypothesis.** Write a single hypothesis ("X causes the error because Y") and test it with the smallest possible change. One variable at a time.
4. **Fix.** Create a test that reproduces the bug, fix at the source (not where the error shows up) and confirm the test passes and nothing else broke.

It also carries a list of warning signs that send you back to phase 1, such as "I will just try this quickly" or the third failed fix in a row. From the third failed attempt on, the skill says to question the architecture instead of insisting.

The skill's folder has references that load only when a phase asks for them: root cause tracing, defense in depth, condition-based waiting (for timing-flaky tests) and a script to find which test pollutes the state of the others.

## How it is triggered in my setup

**Automatic.** The global CLAUDE.md says to call it on its own for any bug, failing test or unexpected behavior, before proposing a fix. Subagents get the same rule in `regras_agentes.md`.

## When to use

- Failing test, exception, crash.
- Strange numerical result in a calculation (energy that does not converge, shifted spectrum).
- Behavior that happens "sometimes".
- Whenever a fix attempt has already failed.

## When not to use

- An obvious typo, with the line and cause already in the message. Even then phase 1 is quick, so in practice the skill runs and finishes in seconds.

## Token cost

- In the listing: a one-line description.
- When called: ~2.2 KB of text (about 550 tokens). The references enter only if a phase needs them.

## Why it is in the setup

Bugs are where the most tokens are wasted. Each wrong attempt costs an edit, a test run and a log read, and the context fills up with dead attempts. Requiring the root cause first swaps several cheap, wrong rounds for one correct investigation.

**Discarded alternatives:**
- `mattpocock-skills:diagnosing-bugs`: same idea, longer text and more ceremony. The whole plugin was left disabled.
- No skill at all: the model tends to propose a fix in its first answer, before reproducing the error.

## How to tell it is working

- The answer starts by reproducing the error and showing the cause, with file and line, before any edit.
- The fix comes with a test that failed before and passes after.
- Three fixes in a row at the same spot do not appear.
