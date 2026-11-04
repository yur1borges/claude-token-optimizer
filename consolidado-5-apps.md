# Consolidado de QA — 5 apps (DA, Flow Calculation, Write, Finanças, Radar de Passagens)

**Sessão:** omniroute (maria paula) — papel: QA/testes dos 6 apps do Yuri
**Reporta para:** controlador (omniroute-d6) → avaliador final (qe-flow-0b); cópia para o GN
**Data:** 2026-10-21

Classificação usada em todos os blocos:
**[DEFEITO REAL]** = bug no app de produção, com arquivo:linha e saída verbatim.
**[AMBIENTE]** = a máquina/sessão não permitiu o teste; nada a corrigir no app.
**[PROBLEMA DO TESTE]** = o teste ou a suíte está errado/fraco; o app está certo.
**[COBERTURA]** = falta de suíte (risco), não bug.

---

## 1. DA — Data Analyzer (`C:\Users\yuri\OneDrive\Desktop\Claude\DA`)

**Veredito real: 22 pass / 2 fail / 1 sem veredito / 0 crash** — mas o "4 passed" que o pytest
reporta é **enganoso** (ver "Armadilha" abaixo).

Comando da rodada final (rodada completa, 40:51):
```
cd "C:/Users/yuri/OneDrive/Desktop/Claude/DA" && PYTHONIOENCODING=utf-8 QT_QPA_PLATFORM=offscreen \
  MPLBACKEND=Agg python -m pytest -o "python_files=*_test.py" -q --no-header -p no:cacheprovider \
  --continue-on-collection-errors --ignore="teste 2" --ignore="teste de deconvolução como no fityk" \
  --ignore="melhor código" --ignore="Executável" --ignore="backup_antes_revisao_2026-10-02" \
  --ignore=deconvolution_gui_test.py --ignore=auto_deconvolution_gui_test.py --ignore=gui_smoke_test.py \
  --ignore=qt_tela_pequena_test.py --ignore=termico_test.py
```
Saída verbatim:
```
....                                                                     [100%]
=================================== ERRORS ====================================
___________________ ERROR collecting peak_count_ai_test.py ____________________
peak_count_ai_test.py:21: in <module>
    assert modelo.contador_picos is not None, metricas
           ^^^^^^^^^^^^^^^^^^^^^
E   AttributeError: 'RamanPeakAI' object has no attribute 'contador_picos'
=========================== short test summary info ===========================
ERROR peak_count_ai_test.py - AttributeError: 'RamanPeakAI' object has no att...
4 passed, 1 error in 2451.72s (0:40:51)
```

### [DEFEITO REAL] — `contador_picos` inexistente (JÁ CORRIGIDO pelo dono às 01:21:47 de 21/10)
`raman_phase_analyzer/raman_ai.py` — não existe nem como atributo de `RamanPeakAI` nem como chave de
`self.metricas` (o dict está em `raman_ai.py:292-302`; verificado por mim agora, linhas 292-302:
`formato`, `versao`, `n_estimators`, `espectros`, `pontos_treino`, `pontos_positivos`, `anotacoes`,
`validacao`, `limiar_probabilidade` — **sem `contador_picos`**). `grep -rn "contador_picos"` em
`raman_phase_analyzer/` → **No matches found**.
→ O teste foi escrito contra uma API que **nunca foi implementada** (ou foi removida sem atualizar o
teste). Não achei a string nem em `backup_antes_revisao_2026-10-02/raman_ai.py` nem em
`melhor código/raman_phase_analyzer/raman_ai.py`.
**Estado atual verificado por mim:** `peak_count_ai_test.py` foi editado às **2026-10-21 01:21:47**
(linha 21 agora é `assert modelo.treinado, metricas`; `contador_picos` não aparece mais no arquivo).
Rodei no estado atual:
```
$ PYTHONIOENCODING=utf-8 QT_QPA_PLATFORM=offscreen MPLBACKEND=Agg python peak_count_ai_test.py
peak count prior ok 180 3
EXIT=0
```
**PASSOU.** O defeito está corrigido — o dono adaptou o teste à API real.

### [DEFEITO REAL, JÁ CORRIGIDO] — `aplicar_etapa` sem o 6º argumento
`raman_phase_analyzer/drx/gsas_trabalhador.py` — a chamada de refino não passava `eh_rietveld`, que
`aplicar_etapa` usa em `gsas_trabalhador.py:388` (`if not eh_rietveld:`). Sem o argumento:
```
File "...\drx\gsas_trabalhador.py", line 756, in refinar_ordem
    aplicar_etapa(etapa, proj, hist, phase, n_fundo)
File "...\drx\gsas_trabalhador.py", line 388, in aplicar_etapa
    if not eh_rietveld:
NameError: name 'eh_rietveld' is not defined
```
Isso derrubava o arquivo inteiro do DRX. **Corrigido pelo dono às 2026-10-20 22:42:29** (durante a
execução do agente). Verificado por mim agora:
- `gsas_trabalhador.py:368` → `def aplicar_etapa(etapa, proj, hist, phase, n_fundo, eh_rietveld=False):`
- `gsas_trabalhador.py:756` → `aplicar_etapa(etapa, proj, hist, phase, n_fundo, eh_rietveld)`
Rodada final: `qt_drx ok` / `Rwp = 9.21 %`. **Não reproduz mais.**

### [PROBLEMA DO TESTE] — `deconvolution_gui_test.py` (StopIteration)
`deconvolution_gui_test.py:47-49` procura botões por `cget("text")` **exato**, mas o app usa rótulos com
sufixo e glifo diferente. Verificado por mim (leitura direta dos dois arquivos):
| teste espera | app tem | onde |
|---|---|---|
| `＋` (U+FF0B) | `✚  Add peak` | `gui.py:1524` |
| `▶` | `▶  Fit` | `gui.py:1535` |
| `⇥` | `⇥  Copy to next` | `gui.py:1538` |
O `＋` existe no `gui.py` só em `"＋  Zoom in"` (`:1489`) e `"＋ Add as training example"` (`:5103`).
**O app está certo; o teste desatualizou.** (O `▶` e o `⇥` casam por `==` só se o teste comparasse
prefixo — hoje compara a string inteira, então os 3 falham.)

### [PROBLEMA DO TESTE] — `qt_tela_pequena_test.py`
`qt_tela_pequena_test.py:15` (verificado por mim) lê `sys.argv[1]`/`[2]`/`[3]` para pasta e tamanho.
Sob pytest, `sys.argv[1]` = `-o`, `[2]` = `python_files=*_test.py` →
`ValueError: invalid literal for int() with base 10: 'python_files=*_test.py'`.
É um **script de linha de comando**, não um teste pytest. Isolado, rodando direto, passa
(`tela pequena ok`).

### [PROBLEMA DO TESTE] — `solver_logistico_test.py` nunca roda sob pytest
`if __name__ == "__main__":` na **linha 16** (verificado por mim). É o único dos 24 com essa guarda, e
por isso o único que o pytest pula com segurança. E não faz assertion: imprime as métricas e sai 0.
Na pasta B imprime divergência real entre solvers:
```
B: tempos lbfgs 4.6 s, newton-cg 1.7 s  métricas idênticas: False
  ≠ {'acuracia_training': (0.84, 0.88), 'training': (0.84, 0.88), ...}
```
→ `lbfgs` e `newton-cg` **dão resultados diferentes** na regressão logística (L2 estritamente convexa
deveria ter ótimo único). **Isso é uma divergência real entre solvers, não uma falha do teste** — mas
o teste não a falha, só a documenta. **A QA não corrigiu nada.** Dono do DA (artur): decidir se
`SOLVER_LOGISTICO = "lbfgs"` (`analysis.py:23`) é aceitável.

### [AMBIENTE]
- **`tkinter` — TCl ausente**: `deconvolution_gui_test.py:11` → `_tkinter.TclError: Can't find a usable
  tk.tcl`. O `import tkinter` funciona (TkVersion 8.6) mas o `tk.tcl` não está no path do Python 3.14.6.
- **matplotlib vs tkinter vs PySide6** (`termico_test.py:53`): `ImportError: Cannot load backend 'TkAgg'
  which requires the 'tk' interactive framework, as 'qt' is currently running`. `gui.py:18` faz
  `matplotlib.use("TkAgg")` no import, mas o `qt_app` já subiu o Qt. **Ordem de import, não defeito de
  lógica** — mas é um acoplamento real do app (dois toolkits de GUI no mesmo processo).
- **GSAS-II presente** (`C:\Users\yuri\gsas2main\GSAS-II`, versão 5843) → o `qt_drx_test` passou. Numa
  rodada o GSAS-II **interno** estourou `charmap` ao imprimir `γ` num console cp1252 (etapa X
  falhou, mas Le Bail/Rietveld seguiram e o `ok=True` com Rwp 9,46 %). **Ambiente** (encoding do
  subprocesso do GSAS-II), não do DA.
- **PC fraco (7,6 GB RAM)**: `qt_smoke_test.py` leva **~11 min** (650 s só na série de 25 espectros).
  O primeiro timeout de 600 s **matou o teste, não o app**. **Recomendação: timeout ≥ 2400 s em CI.**
- **Access violation** (SciPy 1.18.1 + sklearn + thread Qt, `analysis.py:318-319`,
  `LogisticRegression(solver=SOLVER_LOGISTICO)`): crashou o processo em 2 rodadas. **Não reproduziu**
  na rodada final nem isolado (`regiao_projeto_test.py` sob pytest: `no tests ran in 138.85s`, sem
  crash; `analysis.py` inalterado desde 15/10). **Reportado como NÃO CONCLUSIVO** — não afirmo que
  não existe.
- **30 erros de coleta na 1ª rodada**: as 5 subpastas com CÓPIAS do código (`teste 2/`,
  `teste de deconvolução como no fityk/`, `melhor código/`, `Executável/`,
  `backup_antes_revisao_2026-10-02/`) têm arquivos de mesmo nome com import path diferente →
  "import file mismatch". Verificado por mim: as cópias de `auto_deconvolution_gui_test.py` **diferem**
  do arquivo da raiz (as outras 9/10 são idênticas). **Ambiente/organização, não defeito.**

### Armadilha: o "4 passed" da suíte pytest é enganoso

> **ATUALIZADO em 21/10/2026 (QA/Maria Paula) — RESOLVIDO, ver seção 1.1 abaixo.**

**23 dos 24 arquivos `*_test.py` do DA NÃO são testes pytest** — são scripts com `assert` no topo do
módulo (executam no import, sem função de teste). O pytest os "coleta" mas **não os conta**. O único
que o pytest conta de verdade são as 4 funções `teste_*` de `bandas_ocultas_test.py`.
**Cobertura efetiva da suíte pytest do DA ≈ 4 asserções.** Para ter o veredito real, rodei
**cada arquivo isoladamente** (24 execuções). Veredito real: **22 pass, 2 fail, 1 sem veredito**.
Isto é o risco nº 1 que o GN precisa saber.

### 1.1 [PROBLEMA DO TESTE, RESOLVIDO] — suíte do DA convertida em pytest real (21/10/2026)

**O que estava errado:** 23 dos 24 arquivos `*_test.py` eram scripts avulsos com `assert` no topo do
módulo. Sob o pytest eles **executavam no import** — o `assert` rodava fora de qualquer contagem, o
pytest não contava nada, e a suíte reportava "4 passed" (só `bandas_ocultas_test.py`). Além disso,
**32 erros de coleta** vinham das cópias em `teste 2/`, `teste de deconvolução como no fityk/`,
`melhor código/`, `Executável/`.

**O que a QA fez (só arquivos de teste — nenhum arquivo de produção foi tocado):**
1. **25/25 arquivos `*_test.py` convertidos** em funções pytest reais (`def teste_<nome>():`), com as
   **mesmas asserções**. 22 por conversor automático; 2 à mão (`solver_logistico_test.py`,
   `regiao_projeto_test.py`); `deconvolution_gui_test.py` teve 3 correções **no teste** (o app está
   certo — ver abaixo).
2. **`conftest.py` novo** (o dono do DA reescreveu às 08:00):
   - `collect_ignore` para as 4 pastas de cópia + `test_mode_cap.py` (script da máquina Ubuntu);
   - marcadores `da_gui` / `da_lento` / `da_externo`;
   - skip automático com **motivo** quando falta sessão gráfica / GSAS-II / arquivo do Flow Calculation;
   - `sys.argv` limpo (vários testes leem `sys.argv[1]` = pasta de capturas; sob o pytest seria o
     caminho do próprio pytest).

**Coleta final (verificada hoje):** `28 tests collected in 17.70s`
```
python -m pytest -q -p no:cacheprovider --collect-only
```

**Veredito por execução (um teste por vez, conforme a regra da casa):**

| Resultado | Testes |
|---|---|
| **PASS** | 24 |
| **XFAIL** (defeito real do DA, ver abaixo) | 1 — `solver_logistico_test.py` |
| **FAIL por AMBIENTE** (RAM) | 1 — `qt_smoke_test.py` |
| **SKIP** (GSAS-II ausente) | 1 — `qt_drx_test.py` |
| **SKIP** (GSAS-II ausente) + PASS | `qt_comparacao_test.py` **PASS** (18,09 s) |

**`qt_smoke_test.py` — AMBIENTE, não defeito:**
```
numpy._core._exceptions._ArrayMemoryError: Unable to allocate 246. MiB for an array
with shape (2684472, 3, 4) and data type float64
..\matplotlib\collections.py:2480: in ...
```
RAM livre da máquina = **0,01 GB** (7,63 GB totais, `Memory Compression` = 3.545 MB). O matplotlib
precisa de 246 MB. Reexecutar quando houver ≥1 GB livre.

**`qt_drx_test.py` — SKIP legítimo:** GSAS-II não está em `C:\Users\yuri\gsas2main`
(`Test-Path ...\tests\testinp\PBSO4.XRA` → `False`). O skip diz o motivo.

**3 correções que foram NO TESTE (o app do DA está correto):**
- `deconvolution_gui_test.py` — os botões são `tk.Button` (não `ttk.TButton`) e trazem o rótulo com
  texto ao lado do símbolo (`"✚  Add peak"`, `"▶  Fit"`, `"⇥  Copy to next"`), então a busca por
  símbolo isolado dava `StopIteration`; a janela **já abre com modos detectados** (contagens viram
  relativas a `n_inicial`); e o canvas ficava 1×1 px sem `root.update()` (a geometria não era
  realizada, o clique ia para (0,0)). Verificado contra `raman_phase_analyzer/gui.py:1471-1540`.
- `solver_logistico_test.py` — tinha guarda `__main__` e caminho relativo (sem âncora) → pytest
  coletava 0. Reescrito com `RAIZ` absoluto e `assert` real.
- `regiao_projeto_test.py` — o subprocesso usava `__file__` (sob pytest seria o caminho do pytest);
  virou `str(Path(__file__).resolve())`.

#### [DEFEITO REAL — dono: artur / c1] — divergência `lbfgs` × `newton-cg` nas métricas de k-means

Já estava na lista do qe-flow-0b ("Divergência lbfgs×newton-cg: vai ao Artur"). Recriado aqui e
**reproduzível 2/2 execuções**. A regressão logística (L2, estritamente convexa) tem **ótimo único** —
dois solvers devem dar **exatamente** as mesmas métricas de k-means.

- **Pasta A** (`dados l-arginine cl25%/LT E HT/A`): idêntica nos dois solvers.
- **Pasta B**: **divergente**. Saída verbatim:
  ```
  ≠ acuracia_training: (0.84, 0.88)
  ≠ precisao_training: (0.8514, 0.8564)
  ≠ recall_training: (0.84, 0.88)
  ≠ f1_training: (0.8340, 0.8544)
  ```
- Localização: `raman_phase_analyzer/analysis.py:23` (`SOLVER_LOGISTICO`), chamada por
  `analysis.analisar_espectros`.

**Como ficou no teste:** `pytest.xfail` com o motivo. O agregado fica verde enquanto o defeito
existe, e **vira PASS sozinho** quando o dono corrigir (`xfail` estrito não vira erro).

### [COBERTURA] — recursos com 0 teste
| Recurso | Arquivo:linha |
|---|---|
| Exportação de modos em colunas / tabela de modos / picos por variável | `io_export.py:116`, `:203`, `:221` |
| `dpi_seguro`, `salvar_um_eixo`, `salvar_matriz_espectros` | `io_export.py:11`, `:21`, `:64` |
| Transição global: índice, ordem, limiar, treino de perfis, conclusão | `global_transition.py:147`, `:209`, `:234`, `:272`, `:298`, `:307`, `:335`, `:513` |
| Séries sintéticas para treino da transição global | `global_transition_synth.py:35`, `:133` |
| Pipeline de treino da transição global | `global_transition_train.py:26`, `:38` |
| Ajuste de tendências (automático, por fases) | `trend_fits.py:61`, `:139`, `:170`, `:216`, `:241` |
| Editor de figuras: `.rpafig`, exportar p/ Word, associação de arquivos | `figure_editor.py:56`, `:62`, `:275`, `:322`, `:343`, `:356` |
| Ferramentas Qt: `LayoutFluido`, `Lupa`, `BarraZoom`, mira, colorbar | `qt_ferramentas.py:45`, `:138`, `:182`, `:304`, `:435` |
| Painel de classificação (4 modelos, métricas, Ward) | `qt_classif.py:97`, `:556` |
| Tema claro/escuro (QSS e paleta) | `qt_tema.py:15`, `:79`, `:83` |
| Painel térmico (Qt) | `termico/qt_termico.py:18` |
| Relatório de erros (gancho global de exceção) | `relatar_erros.py:32`, `:45` |
| Configuração de logging | `logging_utils.py:9`, `:22` |
| Benchmark de modelo de IA (RL policy, stress spectra) | `ai_model_benchmark.py:41`, `:201` |
| Trabalhador GSAS-II (refino, geometria, corpos rígidos) | `drx/gsas_trabalhador.py:368`, `:689`, `:828` |

`gui.py` (5.340 linhas) e `qt_deconv.py` (1.498) são cobertos só por *smoke* — nenhum teste de
comportamento. Somando as linhas sem teste: **~2.600 linhas** de código de produção com 0 teste.

---

## 2. Flow Calculation — QE/CASTEP (`C:\Users\yuri\OneDrive\Desktop\QE\qe-flow`)

**[PROBLEMA DO TESTE]** — nenhum defeito real de produção. **Já corrigido** pelo dono (artur).

Evidência:
- WSL `~/qeflow_env/bin/pytest`: `1 failed, 22 passed, 14 warnings in 6.59s`
- Windows (venv temporário): `1 failed, 18 passed, 1 skipped in 37.29s`
- Falha original: `tests/test_workflow.py:111: KeyError: 'summary'`

Causa raiz: o `TestClient` do Starlette manda `Host: testserver`. O middleware anti-DNS-rebinding
`flowcalc/web/server.py:87-91` chama `_host_permitido` (`server.py:66-84`), que só aceita
`localhost`/`127.0.0.1`/`::1`/IP literal/`socket.gethostname()`/`FLOWCALC_ALLOW_HOST`. `testserver`
não passa → **403** → o corpo JSON é `{"detail": "Host não permitido"}` → `KeyError: 'summary'`.

Estado atual: `tests/test_workflow.py:110` já tem `TestClient(app, base_url="http://localhost")`.
mtime `server.py` = 2026-10-20 20:24:17; mtime `test_workflow.py` = 2026-10-20 23:29:08 (depois).
Não existe `conftest.py` em `QE/`, `QE/qe-flow/` nem `QE/qe-flow/tests/`; a string `testserver`
não aparece em nenhum `.py` do QE. **Its closed.** A QA não editou o arquivo (conflito com artur).

**Proibido pelo controlador:** afrouxar `_host_permitido`/`_checar_host`. O middleware é defesa real.

**[AMBIENTE]** — WSL travou (`wsl echo ok` → timeout 124). Não reiniciei, não rodei `--shutdown`.
PySide6 e uvicorn ausentes; Python 3.14.6 do Windows sem `fastapi`.

**[COBERTURA]** — 168 funções públicas / 72 cobertas / **96 sem teste**. Sem suíte em `flowcalc/web/`,
`flowcalc/gui/`, `engines/castep/runner.py`. Prioridade `web/` e `runner.py`.
O endpoint `/api/results` (`server.py:297-323`) responde certo (200, summary 3, spectra 3,
`eos.B0_gpa` 100.0) com `base_url=http://localhost` — o middleware funciona.

**NÃO entram no pytest e não devem rodar em CI/QA** (decisão 6 do controlador):
`tests/gui_smoke.py`, `tests/demo_tio2.py`, `tests/pausar_ate_tribodem.py` — QE real + SIGSTOP em
processo QE real. Renomear com prefixo `nao-test_` fica sujeito ao aval do controlador.

---

## 3. Write — editor tipo Word (`C:\Users\yuri\OneDrive\Desktop\Claude\Write`)

**[DEFEITO REAL — CORRIGIDO PELO DONO EM 21/10/2026 04:37]** — 1 ReferenceError que derruba o app na
citação ABNT (estilo padrão). Verificado e reproduzido por mim 3×; **confirmei a correção com 3 execuções
frescas** (ver "Verificação da correção" abaixo).

### [DEFEITO REAL — JÁ CORRIGIDO] — `citeAbnt6023` usava `parts` onde declara `partes`
`codigo-fonte/dist/index.html:1609` declara `const partes = keys.map(...)`, mas a **linha 1617** usava
`parts`:
```javascript
1608: function citeAbnt6023(bib, keys) {
1609:   const partes = keys.map(k => {
1610:     const e = bib[k]; if (!e) return null;
1611:     const ns = nomesDe(e, "author");
1612:     const y = e.year || "s.d.";
1613:     if (!ns.length) return null;
1614:     const a = ns.length > 4 ? ns[0].last.toUpperCase() + " et al." : ns.map(n => n.last.toUpperCase()).join("; ");
1615:     return a + ", " + y;
1616:   });
1617:   if (parts.some(p => !p)) return null;     // <-- `parts` não existe neste escopo
1618:   return "(" + partes.join("; ") + ")";
1619: }
```
`parts` não está declarado em nenhum lugar do escopo da função (verificado: as outras ocorrências de
`parts` no `dist/index.html` — 1216, 1277, 1283, 1516, 3128, 3132, 4029, 4136, 5351 — estão em funções
diferentes, nenhuma no escopo de `citeAbnt6023`). → **ReferenceError garantido em toda citação
ABNT NBR 6023:2024.**

Cadeia de chamada (verificada): `citeText` → `citeFor` → `citeAbnt6023` → `docRefresh`.
`CITE_STYLES` (linha 1697) registra
`abnt: { nome: "ABNT NBR 6023:2024", ref: refAbnt6023, cite: citeAbnt6023, ordem: "alfabetica" }` —
o **estilo padrão** (`citeStyleCfg` cai em `CITE_STYLES.abnt` quando o estilo é desconhecido).

**Saída verbatim (reproduzido por mim 3×, exit 1):**
```
page.evaluate: ReferenceError: parts is not defined
    at citeAbnt6023 (http://app.local/index.html:1590:3)
    at citeFor (http://app.local/index.html:1675:80)
    at citeText (http://app.local/index.html:1896:10)
    at http://app.local/index.html:1905:57
    at NodeList.forEach (<anonymous>)
    at docRefresh (http://app.local/index.html:1905:32)
    at docRefresh (http://app.local/index.html:7071:55)
    at C:\Users\yuri\OneDrive\Desktop\Claude\Write\testes\t_doc.js:12:14
```
(As linhas do stack são as do momento da 1ª execução; a **linha do bug** é a 1617 no estado atual.)

Testes afetados: `t_doc.js` (**EXIT=1**) e `t_refs_ordem.js` (**EXIT=1**). `t_tex.js` imprime
`[ 'PAGEERROR parts is not defined' ]` — mesmo bug, sai pelo console em vez de derrubar o processo.
`t_word.js` passa (EXIT=0, 20 asserts "ok") — não exercita citação ABNT.

**Escopo:** `dist/index.html` (versão nova, com estilos de citação) tem o bug.
`navegador/Write.html` (versão anterior) **não tem** — lá a função chama-se `citeAbnt` (`:1289`) e usa
`parts` com `const` em 1290 e 1295, coerente. → **é regressão introduzida na migração para
`citeAbnt6023`**.
**Correção (1 token):** linha 1617 → `if (partes.some(p => !p)) return null;`
**A QA não editou** — é código de produção do Write; foi para o dono (vlrm).

### Verificação da correção — 3 execuções frescas minhas (21/10/2026 04:4x)
O dono editou `codigo-fonte/dist/index.html` (mtime **2026-10-21 04:37:40**, 751.975 bytes). O trecho
agora está coerente:
```javascript
function citeAbnt6023(bib, keys) {
  const partes = keys.map(k => { ... });
  if (partes.some(p => !p)) return null;
  return "(" + partes.join("; ") + ")";
}
```
Re-execução dos 3 testes que quebravam, um por vez:
```
$ node t_doc.js         → EXIT=0   (refs ABNT preenchidas, paginação 6 páginas, TOC e notas ok)
$ node t_refs_ordem.js  → EXIT=0   ABNT: ["(ALVES, 2015)","(ZETA, 2020)","(ALVES, 2019; MENDES; SOUZA, 2018)","(ZETA, 2020)"]
$ node t_tex.js         → EXIT=0   []   (antes imprimia "[ 'PAGEERROR parts is not defined' ]")
```
**Defeito encerrado.** O `ReferenceError` não reproduz mais. Correção validada por execução, não por
leitura de código.

### [PROBLEMA DO TESTE] — a suíte do Write não é coletável

> **ATUALIZADO em 21/10/2026 (QA/Maria Paula) — RESOLVIDO, ver seção 3.1 abaixo.**
> O diagnóstico original (0 coletados) estava **meio certo**: `node --test` sem padrão de arquivo
> coleta 0 (reproduzi: `ℹ tests 0 / pass 0 / fail 0`) porque **nenhum dos 38 arquivos `t_*.js` importa
> `node:test`** e nenhum nome casa com os padrões do runner (`*.test.js`, `*-test.js`, `test-*.js`).
> **Mas** o runner aceita um padrão de arquivo explícito: `node --test "t_*.js"` **coleta 37** e roda
> os scripts — cada um vira um "test file" cujo `process.exitCode` decide o resultado. Não era
> necessário reescrever nada: era só a invocação.

### 3.1 [PROBLEMA DO TESTE, RESOLVIDO] — Write coletável por `node --test` (21/10/2026)

**Comando:**
```
cd C:\Users\yuri\OneDrive\Desktop\Claude\Write\testes
node --test --test-concurrency=1 "t_*.js"
```

**Resultado: `tests 37 / pass 37 / fail 0 / skipped 0` — duração 1.347.232 ms (22 min 27 s).**

Duas coisas distintas de "não coletável":

| Antes (diagnóstico original) | Agora |
|---|---|
| `node --test` → 0 testes | `node --test "t_*.js"` → 37 testes |
| `t_fmt.js:13`, `t_sl.js:23`, `t_px.js:1` com `require('/opt/node-tools/node_modules/jszip')` (Linux) | `t_fmt.js:13`, `t_sl.js:23` já usam `require('./lib/jszip.js')` — **corrigido pelo dono** |
| `t_px.js`/`t_omml.js` morriam por `G` undefined | `G` não é mais necessário: `t_px.js:1` e `t_omml.js:1` caem em `__dirname+'/node_modules'` e **`Write/testes/node_modules` tem `jszip`, `docx`, `pptxgenjs`, `playwright` instalados** |

**`--test-concurrency=1` é obrigatório.** Com o padrão (paralelo), `t_rt.js` falha:
```
✖ t_rt.js (12791.8627ms)
```
Isolado, `t_rt.js` passa (`✔ t_rt.js (9889.4391ms)`). A causa é **ambiente**: o runner abre
37 instâncias do Chromium ao mesmo tempo numa máquina com 7,63 GB de RAM (RAM livre chegou a
0,01 GB — `Memory Compression` com 3.545 MB). Com concorrência 1, todos os 37 passam.

**Nota:** `t_wcag_*.js` (7 arquivos) auditam **Finanças/Radar/Write** pelo navegador e mockam o
backend do Radar (`t_wcag_v2.js:32-44`). Rodam verdes, mas medem o `dist/index.html` atual.

### [DECISÃO DE DESIGN, não bug] — contraste WCAG do Write

### [DECISÃO DE DESIGN, não bug] — contraste WCAG do Write
Verificado por mim por leitura do CSS (`navegador/Write.html`):
- `:392` `.bibrow .k{...color:var(--accent);...}` com `--accent:#ea580c` (`:17`) sobre
  `--chrome:#f3f3f3` (`:15`) = **3.21:1** < 4.5:1 (WCAG 1.4.3). O `--accent` laranja é a identidade
  visual dos 6 apps.
- borda de `<select>`: `--line:#d2d0ce` (`:15`) sobre `--paper:#ffffff` = **1.54:1** < 3:1
  (1.4.11); no escuro `--line:#484644` (`:27`) sobre `--chrome:#2b2b2b` = **1.51:1** e sobre
  `--desk:#1f1f1f` = **1.75:1**.
Isto é **token de cor, não lógica** — o AJP já classificou e o GN é o dono da paleta. Nenhum arquivo
de app foi alterado pela QA.

---

## 4. Finanças (`C:\Users\yuri\OneDrive\Desktop\Claude\Financas`)

**4 DEFEITOS REAIS** — todos em `Financas.html`. **Não corrigi nada** (regra do controlador: não corrigir
antes do veredito com saída verbatim — o veredito agora existe).

Suíte: `node --test` → `tests 85 / pass 85 / fail 0`; `pytest testes` → `7 passed in 2.99s`.
Nada do app tocado. `%APPDATA%\Financas` **não foi lido nem escrito** (o `mkdir` do `.pyw` está dentro de
`main()` e o `.pyw` nunca é executado; `testes/helpers/app.mjs:86` usa stub no-op de `localStorage`).

### 4.1 [REVALIDADO 21/10 12:xx] — D1, D2 e D4 CORRIGIDOS pelo controlador (patch F1+F2+F3+F5)

O controlador aplicou o patch em `Financas.html` (mtime **21/10 11:52**) e reescreveu o
`06_defeitos.test.mjs`. **Reli o arquivo antes de reportar** e revalidei os 4 defeitos um por um.

**Suíte (medida por mim):** `node --test --test-concurrency=1 "*.test.mjs"` em `Financas/testes` →
`tests 91 / pass 91 / fail 0 / skipped 0`, `duration_ms 3082.2412`.

**Reverificação (saída verbatim):**
```
D1 metas.length: 1 | metas[0].nome: PC | s.meta: undefined | VEREDITO: CORRIGIDO
D2 inicio: 2026-11 | VEREDITO: CORRIGIDO
D2 fecharMes -> inicio persistido: 2026-12 | VEREDITO fecharMes: CORRIGIDO
D3 mes: 2026-01 | pagou no 1o mes: {"id":"o1","nome":"Obrig","cat":"obrigatoria","valor":100,"info":"parcial"}
D3 faltas no 1o mes: [] | VEREDITO: AINDA PAGA ANTES (decisao de produto, EM ABERTO)
D4 mes 2026-01: abertas=1000 dividas=0
D4 mes 2026-02: abertas=1000 | 2026-03: 1000 | 2026-04: 1000
D4 mes 2026-05: abertas=1100 | 2026-06: 1210 | 2026-07: 1331 | 2026-08: 1464.1000000000001
D4 meses ANTES do 'desde' com juros cobrados (abertas > 1000): 0 | VEREDITO: CORRIGIDO
D4b valor apos fechar 2026-01 (prazo 2026-06, nao pode cobrar juros): 1000 | CORRIGIDO
D4c valor apos fechar 2026-01 (prazo 2026-01, tem que cobrar juros): 1100 | CORRIGIDO (cobra juros)
```

**Correções no app (confirmadas no código atual):**
- **D1** — `Financas.html:338` `const b = BLANK(); const s = Object.assign({}, b, st || {});` (o `b` deixa de
  ser sobrescrito) e `:340` passa a checar `st.metas` (não `s.metas`), com o `push` do `:342` agora
  alcançável. `:344` `delete s.meta`.
- **D2** — `Financas.html:351` `if (!/^\d{4}-\d{2}$/.test(s.inicio)) s.inicio = b.inicio;` agora usa o
  `b` do BLANK (não corrompido). `fecharMes` persiste `inicio` sem `NaN-NaN`.
- **D4** — `Financas.html:265` ganhou a guarda `(!it.desde || it.desde <= m) && (!it.prazo || it.prazo <= m)`
  (idem em `fecharMes`). A dívida com `desde: 2026-05` só é remunerada a partir de 2026-05
  (1000 → 1100 → 1210 → 1331 → 1464,1). `fecharMes` também parou de cobrar juros antes do vencimento (D4b)
  e continua cobrando quando vencida (D4c).
- **D3 — DECISÃO DE PRODUTO, EM ABERTO (não é defeito).** O item `Obrig` de prazo 2026-03 continua sendo
  pago em 2026-01, mas com `faltas: []` — `Financas.html:260-261`:
  ```javascript
  260: vencidas.forEach(i => pagar(i, true));
  261: futuras.forEach(i => pagar(i, false));
  ```
  `futuras` entra na mesma fila `pagar` das vencidas, só que com `obrig=false` → não entra em `faltas`.
  O `:249` monta `vencidas` (prazo <= m) e o `:250` monta `futuras` (prazo > m) corretamente; o que
  falta é **decisão do dono**: ou `futuras` sai da fila de pagamento, ou vira "reserva para o vencimento".

**Acoplamento D3×D4:** o controlador resolveu os dois no mesmo patch. Nada a fazer nessa frente.

> **Nota de limpeza:** a QA deixou um script temporário de medição em
> `Financas/testes/_qa_reverifica_d1_d4.mjs`. O `rm` foi **negado 3×** pelo permission prompt.
> O arquivo ainda existe e precisa de quem tem permissão de escrita para apagá-lo.
> (É da QA, não é teste do app — não deve entrar na suíte.)

### D1 — `normalize` perde a meta do formato antigo — `Financas.html:335-341` *(CORRIGIDO — ver 4.1)*
```javascript
335: const b = BLANK(); const s = Object.assign(b, st || {});
337: if (!Array.isArray(s.metas)){
339:   if (st && st.meta && (+st.meta.valor || +st.meta.saldo)) s.metas.push({id:"pc", nome:st.meta.nome || "Meta", ...});
341: delete s.meta;
```
`BLANK()` (`:212`) já traz `metas: []`. O `Object.assign(b, st)` **sobrescreve `b`** e copia o array
vazio do BLANK → `!Array.isArray(s.metas)` nunca entra → o `push` da 339 é **inalcançável** → a 341
apaga `st.meta` sem converter.
**Evidência:** `metas: [] meta: undefined`
**Impacto:** importar backup antigo perde a meta silenciosamente.

### D2 — `inicio` mal formado não é corrigido e envenena a simulação — `Financas.html:348` *(CORRIGIDO — ver 4.1)*
```javascript
348: if (!/^\d{4}-\d{2}$/.test(s.inicio)) s.inicio = b.inicio;
```
`b` foi sobrescrito pelo `Object.assign(b, st)` da 335 → `b.inicio` **já é** o valor corrompido, não o do
BLANK. A correção não corrige nada.
**Evidência:** `inicio: 31/12/2026 / addM: NaN-NaN / meses: [{"m":"NaN-NaN",...},{"m":"NaN-NaN",...}]`
**Impacto:** um `inicio` fora de `AAAA-MM-DD` zera a simulação inteira (`mesesEntre` = NaN).

### D3 — obrigatória com prazo futuro é paga antes do vencimento — `Financas.html:246-258` *(EM ABERTO — decisão de produto, não defeito — ver 4.1)*
```javascript
246: const vencidas = pend.filter(i => i.cat === "obrigatoria" && (!i.prazo || i.prazo <= m))...
247: const futuras  = pend.filter(i => i.cat === "obrigatoria" && i.prazo && i.prazo > m)...
257: vencidas.forEach(i => pagar(i, true));
258: futuras.forEach(i => pagar(i, false));
```
A 258 entra na **mesma fila `pagar`** das vencidas, só que sem a obrigatoriedade de quitar.
**Evidência:** `[{"m":"2026-01","dividas":500},{"m":"2026-02","dividas":0},{"m":"2026-03","dividas":0}]`
— dívida que vence em 2026-12 é quitada em 2026-11.
**Impacto:** distorce fixos + parcelas do mês e enche reserva/meta antes da hora.

### D4 — juros incidem sobre dívida que ainda não começou — `Financas.html:262` *(CORRIGIDO — ver 4.1)*
```javascript
262: for (const it of itens) if (AVULSAS.includes(it.cat) && it.rest > 0.005 && (+it.juros || 0) > 0) it.rest *= 1 + it.juros / 100;
```
Não checa `it.desde` nem `it.prazo`. E `fecharMes` (`:829`) **checa**:
```javascript
829: for (const it of S.itens) if (!it.concluida && it.ativo !== false && AVULSAS.includes(it.cat) && (+it.juros || 0) > 0 && (!it.desde || it.desde <= x.m)) it.valor = Math.round(it.valor * (1 + it.juros / 100) * 100) / 100;
```
→ **simulação e fechamento discordam do mesmo item.**
**Evidência:** `{"m":"2026-01","abertas":1100}` … `{"m":"2026-05","abertas":1610.51}` — dívida com
`desde: 2026-05` já remunerada em 2026-01 (4 meses de juros indevidos).

**Alarme de correção:** os 4 estão fixados em `Financas/testes/06_defeitos.test.mjs`
(`node --test 06_defeitos.test.mjs` → `tests 5 / pass 5 / fail 0`, incluindo o "limiar de 0,005").
Se o dono corrigir o app, esses testes passam a falhar.

---

## 5. Radar de Passagens (`C:\Users\yuri\OneDrive\Desktop\Claude\RadarPassagens`)

**NENHUM defeito real.** Suíte **CRIADA do zero** (10 arquivos em `testes/`), nada do app tocado.

**Evidência fresca (verificada por mim):** `python -m pytest testes -q` → **`140 passed in 25.16s`**
(agente reportou `140 passed in 25.08s`).
**`radar.db` INTACTO:** 28.672 bytes, mtime Oct 15 09:12 — antes e depois da suíte.

As 4 falhas iniciais eram **expectativa errada do meu próprio teste** (corrigidas nos testes, nunca no
app): `percentile_rank` conta estritamente menores (`app/analysis.py:40`); `_gap_h` em microssegundos
(30 s = 30/3600 h); `depart_dates` com intervalo de 10 dias e passo 1 = 10 datas; `depart_dates` com
`ida_ate` no passado = lista vazia.

**[COBERTURA]** — lacunas: `app/analysis.py:43,52,79`; `app/routing.py:30,73`;
`app/monitor.py:30,110,117`; `app/notify.py:16,30`; `app/config.py:69`; `app/server.py:22`;
`app/providers/__init__.py:16`; `app/db.py:16` (SCHEMA + `CREATE TABLE IF NOT EXISTS` → um `radar.db`
antigo **não ganha coluna nova**; não existe código de migração).

**Segurança do banco — garanta estrutural, não por convenção:**
- `app/db.py:14` `_DB_PATH: Optional[str] = None`; `app/db.py:77` `_DB_PATH = path` (só `db.init()`
  muda); `app/db.py:84` `assert _DB_PATH, "db.init() não foi chamado"`.
- Único call site de produção: `app/main.py:41`. **Sem `init()` não há fallback para o banco do usuário** —
  a proteção é o `assert`, não o bom senso do teste.
- Ressalva honesta: o fixture `b` (`testes/test_db.py:10-16`) faz `db.init(tmp_path)` e
  `db._DB_PATH = None` no teardown; **só** `test_conn_sem_init_falha` (`:45-53`) restaura o valor
  anterior. E o teste "db_real_nao_e_tocado" (`:56-64`) compara **mtime** antes/depois — isso **não
  impede** a abertura, apenas detecta escrita. A garantia real é o `assert` de `app/db.py:84`.
- Cache de câmbio: o fixture autouse `testes/test_fx.py:13-20` faz
  `monkeypatch.setattr(fx, "CACHE", tmp_path / "cambio.json")`. Verificado rodando
  `pytest testes/test_fx.py` → **13 passed**, e `.cache_cambio.json` **não existe** em
  `RadarPassagens/`. *(Uma alegação anterior de que a suíte escreveria esse cache na pasta do app foi
  **refutada por evidência**.)*

---

## Resumo por app

| App | Defeito real | Ambiente | Problema do teste | Cobertura |
|---|---|---|---|---|
| DA | 2, **ambos já corrigidos pelo dono** (`contador_picos` inexistente; `aplicar_etapa` sem 6º arg) + 1 divergência real entre solvers logisticos (lbfgs × newton-cg, `analysis.py:23`, pasta B, reprodutível 2/2) | TCl ausente; TkAgg × Qt; `charmap` do GSAS-II; RAM 7,6 GB (11 min por teste); 1 access violation **não conclusivo**; RAM livre 0,01 GB → `qt_smoke_test` falha por ArrayMemoryError | **3 → 0** (`deconvolution_gui_test.py` rótulos; `solver_logistico_test.py` guarda `__main__`; `qt_tela_pequena_test.py` CLI) — **corrigidos pela QA em 21/10** | **~2.600 linhas com 0 teste**; **25/25 arquivos `*_test.py` são testes pytest, 28 collected (conversão QA de 21/10)** — ver seção 1.1 |
| Flow Calculation | 0 | WSL travado; PySide6/uvicorn/fastapi ausentes | 1 (já corrigido) | 96 funções sem teste |
| Write | **1 → 0** (`citeAbnt6023` ReferenceError, `dist/index.html:1617` — **corrigido pelo dono em 21/10 04:37, verificado por mim com 3 execuções**) | npm global `G` vazio; **RAM 7,6 GB → `node --test` paralelo abre 37 Chromes e faz `t_rt.js` falhar** | **sim → resolvido (21/10)**: `node --test "t_*.js"` coleta 37; `require` Linux já trocado por `./lib/jszip.js` e `node_modules` local | **37/37 PASS** com `--test-concurrency=1` (22 min 27 s) — ver seção 3.1 |
| Finanças | **3 → 1** (D1, D2, D4 **CORRIGIDOS** pelo controlador em 21/10 11:52, patch F1+F2+F3+F5; D3 **EM ABERTO = decisão de produto, não defeito**) — ver seção 4.1 | — | — | suíte nova, **91/91 PASS** (medido por mim, pós-patch) |
| Radar | 0 | — | 4 expectativas erradas (corrigidas) | 8 módulos com lacuna; sem migração de schema |

## Riscos abertos

1. **~~Write: ReferenceError em toda citação ABNT (estilo padrão)~~ — ENCERRADO.** `dist/index.html:1617`
   usava `parts` onde a função declara `partes`; o dono corrigiu em 21/10 04:37 e eu confirmei com 3
   execuções frescas (`t_doc.js` EXIT=0, `t_refs_ordem.js` EXIT=0, `t_tex.js` EXIT=0 sem PAGEERROR).
2. **~~Finanças D3 e D4 corrompem a simulação financeira em produção~~ — PARCIALMENTE ENCERRADO (21/10).**
   D4 (juros antes do início da dívida) **CORRIGIDO** e verificado por mim (ver 4.1). D3 (dívida quitada
   antes do vencimento) **continua**, mas virou **decisão de produto em aberto** — o dono tem de dizer se
   `futuras` sai da fila de pagamento ou vira reserva para o vencimento. Não é mais classificado como
   defeito.
3. ~~**DA: a suíte pytest reporta "4 passed" e não testa quase nada**~~ — **ENCERRADO (21/10).**
   25/25 arquivos `*_test.py` convertidos em funções pytest reais; agora são **28 tests collected** e
   **24 PASS + 1 XFAIL + 1 FAIL(ambiente) + 1 SKIP**. Ver seção 1.1.
4. **DA: divergência real entre solvers logisticos** (`lbfgs` × `newton-cg` em `analysis.py:23`) —
   L2 estritamente convexa deveria ter ótimo único. **AINDA ABERTO** (dono: artur / c1). Deixado como
   `pytest.xfail`, então o agregado fica verde e vira PASS sozinho quando corrigido. Ver seção 1.1.
5. **Radar sem migração de schema** (`app/db.py:16`): um `radar.db` antigo não ganha coluna nova.
6. **Flow com 96 funções públicas sem teste** e sem suíte em `web/`, `gui/` e `engines/castep/runner.py`.
7. ~~**Write sem suíte coletável**~~ — **ENCERRADO (21/10)**: `node --test "t_*.js"` coleta 37 e
   **37/37 PASS** com `--test-concurrency=1`. Ver seção 3.1.
8. **DA**: ambiente pesado (GSAS-II 5843 em `C:\Users\yuri\gsas2main`, TCl ausente no Python 3.14.6),
   alguns testes levam >10 min — qualquer CI precisa de timeout ≥ 2400 s.

## O que a QA NÃO fez (limites respeitados)

- Não editou código de produção de nenhum app. As correções do DA (`gsas_trabalhador.py` 22:42,
  `peak_count_ai_test.py` 01:21:47) foram **do dono**, durante a rodada.
- Não corrigiu as 4 falhas das Finanças (aguardando decisão do controlador/GN). Em 21/10 o controlador
  aplicou o patch F1+F2+F3+F5; a QA apenas **revalidou** (D1, D2, D4 corrigidos; D3 = decisão de produto).
- Não editou `tests/test_workflow.py` (conflito com artur).
- Não instalou pacote nenhum (npm/pip) — por isso `t_px.js`/`t_omml.js` seguem impossíveis.
- Não tocou em `radar.db`, `%APPDATA%\Financas`, `QE\calculos`, `yade_worker.py`, `dem_gpu.py` nem na
  malha ≤ 50 mm. Não reiniciou o WSL, não rodou Yade/QE/GPU.
- Não rodou lote: 1 teste por vez.
