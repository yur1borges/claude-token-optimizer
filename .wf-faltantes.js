export const meta = {
  name: 'auditoria-faltantes-3-apps',
  description: 'Auditoria de seguranca+qualidade de DA, Write e TriboDEM (os 3 que nao devolveram resultado na rodada anterior)',
  phases: [{ title: 'Auditar' }, { title: 'Verificar' }],
}

const COMMON = `
Voce e um auditor de seguranca e qualidade de codigo (papel: DAVID, agente de seguranca do Yuri).
ALVO: %ALVO%
PASTA: %PASTA%

REGRAS DURAS (nao negociar):
- READ-ONLY. NAO edite, nao crie, nao apague NENHUM arquivo. Apenas Read/Grep/Glob. Nao rode comandos destrutivos.
- NUNCA imprima o VALOR de um segredo. Cite apenas caminho:linha e o NOME da variavel.
- NUNCA use dados reais do Yuri (pastas de medidas, DRX, resultados de lote). Só nomes de arquivo e caminhos.
- Nao mexa em dem_gpu.py, runner.py, yade_worker.py do TriboDEM (pode ter calculo rodando).
- Nao toque em rede: nao faca requisicao HTTP a servico externo. Nao instale nada.
- Escreva o relatorio em PORTUGUES DO BRASIL.

FOCO (em ordem):
1. Bug real: resultado errado, crash, edge case perdido, callers que discordam do que a funcao retorna, mesma regra aplicada de dois jeitos diferentes.
2. Seguranca: injecao (SQL, shell, path traversal), execucao de programa arbitrario, bind em 0.0.0.0, segredo em log, entrada do cliente nao validada, SSRF, desserializacao insegura.
3. Perda de dado: erro engolido, escrita fora de ordem, sobrescrita sem backup, estado nao persistido.
4. Escala: race de check-then-write, O(n^2) com dados reais, trabalho repetido.
5. Falta de teste: logica arriscada sem teste que falhe se quebrar.
6. Codigo morto / duplicado / lean.

COMO PROVAR CADA ACHADO:
- Cite caminho:linha EXATO.
- Mostre o trecho de codigo que PROVA.
- Diga o caso concreto: entrada/estado -> resultado errado.
- Confirme que o caminho e ALCANCAVEL de verdade (grep dos callers). Codigo morto NAO e achado.
- Se tem comentario "shortcut:"/"ponytail:" que nomeia o limite, e DECISAO, nao achado.
- Se algo e documentado como limitacao consciente em README/TAREFAS/docs, nao e achado.

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
      maxItems: 6,
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

const APPS = [
  {
    nome: 'DA',
    pasta: 'C:\\Users\\yuri\\OneDrive\\Desktop\\Claude\\DA',
    alvo: 'DA (Data Analyzer, ex-RPA) - app Qt de analise de dados / DRX',
    extra: `
ARQUIVOS PRIORITARIOS: DataAnalyzer.py, modulos de analise (espectro, termico, deconvolucao), leitura de .rpa, exportacao (fit, PNG, CSV), i18n, testes na raiz (*_test.py).
CUIDADO: as pastas de dados do Yuri ("dados l-arginine cl25%", "teste 2", "teste de deconvolucao como no fityk") nao devem ser lidas. Foque no codigo.
CUIDADO: Origem e proprietário - nao tente descompilar nada binario.`,
  },
  {
    nome: 'Write',
    pasta: 'C:\\Users\\yuri\\OneDrive\\Desktop\\Claude\\Write',
    alvo: 'Write - editor de texto estilo Word (Electron, Node + renderer)',
    extra: `
ARQUIVOS PRIORITARIOS: main.js / app principal Electron, preload.js, renderer (HTML/CSS/JS), ipc handlers, leitura/escrita de arquivo no disco, auto-save, exportacao (docx/pdf/md), testes em testes\\t_*.js.
FOCO ESPECIFICO: Electron com nodeIntegration/contextIsolation habilitados = risco de execucao remota. Verifique o webPreferences do BrowserWindow, o que o preload expoe, se ha contextIsolation:false ou nodeIntegration:true, se ha CSP, se o IPC valida o que recebe, se abre arquivo de caminho arbitrario.
Nao rode o app. Nao instale nada.`,
  },
  {
    nome: 'TriboDEM',
    pasta: 'C:\\Users\\yuri\\OneDrive\\Desktop\\MESTRADO PPGTIM\\DEM\\TriboDEM_Studio',
    alvo: 'TriboDEM Studio - simulacao DEM (particulas, moinho, correia, caçamba)',
    extra: `
ARQUIVOS PRIORITARIOS: tribodem/*.py (experiments.py, yade_worker.py, dem_gpu.py, runner.py, render.py, alinhamento.py, pecas_padrao.py, minerios.py, vida_util.py), TriboDEM.pyw, qt_app.py, cad_qt.py, config/*.yaml, cli/analise/pos-processamento.
JA CONHECIDO (nao repita, mas confirme/corrija):
- dem_gpu.py:307 e yade_worker.py:2058 usam pickle.load no checkpoint ANTES de conferir o SHA1. O SHA1 valida o CASO, nao a ORIGEM do arquivo. Mitigacao atual: TRIBODEM_SEM_RETOMAR=1. Nao mexa nesses arquivos.
- A serializacao em yade_worker / dem_gpu e grande; foque no resto.
FOCO ESPECIFICO: execucao de subprocesso/shell (rotas, yadedaily, dem-gpu), path traversal em nome de pasta de saida, YAML/JSON de config nao validado, leitura de .stl/.tdcad/.cif de origem externa, o que acontece com resultado科学 errado silenciosamente (criterio de convergencia, PSD, taxa de alimentacao), escrita de resultados em disco (sobrescreve pasta do lote anterior?), e o caminho de "abrir pasta de resultado".
CUIDADO: pode ter LOTE RODANDO. Nao rode, nao escreva, nao apague nada.`,
  },
]

phase('Auditar')
const resultados = await parallel(APPS.map((a) => () =>
  agent(`${COMMON.replace('%ALVO%', a.alvo).replace('%PASTA%', a.pasta)}\n${a.extra}`, {
    label: `auditar:${a.nome}`,
    phase: 'Auditar',
    schema: SCHEMA,
    effort: 'high',
  })
))

const LENTES = [
  { nome: 'caminho-real', p: 'Lente "caminho real": o codigo apurado E realmente alcancavel no app como ele roda hoje? Grep dos callers, verifique se a funcao e chamada por algum entrypoint real (script principal, CLI, worker, thread, handler de janela). Se esta em codigo morto, pasta de backup, deprecado ou nunca chamado, NAO se sustenta. Verifique tambem se a validacao nao existe em outro lugar. Se nao sustenta -> refutado=true.' },
  { nome: 'reproducao', p: 'Lente "reproducao": consegue construir o caso concreto (entrada/estado exato) que produz o resultado errado? Relia o codigo, nao confie no relato. Se o cenario e imaginario ou o codigo ja trata o caso -> refutado=true. Se sustenta, escreva o passo-a-passo.' },
  { nome: 'severidade', p: 'Lente "severidade": dado o uso REAL (Yuri roda local, um usuario, Windows, calculos de pesquisa que duram horas, app de Uso diario), a severidade esta correta? Resultado cientifico errado silenciosamente e grave. Bug de UI -> baixo. Considere o que acontece DEPOIS: o Yuri perde dado, perde resultado, ou ve erro claro?' },
]

const todos = []
for (let i = 0; i < APPS.length; i++) {
  const res = resultados[i]
  if (!res || !res.findings || !res.findings.length) continue
  for (const f of res.findings) {
    const thunks = LENTES.map((L) => {
      const p = `${COMMON.replace('%ALVO%', APPS[i].alvo).replace('%PASTA%', APPS[i].pasta)}\n\nVoce e o VERIFICADOR adversarial. Missao: DERRUBAR o achado. Padrao: se ficar na duvida, refutado=true.\n\nACHADO SOB EXAME:\nid: ${f.id}\narquivo: ${f.file}:${f.line}\nseveridade alegada: ${f.severity}\ncategoria: ${f.category}\ntitulo: ${f.titulo}\nevidencia alegada: ${f.evidencia}\ncaso alegado: ${f.caso}\ncorrecao proposta: ${f.correcao}\n\n${L.p}\n\nVerifique no codigo real, nao na narrativa. Cite caminho:linha do que voce leu.`
      return () => agent(p, {
        label: `verificar:${APPS[i].nome}:${f.id}:${L.nome}`,
        phase: 'Verificar',
        schema: VERDICT,
        effort: 'high',
      })
    })
    const vv = await parallel(thunks)
    const meus = vv.filter(Boolean).filter((v) => v.id === f.id)
    const refutadores = meus.filter((v) => v.refutado).length
    const naoRefutado = meus.filter((v) => !v.refutado).length
    todos.push({ app: APPS[i].nome, ...f, vereditos: meus.map((v) => ({ lente: v.lente, refutado: v.refutado, razao: v.razao, sev: v.severidade_corrigida })), sobreviveu: meus.length > 0 && naoRefutado > refutadores })
  }
}

return { apps: APPS.map((a, i) => ({ nome: a.nome, resumo: resultados[i] ? resultados[i].resumo : 'sem resultado', nao_lido: resultados[i] ? resultados[i].nao_lido : '', n_findings: resultados[i] && resultados[i].findings ? resultados[i].findings.length : 0 })), achados: todos }
