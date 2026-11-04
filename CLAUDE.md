# CLAUDE.md

House rules for agents working in this repository.

## Language

- Portuguese (pt-BR) for all communication

## Skill Invocation

- Agents call relevant skills before starting tasks
- User-invoked skills require explicit trigger
- Model-invoked skills available to both

## Subagent Evaluation

- Classify returns: BOM, ACEITÁVEL, RUIM
- Criteria: completeness, evidence, tests run, no fabrication
- RUIM → return to same subagent once with detailed prompt
- Report grade and reason to user

## Subagent Usage

- Only when user asks or task is large/parallel
- Default: Sonnet 4.6, effort low

## No Em Dashes

- Never use em dashes (-) in prose
- Rewrite with comma, colon, period, parentheses, or conjunction