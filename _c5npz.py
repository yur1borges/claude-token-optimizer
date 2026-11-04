import numpy as np, collections, os
p = r'C:\Users\yuri\OneDrive\Desktop\MESTRADO PPGTIM\DEM\TriboDEM_Studio\testes\realidade\resultados_v9\V9_pino_disco_varredura\ensaio_completo.npz'
d = np.load(p, allow_pickle=True)
print('keys:', list(d.keys()))
t = d['taxa1_mm3Nm']
print('n =', len(t))
print('media 300: =', t[300:].mean())
print('media full =', t.mean())
print('regime counter =', dict(collections.Counter(d['regime_desgaste'])))
print('raio contato um:', d['raio_contato_m'][0] * 1e6, '->', d['raio_contato_m'][-1] * 1e6)
print('p MPa:', d['p_Pa'][0] / 1e6, '->', d['p_Pa'][-1] / 1e6)
print('V1 mm3 final =', d['V1_m3'][-1] * 1e9)
