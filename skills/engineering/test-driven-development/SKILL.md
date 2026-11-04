---
name: test-driven-development
description: "Use when implementing any feature or bugfix, before writing implementation code"
---

# Test Driven Development

TDD obrigatório. Red → Green → Refactor para features, bugfixes, refactor.

## Trigger

User-invoked. "tdd this" antes de escrever código de produção.

## When to reach for it

- Nova feature
- Bugfix (teste de regressão primeiro)
- Refatoração (testes existentes passam)

## What it does

Força ciclo: teste falha → código mínimo passa → refatorar. Não escreve código de produção sem teste falhando antes.

## Common questions

**Q: Para código legacy sem testes?**
Escreve teste de caracterização primeiro.

**Q: Integração vs unitário?**
Começa unitário. Integração se precisar.

## It's working if

Coverage > 80% no código novo. Zero testes comentados.