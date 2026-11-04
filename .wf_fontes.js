export const meta = {
  name: 'fontes-abertas-g99-g133',
  description: 'Caca e verificacao adversarial de fontes abertas com numeros medidos de desgaste para pino-disco (ASTM G99) e esfera-disco (ASTM G133), com prioridade LFS-USP',
  phases: [
    { title: 'Caca', detail: '6 agentes em canais distintos atras de fonte aberta com numeros' },
    { title: 'Verificacao', detail: 'refutar cada candidato: URL viva, trecho literal, DOI Crossref' },
    { title: 'Sintese', detail: 'ranquear e consolidar o que sobrevive' },
  ],
}

var CTX = [
  'Contexto: projeto TriboDEM (Mestrado PPGTIM, Vale/ITV/LFS-USP). Precisamos de FONTES ABERTAS (acesso livre, texto completo legivel) com NUMEROS DE DESGASTE MEDIDOS para servir de referencia de comparacao com o codigo DEM.',
  'Alvo 1 - Pino-disco (ASTM G99): par AISI 52100 (pino) x AISI 1045 (disco), 10 N, 0,1 m/s, 1000 m, ponta hemisférica R=5,0 mm (Ø10 mm), pista R=16,0 mm.',
  'Alvo 2 - Esfera-disco (ASTM G133 / ball-on-disk alternado): esfera Ø9,525 mm, curso 10 mm, 5 Hz, 100 m.',
  'Prioridade da busca: (a) artigos da LFS-USP / Escola de Engenharia de Lorena (Sinatora, Machado, Tressia, Pintaúde, Viana, Penagos, Assis) com acesso aberto; (b) artigos open-access genericos de pin-on-disk e ball-on-disk em MDPI / SpringerOpen / Elsevier OA / Archives of Foundry Engineering / Tribology Online / DergiPark / journals.pan.pl / Coatings / Lubricants / Metals / Wear com numeros medidos.',
  'REGRAS DURAS (a entrega e reprovada se violar):',
  '1. DOI DEVE existir e ser conferido em https://api.crossref.org/works/<doi> devolvendo HTTP 200 com title/autores/ano que batem com a citacao. Guarde o JSON cru.',
  '2. Deve haver URL de TEXTO COMPLETO em acesso aberto (PDF direto). Resumo sozinho NAO basta; marque [so resumo] se for o caso.',
  '3. O TRECHO tem de ser LITERAL do texto completo (copiar as palavras exatas), com pagina/secao/tabela; e os NUMEROS (taxa de desgaste em mm3/(N.m) ou mm3/m, coeficiente k, volume perdido) tem de estar nessa passagem.',
  '4. Declare a GEOMETRIA (carga, velocidade, distancia, tamanho da contraparte, norma, materiais) e diga onde CONCORDA e onde DIVERGE do alvo acima. Se o material for diferente do do codigo, diga explicitamente que a comparacao nao e direta.',
  'Ferramentas: WebSearch, WebFetch, Bash com curl (para PDF) e python + pymupdf para extrair texto. No Git Bash /tmp equivale a C:/Users/yuri/AppData/Local/Temp. A pasta do projeto e C:/Users/yuri/OneDrive/Desktop/MESTRADO PPGTIM/DEM/TriboDEM_Studio (somente LEITURA; nao edite nada la).',
  'NAO edite nenhum arquivo .py nem docs. Apenas pesquise e reporte.'
].join('\n\n')

var SCHEMA = {
  type: 'object',
  properties: {
    candidatos: {
      type: 'array',
      items: {
        type: 'object',
        properties: {
          citacao: { type: 'string' },
          doi: { type: 'string' },
          crossref_json: { type: 'string' },
          url_aberto: { type: 'string' },
          status_http: { type: 'string' },
          trecho_literal: { type: 'string' },
          onde: { type: 'string' },
          numeros: { type: 'string' },
          geometria: { type: 'string' },
          bate: { type: 'string' },
          diverge: { type: 'string' },
          materiais: { type: 'string' },
          alvo: { type: 'string' },
        },
        required: ['citacao', 'doi', 'url_aberto', 'trecho_literal', 'onde', 'numeros', 'geometria', 'diverge', 'alvo'],
      },
    },
    notas: { type: 'string' },
  },
  required: ['candidatos'],
}

var CANAIS = [
  { chave: 'lfs-usp-journal', rot: 'LFS-USP / Escola de Engenharia de Lorena em ABERTO', prompt: 'Procure no Google Scholar, na pagina da revista Wear (Elsevier) via DOAJ/OpenAlex/Unpaywall, no portal da USP (teses.usp.br, periodicos.usp.br, revistas.usp.br), no ResearchGate/Academia.edu de acesso livre e no repositorio da UFOP/ITV (repositorio.itv.org) ARTIGOS DE PERIODICO do LFS-USP/Escola de Lorena sobre DESGASTE por DESLIZAMENTO em pino contra disco, pino-disco, esfera-disco ou wear map, com numeros medidos. Autores-alvo: Amilton Sinatora, Marcelo Piscottini Machado, Gustavo Tressia de Andrade, Thiago Gomes Viana, Giuseppe Pintaude, Wellington Moreira, PauloAssist, R. Torres. Use a API do OpenAlex e do Unpaywall para achar a versao ABERTA (oa_location) de artigos que no Crossref apontem para Elsevier/Springer. Traga PDF aberto.' },
  { chave: 'mdpi-swe', rot: 'MDPI / SpringerOpen / Elsevier OA (wear maps e PoD)', prompt: 'Procure em MDPI (Coatings, Lubricants, Metals, Machines, Proceedings), SpringerOpen (Journal of Engineering Tribology), Elsevier OA (Tribology International, Wear) ARTIGOS OPEN ACCESS com TABELA de taxa de desgaste para pino-disco (ASTM G99) e/ou ball-on-disk alternado (ASTM G133), com pares de materiais que incluam AISI 52100, 100Cr6, AISI 1045 ou aco-carbono equivalente. Priorize quem cite e reproduza as tabelas interlaboratorias do G99 (10 N, 0,1 m/s, 1000 m, 52100 x 52100) ou do G133. Traga DOI conferido no Crossref e o PDF aberto com o trecho literal e a tabela.' },
  { chave: 'g99-interlab', rot: 'Replicacoes/tabelas interlaboratorias G99-G133', prompt: 'O gargalo original: as TABELAS INTERLABORATORIAS do ASTM G99 (par 52100 temperado x 52100, 10 N, 0,1 m/s, 1000 m) e do ASTM G133 estao em paywall. Encontre ARTIGOS open-access, relatorios tecnicos de NPL/BSI/NIST, notas de catalogo ou teses que REPRODUZAM essas tabelas de volumes/taxas de desgaste com numeros. Busque tambem o programa interlaboratorial do ASTM G99 (materials and data) citado em literatura, e normas tecnicas de terceiros (JIS, GOST, EN) que transcrevam a tabela. Qualquer fonte aberta com o numero medido do par 52100 x 52100 a 10 N/1000 m vale ouro. Traga o trecho literal da tabela e a URL aberta.' },
  { chave: 'g133-ball-disk', rot: 'Ball-on-disk alternado ASTM G133 (esfera-disco)', prompt: 'Foque em ensaios BALL-ON-DISK LINEARMENTE ALTERNADO conforme ASTM G133 (reciprocating ball on flat, curso ~10 mm, 1-10 Hz) com numeros de desgaste: 100Cr6/52100 sphere on steel flat, alumina, anodized aluminium, coated surfaces. Fontes: MDPI, Coatings, Tribology Online, Archives of Foundry Engineering, journals.pan.pl, DergiPark, Indian journals (IJETR, IJRTE), teses USP (teses.usp.br, periodicos.usp.br). Traga DOI Crossref, PDF aberto, trecho literal e numeros em mm3/(N.m).' },
  { chave: 'iso7148', rot: 'ISO 7148 e normas de Mancal', prompt: 'Verifique se a norma ISO 7148 (plain bearings, wear) tem ALGUM texto integral aberto: preview gratuito ISO (iso.org/standard/54483.html e vizinhos), catalogos de preview de normas (iTeh, SAI Global, Techstreet, ANSI webstore, BSI shop), normas citadas em dissertacoes que transcrevam as tabelas de ensaio, ou a norma citada em teses da USP com apendice de dados. Alem disso: o metodo de ensaio ASTM G99 esta resumido em manuais/livros digitalizados abertos (Google Books preview, Internet Archive, USP biblioteca digital). Objetivo: um numero medido de desgaste do par 52100 x 52100 em norma aberta. Traga o que for encontrado com DOI/URL e trecho literal; se realmente nao houver, declare isso claramente com as evidencias de busca (o que tentou e o que respondeu).' },
  { chave: 'multimodal', rot: 'Busca por API (Crossref/OpenAlex/Unpaywall/Semantic Scholar/Internet Archive)', prompt: 'Use APIs em vez de busca web: (1) Crossref REST https://api.crossref.org/works?query.bibliographic=... ; (2) OpenAlex https://api.openalex.org/works?search=... com filtro open_access.is_oa=true e filter=type:dissertation ; (3) Unpaywall https://api.unpaywall.org/v2/<doi>?email= ; (4) Semantic Scholar API; (5) Internet Archive full-text search; (6) OpenAIRE. Objetivo: achar QUALQUER texto aberto (incluindo teses da USP/Escola de Engenharia de Lorena) com taxa de desgaste medida em pino contra disco ou esfera contra disco com numeros, preferencialmente par 52100. Para teses USP o padrao de URL e http://www.teses.usp.br/teses/disponiveis/3/3151/<tde-id>/publico/<arquivo>.pdf e o nome do arquivo se acha na pagina pt-br.html. Traga DOI conferido, URL aberta, trecho literal e numeros.' },
]

phase('Caca')
var achados = await parallel(CANAIS.map(function (c) {
  return function () {
    return agent(CTX + '\n\n=== CANAL: ' + c.rot + ' ===\n' + c.prompt + '\n\nTraga ate 3 candidatos por canal, so os que voce de fato abriu e leu.', { label: c.chave, phase: 'Caca', schema: SCHEMA })
      .then(function (r) { return { canal: c.chave, rot: c.rot, r: r } })
  }
}))

var todos = []
achados.filter(Boolean).forEach(function (a) {
  var cs = (a.r && a.r.candidatos) || []
  cs.forEach(function (k) { k.canal = a.canal; todos.push(k) })
})
log('Caca: ' + todos.length + ' candidatos brutos de ' + CANAIS.length + ' canais')

phase('Verificacao')
var V = {
  type: 'object',
  properties: {
    doi_ok: { type: 'boolean' },
    crossref_evidencia: { type: 'string' },
    url_viva: { type: 'boolean' },
    status_e_bytes: { type: 'string' },
    trecho_confere: { type: 'boolean' },
    trecho_corrigido: { type: 'string' },
    numeros_confere: { type: 'boolean' },
    paginacao_confere: { type: 'boolean' },
    sobrevive: { type: 'boolean' },
    motivo: { type: 'string' },
  },
  required: ['doi_ok', 'url_viva', 'trecho_confere', 'numeros_confere', 'sobrevive', 'motivo'],
}

var vereditos = await parallel(todos.map(function (k, i) {
  return function () {
    return agent(CTX + '\n\nVoce e um VERIFICADOR ADVERSARIAL. Tente REFUTAR este candidato. So marque sobrevive=true se TODOS verificarem.\n\nCANDIDATO:\n' + JSON.stringify(k, null, 2) + '\n\nTarefas: (1) curl https://api.crossref.org/works/' + encodeURIComponent(k.doi) + ' e confirme HTTP 200, title, container-title, issued e autores BATEM com a citacao informada; (2) baixe a URL ' + k.url_aberto + ' e confirme que e texto completo (PDF com > 4 paginas, ou HTML longo) e que o TRECHO LITERAL aparece no texto; extraia o trecho real e devolva em trecho_corrigido; (3) confira se os NUMEROS citados aparecem de fato nessa passagem e se a paginacao/tabela confere; (4) se o PDF for 403/HTML de erro/paywall, marque url_viva=false.', { label: 'ver:' + k.canal + ':' + i, phase: 'Verificacao', schema: V, effort: 'high' })
      .then(function (v) { return { cand: k, ver: v } })
  }
}))

var ok = vereditos.filter(Boolean).filter(function (x) { return x.ver && x.ver.sobrevive })
log('Verificacao: ' + ok.length + '/' + todos.length + ' sobreviveram')

phase('Sintese')
var SYN = {
  type: 'object',
  properties: {
    veredito_final: {
      type: 'array',
      items: {
        type: 'object',
        properties: {
          citacao: { type: 'string' },
          doi: { type: 'string' },
          url_aberto: { type: 'string' },
          crossref_json: { type: 'string' },
          trecho_literal: { type: 'string' },
          onde: { type: 'string' },
          numeros: { type: 'string' },
          geometria: { type: 'string' },
          bate: { type: 'string' },
          diverge: { type: 'string' },
          materiais: { type: 'string' },
          alvo: { type: 'string' },
          utilidade: { type: 'string' },
        },
        required: ['citacao', 'doi', 'url_aberto', 'trecho_literal', 'numeros', 'utilidade'],
      },
    },
    iso7148_veredicto: { type: 'string' },
    buracos: { type: 'string' },
  },
  required: ['veredito_final', 'iso7148_veredicto', 'buracos'],
}

var sintese = await agent(CTX + '\n\nVoce e o SINTETIZADOR. Receba a lista de candidatos VERIFICADOS (sobreviventes) e produza o relatorio final.\n\nCANDIDATOS QUE SOBREVIVERAM:\n' + JSON.stringify(ok.map(function (x) { return x.cand }), null, 2) + '\n\nVEREDITOS:\n' + JSON.stringify(ok.map(function (x) { return x.ver }), null, 2) + '\n\nPara cada sobrevivente, monte a ficha final com citacao, doi, url_aberto, crossref_json (o que o Crossref devolveu), trecho_literal (o reextraido, se houver), onde (pagina/secao/tabela), numeros com unidades, geometria, bate, diverge, materiais (com aviso explicito se o material diferir do 52100 x 1045 do codigo), alvo e utilidade. Ordene por utilidade (alta primeiro: numero medido no par certo e geometria proxima do codigo). Depois, em iso7148_veredicto, diga explicitamente se existe texto integral aberto da ISO 7148, com as evidencias do que foi tentado. Em buracos, liste honestamente o que nao se conseguiu achar em texto aberto.\n\nTEXTO INTEIRO, sem resumo.', { label: 'sintese', phase: 'Sintese', schema: SYN, effort: 'high' })

return { total_candidatos: todos.length, sobreviveram: ok.length, veredito: sintese }
