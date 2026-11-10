# verification-before-completion

**Resumo:** proibido dizer "pronto", "corrigido" ou "passou" sem ter rodado a verificação agora e mostrado a saída.

## O que faz

A regra central: **nenhuma afirmação de conclusão sem evidência nova de verificação**. "Nova" quer dizer rodada nesta mensagem; um teste que passou meia hora atrás, antes da última edição, não conta.

Antes de qualquer frase de sucesso, a skill manda passar por um portão:

1. Qual comando prova o que vou afirmar?
2. Rodar esse comando completo, agora.
3. Ler a saída inteira e o código de saída.
4. A saída confirma a afirmação? Se não, dizer o estado real, com a evidência.
5. Só então afirmar.

Ela lista as falhas comuns ("deve funcionar agora", "o linter passou, então compila", confiar no relatório de um subagente sem conferir) e as desculpas que o modelo costuma dar para pular a verificação, já com a resposta para cada uma.

## Como é acionada no meu setup

**Automática.** O CLAUDE.md global manda chamar antes de afirmar que algo está completo, corrigido ou passando, e antes de commit ou PR.

## Quando usar

- Antes de encerrar qualquer tarefa de código.
- Antes de commit e push.
- Ao receber o resultado de um subagente: o "terminei" dele também precisa de evidência.
- Em tarefa fora de código: a evidência é o arquivo criado, o processo rodando, o número medido.

## Quando não usar

- Pergunta que não termina com uma afirmação de "funciona" (explicação, pesquisa).

## Custo em tokens

- Na listagem: uma linha.
- Quando chamada: ~3,6 KB (uns 900 tokens). Sem referências extras.
- O custo real é uma execução de teste a mais por tarefa. Com o hook `filtra-testes.py`, essa execução devolve só o resumo ou as falhas, então sai barata.

## Por que está no setup

Um "pronto" falso é o erro mais caro que existe no meu fluxo. Eu descubro o problema depois, abro outra sessão, o modelo relê tudo do zero e refaz. Uma verificação de poucos segundos antes evita a sessão inteira de retrabalho.

**Alternativas descartadas:** escrever só "sempre teste" no CLAUDE.md. Funciona mal, porque a regra solta não lista as desculpas que o modelo usa para pular a verificação; a skill lista e responde cada uma.

## Como saber que está funcionando

- Toda resposta final de código traz o comando que rodou e a saída (por exemplo "34 passed").
- Quando algo falha, a resposta diz que falhou e mostra a saída, em vez de suavizar.
