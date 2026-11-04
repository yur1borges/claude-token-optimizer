# Pendencias que dependem do Yuri

> Consolidado pelo controlador em 2026-10-20 22:10.
> Regra: nada aqui foi aplicado. Cada item precisa de decisao ou acao do Yuri.

## A. Seguranca (5 itens confirmados com arquivo:linha)

| # | Onde | Problema | Correcao proposta | Urgencia |
|---|---|---|---|---|
| A1 | `C:/Users/yuri/.omniroute/.env` | OmniRoute faz bind em `0.0.0.0:20128` sem `REQUIRE_API_KEY`. `GET http://10.14.13.188:20128/` responde 200 pela rede; `/v1/*` responde 401. Risco = superficie exposta, nao vazamento consumado. | 2 linhas: `OMNIROUTE_SERVER_HOST=127.0.0.1` e `REQUIRE_API_KEY=true`, depois reiniciar. Acessar do celular passa a depender do tunel `ssh_celular\`. | ALTA |
| A2 | `RadarPassagens/app/notify.py:19` e `:26` | Token do Telegram do Yuri em texto no arquivo (e possivelmente no log). | Rotacionar o token no BotFather e mover para variavel de ambiente / `.env` ignorado. | ALTA |
| A3 | `qe-flow/flowcalc/web/server.py:61` | Token exposto no corpo do POST `/api/run`. | Tirar do corpo; ler de env; nao logar. | ALTA |
| A4 | `dem_gpu.py:307` e `yade_worker.py:2058` | `pickle.load` em checkpoint = execucao arbitraria se o arquivo for trocado. | Trocar por formato proprio (JSON) ou no minimo `weights_only=True` + verificacao de assinatura. | MEDIA |
| A5 | `qt_app.py:862` | `rm -rf` com caminho construido - risco de apagar fora da area de trabalho se o path vier de entrada do usuario. | Delimitar o caminho dentro de uma pasta base, com `resolve()` e verificacao de prefixo. | MEDIA |

Ja resolvido por decisao do controlador (nao precisa do Yuri):
- Os 2 textos que mentem (`RadarPassagens/main.py:64-65` e `app/server.py:122`): corrigidos para mostrar enderecos de rede so quando o host != 127.0.0.1. Autorizado ao david (bf).
- SSH no-op: sem efeito real, anotado.

## B. Tarefas que so o Yuri destrava

| # | Tarefa | O que falta |
|---|---|---|
| B1 | T3 - Agente do Lattes | 1) login manual no navegador (a sessao NUNCA pede nem guarda senha/CPF em arquivo); 2) a lista das producoes novas (pasta, lista, ou Scholar/ORCID?); 3) confirmacao final antes de qualquer gravar/enviar no Lattes. |
| B2 | T5 - Pipeline de referencias | Tema final da busca (padrao DEM/Materiais ja liberado) e preferencia de idioma dos resumos. |
| B3 | T4 - Citacoes no Write | Rodar `/entrevista-pre-tarefa` uma vez para o teste real da skill (T1). |

## C. Como responder

Cada item pode ser marcado direto aqui:
- A1: `A1: aplicar` / `A1: adiar` / `A1: ja fiz`
- B1: login feito + caminho da lista de producoes
- B2: tema = ...
