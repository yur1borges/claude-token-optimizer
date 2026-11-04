import json, os
base = r'C:\Users\yuri\OneDrive\Desktop\MESTRADO PPGTIM\DEM\TriboDEM_Studio\testes\realidade\resultados_v9'
AFE = 3.667e-6
for d in ['V9_pino_disco_varredura', 'V9_pino_disco_abrasivo_quartzo', 'V9_esfera_disco_varredura']:
    j = json.load(open(os.path.join(base, d, 'resultado.json'), encoding='utf-8'))
    print('---', d)
    for k in ['volume_desgaste_corpo1_m3', 'distancia_deslizamento_m', 'ensaio_taxa_corpo1_mm3_Nm',
              'ensaio_distancia_m', 'material1', 'material2', 'n_particulas', 'ensaio_regime_desgaste_final']:
        print('   ', k, '=', j.get(k))
    V = j['volume_desgaste_corpo1_m3']; s = j['distancia_deslizamento_m']; F = 10.0
    kdem = V / (F * s) * 1e9
    t = j['ensaio_taxa_corpo1_mm3_Nm']
    print('    DEM k_dim mm3/(N.m) =', kdem)
    print('    gap DEM/analitico =', kdem / t)
    print('    DEM x AFE =', kdem / AFE, ' | analitico x AFE =', t / AFE)
