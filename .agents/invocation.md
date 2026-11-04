# Invocation Rules

Every SKILL.md is either:

- **User-invoked**: `disable-model-invocation: true` plus `policy.allow_implicit_invocation: false` in agents/openai.yaml. Reachable only by human.
- **Model-invoked**: Model- or user-reachable.

[ask-matt](./skills/engineering/ask-matt/SKILL.md) is the router that maps every user-reachable skill and how they relate. Whenever you add, rename, remove, or change how a user-reachable skill fits the flows, re-read ask-matt's SKILL.md and update it so the map stays accurate.