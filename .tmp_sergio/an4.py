import numpy as np
P=r"C:\Users\yuri\OneDrive\Desktop\MESTRADO PPGTIM\DEM\TriboDEM_Studio\testes\realidade\resultados_v9\V9_calibracao_G65_virtual\quadros.npz"
q=np.load(P)
t=q['t']; pos=q['pos']; vel=q['vel']; rad=q['radii']
NF,N=pos.shape[0],pos.shape[1]
mx=np.array([np.nanmax(vel[i]) if np.isfinite(vel[i]).any() else np.nan for i in range(NF)])
print("global max |v| in npz:", np.nanmax(mx), "at frame", int(np.nanargmax(mx)), "t=", t[np.nanargmax(mx)])
top=np.argsort(-mx)[:15]
for f in top: print("  f%3d t=%.4f vmax=%.2f"%(f,t[f],mx[f]))
# distribution of velocities of escaping particles
