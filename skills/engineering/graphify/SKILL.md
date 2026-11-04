# Graphify

Knowledge graph de código. Mapeia relações entre arquivos, funções, imports.

## Trigger

`/graphify` ou pasta `graphify-out/` existe no projeto.

## When to reach for it

- Entender codebase grande
- Encontrar dependências ocultas
- Refatoração cross-file
- Documentar arquitetura

## What it does

Roda análise estática, gera graph em `graphify-out/`. Nós = arquivos/funções, arestas = imports/chamadas.

## Common questions

**Q: Funciona em qualquer linguagem?**
Principais: TS/JS, Python, Go, Rust, Java. Outros: best-effort.

**Q: Atualiza sozinho?**
Re-ride `/graphify` após mudanças grandes.

## It's working if

`graphify-out/graph.json` existe e tem > 50 nós.