import numpy as np
P=r"C:\Users\yuri\OneDrive\Desktop\MESTRADO PPGTIM\DEM\TriboDEM_Studio\testes\realidade\resultados_v9\V9_calibracao_G65_virtual\quadros.npz"
q=np.load(P); pos=q['pos']; vel=q['vel']; rad=q['radii']
NF,N=pos.shape[0],pos.shape[1]
r=np.linalg.norm(pos[:,:,[0,2]],axis=2)
y=pos[:,:,1]
st=np.isfinite(vel)&(np.abs(vel)<0.05)
band=st&(np.abs(y)<0.0064)
rr=r[band]
print("A) static particles in wheel y-band, r_xz fine histogram (1mm bins, 0.100..0.130):")
h,e=np.histogram(rr,bins=30,range=(0.100,0.130))
for i in range(30):
    if h[i]: print("   %.3f-%.3f : %d"%(e[i],e[i+1],h[i]))
print()
print("B) for each candidate outer-surface radius, count static particles at r = R_out + d/2 :")
for R_out in [0.1143,0.1163,0.1168,0.1193,0.1218]:
    tgt=R_out+0.0024
    print("   R_out=%.4f -> rest r=%.4f  count=%d"%(R_out,tgt,np.sum(np.abs(rr-tgt)<0.0006)))
print()
print("C) static particles INSIDE wheel solid (r<0.1143-0.0024) in band:")
print("   count=%d  of %d static-in-band"%(np.sum(rr<0.1119),len(rr)))
print("D) static particles in annulus 0.1119..0.1218 (inside shell if outward):",np.sum((rr>0.1119)&(rr<0.1218)))
