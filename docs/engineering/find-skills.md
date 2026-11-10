# find-skills

**Resumo:** quando falta uma skill para uma tarefa, procura no catálogo público, confere a qualidade e mostra as opções antes de instalar.

## O que faz

Usa o CLI de skills e o ranking de skills mais usadas para achar candidatas. O fluxo:

1. Entender o que eu preciso.
2. Ver primeiro o ranking (as mais usadas costumam ser as mais confiáveis).
3. Buscar pelo termo da tarefa.
4. **Conferir a qualidade antes de recomendar:** quem mantém, quando foi atualizada, se a descrição bate com o conteúdo.
5. Mostrar as opções com o porquê.
6. Instalar só se eu aceitar.

## Como é acionada no meu setup

**Automática** quando pergunto como fazer algo para o qual talvez exista uma skill.

## Quando usar

- Tarefa nova e recorrente, que talvez já tenha uma skill pronta.
- Antes de escrever uma skill do zero.

## Quando não usar

- Tarefa de uma vez só: resolver direto sai mais barato que instalar uma skill.

## Custo em tokens

- Na listagem: uma linha.
- Quando chamada: ~5,2 KB (uns 1.300 tokens).

## Por que está no setup

É o que permite manter a lista pequena. Em vez de instalar pacotes grandes "por garantia" (o `ecc` sozinho trazia ~87 skills), procuro a skill certa na hora em que ela faz falta. Cada candidata ainda passa pelo filtro do [CONTRIBUTING](../../CONTRIBUTING.md): uso semanal, sem duplicar outra, e economia maior que o custo.

## Como saber que está funcionando

- A resposta mostra 1 a 3 opções com fonte e motivo, e não instala nada sem eu aceitar.
