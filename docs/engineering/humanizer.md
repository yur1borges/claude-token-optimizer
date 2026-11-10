# humanizer

**Summary:** removes AI writing patterns from a text so it sounds written by a person, without changing the content.

## What it does

The skill starts by explaining why AI text sounds the way it does, then attacks the patterns one by one, for example:

- **staging instead of saying:** sentences that announce what is coming ("Let's dive into...") instead of saying it;
- excessive hesitation and hedging;
- lists of three items out of habit, sentences all the same length;
- typical AI vocabulary and conclusions that repeat what was already said.

It returns the text rewritten in the requested voice. The references by pattern type load only when I need them.

## How it is triggered in my setup

**Only with `/humanizer`** (`user-invocable-only`).

## When to use

- Email, report, post or academic text that goes to other people.
- Text that is already correct but "looks like AI".

## When not to use

- Code, technical comments, terminal replies.
- Text where technical accuracy matters more than style, without my review afterwards.

## Token cost

- In the listing: zero (hidden).
- When called: ~5.1 KB (about 1,300 tokens).

## Why it is in the setup and why hidden

I use it often on text meant for others, but never on code. Visible, it would compete with caveman (which wants short answers) on every reply. Hidden, it costs nothing until I need it.

## How to tell it is working

- The rewritten text says the same thing, more directly, without the generic openings and closings.
