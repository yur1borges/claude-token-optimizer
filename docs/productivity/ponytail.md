# ponytail

**Resumo:** "dev sênior preguiçoso": a menor mudança que resolve a tarefa inteira. Menos código escrito é menos saída, menos revisão e menos bug.

## O que faz

Antes de escrever código, a skill faz uma escada de perguntas e para no primeiro degrau que resolve:

1. Isso precisa existir? Recurso, opção ou flexibilidade que ninguém pediu fica de fora.
2. Já existe neste projeto? Usar o helper, o componente ou o padrão que já está lá.
3. A biblioteca padrão ou a plataforma resolve?
4. Uma dependência já instalada resolve? Nunca adicionar dependência por poucas linhas.
5. Cabe numa linha que se entende de cara?
6. Só então, o mínimo de código que funciona.

Ela é preguiçosa na solução, **nunca na mudança**: termina tudo o que a tarefa exige, incluindo quem chama a função, os testes e os dados de teste que a mudança afeta. Em correção de bug, manda procurar todos os pontos que chamam a função e corrigir uma vez, na origem. Lógica nova não trivial deixa um teste curto.

Nunca corta: validação de entrada de fonte externa, tratamento de erro que evita perda de dados, segurança, acessibilidade.

## Como é acionada no meu setup

**Sempre ligada, no nível `full`.** O plugin `ponytail@ponytail` injeta o modo por hook no início de cada sessão. A skill fica `user-invocable-only`, assim como `ponytail-audit` (auditoria de repositório inteiro, que chamo quando quero).

## Quando usar

- Toda tarefa de código.

## Quando não usar

- Quando eu peço explicitamente algo completo ou extensível; o pedido explícito vence.

## Custo em tokens

- Custo fixo: o texto do modo injetado pelo hook a cada sessão, que fica no cache.
- Economia: diffs menores, menos arquivos criados, menos rodadas de revisão. Não medi em número.

## Por que está no setup

**Alternativas descartadas:**
- `mattpocock-skills` e `andrej-karpathy-skills`: davam conselhos parecidos (simplicidade, não abstrair cedo) em muito mais texto, e somavam milhares de tokens fixos por sessão. Os dois plugins ficaram desligados.
- `ecc` (everything-claude-code): tinha regras próprias de qualidade, mas o pacote todo era pesado demais.

Junto com o caveman, cobre os dois lados da saída: o caveman encurta o texto e o ponytail encurta o código.

## Como saber que está funcionando

- O diff é menor que a solução óbvia e não traz código "para depois".
- No fim da resposta, uma ou duas linhas dizem o que foi pulado e o risco que fica.
