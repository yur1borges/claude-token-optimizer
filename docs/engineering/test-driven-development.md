# test-driven-development

**Resumo:** escrever o teste antes do código, ver o teste falhar, escrever o mínimo para passar, depois limpar.

## O que faz

A regra central: **nenhum código de produção sem um teste falhando antes**. Se o código foi escrito antes do teste, a skill manda apagar e recomeçar pelo teste.

O ciclo tem três passos, com verificação em cada um:

1. **Vermelho.** Escrever um teste pequeno para um comportamento só, com nome claro. Rodar e **ver falhar pelo motivo certo** (a função não existe ou devolve o valor errado, e não um erro de digitação no teste).
2. **Verde.** Escrever o código mais simples que faz o teste passar. Nada de opções ou recursos a mais. Rodar e ver passar, junto com os outros testes.
3. **Refatorar.** Tirar duplicação e melhorar nomes, mantendo tudo verde.

A skill também ensina como é um bom teste (um comportamento, nome que descreve, código real em vez de mock sempre que possível) e responde às desculpas comuns ("é simples demais para testar", "testo depois"). A referência `writing-good-tests.md` só carrega quando preciso.

## Como é acionada no meu setup

**Só com `/test-driven-development`** (`user-invocable-only` em `skillOverrides`). O modelo não a vê na listagem e não a chama sozinho.

## Quando usar

- Lógica nova com regra clara: parser, conversão de unidades, cálculo, validação.
- Bug que precisa de um teste de regressão.
- Refatoração de código sem testes: primeiro teste de caracterização, depois mexer.

## Quando não usar

- Ajuste visual em interface, texto, configuração.
- Script descartável de uma vez só.
- Edição de uma linha em código já coberto por teste.

## Custo em tokens

- Na listagem: zero (escondida).
- Quando chamada: ~9,6 KB (uns 2.400 tokens). É uma das mais longas, outro motivo para não disparar sozinha.

## Por que está no setup e por que escondida

TDD evita a pior forma de retrabalho: código que "parece certo" e quebra depois. Mas a descrição original dela diz "use ao implementar qualquer recurso ou correção". Se ficasse visível, o modelo carregaria 2.400 tokens e escreveria testes até para trocar uma cor de botão. Escondida, eu ligo nos casos em que vale.

O ponytail já cobre o caso pequeno: lógica nova não trivial deixa um teste curto ou uma autoverificação, sem o ritual completo.

## Como saber que está funcionando

- A primeira edição da tarefa é um arquivo de teste.
- A resposta mostra o teste falhando e depois passando.
- O código novo não tem nada que o teste não exija.
