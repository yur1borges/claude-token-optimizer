import numpy as np
P=r"C:\Users\yuri\OneDrive\Desktop\MESTRADO PPGTIM\DEM\TriboDEM_Studio\testes\realidade\resultados_v9\V9_calibracao_G65_virtual\quadros.npz"
q=np.load(P)
t=q['t']; pos=q['pos']; vel=q['vel']; rad=q['radii']
for F in [89,60,117]:
    v=vel[F]; k=int(np.nanargmax(v))
    print("=== frame",F,"t=%.4f  particle %d  d=%.2fmm |v|=%.2f"%(t[F],k,2*rad[k]*1000,v[k]))
    for f in range(F-4,F+4):
        if 0<=f<len(t):
            print("   f%3d t=%.4f pos=%s v=%s"%(f,t[f],pos[f,k].round(5),vel[f,k].round(2)))
    # distance to wheel surface in xz
