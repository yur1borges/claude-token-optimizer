# Inbox VLRM

> Sessao controladora: `controlador` (este arquivo e o canal de entrada da sessao `vlrm`).
> Criado a pedido da sessao `qe-flow-77` em 2026-10-20.
> Detalhamento recebido de `qe-flow-77` (avaliador final) em 2026-10-20 20:4x.
> Ordem de execucao: T1 -> T2 -> T4 -> T5 -> T3.

## Como usar

- `qe-flow-77` escreve aqui a lista de tarefas para a sessao `vlrm`.
- A sessao `vlrm` le este arquivo, executa e escreve o resultado em `outbox_vlrm.md`.
- `controlador` consolida o que esta no outbox e reporta para `qe-flow-77` a cada 1 hora.

## Tarefas

### Tarefa 1 - Skill de entrevista pre-tarefa
_Status: em andamento (SKILL.md criado; falta teste + decisao de disparo)_

- Objetivo: toda sessao faz >=5 perguntas antes de tarefa nova.
- Escopo: skill em ~/.claude/skills/entrevista-pre-tarefa. Fora: mexer em settings/CLAUDE.md.
- Saida: SKILL.md (ja existe).
- Pronto: o Yuri invoca /entrevista-pre-tarefa e recebe >=5 perguntas cobrindo os 5 elementos. Testar uma vez e reportar.
- Decisao pendente: dispara sozinha ou so pelo comando?

### Tarefa 2 - Agente de propostas de melhoria
_Status: aguardando execucao_

- Objetivo: lista viva de melhorias concretas dos 6 softwares (Write, DA, Financas, Radar Passagens, Flow Calculation, TriboDEM).
- Escopo: so leitura do codigo + escrita em omniroute/propostas.md. Fora: aplicar mudanças.
- Saida: propostas.md com data/hora, software, arquivo:linha, problema, melhoria, ganho esperado, esforco.
- Pronto: >=3 entradas novas por ciclo, sem duplicatas, a cada 30 min e ao fim de cada tarefa.
- Decisao pendente: propostas aprovadas viram tarefa automaticamente?

### Tarefa 3 - Agente do Lattes
_Status: aguardando execucao_

- Objetivo: curriculo Lattes atualizado com as producoes novas do Yuri.
- Escopo: 3 agentes via Playwright (leitor exporta/le o atual; atualizador preenche; verificador confere campo a campo). Login manual pelo Yuri no navegador; senha e CPF nunca em arquivo, log ou mensagem. Nada e salvo/enviado no Lattes sem confirmacao final do Yuri.
- Saida: relatorio lattes_diff.md (antes x depois) + preenchimento pronto para ele confirmar.
- Pronto: verificador mostra 0 divergencia entre a lista de producoes e o Lattes.
- Decisao pendente: fonte das producoes novas (pasta? lista? Scholar/ORCID?).

### Tarefa 4 - Citacoes automaticas no Write
_Status: aguardando execucao_

- Objetivo: o Yuri aponta uma pasta de PDFs -> o Write insere a citacao no texto e gera a lista de referencias.
- Escopo: extrair DOI/metadados (texto do PDF + CrossRef/OpenAlex) e formatar em ABNT NBR 6023, APA 7 ou numerico (Vancouver). Fora: baixar PDFs.
- Saida: modulo + teste no app Write. Caminho do Write: confirmar com o Yuri (provavel Desktop\Claude\Write).
- Pronto: com uma pasta de 10 PDFs de teste, >=9 referencias corretas em cada um dos 3 estilos, e o teste passa.

### Tarefa 5 - Pipeline buscador de referencias
_Status: aguardando execucao_

- Objetivo: base bibliografica de alto nivel para um tema do Yuri.
- Escopo: 4 agentes - entrevistador (tema, palavras-chave, periodo, idiomas), buscador (so fontes legais: Periodicos CAPES, Google Scholar, Scopus, Web of Science, BDTD, Catalogo de Teses CAPES, OpenAlex, Unpaywall), avaliador (Qualis A1/A2, citacoes, relevancia), tradutor (resumos em PT). Fora: qualquer site pirata.
- Saida: planilha/MD com referencia completa, DOI/link, Qualis, tipo, resumo PT, nota de relevancia.
- Pronto: >=100 artigos, >=10 teses, >=10 dissertacoes, >=5 livros, todos com link valido verificado.
- Decisao pendente: tema da primeira busca e area de avaliacao do Qualis (provavel Engenharias II/Materiais).

## Log

- 2026-10-20 - arquivo criado, aguardando as 5 tarefas de `qe-flow-77`.
- 2026-10-20 20:45 - detalhamento completo das 5 tarefas recebido de `qe-flow-77` e transcrito aqui. vlrm inicia T1.
