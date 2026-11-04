# Task Observer

Monitora execução de tarefas multi-step para melhorar skills.

## Trigger

Auto-invoked em tarefas > 3 passos. Ou user-invoked: "observe this task".

## When to reach for it

- Workflows complexos
- Debug de skills
- Otimização de processos

## What it does

Registra: passos, ferramentas usadas, tempo, erros, decisões. Gera relatório no fim com padrões e sugestões de skills.

## Common questions

**Q: Salva dados sensíveis?**
Não. Só metadados de execução.

**Q: Onde fica o relatório?**
`.claude/task-observer/` no projeto.

## It's working if

Relatório gerado com > 3 insights acionáveis.