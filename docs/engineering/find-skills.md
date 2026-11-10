# find-skills

**Summary:** when a skill is missing for a task, it searches the public catalog, checks quality and shows the options before installing.

## What it does

It uses the skills CLI and the ranking of most-used skills to find candidates. The flow:

1. Understand what I need.
2. Check the ranking first (the most used are usually the most trustworthy).
3. Search by the task's keyword.
4. **Check quality before recommending:** who maintains it, when it was last updated, whether the description matches the content.
5. Show the options with the reasoning.
6. Install only if I accept.

## How it is triggered in my setup

**Automatic** when I ask how to do something for which a skill may exist.

## When to use

- A new, recurring task that may already have a ready-made skill.
- Before writing a skill from scratch.

## When not to use

- A one-off task: solving it directly is cheaper than installing a skill.

## Token cost

- In the listing: one line.
- When called: ~5.2 KB (about 1,300 tokens).

## Why it is in the setup

It is what lets me keep the list small. Instead of installing large packages "just in case" (`ecc` alone brought ~87 skills), I look for the right skill at the moment it is needed. Each candidate still goes through the [CONTRIBUTING](../../CONTRIBUTING.md) filter: weekly use, no overlap with another skill, and savings greater than the cost.

## How to tell it is working

- The answer shows 1 to 3 options with source and reason, and installs nothing until I accept.
