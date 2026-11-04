import numpy as np
P=r"C:\Users\yuri\OneDrive\Desktop\MESTRADO PPGTIM\DEM\TriboDEM_Studio\testes\realidade\resultados_v9\V9_calibracao_G65_virtual\quadros.npz"
q=np.load(P)
t=q['t']; pos=q['pos']; vel=q['vel']; rad=q['radii']
NF,N=pos.shape[0],pos.shape[1]
r=np.linalg.norm(pos[:,:,[0,2]],axis=2)   # (NF,N)
# static particles: |v| < 0.05 and finite
v=vel
st=np.isfinite(v)&(np.abs(v)<0.05)
# radius of static particles
rr=np.where(st,r,np.nan)
vals=rr[np.isfinite(rr)]
print("static particle-center radii (m): n=%d"%len(vals))
hist,edges=np.histogram(vals,bins=40,range=(0.0,0.30))
for i in range(40):
    if hist[i]: print("  r=%.4f..%.4f : %d"%(edges[i],edges[i+1],hist[i]))
print()
for R in [0.1143,0.1163,0.1193,0.1215,0.1227]:
    print("count near R=%.4f (+-1.5mm): %d"%(R,np.sum(np.abs(vals-R)<0.0015)))
