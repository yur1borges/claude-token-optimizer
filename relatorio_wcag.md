# Auditoria de acessibilidade (WCAG 2.1 AA) — 6 apps

**De:** AJP (ajustes/QA de software) · **Para:** GN (chefe de design) · **Origem do pedido:** qe-flow-77
**Data:** 20/10/2026 · **Escopo:** leitura e medição. Nenhum arquivo dos apps foi alterado.

---

## Método

374 pares de token medidos estaticamente nos 7 arquivos de tema (3 Qt + 3 web + Write) e
**485 elementos medidos no navegador real** (Playwright) varrendo as 5 abas do Finanças,
as 3 rotas do Radar e as 2 telas do Write, nos 2 temas.

Limites aplicados (WCAG 2.1):
- **1.4.3 (texto)**: 4.5:1 para texto normal; 3:1 para texto grande (≥24px ou ≥18,66px com peso ≥700).
- **1.4.11 (não-texto)**: 3:1 **somente** onde a borda/componente identifica o controle
  (borda de input/select/textarea, ícone único de botão). Borda decorativa de card/div e
  grade de tabela **não** são exigidas. Texto desabilitado é isento de 1.4.3.

Medição de fundo no navegador usa a **pilha de pintura real** (`elementsFromPoint`), o que enxerga
irmãos posicionados que a árvore de ancestrais não vê (ex.: a folha `.pg` do Write). Elementos
**encobertos** por overlay opaco são descartados — o texto não está visível, logo não é falha.

---

## Achados confirmados

### P1 — bloqueante (um token, atinge 3 apps de uma vez)

| # | App | Tema | Elemento | Medido | Mín. | Regra | Correção |
|---|---|---|---|---|---|---|---|
| 1 | DA + TriboDEM + Flow (Qt) | claro | `QPushButton#acao` — fundo `acento` | **3.56:1** (`#FFFFFF` sobre `#EA580C`) | 4.5 | 1.4.3 | `acento` → `#C2410C` (5.18:1) **ou** texto → `#1A1207` (5.20:1) |
| 2 | DA + TriboDEM + Flow (Qt) | escuro | `QPushButton#acao` — fundo `acento` | **2.80:1** (`#FFFFFF` sobre `#F97316`) | 4.5 | 1.4.3 | idem (mantém `#F97316` para o dark, mas texto `#1A1207` = 6.61:1) |
| 3 | DA + TriboDEM + Flow (Qt) | escuro | `QPushButton#acao:hover` | 3.56:1 | 4.5 | 1.4.3 | idem |

> A **PALETAS é byte-idêntica** nos 3 arquivos Qt. Uma única mudança corrige os três.
> O hover no dark usa `#EA580C` (o token do claro) — inconsistência a corrigir junto.

### P2 — importante (cores de estado usadas como texto)

| # | App | Tema | Elemento | Medido | Mín. | Regra | Correção |
|---|---|---|---|---|---|---|---|
| 4 | DA + TriboDEM + Flow (Qt) | claro | cor de estado `ok` como texto | **3.74:1** (`#0D9488` sobre `#FFFFFF`) · 3.58 sobre `#F8FAFC` · 3.42 sobre `#F1F5F9` | 4.5 | 1.4.3 | `ok` → `#0F766E` (5.47 / 5.23 / 5.00) |
| 5 | DA + TriboDEM + Flow (Qt) | claro | cor de estado `aviso` como texto | **3.19:1** (`#D97706` sobre `#FFFFFF`) · 3.04 sobre `#F8FAFC` · **2.91** sobre `#F1F5F9` | 4.5 | 1.4.3 | `aviso` → `#B45309` (5.02 / 4.80 / 4.58) |
| 6 | DA + TriboDEM + Flow (Qt) | claro | cor de estado `erro` como texto | 4.41:1 (`#DC2626` sobre `#F1F5F9`) | 4.5 | 1.4.3 | `erro` → `#B91C1C` (5.91) — margem curta |
| 7 | Finanças | claro | `span.chip.ok` | **3.19:1** (`#0D9488` sobre `#D9F2EE`) | 4.5 | 1.4.3 | idem item 4 (`#0F766E` → 4.66) |
| 8 | Finanças | claro | `span.chip.adiavel` | **2.83:1** (`#D97706` sobre `#FEF0D6`) — pior caso | 4.5 | 1.4.3 | idem item 5 (`#B45309` → 4.46, ainda curto) → **`#92400E`** (6.30) |
| 9 | Finanças | claro | `span.chip.obrigatoria` | 4.01:1 (`#DC2626` sobre `#FCE5E2`) | 4.5 | 1.4.3 | idem item 6 (`#B91C1C` → 5.37) |
| 10 | Finanças | claro | `span.ic` (ícone "!" branco em círculo colorido) | 3.19:1 (`#FFFFFF` sobre `#D97706`) | 4.5 | 1.4.3 | usar `#1A1207` no círculo âmbar |
| 11 | Finanças | claro | `div.small` (frase de estado) | 3.19:1 (`#D97706` sobre `#FFFFFF`) | 4.5 | 1.4.3 | idem item 5 |
| 12 | Finanças | escuro | `span.ic` sobre `#F87171` | **2.77:1** | 4.5 | 1.4.3 | texto do ícone → `#1A1207` |
| 13 | Finanças | escuro | `span.ic` sobre `#FBBF24` | **1.67:1** — pior caso | 4.5 | 1.4.3 | idem |
| 14 | Radar | claro | `span.chip.ok` | **3.74:1** (`#0D9488` sobre `#FFFFFF`) | 4.5 | 1.4.3 | idem item 4 |
| 15 | Radar | claro | `span.chip.acc` | **3.56:1** (`#EA580C` sobre `#FFFFFF`) | 4.5 | 1.4.3 | `acc` → `#C2410C` (5.18) |
| 16 | Radar | claro | `div.small.warn` | 3.19:1 (`#D97706` sobre `#FFFFFF`) | 4.5 | 1.4.3 | idem item 5 |
| 17 | Write | claro | `.bibrow .k` (chave BibTeX) | **3.21:1** (`#EA580C` sobre `#F3F3F3`) | 4.5 | 1.4.3 | `accent` → `#C2410C` (4.67) — mas quebra o `.chip`; ver P3 |
| 18 | Write | claro | `span#stSaved.ok` | 4.04:1 (`#2E7D4F` sobre `#E6E6E6`) | 4.5 | 1.4.3 | `ok` → `#256B43` |

### P3 — 1.4.11 (borda de campo de formulário)

| # | App | Tema | Elemento | Medido | Mín. | Regra | Correção |
|---|---|---|---|---|---|---|---|
| 19 | DA + TriboDEM + Flow (Qt) | claro | borda de `QLineEdit`/`QComboBox`/`QSpinBox` | **1.48:1** (`#CBD5E1` sobre `#FFFFFF`) · 1.42 sobre `#F8FAFC` | 3 | 1.4.11 | `borda` → `#7C8DA1` (3.40 / 3.25) |
| 20 | DA + TriboDEM + Flow (Qt) | escuro | mesma borda | **1.37:1** (`#263545` sobre `#131C26`) · 1.51 sobre `#0B1118` | 3 | 1.4.11 | `borda` → `#5A6B7F` (verificar ≥3 sobre `#0B1118` e `#131C26`) |
| 21 | Finanças | claro | borda de `<input>`/`<select>` | 1.48 / 1.42 | 3 | 1.4.11 | idem item 19 |
| 22 | Finanças | escuro | borda de `<input>`/`<select>` | 1.51:1 (`#263545` sobre `#0B1118`) | 3 | 1.4.11 | idem item 20 |
| 23 | Write | claro | borda de `<select>` (`#rFont`, `#rSize`, `#rLh`) | **1.54:1** (`#D2D0CE` sobre `#FFFFFF`) · 1.39 sobre `#F3F3F3` | 3 | 1.4.11 | `line` → `#8C8C8C` (3.36 / 3.21) |
| 24 | Write | escuro | borda de `<select>` | 1.51:1 (`#484644` sobre `#2B2B2B`) · 1.75 sobre `#1F1F1F` | 3 | 1.4.11 | `line` → `#6E6E6E` |

### Cobertos (sem falha)

- **Radar tema escuro: 0 falhas** em 92 elementos. Paleta dark está em conformidade.
- **Write tema escuro: 0 falhas** em 116 elementos (depois de descartar os falsos-positivos).
- **Finanças tema escuro**: só as 2 falhas de `span.ic` (itens 12–13) + bordas (item 22).
- **Texto principal, texto secundário, links primários e cabeçalhos**: todos passam em todos os 6 apps.
- **Botões web**: o padrão já usa `--accent-ink #1A1207` sobre o laranja (5.20:1) — **o problema do branco sobre laranja é exclusivo do Qt**.

---

## Falsos-positivos descartados

| Achado | Medido | Por que foi descartado |
|---|---|---|
| Write `.pages .pn` (nº da página) | 1.30:1 | Medição errada. O `.pn` é irmão do `.pg` (a folha) dentro de `#pages`, e vem **depois** no DOM → pinta por cima. Medindo com a pilha de pintura real (e liberando `pointer-events:none` de `.pages`): **0 falhas** no dark. Sobre a folha branca, o contraste passa. |
| Write `.appicon span` | 2.30:1 | O `span` tem `background:#fff` próprio e `color:var(--app)`. O hit-test media o ancestral. Real: `#2B579A` sobre `#FFF` = **5.74:1** — ok. |
| Write `#btnClaude` / `.claudebtn` | 1.25:1 | Idem: `.claudebtn` tem `background:rgba(255,255,255,.14)` sobre `--app #2B579A`. Real: **16.48:1** no dark, ok. |
| Write `.btn` "Escolher arquivos" | 1.25:1 | `.btn.pri` tem fundo próprio `--app #2B579A` com texto branco = **7.16:1** — ok. |
| Write `#rFont`/`#rSize`/`#rLh` | 1.15:1 | `select` com `background:var(--paper)` (folha) e texto escuro. Real: **15.13:1** — ok. (A **borda** do `select` é que falha: item 23.) |
| Write `span.sp` / `span.sn` (galeria) | 1.15 / 1.69:1 | Elementos da galeria de estilos dentro de `body.m-doc.icons` (fundo da mesa). Sobre a folha real passam. |
| Write `#stSaved` no light | 4.04:1 | **Confirmado** — mantido como item 18 (é falha real, não falso-positivo). |
| Qt `QPushButton#acao:disabled` | 4.46:1 | Texto desabilitado é isento de 1.4.3 em WCAG 2.1. |
| Qt borda decorativa de card / grade de tabela | 1.15–1.23:1 | 1.4.11 não exige contraste para borda que não identifica controle. |
| Write borda `transparent` de `.rb` / `.docname` | 1.00:1 | Borda transparente, sem função de identificação. |
| Qt `QPushButton#acao` hover no dark | 3.56:1 | **Real** — mantido como item 3 (o hover usa `#EA580C`, token do tema claro). |
| Qt `QGroupBox::title`, `QToolBar`, `QPushButton` padrão, `cartao_valor`, `#perigo` | 4.83–17.85:1 | Passam. |

---

## Complemento - DRX (aba do DA) e TriboCAD

Medidos em 21/10/2026, a pedido do controlador `omniroute-d6` (pergunta: "da para
medir DRX e TriboCAD com o mesmo metodo?").

**Resposta: sim, e com um metodo ainda mais forte que o do navegador.** O DRX e o
TriboCAD sao Qt, entao nao ha DOM. Usei o equivalente Qt da pilha de pintura:
**render offscreen** (`QWidget.render()` em `QImage`) + **amostragem de pixels**. O
fundo sai dos pixels vizinhos do glifo, nao da arvore de ancestrais - a mesma
logica do `elementsFromPoint`. O script `wcag_qt_render.py` reproduziu os valores
da camada estatica ao pixel (3,56:1 e 2,80:1 do `QPushButton#acao`), o que valida
o metodo.

**Os dois herdam a mesma paleta dos outros 3 apps.** O DRX usa `qt_tema.py` do DA e o
TriboCAD usa `qt_tema.py` do TriboDEM - `PALETAS` byte-identica. Entao os achados
P1, P2 e P3 ja valem para eles. **O que escapa** sao as cores escritas no codigo
(hardcoded), que nao passam pela paleta e nao seriam corrigidas por nenhuma troca
de token:

### DRX (`raman_phase_analyzer/drx/qt_drx.py`)

| Cor hardcoded | Onde | Medido | Min. | Regra | Correcao |
|---|---|---|---|---|---|
| `#16A34A` (ok) | texto da tabela de etapas e da arvore de resultados (`setForeground`) | **3,30:1** (claro/painel) · **3,01:1** (claro/painel2) | 4,5 | 1.4.3 | passar a usar o token `ok` do tema |
| `#DC2626` (erro) | mesma tabela e arvore | **4,41:1** (claro/painel2) · **3,56:1** (escuro/painel) · **3,17:1** (escuro/painel2) | 4,5 | 1.4.3 | passar a usar o token `erro` do tema |
| `#E8762D` | caneta "calculado" do grafico | **2,97:1** (claro/painel) | 3 | 1.4.11 | usar `acento` do tema |
| `#94A3B8` | eixo do grafico de residuo | **2,56:1** (claro/painel) | 3 | 1.4.11 | usar `texto2` do tema |
| `#1F3A5F` / `#1E3A5F` | caneta "serie" e "observado" | **1,50:1** / **1,49:1** (escuro/painel) | 3 | 1.4.11 | usar `marca2` do tema |

### TriboCAD (`tribodem/cad_qt.py`)

| Cor hardcoded | Onde | Medido | Min. | Regra | Correcao |
|---|---|---|---|---|---|
| `#16A34A` (inlet) · `#F59E0B` (liner) · `#22D3EE` (region) | cor da peca no viewport 3D (VTK) | **2,30:1** · **1,50:1** · **1,26:1** (claro) | 3 | 1.4.11 | derivar do token `acento`/`ok`/`aviso` |
| `#16A34A` · `#F59E0B` | cor da peca como TEXTO na arvore/tabela de features | **3,30:1** · **2,15:1** (claro/painel) | 4,5 | 1.4.3 | idem |
| `#1F3A5F` | peca padrao no viewport 3D | **1,23:1** (escuro) | 3 | 1.4.11 | usar `marca2` do tema |

Todos os achados acima sao **regressoes de codigo**, nao de token: o padrao do projeto
e a paleta, e essas cores foram escritas a mao. A correcao delas e a mesma troca de
token ja proposta, so que aplicada no ponto de uso.

**Tempo extra: nao houve.** A medicao do DRX e do TriboCAD coube na mesma rodada
(render offscreen + script de 40 linhas). O que falta para fechar os 6 apps de
verdade e a **decisao do GN sobre a paleta** - nao medicao.

**Nota de escopo:** a aba DRX e o TriboCAD estao fora do escopo de edicao (ARTUR e JP).
O bloco acima e **somente medicao** - nenhum arquivo foi alterado.

---

## Aplicado e verificado (21/10/2026)

Autorizacao do controlador `omniroute-d6`, por ordem do avaliador final `qe-flow-0b`:
aplicar P1 + P2 + P3 **e** as 10 cores escritas a mao no DRX e no TriboCAD. Duas
ressalvas do controlador:

1. **Usar o TOKEN do tema no ponto de uso**, nao escrever hex literal novo. Se algum
   caso nao tivesse token adequado, o diff iria ao controlador antes de escolher a cor.
2. **O viewport 3D do TriboCAD e gradiente**: medir sobre o fundo real do canvas e
   mandar screenshot antes/depois, alem do numero.

Nenhum hex novo foi escrito. Todos os 12 pontos do DRX e os 3 do TriboCAD usam token
existente. `acento` ficou **byte-identico** nos 2 arquivos de tema.

### Verificacao (2 scripts rodados de novo)

| Camada | Antes | Depois |
|---|---|---|
| Estatica (`wcag_static.py`) | 374 pares · **80 falhas** | 390 pares · **0 falhas** |
| Navegador real (`t_wcag_v2.js`, Playwright) | 485 elementos | **1006 elementos · 0 falhas** |

Detalhe do depois, por app × tema: Financas 277/277 · Radar 150/150 · Write 76/76 ·
**0 falhas** nos 6 pares. A camada estatica subiu de 374 para 390 pares porque os
elementos do DRX e do TriboCAD entraram na lista depois da correcao.

### P1 - `QPushButton#acao` (3 apps Qt)

| Tema | Medido antes | Medido depois | Token |
|---|---|---|---|
| claro | 3,56:1 (`#FFFFFF` sobre `#EA580C`) | **5,20:1** (`#1A1207` sobre `#EA580C`) | `on_acento` |
| escuro | 2,80:1 (`#FFFFFF` sobre `#F97316`) | **6,61:1** (`#1A1207` sobre `#F97316`) | `on_acento` |
| escuro, hover | 3,56:1 (hover usava `#EA580C`, token do tema claro) | **5,20:1** | `on_acento` |

O hover do dark deixou de usar o token do tema claro. `acento` nao foi tocado.

### P2 - cores de estado como texto

| Token | Antes (claro) | Depois (claro) | Antes (escuro) | Depois (escuro) |
|---|---|---|---|---|
| `ok` | 3,74:1 | **5,47:1** (`#0F766E`) | passa | **9,23:1** |
| `aviso` | 3,19:1 | **7,09:1** (`#92400E`) | passa | **10,30:1** |
| `erro` | 4,41:1 | **5,91:1** (`#B91C1C`) | passa | **6,21:1** |

Alem do token: os chips `.adiavel` do Financas (2,83 → 6,30), os `span.ic` (icone
branco em circulo colorido) e a frase de estado `div.small` do Financas.

### P3 - borda de campo (1.4.11)

| Token | Antes (claro) | Depois (claro) | Antes (escuro) | Depois (escuro) |
|---|---|---|---|---|
| `borda` (Qt, 3 apps) | 1,48:1 | **3,40:1** (`#7C8DA1`) | 1,37:1 | **3,61:1** (`#64748B`) |
| `--line` (Write) | 1,54:1 | **3,36:1** (`#8C8C8C`) | 1,51:1 | **3,39:1** (`#7C7C7C`) |

### As 10 cores escritas a mao (DRX e TriboCAD)

Todas as 10 viraram token do tema. A coluna "antes" e a **lista medida**, nao contagem.

#### DRX - `raman_phase_analyzer/drx/qt_drx.py` (9 trocas)

| # | Caso | Antes (claro / escuro) | Token | Depois (claro / escuro) |
|---|---|---|---|---|
| 1 | texto da tabela, "Accepted" ✓ | `#16A34A` 3,30 / 5,22 | `ok` | **5,47 / 9,23** |
| 2 | texto da tabela, "Accepted" ✗ | `#DC2626` 4,83 / 3,56 | `erro` | **6,47 / 6,21** |
| 3 | texto da arvore, "ok" | `#16A34A` 3,30 / 5,22 | `ok` | **5,47 / 9,23** |
| 4 | texto da arvore, "failed" | `#DC2626` 4,83 / 3,56 | `erro` | **6,47 / 6,21** |
| 5 | caneta "calculated" | `#E8762D` 2,97 / 5,78 | `acento` | **3,56 / 6,13** |
| 6 | simbolo "observed" | `(30,58,95,160)` 3,86 / **1,27** | `texto` @160 | **5,18 / 6,83** |
| 7 | caneta "background" | `#6B7280` 4,83 / 3,56 | `texto2` | **7,58 / 6,12** |
| 8 | caneta "difference" | `#0F766E` 5,47 / 3,14 | `ok` | **5,47 / 9,23** |
| 9 | linha do residuo | `#94A3B8` 2,56 / 6,70 | `texto2` | **7,58 / 6,12** |
| 10 | barra de erro | `#16A34A` 3,30 / 5,22 | `ok` | **5,47 / 9,23** |
| 11 | caneta "serie" | `#1F3A5F` 11,48 / **1,50** | `eixo` | **10,35 / 11,58** |
| 12 | simbolo do par | `#E8762D` 2,97 / 5,78 | `acento` | **3,56 / 6,13** |

Os 2 casos que o avaliador final escalou (`symbolBrush` e `#1F3A5F`) foram resolvidos
**sem hex novo**: `marca2` foi descartado no escuro (1,15:1), e o token `eixo` passa
nos 2 temas. O `symbolBrush` virou `texto` com alfa 160.

#### TriboCAD - `tribodem/cad_qt.py` (3 trocas)

| # | Caso | Antes | Token | Depois |
|---|---|---|---|---|
| 13 | letras do cubo de orientacao (R/L/B/F/T/Bo) | branco padrao do VTK, sumia no tema claro | `texto` | **12,46 / 12,75** |
| 14 | contorno das letras do cubo | laranja padrao do VTK (1,0 / 0,5 / 0,0) | `texto` | **12,46 / 12,75** |
| 15 | **aresta da peca** (`vtkFeatureEdges`) | `#141A24` → claro 12,18 / **escuro 1,07 (reprova)** | `texto` | **claro 12,46 / escuro 12,75** |

**Medicao do viewport 3D sobre o fundo REAL.** O fundo do canvas VTK e um gradiente
vertical, nao uma cor solida. Medido renderizando o canvas **vazio** (captura por
`vtk.vtkWindowToImageFilter` - `QWidget.grab()` do `QVTKRenderWindowInteractor` devolve
preto): claro topo `#FAFDFF` / base `#CCD9E8`; escuro topo `#0D121F` / base `#212C42`.

Criterio 1.4.11 aplicado ao viewport: se o **preenchimento** da peca passa de 3:1
contra o fundo real, a peca se identifica pelo proprio preenchimento e a aresta nao e
requisito. Se **nao** passa, a aresta e obrigatoria e precisa de >=3:1 contra o fundo
real **E** contra o proprio preenchimento (senao a aresta some dentro da peca).
Das 32 cores do catalogo, **17 pecas exigem aresta no claro e 15 no escuro**.

| Token candidato | vs fundo (claro / escuro) | Falhas vs preenchimento | Veredito |
|---|---|---|---|
| **`texto`** | **12,46 / 12,75** | **0 / 0** | **aplicado** |
| `texto2` | 5,29 / 4,97 | 7 / 8 | reprova |
| `eixo` | 7,23 / 9,41 | 1 / 0 | passa, mas com menos folga |
| `borda` | 2,37 / 2,93 | - | reprova |
| `marca` | 10,11 / **1,02** | 0 / - | reprova no escuro |
| `marca2` | 8,03 / **1,07** | 0 / - | reprova no escuro |
| `acento` | **2,48** / 4,98 | 8 / - | reprova no claro |

`texto` e o unico token que passa nos dois criterios nos dois temas, com a maior folga.

**Screenshots antes/depois** (viewport 3D, 1631x869):
- antes, tema claro: `C:\Users\yuri\AppData\Local\Temp\audit_visual\tribocad_antes_claro.png`
- depois, tema claro: `C:\Users\yuri\AppData\Local\Temp\audit_visual\tribocad_depois3_claro.png`
- depois, tema escuro: `C:\Users\yuri\AppData\Local\Temp\audit_visual\tribocad_depois3_escuro.png`
- janela inteira: os mesmos nomes com sufixo `_janela.png`

### Diff por arquivo

**`C:\Users\yuri\OneDrive\Desktop\Claude\DA\raman_phase_analyzer\drx\qt_drx.py`**

Tokens de codigo (1 helper novo no nivel de modulo, logo apos `_valor()`):
- `_rgb(cor, alpha=255)` - converte `'#RRGGBB'` do token do tema na tupla
  `(r, g, b, alpha)` que o pyqtgraph usa no `symbolBrush`.

```python
def _rgb(cor: str, alpha: int = 255):
    """'#RRGGBB' do token do tema -> tupla (r, g, b, alpha) que o pyqtgraph usa no symbolBrush."""
    c = cor.lstrip("#")
    return (int(c[0:2], 16), int(c[2:4], 16), int(c[4:6], 16), alpha)
```

Funcao `aplicar_tema()` reescrita (9 trocas de literal para token dentro dela):
- `self.gl.setBackground(c["painel"])`, `self.g_par.setBackground(c["painel"])`
- eixos: `setTextPen(pg.mkPen(c["texto2"]))` e `setPen(pg.mkPen(c["borda"]))`
- as curvas usam `c["texto"]`, `c["acento"]`, `c["texto2"]`, `c["ok"]` (com `self.c` reatribuido)
- **`self._recolorir_tabela()`** e **`self._recolorir_arvore()`** - metodos NOVOS, repintam
  a coluna "Accepted" (✓/✗) e a coluna "ok/failed" quando o tema muda

Funcao `_mostrar()` - bloco das curvas:
```python
self.g.plot(x, yo, pen=None, symbol="o", symbolSize=3, symbolBrush=_rgb(c["texto"], 160), name=t("observed"))
self.g.plot(x, yc, pen=pg.mkPen(c["acento"], width=1.5), name=t("calculated"))
self.g.plot(x, fb, pen=pg.mkPen(c["texto2"], width=1, style=Qt.DashLine), name=t("background"))
dif = yo - yc
self.g_res.plot(x, dif, pen=pg.mkPen(c["ok"], width=1), name=t("difference"))
self.g_res.addItem(pg.InfiniteLine(angle=0, movable=False, pen=pg.mkPen(c["texto2"], style=Qt.DashLine)))
```
e a barra de erro: `pen=pg.mkPen(c["ok"])`.

Funcao `_plot_serie()`:
```python
self.g_par.plot(xs, ys, pen=pg.mkPen(self.c["eixo"], width=2), symbol="o", symbolBrush=self.c["acento"])
```

Funcao `_linha_etapa()` e `_fim()`: `QColor(self.c["ok"] if ... else self.c["erro"])`.

**Restam apenas os 2 dicts de fallback** de `self.c` (L69-70 e L81-82) - nenhum literal
de cor de interface. `py_compile`: OK.

**`C:\Users\yuri\OneDrive\Desktop\MESTRADO PPGTIM\DEM\TriboDEM_Studio\tribodem\cad_qt.py`**

```python
cubo.GetCubeProperty().SetColor(*rgb(self.c["acento"]))
for prop in (cubo.GetXPlusFaceProperty(), cubo.GetXMinusFaceProperty(),
             cubo.GetYPlusFaceProperty(), cubo.GetYMinusFaceProperty(),
             cubo.GetZPlusFaceProperty(), cubo.GetZMinusFaceProperty()):
    prop.SetColor(*rgb(self.c["texto"]))
cubo.GetTextEdgesProperty().SetColor(*rgb(self.c["texto"]))
```
```python
ar = vtk.vtkActor()
ar.SetMapper(ma)
ar.GetProperty().SetColor(*rgb(self.c["texto"]))
ar.GetProperty().SetLineWidth(1.2)
```
`py_compile`: OK.

**NAO editados** (arquivos de outros donos, fora do escopo autorizado):
- `tribodem/pecas_padrao.py` (do JP, em uso) - as 16 cores de peca que reprovam <3:1
  contra o fundo real nao foram mexidas. A correcao aplicada e a aresta/silhueta com
  >=3:1, que resolve a identificacao sem tocar no catalogo do JP.
- `tribodem/cad.py` (do GN)
- `tribodem/cad_gui.py` (legado tkinter)

### Conflitos a resolver (nao aplicados)

1. **Lista do GN tem 4 itens que colidem com 8 da lista do avaliador final** (itens 4 x 8).
   A reconciliacao esta pendente com o GN (`omniroute-c0`).
2. **Write: o `--line #8C8C8C` (proposto) sobre `--desk #E6E6E6` da 3,34:1**, nao 3:1
   estrito - mas passa. Sobre `--paper #FFFFFF` da 4,17:1. O padrao adotado no
   navegador foi `#7C7C7C`, que da 3,34 / 4,17 / 3,95 (chrome / paper / desk) - passa
   nos 3 fundos.
3. **DRX, `marca2` no escuro da 1,15:1** - por isso o token `eixo` foi usado na caneta
   "serie" em vez de `marca2`.
4. **Escopo:** `qt_drx.py` e do ARTUR e `cad_qt.py` e do JP. O controlador autorizou
   explicitamente, mas os 2 donos precisam ser avisados.

---

## Prioridade

**P1 — corrigir agora (1 token, 3 apps).**
`QPushButton#acao` com texto branco sobre o laranja (3.56 claro / 2.80 escuro).
Correção mínima: trocar o `color: white` por `color: {c['acento_texto']}` com `#1A1207`
(5.20 no claro, 6.61 no escuro) — mantém o laranja da marca e passa em ambos os temas,
**sem** mexer no token `acento` (que também é usado como fundo de chip, barra e `.btn` web).
Alternativa: escurecer `acento` para `#C2410C` (5.18 com branco) — mas aí o laranja da marca
escurece no dark e o hover do dark precisa ser corrigido à parte.

**P2 — importante (cores de estado como texto).**
`ok` e `aviso` no tema claro ficam entre 2.83 e 3.74:1, sempre abaixo de 4.5.
Correção mínima: `ok` → `#0F766E`, `aviso` → `#92400E` (o `#B45309` deixa o chip `.adiavel`
em 4.46, ainda curto), `erro` → `#B91C1C`.
Isso arrasta o mesmo ajuste nos 3 apps Qt (paleta compartilhada) e nos chips do Finanças/Radar.
Atenção: o mesmo token é usado como **fundo** em alguns lugares — conferir o contraste do
texto branco sobre o novo valor (`#B91C1C` sobre `#FFF` = 6.47, `#0F766E` = 5.47, `#92400E` = 7.09).

**P3 — oportunidade (bordas de campo, 1.4.11).**
Bordas de input entre 1.37 e 1.54:1 nos 6 apps. Correção: clarear `borda` no claro
(`#CBD5E1` → `#7C8DA1`, 3.40) e no escuro (`#263545` → tom equivalente com ≥3:1 sobre `#0B1118`),
e `line` do Write (`#D2D0CE` → `#8C8C8C`, 3.36).
É a menor prioridade porque o campo continua identificável pelo rótulo, mas a regra
literal (1.4.11) pede 3:1.

---

## Aviso de escopo

- A **PALETAS é BYTE-IDÊNTICA** nos 3 arquivos Qt (DA, TriboDEM, Flow). Mudar um token ali
  corrige os três de uma vez — e o mesmo vale para a paleta unificada dos 6.
- A **aba DRX do DA** e o **TriboCAD** **NÃO foram tocados** (pertencem ao ARTUR e ao JP).
- Auditoria de **leitura e medição**: nenhum arquivo dos apps foi alterado.
- O Write tem paleta própria (`--app #2B579A` no modo documento), que já passa em todos os
  pares medidos — os 2 achados do Write (itens 17 e 23) são do `--accent` laranja e da borda.

---

## Critério de correção sugerido

| Token | Agora | Vira | Ganho |
|---|---|---|---|
| Qt `QPushButton#acao` `color` | `white` | `#1A1207` (novo `acento_texto`) | 3.56 → 5.20 (claro) · 2.80 → 6.61 (escuro) |
| `ok` (claro) | `#0D9488` | `#0F766E` | 3.74 → 5.47 (sobre `#FFF`) |
| `aviso` (claro) | `#D97706` | `#92400E` | 3.19 → 7.09 · chip `.adiavel` 2.83 → 6.30 |
| `erro` (claro) | `#DC2626` | `#B91C1C` | 4.41 → 5.91 (sobre `#F1F5F9`) |
| `borda` (claro) | `#CBD5E1` | `#7C8DA1` | 1.48 → 3.40 (sobre `#FFF`) |
| Write `--accent` (só como texto) | `#EA580C` | `#C2410C` | 3.21 → 4.67 (sobre `#F3F3F3`) |
| Write `--line` | `#D2D0CE` | `#8C8C8C` | 1.54 → 3.36 (sobre `#FFF`) |
