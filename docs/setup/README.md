# Meu setup do Claude Code (estado de novembro de 2026)

Retrato real e sem dados pessoais do meu `~/.claude`. O objetivo de tudo aqui é gastar menos tokens por sessão sem perder qualidade. Cada item diz **o que é**, **por que está** e, quando foi tirado, **por que saiu**.

Máquina: notebook Windows 11, 7,6 GB de RAM, VS Code + Claude Code. Isso pesa em várias escolhas (pouca RAM, um processo pesado por vez).

## Visão geral: de onde vem o custo

Uma sessão paga tokens em quatro lugares. Cada camada do setup ataca um deles:

| Custo | O que gera | O que uso contra |
|---|---|---|
| Prefixo fixo (todo turno) | lista de skills, plugins, MCPs, CLAUDE.md | poucas skills visíveis, plugins desligados, sem MCP global |
| Entrada de ferramentas | saída de comandos, testes, arquivos lidos | rtk, `filtra-testes.py`, `bashOutputMaxChars`, ler por faixa |
| Saída do modelo | texto das respostas, thinking | caveman, ponytail, `effortLevel: low`, thinking desligado |
| Repetição | releituras, loops de erro, contexto velho | cache de 1 h, `loop-edicao.py`, compactação guiada, `/clear` por assunto |

## 1. Skills: poucas visíveis, o resto escondido

Toda skill visível entra na listagem do início de cada sessão. Por isso:

| Onde | O que | Efeito |
|---|---|---|
| `~/.claude/skills/` | ~24 skills que uso de fato | listadas |
| `~/.claude/skills_desligadas/` | 26 skills fora de uso (Maestri, engenharia reversa, brainstorming, llm-council, writing-plans etc.) | não carregam; volto com um `mv` |
| `skillOverrides` | skills de plugin em `user-invocable-only` ou `off` (~55 entradas) | só com `/nome` explícito |
| `skillListingMaxDescChars: 150` | corta cada descrição | listagem menor |
| `skillListingBudgetFraction: 0.002` | teto da listagem no contexto | limite rígido |

Regras das skills:
- Descrição de uma linha, começando com "Use when ...", sem exemplos. Texto longo vai para `references/` dentro da skill e só carrega quando preciso.
- `user-invocable-only` quando a skill é útil mas não deve disparar sozinha (caveman, ponytail, graphify, humanizer, TDD). `off` quando não uso mais.
- Desligar é mover para `skills_desligadas/`, nunca apagar. Volta fácil e não perde o trabalho.
- Skills pessoais (TriboDEM, DA, DRX, Lattes, meus apps) não entram neste repo; veja [SCOPE](../../SCOPE.md).

Quais o modelo chama sozinho, por tipo de tarefa (regra no CLAUDE.md global):

| Tarefa | Skill |
|---|---|
| bug | systematic-debugging |
| review | code-review (nativa) |
| antes de dizer "pronto" | verification-before-completion |
| interface | ui-ux-pro-max |
| página/Artifact | artifact-design (nativa) |
| pesquisa ampla | deep-research (nativa) |
| testar app desktop como leigo | teste-leigo |

**Por que saíram:**
- `brainstorming`, `writing-plans`, `llm-council`: ritual longo antes de cada tarefa. Gastavam mais tokens do que economizavam em tarefas do dia a dia. Plano curto vai em `~/.claude/planos/` só se tiver mais de 3 passos.
- Maestri (7 skills) e `orca-cli`: orquestração externa que parei de usar. Arquivadas, não apagadas.
- Skills de engenharia reversa: uso raro; ficam desligadas e religo quando preciso.
- `impeccable` e `taste-skill` como plugin: duplicavam as versões em `~/.claude/skills/`. Ficou a cópia local em `user-invocable-only`, e `ui-ux-pro-max` é a padrão para interface (uma só, para não carregar três guias de design).

## 2. Plugins: só os que encurtam a saída

Ligados:
- **caveman**: respostas tersas (fragmentos, sem cerimônia). Corta a saída, que é o token mais caro. Uso no nível `ultracave`.
- **ponytail**: "dev sênior preguiçoso", o menor diff que resolve. Menos código escrito é menos saída e menos revisão.

Os dois rodam por hook de `SessionStart`, por isso as skills deles ficam `user-invocable-only` (já estão ativas, não precisam aparecer na listagem).

Registrados em `extraKnownMarketplaces` mas `false` (ligo para uma tarefa e desligo depois):

| Plugin | Por que está desligado |
|---|---|
| `ecc` (everything-claude-code) | pesado: ~87 skills e o GateGuard, que forçava texto extra antes de agir |
| `context-mode` | texto de início grande, servidor MCP junto e compressor de Bash que duplicava o rtk |
| `context-optimizer` (cco) | redundante com rtk + compactação guiada |
| `mattpocock-skills`, `andrej-karpathy-skills` | redundantes com ponytail/caveman; tiravam uns 5 a 10 mil tokens fixos (estimativa, não medida) |
| `sentry-skills`, `cloudflare` | só servem para esses serviços, que não uso no dia a dia |
| `impeccable`, `taste-skill` | duplicavam as cópias locais (ver seção 1) |
| `setup-token-savings`, `context-engineering` | testados; o que tinham de útil já está nos meus settings e hooks |

Também nego em `permissions.deny` os subagentes `caveman:cavecrew-*` (Haiku): eram chamados sem eu pedir e o retorno era fraco para o meu tipo de trabalho. Uso o `triage` próprio no lugar (seção 5).

## 3. Hooks

| Hook | Evento | Por que |
|---|---|---|
| `rtk hook claude` (via `filtra-testes.py`) | `PreToolUse` Bash | [rtk](https://github.com/rtk-ai/rtk) condensa a saída de comandos antes de entrar no contexto |
| [`filtra-testes.py`](hooks/filtra-testes.py) | `PreToolUse` Bash | comando de teste: roda uma vez, salva o log e devolve só falhas (traceback com `-A 15`) + resumo. Passou, devolve só o fim |
| [`loop-edicao.py`](hooks/loop-edicao.py) | `PostToolUse` Edit/Write/Bash/PowerShell | 5 edições no mesmo arquivo sem rodar teste: avisa o agente. Evita loop de "edita, erra, edita" que queima tokens |
| [`pre-compact.py`](hooks/pre-compact.py) | `PreCompact` | diz à compactação o que GUARDAR (pedidos literais, decisões, arquivos, números) e o que JOGAR FORA (logs, tentativas mortas). Resumo até ~800 palavras. Também grava `HANDOFF.md` no projeto para uma sessão nova retomar lendo só ele |
| `troca-assunto.py` (pessoal, não incluído) | `UserPromptSubmit` + `SessionStart` | detecta troca de projeto no prompt (TriboDEM, DA etc.), sugere `/clear` e, depois do `/clear`, reexecuta o pedido sozinho. Contexto de um projeto não contamina o outro |
| watchdog do Remote Control (pessoal) | `SessionStart` | reconecta o Remote Control quando a internet volta |
| Orca e Codenotch (pessoais) | vários | status e notificações no desktop; não afetam tokens |

**Por que saíram** (ficam em `hooks/_arquivados/`, não apagados):
- `laya-gate.mjs`: filtro de thinking. Carregava um modelo ONNX a cada prompt e custava ~35 tokens por turno; com thinking desligado e effort `low`, não compensava.
- `context-mode-cache-heal.mjs`: só existia por causa do plugin context-mode, que desliguei.
- `autoclear.ps1`: limpava sozinho; trocado pelo `troca-assunto.py`, que pergunta antes e não perde o pedido.
- `caveman-statusline.ps1`, `start_orchestrator.ps1`, `erros_softwares.py`: substituídos pela statusline do Orca ou sem uso.

## 4. Settings que economizam

Veja [`settings.example.json`](settings.example.json).

| Setting | Por que |
|---|---|
| `model: opus` + `effortLevel: low` em todos os modelos | modelo forte, raciocínio curto por padrão; subo o effort só quando a tarefa pede |
| `alwaysThinkingEnabled: false`, `showThinkingSummaries: false` | thinking é saída paga; desligado por padrão |
| `promptCacheTtl: "1h"` | cache sobrevive a pausas longas; o prefixo fixo é cobrado barato |
| `autoCompactWindow: 200000` + `precomputeCompactionEnabled` | compacta antes de estourar, já com o resumo pré-calculado |
| `bashOutputMaxChars: 10000` | teto para saída de ferramenta |
| `includeGitInstructions: false` | tira o texto de git embutido no prompt |
| `promptSuggestionEnabled`, `awaySummaryEnabled`, `autoMemoryEnabled: false` | cada um gera chamadas ou contexto extra que não uso |
| `disableClaudeAiConnectors`, `syncClaudeAiPlugins: false` | conectores do claude.ai viram MCPs no prefixo; desligados |
| `CLAUDE_CODE_GOAL_CHECKIN_MINUTES=0` | sem check-in periódico automático |

**Por que não uso** `CLAUDE_CODE_SUBAGENT_MODEL` global (usava antes): cada agente agora declara o próprio `model` no frontmatter (seção 5), o que é mais preciso.

## 5. Subagentes

Regra: delegar só leitura grande (mais de ~5 arquivos ou logs grandes), pesquisa web, ou quando eu peço. Cada subagente começa do zero e relê contexto, então tarefa pequena faz direto.

| Agente | Modelo | Para quê |
|---|---|---|
| `triage` ([exemplo](agents/triage.md)) | Haiku | busca barata: arquivo, símbolo, config, erro. Resposta em até 120 tokens |
| `programador`, `design`, `documentador`, `teste` | Sonnet, effort low, `maxTurns: 50` | implementar, UI, docs, rodar testes |
| `revisor` ([exemplo](agents/revisor.md)) | Sonnet | revisa diff sem editar |
| `pesquisador`, `fisico` | Sonnet + WebSearch | literatura e análise numérica |
| `Explore` | Sonnet | varredura só leitura |

- Todos leem `~/.claude/regras_agentes.md` (regras comuns: pt-BR, não apagar dados, processo longo em segundo plano, entregar com evidência). Fica num arquivo só para não repetir em cada agente.
- Pergunta estreita com formato de saída fixo.
- Retorno avaliado: BOM, ACEITÁVEL ou RUIM. RUIM volta uma vez com prompt mais detalhado; se continuar ruim, faço sozinho.

## 6. Hábitos do CLAUDE.md global

- Regras curtas e imperativas: idioma, autonomia, git, tokens, skills, subagentes.
- Ler arquivo por faixa ou grep, nunca inteiro sem precisar. Saída grande vai para log em disco e leio com `grep -A 15 -E 'ERROR|FAIL|Traceback'` + `head`.
- Mudou de assunto ou voltou depois de mais de 1 h: `/clear` (com `/rename`). `/compact` só no fim de fase.
- **Prefixo estável**: não trocar modelo, MCPs, skills ou CLAUDE.md no meio da sessão. Qualquer troca invalida o cache e o prefixo inteiro é cobrado de novo.
- Commit e push uma vez por mês (menos ruído e menos turnos gastos em git).

## 7. MCPs

Nenhum MCP global. Os conectores do claude.ai estão desligados e o único MCP fica no escopo de um projeto específico. **Por quê:** cada MCP põe a descrição de todas as ferramentas no prefixo de toda sessão. Ferramentas de navegador e afins entram como "deferred" (só o nome aparece) e carrego com `ToolSearch` quando preciso.

## 8. Projetos relacionados

| Projeto | Ideia | Situação |
|---|---|---|
| [JuliusBrussee/caveman](https://github.com/JuliusBrussee/caveman) | voz terse | em uso |
| [DietrichGebert/ponytail](https://github.com/DietrichGebert/ponytail) | menor diff | em uso |
| [rtk-ai/rtk](https://github.com/rtk-ai/rtk) | condensa saída de comandos | em uso (v1.1.0) |
| [Kulaxyz/token-diet](https://github.com/Kulaxyz/token-diet) | skill sempre ligada de respostas curtas | sobrepõe caveman + ponytail; não instalado |
| [nidhinjs/prompt-master](https://github.com/nidhinjs/prompt-master) | reescreve prompts para acertar de primeira | candidato sob demanda |
| [foryourhealth111-pixel/Vibe-Skills](https://github.com/foryourhealth111-pixel/Vibe-Skills) | roteia entre ~195 skills | pesado; minha solução é ter menos skills visíveis |
