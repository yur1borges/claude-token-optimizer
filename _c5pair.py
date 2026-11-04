import sys, collections
sys.path.insert(0, r'C:\Users\yuri\OneDrive\Desktop\MESTRADO PPGTIM\DEM\TriboDEM_Studio')
import numpy as np
from tribodem import ensaio_completo as EC, physics as F

HV = F.HV_PARA_PA
M = F.MATERIAIS
M1 = M['AISI 52100 (rolamento, 62 HRC)']
AFE = 3.667e-6


def Er(a, b):
    return 1 / ((1 - a['poisson'] ** 2) / (a['E_GPa'] * 1e9) + (1 - b['poisson'] ** 2) / (b['E_GPa'] * 1e9))


for nome, M2 in (('disco AISI 1045 (200 HV, par antigo)', M['AISI 1045']),
                 ('disco AISI 52100 (750 HV, par novo)', M['AISI 52100 (rolamento, 62 HRC)'])):
    H1 = M1['dureza_HV'] * HV
    H2 = M2['dureza_HV'] * HV
    e = EC.projetar_pino(0.6, 10, 0.1, 1000, 'seco', 3e-3, 2 * np.pi * 7e-3,
                         M1, M2, H1, H2, Er(M1, M2))
    t = e['taxa1_mm3Nm']
    reg = collections.Counter(e['regime_desgaste'])
    print(nome)
    print('   H2 HV =', M2['dureza_HV'], '| V1 mm3 =', round(e['V1_m3'][-1] * 1e9, 6))
    print('   taxa1 final =', t[-1], '| taxa1 media 2a metade =', t[300:].mean())
    print('   x AFE  final =', t[-1] / AFE, '| media =', t[300:].mean() / AFE)
    print('   regime contagem =', dict(reg), '| raio contato um =', e['raio_contato_m'][0] * 1e6, '->', e['raio_contato_m'][-1] * 1e6)
    print('   p MPa =', e['p_Pa'][0] / 1e6, '->', e['p_Pa'][-1] / 1e6)
