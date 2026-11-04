# Outbox VLRM

> Canal de saida da sessao `vlrm` para a sessao controladora `controlador`.
> Ler este arquivo: C:/Users/yuri/OneDrive/Desktop/omniroute/inbox_vlrm.md
> Reportado por `controlador` para `qe-flow-77` a cada 1 hora.

## Convencao

- Um bloco `## Tarefa N` por tarefa, com: Status (feito / em andamento / bloqueado),
  Resumo, Entregaveis (caminhos de arquivo), Verificacao (como foi checado), Pendencias.

## Resultados

## Tarefa 1 - Skill de entrevista pre-tarefa
_Status: FEITA (90) - dispatch automatico em tarefa nova nao-trivial, decidido pelo controlador em 21/05_

- Resumo: SKILL.md criado em C:/Users/yuri/.claude/skills/entrevista-pre-tarefa/SKILL.md (1792 bytes, 20:30 de hoje). Frontmatter valido (name + description + version). O harness desta sessao ja listou a skill entre as disponiveis, o que confirma deteccao. Regra: >=5 perguntas ao Yuri antes de toda tarefa nova, cobrindo objetivo, escopo, formato de saida, prazo e criterio de pronto. Excecao declarada: nao interviewar para pergunta factual pontual, tarefa de 1 comando sem entregavel, ou quando o Yuri ja deu os 5 elementos na mesma mensagem. Seguranca: nunca pedir senha, token ou chave.
- Entregaveis: C:/Users/yuri/.claude/skills/entrevista-pre-tarefa/SKILL.md
- Verificacao: leitura do arquivo; confirmacao de que o Claude Code anunciou a skill na lista de skills disponiveis. Teste de disparo real pendente com o Yuri.
- Pendencias: (a) disparar sozinha ou so pelo comando /entrevista-pre-tarefa; (b) o Yuri rodar o comando uma vez e confirmar que recebe >=5 perguntas cobrindo os 5 elementos.

## Tarefa 2 - Agente de propostas de melhoria
_Status: LIBERADA - varredura dos 6 apps em andamento no controlador_

- Resumo: escopo confirmado - leitura do codigo dos 6 apps (Write, DA, Financas, Radar Passagens, Flow Calculation, TriboDEM) + escrita em omniroute/propostas.md. Fora do escopo: aplicar mudancas. Criterio: >=3 entradas novas por ciclo, sem duplicatas, a cada 30 min e ao fim de cada tarefa.
- Pendencias: (a) aprovacao de proposta vira tarefa automaticamente ou so entra na lista; (b) confirmar a frequencia de 30 min e o gatilho de fim de tarefa.

## Tarefa 3 - Agente do Lattes
_Status: LIBERADA (codigo) - execucao e fonte das producoes ficam com o Yuri_

- Resumo: 3 agentes via Playwright (leitor exporta/le o atual, atualizador preenche, verificador confere campo a campo). Login manual pelo Yuri no navegador. Senha e CPF nunca em arquivo, log ou mensagem. Nada e salvo/enviado no Lattes sem confirmacao final do Yuri. Saida: lattes_diff.md (antes x depois).
- Pendencias: fonte das producoes novas (pasta de PDFs / lista manual / ORCID publico / Scholar).

## Tarefa 4 - Citacoes automaticas no Write
_Status: EM ANDAMENTO - modulo pronto e testado (10/10 em cada uma das 3 normas). Falta o teste de uso com o Yuri numa pasta real de PDFs._

- Resumo: modulo `cite.js` no app Write. Extrator de DOI (texto do PDF via pdf.js) + metadados (CrossRef, com fallback OpenAlex por titulo) + 3 formatadores (ABNT NBR 6023:2025, APA 7, Vancouver/ICMJE) + citacao autor-data (NBR 10520:2023 e APA) + ordenacao da lista (alfabetica / ordem de citacao). 8 pontos de chamada nos 8 arquivos do Write routed por `refFor`/`citeFor`/`sortRefs`. Fora do escopo respeitado: nenhum PDF baixado.
- Entregaveis:
  - `C:/Users/yuri/OneDrive/Desktop/Claude/Write/codigo-fonte/src/cite.js` (modulo novo)
  - `C:/Users/yuri/OneDrive/Desktop/Claude/Write/testes/t_refs_normas.js` (teste de aceitacao das 3 normas)
  - `C:/Users/yuri/OneDrive/Desktop/Claude/Write/testes/harness.js` (replay offline das respostas CrossRef/OpenAlex)
  - `C:/Users/yuri/OneDrive/Desktop/omniroute/pdfs_teste/indice.tsv` (gabarito dos 10 PDFs)
- Alteracoes `arquivo:linha` desta rodada:
  - `codigo-fonte/src/cite.js:290` - `citeAbnt6023`: `parts` -> `partes` (era o bug que quebrava TODA citacao ABNT, o estilo padrao)
  - `codigo-fonte/src/cite.js:340` - `citeApa7`: `parts` -> `partes` (mesmo bug)
  - `codigo-fonte/src/cite.js:64-72` - `tituloAproximado`: descarta o carimbo arXiv/bioRxiv (ele sai da margem em corpo MAIOR que o titulo) antes de medir o corpo maximo
  - `codigo-fonte/src/cite.js:73-76` - `colapsarDuplicados`: colapsa glifos duplicados ("elemennt" -> "element") antes de consultar por titulo
  - `codigo-fonte/src/cite.js:77-93` - `pistasDoPdf` + `corrobora`: le a faixa de paginas e o ano do cabecalho do PDF para corroborar o registro quando o titulo esta em japones (similaridade de string = 0)
  - `codigo-fonte/src/cite.js:95-110` - `parecidoTitulo`: similaridade por trigramas (tolera texto embaralhado do PDF)
  - `codigo-fonte/src/cite.js:126-139` - `crossrefPorTitulo` + `openAlexPorTitulo`: fallback por titulo (4 dos 10 PDFs nao imprimem o proprio DOI)
  - `codigo-fonte/src/cite.js:154-163` - `crossrefParaBib`: ano da tese vem de `created` (o CrossRef deixa `issued` vazio); `institution` lido como objeto (virava `[object Object]`)
  - `codigo-fonte/src/cite.js:29-51` - `extrairDoisDePaginas`: cola linhas vizinhas (DOI partido entre duas linhas)
  - `codigo-fonte/src/cite.js:231-243` - `apaAutores`: separador `, & ` antes do ultimo autor (antes virava "Thakur, S. C.Ooi, J. Y., Ahmadian, H., &")
  - `codigo-fonte/src/cite.js:226-230` - `abntAutores`: remove o ponto duplicado do "et al."
  - `codigo-fonte/src/cite.js:245-279` - `refAbnt6023`: `In:` restaurado, branch `preprint`
  - `codigo-fonte/src/cite.js:295-345` - `refApa7`: DOI como `https://doi.org/...` sem rotulo e sem ponto final (7a ed.), `n.d.` no lugar de `s.d.`, issue colada no volume sem virgula, editors NAO invertidos no `In`, 21+ autores = 19 primeiros + reticencias + ultimo (sem `et al.`), paginas com en dash, branch `preprint`
  - `codigo-fonte/src/cite.js:345-425` - `refVancouver` reescrito conforme ICMJE/NLM: iniciais SEM ponto (max 2), 6+ autores = 6 + et al, ordem do livro `Autor. Titulo. Edicao. Local: Editora; Ano.`, `dissertation` (doutorado) vs `master's thesis` (mestrado), paginas abreviadas (123-125 -> 123-5), `p.` para capitulo, `doi:` sem URL
  - `testes/harness.js:8-21,45-46` - replay offline das buscas por titulo (7 queries capturadas em `testes/fixtures/busca/`)
  - `testes/t_refs_normas.js:75-79` - marcadores de tipo por estilo corrigidos (os 2 "9/10" anteriores eram regex erradas do TESTE, nao defeito do codigo)
- Calibracao da ABNT contra a norma (rodada 2, fonte primaria):
  - `codigo-fonte/src/cite.js:5` - cabecalho: "ABNT NBR 6023:2024" -> "6023:2025"
  - `codigo-fonte/src/cite.js:247-262` - novo `abntLink`: 6023:2025 §7.7.6/§6.6 fixa a ordem dos elementos de meio eletronico no fim da referencia (DOI, "Disponivel em:", "Acesso em:"). **Corrige bug real: o DOI sumia sempre que a obra tinha URL** (o `if/else` antigo era mutuamente exclusivo). O "Acesso em" fica de fora de proposito - a data de acesso nao e persistida, e uma data volatil mudaria o texto do documento a cada reabertura.
  - `codigo-fonte/src/cite.js:270-276` - `refAbnt6023` tese/dissertacao: 6023:2025 §7.1.2 (autor, titulo, ano de deposito, tipo com grau entre parenteses, vinculo, local, data de defesa). Antes nao tinha local nem data de defesa.
  - `codigo-fonte/src/cite.js:229-236` - `abntAutores`: 6023:2025 §8.1.1.1 (ate 3 autores, todos) e §8.1.1.2 (4 ou mais, so o primeiro + "et al."). O corte era em 4 (5+).
  - `codigo-fonte/src/cite.js:288-292` - `citeAbnt6023`: NBR 10520:2023 - 4+ autores na citacao tambem viram "Primeiro et al.". O corte era em 4 (5+).
  - `codigo-fonte/src/cite.js:444` - `CITE_STYLES.abnt.nome`: "ABNT NBR 6023:2024" -> "2025"
  - Edicao da norma: **6023:2025** (3a ed., 68 p.) = 6023:2018 (2a ed.) + Emenda 1 de 21.05.2025, que cancela e substitui a 2018. **Nao existe edicao 2024** - o rotulo antigo estava errado. Fonte primaria: PDF da 3a ed. lido em `engenhariaedesenvolvimentosustentavel.ufes.br/.../abnt_nbr_6023_-_referencias.pdf` (prefaces lido verbatim); 2018 conferida em `ufpe.br/documents/40070/1837975/ABNT+NBR+6023+2018+(1).pdf`
- Verificacao:
  - `node t_refs_normas.js` EXIT=0 - **DOI 10/10, ABNT 10/10, APA 10/10, NUM 10/10** (criterio: >=9 em cada)
  - `node t_doc.js` EXIT=0 | `node t_refs_ordem.js` EXIT=0 | `node t_rt_abnt.js` EXIT=0 | `node t_tese.js` EXIT=0
  - suite completa do Write: 22/25 EXIT=0. As 3 nao-zero: `t_omml.js` e `t_px.js` (exigem a env var `G` apontando o caminho do playwright - problema de ambiente, nao de codigo) e `t_office.js` (TimeoutError de screenshot - flake, EXIT=0 ao re-rodar)
  - `node --check src/cite.js` OK; `python build.py` -> dist/index.html com 759480 chars
  - Rodada 2 (calibracao ABNT): `node t_refs_normas.js` EXIT=0 - **DOI 10/10, ABNT 10/10, APA 10/10, NUM 10/10**; `t_doc.js`, `t_refs_ordem.js`, `t_rt_abnt.js`, `t_tese.js` todos EXIT=0
  - **Suite completa: 25/25 EXIT=0** (rodada final, com `docx` e `pptxgenjs` instalados e o fallback do `require`). As nao-zero intermediarias eram ambiente, nao codigo: `t_omml`/`t_px` quebravam porque `process.env.G` (caminho do `node_modules`) nao estava definido e os pacotes `docx`/`pptxgenjs` nao estavam instalados; `t_anim`/`t_tese_shot`/`t_office` eram flake de screenshot (`page.screenshot: Timeout 30000ms exceeded`), EXIT=0 ao re-rodar.
  - `graphify update . --force` rodado: 7368 nos, 17807 arestas, 213 comunidades
- Pendencias:
  - (a) o Yuri aponta uma pasta real de PDFs e o Write insere a citacao no texto + gera a lista de referencias de ponta a ponta (criterio de aceite do enunciado) - **UNICO ITEM DO T4 QUE FALTA**
  - (b) a ABNT usa citacao autor-data (NBR 10520:2023) por padrao. Se o Yuri quiser o numerico-autor como padrao da ABNT, o estilo `num` ja cobre.
  - (c) calibracao das 3 normas: as 3 especificacoes (APA 7, Vancouver/ICMJE, ABNT 6023:2025) foram entregues com fonte citada. O que a especificacao marca como "NAO CONFIRMADO" (ex.: forma `[n]` de citacao numerica ABNT, modelo de preprint na ABNT - a norma nao tem) ficou no padrao mais conservador e documentado no codigo.
  - (d) `graphify label` continua pendente (precisa de credencial de LLM + RAM); `graphify update` da pasta do Write rodado no fim das duas rodadas.

### T4 - rodada 2: ambiente de teste consertado

- `testes/t_omml.js:1` - `require(process.env.G+'/docx')` -> `require((process.env.G||__dirname+'/node_modules')+'/docx')`. Sem a env var `G` o require virava `undefined/docx` e o teste morria antes de rodar.
- `testes/t_px.js:1` - mesma correcao para `pptxgenjs`.
- `testes/package.json` - `docx ^9.13.0` e `pptxgenjs ^4.0.1` declarados como dependencia (antes so `playwright`).
- `testes/node_modules/` - instalados `docx` e `pptxgenjs` (faltavam).

## Tarefa 5 - Pipeline buscador de referencias
_Status: LIBERADA - Qualis Engenharias II, tema padrao DEM/Materiais, tema final com o Yuri_

- Resumo: 4 agentes - entrevistador (tema, palavras-chave, periodo, idiomas), buscador (so fontes legais: Periodicos CAPES, Google Scholar, Scopus, Web of Science, BDTD, Catalogo de Teses CAPES, OpenAlex, Unpaywall), avaliador (Qualis A1/A2, citacoes, relevancia), tradutor (resumos PT). Criterio: >=100 artigos, >=10 teses, >=10 dissertacoes, >=5 livros, todos com link valido verificado.
- Pendencias: tema da primeira busca e area do Qualis (provavel Engenharias II/Materiais). Verificar se a skill existente dem-vale-referencias (notas manuais de DEM/Valle/USP) serve de base ou se o pipeline precisa ser generico.

## Log

- 2026-10-20 - arquivo criado, aguardando as 5 tarefas em inbox_vlrm.md.
- 2026-10-20 20:45 - detalhamento das 5 tarefas transcrito para inbox_vlrm.md. Cron de consolidacao restaurado (id 86683d62, :17 de cada hora). T1 com SKILL.md criado; T2-T5 aguardando decisoes do Yuri.

## Decisoes do controlador (qe-flow-2e autorizou em 2026-10-20 21:05)

| # | Tarefa | Decisao | Quem |
|---|---|---|---|
| 1 | T1 | Dispara automaticamente em tarefa nova nao-trivial (alem do comando /entrevista-pre-tarefa) | controlador |
| 2 | T2 | Proposta aprovada pelo controlador vira tarefa; >=3 entradas novas por ciclo, a cada 30 min e ao fim de cada tarefa | controlador |
| 3 | T3 | Codigo dos 3 agentes (leitor/atualizador/verificador) pode ser escrito; a LISTA de producoes, o login e o envio ficam SO com o Yuri | Yuri |
| 4 | T4 | Caminho do Write = C:/Users/yuri/OneDrive/Desktop/Claude/Write (existe); PDFs de teste = artigos open access via Unpaywall em pasta nova de teste | controlador |
| 5 | T5 | Qualis = Engenharias II; tema padrao = DEM/Materiais (derivado do baseline); tema final da busca e fontes em PT ficam com o Yuri | Yuri |

Prazos provisorios: T2 24 h, T4 72 h, T5 1 semana. T1 e T3 sem prazo (T1 precisa so do teste do Yuri).

## Log (continuacion)

- 2026-10-20 21:05 - controlador assumiu o papel de avaliador substituto (ordem do qe-flow-2e), registrou as decisoes acima, liberou T2/T4/T5 para execucao.
- 2026-10-21 09:38 - T4 rodada 2: ABNT recalibrada na 6023:2025 (fonte primaria), bug do DOI sumindo em referencia com URL corrigido, 4+ autores com "et al.", tese com local e data de defesa. Suite 25/25 EXIT=0.
- 2026-10-21 10:45 - T4 rodada 2 fechada no codigo. Grafo do Write atualizado (7372 nos, 17811 arestas, 209 comunidades). Relatorio enviado ao qe-flow-0b (o controlador `omniroute-d6` saiu do mapa; pedi identificacao de quem consolida agora).
- 2026-10-21 10:45 - ambiente de teste consertado: `docx` e `pptxgenjs` instalados, fallback no `require` de `t_omml.js` e `t_px.js`, `package.json` com as dependencias declaradas.
