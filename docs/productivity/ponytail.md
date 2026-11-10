# ponytail

**Summary:** "lazy senior dev": the smallest change that solves the whole task. Less code written means less output, less review and fewer bugs.

## What it does

Before writing code, the skill goes through a ladder of questions and stops at the first rung that solves it:

1. Does it need to exist? Any feature, option or flexibility nobody asked for stays out.
2. Does it already exist in this project? Use the helper, component or pattern that is already there.
3. Does the standard library or the platform solve it?
4. Does an already installed dependency solve it? Never add a dependency for a few lines.
5. Does it fit in one line that is understood at a glance?
6. Only then, the minimum code that works.

It is lazy about the solution, **never about the change**: it finishes everything the task requires, including the callers of the function, the tests and the test data the change affects. For bug fixes, it says to find every place that calls the function and fix it once, at the source. Non-trivial new logic leaves a short test.

It never cuts: validation of input from external sources, error handling that prevents data loss, security, accessibility.

## How it is triggered in my setup

**Always on, at the `full` level.** The `ponytail@ponytail` plugin injects the mode through a hook at the start of each session. The skill is `user-invocable-only`, as is `ponytail-audit` (a whole-repository audit, which I call when I want it).

## When to use

- Every coding task.

## When not to use

- When I explicitly ask for something complete or extensible; the explicit request wins.

## Token cost

- Fixed cost: the mode text injected by the hook each session, which stays in the cache.
- Savings: smaller diffs, fewer files created, fewer review rounds. I have not measured it in numbers.

## Why it is in the setup

**Discarded alternatives:**
- `mattpocock-skills` and `andrej-karpathy-skills`: gave similar advice (simplicity, do not abstract early) in much more text, and added thousands of fixed tokens per session. Both plugins were turned off.
- `ecc` (everything-claude-code): had its own quality rules, but the whole package was too heavy.

Together with caveman, it covers both sides of the output: caveman shortens the text and ponytail shortens the code.

## How to tell it is working

- The diff is smaller than the obvious solution and carries no "for later" code.
- At the end of the reply, one or two lines say what was skipped and what risk remains.
