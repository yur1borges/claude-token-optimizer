# Writing Plans

Planos de implementação para tarefas multi-step.

## Trigger

User-invoked. "plan this" ou "write plan" antes de tarefa complexa.

## When to reach for it

- Features > 3 arquivos
- Refatoração cross-cutting
- Migração
- Qualquer tarefa com dependências

## What it does

Gera plano: objetivo, passos ordenados, arquivos afetados, riscos, testes, rollback. Formato: markdown com checkboxes.

## Common questions

**Q: O modelo segue o plano?**
Deve. Desvio = novo plano.

**Q: Detalhe excessivo?**
Nível: arquivo + função. Não linha.

## It's working if

Plano existe antes do código. Execução segue plano ou documenta desvio.