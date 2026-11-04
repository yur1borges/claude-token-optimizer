export const meta = {
  name: 'wf-smoke-test',
  description: 'Valida o runner do Workflow com um unico agente',
  phases: [{ title: 'Teste' }],
}

phase('Teste')
const r = await agent('Responda apenas com a palavra OK.', { label: 'smoke' })
log('resultado: ' + JSON.stringify(r))
return { ok: true, r }
