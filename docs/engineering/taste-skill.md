# taste-skill

**Summary:** art direction for websites, against the generic template look. Based on a study of 247 sites from design galleries.

## What it does

taste-skill treats the page as an art direction project, not an assembly of components. The flow has ten steps:

1. Read the request and the existing project.
2. Write the argument: what the page needs to convince people of.
3. Choose a visual direction from a library of researched directions (idea, composition, typography, palette, photography, section structure).
4. Find the page's central idea.
5. Write the copy.
6. Build.
7. Pass a quality gate with strict rules against the generic look.
8. Look at the rendered result.
9. Adjust the motion.
10. Report what was done.

## How it is triggered in my setup

**Only with `/taste-skill`** (`user-invocable-only`). The `taste-skill@taste-skill` plugin is **disabled**; only the local copy remains.

## When to use

- A presentation page, portfolio or project site where visual identity matters.
- When the ui-ux-pro-max result came out correct but without personality.

## When not to use

- Working interface (form, table, dashboard): there clarity is worth more than personality.
- Desktop app.

## Token cost

- In the listing: zero (hidden).
- When called: ~34 KB (about 8,500 tokens), the longest in the setup, plus the directions library. This is the main reason it stays hidden.

## Why it is in the setup and why hidden

It gives a result the others do not: a page with its own character. But it is expensive and has strong opinions that clash with those of ui-ux-pro-max. It is kept for when that is exactly the goal.

## How to tell it is working

- The answer starts with the argument and the chosen direction, not with code.
- The result does not look like a generic landing page template.
