# taste-skill

**Resumo:** direção de arte para sites, contra o visual genérico de template. Baseada no estudo de 247 sites de galerias de design.

## O que faz

A taste-skill trata a página como um projeto de direção de arte, não como montagem de componentes. O fluxo tem dez passos:

1. Ler o pedido e o projeto existente.
2. Escrever o argumento: o que a página precisa convencer.
3. Escolher uma direção visual numa biblioteca de direções pesquisadas (ideia, composição, tipografia, paleta, fotografia, estrutura das seções).
4. Achar a ideia central da página.
5. Escrever os textos.
6. Construir.
7. Passar por um portão de qualidade com regras rígidas contra o visual genérico.
8. Olhar o resultado renderizado.
9. Ajustar o movimento.
10. Relatar o que foi feito.

## Como é acionada no meu setup

**Só com `/taste-skill`** (`user-invocable-only`). O plugin `taste-skill@taste-skill` está **desligado**; fica só a cópia local.

## Quando usar

- Página de apresentação, portfólio, site de projeto, em que a identidade visual importa.
- Quando o resultado do ui-ux-pro-max ficou correto mas sem personalidade.

## Quando não usar

- Interface de trabalho (formulário, tabela, dashboard): aí clareza vale mais que personalidade.
- App desktop.

## Custo em tokens

- Na listagem: zero (escondida).
- Quando chamada: ~34 KB (uns 8.500 tokens), a mais longa do setup, mais a biblioteca de direções. É o principal motivo de ficar escondida.

## Por que está no setup e por que escondida

Ela dá um resultado que as outras não dão: uma página com cara própria. Mas é cara e tem opiniões fortes, que brigam com as do ui-ux-pro-max. Fica guardada para quando o objetivo é justamente esse.

## Como saber que está funcionando

- A resposta começa pelo argumento e pela direção escolhida, não pelo código.
- O resultado não parece um template genérico de landing page.
