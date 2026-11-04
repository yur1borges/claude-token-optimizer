import numpy as np
P=r"C:\Users\yuri\OneDrive\Desktop\MESTRADO PPGTIM\DEM\TriboDEM_Studio\testes\realidade\resultados_v9\V9_calibracao_G65_virtual\quadros.npz"
q=np.load(P)
t=q['t']; pos=q['pos']; vel=q['vel']; rad=q['radii']; tri=q['tri']
print("t step:",np.diff(t).min(), np.diff(t).max())
NF=pos.shape[0]; N=pos.shape[1]
R=0.1143
def r_xz(p): return np.linalg.norm(p[:,[0,2]],axis=1)
vmax=vel.max(axis=1)
print("v_max per frame: max",vmax.max(),"at frame",int(vmax.argmax()),"t",t[vmax.argmax()])
# frames with any v>15
fr=[i for i in range(NF) if vel[i].max()>15]
print("frames with v>15:",fr[:50], "count",len(fr))
# per particle: which particle reaches big v
big=np.argwhere(vel>15)
print("particles with v>15 (unique):",np.unique(big[:,1]))
# max v per particle
mv=vel.max(axis=0)
idx=np.argsort(-mv)[:12]
print("top particles by vmax: idx, vmax, d(mm), r_end")
for i in idx:
    print("  p%3d vmax=%8.1f  d=%.2fmm  r_final=%.5f  r_min=%.5f"%(i,mv[i],2*rad[i]*1000,r_xz(pos[-1,i:i+1])[0],r_xz(pos[:,i]).min()))
