# graphify

**Resumo:** monta um grafo do código (arquivos, funções, imports, chamadas) em `graphify-out/`. No meu setup serve só para localizar arquivos.

## O que faz

Analisa o código estaticamente e gera um grafo: os nós são arquivos e funções, as arestas são imports e chamadas. Com o grafo pronto, dá para perguntar "quem chama esta função?" ou "quais arquivos dependem deste módulo?" sem abrir os arquivos um a um.

O resultado fica em `graphify-out/` no projeto. As referências da skill só carregam no passo que pede.

## Como é acionada no meu setup

**Só com `/graphify`** (`user-invocable-only`). A regra no CLAUDE.md global é explícita: "graphify só localiza arquivos". Depois de achar o arquivo, leio por faixa ou com grep.

## Quando usar

- Repositório grande, em que não sei onde está uma função ou quem depende dela.
- Antes de uma refatoração que atravessa vários arquivos, para saber o tamanho do impacto.

## Quando não usar

- Para entender o código: ler o grafo inteiro custa mais que um grep certeiro.
- Repositório pequeno, em que um grep resolve.

## Custo em tokens

- Na listagem: zero (escondida).
- Quando chamada: ~5,3 KB (uns 1.300 tokens). O grafo em si pode ser grande; por isso consulto só o trecho necessário.

## Por que está no setup e por que limitada

Em repositório grande, achar o arquivo certo de primeira economiza várias leituras erradas. Mas o grafo vira armadilha se o modelo tenta lê-lo inteiro "para entender a arquitetura". Limitar o uso a localizar mantém o ganho e corta o risco.

## Como saber que está funcionando

- A resposta usa o grafo para apontar arquivo e linha, e depois lê só esse trecho.
