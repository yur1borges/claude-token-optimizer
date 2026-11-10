# systematic-debugging

**Resumo:** antes de corrigir qualquer bug, achar a causa raiz. Nada de "tentar uma coisa e ver se resolve".

## O que faz

A skill impõe uma regra central, chamada de "lei de ferro": **nenhuma correção sem investigar a causa raiz primeiro**. Corrigir o sintoma conta como falha, mesmo em bug simples.

O trabalho segue quatro fases, sem pular nenhuma:

1. **Causa raiz.** Ler a mensagem de erro inteira, reproduzir o problema de forma confiável, ver o que mudou recentemente (git diff, dependências, configuração) e rastrear de onde vem o valor errado, voltando pela pilha de chamadas até a origem.
2. **Padrão.** Procurar no próprio código um caso parecido que funciona e comparar com o que quebra. A diferença costuma ser a causa.
3. **Hipótese.** Escrever uma hipótese só ("X causa o erro porque Y") e testar com a menor mudança possível. Uma variável por vez.
4. **Correção.** Criar um teste que reproduz o bug, corrigir na origem (não no ponto onde o erro aparece) e confirmar que o teste passa e nada mais quebrou.

Também traz uma lista de sinais de alerta que mandam voltar à fase 1, como "vou só tentar isso rapidinho" ou a terceira correção seguida que não funcionou. A partir da terceira tentativa falha, a skill manda questionar a arquitetura em vez de insistir.

A pasta da skill traz referências que só carregam quando a fase pede: rastreamento de causa raiz, defesa em profundidade, espera por condição (para testes instáveis por tempo) e um script para achar qual teste polui o estado dos outros.

## Como é acionada no meu setup

**Automática.** O CLAUDE.md global manda chamar sozinho em qualquer bug, teste falhando ou comportamento inesperado, antes de propor correção. Os subagentes recebem a mesma regra em `regras_agentes.md`.

## Quando usar

- Teste falhando, exceção, crash.
- Resultado numérico estranho em cálculo (energia que não converge, espectro deslocado).
- Comportamento que "às vezes" acontece.
- Sempre que já houve uma tentativa de correção que não resolveu.

## Quando não usar

- Erro de digitação óbvio, com a linha e a causa já na mensagem. Mesmo aí a fase 1 é rápida, então na prática a skill roda e termina em segundos.

## Custo em tokens

- Na listagem: uma linha de descrição.
- Quando chamada: ~2,2 KB de texto (uns 550 tokens). As referências só entram se a fase precisar.

## Por que está no setup

Bug é onde mais se desperdiça token. Cada tentativa errada custa uma edição, uma execução de teste e uma leitura de log, e o contexto vai enchendo de tentativas mortas. Exigir a causa raiz antes troca várias rodadas baratas e erradas por uma investigação certa.

**Alternativas descartadas:**
- `mattpocock-skills:diagnosing-bugs`: mesma ideia, texto mais longo e com mais cerimônia. O plugin inteiro ficou desligado.
- Sem skill nenhuma: o modelo tende a propor correção na primeira resposta, antes de reproduzir o erro.

## Como saber que está funcionando

- A resposta começa reproduzindo o erro e mostrando a causa, com arquivo e linha, antes de qualquer edição.
- A correção vem com um teste que falhava antes e passa depois.
- Não aparecem três correções seguidas no mesmo ponto.
