import numpy as np
P=r"C:\Users\yuri\OneDrive\Desktop\MESTRADO PPGTIM\DEM\TriboDEM_Studio\testes\realidade\resultados_v9\V9_calibracao_G65_virtual\quadros.npz"
q=np.load(P); pos=q['pos']; vel=q['vel']; rad=q['radii']
NF,N=pos.shape[0],pos.shape[1]
r=np.linalg.norm(pos[:,:,[0,2]],axis=2); y=pos[:,:,1]; x=pos[:,:,0]
st=np.isfinite(vel)&(np.abs(vel)<0.05)
rr=r[st]; yy=y[st]; xx=x[st]
d2=np.repeat((rad/1.0)[None,:],NF,axis=0)[st]
print("estaticos:",len(rr))
for R_out in [0.1143,0.1168,0.1193]:
    tgt=R_out+d2
    print("R_out=%.4f  camada de repouso (raio do centro) -> dentro +-0.4mm: %d"%(R_out,np.sum(np.abs(rr-tgt)<0.0004)))
for Xf in [0.1163,0.1113]:
    print("plano x=%.4f : particulas com |dist|d/2 < 0.4mm: %d"%(Xf,np.sum(np.abs(np.abs(xx-Xf)-d2)<0.0004)))
print()
print("histograma 2D (r_xz, y) de estaticos, bins 5mm x 1.4mm:")
hb,eb,hb2,eb2=np.histogram2d(rr,yy,bins=[np.arange(0.085,0.135,0.005),np.arange(-0.007,0.0071,0.0014)])
print("   y:", " ".join("%+.4f"%v for v in eb2[:-1]))
for i in range(len(eb)-1):
    print(" r=%.3f" %eb[i], " ".join("%5d"%v for v in hb[i]))
