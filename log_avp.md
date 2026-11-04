# log_avp.md — Avaliador Global Prévia (sessão `omniroute-16`)

Cada sessão grava aqui; o controlador (`omniroute-d6`) consolida. Regra do controlador: "cada sessao grava no seu
proprio log_<sessao>.md e eu consolido. Crie o seu `log_avp.md`."

Hierarquia: `qe-flow-0b` (avaliador final) → controlador `omniroute-d6` → **AVP (`omniroute-16`)** → GN (`c0`), SEG (`09`).

Limites permanecem (do controlador): sem git push, não apagar arquivos, não expor portas nem tokens, não mexer no
`.env`, editar `.py` só com Edit/Write, nunca 2 DEM-Engine ao mesmo tempo, nada de dado real do DRX, não mudar
permissão nem configuração. Decisão irreversível ou que dependa do Yuri: anotar e esperar.

---

## 2026-10-21 — Rodada AVP: veredito do pino-disco, correção de número publicado, incidente do v9

### 1. VEREDITO DO PINO-DISCO — o número que eu havia publicado estava ERRADO

**O que eu havia publicado (errado):** "a troca do disco para 52100 derruba o desgaste do disco **11,25×**, de
1,472e-04 para **1,307e-05 mm³/(N·m)**, e o par novo cai **DENTRO** da faixa medida (3,67e-06 AFE 2017 … 7,89e-05
LFS-USP)".

**Por que estava errado:** eu apliquei a razão `k/H` (0,0889 ⇒ queda de 11,25×) ao valor medido do v9, sem rodar o
caminho analítico de verdade. A razão `k/H` **não é o preditor correto** aqui: subir a dureza do disco de 200 para
750 HV muda `p/H` e portanto **a fração do caminho no regime severo** (0,588 → 0,012), e é isso — não a razão `k/H` —
que domina a taxa final.

**Números corretos (rodados no caminho real, `ensaio_completo.projetar_pino`, mesmos parâmetros do `yade_worker`):**

| par | taxa pino | taxa disco | V pino | V disco | severo pino | severo disco |
|---|---|---|---|---|---|---|
| v9 real 52100 × 1045 | **2,693710e-06** | **1,472040e-04** | 0,038714 mm³ | 1,719929 mm³ | 0,012 | 0,588 |
| novo 52100 × 52100 | **2,714201e-06** | **2,714201e-06** | 0,039214 mm³ | 0,039214 mm³ | 0,012 | 0,012 |

- A linha **v9 real reproduz o `resultado.json` dígito a dígito** (2,6937102800060497e-06 / 0,00014720404707768545) ⇒
  o caminho de cálculo está certo e é o mesmo que o worker usa.
- **Queda real do disco: 54,24×** (não 11,25×).
- **Consequência no critério 6 (inverte o que eu havia escrito):** 2,714201e-06 é **0,740× o mínimo do AFE 2017
  (3,67e-06)** ⇒ o par novo **cai ABAIXO da faixa medida**, não dentro dela. O par antigo estava 40,11× acima do
  mesmo mínimo. **A afirmação "cai DENTRO da faixa" está RETIRADA.**

**O que sobrevive e é mais forte (medido, não razão de catálogo):**
- Reprodução exata do v9 pelo mesmo caminho analítico (2,693710e-06 / 1,472040e-04).
- **NIST IR 89-4170 (VAMAS Round 1) tem condições IDÊNTICAS às do código** (52100 × 52100, 10 N, 0,1 m/s, 1000 m):
  COF 0,60 ± 0,11; taxa de desgaste do sistema 70 ± 20 µm/km; cicatriz na esfera 2,11 ± 0,27 mm; largura da pista no
  disco **não impressa** para o par aço-aço (logo não há taxa volumétrica derivável para o disco).
  - Modelo, par novo: calota da ponta h = 64,74 µm ⇒ **redução de diâmetro da cicatriz 129,5 µm em 1000 m
    (129,5 µm/km)**; profundidade do sulco no disco média 0,0814 µm/km.
  - RESSALVA binding: a taxa do NIST é **linear (µm/km)**, não volumétrica; e a largura de pista do disco não é
    impressa ⇒ a comparação do sulco do disco com 70 µm/km **não é alvo válido**; a da cicatriz da bola é a
    comparação geométrica legítima.
- **Nas condições do AFE 2017** (30 N, 0,063 m/s, 100 m, R = 5 mm, 52100 × 100Cr6 ≡ 52100): modelo taxa
  8,598730e-06 mm³/(N·m) = **2,343× o k medido de 3,67e-06**; V bola 0,033964 mm³ contra 0,029 medido (1,171×);
  V disco 0,033964 contra 0,011 medido (3,088×).

**Status do pino-disco:** o critério 6 **inverte** de sinal em relação ao que eu havia publicado. O pino-disco **não**
é "o melhor por ter fonte primária que sustenta o número" — é o que tem a **fonte primária mais diretamente
aplicável** (o NIST VAMAS Round 1 é literalmente o par e as condições do código) e é exatamente por isso que o
desvio dele é **mensurável** e grande. Os critérios 2 e 7 continuam parciais até o re-run, porque
`resultado.json` ainda mostra `material2: "AISI 1045"` (evidência do par antigo).

### 2. INCIDENTE CRÍTICO — o snapshot `resultados_v9/` foi DESTRUÍDO e restaurado

- **Causa:** `python testes/realidade.py --help` caía no `gerar("--help")`; `gerar()` faz
  `shutil.rmtree` em todo `BASE.glob("resultados_v*")` ⇒ **apagou a rodada v9 inteira às 23:13:42 de 20/10/2026**.
  A v9 é a base de evidência do 66,6/100 oficial.
- **Recuperação:** o OneDrive ressincronizou e a pasta reapareceu completa (11 casos com `resultado.json` e
  `caso.json`). **As minhas edições de `caso.json` foram revertidas pelo restore** e tive de reaplicá-las.
- **Correção da causa raiz (em `testes/realidade.py`):** guarda `_versao_valida()` (só letras, dígitos, `-`, `_`) que
  aborta **antes** de qualquer `rmtree`, e um ramo `--help`/`-h` de verdade (impressão em ASCII, `SystemExit(0)`).
  **Verificado:** `python testes/realidade.py --help` ⇒ exit 0 e v9 intacta (11 entradas).

### 3. EQUIVALÊNCIA 100Cr6 ≡ 52100 registrada em lugar que sobrevive ao round-trip da GUI

- `tribodem/physics.py:42` — o catálogo do 52100 agora traz, no campo `origem`, a equivalência
  100Cr6 (DIN/EN) = AISI 52100 (ASTM A2959) e o k medido de 3,67e-06 mm³/(N·m) do AFE 2017
  (DOI 10.1515/afe-2017-0119).
- Os **três `caso.json` da v9** (`V9_pino_disco_varredura`, `V9_esfera_disco_varredura`,
  `V9_pino_disco_abrasivo_quartzo`) têm `origem` e uma chave nova `nota_equivalencia` em
  `bibliotecas.materiais["AISI 52100 (rolamento, 62 HRC)"]`.
- **Por que na biblioteca e não em `padroes()`:** a GUI (`gui.py:309-340` `_construir_form` e `:390-408` `caso_do_form`)
  **reconstrói o caso campo a campo** a partir de `experiments.padroes(tipo)` ⇒ uma chave nova em `padroes()` seria
  **descartada** no round-trip. Já `runner.py:169` grava o dict inteiro do caso (incluindo `bibliotecas`) no
  `caso.json` ⇒ a biblioteca persiste. **Pendência:** confirmar a presença no `caso.json` do próximo re-run.

### 4. ESCOPO DA ESFERA-DISCO — corrigido (reformulação, sem "cópia")

O veredito anterior de "cópia do ensaio do pino" está **ERRADO e foi revertido**. Os números de Hertz da
esfera-disco (`E_estrela_GPa` 113,62, `a_hertz_um` 58,29, `p0_hertz_MPa` 1405,38) são **identidade matemática**:
`a_hertz = (3·Fn·R/(4·E_red))^(1/3)` (`ensaio_completo.py:165`; idêntica em `yade_worker.py:141-148`), e os dois
casos têm o **mesmo R = 3,0 mm**, a **mesma Fn = 10 N** e o **mesmo par** ⇒ têm de dar o mesmo Hertz.
**O defeito real é o ATRITO:** `mu_medio_DEM` 0,06056 (esfera rolando) contra `mu_modelo_final` 0,6, e o caminho
analítico é semeado pelo μ do DEM (`yade_worker.py:355-396` passa `mu_ss = float(np.mean(mu_med))` para
`EC.projetar_pino`). A esfera tem `modo_contato: "rolling_sliding"`, `srr_pct` 10 ⇒ `fracao_escorregamento`
0,0952381 ⇒ `distancia_escorregada_ensaio_m` = 28,5714 m (contra 1000 m de deslizamento do pino), e sai em
`ensaio_regime_desgaste_final` "severo" (o pino sai "leve").
**Consequência:** o re-run da esfera-disco **não** precisa "desfazer cópia de Hertz" — precisa **corrigir o tratamento
de rolamento** (o μ do modelo tem de ser o de rolamento/escorregamento da própria esfera, e a distância escorregada,
não a rolada).

### 5. BLOQUEIOS (re-run bloqueado)

- **WSL DOWN:** `wsl.exe -l -v` ⇒ "Ubuntu Stopped"; `wsl.exe -e bash -lc` ⇒
  `Wsl/Service/CreateInstance/HCS_E_CONNECTION_TIMEOUT`. **Não reiniciei** (regra da casa: o CPOD segura a VM).
- **RAM:** 7,63 GB total / **0,01 GB livre**.
- ⇒ **O re-run na CPU do pino-disco e da esfera-disco com 52100 × 52100 NÃO dispara sem janela.** Avisado ao
  controlador. Quando disparar: `powershell -File testes\rodar_lote_janela.ps1` + Monitor aberto na tela.
- **Nunca** lançar defletora/caçamba v10 antes do tracker + malha ≤ 50 mm + PSD real.

### 6. BACKUP DA EVIDÊNCIA + GUARDA DE APAGAMENTO (ordem do avaliador final, 21/10/2026)

**Backup (cópia, nada movido nem apagado):** `C:\Users\yuri\backup_tribodem\v9_2026-10-21\`
contém os 214 arquivos da rodada v9 (1.817.873.428 bytes) + `MANIFESTO_SHA256.txt` (SHA256 por arquivo) +
`HASH_EVIDENCIA.txt` (hash agregado).

**Hash da evidência (origem e cópia, byte a byte idênticos — verificado arquivo a arquivo):**

```
SHA256_EVIDENCIA  b113a41a3e3d44f50b4d19adda27d0584942b202a6a53a39c033e02eb26210eb
ARQUIVOS          214
BYTES             1817873428
```

- A única diferença entre origem e cópia é o **próprio `MANIFESTO_SHA256.txt`**, que mora dentro da cópia.
  Os 214 arquivos de evidência são idênticos (diff por nome + SHA256 por arquivo: vazio).
- ⚠️ **O hash `15c1ebdf…a01a3efffbe` publicado antes no log foi calculado sobre a pasta INCLUINDO o manifesto e
  NÃO REPRODUZ.** O valor oficial é o `b113a41a…eb26210eb` acima (a pasta de evidência, sem manifesto).

**Guarda de apagamento — `tribodem/seguranca_rmtree.py` (módulo novo, compartilhado):**
- `apagar_rodada(v, base, outros=())` — rotação de rodada: valida o rótulo **antes** de qualquer `rmtree`;
  levanta `ApagamentoRecusado` (nunca engolida) e **preserva** as rodadas do registro de proteção.
- `apagar_dentro(base, nome, exceto=())` — limpa o *conteúdo* de uma pasta de trabalho.
- `apagar_caminho(p, motivo="")` — apaga UM caminho (pasta de caso, quadro temporário); recusa base de evidência.
- **Registro de rodadas protegidas:** `testes/realidade/RODADAS_PROTEGIDAS.txt` (hoje: `9`). Uma rodada
  listada nunca é apagada — nem pela rotação. Para apagar de propósito, tira-se a linha (ato deliberado).
- **Vetor de rótulo:** `^[A-Za-z0-9][A-Za-z0-9_-]*$` — sem ponto, barra, espaço, dois pontos ou hífen inicial.
  É isso que impede `gerar("--help")` de virar uma rodada e matar a v9.

**Extensão da guarda a TODOS os `rmtree`** (a ordem era "toda ferramenta que use rmtree"):
`tribodem/runner.py` (2), `tribodem/render.py` (3), `tribodem/vida_util.py` (2), `tribodem/qt_app.py` (1),
`testes/realidade.py` (3) e os 10 scripts de `testes/` (campanha_lubrificantes, cena_caso,
cena_correia_desalinhada, fumaca_cacamba, fumaca_correia, fumaca_tipo, fumaca_tribometros, teste_cacamba,
teste_papeis_liner, teste_pilha, teste_video_movimento). **Nenhum `shutil.rmtree` solto sobrou** (fora do
módulo da guarda). 10 imports `shutil` que ficaram órfãos foram removidos (código morto = penalidade na rubrica).

**Teste de regressão:** `testes/teste_guarda_apagamento.py` (novo, pedido do avaliador final).
**17/17 checks OK**:
1. `--help` sai com 0, a v9 continua com as 11 entradas, e `resultados_v--help` / `lote_v--help.json`
   **não** são criados;
2. 9 rótulos inválidos (`--help`, `-h`, `""`, `None`, `v9/../v9`, `9 9`, `.9`, `../x`, `v9*`) recusados
   **antes** de apagar;
3. apagar a v9 por caminho é recusado e ela fica intacta;
4. a rotação **preserva** a v9 (protegida) e apaga a v8 (não protegida), e a v8 consta na lista do que foi apagado.

### 7. Ações pendentes (continuam abertas)

- [x] ~~`graphify update` na pasta do TriboDEM~~ — **FEITO** (21/10/2026): `graphify update . --force` na pasta
      do TriboDEM ⇒ 1977 nós, 4668 arestas, 138 comunidades; `graph.json`, `graph.html` e `GRAPH_REPORT.md`
      atualizados. (A pasta do `omniroute` é a segunda, a ser feita numa próxima rodada.)
- [x] ~~Re-dispatch dos 5 subagentes mortos~~ — **FEITO** sob a forma de **relatórios curtos por dono** em
      `docs/loop/relatorio_donos_21out2026.md` (aprovado pelo qe-flow-0b), com a tarefa de cada dono
      reenviada por SendMessage. Re-dispatch pesado **não** foi feito (RAM 0,01 GB).
- [ ] **Relatório ao CONTROLADOR `omniroute-d6` ainda NÃO entregue** — a sessão saiu da lista de peers durante a
      rodada. Conteúdo pronto (seção 8 acima); reenviar quando reaparecer.
- [ ] **Relatório ao JP (`omniroute-69`) precisa ser reenviado** — a sessão também saiu da lista de peers.
- [ ] Confirmar `nota_equivalencia` no `caso.json` do próximo re-run.
- [ ] Agente de conferência da métrica NIST VAMAS (`ae60f38188148eb9a`) **falhou por falta de memória da API**
      ("Out of memory") depois de já ter lido o PDF e estar no OCR dos apêndices escaneados. Precisa ser
      re-disparado com escopo menor (só os números do apêndice de dados, sem OCR completo) — **só quando houver
      RAM**.
### 8. RELATÓRIOS CURTOS POR DONO (21/10/2026, ordem do avaliador final)

Arquivo: `docs/loop/relatorio_donos_21out2026.md` — uma seção por dono (sergio, maria paula, laura, artur, JP),
cada uma com **"Ficou feito"** (verificado lendo o código / rodando os testes que não precisam de WSL) e
**"O que falta"** (com o bloqueio de cada item). Fecha com a tabela dos 5 bloqueios por dono.

Resumo dos 5 bloqueios, em uma tela:

| Dono | Falta | Destrava com |
|---|---|---|
| sergio | DEF 4 / DEF 5 (autorização do controlador), `sem_expand` (RAM), **expor o log de anomalia do DEM-Engine** | RAM + autorização; o item 32 **não precisa de GPU** |
| maria paula | incorporar `teste_guarda_apagamento.py` (17/17) ao agregado; 4 testes com `sys.argv[1]` sem default; *skip* explícito p/ captura de tela sem desktop | edição de `.py` (1 linha por arquivo) — o JP/sergio têm exclusividade |
| laura | **MATERIAL de fonte aberta do par do disco-disco** (a geometria já tem fonte verificada — MODELOS_PRIORIDADE Nota 7; o marcador `'# fonte a confirmar (Vale/ITV)'` em `experiments.py:224/225/229` está **VENCIDO**, conforme o qe-flow-0b em 21/10/2026, e a remoção é do **sergio**, via controlador); conferir a tabela do apêndice NIST | leitura de fonte (sem GPU/RAM pesada) |
| artur | aplicar a **reancoração de `Orig`** (`gsas_trabalhador.py:342`); degraus 4, 5 e 7 (carrera de perfil / sítios especiais / corpo rígido do metilamônio) | **decisão do qe-flow-0b** sobre re-graduar "átomos" na métrica invariante de gauge |
| JP | **default `malha_liner_mm` ainda 0** em `pecas_padrao.py:45/65/82/102` (malha inerte ⇒ −3 na rubrica); teste da rotina de aplicação sem GPU; defletora v10 e caçamba dependem de (1) tracker, (2) malha, (3) PSD real | decisão do Yuri/JP sobre o default + **sonda do tracker** |

**Nenhum item acima exige WSL, GPU ou RAM para ser adelantado** — exceto o marcado como bloqueado por RAM.
**Nada de simulação longa** (defletora, caçamba, G65) antes de (1) sonda do tracker, (2) malha ≤ 50 mm, (3) PSD real.

### 9. Distribuição e correções da rodada (21/10/2026)

- **Relatórios curtos enviados** (SendMessage) a: **sergio** (omniroute-dd), **maria paula** (omniroute-a0),
  **laura** (omniroute-a5), **artur** (omniroute-c1), **JP** (omniroute-69). Relatório ao **avaliador final**
  (qe-flow-0b) enviado com nota 66,6/100, delta 30,4, top 3 riscos e decisões D1–D6. **aprovado** por ele.
- **Correção do R2 (qe-flow-0b, 21/10/2026):** os marcadores `'# fonte a confirmar (Vale/ITV)'` de
  `experiments.py:224/225/229` estão **VENCIDOS** — a **geometria** do disco-disco já tem fonte verificada
  (`MODELOS_PRIORIDADE` Nota 7: Lewis & Olofsson 2004 *Wear* 257(7-8) 721-729, DOI 10.1016/j.wear.2004.03.019;
  Fletcher & Beynon 2000 *Proc. IMechE Part F* 214(2) 93-105; Lewis/Dwyer-Joyce/Bruni 2003 *CM 2003*, ePrints
  WhiteRose 878), com a taxa por Tγ/A por regime e a perda mássica de 0,5–3,5 g de aço perlítico por disco em
  100 000 ciclos. **O que falta é o MATERIAL do par** (1045 × 1045 por herança) — a única fonte aberta com os
  dois aços do código é Castro et al., *ABM Proceedings* 2015 (DOI 10.5151/1516-392x-26482), mas com pino de
  alumina (posição invertida), 14,71 N, 4400 m e k em ×10⁻² sem unidade ⇒ **faixa de referência, não valor
  transponível**. A remoção do marcador é do **sergio**, via controlador.
  ⇒ **O R2 reprecificado é menor do que eu havia publicado** (o que pesa é o material sem fonte, não a ausência
  total de fonte do disco-disco). Relatório e log corrigidos; laura e sergio avisados do ajuste.
- **`graphify update . --force` rodado na pasta do TriboDEM** (uma pasta por vez): 1977 nós, 4668 arestas,
  138 comunidades; `graph.json`, `graph.html` e `GRAPH_REPORT.md` atualizados. O relatório avisa que 22
  comunidades mudaram de rótulo (o `graphify label`, que usa LLM, não foi rodado — não havia RAM).
- **Sessões que saíram da lista de peers durante a rodada:** `omniroute-69` (JP) e `omniroute-d6`
  (controlador) deixaram de ser alcançáveis. ⇒ **O relatório ao CONTROLADOR ainda NÃO foi entregue** (a
  mensagem falha com *"No agent named 'omniroute-d6' is reachable"*). O conteúdo está pronto acima (seção 8 da
  lista de pendências) e precisa ser reenviado quando o controlador reaparecer. **O relatório do JP (seção 5 do
  `relatorio_donos_21out2026.md`) também precisa ser reenviado** ao JP quando a sessão voltar.
- **RAM reconferida:** 0,01 GB livres de 7,63 GB. WSL parado. Nada pesado disparado.

- [x] ~~Rota de código da laura para o sergio~~ — **RESOLVIDO pelo JP** (avaliador final, 21/10/2026):
      `tribodem/assistente.py` **JÁ** herda o par de `experiments.padroes()` (helper `_materiais_tribometro()`,
      `assistente.py:106-116`, + `mat_vars.clear()` ao trocar de modelo, `:177`) ⇒ pino-disco e esfera-disco =
      **52100×52100**, disco-disco = **1045×1045**. `testes/teste_assistente_materiais.py` **4/4 OK**
      (rodado e conferido pelo AVP). **Não precisa ir ao sergio.** Regressão do JP: `teste_escala_real.py`
      13/13 OK, `teste_cad_acoplar.py` OK. Registrado em `docs/loop/NOTAS.md:649` como ENCERRADA.

