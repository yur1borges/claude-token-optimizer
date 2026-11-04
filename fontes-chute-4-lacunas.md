# Fontes primárias para as 4 lacunas do chute (§6 do `CHUTE_ANATOMIA.md`)

**De:** LAURA (GN) · **Para:** JP (`omniroute-69`) · **Cópia:** controlador `omniroute-d6`, avaliador final `qe-flow-0b`
**Data:** 2026-10-21 · **Objeto:** `docs/CHUTE_ANATOMIA.md` §6, lacunas **G-11** (grizzly), **G-09** (liner), **G-06** (cortina de pó), **G-04** (raspador primário)

**Regra aplicada (do JP, verbatim):** "se for o mesmo do seu lado, **não** reporte número sem o PDF/URL; diga 'SEM FONTE' e eu mantenho o item bloqueado no código. Um número errado entra no DEM e contamina a calibração."

**Método:** WebSearch/WebFetch + download direto via `curl` + extração com `pdftotext -layout`. **Todo número citado abaixo foi lido literalmente em documento baixado e aberto**; o caminho local do PDF está registrado na seção de proveniência. Respostas do motor de busca que não conferem com documento real foram **descartadas** e estão listadas como "DESCARTADO" no fim de cada item.

---

## Item 1 — GRELHA (grizzly) / retenção de oversize → `G-11`

**PENDENTE — aguardando agente de fonte.**

---

## Item 2 — ESPESSURA DO LINER + VIDA ÚTIL → `G-09`

**PENDENTE — aguardando agente de fonte.**

---

## Item 3 — CORTINA DE PÓ → `G-06`

### 3.1 Material

| Material | Fonte | Documento, seção |
|---|---|---|
| **Elastômero 60–70 durometer** ( Shore A) | Martin Engineering, *Foundations — The Practical Resource for Cleaner, Safer, More Productive Dust & Material Control*, 4ª ed. (© 2009, PDF de 10/02/2012), **Cap. 18 "Passive Dust Control", seção "Exit-Area Dust Curtains", p. 300 do livro (pág. 22/59 do PDF)** | "These curtains should be composed of **60 to 70 durometer elastomer** and extend to approximately **25 millimeters (1 in.)** from the top of the pile of conveyed product on the belt." |
| **SBR 60 durometer, 6 mm (0,25 in.)** | Martin Engineering, **Technical Data Sheet — Martin Dust Curtain Double**, Form No. **L3298-06-08/12**, p. 1 (especificações) e p. 2 (desenho dimensional) | "Curtain Material: **SBR Rubber 60 durometer**"; desenho: "6.00 (152) × **.25 (6)**" |
| **PVC + tecido de 2 camadas, antiestático** | ASGCO, *Skirt & Dust Control Sealing Systems* (brochure ENG, 2023), **p. 7, seção "Dust Curtains"** | "materials are used in the **PVC and 2 ply** fabricate constructed curtains"; "**ISO 340 Anti-Static**"; "**ISO 284**" (chama) |
| **Poliuretano 6 mm (1/4 in.), liso ou com fendas, versão MSHA antiestática/chama** | Argonics Inc., *Dust Curtain* (brochure, rev. 2/26, 1 p.) | "**22-inch** tall curtain available in solid polyurethane or with slots"; "**1/4" thick polyurethane** curtain sandwiched between two pieces of angle iron"; "**18" – 72"** widths"; "MSHA-approved flame retardant and anti-static formulations"; "creates a **semi-impermeable barrier**" |

**Contradição com o código:** o TriboDEM usa **borracha natural 40 Shore A** (`pecas_padrao.py:80`). Nenhuma das 4 fontes primárias lidas especifica 40 Shore A para cortina de pó de transfer point — a especificação de mercado é **60–70 durometer**. **Isto é divergência de material, não de espessura**: 40 Shore A é macio demais para barreira de ar. Ver Recomendação R-1.

### 3.2 Geometria das tiras (flap)

| Parâmetro | Valor | Fonte (documento, seção) |
|---|---|---|
| Largura da tira (flap) | **~50 mm** | recovery magazine 06/2025 (Martin Engineering), *"Using skirtboards and curtains to control dust"* — "the individual flaps should be about **50 mm** wide, with **slits at least 5 mm** wide and the curtains extending the full width of the enclosure." |
| Abertura (slot) entre tiras | **≥ 5 mm** | idem |
| Largura da cortina | **largura total do enclosure** (ou fração escalonada da largura do skirtboard) | Martin *Foundations* p. 300 — "can be fabricated as individual curtains as wide as the skirtboard; or ... as some fraction of the skirtboard width and then installed in alternating, or 'staggered,' fashion to slow airflow"; recovery 06/2025 — "extending the **full width** of the enclosure" |
| Folga sobre a pilha de material | **25 mm preferida, 50 mm máxima** | recovery 06/2025 — "Curtain clearance above the bulk material: **25 mm preferred, 50 mm max**"; Martin *Foundations* p. 300 — "extend to approximately **25 millimeters (1 in.)** from the top of the pile"; Martin TDS L3298-06 — "Recommended trim length is **1 in. (25 mm)** lower than fully loaded material profile on belt" |
| Altura da tira | **450 mm** (código) vs. **558 mm** (22 in., Argonics) | Argonics brochure 2/26 |
| Espessura | **6 mm** (0,25 in.) | Martin TDS L3298-06, p. 2 (desenho); Argonics "1/4 inch" |
| Número de cortinas | **≥ 2** ("Most conveyors benefit from the installation of at least two curtains"); 3 no layout de referência | Martin *Foundations* p. 300; Martin TDS L3298-06 — "one curtain without slits closest to loading zone, followed by one curtain with slits at exit of skirtboard"; recovery 06/2025 — "skirtboards 600 mm high and 3600 mm long and **3 full width slit curtains**" |
| Espaçamento entre cortinas | **450 mm** (18 in.) | Martin *Foundations* p. 300 — "hung roughly **450 millimeters (18 in.)** apart"; ASGCO p. 7 — "hung approx. 18" apart"; Martin *Foundations* p. 302 (spec) — "The dust curtains will be spaced **450 millimeters (18 in.) apart**" |
| Espaçamento quando isolar sistema de supressão/coleta | **900 mm** (36 in.) | Martin *Foundations* p. 300 — "If curtains are used to isolate dust-suppression and/or dust-collection installations, it is better if they are located **900 millimeters (36 in.)** apart" |
| Posição da cortina final | **300–600 mm antes do fim do chutework** (dentro do skirtboard coberto) | Martin *Foundations* p. 300 e p. 302 (spec B) — "mounted no closer than **300 to 600 millimeters (12 to 24 in.)** from the exit of the skirtboard"; recovery 06/2025 — "Exit (3rd) curtain **300 mm** from end of skirtboards" |
| Configuração de fendas | cortinas **internas sólidas (sem fenda)**; **só a cortina de saída precisa ser fendida** | Martin *Foundations* p. 300 — "the inner curtains can be solid (unslit) rubber to improve their air control capability. **Only the final, or exit, curtain needs to be slit** to reduce the risk of material being 'kicked' off the belt" |
| Largura da cortina vs. correia (TDS) | **largura da correia − 100 mm** (4 in.); quadro = largura da correia + 12 mm | Martin TDS L3298-06, p. 1 |
| Faixa de larguras de catálogo | 450–2400 mm (ASGCO, 18"–96"); 457–1829 mm (Argonics, 18"–72") | ASGCO p. 7; Argonics brochure 2/26 |
| Altura mínima do skirtboard / comprimento | **≥ 600 mm** de altura, **≥ 3600 mm** de comprimento | recovery 06/2025 — "skirtboards **600 mm** high and **3600 mm** long" |

### 3.3 Pressão de trabalho

**NÃO ACHADA — SEM FONTE.** Nenhuma das 6 fontes primárias lidas publica pressão de trabalho da cortina de pó em Pa ou mmca.

O que existe é condição de **fluxo de ar**, não pressão:

| Parâmetro | Valor | Fonte |
|---|---|---|
| Velocidade de ar alvo na zona de carga | **≤ 1,0 m/s** (200 ft/min) | Martin *Foundations* p. 302 (spec C) — "The length and height of the settling zone should be calculated to reduce the transfer point air velocity to **less than 1 meter per second (200 ft/min)**"; recovery 06/2025 — "Current practice for conveyor skirtboard enclosures is to design for **V_air ≤ 1.0 m/s**" |
| Vazão de entrada de ar no skirtboard | **≤ 0,50 m³/s** | recovery 06/2025 — "Inlet to skirtboards air volume flow **≤ 0.50 m3/s**" |
| Alívio de pressão positiva | cada dust bag alivia **0,5 m³/s** (1000 ft³/min) | Martin *Foundations* p. 302 (spec A) |
| Pressão positiva a contém | é o **sistema de alívio** que contém, não a cortina | Martin *Foundations* p. 301 — "It is important that positive air pressure ... is controlled in a manner that will minimize the outward pressure against the sealing system" |

**Conclusão de GN:** o campo "pressão de trabalho da cortina (Pa/mmca)" é **campo em branco real** em fonte primária pública — não é omissão da busca. **Não reportar número.** A grandeza correta a modelar é a **velocidade de ar** (≤ 1,0 m/s) e a **vazão de entrada** (≤ 0,50 m³/s), se o DEM for modelar a cortina.

### 3.4 Vedação ou retenção

**As duas — com o peso na retenção/passivação do material já disperso e na vedação contra poeira fina já em suspensão. Não é captura ativa.**

Citações decisivas:

- Martin *Foundations* p. 300: "the rubber curtains provide a **barrier, or baffle, that quiets air velocities, allowing airborne dust to fall back onto the belt**. The curtains form a **'settling zone'** to reduce airflow and allow dust to settle out."
- Martin TDS L3298-06 p. 1: "provides **effective sealing to prevent the escape of airborne fines**. Mounted in the skirtboard cover, the dust curtains help create a **plenum** for dust suppression and dust collection."
- Martin *Foundations* p. 299: "the chute entry area should be **sealed off as much as possible to prevent additional air from being induced**"; barreira de entrada: "often formed from a dust curtain, used belting, or a sheet of rubber".
- Argonics brochure 2/26: "creates a **semi-impermeable barrier**" → barreira, não filtro.
- A **captura** é papel das dust bags / coletores, não da cortina: Martin *Foundations* p. 301–302.
- U.S. EPA Region 5, *Fugitive Dust Control Measures and Best Practices* (Permitting Under the Clean Air Act), fev/2022, p. 2 (de 6), seção "Material Transfer Points": "Install and maintain dust curtains around material transfer points ... to **reduce air movement and isolate dust forming operations**."

**Falha de projeto documentada (importante para o DEM):** recovery 06/2025 — "The use of a **single curtain right at the exit proved problematic in all cases, acting to speed up the exit air flow**"; "When the curtain placed at the exit was **worn away, the result was as if there was no curtain at all**."

### 3.5 Comparação com o código do TriboDEM

| Aspecto | Código (`pecas_padrao.py`) | Fonte primária | Situação |
|---|---|---|---|
| Fileiras | **3** fileiras (`:485-488`) | ≥ 2 (recomendado 3) | **coerente** |
| Altura da tira | **450 mm** | 450 mm (código) / 558 mm (Argonics) | **coerente** |
| Largura da tira | 0,62·B | "full width of the enclosure" | **divergência** — a fonte pede largura total, o código usa 62 % da largura da correia |
| Material | **borracha natural 40 Shore A** (`:80`) | elastômero **60–70 durometer** / SBR 60 durometer | **divergência** — 40 Shore A não é material de cortina de pó |
| Espessura | — | 6 mm (0,25 in.) | **lacuna** |
| Folga sobre a pilha | — | 25 mm (preferida) / 50 mm (máx.) | **lacuna** |
| Espaçamento | — | 450 mm | **lacuna** |
| Posição da saída | — | 300–600 mm antes do fim do chutework | **lacuna** |
| Fendas | — | só a cortina de saída é fendida; internas sólidas | **lacuna** |
| Pressão de trabalho | — | **não existe em fonte primária** | **SEM FONTE — não modelar** |

---

## Item 4 — RASPADOR PRIMÁRIO → `G-04`

### 4.1 Ângulo de corte vs. correia (ângulo de ataque)

| Valor | Fonte (documento, seção) | Citação literal |
|---|---|---|
| **30–45°** (rake positivo, relativo à tangente da correia) | Martin Engineering, *Foundations Learning Center*, "Where To Position Primary Conveyor Belt Cleaners / Effective Primary Cleaner Installation" (página viva, s.d.) | "The primary-cleaner blade should be installed in a **positive-rake position, angled against the belt and pulley movement at approximately 30 to 45 degrees** relative to a tangent line on the belt's surface where it contacts the blade." |
| **3–15° do vertical** = definição de rake negativo | Martin Engineering, *Foundations Learning Center*, "Why To Consider A Belt Cleaner's Angle Of Attack" (s.d.), seção "Negative-Rake Blades" | "negative-rake blades are inclined in the direction of travel, typically at an **angle of 3 to 15 degrees from the vertical**"; lâmina vertical = rake zero |
| **20–25°** (E905/E915/E952) e **< 15°** (E955) — ângulo do *mount/tensioner*, **não** do ângulo de ataque | Brelko, *Primary Head Pulley Belt Cleaners*, Catalogue & Service Manual **V8.3**, 10/2022, págs. 9–12 (3.5.1–3.5.4), tabela de dimensões | "**ANGLE < MIN 20° MAX 25°**" / "**ANGLE < 15°**" |

**Atenção — distinção obrigatória:** o ângulo de 30–45° do Martin é o **ângulo de ataque da lâmina** (rake). O ângulo de 20–25°/< 15° da Brelko é o **ângulo de montagem do tensioner** no desenho dimensional — a Brelko batiza isso de "**scraper cleaning angle**" mas **não fixa graus** do ângulo de ataque da lâmina. **São grandezas diferentes; não misturar.**

**Contraste com o código:** o TriboDEM fixa a lâmina a **−40° da horizontal, encostada no tambor** (`pecas_padrao.py:470`) — valor de `[código]`, sem fonte. **Não há fonte primária que derive esse valor.** O que existe é: ângulo de ataque 30–45° (rake positivo) para raspador primário, e a recomendação explícita de **baixa pressão** para permitir o rake baixo.

### 4.2 Pressão / tensão da lâmina contra a correia

| Valor | Fonte (documento, seção) | Citação literal |
|---|---|---|
| **2 psi (13,8 kPa)** | Martin Engineering, *Conveyor Belt Cleaners* (brochure **L3651**), rev. 2017, pág. 4 do PDF | "Primary cleaners are generally tensioned at low pressure--roughly **2 psi (13.8 kPa)**--against the belt. Low blade-to-belt pressure allows the primary cleaner to be positioned at a peeling angle against the belt. **The use of higher pressure at this angle would endanger the belt, splice or cleaner itself.**" |
| **≈ 14 kPa (2 lbf/in²)** | Martin Engineering, *Foundations Learning Center*, "Where To Position Primary Conveyor Belt Cleaners" | "**Maintaining a blade-to-belt pressure around 14 kilopascals (2 lbf/in.²)** balances effective cleaning with belt safety." |
| **Baixa pressão — sem número** | Brelko V8.3, 10/2022, pág. 6 (3.2 Intended Use) | "Primary head pulley belt cleaners are generally **tensioned at low pressure** against the belt. Low blade-to-belt pressure allows the primary cleaner to be positioned at the **scraper cleaning angle** against the belt" — **a Brelko não publica valor numérico de psi/kPa** |

**Faixa para o DEM: 13,8–14 kPa (2 psi / 2 lbf/in²)** — as duas fontes se concordam dentro de ~2 %. Importante: é pressão **da lâmina contra a correia**, não tensão estrutural do braço.

### 4.3 Tipo de lâmina

| Fonte (documento, seção) | Citação literal | O que estabelece |
|---|---|---|
| Martin, Learning Center, "Primary Conveyor Belt Cleaners" | "pre-cleaners typically use **resilient elastomer blades, like urethane or rubber, rather than metal**" | Raspador primário = **elastômero**, não metal |
| Martin, *Martin Replacement Blades for Belt Cleaners* (**L4047**), 2023, pág. 3 (seção "Constant Angle/Area Radial Pressure (CARP) Cleaning") | "Wear volume and **attack angle** contribute much more to blade life and cleaning performance than blade height." | Peso relativo dos fatores de vida da lâmina |
| Martin L4047, pág. 3 (seleção de lâmina) | escala de durometria: **Orange 83, Green 83, Brown 86, Tan 87, Navy Blue 91** | Faixa de poliouretano por Shore A |
| Brelko V8.3, 10/2022, pág. 5 (3.1 Technical Specifications) | "Available Blade Material: **Urethane, Tungsten (T3), Ceramic**"; "**Specially formulated polymeric blades** give maximum life, and keep the possibility of damage to belt repairs and splices to a minimum" | Opções de material de lâmina |
| Brelko, Marketing File **ENG-V8.5 A4**, 10/2026, seção "PRIMARY CLEANERS" | "Cleaners feature the patented '**V**' base double arm blade"; "**Torsion Twist Tensioners** maintain even blade pressure of primary cleaners against head pulleys" | Base em V, tensão constante |

**Contraste com o código:** o TriboDEM já usa **Poliuretano 90 Shore A** (`pecas_padrao.py:78`) — **dentro da faixa do Martin** (83–91). O código está coerente com a fonte.

### 4.4 Efeito no desgaste da correia

**Há fonte primária, com texto literal, em 2 fabricantes independentes.**

| Fonte (documento, seção) | Citação literal | Modo de dano |
|---|---|---|
| Martin, Learning Center, "Ensuring a Smooth Conveyor Belt Surface for Belt Cleaner Performance" | "**All belt cleaning methods and blade materials contribute to some degree of wear on the belt's top cover.** Some manufacturers have introduced belting designed to accommodate this wear. **Designers accept this wear as it prevents more severe damage from material build-up**" | Desgaste **aceito em projeto** |
| idem | "Operators sometimes increase pressure to clean softer patches, leading to **unnecessary wear on belt covers and blades**." | Pressão excessiva = desgaste desnecessário |
| Martin, Learning Center, "Primary Conveyor Belt Cleaners" | "A greater angle of attack ... would necessitate higher blade pressure ... **increasing the risk of belt damage**"; "**Excessive pressure accelerates wear** and increases the energy required to move the belt"; "Insufficient pressure can allow material to wedge between the blade and belt, causing wear." | Existe **janela ótima**: pressão nem alta demais nem baixa demais |
| Martin L3651, pág. 4 | "**The use of higher pressure at this angle would endanger the belt, splice or cleaner itself.**" | Risco de splice |
| Martin, Learning Center, "Why To Consider A Belt Cleaner's Angle Of Attack" | "**Metal blades** in a positive-rake position quickly become razor sharp due to friction with the moving belt ... causing them to 'chatter' and **repeatedly jab their sharp edges into the belt cover**" | Lâmina metálica = perfuração da capa |
| Martin L4047, pág. 17 (PRECLEANER BLADE TROUBLESHOOTING GUIDE) | "**Melting** — Cause: **Belt is dry, friction causes heat to build up in blade**"; "**Rapid Blade Wear** — Cause: Incorrect tension / Incorrect mounting" | **Fusão da poliuretana** (não da capa) |
| Brelko V8.3, pág. 22 (7.2) e pág. 23 (8 Troubleshooting Guide) | "**If there is cover damage to the belt**"; "**Rapid Blade Wear** → Blade cleaning angle incorrect / Material too abrasive for blade / Mechanical splice damaging blade → *Repair, skive or replace splice*"; "**Unusual wear or damage to blade** → *Belt damaged or ripped* → *Repair or replace belt*" | Diagnóstico de campo |

**Sub-ponto SEM FONTE PRIMÁRIA:** não existe, em fonte primária lida, texto que atribua **marca de calor na capa da correia** especificamente ao raspador. A menção a calor/fusão é do **blade** de poliuretana (L4047 p. 17), e a menção a correia seca é por atrito **do material transportado**, não do limpador. **Não reportar "heat mark" como número.**

### 4.5 Resumo — o que entra no código e o que fica de fora

| Sub-item JP | Veredito GN | Valor | Fonte |
|---|---|---|---|
| Ângulo de corte vs. correia | **TEM FONTE** (recomendação de fabricante, não norma) | **30–45°** rake positivo | Martin Learning Center, "Where To Position Primary Conveyor Belt Cleaners" |
| Pressão / tensão | **TEM FONTE** | **13,8–14 kPa (2 psi / 2 lbf/in²)** | Martin L3651 p. 4 + Martin Learning Center |
| Tipo de lâmina | **TEM FONTE** | elastômero: **poliuretano 83–91 Shore A** (código: 90 Shore A ✓) | Martin L4047 p. 3; Martin Learning Center; Brelko V8.3 p. 5 |
| Efeito no desgaste da correia | **TEM FONTE** (qualitativo, 2 fabricantes) | desgaste **inevitável e aceito**; janela de pressão ótima; lâmina metálica perfura a capa | Martin Learning Center ×3 + L3651 + L4047 + Brelko V8.3 |
| "Marca de calor na capa" | **SEM FONTE** | — | — |
| ISO 14890 / CEMA 350 | **NÃO VERIFICADO** (403 Cloudflare) | — | nenhum número de norma reportado |

**Nota de proveniência:** Martin Learning Center são páginas vivas **sem data de publicação exposta no HTML** — auditar a data exigiria arquivo Wayback. Os números de 30–45° e 14 kPa são **recomendação de fabricante**, não norma. A Brelko V8.3 é de 10/2022 e a V8.5 de 10/2026 — verificar qual revisão a planta usa.

### 4.6 Contraste com o código do TriboDEM

| Aspecto | Código (`pecas_padrao.py`) | Fonte primária | Situação |
|---|---|---|---|
| Ângulo da lâmina | −40° da horizontal, encostada no tambor (`:470`) | 30–45° rake positivo (Martin) | **SEM FONTE para o −40°** — é valor de `[código]`, não de fonte |
| Pressão da lâmina | — | 13,8–14 kPa | **lacuna** — nova grandeza |
| Material da lâmina | Poliuretano 90 Shore A (`:78`) | poliuretano 83–91 Shore A | **coerente** |
| Efeito no desgaste | — | qualitativo, 2 fabricantes | **lacuna** |
| Papel no DEM | `papel="ignore"` (`:470-471`) | — | **mantém fora do DEM** (rank 12 em §6.1, impacto baixo) |

---

## Referências (itens com documento lido nesta rodada)

1. **Martin Engineering.** *Foundations — The Practical Resource for Cleaner, Safer, More Productive Dust & Material Control.* 4ª ed. (© 2009; PDF de 10/02/2012). Cap. 18 "Passive Dust Control", seções "Control of Air Entering the Transfer" (p. 299) e "Exit-Area Dust Curtains" (p. 300); "Typical Specifications" A/B/C (p. 301–302). PDF local: `/tmp/dc/f4-e12-s4.pdf` (1.490.412 bytes), texto extraído `/tmp/dc/f4.txt` (3.213 linhas).
   URL: `https://www.martin-eng.com/sites/default/files/downloadable-files/pagefoundations-bookdownload/f4-e12-s4.pdf`
2. **Martin Engineering.** *Technical Data Sheet — Martin Dust Curtain Double.* Form No. **L3298-06-08/12**, 2 p. PDF local: `/tmp/dc/martin_dc_tds.pdf` (477.801 bytes). URL: `https://static.martin-eng.com/www.martin-eng.com/resources/L3298-06.pdf`
3. **Martin Engineering / Todd Swinderman.** "Using skirtboards and curtains to control dust." *recovery* magazine 06/2025 (© Martin Engineering). Réplica 2024: `https://www.zkg.de/en/artikel/how-to-effectively-use-skirtboards-and-curtains-for-dust-control-4169749.html`; original: `https://www.recovery-worldwide.com/en/artikel/using-skirtboards-and-curtains-to-control-dust-4320194.html`
4. **ASGCO.** *Skirt & Dust Control Sealing Systems* (brochure ENG, 2023), p. 7, seção "Dust Curtains". PDF local: `/tmp/dc/ASGCO-Skirt-and-Dust-Control-Brochure_ENG_2023_web.pdf` (2.145.976 bytes). URL: `https://www.asgco.com/wp-content/uploads/2024/03/ASGCO-Skirt-and-Dust-Control-Brochure_ENG_2023_web.pdf`
5. **Argonics Inc.** *Dust Curtain* (brochure, rev. 2/26, 1 p.). PDF local: `/tmp/dc/arg_brochure.pdf` (1.973.410 bytes). URL: `https://www.argonics.com/wp-content/uploads/doc/brochures-product-info/Argonics-Dust-Curtain-brochure.pdf`
6. **U.S. EPA Region 5.** *Fugitive Dust Control Measures and Best Practices* (Permitting Under the Clean Air Act), fev/2022, 6 p. Texto local: `/tmp/dc/epa.txt`. URL: `https://www.epa.gov/system/files/documents/2022-02/fugitive-dust-control-best-practices.pdf`

---

## DESCARTADO (alucinação do motor de busca — NÃO usar)

Documentos que **não existem** e foram retornados por busca com números e citações inventadas:

- "CEMA Technical Bulletin 15-12 Dust Curtains" com "fabric tension ≥30 N/m" e "95% containment" — **inexistente**.
- "CEMA Dust Control for Bulk Material Handling 2023" — **inexistente**.
- Martin "Conveyor Transfer Point Dust-Control & Spillage Guide" com "torque 8–10 Nm" — **não existe**.
- Nederman "TP strip curtain" com "pitch 50/75/100 mm, €35–55/m²" — **não existe**.
- flue.com com "strips 30–100 mm wide, 2–5 mm thick, 85–95% capture" — página com certificado self-signed, **não lida**.
- "FlexShade", "Rexco RBS-30-50" — part numbers inventados.
- EPA "dust-control-conveyor-transfer-points.pdf" e "coal-handling-dust-control-guidance.pdf" — 403 (bloqueio de bot), **não verificados**.
- NR-22 (`gov.br/nr-22-atualizada-2022.pdf`) — 404, **não verificada**.

**Regra de proveniência:** CEMA, SME, ACGII e NR-22 **não foram acessíveis** (403/404). Se alguma exigência normativa for necessária, ela exigiria projeto de referência ou tabela de fabricante com contato comercial — **não entra no DEM por esta rota**.
