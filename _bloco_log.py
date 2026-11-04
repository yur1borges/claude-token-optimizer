# -*- coding: utf-8 -*-
"""Anexa o bloco de decisoes 2026-10-21 02:4x ao log_controlador.md."""
from pathlib import Path

BLOCO = """

---

## 2026-10-21 - 02:4x - Controlador: revogacao WCAG, Financas D1-D4, veredito AVP, Nota 8 da GN

### 1. WCAG - revogacao do controlador, NAO revertida
- O avaliador final (`qe-flow-0b`) revogou minha decisao de "nao ha correcao autorizada" e ordenou: AJBS (26) aplica P1+P2+P3 + as 10 cores a mao do DRX/TriboCAD.
- **Eu nao reverto.** Regra vigente do avaliador final: "quando eu ja tiver decidido, voce nao reverte; se discordar, me mande a objecao e espere. Na minha ausencia, decida normalmente."
- **Objecao enviada (1, nao revogacao):** as 10 cores a mao sao regressao de CODIGO, nao de token (classificacao do proprio AJP: "corrigir e usar o token do tema no ponto de uso"). Trocar por hex literal novo repete o problema na proxima refatoracao de tema. Resposta do avaliador final: as duas objecoes procedem e foram repassadas ao AJBS como ordem (token no ponto de uso; viewport 3D medido sobre o fundo real, com screenshot).
- **Correcao do avaliador final sobre a meta:** o "antes" nao e contagem de falhas (0) - e a LISTA P1-P3 que o AJP mediu. Meta = 0 depois. JA CORRIGIDO no pedido ao AJBS.
- Ordem ao AJBS (26): P1 `#1A1207` (texto de botao, `acento` intacto) | P2 `ok #0F766E`, `aviso #92400E`, `erro #B91C1C` | P3 borda clara `#7C8DA1`, borda escura `#64748B`. Entrega exigida: razao de contraste antes -> depois item a item, diff separado token x codigo, `acento` byte-identico, screenshot do viewport 3D, caminho final do `relatorio_wcag.md`.

### 2. Financas D1-D4 - dono e rota de execucao
- **Mapa de dono do Financas continua incompleto.** Checagem feita: quem editou `Claude/Financas/Financas.html` historicamente = 3 sessoes de agente de refinamento de UI (1bf90810: 43 Edits; 2c41a190: 2; d317f4da: 2) - nenhuma delas e uma sessao peer viva. Mapa de peers: 09=AVP, 0b=avaliador final, 16=AVP, 26=AJP/AJBS, 42=vlrm, a5=LAURA (GN), a0=QA (maria paula), bf=david, c1=artur, dd=sergio, 69=JP. **Nenhum peer vivo e dono do codigo logico do Financas** (o GN e dono de design, nao de regra de negocio).
- **Decisao do controlador (na ausencia do Yuri, decido normalmente):** nao atribuo D3/D4 (regra financeira) a ninguem por improviso. O controlador aplica os 4 patches ele mesmo, com `Edit` surgical, DEPOIS que o AJBS entregar o WCAG no mesmo arquivo - para nao haver dois escritores em `Financas.html` ao mesmo tempo. Depois, a QA (maria paula) re-roda a suite e reporta antes x depois.
- **Evidencia verificada de novo, linha a linha, neste log:**
  - D1 `Financas.html:335-341` - `const b = BLANK(); const s = Object.assign(b, st || {})` sobrescreve `b`; `s.metas` ja vem `[]` de BLANK, entao o `if (!Array.isArray(s.metas))` da 337 nunca entra e o `push` da 339 e INALCANCAVEL; a 341 `delete s.meta` descarta a meta do formato antigo sem converter. **Correcao:** ler `st.meta` direto, antes do `Object.assign`, e popular `metas` a partir dele.
  - D2 `Financas.html:348` - `s.inicio = b.inicio` usa `b.inicio` JA sobrescrito (valor corrompido), nao o do BLANK. **Correcao:** usar o `inicio` do BLANK (constante, nao sobrescrita).
  - D3 `Financas.html:245-258` - `pend` filtra por `desde`; `vencidas` = obrigatoria com `prazo <= m`; `futuras` = obrigatoria com `prazo > m`; e 258 `futuras.forEach(i => pagar(i, false))` paga a divida futura NO MESMO MES, e `pagar` nao distingue "nao vence agora" de "parcial por falta de dinheiro". **Correcao:** nao pagar `futuras` no mes corrente; so entram em `faltas`/carteira quando o prazo chegar.
  - D4 `Financas.html:262` - juros de AVULSAS incidem sem checar `desde`/`prazo`, enquanto `fecharMes` (829) checa `(!it.desde || it.desde <= x.m)`. Simulacao e fechamento discordam do mesmo item. **Correcao:** aplicar o mesmo filtro de 829 na 262.
- **Nao corrigido ainda** (aguardando o AJBS fechar o WCAG no mesmo arquivo). Alarme da QA: `Financas/testes/06_defeitos.test.mjs` - quando o app for corrigido, esses alarms passam a FALHAR, e esse e o sinal de correcao, nao de regressao.

### 3. AVP (16) - veredito do pino-disco, numero publicado errado
- **Retirada explicita do AVP** do numero publicado: "queda de 11,25x, de 1,472e-04 para 1,307e-05, caindo DENTRO da faixa". O erro foi aplicar a razao k/H do catalogo (0,0889) ao valor medido sem rodar o caminho analitico: subir a dureza do disco (200 -> 750 HV) muda p/H e a FRACAO do caminho no regime severo (0,588 -> 0,012), e e isso, nao a razao k/H, que domina a taxa.
- **Numeros medidos (caminho real `ensaio_completo.projetar_pino`, reproduz o `resultado.json` da v9 digito a digito: 2,6937102800060497e-06 / 0,00014720404707768545):** v9 real 52100 x 1045 = pino 2,693710e-06 | disco 1,472040e-04 mm3/(N.m). Novo 52100 x 52100 = pino = disco = 2,714201e-06. **A queda real do disco e 54,24x, nao 11,25x.**
- **Criterio 6 INVERTE DE SINAL:** 2,714201e-06 e 0,740x o minimo do AFE 2017 (3,67e-06) => o par novo cai ABAIXO da faixa medida, nao dentro dela. O par antigo estava 40,11x acima.
- **O que sobrevive (mais forte, e medido):** NIST IR 89-4170 (VAMAS Round 1) tem condicoes IDENTICAS as do codigo (52100 x 52100, 10 N, 0,1 m/s, 1000 m) - COF 0,60 +- 0,11; taxa do sistema 70 +- 20 um/km; cicatriz na esfera 2,11 +- 0,27 mm; **LARGURA DA PISTA NO DISCO NAO IMPRESSA no par aco-aco** => nao ha taxa volumetrica derivavel para o disco. Modelo, par novo: calota h = 64,74 um => reducao de diametro da cicatriz 129,5 um em 1000 m; sulco no disco 0,0814 um/km. **Ressalva binding:** a taxa do NIST e LINEAR (um/km), nao volumetrica; comparar o sulco do disco com 70 um/km NAO e alvo valido; a comparacao da cicatriz da bola e a geometrica legitima. AFE 2017 (30 N, 0,063 m/s, 100 m, R=5 mm, 52100 x 100Cr6=52100): taxa 8,598730e-06 = 2,343x o k medido; V bola 0,033964 vs 0,029 (1,171x); V disco 0,033964 vs 0,011 (3,088x).
- **Leitura correta:** o pino-disco nao ganha por "cair dentro da faixa" - ganha por ter a fonte primaria mais diretamente aplicavel (o NIST e o par e as condicoes do codigo) e por isso o desvio dele e mensuravel e grande. Criterios 2 e 7 seguem parciais ate o re-run.
- **Escopo esfera-disco (reformulado, sem "copia"):** os numeros de Hertz sao IDENTIDADE MATEMATICA (mesmo R=3,0 mm, mesma Fn=10 N, mesmo par => mesmo Hertz). O defeito real e o ATRITO: mu_medio_DEM 0,06056 (rolamento) semeia o mu do modelo via `yade_worker.py:355-396`, contra mu_modelo_final 0,6; a esfera tem modo_contato rolling_sliding, srr 10% => fracao_escorregamento 0,0952381 => so 28,5714 m de 300 m escorregam. Precisa corrigir o TRATAMENTO DE ROLAMENTO (mu e distancia da propria esfera), nao o Hertz.
- **Incidente:** `python testes/realidade.py --help` caiu em `gerar("--help")` e o `shutil.rmtree` APAGOU a rodada v9 inteira (base do 66,6/100) as 23:13 de 20/10. OneDrive ressincronizou e a pasta voltou (11 casos), mas as edicoes de `caso.json` foram revertidas. **Causa raiz corrigida** em `testes/realidade.py`: guarda `_versao_valida()` que aborta ANTES de qualquer rmtree, e ramo `--help` de verdade (ASCII, `SystemExit(0)`). Verificado: `--help` => exit 0 e v9 intacta.
- **Re-run BLOQUEADO:** WSL DOWN (`wsl.exe -l -v` => "Ubuntu Stopped"; `wsl.exe -e bash -lc` => `Wsl/Service/CreateInstance/HCS_E_CONNECTION_TIMEOUT`) e RAM 0,01-0,09 GB livre. Nao reiniciei a distro (regra da casa). Quando abrir: `powershell -File testes\\rodar_lote_janela.ps1` + Monitor na tela. **Nunca defletora/cacamba v10 antes de tracker + malha <= 50 mm + PSD real.**
- **Decisao do controlador:** o AVP despacha os 5 subagentes mortos (sergio tracker; maria paula suite completa com pass/fail real; laura fonte aberta do par 1045 x 1045 do twin-disc; artur reancoragem P2_1 + tabela de 10 graus; JP malha <= 50 mm + defletora v10 com PSD real + cacamba com fluxo), **porem so a partir de uma janela de RAM** - a fila de RAM do controlador ja tem 2 jobs de `graphify label` na frente. Prioridade de fila: maria paula (suite) -> sergio (tribometros) -> graphify label. E reforcado: **nenhum relatorio desses 5 existe em `docs/loop/`; nenhum agente pode reportar "feito" sem relatorio gravado no arquivo.**

### 4. Fila de RAM - estado
- `fila_ram.py` (task b9jebxe69) rodando. `label qe-flow` CONCLUIDO: exit=0 em 422 s, 26 comunidades, nomeadas via `claude -p` (sem API key no ambiente). `label TriboDEM` aguardando janela (RAM 0,01-0,25 GB livre, 98,9% de uso).
- Grafo do TriboDEM confirmado pelo AVP: 1819 nos / 4367 arestas (o meu controle deu 1817/4362 - 2 nos e 5 arestas de diferenca, provavelmente arestas de community labeling do proprio AVP depois da minha medicao; sem impacto).

### 5. LAURA (GN) - Nota 8 e correcao de erro proprio
- Nota 8 gravada em `docs/MODELOS_PRIORIDADE.md` (TriboDEM_Studio): interlaboratorial ASTM G99 resolvido em acesso aberto (NIST IR 89-4170), veredito ISO 7148 **corrigido** (nao e paywall: existe texto integral aberto no iTeh, 5 URLs HTTP 200) e 4 candidatos abertos novos. Escopo: **so o .md**.
- **Correcao de erro da LAURA (o que importa):** ela havia atribuido 81 +- 29 um/km e 2,08 +- 0,35 mm ao kit "Ceramic-steel". Errado - sao do kit "Steel-ceramic" (esfera 52100 x disco alumina). Convencao do NIST e **sphere|disk**, provada por p. 47 ("Ball | Disk"), p. 38 ("Stationary ball against rotating disc") e p. 17 ("the average ball wear volume is largest for the steel/steel couple"). Causa raiz: OCR do Windows le em bloco e embaralha as linhas da tabela; adotou a camada de texto do PDF com coordenadas de caractere. Corrigido na linha 23 (row 6), na 122 (Nota 5) e na 8.1.
- Pendencia deixada de fora de proposito: correcao de material para o alvo 5 (razao de durezas invertida no codigo) - `experiments.py` fora de escopo; 4 pares com fonte listados na 8.4 para o `sergio` decidir.
- Veredito do controlador: aceite. A correcao do erro proprio e exatamente o tipo de coisa que a auditoria independente deveria pegar; registrada como risco 21.

**RISCOS NOVOS**

21. **A GN trocou silenciosamente os kits do NIST (sphere|disk)** - ja corrigido, mas a Tabela 5 continua ancorada por COORDENADA, nao por leitura visual. Qualquer agente que citar essa tabela precisa declarar a convencao, senao troca os kits de novo e o numero sai errado com cara de certo.
22. **Divida obrigatoria futura sendo paga no mes corrente (Financas D3)** - enquanto nao corrigir, a simulacao do Financas subestima a divida e o usuario ve "quitou" o que nao quitou. E o defeito de producao mais custoso dos 4, porque afeta decisao financeira real do Yuri.
23. **Numero publicado do pino-disco estava errado (11,25x / "cai dentro da faixa") e a inversao de sinal do criterio 6 so apareceu com o caminho analitico rodado** - nenhum numero de faixa pode ser citado sem o caminho de calculo que o produz. O re-run de 52100 x 52100 ainda nao rodou (WSL down + RAM) - ate rodar, o criterio 6 fica INVERSO e nao pode ser dado como fechado.
24. **`relatorio_wcag.md` e `wcag_drx_tribocad.txt` estao DENTRO de `omniroute/`** - o AJP mandou "agora esta em omniroute (o Temp some)". Corrigido, mas o AVP precisou dizer onde estava = sinal de que o caminho precisa ficar escrito no relatorio, nao na conversa.
"""


def main() -> None:
    p = Path(__file__).with_name("log_controlador.md")
    t = p.read_text(encoding="utf-8")
    assert "Cores hardcoded" in t, "log_controlador.md inesperado: marcador de risco 18 ausente"
    assert "LAURA (GN)" in t, "log_controlador.md inesperado: bloco da GN ausente"
    assert "2026-10-21 - 02:4x" not in t, "bloco ja anexado"
    p.write_text(t + BLOCO, encoding="utf-8")
    print("OK len", len(p.read_text(encoding="utf-8")))


if __name__ == "__main__":
    main()
