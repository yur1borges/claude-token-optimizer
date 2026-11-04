import numpy as np
P=r"C:\Users\yuri\OneDrive\Desktop\MESTRADO PPGTIM\DEM\TriboDEM_Studio\testes\realidade\resultados_v9\V9_calibracao_G65_virtual\quadros.npz"
q=np.load(P); pos=q['pos']; vel=q['vel']; rad=q['radii']; t=q['t']
NF,N=pos.shape[0],pos.shape[1]; dt=6.6667e-3
D=np.linalg.norm(np.diff(pos,axis=0),axis=2)
VMAX=60.0
print("A) amostras com v gravada > SetMaxVelocity(60):")
n=0
for f in range(NF):
    v=vel[f]
    k=np.where(np.isfinite(v)&(np.abs(v)>VMAX))[0]
    if len(k): n+=len(k); 
    if len(k) and f<200: print("   f%3d t=%.4f  n=%d  vmax=%.1f"%(f,t[f],len(k),np.nanmax(np.abs(v))))
print("   total amostras com |v|>60 :",n)
print()
print("B) coerencia: v observada (do salto) vs v gravada, para os 30 maiores |v| gravados")
rows=[]
for f in range(NF):
    for i in range(N):
        v=vel[f,i]
        if not np.isfinite(v) or abs(v)<20: continue
        if f==0 or f==NF-1: continue
        dp=D[f-1,i]
        if not np.isfinite(dp): continue
        vobs=dp/dt
        rows.append((f,i,abs(v),vobs,dp,pos[f-1,i],pos[f,i]))
rows.sort(key=lambda r:-r[2])
print("  f     p   v_gravada  v_observada  |dp|(m)   pos_antigo            pos_novo")
for f,i,vg,vo,dp,p0,p1 in rows[:20]:
    print("%4d %4d  %9.1f  %9.1f  %8.4f  %s -> %s"%(f,i,vg,vo,dp,p0.round(4),p1.round(4)))
print()
print("C) razao v_observada/v_gravada (mediana) para v_gravada>20:",np.median([r[3]/max(r[2],1e-9) for r in rows]))
