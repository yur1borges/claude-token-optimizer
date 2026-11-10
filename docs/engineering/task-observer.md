# task-observer

**Summary:** watches tasks and records my corrections, repeated patterns and methods worth keeping, so they can later become improvements to the skills.

## What it does

During the work, the skill records in a workspace log:

- corrections I make to the model's behavior;
- repeated work that could become a new skill;
- methods that worked and are worth preserving.

In a periodic review, it turns these notes into proposed changes to the skills and archives what has already been handled. It has a taxonomy to classify each observation and a protocol to decide when to show a suggestion.

## How it is triggered in my setup

**Only with `/task-observer`** (`user-invocable-only`).

## When to use

- In a long work session, when I want the hits and corrections to become improvements to the skills.
- In the skills review, to see what was noted.

## When not to use

- In ordinary day-to-day work. That is exactly why it stays hidden.

## Token cost

- In the listing: zero (hidden). The original description is over 1,000 characters and asks to be called before the first tool of **every** session.
- When called: ~33 KB (about 8,000 tokens), plus the log writes.

## Why it is in the setup and why hidden

The idea is good: the setup improves with use. But as shipped, it would run in every session and spend thousands of tokens before any work. Hidden, I turn it on in the sessions where I want to harvest learning.

## How to tell it is working

- The observation log gains entries with the context and the suggestion.
- In the review, the entries become concrete changes to skills.
