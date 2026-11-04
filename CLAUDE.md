# omniroute

Proxy local que roteia requisições Claude Code para múltiplos provedores gratuitos via combo de modelos.

## Roteamento por tarefa (combos)

OBRIGATÓRIO: antes de executar qualquer tarefa não trivial, delegue com a ferramenta Agent (subagent_type abaixo). Não faça você mesmo. Tarefa com várias partes: delegue cada parte ao subagente da sua categoria.
- código/scripts → `programador` (combo/programacao)
- testes/verificação → `testador` (combo/testes)
- revisão de código ou texto → `revisor` (combo/revisao)
- pesquisa/raciocínio/análise → `pesquisador` (combo/pesquisa)
- segurança/auditoria → `seguranca` (combo/seguranca)
- infra/deploy/Docker/CI → `devops` (combo/devops)
- difícil/crítico/arquitetura → `especialista` (combo/especialistas)
- só perguntas simples ou leitura rápida ficam na sessão principal (combo/modelos gratuitos)

`/model opus` = especialistas, `/model sonnet` = programacao, `/model haiku` = modelos gratuitos.

## Agent skills

### Issue tracker

Issues vivem como arquivos markdown em `.scratch/`. Veja `docs/agents/issue-tracker.md`.

### Domain docs

Single-context: `GLOSSARY.md` na raiz + `docs/adr/`. Veja `docs/agents/domain.md`.
