export const meta = {
  name: 'seg-verify-audit',
  description: 'Verifica adversarialmente achados de seguranca dos 4 apps e caeca vulnerabilidades restantes',
  phases: [
    { title: 'Verify', detail: 'verificadores tentam refutar cada achado' },
    { title: 'Sweep', detail: 'cacadores multidimensionais' },
    { title: 'Critic', detail: 'critico de completude' },
  ],
}

const P = args.paths
const A = args.achados
const REGRAS = args.regras

const V = args.verificadores
const SCHEMA_V = {
  type: 'object',
  properties: {
    achados: { type: 'array', items: { type: 'object', properties: {
      id: { type: 'string' }, refutado: { type: 'boolean' },
      confianca: { type: 'string', enum: ['alta', 'media', 'baixa'] },
      motivo: { type: 'string' }, correcao_necessaria: { type: 'string' },
    }, required: ['id', 'refutado', 'confianca', 'motivo'] } },
    novos_problemas: { type: 'array', items: { type: 'object', properties: {
      arquivo: { type: 'string' }, linha: { type: 'integer' },
      severidade: { type: 'string', enum: ['ALTO', 'MEDIO', 'BAIXO', 'INFO'] },
      descricao: { type: 'string' },
    }, required: ['arquivo', 'linha', 'severidade', 'descricao'] } },
  },
  required: ['achados', 'novos_problemas'],
}
const SCHEMA_S = {
  type: 'object',
  properties: {
    problemas: { type: 'array', items: { type: 'object', properties: {
      app: { type: 'string' }, arquivo: { type: 'string' }, linha: { type: 'integer' },
      severidade: { type: 'string', enum: ['ALTO', 'MEDIO', 'BAIXO', 'INFO'] },
      descricao: { type: 'string' }, cenario: { type: 'string' },
      status: { type: 'string', enum: ['corrigido', 'pendente', 'nao-tocar'] },
    }, required: ['app', 'arquivo', 'linha', 'severidade', 'descricao', 'cenario', 'status'] } },
  },
  required: ['problemas'],
}

phase('Verify')
const verif = await parallel(V.map((v) => () => agent(
  args.promptVerify + '\n\nApp: ' + v.app + '\nLente: ' + v.lente + '\n' + v.foco +
  '\n\nPaths: ' + JSON.stringify(P) +
  '\n\nACHADOS:\n' + JSON.stringify(A[v.app], null, 2) +
  '\n\nRetorne achados[] e novos_problemas[].',
  { label: 'verify:' + v.app + ':' + v.lente, phase: 'Verify', schema: SCHEMA_V })))

phase('Sweep')
const varreduras = await parallel(args.cacadores.map((c) => () => agent(
  'Cacador - dimensao: ' + c.nome + '\n' + c.foco +
  '\n\nPaths:\n' + JSON.stringify(P, null, 2) + '\n\n' + REGRAS + '\n\nRetorne problemas[].',
  { label: 'sweep:' + c.nome, phase: 'Sweep', schema: SCHEMA_S })))

phase('Critic')
const critico = await agent(
  args.promptCritic + '\n\nPaths:\n' + JSON.stringify(P, null, 2) + '\n\n' + REGRAS + '\n\nRetorne problemas[].',
  { label: 'critic:completude', phase: 'Critic', schema: SCHEMA_S })

return { verif: verif.filter(Boolean), varreduras: varreduras.filter(Boolean), critico }
