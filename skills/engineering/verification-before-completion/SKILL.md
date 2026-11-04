---
name: verification-before-completion
description: "Use when about to claim work is complete, fixed, or passing, before committing or creating PRs - requires running verification commands and confirming output before making any success claims; evidence before assertions always"
---

# Verification Before Completion

Evidência antes de claims. "complete", "fixed", "passing" requerem prova.

## Trigger

Auto-invoked quando agente diz "done", "fixed", "complete", "passing".

## When to reach for it

- Sempre. É guardrail obrigatório.

## What it does

Bloqueia claim sem evidência: test output, build log, screenshot, diff. Força: "tests pass: [output]" não "tests pass".

## Common questions

**Q: Para tarefas não-código?**
Sim. Evidência = output relevante (arquivo criado, comando rodou, etc.)

**Q: Pode ser desativado?**
Não. Hard rule no CLAUDE.md.

## It's working if

Zero claims sem evidência no histórico.