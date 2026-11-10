# humanizer

**Resumo:** tira os padrões de escrita de IA de um texto para que soe escrito por uma pessoa, sem mudar o conteúdo.

## O que faz

A skill começa explicando por que texto de IA soa como soa, e depois ataca os padrões um por um, por exemplo:

- **encenar em vez de dizer:** frases que anunciam o que vem ("Vamos mergulhar...") em vez de dizer;
- hesitações e ressalvas em excesso;
- listas de três itens por hábito, frases todas do mesmo tamanho;
- vocabulário típico de IA e conclusões que repetem o que já foi dito.

Ela devolve o texto reescrito na voz pedida. As referências por tipo de padrão só carregam quando preciso.

## Como é acionada no meu setup

**Só com `/humanizer`** (`user-invocable-only`).

## Quando usar

- E-mail, relatório, post ou texto acadêmico que vai para outras pessoas.
- Texto que já está correto mas "tem cara de IA".

## Quando não usar

- Código, comentários técnicos, respostas no terminal.
- Texto em que a precisão técnica importa mais que o estilo, sem revisão minha depois.

## Custo em tokens

- Na listagem: zero (escondida).
- Quando chamada: ~5,1 KB (uns 1.300 tokens).

## Por que está no setup e por que escondida

Uso com frequência em textos para fora, mas nunca no código. Visível, ela competiria com o caveman (que quer respostas curtas) a cada resposta. Escondida, não custa nada até eu precisar.

## Como saber que está funcionando

- O texto reescrito diz a mesma coisa, mais direto, sem as aberturas e fechamentos genéricos.
