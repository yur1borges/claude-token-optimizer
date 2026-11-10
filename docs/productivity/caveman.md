# caveman

**Resumo:** respostas tersas, sem cerimônia, mantendo todo fato técnico. É a skill que mais economiza no setup, porque ataca a saída do modelo.

## O que faz

Corta tudo o que não carrega informação:

- **some:** saudações, "claro, vou ajudar", ressalvas, resumo no fim repetindo o que foi dito, oferta de ajuda extra;
- **fica:** código, comandos, caminhos, números com unidade, mensagens de erro exatas, negações (não, nunca, só, exceto).

Tem níveis:

| Nível | Comando | Estilo |
|---|---|---|
| normal | `/caveman` | frases curtas, gramática inteira |
| ultra | `/ultracave` | fragmentos, só o conteúdo |
| mega | `/megacave` | compressão máxima |

Algumas coisas sempre saem em texto normal, mesmo no nível máximo: avisos de segurança, confirmação antes de ação irreversível, qualquer frase com dois sentidos possíveis e tudo o que é salvo fora do chat (código, commits, documentos).

## Como é acionada no meu setup

**Sempre ligada, no nível `ultracave`.** O plugin `caveman@caveman` injeta o modo por hook no início de cada sessão e reforça a cada mensagem. Por isso a skill fica `user-invocable-only`: já está ativa e não precisa ocupar a listagem. `caveman-commit` fica desligada (os commits seguem minha regra de uma vez por mês).

Os subagentes do plugin (`caveman:cavecrew-*`) estão **negados** em `permissions.deny`: eram chamados sem eu pedir e devolviam resultados fracos para meu tipo de trabalho.

## Quando usar

- Sempre, no terminal.

## Quando não usar

- Texto para outras pessoas (o modo já sai sozinho nesses casos).
- Quando eu estou confuso com uma resposta: aí peço explicação normal.

## Custo em tokens

- Custo fixo: o texto do modo injetado pelo hook a cada sessão (algumas centenas de tokens), que fica no cache.
- Economia: o próprio projeto diz que a saída cai de 40 a 60%. Não medi no meu uso. A saída é o token mais caro, então essa troca compensa.

## Por que está no setup

**Alternativas descartadas:**
- `Kulaxyz/token-diet`: faz o mesmo e soma outras regras (ler pouco, testar pouco) que já cubro com o ponytail e os hooks. Teria sobreposição.
- Só uma regra "seja breve" no CLAUDE.md: o modelo esquece depois de algumas respostas. O hook reforça a cada mensagem.

## Como saber que está funcionando

- As respostas vêm direto ao ponto, sem abertura nem fechamento.
- Comandos, caminhos e erros aparecem exatos.
