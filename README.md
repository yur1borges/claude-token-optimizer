# claude-token-optimizer

O conjunto de skills, plugins, hooks e settings que uso no Claude Code para **gastar menos tokens sem perder qualidade**. Não é uma coleção grande de skills: é uma seleção pequena e de propósito, com o motivo de cada peça e de cada coisa que ficou de fora.

Estado de novembro de 2026. O setup completo, com cada setting e hook explicado, está em [docs/setup](./docs/setup/README.md).

## Por que tão poucas skills

Instalar skills é fácil; cada uma parece grátis. Não é. Mantive só 13 (11 de engenharia e 2 de produtividade) por quatro motivos:

1. **Toda skill visível é cobrada em toda sessão.** O nome e a descrição de cada skill entram na listagem do início, que faz parte do prefixo de todo turno. 100 skills com descrição de 150 caracteres são ~15 mil caracteres (uns 4 mil tokens) pagos antes de qualquer pergunta, mesmo que nenhuma seja usada.
2. **Muitas skills confundem a escolha.** Com dezenas de descrições parecidas ("design", "frontend", "UI"), o modelo chama a errada, chama duas, ou não chama nenhuma. Com uma skill por tipo de tarefa, o gatilho é claro: bug chama `systematic-debugging`, interface chama `ui-ux-pro-max`.
3. **Skills sobrepostas brigam.** Três guias de design ou dois modos de "resposta curta" dão instruções diferentes para a mesma coisa. O resultado é texto mais longo (o modelo tenta satisfazer as duas) e menos consistente.
4. **Rituais custam mais que economizam.** Skills que exigem um processo longo antes de toda tarefa (brainstorming, plano formal, conselho de 5 modelos) fazem sentido em projeto grande e novo. No dia a dia, com tarefas de 1 a 3 arquivos, elas gastam mais tokens do que poupam em retrabalho.

A regra que sobra: **uma skill entra só se eu uso toda semana, se não há outra fazendo o mesmo, e se ela economiza mais do que custa na listagem.** O resto fica desligado (movido para `~/.claude/skills_desligadas/`, sem apagar) e volta com um `mv` quando preciso.

## As skills e por que cada uma

### Engenharia: `skills/engineering/`

| Skill | O que faz | Por que esta e não outra |
|---|---|---|
| [systematic-debugging](./skills/engineering/systematic-debugging/SKILL.md) | acha a causa raiz antes de propor correção | evita o ciclo "tenta, erra, tenta", que é o maior desperdício de tokens em bug. Ganhou do `diagnosing-bugs` (mattpocock) por ser mais curta |
| [verification-before-completion](./skills/engineering/verification-before-completion/SKILL.md) | obriga a rodar o teste e ver a saída antes de dizer "pronto" | um "pronto" falso custa uma sessão inteira de volta. Barata e sempre útil |
| [test-driven-development](./skills/engineering/test-driven-development/SKILL.md) | escreve o teste antes do código | `user-invocable-only`: útil em lógica nova, caro demais se dispara em toda edição |
| [ui-ux-pro-max](./skills/engineering/ui-ux-pro-max/SKILL.md) | guia de interface (layout, cor, tipografia, acessibilidade) | a **única** de design chamada sozinha. Cobre web e desktop (meus apps são PyQt), o que as outras não fazem |
| [impeccable](./skills/engineering/impeccable/SKILL.md) | polimento fino de frontend web | só sob `/impeccable`: boa para página web caprichada, redundante com ui-ux-pro-max no resto |
| [taste-skill](./skills/engineering/taste-skill/SKILL.md) | direção de arte "anti-genérico" para sites | só sob demanda, pelo mesmo motivo. Mantida porque dá um resultado visual diferente quando quero |
| [teste-leigo](./skills/engineering/teste-leigo/SKILL.md) | testa app desktop como usuário impaciente | escrita por mim; nenhuma skill pública testa GUI desktop assim |
| [graphify](./skills/engineering/graphify/SKILL.md) | grafo de arquivos e chamadas do código | só para **localizar** arquivos em repo grande; ler o grafo inteiro custaria mais do que um grep |
| [humanizer](./skills/engineering/humanizer/SKILL.md) | tira padrões de texto de IA | só sob demanda, para textos que vão para pessoas (e-mail, relatório) |
| [find-skills](./skills/engineering/find-skills/SKILL.md) | procura e instala skill quando falta uma | evita instalar pacotes grandes "por garantia": busco a skill na hora que preciso |
| [task-observer](./skills/engineering/task-observer/SKILL.md) | anota correções e padrões para melhorar as skills | `user-invocable-only`: a descrição original pede para rodar em toda sessão, o que seria caro |

### Produtividade: `skills/productivity/`

| Skill | O que faz | Por que |
|---|---|---|
| [caveman](./skills/productivity/caveman/SKILL.md) | respostas tersas, sem cerimônia, todo fato técnico mantido | saída é o token mais caro; corta 40 a 60% do texto. Venceu o `token-diet`, que fazia o mesmo e mais coisas que eu não queria |
| [ponytail](./skills/productivity/ponytail/SKILL.md) | menor mudança que resolve a tarefa inteira | menos código escrito é menos saída, menos revisão e menos bug. Substituiu `mattpocock-skills` e `andrej-karpathy-skills`, que davam conselhos parecidos em mais texto |

As duas rodam por hook no início da sessão. Por isso ficam `user-invocable-only`: já estão ativas e não precisam ocupar a listagem.

### Desligadas: `skills/deprecated/`

| Skill | Por que saiu |
|---|---|
| [brainstorming](./skills/deprecated/brainstorming/SKILL.md) | exigia sessão de ideias antes de qualquer tarefa criativa; caro e quase sempre desnecessário |
| [writing-plans](./skills/deprecated/writing-plans/SKILL.md) | plano formal longo; trocado por um plano curto em arquivo só quando a tarefa tem mais de 3 passos |
| [llm-council](./skills/deprecated/llm-council/SKILL.md) | 5 "conselheiros" por decisão multiplicam o custo por 5 |

## Como o repo é organizado

```
skills/
  engineering/    uso diário em código (promovidas: vão para ~/.claude/skills)
  productivity/   modo de trabalho, fora do código (promovidas)
  misc/           guardadas, uso raro, não instaladas
  in-progress/    em teste, não instaladas
  deprecated/     desligadas, mantidas como referência
docs/
  engineering/    uma página por skill: o que faz, quando usar, por que está aqui
  productivity/
  setup/          meu setup real: settings, hooks, agentes, MCPs, com o porquê
.agents/          regras para quem edita o repo e decisões registradas (ADRs)
scripts/          instalação (link-skills.sh) e checagem (check.sh)
```

**Por que buckets:** separar "promovida" de "guardada" deixa claro o que entra no contexto. Só `engineering/` e `productivity/` são instaladas; tirar uma skill do setup é movê-la de pasta, sem perder o histórico.

**Por que skill e doc separadas:** o `SKILL.md` é lido pelo modelo e precisa ser curto. A página em `docs/` é para pessoas e pode explicar o contexto sem custar tokens.

**O que não está aqui:** skills pessoais (meus softwares de pesquisa, Lattes, DRX, DEM) e configurações com caminhos e chaves. Veja [SCOPE.md](./SCOPE.md).

## Instalação

```bash
git clone https://github.com/yur1borges/claude-token-optimizer
cd claude-token-optimizer
bash scripts/link-skills.sh
```

Cria links de cada skill promovida em `~/.claude/skills` e `~/.agents/skills` (serve para Claude Code e Codex). Rode de novo depois de `git pull`.

Checagem (frontmatter, links, travessões): `bash scripts/check.sh`

## Mais

- [docs/setup](./docs/setup/README.md): settings, plugins, hooks, subagentes e MCPs, com o porquê de cada um
- [AGENTS.md](./AGENTS.md): subagentes e quando delegar
- [CONTRIBUTING.md](./CONTRIBUTING.md): como adicionar ou aposentar uma skill
