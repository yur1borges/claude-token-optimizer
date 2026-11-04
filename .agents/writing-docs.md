# Writing Docs

When you add, rename, or change the behaviour of a skill in engineering/ or productivity/, create or re-sync its docs page following this guide.

A finished page carries four sections in order:

1. **What it does**
2. **When to reach for it**
3. **Common questions**
4. **It's working if**

## Template

```markdown
# Skill Name

## What it does

[One paragraph. What the skill actually does when invoked.]

## When to reach for it

- [Use case 1]
- [Use case 2]

## Common questions

**[Question?]**
[Answer.]

## It's working if

[Observable success criterion.]
```

## Where to hunt for questions

- User questions in issues/PRs
- Confusion in code review
- "How do I..." in conversations
- Edge cases the skill handles

## Archived skills

If a promoted skill is removed outright, its page stays, marked archived at the top:

```markdown
> **Archived.** This skill is no longer promoted. Kept for reference.
```