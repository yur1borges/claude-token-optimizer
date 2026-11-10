# ADR 0001: Organização em buckets

## Decisão

Skills ficam em `skills/<bucket>/`:

- `engineering/`: uso diário em código (instaladas)
- `productivity/`: modo de trabalho (instaladas)
- `misc/`: uso raro (não instaladas)
- `in-progress/`: em teste (não instaladas)
- `deprecated/`: desligadas, mantidas como referência

## Por quê

Toda skill instalada entra na listagem de cada sessão e custa tokens. O bucket diz, só pelo caminho, se a skill está no contexto ou não. Aposentar é mover de pasta: o histórico fica, e voltar é um `git mv`.

Buckets promovidos (`engineering/`, `productivity/`) precisam estar no README principal.
