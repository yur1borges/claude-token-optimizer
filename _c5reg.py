import numpy as np
p = r'C:\Users\yuri\OneDrive\Desktop\MESTRADO PPGTIM\DEM\TriboDEM_Studio\testes\realidade\resultados_v9\V9_pino_disco_varredura\ensaio_completo.npz'
d = np.load(p, allow_pickle=True)
HV = 9.80665e6
H1 = 750 * HV   # pino 52100
H2 = 200 * HV   # disco 1045 (par do caso v9 salvo)
TRANS = 5e-3
s = d['s_m']; ppa = d['p_Pa']
mild_H1 = ppa / H1 <= TRANS
mild_H2 = ppa / H2 <= TRANS
print('fracao leve por H1 (criterio do _k_efetivo) =', mild_H1.mean())
print('fracao leve por min(H1,H2)=H2 (rotulo exportado) =', mild_H2.mean())
print('p no instante da virada por H1 =', TRANS * H1 / 1e6, 'MPa -> s =', s[np.argmax(mild_H1)], 'm de', s[-1], 'm')
print('p no instante da virada por H2 =', TRANS * H2 / 1e6, 'MPa -> s =', s[np.argmax(mild_H2)], 'm')
# taxa media na 2a metade
t = d['taxa1_mm3Nm']
print('taxa media 300: =', t[300:].mean(), ' x AFE =', t[300:].mean() / 3.667e-6)
print('volume suave: leve =', d['V1_m3'][np.argmax(mild_H1)] * 1e9, 'de', d['V1_m3'][-1] * 1e9)
