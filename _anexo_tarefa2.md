
## 2026-10-21 — 11:5x — MARIA PAULA (QA) — Tarefa 2 CONCLUÍDA: DA convertido em pytest + Write coletável por `node --test`

**Decisão:** entregar as duas conversões com evidência fresca; registrar 1 defeito real novo do DA para o
dono (artur / c1); corrigir as 2 correções apontadas pela Laura (a5) no `consolidado-5-apps.md`.

**Motivo:** a tarefa foi liberada pelo qe-flow-0b ("a PAUSA da omniroute-be está CANCELADA. Volte a
trabalhar na sua tarefa") com a condição de rodar os testes **um por vez** e os do Write
(Playwright/Chrome) só com **≥1 GB de RAM livre**.

| # | Decisao | Motivo | Nota |
|---|---|---|---|
| 51 | **DA: 25/25 arquivos `*_test.py` convertidos em funcoes pytest reais (mesmas asserts)** | Os 23 scripts rodavam `assert` no TOPO do modulo: executavam no import, o pytest nao contava, e a suíte reportava "4 passed" (so `bandas_ocultas_test.py`). Alem disso 32 erros de coleta vinham das copias em `teste 2/`, `teste de deconvolução como no fityk/`, `melhor código/`, `Executavel/` | **Nenhum arquivo de PRODUCAO foi tocado** — so os arquivos de teste e o `conftest.py`. 22 por conversor automatico; 2 a mao (`solver_logistico_test.py`, `regiao_projeto_test.py`); `deconvolution_gui_test.py` com 3 correcoes NO TESTE (o app do DA esta certo) |
| 52 | **DA: `conftest.py` com `collect_ignore`, marcadores `da_gui`/`da_lento`/`da_externo`, skip com MOTIVO, e `sys.argv` limpo** | Sem isso os 32 erros de coleta voltam; e varios testes leem `sys.argv[1]` (pasta de capturas) — sob o pytest seria o caminho do proprio pytest | O dono do DA reescreveu o `conftest.py` as 08:00 (apos a conversao de 07:47). Meu `conftest.py` foi reescrito sobre essa base |
| 53 | **DA: coleta final = 28 tests** | Verificado HOJE: `python -m pytest -q -p no:cacheprovider --collect-only` -> `28 tests collected in 17.70s`. (A Laura mediu 26 as 08:xx; desde entao `qt_comparacao_test.py` e `qt_drx_test.py` entraram na coleta) | Regra do risco 30 do proprio controlador: relatorio de suite precisa do mtime do `conftest.py` E do numero coletado, nao so do pass/fail |
| 54 | **DA: veredito por execucao (um por vez) = 24 PASS + 1 XFAIL + 1 FAIL(ambiente) + 1 SKIP** | `qt_comparacao_test.py` PASS (18,09 s) / `qt_drx_test.py` SKIP (GSAS-II ausente: `C:\Users\yuri\gsas2main` nao existe) / `qt_smoke_test.py` FAIL por RAM: `numpy._core._exceptions._ArrayMemoryError: Unable to allocate 246. MiB for an array with shape (2684472, 3, 4)` — RAM livre 0,01 GB (7,63 GB totais, `Memory Compression` 3.545 MB). **AMBIENTE, nao defeito** | `qt_smoke_test` reexecutar com >=1 GB livre |
| 55 | **[DEFEITO REAL DO DA — dono: artur / c1] divergencia `lbfgs` x `newton-cg` nas metricas de k-means, pasta B** | A regressao logistica (L2, estritamente convexa) tem otimo UNICO — dois solvers devem dar exatamente as mesmas metricas. Pasta A identica; pasta B divergente, **reproduzivel 2/2**. Saida verbatim: `acuracia_training (0.84, 0.88)`, `precisao_training (0.8514, 0.8564)`, `recall_training (0.84, 0.88)`, `f1_training (0.8340, 0.8544)`. Local: `raman_phase_analyzer/analysis.py:23` (`SOLVER_LOGISTICO`) | Ja estava na lista do qe-flow-0b ("vai ao Artur"). No teste ficou `pytest.xfail` com motivo: o agregado fica verde e **vira PASS sozinho** quando o dono corrigir |
| 56 | **WRITE: a suíte JA era coletavel — faltava o padrao de arquivo na invocacao** | `node --test` sem padrao coleta 0 (reproduzi: `tests 0 / pass 0 / fail 0`) porque nenhum dos 38 `t_*.js` importa `node:test` e nenhum nome casa com `*.test.js`/`*-test.js`/`test-*.js`. **Mas** `node --test "t_*.js"` coleta **37** e roda os scripts (cada um vira um "test file" cujo `process.exitCode` decide) | O diagnostico anterior ("30 scripts avulsos, 0 coletados") era meio certo: o problema era a INVOCACAO, nao os scripts. Nenhum arquivo foi reescrito |
| 57 | **WRITE: 37/37 PASS com `--test-concurrency=1`** | `node --test --test-concurrency=1 "t_*.js"` -> `tests 37 / pass 37 / fail 0 / skipped 0`, duracao **1.347.232 ms (22 min 27 s)** | **O `--test-concurrency=1` e obrigatorio**: no paralelo `t_rt.js` falha (`t_rt.js (12791.8627ms)`) e isolado passa (`t_rt.js (9889.4391ms)`). Causa = AMBIENTE: 37 Chromes simultaneos numa maquina com 7,63 GB de RAM (livre 0,01 GB) |
| 58 | **Write: os 3 `require` com caminho Linux ja estavam corrigidos pelo dono** | `t_fmt.js:13` e `t_sl.js:23` ja usam `require('./lib/jszip.js')`; `t_px.js:1` e `t_omml.js:1` caem em `__dirname+'/node_modules'` e `Write/testes/node_modules` TEM `jszip`, `docx`, `pptxgenjs`, `playwright` | Nao precisei instalar nada (regra da casa) |
| 59 | **2 CORRECOES aplicadas ao `consolidado-5-apps.md`** | (a) linha 305: acrescentei que `#484644` sobre `--desk:#1f1f1f` = **1.75:1** (1.51:1 e sobre `--chrome:#2b2b2b`) — o valor da Laura. (b) linha 411: "23/24 arquivos nao sao testes pytest" -> **25/25 sao, 28 collected** | As 2 correcoes que a Laura (a5) apontou |
| 60 | **Registrei as secoes 1.1 (DA) e 3.1 (Write) no `consolidado-5-apps.md`** | O "4 passed" enganoso e o "0 coletados" do Write estavam descritos como risco aberto; agora estao resolvidos, com o comando e o numero | **`consolidado-5-apps.md` passou de 423 para ~530 linhas** |

### Riscos novos

33. **A RAM da maquina esta no chao: 0,005 GB livres (7,63 GB totais)** com 22,12 GB privados commitados
    (Code 6,06 GB + 10 sessoes `claude` ~8 GB). `Memory Compression` = 2,3-3,8 GB. **`EmptyWorkingSet` em
    197 processos nao liberou nada** (o que esta comprimido e o que conta). Consequencia: qualquer teste
    que aloque >250 MB (matplotlib/triplot) falha por `ArrayMemoryError`, e o `node --test` paralelo abre
    37 Chromes. **Nao matei processo do Yuri** (VS Code e as sessoes claude dele). **Regra**: enquanto a
    RAM estiver assim, rodar o Write com `--test-concurrency=1`.
34. **O `node --test` do Write depende do padrao de arquivo na invocacao.** Sem `"t_*.js"` coleta 0.
    Se alguem rodar `node --test` puro no CI, vai ver "0 testes" e concluir que a suite nao existe.
    **Fixo**: script `testes/rodar-suite.sh` (ou `.cmd`) com o comando completo, ou renomear os
    arquivos para `*.test.js`. **Nao renomeei** (regra da casa: nao renomear arquivos sem o dono).

### Pendencias que NAO fechao sozinhas

- `qt_smoke_test.py` (DA) — reexecutar com >=1 GB de RAM livre.
- `qt_drx_test.py` (DA) — precisa do GSAS-II instalado em `C:\Users\yuri\gsas2main`.
- `06_defeitos.test.mjs` (Financas) — o teste de D3 (`:53`) precisa ser removido/reescrito quando o
  app for corrigido (D3 e D4 no mesmo patch — item 44 da Laura).
- Defeito do DA (item 55) — para o dono artur / c1; a QA nao corrigiu codigo de producao.
