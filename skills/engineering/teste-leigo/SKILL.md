---
name: teste-leigo
description: "Use to test Yuri's desktop apps as a layperson and impatient user (random clicks, wrong inputs, double click, resizing) and find breakages."
---

# Teste Leigo

Test as a layperson/impatient user. For desktop apps.

## Trigger

User-invoked. "teste leigo" or "layman test" before shipping.

## When to reach for it

- Desktop apps (Tauri, Electron, WPF)
- Critical user flows
- Before a release

## What it does

Simulates a user who: does not read instructions, clicks the wrong thing, is impatient, does not know shortcuts. Finds UX bugs that devs do not see.

## Common questions

**Q: Does it replace automated tests?**
No. It complements them. It catches UX, not logic bugs.

**Q: How long does it take?**
15-30 min per main flow.

## It's working if

Finds > 3 UX issues per tested flow.