export const meta = {
  name: 'auditoria-flow-retry',
  description: 'Re-disparo da auditoria do Flow Calculation que falhou na rodada anterior',
  phases: [{ title: 'Auditar' }, { title: 'Verificar' }],
}

const COMMON = `
Voce e um auditor de seguranca e qualidade de codigo (papel: DAVID, agente de seguranca do Yuri).
ALVO: Flow Calculation (QE/CASTEP) em C:\\Users\\yuri\\OneDrive\\Desktop\\QE\\qe-flow

REGRAS DURAS (nao negociar):
- READ-ONLY. NAO edite, nao crie, nao apague NENHUM arquivo. Apenas Read/Grep/Glob. Nao rode comandos destrutivos.
- NUNCA imprima o VALOR de um segredo. Cite apenas caminho:linha e o NOME da variavel.
- Nao mexa no OmniRoute. Nao mexa em dem_gpu.py / yade_worker.py / runner.py do TriboDEM.
- Nao toco em rede: nao faca requisicao HTTP a servico externo.
- Escreva o relatorio em PORTUGUES DO BRASIL.

FOCO (em ordem):
1. Bug real: resultado errado, crash, edge case perdido, callers que discordam do que a funcao retorna, mesma regra aplicada de dois jeitos diferentes.
2. Seguranca: injecao (SQL, shell, path traversal), execucao de programa arbitrario, bind em 0.0.0.0, segredo em log, entrada do cliente nao validada, SSRF.
3. Perda de dado: erro engolido, escrita fora de ordem, sobrescrita sem backup.
4. Escala: race de check-then-write, O(n^2) com dados reais.
5. Falta de teste: logica arriscada sem teste que falhe se quebrar.
6. Codigo morto / duplicado / lean.

ARQUIVOS: flowcalc/*.py (analysis, cli, config, doctor, errors, executor, fila, graficos, inputs_only, limpeza, molecula, pseudos, relatar_erros, structure, vibracao, plots), flowcalc/gui/*.py, flowcalc/monitor/*.py, flowcalc/web/{dashboard,launcher,server}.py, flowcalc/engines/__init__.py.

JA CONHECIDO (nao repita como achado novo, mas confirme ou corrija se estiver errado):
- flowcalc/web/server.py hoje tem 3 bugs de uma edicao de 19/10 21:39: (a) linha 184 chama _dentro_do_projeto() que NAO EXISTE (existem _dentro_de na 41 e _raiz_permitida na 49) -> NameError -> HTTP 500 em POST /api/run com structure_path; (b) linha 54 usa tempfile.gettempdir() mas tempfile NAO esta nos imports (linhas 3-15) -> NameError; (c) _raiz_permitida (o guarda de path traversal) e codigo morto: definida, nunca chamada. Verifique se e isso mesmo e se ha MAIS bug da mesma edicao.
- O launcher usa FLOWCALC_HOST/QE_FLOW_HOST com default 127.0.0.1.
- fila.py usa flock, executor.py, limpeza.py e dashboard.py (Streamlit) ja foram lidos por mim.

COMO PROVAR CADA ACHADO:
- Cite caminho:linha EXATO.
- Mostre o trecho de codigo que PROVA.
- Diga o caso concreto: entrada/estado -> resultado errado.
- Confirme que o caminho e ALCANCAVEL de verdade (grep dos callers). Codigo morto NAO e achado.
- Se tem comentario "shortcut:"/"ponytail:" que nomeia o limite, e DECISAO, nao achado.

Severidade: critical = perda de dado do usuario, execucao de codigo nao confiavel, vazamento de segredo, resultado cientifico/financeiro errado silenciosamente. high = crash em fluxo comum, corrupcao, bypass de validacao, race com perda de escrita. medium = risco real com mitigacao parcial, bug em caso raro, entrada nao validada. low = limpeza, duplicacao, codigo morto, lentidao pequena.

FORMATO DE SAIDA: devolva SO o objeto JSON do schema. Sem texto antes, sem markdown. Se nao achou nada real: findings vazio. Nao invente achado para preencher.`

const SCHEMA = {
  type: 'object',
  properties: {
    app: { type: 'string' },
    resumo: { type: 'string' },
    nao_lido: { type: 'string' },
    findings: {
      type: 'array',
      maxItems: 5,
      items: {
        type: 'object',
        properties: {
          id: { type: 'string' },
          file: { type: 'string' },
          line: { type: 'integer' },
          severity: { type: 'string', enum: ['critical', 'high', 'medium', 'low'] },
          category: { type: 'string' },
          titulo: { type: 'string' },
          evidencia: { type: 'string' },
          caso: { type: 'string' },
          impacto: { type: 'string', description: 'paragrafo em portugues do Brasil pronto para enviar ao Yuri' },
          correcao: { type: 'string' },
          tamanho_fix: { type: 'string' },
          toca_fluxo_do_usuario: { type: 'boolean' },
          confianca: { type: 'string', enum: ['alta', 'media', 'baixa'] },
        },
        required: ['id', 'file', 'line', 'severity', 'category', 'titulo', 'evidencia', 'caso', 'impacto', 'correcao', 'tamanho_fix', 'toca_fluxo_do_usuario', 'confianca'],
      },
    },
  },
  required: ['app', 'resumo', 'nao_lido', 'findings'],
}

const VERDICT = {
  type: 'object',
  properties: {
    id: { type: 'string' },
    lente: { type: 'string' },
    refutado: { type: 'boolean' },
    razao: { type: 'string' },
    severidade_corrigida: { type: 'string', enum: ['critical', 'high', 'medium', 'low', 'inexistente'] },
  },
  required: ['id', 'lente', 'refutado', 'razao', 'severidade_corrigida'],
}

phase('Auditar')
const res = await agent(`${COMMON}\n\nTAREFA: audite o Flow Calculation inteiro. O codigo e grande: leia por simbolo (Grep/Read com offset), nao tudo de uma vez.`, {
  label: 'auditar:FlowCalculation',
  phase: 'Auditar',
  schema: SCHEMA,
  effort: 'high',
})

const achados = (res && res.findings) ? res.findings : []
if (!achados.length) return { app: 'FlowCalculation', resumo: res ? res.resumo : 'sem resultado', nao_lido: res ? res.nao_lido : '', achados: [] }

const LENTES = [
  { nome: 'caminho-real', p: 'Lente "caminho real": o codigo apurado E realmente alcancavel no app como ele roda hoje? Grep dos callers, verifique se a funcao e chamada por algum entrypoint real (FlowCalculation.py, CLI, worker, thread, launcher). Se esta em codigo morto, pasta de backup ou nunca chamado, NAO se sustenta. Verifique tambem se a validacao nao existe em outro lugar. Se nao sustenta -> refutado=true.' },
  { nome: 'reproducao', p: 'Lente "reproducao": consegue construir o caso concreto (entrada/estado exato) que produz o resultado errado? Relia o codigo, nao confie no relato. Se o cenario e imaginario ou o codigo ja trata o caso -> refutado=true. Se sustenta, escreva o passo-a-passo.' },
  { nome: 'severidade', p: 'Lente "severidade": dado o uso REAL (Yuri roda local, um usuario, Windows com WSL, calculos de pesquisa que duram horas), a severidade esta correta? Resultado cientifico errado silenciosamente e grave. Bug de UI -> baixo. Considere o que acontece DEPOIS: o Yuri perde dado, perde resultado, ou ve erro claro?' },
]

const vereditos = await parallel(achados.flatMap((f) => LENTES.map((L) => () =>
  agent(`${COMMON}\n\nVoce e o VERIFICADOR adversarial. Missao: DERRUBAR o achado. Padrao: se ficar na duvida, refutado=true.\n\nACHADO SOB EXAME:\nid: ${f.id}\narquivo: ${f.file}:${f.line}\nseveridade alegada: ${f.severity}\ncategoria: ${f.category}\ntitulo: ${f.titulo}\nevidencia alegada: ${f.evidencia}\ncaso alegado: ${f.caso}\ncorrecao proposta: ${f.correcao}\n\n${L.p}\n\nVerifique no codigo real, nao na narrativa. Cite caminho:linha do que voce leu.`, {
    label: `verificar:${f.id}:${L.nome}`,
    phase: 'Verificar',
    schema: VERDICT,
    effort: 'high',
  })
)))

const vv = vereditos.filter(Boolean)
const out = achados.map((f) => {
  const meus = vv.filter((v) => v.id === f.id)
  const refutadores = meus.filter((v) => v.refutado).length
  const naoRefutado = meus.filter((v) => !v.refutado).length
  return { ...f, vereditos: meus.map((v) => ({ lente: v.lente, refutado: v.refutado, razao: v.razao, sev: v.severidade_corrigida })), sobreviveu: meus.length > 0 && naoRefutado > refutadores }
})

return { app: 'FlowCalculation', resumo: res.resumo, nao_lido: res.nao_lido, achados: out }
