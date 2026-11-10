---
name: llm-council
description: "Use when asked for advice or a decision ('council this'): 5 advisors debate."
---

# LLM Council

Council of 5 advisors with different perspectives. For hard decisions.

## Trigger

User-invoked. "council this" or "llm council".

## When to reach for it

- Architectural decisions
- Complex trade-offs
- Controversial code review
- Tech stack choice

## What it does

Invokes 5 personas: Pragmatist, Architect, Security, Performance, User Advocate. Each gives an opinion. Final synthesis with a recommendation.

## Common questions

**Q: Does it take long?**
~30-60s. Worth it for irreversible decisions.

**Q: Different models?**
All use the same model, different prompts.

## It's working if

Decision documented with each advisor's rationale.