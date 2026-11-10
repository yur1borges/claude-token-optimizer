# teste-leigo

**Summary:** tests my desktop apps as a lay, impatient user would: random clicks, wrong inputs, double clicks, resized window. Finds what breaks.

## What it does

It is a skill **written by me**. It uses a "monkey" (`macaco.py`) that drives the real app without knowing the code:

- clicks random places and buttons out of order;
- types text into a number field, empty fields, huge values, special characters;
- double-clicks where a single click is expected, clicks again before the operation finishes;
- resizes, maximizes and minimizes the window in the middle of an operation.

Each app has an adapter (`adaptadores.py` plus one per app) that says where the windows are and which screens exist. There are versions for web apps (`macaco_web.py`) and Electron (`macaco_electron.js`). The skill has safety rules (do not delete real data, work on a copy) and takes screenshots of the failures.

## How it is triggered in my setup

**Automatic** when I ask to test one of my desktop apps. I also use it before delivering a new version.

## When to use

- Before delivering a version of an app with a graphical interface.
- After changing forms, dialogs or screen flow.

## When not to use

- To test calculation logic: unit tests are the right tool there.
- On an app without an adapter, until one is written.

## Token cost

- In the listing: one line.
- When called: ~2.2 KB (about 550 tokens). The monkey runs as a script and returns only the failure report, not the whole log.

## Why it is in the setup

No public skill tests desktop apps this way. Unit tests verify the logic; the monkey catches what only shows up with a human poking at it: a freeze on double click, an error with an empty field, a layout that breaks on resize. Finding this beforehand saves a cycle of "the user found it, I reopen the session, the model rereads everything".

## How to tell it is working

- A report comes out with each failure, the step that caused it and the screenshot.
- The failures found become tests or fixes.
