# ui-ux-pro-max

**Resumo:** a skill de interface padrão do setup. Base de dados de estilos, paletas, fontes e regras de usabilidade, consultada por busca, para web, mobile e desktop.

## O que faz

Em vez de colocar todo o conhecimento de design no texto da skill, ela traz uma **base de dados em CSV** (cores, fontes, ícones, gráficos, tipos de página, interface de app, guias por tecnologia) e um script de busca. O modelo consulta só o que precisa para a tela em questão.

O fluxo:

1. **Analisar o pedido:** tipo de produto, público, estilo, tecnologia (React, Flutter, PyQt etc.).
2. **Gerar um design system** para páginas ou projetos novos: paleta, tipografia, espaçamentos, componentes. Pode salvar como um arquivo mestre com exceções por página, para manter a consistência entre sessões.
3. **Buscas complementares** quando precisa de algo específico: um tipo de gráfico, uma paleta para um setor, um padrão de formulário.
4. **Guia da tecnologia:** regras específicas da biblioteca usada.

As regras são ordenadas por prioridade: acessibilidade e contraste primeiro, depois áreas de toque, desempenho, layout, tipografia, animação, gráficos.

## Como é acionada no meu setup

**Automática.** O CLAUDE.md global manda chamar em qualquer trabalho de interface. O agente `design` também a usa.

## Quando usar

- Criar ou revisar tela, página, componente, dashboard.
- Corrigir problema de contraste, alinhamento, hierarquia visual.
- Escolher cores, fontes e tipo de gráfico para dados.
- Interfaces dos meus apps desktop em PyQt.

## Quando não usar

- Código sem interface (backend, cálculo, script).
- Página web de vitrine em que eu quero um resultado visual mais autoral: aí chamo `/taste-skill` ou `/impeccable`.

## Custo em tokens

- Na listagem: uma linha.
- Quando chamada: ~15,6 KB de instruções (uns 3.900 tokens). A base de dados **não** entra no contexto; só os resultados de cada busca, que são pequenos.

## Por que esta e não as outras

Eu tinha três skills de design (ui-ux-pro-max, impeccable e taste-skill), cada uma com a própria opinião sobre a mesma tela. Com as três visíveis, o modelo às vezes carregava duas e tentava satisfazer as duas, gastando o dobro e produzindo um resultado menos coerente.

Fiquei com esta como padrão porque:

- **Cobre desktop.** Meus programas são PyQt; as outras duas são focadas em web.
- **Consulta em vez de despejar.** O conhecimento fica na base de dados e só entra o trecho buscado. As outras colocam tudo no texto da skill.
- **Começa pela acessibilidade**, que é o que mais quebra em interface feita às pressas.

As outras duas continuam instaladas, mas só com `/nome`.

## Como saber que está funcionando

- A resposta cita a paleta, as fontes e as regras aplicadas, vindas da busca.
- O resultado passa nos critérios de contraste e não tem elementos pequenos demais para clicar.
- Telas diferentes do mesmo app mantêm o mesmo design system.
