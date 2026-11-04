# Systematic Debugging

Debug sistemático (root cause first). Para qualquer bug/falha.

## Trigger

User-invoked. "debug this" ou "systematic debugging" ao encontrar bug.

## When to reach for it

- Testes falhando
- Comportamento inesperado
- Crash/exception
- Performance degradation

## What it does

Processo: reproduce → isolate → hypothesize → test hypothesis → fix → verify → prevent regression. Não pula etapas.

## Common questions

**Q: Funciona para bugs de produção?**
Sim. Mesmo processo, mais cuidado com dados.

**Q: Precisa de testes?**
Cria teste de regressão se não existir.

## It's working if

Root cause identificado, fix minimal, teste de regressão passando.