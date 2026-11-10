# AGENTS.md

Subagentes que uso hoje (`~/.claude/agents/`). O porquê de cada escolha está em [docs/setup](./docs/setup/README.md), seção 5.

## Agentes próprios

| Agente | Modelo | Effort | Ferramentas | Uso |
|---|---|---|---|---|
| triage | Haiku | padrão | Read, Grep, Glob | busca barata: arquivo, símbolo, config, erro (até 120 tokens) |
| programador | Sonnet | low | Read, Write, Edit, Grep, Glob, Bash, Skill | implementar e corrigir código, lançar testes/lotes |
| design | Sonnet | low | Read, Write, Edit, Grep, Glob, Bash, Skill | interface, cores, ícones, layout |
| documentador | Sonnet | low | Read, Write, Edit, Grep, Glob, Bash | notas, docs, relatórios |
| teste | Sonnet | low | Read, Grep, Glob, Bash, Skill | rodar suítes e relatar pass/fail |
| revisor | Sonnet | low | Read, Grep, Glob, Bash | revisar diff sem editar |
| pesquisador | Sonnet | low | + WebSearch, WebFetch | literatura e dados na web |
| fisico | Sonnet | low | + WebSearch, WebFetch | análise física/numérica de resultados |
| Explore | Sonnet | low | Read, Grep, Glob, Bash | varredura só leitura |

Todos com `maxTurns: 50` (menos o triage e o Explore) e todos leem `~/.claude/regras_agentes.md` antes de começar.

## Nativos usados

`general-purpose`, `Plan`, `claude-code-guide`, `statusline-setup`.

## Removidos e por quê

- `caveman:cavecrew-builder/investigator/reviewer`: negados em `permissions.deny`; disparavam sem pedido e o retorno era fraco. O `triage` cobre a busca barata.
- `especialista` (Opus), `seguranca`, `devops`, `testador`: sobrepunham com a sessão principal (já em Opus) e com `teste`/`revisor`.
- Roteamento por combos do proxy (`combo/programacao` etc.): fora deste repo; cada agente declara o modelo no frontmatter.

## Regras

- Delegar só leitura grande (mais de ~5 arquivos ou logs grandes), pesquisa web, ou quando pedido.
- Pergunta estreita, formato de saída fixo.
- Retorno avaliado: BOM, ACEITÁVEL ou RUIM; RUIM volta uma vez com prompt mais detalhado.
- Skills: `disable-model-invocation: true` para as só do usuário. Veja `.agents/invocation.md`.
