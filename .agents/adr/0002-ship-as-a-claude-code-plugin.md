# ADR 0002: Instalar por links, plugin depois

## Decisão

Hoje a instalação é por links simbólicos (`scripts/link-skills.sh`) em `~/.claude/skills` e `~/.agents/skills`. Empacotar como plugin do Claude Code fica para depois.

## Por quê

Com links, editar a skill no repo muda a instalada na hora, sem republicar. Plugin só compensa se outras pessoas forem instalar. Se virar plugin, o manifesto deve listar exatamente o conjunto promovido, validado com `claude plugin validate . --strict`.
