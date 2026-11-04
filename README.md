# Skills for SAVING CLAUDE TOKEN

Documentação completa das skills do Claude Code, organização, hooks e configurações do Yuri.

## Estrutura do Repositório

```
.
├── skills/           # Lista de skills instaladas com descrições
├── hooks/            # Configuração de hooks do Claude Code
├── settings.json     # Configurações completas do settings.json
├── agents/           # Tipos de subagentes disponíveis
└── marketplaces/     # Marketplaces de skills configurados
```

## Skills Instaladas (37 skills)

### Skills Principais (ativas)
| Skill | Descrição | Trigger |
|-------|-----------|---------|
| `brainstorming` | Pré-requisito para trabalho criativo | Criar features, componentes |
| `career-ops` | Candidaturas e LinkedIn do Yuri | "preencher vaga", "candidatura" |
| `claude-real-video` | Assistir vídeos (YouTube/local) | URL de vídeo ou arquivo |
| `computer-use` | GUI automation via Orca | Janela visível precisa controle |
| `dem-vale-referencias` | Modelagem/calibração DEM e desgaste | TriboDEM, literatura |
| `drx-refinamento` | Refinamento XRD (Le Bail, Rietveld) | GSAS-II no DA |
| `entrevista-pre-tarefa` | 5-15 perguntas antes de tarefa complexa | `/entrevista-pre-tarefa` |
| `find-skills` | Descobrir e instalar skills | "como fazer X", "find skill" |
| `graphify` | Knowledge graph de código | `/graphify` ou graphify-out/ |
| `humanizer` | Remover padrões de escrita de IA | Textos a humanizar |
| `impeccable` | Design/frontend de alto nível | UI, landing pages, dashboards |
| `lattes-agente` | Currículo Lattes e PDF do CV | Lattes, certificados |
| `llm-council` | Conselho de 5 advisors | "council this" |
| `maestri` | Comunicação inter-agentes no canvas | "ask [name] to..." |
| `maestri-chat` | Mensagens do Maestri Chat | Header Maestri Chat |
| `maestri-computer` | Controle de apps via Maestri | Operar apps externos |
| `maestri-manager` | Orquestração de agentes no canvas | "assemble team", "delegate" |
| `maestri-portal` | Browser automation no canvas | "browse URL", "test web UI" |
| `maestri-portal-devices` | Android emulator/phone no canvas | "run mobile app" |
| `maestri-routines` | Rotinas agendadas no canvas | "schedule command" |
| `maestri-workspace` | Provisionar workspaces/floors | "new workspace", "new floor" |
| `maestro` | Sessão Maestro (planeja/delega) | `/maestro` |
| `orca-cli` | Orca worktrees, terminais, browser | "$orca-cli", "Orca worktree" |
| `orchestration` | Workers Orca (Codex, Claude) | "Have Codex review this" |
| `rpa-dev` | DA (Data Analyzer) - arquitetura, testes | DA, i18n, pitfalls |
| `skills-smart-manager` | Auditar/fundir/aposentar skills | Ciclo de vida de skills |
| `softwares-do-yuri` | Mapa dos 6 softwares do Yuri | DA, TriboDEM, FlowCalc, etc |
| `systematic-debugging` | Debug sistemático (root cause first) | Qualquer bug/falha |
| `task-observer` | Monitora execução para melhorar skills | Multi-step tasks |
| `taste-skill` | Design frontend anti-slop | Landing pages, marketing sites |
| `test-driven-development` | TDD obrigatório | Features, bugfixes, refactor |
| `teste-leigo` | Teste como usuário leigo/impaciente | Apps desktop PySide6 |
| `tribodem-dev` | TriboDEM Studio (Yade, Chrono, OpenFOAM) | TriboDEM, lotes, Monitor |
| `ui-ux-pro-max` | Design intelligence (79 styles, 192 palettes) | UI/UX, acessibilidade |
| `verification-before-completion` | Evidência antes de claims | "complete", "fixed", "passing" |
| `writing-plans` | Planos de implementação | Multi-step tasks |

### Skills Caveman (ativas)
- `caveman` - Modo caveman (terse, smart)
- `caveman:caveman-commit` - Commits caveman
- `caveman:caveman-compress` - Compressão caveman
- `caveman:caveman-discover` - Descoberta caveman
- `caveman:caveman-evidence-review` - Review de evidência
- `caveman:caveman-explore` - Exploração caveman
- `caveman:caveman-help` - Ajuda caveman
- `caveman:caveman-learn` - Aprendizado caveman
- `caveman:caveman-manage` - Gerenciamento caveman
- `caveman:caveman-optimize` - Otimização caveman
- `caveman:caveman-review` - Review caveman
- `caveman:caveman-setup` - Setup caveman
- `caveman:caveman-stats` - Stats caveman
- `caveman:investigate-first` - Investigar primeiro
- `caveman:lean-build` - Build enxuto
- `caveman:migration` - Migração caveman
- `caveman:safe-refactor` - Refatoração segura
- `caveman:surgical-patch` - Patch cirúrgico
- `caveman:verify-and-stop` - Verificar e parar

### Skills Ponytail (ativas)
- `ponytail` - Lazy senior developer
- `ponytail:ponytail-audit` - Auditoria ponytail
- `ponytail:ponytail-debt` - Dívida técnica
- `ponytail:ponytail-gain` - Ganhos ponytail
- `ponytail:ponytail-help` - Ajuda ponytail
- `ponytail:ponytail-review` - Review ponytail

### Skills Desabilitadas (off no settings.json)
- `brainstorming`, `writing-plans` (superpowers)
- `systematic-debugging`, `test-driven-development`, `verification-before-completion` (superpowers)
- `computer-use`, `maestro`, `lattes-agente`, `llm-council`
- `orca-cli`, `maestri-chat`, `maestri-computer`, `maestri-manager`, `maestri-portal`, `maestri-routines`, `maestri-workspace`, `maestri`
- `brainstorming`, `writing-plans` (duplicados)
- `skills-smart-manager`

## Subagentes Disponíveis (18 tipos)

| Agente | Uso | Modelo/Esforço |
|--------|-----|----------------|
| `caveman:cavecrew-builder` | Edits cirúrgicos 1-2 arquivos | Haiku, low |
| `caveman:cavecrew-investigator` | Localizador read-only | Haiku, low |
| `caveman:cavecrew-reviewer` | Review de diff/branch/arquivo | Haiku, low |
| `claude` | Catch-all geral | Sonnet 4.6, low |
| `claude-code-guide` | Perguntas sobre Claude Code/SDK/API | Haiku, low |
| `design` | Interface, cores, ícones, layout | Sonnet 4.6, low |
| `devops` | Infra, deploy, Docker, CI/CD | Sonnet 4.6, low |
| `documentador` | Docs, notas, TAREFAS.md, relatórios | Sonnet 4.6, low |
| `especialista` | Tarefas difíceis/críticas/arquitetura | Opus 5.5, low |
| `Explore` | Busca read-only ampla | Sonnet 4.6, low |
| `fisico` | Análise física/numérica | Sonnet 4.6, low |
| `general-purpose` | Pesquisa complexa, multi-step | Sonnet 4.6, low |
| `pesquisador` | Pesquisa, raciocínio longo, análise | Sonnet 4.6, low |
| `Plan` | Arquiteto de software (planos) | Sonnet 4.6, low |
| `programador` | Escrever/editar/refatorar/debug código | Sonnet 4.6, low |
| `revisor` | Review código, diffs, textos | Sonnet 4.6, low |
| `seguranca` | Security review, auditoria, segredos | Sonnet 4.6, low |
| `statusline-setup` | Configurar status line | Haiku, low |
| `testador` | Testes, verificações | Sonnet 4.6, low |
| `teste` | Rodar suítes de teste | Sonnet 4.6, low |

## Roteamento por Tarefa (combos obrigatórios)

**OBRIGATÓRIO:** Antes de tarefa não trivial, delegue com ferramenta Agent (subagent_type abaixo).

| Categoria | Subagente | Combo |
|-----------|-----------|-------|
| Código/scripts | `programador` | combo/programacao |
| Testes/verificação | `testador` | combo/testes |
| Revisão código/texto | `revisor` | combo/revisao |
| Pesquisa/raciocínio/análise | `pesquisador` | combo/pesquisa |
| Segurança/auditoria | `seguranca` | combo/seguranca |
| Infra/deploy/Docker/CI | `devops` | combo/devops |
| Difícil/crítico/arquitetura | `especialista` | combo/especialistas |
| Perguntas simples/leitura rápida | Sessão principal | combo/modelos gratuitos |

## Configuração de Hooks (settings.json)

### Hooks Ativos

| Evento | Comando | Descrição |
|--------|---------|-----------|
| `PreToolUse` (Bash) | `rtk hook claude` | Hook RTK para comandos Bash |
| `PreToolUse` (*) | `orca-agent-hook.exe claude` | Orca agent hook (timeout 10s) |
| `SessionStart` | `remote_control_watchdog.ps1` | Watchdog Remote Control |
| `SessionStart` | `orca-agent-hook.exe claude` | Orca agent hook |
| `PreCompact` | `pre-compact.py` | Pre-compact hook (timeout 10s) |
| `UserPromptSubmit` | `orca-agent-hook.exe claude` | Orca agent hook |
| `Stop` | `orca-agent-hook.exe claude` | Orca agent hook |
| `StopFailure` | `orca-agent-hook.exe claude` | Orca agent hook |
| `SubagentStart` | `orca-agent-hook.exe claude` | Orca agent hook |
| `SubagentStop` | `orca-agent-hook.exe claude` | Orca agent hook |
| `TeammateIdle` | `orca-agent-hook.exe claude` | Orca agent hook |
| `PostToolUse` (*) | `orca-agent-hook.exe claude` | Orca agent hook |
| `PostToolUseFailure` (*) | `orca-agent-hook.exe claude` | Orca agent hook |
| `PermissionRequest` (*) | `orca-agent-hook.exe claude` | Orca agent hook |
| `PostCompact` | `orca-agent-hook.exe claude` | Orca agent hook |
| `Elicitation` (*) | `orca-agent-hook.exe claude` | Orca agent hook |
| `ElicitationResult` (*) | `orca-agent-hook.exe claude` | Orca agent hook |
| `SessionEnd` | `orca-agent-hook.exe claude` | Orca agent hook |

### Hooks Arquivados (em `~/.claude/hooks/_arquivados/`)
- `caveman-statusline.ps1` - Status line caveman
- `context-mode-cache-heal.mjs` - Cache heal context mode
- `erros_softwares.py` - Erros de softwares
- `laya-gate.mjs` - Laya gate
- `start_orchestrator.ps1` - Start orchestrator

## Marketplaces de Skills Configurados

| Marketplace | Source | Repo |
|-------------|--------|------|
| `claude-plugins-official` | github | anthropics/claude-plugins-official |
| `ponytail` | github | DietrichGebert/ponytail |
| `caveman` | github | JuliusBrussee/caveman |
| `msadura` | github | msadura/claude-plugins-marketplace |
| `ecc` | github | affaan-m/everything-claude-code |
| `context-engineering-marketplace` | github | muratcankoylan/agent-skills-for-context-engineering |
| `mattpocock` | github | mattpocock/skills |
| `karpathy-skills` | github | forrestchang/andrej-karpathy-skills |
| `cloudflare` | github | cloudflare/skills |
| `context-mode` | github | mksglu/context-mode |
| `cco` | github | egorfedorov/claude-context-optimizer |
| `sentry-skills` | github | getsentry/skills |

## Configurações Importantes (settings.json)

```json
{
  "model": "haiku",
  "defaultMode": "bypassPermissions",
  "CLAUDE_CODE_SUBAGENT_MODEL": "claude-sonnet-4-6",
  "promptCacheTtl": "1h",
  "autoCompactEnabled": true,
  "autoCompactWindow": 100000,
  "precomputeCompactionEnabled": true,
  "bashOutputMaxChars": 10000,
  "syntaxHighlightingDisabled": true,
  "feedbackDrafts": "off",
  "autoMemoryEnabled": false,
  "showThinkingSummaries": false,
  "skipDangerousModePermissionPrompt": true,
  "theme": "dark"
}
```

### Model Settings (effortLevel)
- `claude-opus-5-5`: medium
- `claude-sonnet-4-6`: low
- `claude-opus-4-6`: low
- `claude-sonnet-5-5`: low
- `combo/modelos gratuitos`: xhigh

## Regras da Casa (CLAUDE.md)

### Idioma
- **Apenas Português Brasileiro (pt-BR)** em todas as sessões
- Tudo automático, sem passos manuais

### Skills - Regra de Ouro
- Todo agente chama **sozinho, antes de começar**, as skills da tarefa:
  - TriboDEM → `tribodem-dev` (+ `dem-vale-referencias`)
  - Softwares do Yuri → `softwares-do-yuri` (+ `rpa-dev` no DA, `drx-refinamento` em DRX)
  - Pesquisa → `anthropic-skills:deep-research`
  - Bug → `systematic-debugging`
  - Revisão → `code-review`
  - Testes → `verification-before-completion`
  - UI → `artifact-design`

### Avaliação de Retornos de Subagentes
- Classificar: **BOM**, **ACEITÁVEL** ou **RUIM**
- Critérios: respondeu tudo, com evidência/fonte/file:line, números com unidade, testes rodados, sem inventar
- RUIM (ou ACEITÁVEL com lacuna) → devolver ao MESMO subagente (máx 1 refazer)
- Dizer ao Yuri a nota e por quê

### Subagentes
- Só usar quando Yuri pedir, ou tarefa grande e paralela
- Todo subagente usa **Sonnet 4.6 com esforço low** (model: claude-sonnet-4-6, effort: low)

## Plugins Habilitados
- `ponytail@ponytail`: true
- `caveman@caveman`: true
- Demais: false

## Status Line
- Comando: `C:/Users/yuri/.orca/agent-hooks/claude-statusline.cmd`

---

*Gerado automaticamente em 2026-11-04*