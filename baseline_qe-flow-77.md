# Baseline da avaliação final (qe-flow-77) — 20/10/2026

Ponto de partida para comparar quando o avaliador final voltar.

## TriboDEM — nota por evidência medida (AVP, 20/10): 66,6/100
| Experimento | Nota |
|---|---|
| pino-disco | 80 |
| esfera-disco | 76 |
| disco-disco | 71 |
| chute | 65 |
| correia | 62 |
| caçamba | 59 |
| defletora | 53 |
Trajetória do código: 71,86/100. Meta: 98/100.

## Decisões vigentes
- Disco 52100 (≡100Cr6, AFE 2017); re-run pino-disco e esfera-disco na CPU, depois de desfazer a cópia de Hertz da esfera-disco.
- Ordem da defletora: tracker → malha ≤ 50 mm → PSD real → v10. Nunca 2 DEM-Engine ao mesmo tempo.
- Escala (JP): queda da defletora ≈13 m; esfera-disco 25 N; o chute oficial é a escala real; passo dos dentes da caçamba 140 mm (JP+GN); catálogo da correia alinhado ao experiments.py.
- Caçamba: tirar o override de vazão (yade_worker.py:626).
- DRX degrau 1: gauge P2₁, reancorar Orig; aceito só se o Rwp for idêntico.

## Em curso
- sergio: tracker (v_max 183,75; vazamento 1,23 %) + assistente.py
- JP: pendência 9 (assistente.py + recalcular_carga_hertz) + docs/CHUTE_ANATOMIA.md
- laura: fonte do par 1045×1045
- artur: reanchor P2₁ + tabela dos 10 degraus
- maria paula: suíte testes/ com pass/fail real
- SEG: P33 (CSP) + tabelas de ranking
- vlrm: T1 teste da entrevista → T2 propostas → T4 citações no Write → T5 buscador → T3 Lattes

## Softwares (meta 98/100)
Write, DA, Finanças, Radar Passagens, Flow Calculation, TriboDEM — notas por subsistema pendentes de rubrica da AVP.
