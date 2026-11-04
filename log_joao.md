# log JOÃO (JP) — TriboCAD/geom — sessão omniroute (TriboDEM Studio)

Regra: cada sessão grava no seu próprio `log_<sessao>.md`; o controlador consolida em `log_controlador.md`.
Reporta para: controlador (omniroute-d6) → avaliador final (qe-flow-0b); GN (omniroute-c0) é o avaliador
intermediário dos arquivos de geometria.

Repo: `C:\Users\yuri\OneDrive\Desktop\MESTRADO PPGTIM\DEM\TriboDEM_Studio`

---

## 2026-10-21 — 13:00-14:30 — Rodada 9: **G-10 IMPLEMENTADO** (default do catálogo `malha_liner_mm` = 50)

**Decisão:** ligar o refino do revestimento **no catálogo**, não só no mecanismo. O AVP (21/10/2026) reportou
que o mecanismo existia e estava testado, mas o catálogo entregava `"malha_liner_mm": 0` ⇒ "malha de revestimento
inerte = −3 na rubrica". Mudei o **default** para 50 nos 4 componentes com revestimento.

**Arquivo de produção alterado: só `tribodem/pecas_padrao.py`** (meu). `tribodem/cad.py` **não foi tocado**
(arquivo do GN) — não houve necessidade.

| Linha | Componente | Antes | Depois |
|---|---|---|---|
| `tribodem/pecas_padrao.py:49` | `correia` | `"malha_liner_mm": 0` | **`"malha_liner_mm": 50`** |
| `tribodem/pecas_padrao.py:69` | `transferencia` | `"malha_liner_mm": 0` | **`"malha_liner_mm": 50`** |
| `tribodem/pecas_padrao.py:86` | `chute` | `"malha_liner_mm": 0` | **`"malha_liner_mm": 50`** |
| `tribodem/pecas_padrao.py:118` | `cacamba` | `"malha_liner_mm": 0` | **`"malha_liner_mm": 50`** |

O cabeçalho (`pecas_padrao.py:30-33`) foi reescrito para dizer o que
o número significa (50 = refino ligado; 0 = sem refino, mantém 140–180 mm) e **por que** (o critério
`vida_util._pico_area` agrupa as facetas em células de 100 mm; faceta maior que a célula ⇒ critério inerte).

### Prova numérica de que o refino ATIVA o critério de vida útil por área de inspeção

`vida_util._pico_area` (célula de 100 mm) devolve o **máximo da média** por célula — o critério de troca por
espessura local medida por **ultrassom** numa janela de ~100 mm. Com a malha grossa, a célula leva ~1 faceta ⇒
a "média" **é** a faceta ⇒ o critério devolve o pico de um triângulo de 150 mm, que não é o que o ultrassom mede.

Experimento (sem GPU, sem Yade): parede de revestimento 1,0 × 1,0 m com **hotspot gaussiano de impacto**
(σ = 120 mm), **mesmo desgaste total** nas duas malhas (8 000 µm somados), vida pelo limite de troca de 25 mm:

| Malha | Facetas | Facetas/célula de 100 mm | Pico por faceta | Pico por **área** | Razão área/faceta | Vida |
|---|---:|---:|---:|---:|---:|---:|
| **150 mm** (a de hoje) | 98 | **1,2** | 867,4 µm | 867,4 µm | **1,000** (colapsa no pico da faceta) | **29 h** |
| **50 mm** (o alvo) | 800 | **8,0** | 108,4 µm | 89,4 µm | **0,824** (mede área) | **280 h** |

O desgaste é o mesmo; **a malha decide o que o critério de troca lê**. Na v9, com a malha de hoje, o critério
de inspeção por ultrassom estava **inerte** (e a vida da saia saía em 0,129 h contra 86,4 h da cobertura).

### Custo real (medido, sem GPU/Yade)

- **GPU: nada.** `dem_gpu.py:371-378` já refina toda malha no carregamento ⇒ o nº de triângulos que o
  DEM-Engine carrega é o **mesmo** com ou sem refino no CAD.
- **`dt`: nada.** `dt = tc/20 · FATOR_DT`, `tc` depende só da partícula; integrador **explícito** (nenhuma
  ocorrência de `SetSolverType`/`SetIntegrationType` em `dem_gpu.py`) ⇒ o refino **não cria passos novos**.
- **Custo real: npz e csv.** `desg` é (n_quadros × n_facetas) ⇒ transferência 3,0 → **228,0 MB** (+11,3 s de
  gravação), cacamba 2,0 → **278,8 MB**, chute 1,0 → **116,3 MB**, correia 1,1 → **52,8 MB**;
  `desgaste_mapa.csv` (transferencia) 0,03 → 2,50 MB. Mais a cena da Yade (CPU).
  Disco em C: 60 GB livres (88 % usado) — viável para 4–6 casos, **mas o crescimento é real**.
- O "+10,8 % de tempo" citado antes (5,71 h → 6,33 h) é o **teto pessimista de todo o lote v9** (Yade/CPU +
  IO do npz), **não** o custo de GPU.

### Testes (números de saída)

- `testes/teste_malha_liner.py` — **6/6 OK**. Novo: (4) `test_default_do_catalogo_sai_com_facetas_pequenas`
  (sem passar parâmetro, o STL já sai com lado máximo ≤ 50 mm: 43,8 / 48,3 / 47,9 mm nos 3 revestimentos) e
  (6) `test_aplicar_malha_revestimentos_sem_gpu` (rotina de montagem salva: 3 revestimentos refinados, peças
  não-liner intactas, **original intocada**) — este é o **pedido nº 2 do AVP**.
- Regressão: `teste_escala_real.py` **13/13** · `teste_cad_acoplar.py` OK (16 peças, 7 simuladas, 1 região) ·
  `teste_cad_brep.py` "TriboCAD B-rep ok" · `verificar_montagens.py` **0 problema(s)**.

### §6.1 — ranking G-01..G-17 entregue

Registrado em `docs/CHUTE_ANATOMIA.md` §6.1 e replicado no `NOTAS.md`: rank 1 **G-07**, rank 2 **G-10**
(entregue), rank 3 G-09, rank 4 G-12, rank 5 G-02, rank 6 G-03, rank 7 G-14, … rank 16 **G-11** e
rank 17 **G-01** = **SEM FONTE, bloqueados**.
Sequência: G-10 (feito) → **G-07 (próxima)** → G-12 → G-03 → G-02 → G-09 → G-14 → G-08/G-15/G-17/G-16 →
G-04/G-05/G-06/G-13.

**Registrado no repo:** `docs/loop/rodada9_joao.md` (detalhe) e `docs/loop/NOTAS.md` (linhas 69, 74, 134, 179,
660 + subseção nova "G-10 — default ligado") e `docs/CHUTE_ANATOMIA.md` (linha de G-10 + status da sequência).

**Não feito:**
- **Nenhum npz foi regravado.** A v9 e o CPOD estão intactos.
- **As montagens já salvas** (v9, CPOD) continuam com 140–180 mm: aplicar `cad.aplicar_malha_revestimentos`
  sobre elas **reescreve os STLs da v9** ⇒ **decisão do controlador (omniroute-d6)**, não minha.
- **Nada rodado na GPU** (o CPOD está na GPU) nem Yade, nem lote.
- **Não toquei** `dem_gpu.py`, `runner.py`, `yade_worker.py` (proibidos) nem `experiments.py`, `physics.py`,
  `minerios.py`, `vida_util.py` (Sérgio). **`cad.py` não foi alterado** (GN).
- **Pedido nº 4 do AVP (reavaliar a carga derivada 7 198,2 N se a Laura mudar o par 1045×1045): NÃO
  resolvido** — depende do par novo; não inventei número.
- **3 agentes de pesquisa** (saia / cortina / raspador / grelha / vale) seguem rodando com saída de **0 byte**.
- `chute_mais_correia.tdcad` está com **mix** de `malha_liner_mm` 50 (17 peças) e 0 (13 peças) — **não foi
  regenerada**.

**Riscos:** o crescimento do npz (76× no caso da transferência) precisa entrar na conta de disco do lote v9;
o render (`render.py:273` `Poly3DCollection`, `render_vtk.py:713`) e o `vida_util.video()` leem a malha do npz
e ficam pesados com 104 634 facetas — **não medi** o custo de render. E o **default 50 vale para montagem nova**:
as simulações já em curso (CPOD) usam os STLs antigos.

---

## 2026-10-21 — 04:00-05:00 — Rodada 8: `docs/CHUTE_ANATOMIA.md` + pendência nº 9 ENCERRADA

**Decisão:** entregar a anatomia do chute como documento **auditável**, com nível de evidência explícito por
número (`[verificado no texto completo]` / `[derivado]` / `[SEM FONTE]` / `[código]`). **Não adotei** nenhum valor
sem lastro primário — em especial o "ângulo de vale" de 30°-45°, que circulatei na literatura mas **não** é
auditável nas 6 fontes primárias lidas.

**Motivo:** o pedido do qe-flow-dd (reenviado pelo qe-flow-0b) era "cite tudo, nada inventado, marque
estimado/SEM FONTE onde não há fonte". A busca web disponível neste ambiente devolveu raciocínio de modelo sem
documento (sem URL real) — não é fonte, então **não** a usei. Todo o lastro veio de 6 PDFs primários já em cache
local, lidos no integral.

**Resultado — 1) `docs/CHUTE_ANATOMIA.md` (360 linhas, 9 seções, NOVO):**
- Tabela-mestra: **15 peças internas × (ângulo, dimensão, material, função, fonte)** — capuz/hood, colher/spoon,
  caixa de pedra (rock box) e prateleiras, placas de impacto, defletores, revestimentos (AR400/500, alumina 92 %,
  CCO ≥60 % M₇C₃, borracha 40 Shore A, UHMWPE), cortinas de pó, raspador primário, saia/skirt, guias, calha de
  retorno/dribble, portas de inspeção, grelha, bico de descarga, folga de borda livre de 6 %, spray bars/detectores.
- Esquema em corte (ASCII) do chute com capuz curvo R 1,8 m, colher R 1,6 m, leito morto, saia, cortina,
  raspador, roletes de impacto.
- Seção de ângulos: **parede 65°-70°** (35°-45° p/ minério grosso) e a relação dela com o **ângulo de drawdown /
  atrito interno** do minério; ângulos de Oliveira 2025 (repouso 52,6°/49,3°; deslizamento 36,1°/33,7°;
  drawdown 62,64°; tambor 112°/114°; placas de piloto a 32°/37°/42°). **"Ângulo de vale" (V) = SEM FONTE** —
  nenhuma fonte primária auditada usa o conceito; o que o código tem (`angulo_chapa` 55°,
  `angulo_placa_impacto` 70°) está marcado `[código]`.
- Seção de velocidade: Tabela 1 (queda livre × chute 45/60/70°) e Tabela 2 (V_E para carga a 100 %/50 % de V_B)
  transcritas; **5 critérios** de Ilic; **Opções 1-4** com 1000 / 750 / 150 mm; velocidades medidas 4,9 / **3,2** /
  ≈2,5 / 4,5 m/s contra correia de 3,6 m/s; `N_WB` 1,00/1,00 · 0,63/0,34 · 0,57/0,37 · **0,37/0,15**; regra de
  desgaste 40-50 % de V_B (nunca 50-90 %); Palabora **+300 %** de vida de correia, carvão 11 → 4,5 m/s com
  **−83 %** de energia cinética, curved chute **5×** menos cisalhamento que rock box, Los Pelambres −36 %,
  Ash Grove perna superior **65°** / inferior **70°**.
- §7 lista explícita dos números SEM FONTE (espessuras de liner, ângulo de vale, abertura da grelha, cortina,
  raspador, spray bars).
- §8 referências completas, com **aviso declarado**: BELTCON 11 (Roberts 2001) e o 17º Simpósio ABM (Ilic &
  Hicks 2016) são citados **via** Ilic 2019 — o texto primário **não** foi lido.
- §9: "este documento não altera nenhum arquivo de produção".
- Varredura de caracteres não-portugueses (CJK/fullwidth): **0 restantes** (corrigi 4 tokens que escaparam:
  `帽子`, `碎片`, `離`, `推荐`).

**Resultado — 2) Lacunas do TriboCAD: G-01 a G-17** (com linha exata de `pecas_padrao.py` / `cad.py` /
`physics.py`), no §6 do documento. Prioridade sugerida (não aplicada): **G-07** (critério de velocidade de
carregamento), **G-02** (saia), **G-03** (folga 6 %), **G-09** (liner por peça) têm fonte forte; **G-01**
(vale) e **G-11** (grelha) **não têm** e não podem virar número no código sem lastro.

**Resultado — 3) Pendência nº 9 do NOTAS.md — ENCERRADA (dois blocos):**
- (a) defaults de forma e carga: **7/7 OK** em `testes/teste_assistente_carga_derivada.py` (entregue antes).
- (b) **achado do qe-flow-0b (21/10/2026) corrigido**: `assistente.py:303` (versão anterior) tinha default
  **próprio** de material de disco (`"AISI 1045"`) que sobrescrevia em `_caso()` o par de
  `experiments.padroes()` → **todo** caso do assistente voltava a ser 52100×1045, anulando `experiments.py:516`.
  Correção (arquivo do JP): helper `_materiais_tribometro()` em `assistente.py:106-116` **herda** o par de
  `experiments.padroes()` (sem segundo default); `assistente.py:316-317` usa esse par nos comboboxes;
  `assistente.py:177` faz `mat_vars.clear()` ao trocar de modelo (o `mat_vars` não era limpo e vazava o par do
  modelo anterior). Novo teste `testes/teste_assistente_materiais.py`: **4/4 OK** — pino-disco e esfera-disco
  **52100×52100**, disco-disco **1045×1045**.
- NOTAS.md atualizado: linha da pendência nº 9 → **ENCERRADA**; linha da tabela de divergências → RESOLVIDO.

**Regressão (tudo verde):** `teste_assistente_carga_derivada.py` **7/7 OK** ·
`teste_assistente_materiais.py` **4/4 OK** · `teste_escala_real.py` **13/13 OK** · `teste_cad_acoplar.py` OK
(16 peças, 7 simuladas, 1 região).

**Registrado:** `docs/loop/rodada8_joao.md` (repo) e §2/§3 do NOTAS.md.

**Não feito:**
- Não toquei `experiments.py`, `physics.py`, `minerios.py`, `vida_util.py` (Sérgio) nem `dem_gpu.py`,
  `runner.py`, `yade_worker.py` (proibidos). Não alterei `tribodem/cad.py`.
- Não rodei GPU, Yade nem lote.
- Não apliquei as correções de código das lacunas G-01..G-17: são mudança de geometria/calibração e cada uma
  precisa de teste que prove, com número de saída.
- **3 agentes de pesquisa** (saia/cortina/raspador/grelha/vale · catálogos Martin/Multotec · manual de projeto
  de chute + Roberts BELTCON) seguem rodando, com saída de **0 byte**. Se voltarem com fonte auditável, as
  lacunas correspondentes saem de `SEM FONTE`.
- **Aguarda o GN**: passo dos dentes da caçamba (140 mm vs. 200 mm deduzido do layout) segue aberto.
- **Aguarda decisão do controlador**: se as lacunas G-02/G-03/G-07/G-09 entram nesta rodada ou na seguinte.

**Riscos:** o `CHUTE_ANATOMIA.md` cita BELTCON 11 e o 17º Simpósio ABM **indiretamente** (via Ilic 2019) —
declarado no documento, mas quem quiser o número original precisa do acesso. E o `teste_assistente_materiais.py`
cobre o par herdado e o `_caso()`, **não** a interface Tk (sem tela) — o `mat_vars.clear()` foi verificado por
leitura de código, não por captura.
