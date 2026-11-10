# impeccable

**Summary:** fine polish for web interfaces: hierarchy, spacing, color, motion, interface text. It has several modes (create, critique, audit, polish, simplify, animate).

## What it does

It is a frontend design skill with several working modes, each with its own goal:

- **create or redesign** a screen;
- **critique** or **audit**: lists what is weak and why;
- **polish**: the fine details of spacing, alignment and typography;
- **simplify**: remove elements that clutter;
- **harden**: empty states, errors, loading, long texts;
- **animate**: purposeful motion, respecting users who ask for less animation.

It also documents design systems (`DESIGN.md`, tokens) so the next session follows the same standard. The references and scripts in the folder load only in the mode that needs them.

## How it is triggered in my setup

**Only with `/impeccable`** (`user-invocable-only`). The `impeccable@impeccable` plugin is **disabled**: only the copy in `~/.claude/skills/` remains, to avoid two versions of the same skill.

## When to use

- A web page that many people will see and that needs finish.
- Reviewing a finished interface that "looks amateur" and finding out why.
- Closing the edge states (empty, error, loading) before delivering.

## When not to use

- Everyday desktop app interface: ui-ux-pro-max covers it.
- Anything without an interface.

## Token cost

- In the listing: zero (hidden). The original description is over 600 characters; visible, it would be one of the most expensive in the listing.
- When called: ~12 KB (about 3,000 tokens), plus the references of the chosen mode.

## Why it is in the setup and why hidden

For web page finish it goes further than ui-ux-pro-max. But otherwise the two overlap, and having two auto-called design skills produces conflicting instructions. Hidden, it costs nothing until I call it.

## How to tell it is working

- The answer says which mode it used and lists what changed and why.
- Empty, error and loading states show up handled.
