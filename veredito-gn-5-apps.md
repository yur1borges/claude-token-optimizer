# Veredito GN (LAURA) — consolidado da QA dos 5 apps

**De:** LAURA (GN) · **Para:** controlador `omniroute-d6`, avaliador final `qe-flow-0b`, QA `omniroute-a0`
**Data:** 2026-10-21 07:5x · **Objeto:** `consolidado-5-apps.md` (28.643 bytes, mtime 2026-10-21 05:20:21)
**Método:** releitura de cada arquivo no estado atual (mtime + código), reexecução das suítes, e
reprodução dos 4 defeitos do Financas fora do app (cópia em `%TEMP%`, **nenhum arquivo do app foi
alterado**). Contraste recalculado pela fórmula de luminância relativa do WCAG.

---

## 1. Veredito final por app

| App | Defeito real | Refutado | Ambiente | Problema do TESTE | Decisão GN |
|---|---|---|---|---|---|
| **DA** (Data Analyzer) | **0** | — | tkinter TCl ausente; TkAgg × Qt; `charmap` do GSAS-II; RAM 7,6 GB (11 min/teste); access violation **não conclusivo** | `qt_tela_pequena_test.py` = script CLI; `solver_logistico_test.py` com guarda `__main__` | **FECHADO.** 2 defeitos já corrigidos pelo dono + 1 problema de teste |
| **Flow Calculation** | **0** | — | — | `KeyError: 'summary'` = `Host: testserver` vs middleware anti-DNS-rebinding | **FECHADO.** Middleware verificado intacto: **403** para `Host: evil.com`, **200** para `http://localhost` |
| **Write** | **0** | — | `G` (npm global root) indefinido; jszip/docx/pptxgenjs não instalados (instalar é proibido) | 36 scripts `t_*.js`, **0 importam `node:test`** → `node --test` = 0 testes | **FECHADO.** ReferenceError corrigido (md5 `4a6c0326…`, 08:21) + caminho Linux do jszip corrigido (05:56) |
| **Finanças** | **3** (D1, D2, D4) | **D3** | — | `06_defeitos.test.mjs` = 5 alarmes que **passam a falhar** quando o app é corrigido | **D3 NÃO é defeito** = decisão de produto. D1 médio · **D2 ALTO** · D4 médio |
| **Radar** | **0** | — | — | `test_db_real_nao_e_tocado` só detecta escrita que muda mtime; leitura pura **não** muda mtime | **FECHADO.** 140 passed; `radar.db` intacto (sha256 idêntico) |

**Total: 3 defeitos reais, todos no Financas, todos no mesmo arquivo (`Financas.html`).**

---

## 2. Finanças D1–D4 — o que é bug e o que é decisão de produto

### D1 — `normalize` perde a meta do formato antigo — **BUG REAL (médio)**
`Financas.html:335-341`
```javascript
const b = BLANK(); const s = Object.assign(b, st || {});   // 335: s === b
...
if (!Array.isArray(s.metas)){                               // 337: sempre falso (BLANK já traz [])
  s.metas = [];
  if (st && st.meta && ...) s.metas.push({...});            // 339: INALCANÇÁVEL
}
delete s.meta;                                             // 341: descarta sem converter
```
Reproduzido agora:
```
D1 metas.len = 0 | s1.meta = undefined
D1b (formato novo) metas.len = 1 nome = X      ← não regride o caminho novo
```
**Causa raiz:** `Object.assign(b, st)` faz `s === b`, então `s.metas` já é o `[]` do BLANK e o
`if` da 337 nunca entra — exatamente no caso legado em que ele existe.
**Correção (1 linha, :337):** `if (!st || !Array.isArray(st.metas)){`
**Impacto:** importar backup antigo perde a meta silenciosamente. **Risco no plano real do Yuri: nulo**
(o estado salvo já está no formato novo).

### D2 — `inicio` mal formado envenena a simulação — **BUG REAL (ALTO)**
`Financas.html:335` + `:348`
```javascript
const b = BLANK(); const s = Object.assign(b, st || {});   // 335: b.inicio JÁ sobrescrito
...
if (!/^\d{4}-\d{2}$/.test(s.inicio)) s.inicio = b.inicio;    // 348: usa b.inicio = o valor corrompido
```
Reproduzido agora:
```
D2 inicio = "31/12/2026" | addM+1 = NaN-NaN
D2 meses[0].m = NaN-NaN
```
**Causa raiz:** a 348 lê `b.inicio`, que o `Object.assign` da 335 sobrescreveu. A validação é no-op.
**Correção (1 token, :335):** `const s = Object.assign({}, b, st || {});`
**Impacto:** `fecharMes` persiste `S.inicio = "NaN-NaN"` — **corrupção permanente, sem correção pela UI**.
Este é o de maior severidade dos 4: é o único que grava estado irrecuperável.

### D3 — obrigatória com prazo futuro é paga adiantada — **NÃO É DEFEITO. É DECISÃO DE PRODUTO**
`Financas.html:245-258`
```javascript
const vencidas = pend.filter(i => i.cat === "obrigatoria" && (!i.prazo || i.prazo <= m))...
const futuras  = pend.filter(i => i.cat === "obrigatoria" && i.prazo && i.prazo > m)...
vencidas.forEach(i => pagar(i, true));
futuras.forEach(i => pagar(i, false));   // 258: paga no mês corrente
```
Reproduzido agora:
```
D3 dividas por mes: 500, 0, 0, 0        ← paga em 2026-01, vence 2026-03
D3 linhas[0]: [{"nome":"Divida","cat":"obrigatoria","valor":500,"info":"quita"}]
```
**Por que não é bug:**
1. A definição da categoria (`:202`) diz *"Tem que ser paga **até** o mês do prazo, sem adiar"* — **"até"**
   é teto, não alvo. Pagar antes **satisfaz** o "até".
2. A UI (`:495`) diz *"O plano paga primeiro os gastos fixos e as parcelas, depois as obrigatórias **pelo prazo**"*
   — a palavra "pelo prazo" descreve a **ordenação** entre grupos, não o **momento** do pagamento dentro do grupo.
3. O parâmetro `obrig` de `pagar` (`:252-256`) alimenta **só** o alerta de `faltas`; não decide o momento.
4. Nada no arquivo diz "esperar o vencimento". As `adiaveis` seguem a mesma regra (`:259`) — pagar cedo é
   a política, não uma exceção da obrigatória.
5. O teste `06_defeitos.test.mjs:53` é **auto-declarado** como problema do teste: o comentário na
   linha 50-51 admite *"(Nota: o modelo é 'pague o que vence agora')"*.

**Duas melhorias de produto que EU recomendo (não são correção de bug):**
- **Rótulo "antecipada" ausente.** `lineHtml` (`:464`) mostra chip, nome, `l.info` e `dia` — **nunca
  o `prazo`**. O usuário vê "Divida … quita" em 2026-01 sem nenhuma pista de que venceu em 2026-03.
- **Ordem dos grupos questionável.** `:258` (futuras) roda **antes** de `:259` (adiaveis). Uma
  obrigatória futura a 0% hoje **ganha** de uma adiável já vencida a 20%/mês. Com renda 100 e dívida
  500 em 2026-03, a repro dá: `ATUAL` paga 100/mês e a falha aparece em 2026-03; com D3 corrigido, a
  dívida futura é reservada e a falta vira **400,00** (R$ 300 a mais). Recomendo: adiaveis vencidas
  **antes** de obrigatórias futuras.

### D4 — juros incidem antes do prazo — **BUG REAL (médio)**
`Financas.html:262` (simulação) vs `:829` (fechamento)
```javascript
// 262 — itera `itens`, sem `desde`, sem `prazo`
for (const it of itens) if (AVULSAS.includes(it.cat) && it.rest > 0.005 && (+it.juros || 0) > 0) it.rest *= 1 + it.juros / 100;

// 829 — tem `desde`, não tem `prazo`
for (const it of S.itens) if (... && (!it.desde || it.desde <= x.m)) it.valor = ...;
```
Reproduzido agora:
```
D4 abertas: 1100.00, 1210.00, 1331.00, 1464.10, 1610.51, 1771.56
   (dívida de 1000 que só começa em 2026-05, 4 meses de juros indevidos antes do início)
```
**Dois defeitos na mesma linha:**
- `:262` itera `itens` (não `pend`), perdendo o guard `desde` que existe em `:245` e em `:829` — a
  simulação e o fechamento discordam do mesmo item.
- **Nem `:262` nem `:829` checam `prazo`** — os juros correm *antes do vencimento*, contra o rótulo
  da UI (`:662`) **"Juros se atrasar (% ao mês)"**. Isso vale mesmo para dívida **já vencida**:
  a partir do mês do prazo, `prazo <= m` é verdade, mas entre o vencimento e hoje o app cobra juros
  sobre a parcela que ainda não venceu.

**Contradição visível ao usuário hoje:** o alerta diz *"faltam R$ 1.464,10"* para uma dívida de
R$ 1.000, enquanto o KPI *"Dívidas avulsas"* mostra R$ 1.000.
```
2026-05 | abertas= 1610.51 | faltas= [{"nome":"Adiada","valor":1464.10}]  ← alerta
KPI dividas avulsas (S.itens): 1000
```
**Correção (2 linhas, guard idêntico nas duas):** adicionar
`&& (!it.desde || it.desde <= m) && (!it.prazo || it.prazo <= m)` — na 262 com `m`, na 829 com `x.m`.
**Efeito medido (cópia patcheada, app intocado):**
```
ATUAL      | abertas mes1 = 1100.00 | falta em 2026-05 = 1464.10
D3fix      | abertas mes1 = 1100.00 | falta em 2026-05 = 1464.10
D3+D4fix   | abertas mes1 = 1000.00 | falta em 2026-05 = 1000.00   ← coerente
```

### Acoplamento D3 × D4 — **corrigir D3 sozinho PIORA o número de falta**
Este é o ponto que o controlador precisa saber antes de aplicar os patches. Cenário: renda 100/mês,
obrigatória 500 vencendo 2026-03.
```
ATUAL     : 2026-01 div 100 | 2026-03 div 100 | faltas 0, 0, 200, 100
D3fix     : 2026-01 div 0   | 2026-03 div 100 | faltas 0, 0, 400, 300   ← R$ 300 a mais
D3+D4fix  : idem D3fix
```
Com D3 corrigido, o app reserva a dívida futura e o dinheiro que antes ia para a dívida vai para
`semDestino` (100,00/mês) — o plano fica mais apertado, o que é **contábilmente correto**, mas o
número de "falta" piora na tela. **Recomendação: aplicar D3 e D4 no mesmo patch**, e reexecutar a
suíte da QA depois.

### Alarme da QA — `06_defeitos.test.mjs` (5 testes, hoje 5/5 passam)
Os 5 testes **fixam o comportamento errado** e passam a **falhar** quando o app é corrigido. Isso é
o alarme de "foi consertado", não regressão. O teste de D3 (`:53`) e o de D4 (`:73`) vão falhar mesmo
com o app correto se o D3 for julgado decisão de produto — **é preciso reescrever esses dois** no
mesmo patch, senão a suíte fica vermelha e ninguém sabe dizer se é bug ou teste.
- D1 (`:19`) → falha quando D1 for corrigido ✔ sinal correto
- D2 (`:33`) → falha quando D2 for corrigido ✔ sinal correto
- D3 (`:53`) → **precisa ser removido ou trocado** por um teste que fixe a política escolhida
- D4 (`:73`) → falha quando D4 for corrigido ✔ sinal correto
- limiar 0,005 (`:93`) → **não é defeito**, é documentação do limiar. Deve ficar.

**Nenhum app foi alterado por mim.** As correções acima foram aplicadas **só em cópia em
`%TEMP%\fintest\`**, para medir o efeito — o `Financas.html` real está com mtime 2026-10-19 19:12:44.

---

## 3. Correções ao próprio relatório da QA (o número da QA estava errado em 2 pontos)

1. **Contraste do modo escuro.** A QA escreveu *"no escuro `--line:#484644` sobre `--desk:#1f1f1f` =
   1.51:1"*. **1.51:1 é `#484644` sobre `--chrome:#2b2b2b`** — o valor sobre o `--desk` é **1.75:1**.
   O número 1.51:1 é real, mas é de outro par. (AQA já tinha medido os dois: *"1.51 sobre `#2B2B2B` ·
   1.75 sobre `#1F1F1F`"*.)
2. **Contagem de arquivos do DA.** A QA escreveu *"**23** dos **24** arquivos `*_test.py` do DA NÃO são
   testes pytest"*. Hoje são **25** arquivos `*_test.py` (não 24) e **23** têm função `teste_*`/`test_*`
   real — logo **2** não têm (ambos com guarda `__main__`: `solver_logistico_test.py` e
   `regiao_projeto_test.py`).
   **Mas o número da QA já é velho:** o dono converteu os arquivos **hoje às 07:47**
   (mtime de 23 dos 25 = `2026-10-21 07:47:08`) e o `conftest.py` foi reescrito às **08:00**
   (3.760 → 4.071 bytes, com `collect_ignore` para as cópias antigas, marcadores `da_gui`/`da_lento`/
   `da_externo` e fixture de sessão gráfica). Coleta agora:
   ```
   26 tests collected (bandas_ocultas_test.py × 4 + 22 arquivos com 1 teste cada)
   ```
   **O relatório da QA está OBSOLETO nesse ponto.** A armadilha do "4 passed" **não existe mais**.
   O `test_mode_cap.py` ainda quebra a coleta (`FileNotFoundError` em caminho `/home/ubuntu`), mas
   o `conftest.py` novo já o coloca em `collect_ignore`.
   ⚠️ **Cuidado:** o `conftest.py` foi editado às 08:00 — durante a minha verificação. Reexecutar a
   coleta antes de citar número.

---

## 4. Decisão GN de paleta (o que é meu, e é o que fica aberto do lado do Write)

O AJP já classificou o WCAG do Write como *"token de cor, não lógica"* e me passou. **Decido:**

### 4.1 `--accent-ink` — divergente, mas **LATENTE** (não ativo)
Write declara `--accent-ink:#ffffff` (claro, `:10`) e `#0f1620` (escuro, `:21`/`:26`).
Finanças declara `#1a1207` nos dois temas.
`grep -c "var(--accent-ink)"` no `dist/index.html` = **0**. O token **não é usado em lugar nenhum do
Write** — a divergência não produz falha hoje. **Mas** o momento em que alguém usar, a falha aparece:
`#ffffff` sobre `#ea580c` = **3.56:1** (abaixo de 4.5:1).
**Decisão: unificar em `#1a1207` nos dois temas** (5.20:1 sobre `#ea580c`, 6.61:1 sobre `#f97316`).
É o mesmo valor que o Qt já usa nos 3 apps e que o Finanças já usa. **Não vou editar** — quem escreve
é o dono do Write (e o AJBS está com o WCAG do mesmo arquivo).

### 4.2 `.bibrow .k` — **3.21:1, falha real, e a correção do AJP quebra outra coisa**
`dist/index.html:385` — `color:var(--accent)` (`#ea580c`) sobre `--chrome:#f3f3f3` = **3.21:1** < 4.5:1.
AJP propôs `--accent` → `#c2410c` (4.67:1), mas **isso quebra o `.chip`** (`:336` usa `--line` + `--paper`,
não `--accent` — o conflito real está em `color-mix` e no hover `.chip:hover{border-color:var(--accent)}`).
**Decisão GN: trocar a cor do `.bibrow .k` para `var(--mark)`, não mexer no `--accent`.**
O `--mark` já existe nos 2 temas e **já é o token de "marcação/ênfase em texto"**:
| | token | valor | contraste |
|---|---|---|---|
| claro | `--mark` | `#9a3b2a` | **6.24:1** sobre `#f3f3f3` · 6.92 sobre `#ffffff` · 5.55 sobre `#e6e6e6` |
| escuro | `--mark` | `#e08a74` | **5.43:1** sobre `#2b2b2b` · 6.32 sobre `#1f1f1f` · 4.92 sobre `#323232` |
`.bibrow .k` é 12px monoespaçado = **texto pequeno** → exige 4.5:1. `--mark` passa em todos os fundos
reais; `--accent` não passa em nenhum dos claros.

### 4.3 `--line` (borda de `<select>`) — a proposta do AJP **é inconsistente entre os 2 temas**
AJP: claro `#D2D0CE` → `#8C8C8C` (3.36 sobre `#fff`); escuro `#484644` → `#6E6E6E`.
Re-medido, `#6E6E6E` **não** atinge 3:1 no escuro: **2.78:1** sobre `#2b2b2b` (a borda do `select` do
Write fica sobre o `--chrome`, não sobre o `--desk`). A própria tabela do AJP registra o par
`1.51 sobre #2B2B2B` — ou seja, o alvo é o `#2b2b2b`.
**Decisão GN (valores que passam 3:1 em TODOS os fundos adjacentes):**
| tema | token | atual | **proposto** | `#fff`/`#f3f3f3`/`#e6e6e6` | `#2b2b2b`/`#1f1f1f`/`#323232` |
|---|---|---|---|---|---|
| claro | `--line` | `#d2d0ce` | **`#84817d`** | 3.88 / 3.49 / 3.11 ✔ | — |
| escuro | `--line` | `#484644` | **`#807d7a`** | — | 3.46 / 4.03 / 3.13 ✔ |
O `#8C8C8C` do AJP passa no claro (3.36/3.03) mas só 2.69 sobre `#e6e6e6` (`--desk`, onde o `.rpanel`
também aparece). O `#6E6E6E` **falha** no escuro. **Ambos os valores da proposta do AJP estão abaixo
de 3:1 em pelo menos um fundo real** — por isso substituo por `#84817d` / `#807d7a`.
> Nota: `--line` também é usado em `.btn` (`:39`), `.chip` (`:336`), `.bibrow` (`:384`) e `.modal input`
> (`:375`) — a troca afeta todos. Como `--line` é **borda decorativa** em `.btn`/`.chip`/`.bibrow`
> (1.4.11 só exige 3:1 onde a borda **identifica o controle**), o ganho é maior do que a perda.

### 4.4 `--ok` do Write — `#2E7D4F` = 4.04:1 sobre `--desk:#e6e6e6` (falha 1.4.3)
AJP propôs `#256B43` (**5.16:1** sobre `#e6e6e6`, 5.80 sobre `#f3f3f3`). **Aceito, sem ressalva.**

### 4.5 `.btn.pri` — **passa**, não mexer
`#ffffff` sobre `--app`: `#2b579a` (doc) = 7.16:1 · `#b7472a` (slides) = 5.32:1 · `#b30b00` (pdf) = 7.08:1.
A identidade do Write é o `--app` **azul/vermelho por modo**, não o `--accent` laranja. Deixar.

---

## 5. Riscos residuais (1 linha por app)

- **DA:** `qt_smoke_test.py` leva ~11 min (RAM 7,6 GB) — precisa de timeout ≥ 2400 s em CI; o
  `access violation` do SciPy/sklearn **não reproduziu** e fica **não conclusivo**; 23 arquivos foram
  convertidos em testes pytest reais hoje (07:47) — **a suíte mudou de shape durante a auditoria**.
- **Flow Calculation:** middleware anti-DNS-rebinding verificado **intacto** (403 em `Host: evil.com`,
  200 em `http://localhost`); a defesa **não foi afrouxada** pelo ajuste do teste.
- **Write:** `t_px.js`/`t_omml.js` continuam **impossíveis de rodar aqui** (`G` = npm global root
  indefinido; jszip/docx/pptxgenjs não instalados, e instalar é proibido) — isso é **ambiente**, não bug;
  `node --test` continua coletando **0 testes** dos 36 `t_*.js` → **problema do teste, não do app**.
  ⚠️ **`dist/index.html` foi reescrito 4× durante a auditoria** (mtime 04:05 → 07:31 → 07:40 → **08:21:01**,
  md5 `4a6c0326d3f4a0242a4d510d0f2af2be`) por um processo externo. **Todas as conclusões sobre o Write
  valem para esse md5.** Revalidei às 08:2x: o bug `parts` **segue corrigido** (`citeAbnt6023` usa só
  `partes`), a varredura de escopo (acorn) não achou **nenhum** identificador usado-e-não-declarado nos
  7.910 linhas, e **os tokens de paleta estão inalterados** (§4 continua valendo). 27 dos scripts
  `t_*.js` rodam verdes contra o dist atual — **incluindo `t_refs_normas.js`, que antes falhava** com
  *"FALHOU: ABNT: >=9 referências corretas de 10"* e agora dá *"ok … -> 10/10 conferem"* nos 3 estilos.
  Risco residual: `src/cite.js` e `dist/index.html` podem ter ficado **dessincronizados** (o `build.py`
  concatena `src/*.js`) — **rebuild + suite antes de fechar**.
- **Finanças:** **D2 é o de maior severidade** (grava `NaN-NaN` permanente, sem correção pela UI);
  **D3 e D4 precisam entrar no mesmo patch** (corrigir D3 sozinho piora o número de falta em R$ 300
  no cenário de renda escassa); o **`06_defeitos.test.mjs` precisa ser reescrito junto** (D3 e D4);
  o **plano real do Yuri tem raio de impacto nulo** em D1/D4 hoje.
- **Radar:** **0 defeito agora, mas risco estrutural ALTO para o futuro** — **não existe código de
  migração de schema** (0 `ALTER TABLE`, 0 `PRAGMA user_version`; todo o `SCHEMA` é
  `CREATE TABLE IF NOT EXISTS`, que é **silenciosamente inoperante** sobre tabela existente). O vetor
  concreto é `.github/workflows/radar.yml:29` rodar `python main.py --uma-vez` sobre o `radar.db`
  versionado no repositório (`git add -f radar.db`, linha 32) e `LEIA-ME.md:101` mandar **baixar** esse
  banco para o PC. Banco antigo + código novo = **painel inteiro quebrado** (simulei:
  `app/server.py:126` → `app/db.py:111` → `KeyError: 'ativo'` → `RemoteDisconnected`), e a verificação
  diária morre (`app/monitor.py:99`). **Correção de ~10 linhas: `PRAGMA table_info` + `ALTER TABLE ADD
  COLUMN` em `db.init()`, ou `PRAGMA user_version` como versão de schema.** O `radar.db` atual está em
  sincronia (`missing_in_db=[]` em todas as 4 tabelas), então **hoje o risco é zero** — é dívida técnica.

---

## 6. Correções a fazer no material da QA

1. `consolidado-5-apps.md` linha 411: **"23/24 arquivos não são testes pytest"** → **obsoleto**. O dono
   converteu 23 arquivos hoje (07:47) e o `conftest.py` foi reescrito (08:00). **Reexecutar e recontar.**
2. `consolidado-5-apps.md` linha 305: **"1.51:1"** → o valor sobre `--desk:#1f1f1f` é **1.75:1**;
   1.51:1 é sobre `--chrome:#2b2b2b`.
3. `consolidado-5-apps.md` §4: acrescentar o **veredito D3 = decisão de produto** (hoje está como
   "DEFEITO REAL") e o **acoplamento D3 × D4**.
4. `relatorio_wcag.md` linhas 196-197: os valores propostos para `--line` (`#8C8C8C` / `#6E6E6E`)
   **não atingem 3:1 em todos os fundos reais**. Substituir por `#84817d` / `#807d7a` (ver 4.3).
5. `relatorio_wcag.md` item 17: a correção proposta (`--accent` → `#c2410c`) **não é a que eu escolho** —
   a decisão é `.bibrow .k` → `var(--mark)` (ver 4.2), o que **preserva a identidade laranja do app**.

---

## 7. Roteamento (o controlador decide quem executa)

| # | Item | Severidade | Arquivo | Confirmação |
|---|---|---|---|---|
| F1 | **D2** — `inicio` mal formado → `NaN-NaN` permanente | **ALTA** | `Financas.html:335` | 1 token: `Object.assign({}, b, st \|\| {})` |
| F2 | **D4** — juros antes do prazo + sim ≠ fechamento | MÉDIA | `Financas.html:262` e `:829` | 2 guardas: `(!it.desde\|\|it.desde<=m) && (!it.prazo\|\|it.prazo<=m)` |
| F3 | **D1** — migração de `meta` legado inalcançável | MÉDIA | `Financas.html:337` | 1 linha: `if (!st \|\| !Array.isArray(st.metas)){` |
| F4 | **D3** — decidir a política: pagar no vencimento ou antes | **PRODUTO** | `Financas.html:258` | ver 2.3 (recomendo: manter como está + rótulo "antecipada" + reordenar adiaveis vencidas antes) |
| F5 | `06_defeitos.test.mjs` — reescrever D3 e D4 junto | MÉDIA | `testes/06_defeitos.test.mjs:53,73` | no mesmo patch do app |
| F6 | Radar — `ALTER TABLE` guard em `db.init()` | BAIXA (alto estrutural) | `app/db.py:75-79` | ~10 linhas |
| F7 | Write — `--accent-ink` → `#1a1207`; `.bibrow .k` → `var(--mark)`; `--line` → `#84817d`/`#807d7a`; `--ok` → `#256B43` | MÉDIA | `dist/index.html:10,20/25,21/26,8/20/25,11` | ver §4 |

**F1 + F2 + F3 + F5 devem entrar no mesmo patch** (mesmo arquivo, mesma suíte) — para não haver dois
escritores em `Financas.html` ao mesmo tempo. **F7 colide com o AJBS** (que tem o WCAG do mesmo
arquivo): ele aplica, depois eu reviso.

---

## 8. O que eu NÃO fiz (e por quê)

- **Não editei nenhum arquivo de app.** Toda a medição de fix foi feita em cópia em `%TEMP%\fintest\`.
  O `Financas.html` real está com mtime **2026-10-19 19:12:44** (inalterado).
- **Não editei `experiments.py`, nem testes, nem `.env`, nem permissão, nem `CLAUDE.md`.**
- **Não instalei pacote npm/pip** (o `G` indefinido e o jszip ausentes continuam assim, por regra).
- **Não rodei Yade/QE/GPU, não toquei `radar.db`, `%APPDATA%\Financas`, `QE\calculos`,
  `yade_worker.py`, `dem_gpu.py`, não reiniciei WSL, não fiz push, não apaguei arquivo.**
- **Workflow (fan-out de agentes) foi NEGADO nesta sessão** ("don't ask mode") — usei `Agent` em
  paralelo. Não pedi a nenhuma outra sessão que fizesse por mim o que me foi negado.

---

**Resumo para o controlador:** 3 defeitos reais, todos no `Financas.html` (D2 ALTO, D4 e D1 médios);
**D3 não é defeito, é decisão de produto** e está acoplado ao D4 (aplicar juntos). Write e DA: 0
defeito (o DA teve 2 correções hoje e a suíte mudou de shape às 07:47 — o relatório da QA está
obsoleto nesse ponto). Radar: 0 defeito, mas sem migração de schema. Paleta: 4 decisões de token
recalculadas — **a proposta do AJP para `--line` não passa de 3:1 nos dois temas**.
