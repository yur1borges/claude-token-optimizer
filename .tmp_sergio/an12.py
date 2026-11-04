import numpy as np
P=r"C:\Users\yuri\OneDrive\Desktop\MESTRADO PPGTIM\DEM\TriboDEM_Studio\testes\realidade\resultados_v9\V9_calibracao_G65_virtual\quadros.npz"
q=np.load(P); pos=q['pos']; vel=q['vel']; rad=q['radii']; t=q['t']
NF,N=pos.shape[0],pos.shape[1]
dt=6.6667e-3
D=np.linalg.norm(np.diff(pos,axis=0),axis=2)      # (NF-1,N)
Vmid=0.5*(vel[:-1]+vel[1:])
rows=[]
for f in range(NF-1):
    for i in range(N):
        if not np.isfinite(D[f,i]) or not np.isfinite(Vmid[f,i]): continue
        rows.append((D[f,i], Vmid[f,i]*dt, f, i, Vmid[f,i]))
R=np.array(rows)
print("n amostras:",len(R))
ratio=R[:,0]/np.maximum(R[:,1],1e-9)
print("razao |dp| / (v*dt): mediana %.4f  p05 %.4f p95 %.4f"%(np.median(ratio),np.percentile(ratio,5),np.percentile(ratio,95)))
print()
print("caso NORMAL (ratio 0.5..2) e v>0.5: n=%d"%np.sum((ratio>0.5)&(ratio<2)&(R[:,4]>0.5)))
print("caso TELEPORT (ratio>3) : n=%d"%np.sum(ratio>3))
print("caso v>50 mas ratio<2 (v sem movimento) : n=%d"%np.sum((R[:,4]>50)&(ratio<2)))
print()
tel=R[ratio>3]
tel=tel[np.argsort(-tel[:,4])]
print("TELEPORTS (ratio>3), top 20 por v:")
for d,vdt,f,i,v in tel[:20]:
    print("  f%3d->%3d p%3d  |dp|=%8.4f m  v*dt=%8.4f m  v=%8.1f m/s"%(f,f+1,i,d,vdt,v))
print()
print("|dp| max entre teleports: %.4f m ; min %.4f"%(tel[:,0].max(),tel[:,0].min()))
