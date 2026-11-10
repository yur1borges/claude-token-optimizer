# verification-before-completion

**Summary:** forbidden to say "done", "fixed" or "passed" without having run the verification now and shown the output.

## What it does

The core rule: **no completion claim without fresh verification evidence**. "Fresh" means run in this message; a test that passed half an hour ago, before the last edit, does not count.

Before any success statement, the skill sends you through a gate:

1. Which command proves what I am about to claim?
2. Run that command in full, now.
3. Read the whole output and the exit code.
4. Does the output confirm the claim? If not, state the real status, with the evidence.
5. Only then make the claim.

It lists the common failures ("it should work now", "the linter passed, so it compiles", trusting a subagent's report without checking) and the excuses the model usually gives to skip verification, each already with its answer.

## How it is triggered in my setup

**Automatic.** The global CLAUDE.md says to call it before claiming something is complete, fixed or passing, and before a commit or PR.

## When to use

- Before closing any code task.
- Before commit and push.
- When receiving a subagent's result: its "I am done" also needs evidence.
- In non-code tasks: the evidence is the file created, the process running, the number measured.

## When not to use

- A question that does not end with a "it works" claim (explanation, research).

## Token cost

- In the listing: one line.
- When called: ~3.6 KB (about 900 tokens). No extra references.
- The real cost is one extra test run per task. With the `filtra-testes.py` hook, that run returns only the summary or the failures, so it is cheap.

## Why it is in the setup

A false "done" is the most expensive error in my workflow. I find the problem later, open another session, the model rereads everything from scratch and redoes it. A verification of a few seconds beforehand avoids a whole session of rework.

**Discarded alternatives:** just writing "always test" in CLAUDE.md. It works poorly, because a loose rule does not list the excuses the model uses to skip verification; the skill lists them and answers each one.

## How to tell it is working

- Every final code answer carries the command that was run and the output (for example "34 passed").
- When something fails, the answer says it failed and shows the output, instead of softening it.
