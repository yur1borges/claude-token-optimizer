# log GN (LAURA) — avaliador intermediário — sessão omniroute-c0

Regra: cada sessão grava no seu próprio `log_<sessao>.md`; o controlador consolida em `log_controlador.md`.
Reporta para: controlador (omniroute-d6) → avaliador final (qe-flow-0b).

Repo: `C:\Users\yuri\OneDrive\Desktop\MESTRADO PPGTIM\DEM\TriboDEM_Studio`

---

## 2026-10-21 — Resposta ao JP: passo dos dentes da caçamba (140 mm vs 200 mm) — FECHADO

O `log_joao.md` (linha "Aguarda o GN") deixou a pergunta aberta: **passo dos dentes da caçamba — 140 mm
(declarado na fonte citada) vs 200 mm (deduzido do layout do código)**. A sessão `omniroute-69` (JP) saiu do
mapa de peers, então a resposta vai por arquivo. Ela está **também** no repo, em
`docs/loop/NOTAS.md` (§ "Achado do GN (21/10/2026)") e em `docs/loop/gn_consolidacao_21out2026.md`.

### Veredito

**O número do código está certo: passo = 200,00 mm.** E o "140 mm" é um **número órfão nas DUAS fontes
citadas** — não é que uma fonte diz 140 e o código diz 200; nenhuma das duas fontes diz 140.

**Prova no código** (`tribodem/pecas_padrao.py`):
- `pecas_padrao.py:115` — o catálogo da caçamba: `"largura": 2000` (mm) e `"n_dentes": 10`.
- `pecas_padrao.py:542` (`def dentes_layout`) e `:556` (`y = -W/2 + W*(k+0.5)/n`) ⇒ **passo = W/n exatamente**.
- ⇒ passo = 2000/10 = **200,00 mm**.
- Medido no artefato `desgaste_por_dente.json` da v9: **9 passos de exatamente 0,2 m** (y = ±0,9 / ±0,7 / ±0,5 /
  ±0,3 / ±0,1 m) — 9 vãos para 10 dentes, confirmando o layout.

**Prova nas fontes** (auditoria já feita, convergente):
- **JP**, 20/10/2026: leu o texto integral de *Minerals* (2021) 11(6), 623 (27 p.) — **ZERO** ocorrências de
  "spacing", "pitch", "140" e "tooth". A frase real da fonte traz **largura 2,0 m com 8–10 dentes**, o que dá
  passo de 200–250 mm, **não** 140 mm. (Com 2,0 m e passo 140 mm exigiria ≈ 14 dentes.)
- **GN**, 21/10/2026: auditei **Li et al. 2017** (DOI `10.3390/ma10050520`, texto integral lido via PMC5459068
  / Europe PMC `fullTextXML`) — **ZERO** ocorrências de "bucket", "excavat*", "shovel", "tooth", "Esco",
  "Ultralok", "pitch". **Não é artigo de caçamba.** Confirma o JP (rodada2/rodada3: "Texto lido integralmente;
  nada reconstruído de memória").

### A contradição que resta (e não é do JP)

`docs/MODELOS_PRIORIDADE.md:21` **já está rebaixado** pelo JP para `[estimativa sem fonte]` (20/10/2026) nos dois
valores (concha e dentes). O que **ainda** está quebrado é a **contradição interna** da linha: ela combina
"8 a 10 dentes" + "passo 140 mm" + "largura 2,0 m", e as três não fecham entre si:

| dentes | largura 2,0 m ⇒ passo | passo 140 mm ⇒ largura | largura 1,4 m ⇒ passo |
|---:|---:|---:|---:|
| 8 | 250 mm | 1,12 m | 175 mm |
| 10 | 200 mm | 1,40 m | 140 mm |
| 14 | 143 mm | 1,96 m | 100 mm |

O passo de 140 mm é compatível com **1,4 m de largura e 10 dentes**, ou com **2,0 m e ~14 dentes** — nenhuma das
duas com a combinação que a linha publica. **A correção que fecha** (uma das três que o JP e a GN já
listaram em `gn_consolidacao_21out2026.md:120-140`):
- (a) manter 2,0 m e corrigir para **14 dentes** a 140 mm (passo 142,86 mm);
- (b) manter 8–10 dentes a 140 mm e **reduzir a largura para ≈1,4 m**;
- (c) rebaixar a linha inteira para `[estimativa sem fonte]`.

**A GN não aplicou (a), (b) ou (c).** `pecas_padrao.py` e `experiments.py` são do Sérgio (proibido para o JP)
e a escolha de modelagem é do Yuri — e note que **(c) é o que o JP já fez**. A GN só mediu e **não** reescreveu
`MODELOS_PRIORIDADE.md:21` por ser um arquivo de fonte do JP.

### O que realmente pesa na caçamba agora (e NÃO é o passo dos dentes)

> **RETIFICAÇÃO (GN, 21/10/2026, rodada de verificação).** Uma versão intermediária deste log afirmava que
> `vazao_media_tph` era um **erro de unidade** (kg/h rotulado como t/h). **Isso estava errado.** `kg/s × 3,6
> = t/h` é a conversão correta: a conferência aritmética fecha exatamente
> (`134306,955 kg / 63,478 s × 3,6 = 7616,8665`, idêntico ao valor gravado) e vale para **todos** os 7 casos
> v9 com massa. A conversão errada era a do meu **primeiro script de recálculo**, que tratava a massa da pilha
> em toneladas. **O defeito real não é de unidade** — é o **override** que descarta a vazão declarada e o
> fato de o caso **ignorar a própria granulometria**. Os números da tabela abaixo estão corrigidos.

A GN mediu as divergências do `V9_cacamba_10dentes_labio_reta` (artefato **GPU**, Chrono DEM-Engine) e a
maior **não** é o passo. Todos os números abaixo foram **recalculados do zero** por
`docs/loop/gn_recalc_cacamba.py` (EXIT=0) a partir dos artefatos v9 — nenhum copiado da NOTAS:

| grandeza | valor medido | referência | desvio |
|---|---|---|---|
| vazão medida | **7616,87 t/h** | 1500 t/h declarados | **5,08x acima** |
| vazão do override (pilha despejada) | **40346,05 t/h** | 1500 t/h | **26,90x acima** |
| volume da caixa do modelo | **5,6998 m³** | 43 m³ da fonte | **7,54x MENOR** |
| d50 do modelo | **127,08 mm** | banda CG declarada 30–50 mm | **2,54x–4,24x** |
| desgaste dos dentes | 21,73 µm/ciclo | lábio 0,395 (55,05x) / concha 0,048 (452,70x) | fonte diz "3x–5x menos" |
| desgaste por carga (dentes) | 3,9144 mm/1000 t | banda 0,1–0,8 | 4,89x–39,1x |
| desgaste por carga (adapters) | 8,0834 mm/1000 t | banda 0,1–0,8 | 10,10x–80,8x |
| v_max | 64,06 m/s (física 14,44) | 14,44 m/s | **4,44x** |
| vazamento real (`diag_vazadas_pct`) | **0,1934 %** | — | — |
| retenção na caixa (`cacamba_retencao_pct`) | 27,0098 % | — | (retenção, **não** vazamento) |

**A origem da vazão é um override, não física.** `yade_worker.py:1227` sobrescreve
`CASO["vazao_tph"] = massa_pilha / t_desp * 3.6` (com `massa_pilha` em **kg**, em `yade_worker.py:1216`:
`math.pi*Rp_**2*Hp/3*0.60*M2["densidade"]`) — a conversão kg/s→t/h é **correta**; o defeito é que o valor
declarado de 1500 t/h é **descartado**. O `Alimentador` (`yade_worker.py:626`) só *lê* o campo, e é criado
**depois** do override (`yade_worker.py:1344` > `:1227`), então consome o valor sobrescrito: 40346,05 t/h.
No caminho **GPU** o valor gravado em `vazao_alvo_tph` é 1500 (o override é do caminho Yade/CPU), e
`vazao_media_tph` = 7616,87 t/h sai de `dem_gpu.py:1072` (`massas.sum()/t_s*3.6`) — **unidade correta**,
pois `massas` está em kg e `3.6` converte kg/s→t/h. Verificado: `134306,955 kg / 63,478 s × 3,6 =
7616,8665` — bate exatamente com o gravado.

**A retenção de 27,01 % NÃO é "razão de vazamento"** — `cacamba_retencao_pct` é material retido na caixa; o
vazamento real é `diag_vazadas_pct` = **0,1934 %**.

**Novo defeito — o caso ignora a própria granulometria.** `testes/realidade.py:30` define
`"distribuicao": "uniform"`, `"diametro_medio_mm": 120.0`, `"escala_cg": 1.0`; e o caso ainda declara
`"peneiras": "10:5;20:30;25:50;31.5:80;40:100"`. Em `experiments.tabela_psd_bruta`
(`tribodem/experiments.py:445-472`) a chave `peneiras` só é lida quando `modo == "sieves"` (`:462-471`); com
`distribuicao = "uniform"` a função cai no `return None` da linha **472** ⇒ **a tabela de peneiras do próprio
caso é descartada**. E `escala_cg` só é aplicado no ramo `PSD_MINERIOS` (`:450-455`), então o
**CG declarado em `docs/MODELOS_PRIORIDADE.md:21` ("Diâmetro médio escalado para 30–50 mm") não é aplicado
neste caso**: o modelo roda 120 mm uniforme, com d50 = 127,08 mm = **2,54x–4,24x** a banda declarada e
**3,18x** o topo da própria tabela de peneiras do caso (40 mm).

E o critério 4 (forma) do caso **sobe** para 6/6 porque o motor GPU **aceitou** `clump4` aqui (4,00
esferas/partícula) — a limitação "só esferas" da defletora é limitação de motor declarada, não escolha.

### Testes

`pytest testes/teste_escala_real.py` → **13 passed in 0.67s** (re-executado nesta rodada, EXIT=0).
`python docs/loop/gn_recalc_cacamba.py` → **EXIT=0** (recalcula **todas** as grandezas da tabela acima a
partir dos artefatos v9; nenhum número copiado da NOTAS).

**Aviso de honestidade:** `testes/teste_escala_real.py:167-183` (`test_cacamba_passo_dentes_sem_fonte`)
**fixa** a divergência em vez de detectá-la — exige *ao mesmo tempo* `all(abs(p-200.0) < TOL)` **e**
`abs(cat["largura"]/140.0 - 14.29) < 0.01`, imprimindo "DIVERGE DECLARADA". Ou seja: o teste passa
**quando a contradição está declarada**; ele não é um detector. O mesmo vale para
`test_defletora_queda_medida` (linhas 118-139), que exige `abs(queda - 9.6774) < 1e-3` e imprime "DIVERGE".

**Pendências que a GN abre para o JP** (a tabela é do AVP; a GN não reprecificou nada):
- **#39** — `docs/MODELOS_PRIORIDADE.md:21`: fechar a contradição "8–10 dentes × 140 mm × 2,0 m" por uma das
  três vias (a)/(b)/(c). O (c) já está feito; falta registrar o porquê e padronizar a linha.
- **#40 (nova)** — `testes/realidade.py:30` + `tribodem/experiments.py:445-472`: a caçamba declara
  `peneiras = "10:5;20:30;25:50;31.5:80;40:100"` mas roda `distribuicao = "uniform"` com
  `diametro_medio_mm = 120.0` e `escala_cg = 1.0`. A tabela de peneiras do caso é **descartada**
  (`return None` em `experiments.py:472`) e o CG declarado em `MODELOS_PRIORIDADE.md:21` (30–50 mm) **não é
  aplicado** — o d50 medido é 127,08 mm (2,54x–4,24x a banda). Ou o caso passa a `distribuicao = "sieves"`
  (com a CG coerente), ou o `escala_cg` passa a valer no ramo `uniform`.
- **#41 (nova)** — `tribodem/yade_worker.py:1227`: o override `CASO["vazao_tph"] = massa_pilha/t_desp*3.6`
  descarta a vazão declarada (1500 t/h) e a substitui por 40346,05 t/h (26,90x). Ou o override passa a ser
  limitado pela vazão-alvo do caso, ou a vazão-alvo deixa de ser gravada em `vazao_alvo_tph` como se fosse
  a referência.

**Arquivos que a GN tocou nesta rodada:** `docs/loop/NOTAS.md` (só acréscimo: a tabela do AVP ficou intacta),
`docs/loop/gn_adendo_p2_21out2026.md` (novo), `docs/loop/gn_recalc_cacamba.py` (novo), este `log_gn.md` (novo).
Backup: `docs/loop/NOTAS.md.bak_gn3`.
**Não** toquei em `pecas_padrao.py`, `experiments.py`, `physics.py`, `minerios.py`, `vida_util.py`, `dem_gpu.py`,
`runner.py`, `yade_worker.py` nem no `.env`.
