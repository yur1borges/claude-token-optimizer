# teste-leigo

**Resumo:** testa meus apps desktop como um usuário leigo e impaciente: cliques aleatórios, entradas erradas, duplo clique, janela redimensionada. Acha o que quebra.

## O que faz

É uma skill **escrita por mim**. Ela usa um "macaco" (`macaco.py`) que controla o app de verdade, sem conhecer o código:

- clica em lugares aleatórios e em botões fora de ordem;
- digita texto em campo de número, campos vazios, valores enormes, caracteres especiais;
- dá duplo clique onde se espera clique simples, clica de novo antes de terminar;
- redimensiona, maximiza e minimiza a janela no meio de uma operação.

Cada app tem um adaptador (`adaptadores.py` e um por app) que diz onde ficam as janelas e quais telas existem. Há versões para app web (`macaco_web.py`) e Electron (`macaco_electron.js`). A skill tem regras de segurança (não apagar dados reais, trabalhar em cópia) e tira capturas de tela das falhas.

## Como é acionada no meu setup

**Automática** quando peço para testar um app desktop meu. Também uso antes de entregar uma versão nova.

## Quando usar

- Antes de entregar uma versão de um app com interface gráfica.
- Depois de mexer em formulários, diálogos ou fluxo de telas.

## Quando não usar

- Para testar lógica de cálculo: aí servem os testes unitários.
- Em app sem adaptador, até escrever um.

## Custo em tokens

- Na listagem: uma linha.
- Quando chamada: ~2,2 KB (uns 550 tokens). O macaco roda como script e devolve só o relatório de falhas, não o log inteiro.

## Por que está no setup

Nenhuma skill pública testa app desktop desse jeito. Testes unitários verificam a lógica; o macaco pega o que só aparece com um humano mexendo: travamento com duplo clique, erro com campo vazio, layout que quebra ao redimensionar. Encontrar isso antes poupa um ciclo de "o usuário achou, eu reabro a sessão, o modelo relê tudo".

## Como saber que está funcionando

- Sai um relatório com cada falha, o passo que a causou e a captura de tela.
- As falhas encontradas viram testes ou correções.
