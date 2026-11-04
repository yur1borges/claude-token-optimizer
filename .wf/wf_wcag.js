export const meta = {
  name: 'wcag-verify',
  description: 'Verifica adversarialmente cada achado de contraste WCAG nos 6 apps e consolida a lista final',
  phases: [
    { title: 'Verificar', detail: 'um verificador adversarial por grupo de achados' },
    { title: 'Criticar', detail: 'caça a achados que faltaram' },
    { title: 'Sintetizar', detail: 'consolida a lista final com ratio medido' },
  ],
}

const ACHADOS = 'C:\\Users\\yuri\\AppData\\Local\\Temp\\audit_visual\\achados_wcag.json'

const VERDICT_SCHEMA = {
  type: 'object',
  properties: {
    achados: {
      type: 'array',
      items: {
        type: 'object',
        properties: {
          id: { type: 'string' },
          veredito: { type: 'string', enum: ['CONFIRMADO', 'PARCIAL', 'REFUTADO'] },
          ratio_rea: { type: 'string', description: 'ratio recalculado pelo verificador' },
          razao_ajuste: { type: 'string', description: 'por que mudou ou por que se mantem' },
          correcao: { type: 'string', description: 'correcao minima sugerida no token, com hex' },
        },
        required: ['id', 'veredito', 'ratio_rea', 'razao_ajuste', 'correcao'],
      },
    },
    notas: { type: 'string' },
  },
  required: ['achados', 'notas'],
}

const CONTEXTO = [
  'Voce e um verificador adversarial de acessibilidade (WCAG 2.1 AA) em Windows.',
  'Papel: TENTAR REFUTAR cada achado. Padrao e REFUTADO se nao conseguir confirmar lendo o codigo-fonte.',
  '',
  'Arquivo com os achados a verificar (JSON): ' + ACHADOS,
  '',
  'Arquivos-fonte (LEITURA APENAS - NAO EDITE NENHUM):',
  '- Qt DA:      C:\\Users\\yuri\\OneDrive\\Desktop\\Claude\\DA\\raman_phase_analyzer\\qt_tema.py',
  '- Qt TriboDEM: C:\\Users\\yuri\\OneDrive\\Desktop\\MESTRADO PPGTIM\\DEM\\TriboDEM_Studio\\tribodem\\qt_tema.py',
  '- Qt Flow:     C:\\Users\\yuri\\OneDrive\\Desktop\\QE\\qe-flow\\flowcalc\\gui\\tema.py',
  '- Web Financas: C:\\Users\\yuri\\OneDrive\\Desktop\\Claude\\Financas\\Financas.html',
  '- Web Radar:    C:\\Users\\yuri\\OneDrive\\Desktop\\Claude\\RadarPassagens\\web\\index.html',
  '- Web Write:    C:\\Users\\yuri\\OneDrive\\Desktop\\Claude\\Write\\codigo-fonte\\src\\style.css',
  '',
  'REGRAS WCAG que valem (nao invente outras):',
  '- 1.4.3 Contraste minimo: 4.5:1 para texto normal; 3:1 para texto grande (>=24px, ou >=18.66px com peso >=700).',
  '- 1.4.11 Contraste nao-texto: 3:1 SOMENTE para elementos que identificam um controle de UI',
  '  (borda de input/select/textarea, indicador de foco, icone de botao que e o unico rotulo).',
  '  Borda decorativa de card/div, grade de tabela, borda transparente NAO sao exigidas por 1.4.11.',
  '- Texto desabilitado (disabled) e isento de 1.4.3 em WCAG 2.1.',
  '- Texto sobre imagem/fundo com gradiente: medir fora.',
  '- Alpha: composite(fg,bg) = fg.rgb*a + bg.rgb*(1-a).',
  '- Luminancia relativa: L = 0.2126R + 0.7152G + 0.0722B com canais normalizados 0..1 e linearizados',
  '  (c/12.92 se c<=0.03928, senao ((c+0.055)/1.055)^2.4). ratio = (L1+0.05)/(L2+0.05), L1>=L2.',
  '',
  'METODO (obrigatorio):',
  '1. Leia o grupo de achados atribuido no JSON.',
  '2. Abra os arquivos-fonte relevantes e CONFIRME que a regra CSS/QSS citada existe de fato, com o',
  '   token/valor exato. Se a regra nao existe, REFUTE.',
  '3. Recalcule o ratio de contraste VOCE MESMO. Use python via Bash com esta formula:',
  '   def lin(c):',
  '       c = c/255.0',
  '       return c/12.92 if c <= 0.03928 else ((c+0.055)/1.055)**2.4',
  '   def lum(h):',
  '       h = h.lstrip("#")',
  '       r,g,b = int(h[0:2],16), int(h[2:4],16), int(h[4:6],16)',
  '       return 0.2126*lin(r) + 0.7152*lin(g) + 0.0722*lin(b)',
  '   def ratio(a,b):',
  '       l1, l2 = lum(a), lum(b)',
  '       if l1 < l2: l1, l2 = l2, l1',
  '       return (l1+0.05)/(l2+0.05)',
  '4. Julgue a APLICABILIDADE da regra: 1.4.3 exige 4.5 ou 3 conforme o tamanho/peso real do texto?',
  '   1.4.11 exige 3:1 aqui, ou e borda decorativa (nao exigida)?',
  '5. Verifique se a cor do estado e realmente usada COMO TEXTO em algum lugar do app',
  '   (grep por c["ok"], c["erro"], c["aviso"], color:var(--ok), color:var(--warn)) ou se e so cor de fundo.',
  '   Isso muda a regra aplicavel.',
  '6. Aplique o juizo adversarial: a medicao esta errada? o fundo real e outro? o texto e grande?',
  '   o elemento esta desabilitado? o par nao aparece junto na tela?',
  '',
  'Para cada achado atribuido, devolva: id, veredito (CONFIRMADO/PARCIAL/REFUTADO), ratio_rea,',
  'razao_ajuste, correcao (correcao MINIMA no token, com hex, que nao quebre a identidade visual).',
  '',
  'IMPORTANTE:',
  '- A PALETAS dos 3 arquivos Qt e byte-identica. Se um token falha em um, falha nos tres.',
  '- Texto com o token de estado usado como cor de texto herda 1.4.3 (4.5:1).',
  '- Nao edite nenhum arquivo dos apps. Somente leitura e medicao.',
].join('\n')

phase('Verificar')
const GRUPOS = ['G1', 'G2', 'G3', 'G4', 'G5', 'G6']
const vereditos = await parallel(GRUPOS.map((g) => () =>
  agent(CONTEXTO + '\n\nVerifique o grupo ' + g + ' (e so ele) do arquivo de achados.', {
    label: 'verifica:' + g,
    phase: 'Verificar',
    schema: VERDICT_SCHEMA,
  })
))

const ok = vereditos.filter(Boolean)
log(ok.length + '/' + GRUPOS.length + ' verificadores responderam')

phase('Criticar')
const lacunas = await agent(CONTEXTO + [
  '',
  'Agora fa o papel de CRITICO DE COMPLETUDE. Os verificadores responderam com estes vereditos (JSON):',
  JSON.stringify(ok, null, 2),
  '',
  'Sua tarefa: CAZAR O QUE FALTOU. Leia os arquivos-fonte e identifique pares de contraste',
  'relevantes que NAO estao na lista - em especial:',
  '- texto em tamanho grande (>=18.66px bold ou >=24px) julgado com 4.5:1 quando 3:1 bastaria',
  '- links e botoes nos 3 apps web e no Qt',
  '- o header do Radar (background:var(--pri) com color:#fff) nos 2 temas',
  '- a sheet de novo monitoramento do Radar (labels, inputs, botao)',
  '- o painel do Claude no Write',
  '- QToolTip, QMenu, QStatusBar, QProgressBar, QTabBar, QCheckBox, QScrollBar nos 3 apps Qt',
  '- Write: .stylegal/.fxgal/.themegal (fundos brancos fixos), .pages .rh, .fig .imgwrap:after',
  '- Financas: .alert .ic, .btn.danger, .chip.off, .tabs, .iconbtn, tabela de meses',
  '- Radar: .fab, .btn.danger, .btn.sec, .tabs button.on, header button, .stat, .bar, svg text',
  'Verifique cada um lendo o codigo, recalcule o ratio, e so reporte se o par FALHAR de verdade',
  '(ratio abaixo do minimo aplicavel) e for RELEVANTE. Para cada um: o par, o ratio, o minimo,',
  'a regra aplicavel. Se nao achar nada novo, diga "nenhuma lacuna".',
  '',
  'Responda em texto corrido, em portugues do Brasil, sem markdown pesado.',
].join('\n'), {
  label: 'critico:completude',
  phase: 'Criticar',
})

phase('Sintetizar')
const relatorio = await agent([
  'Voce e o redator final do relatorio de auditoria WCAG AA dos 6 apps do Yuri.',
  '',
  'DADOS:',
  '1) Vereditos adversariais por grupo (JSON):',
  JSON.stringify(ok, null, 2),
  '',
  '2) Criterio de completude (texto):',
  lacunas || '(sem retorno)',
  '',
  '3) Achados originais (JSON) para referencia:',
  ACHADOS,
  '',
  'Escreva o RELATORIO FINAL em portugues do Brasil, pronto para enviar ao GN (chefe de design).',
  'Formato:',
  '',
  '## Auditoria de acessibilidade (WCAG 2.1 AA) - 6 apps',
  '',
  '**Metodo.** (1 linha: 374 pares de token medidos estaticamente nos 7 arquivos de tema +',
  '1.234 elementos medidos no navegador real com composicao de alpha, varrendo as 5 abas do Financas',
  'e as 3 rotas do Radar; limites 1.4.3 e 1.4.11 conforme WCAG 2.1)',
  '',
  '**Achados confirmados** - tabela:',
  '| # | App | Tema | Elemento | Medido | Minimo | Regra | Correcao |',
  'Use so achados CONFIRMADO ou PARCIAL. Para PARCIAL, diga o que muda.',
  '',
  '**Falsos-positivos descartados** - lista curta com o motivo.',
  '',
  '**Achados novos da caca de completude** (se houver) - mesma tabela.',
  '',
  '**Prioridade** - 3 niveis (P1 bloqueante / P2 importante / P3 oportunidade), do mais grave ao menos.',
  '',
  '**Aviso de escopo.** A PALETAS e BYTE-IDENTICA nos 3 arquivos Qt (DA, TriboDEM, Flow): mudar um token',
  'ali corrige os tres de uma vez - e o mesmo vale para a paleta unificada dos 6. A aba DRX do DA e o',
  'TriboCAD NAO foram tocados (nao entram no escopo). A auditoria e de leitura: nenhum arquivo dos apps',
  'foi alterado.',
  '',
  '**Criterio de correcao sugerido** - a menor mudanca de token que resolve cada nivel, com hex.',
  '',
  'Regras: nao invente numeros. Todo ratio no relatorio tem que vir dos vereditos ou da lista de',
  'lacunas. Nao inclua achados REFUTADO. Se um achado foi PARCIAL, explique a correcao real.',
].join('\n'), {
  label: 'sintetiza:relatorio',
  phase: 'Sintetizar',
})

return { relatorio: relatorio, vereditos: ok, lacunas: lacunas }
