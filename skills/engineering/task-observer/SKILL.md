---
name: task-observer
description: "Monitors task execution for skill improvement opportunities: logs patterns, user corrections and methodology worth preserving to the workspace, turns them into skill updates in a weekly review, and flags repeating work as new skills. Use during ANY multi-step task, agentic workflow, or work session."
---

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