# impeccable

**Resumo:** polimento fino de interface web: hierarquia, espaçamento, cor, movimento, texto da interface. Tem vários modos (criar, criticar, auditar, polir, simplificar, animar).

## O que faz

É uma skill de design para frontend com vários modos de trabalho, cada um com um objetivo:

- **criar ou redesenhar** uma tela;
- **criticar** ou **auditar**: lista o que está fraco e por quê;
- **polir**: os detalhes finos de espaçamento, alinhamento e tipografia;
- **simplificar**: tirar elementos que poluem;
- **endurecer**: estados vazios, erros, carregamento, textos longos;
- **animar**: movimento com propósito, respeitando quem pede menos animação.

Também documenta design systems (`DESIGN.md`, tokens) para que a próxima sessão siga o mesmo padrão. As referências e scripts da pasta só carregam no modo que precisa.

## Como é acionada no meu setup

**Só com `/impeccable`** (`user-invocable-only`). O plugin `impeccable@impeccable` está **desligado**: fica só a cópia em `~/.claude/skills/`, para não ter duas versões da mesma skill.

## Quando usar

- Página web que vai ser vista por muita gente e precisa de acabamento.
- Revisar uma interface pronta que "parece amadora" e descobrir o porquê.
- Fechar os estados de borda (vazio, erro, carregando) antes de entregar.

## Quando não usar

- Interface de app desktop do dia a dia: o ui-ux-pro-max cobre.
- Qualquer coisa sem interface.

## Custo em tokens

- Na listagem: zero (escondida). A descrição original tem mais de 600 caracteres; visível, seria uma das mais caras da listagem.
- Quando chamada: ~12 KB (uns 3.000 tokens), mais as referências do modo escolhido.

## Por que está no setup e por que escondida

No acabamento de página web ela vai mais longe que o ui-ux-pro-max. Mas no resto as duas se sobrepõem, e ter duas skills de design chamadas sozinhas gera instruções conflitantes. Escondida, ela não custa nada até eu chamar.

## Como saber que está funcionando

- A resposta diz qual modo usou e lista o que mudou e por quê.
- Estados vazios, de erro e de carregamento aparecem tratados.
