# Skills for SAVING CLAUDE TOKEN

Documentação genérica de skills do Claude Code, organização, hooks e configurações.

## Estrutura do Repositório

```
.
├── skills/           # Lista de skills instaladas com descrições
├── hooks/            # Configuração de hooks do Claude Code
├── settings.json     # Configurações completas do settings.json
├── agents/           # Tipos de subagentes disponíveis
└── marketplaces/     # Marketplaces de skills configurados
```

## Skills Instaladas (14 skills genéricas)

### Skills Principais (ativas)
| Skill | Descrição | Trigger |
|-------|-----------|---------|
| `brainstorming` | Pré-requisito para trabalho criativo | Criar features, componentes |
| `find-skills` | Descobrir e instalar skills | "como fazer X", "find skill" |
| `graphify` | Knowledge graph de código | `/graphify` ou graphify-out/ |
| `humanizer` | Remover padrões de escrita de IA | Textos a humanizar |
| `impeccable` | Design/frontend de alto nível | UI, landing pages, dashboards |
| `llm-council` | Conselho de 5 advisors | "council this" |
| `systematic-debugging` | Debug sistemático (root cause first) | Qualquer bug/falha |
| `task-observer` | Monitora execução para melhorar skills | Multi-step tasks |
| `taste-skill` | Design frontend anti-slop | Landing pages, marketing sites |
| `test-driven-development` | TDD obrigatório | Features, bugfixes, refactor |
| `teste-leigo` | Teste como usuário leigo/impaciente | Apps desktop |
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

## Subagentes Genéricos

| Agente | Uso | Modelo/Esforço |
|--------|-----|----------------|
| `caveman:cavecrew-builder` | Edits cirúrgicos 1-2 arquivos | Haiku, low |
| `caveman:cavecrew-investigator` | Localizador read-only | Haiku, low |
| `caveman:cavecrew-reviewer` | Review de diff/branch/arquivo | Haiku, low |
| `claude` | Catch-all geral | Sonnet 4.6, low |
| `claude-code-guide` | Perguntas sobre Claude Code/SDK/API | Haiku, low |
| `design` | Interface, cores, ícones, layout | Sonnet 4.6, low |
| `devops` | Infra, deploy, Docker, CI/CD | Sonnet 4.6, low |
| `documentador` | Docs, notas, relatórios | Sonnet 4.6, low |
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

## Roteamento por Tarefa (combos)

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

## Configuração de Hooks (genérica)

### Hooks Comuns
| Evento | Descrição |
|--------|-----------|
| `PreToolUse` | Executa antes de ferramentas |
| `SessionStart` | Início de sessão |
| `PreCompact` | Antes de compactar contexto |
| `UserPromptSubmit` | Envio de prompt do usuário |
| `Stop` | Fim de execução |
| `StopFailure` | Falha na execução |
| `SubagentStart` | Início de subagente |
| `SubagentStop` | Fim de subagente |
| `TeammateIdle` | Colega ocioso |
| `PostToolUse` | Após ferramenta |
| `PostToolUseFailure` | Falha de ferramenta |
| `PermissionRequest` | Solicitação de permissão |
| `PostCompact` | Após compactação |
| `Elicitation` | Elicitação |
| `ElicitationResult` | Resultado elicitação |
| `SessionEnd` | Fim de sessão |

### Hooks Arquivados (exemplos)
- `caveman-statusline.ps1` - Status line caveman
- `context-mode-cache-heal.mjs` - Cache heal context mode
- `laya-gate.mjs` - Laya gate
- `start_orchestrator.ps1` - Start orchestrator

## Marketplaces de Skills (públicos)

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

## Configurações Importantes (settings.json genérico)

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

## Regras Genéricas

### Idioma
- Configurável por usuário

### Skills
- Agentes chamam skills relevantes antes de começar tarefas

### Avaliação de Retornos
- Classificar: **BOM**, **ACEITÁVEL** ou **RUIM**
- Critérios: completude, evidência, testes, sem invenção

### Subagentes
- Usar quando solicitado ou tarefa grande/paralela
- Modelo padrão: Sonnet 4.6, esforço low

## Plugins
- `ponytail@ponytail`: true
- `caveman@caveman`: true
- Demais: false

---

*Documentação genérica - adaptar conforme necessário*