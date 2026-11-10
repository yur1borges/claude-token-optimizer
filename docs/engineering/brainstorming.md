# brainstorming (desligada)

**Status:** fora do setup. O código está em [skills/deprecated/brainstorming](../../skills/deprecated/brainstorming/SKILL.md) e no meu PC fica em `~/.claude/skills_desligadas/`.

## O que fazia

Sessão de ideias obrigatória antes de qualquer trabalho criativo ou recurso novo, com perguntas, alternativas e um documento de design antes do código.

## Por que saiu

A descrição dela dizia "use antes de qualquer trabalho criativo", então disparava em quase toda tarefa. Para mudanças de 1 a 3 arquivos, a conversa de ideias custava mais tokens que a própria tarefa.

## Como voltar

Mover a pasta de volta para `~/.claude/skills/` e tirar a entrada `"brainstorming": "off"` de `skillOverrides`.
