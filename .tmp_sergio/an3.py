import numpy as np
P=r"C:\Users\yuri\OneDrive\Desktop\MESTRADO PPGTIM\DEM\TriboDEM_Studio\testes\realidade\resultados_v9\V9_calibracao_G65_virtual\quadros.npz"
q=np.load(P)
t=q['t']; pos=q['pos']; vel=q['vel']; rad=q['radii']
NF,N=pos.shape[0],pos.shape[1]
def r_xz(p): return np.linalg.norm(p[:,[0,2]],axis=1)
r=r_xz(pos.reshape(-1,3)).reshape(NF,N)
# particles that ended far away
end=r[-1]
far=np.where(end>0.2)[0]
print("particles ending r>0.2:",far)
for i in far:
    # find first frame where r>0.15
    idx=np.where(r[:,i]>0.15)[0]
    k=idx[0] if len(idx) else None
    print("p%3d d=%.2fmm  final r=%.3f  first r>0.15 at frame %s t=%.4f"%(i,2*rad[i]*1000,end[i],k,t[k] if k is not None else -1))
    if k:
        for f in range(max(0,k-3),min(NF,k+3)):
            v=vel[f,i]
            print("     f%3d t=%.4f pos=%s r=%.5f v=%s |v|=%.2f"%(f,t[f],pos[f,i].round(4),r[f,i],v.round(1),np.linalg.norm(v)))
