# test-driven-development

**Summary:** write the test before the code, watch the test fail, write the minimum to pass, then clean up.

## What it does

The core rule: **no production code without a failing test first**. If the code was written before the test, the skill says to delete it and start over from the test.

The cycle has three steps, with a check at each:

1. **Red.** Write a small test for a single behavior, with a clear name. Run it and **watch it fail for the right reason** (the function does not exist or returns the wrong value, not a typo in the test).
2. **Green.** Write the simplest code that makes the test pass. No extra options or features. Run it and watch it pass, along with the other tests.
3. **Refactor.** Remove duplication and improve names, keeping everything green.

The skill also teaches what a good test looks like (one behavior, a descriptive name, real code instead of a mock whenever possible) and answers the usual excuses ("too simple to test", "I will test later"). The `writing-good-tests.md` reference loads only when I need it.

## How it is triggered in my setup

**Only with `/test-driven-development`** (`user-invocable-only` in `skillOverrides`). The model does not see it in the listing and does not call it on its own.

## When to use

- New logic with a clear rule: parser, unit conversion, calculation, validation.
- A bug that needs a regression test.
- Refactoring code without tests: characterization test first, then change.

## When not to use

- Visual tweak in an interface, text, configuration.
- A throwaway one-off script.
- A one-line edit in code already covered by a test.

## Token cost

- In the listing: zero (hidden).
- When called: ~9.6 KB (about 2,400 tokens). It is one of the longest, another reason not to fire on its own.

## Why it is in the setup and why hidden

TDD avoids the worst kind of rework: code that "looks right" and breaks later. But its original description says "use when implementing any feature or fix". If it stayed visible, the model would load 2,400 tokens and write tests even to change a button color. Hidden, I turn it on in the cases where it is worth it.

ponytail already covers the small case: non-trivial new logic leaves a short test or a self-check, without the full ritual.

## How to tell it is working

- The first edit of the task is a test file.
- The answer shows the test failing and then passing.
- The new code has nothing the test does not require.
