import numpy as np
d = np.load('testes/realidade/resultados_v9/V9_calibracao_G65_virtual/quadros.npz')
v = d['vel']; pos = d['pos']; t = d['t']
K, N = pos.shape[0], pos.shape[1]
dt = np.diff(t)
salto = np.linalg.norm(pos[1:] - pos[:-1], axis=2)
vp = v[:-1] * dt[:, None]
masc = (v[:-1] > 0.5) & np.isfinite(salto) & np.isfinite(vp) & (vp > 0)
razao = np.where(masc, salto / np.maximum(vp, 1e-30), np.nan)
inco = np.nanmax(np.where(masc, 1.0 / razao, np.nan), axis=0)
print('particulas com 1/razao > 1.5:', int((inco > 1.5).sum()))
print('particulas com 1/razao > 2  :', int((inco > 2).sum()))
print('particulas com 1/razao > 3  :', int((inco > 3).sum()))
print('max 1/razao: %.2f' % np.nanmax(inco))
sm = np.nanmax(salto, axis=0)
print()
for th in (1, 2, 5, 10, 20, 50):
    print('particulas com salto max > %3d mm: %3d' % (th, int((sm > th).sum())))
print()
# quantos "eventos de espasmo" no sentido: quadro onde a particula tem razao muito baixa E v alta
ev = masc & (razao < 0.6) & (v[:-1] > 10)
print('eventos (v>10 e razao<0.6):', int(ev.sum()))
ev2 = masc & (razao < 0.6) & (v[:-1] > 5)
print('eventos (v>5 e razao<0.6) :', int(ev2.sum()))
part_ev = ev.any(axis=0)
print('particulas com >=1 evento :', int(part_ev.sum()))
