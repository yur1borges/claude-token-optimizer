# task-observer

**Resumo:** observa as tarefas e anota correções minhas, padrões repetidos e métodos que valem guardar, para depois virarem melhorias nas skills.

## O que faz

Durante o trabalho, a skill registra num log do workspace:

- correções que eu faço no comportamento do modelo;
- trabalho que se repete e poderia virar uma skill nova;
- métodos que funcionaram e valem ser preservados.

Numa revisão periódica, transforma essas anotações em propostas de mudança nas skills e arquiva o que já foi tratado. Tem uma taxonomia para classificar cada observação e um protocolo para decidir quando mostrar uma sugestão.

## Como é acionada no meu setup

**Só com `/task-observer`** (`user-invocable-only`).

## Quando usar

- Numa sessão longa de trabalho, quando quero que os acertos e as correções virem melhorias nas skills.
- Na revisão das skills, para ver o que foi anotado.

## Quando não usar

- No dia a dia comum. É justamente por isso que fica escondida.

## Custo em tokens

- Na listagem: zero (escondida). A descrição original tem mais de 1.000 caracteres e pede para ser chamada antes da primeira ferramenta de **toda** sessão.
- Quando chamada: ~33 KB (uns 8.000 tokens), mais as escritas no log.

## Por que está no setup e por que escondida

A ideia é boa: o setup melhora com o uso. Mas, do jeito que vem, ela rodaria em toda sessão e gastaria milhares de tokens antes de qualquer trabalho. Escondida, eu ligo nas sessões em que quero colher aprendizado.

## Como saber que está funcionando

- O log de observações ganha entradas com o contexto e a sugestão.
- Na revisão, as entradas viram mudanças concretas em skills.
