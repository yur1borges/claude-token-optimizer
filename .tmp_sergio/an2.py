import numpy as np
P=r"C:\Users\yuri\OneDrive\Desktop\MESTRADO PPGTIM\DEM\TriboDEM_Studio\testes\realidade\resultados_v9\V9_calibracao_G65_virtual\quadros.npz"
q=np.load(P)
t=q['t']; pos=q['pos']; vel=q['vel']; rad=q['radii']
print("vel nan count", np.isnan(vel).sum(), "of", vel.size)
print("pos nan count", np.isnan(pos).sum())
nanf=np.isnan(vel).any(axis=1)
print("frames with any nan vel:", np.where(nanf)[0][:20], "first t=", t[np.where(nanf)[0][0]] if nanf.any() else None)
# finite max per frame
for i in [0,1,2,50,100,300,400,500,550,560,570,580,590,595,596,597,598,599,600]:
    v=vel[i]
    fm=np.nanmax(v) if np.isfinite(v).any() else float('nan')
    nf=np.isnan(v).sum()
    print("frame %3d t=%.4f vmax_finite=%8.2f n_nan=%d  pos_nan_particles=%d"%(i,t[i],fm,nf,np.isnan(pos[i]).any(axis=1).sum()))
