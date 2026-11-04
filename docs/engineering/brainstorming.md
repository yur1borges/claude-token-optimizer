# Brainstorming

## What it does

Forces divergent thinking before convergent. Produces a structured list of options with trade-offs so you pick deliberately instead of drifting into the first idea.

## When to reach for it

- New feature design
- Component architecture decisions
- API design choices
- Naming things
- Any decision that will live in code for months

## Common questions

**Do I need this for small decisions?**
No. Use for decisions that will live in code for months.

**Can the model invoke it?**
No. `disable-model-invocation: true`. Only you can trigger it.

## It's working if

You have 3+ distinct options written down with pros/cons before writing code.