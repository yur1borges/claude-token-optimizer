import numpy as np
P=r"C:\Users\yuri\OneDrive\Desktop\MESTRADO PPGTIM\DEM\TriboDEM_Studio\testes\realidade\resultados_v9\V9_calibracao_G65_virtual\quadros.npz"
q=np.load(P); pos=q['pos']; vel=q['vel']; rad=q['radii']; t=q['t']
NF,N=pos.shape[0],pos.shape[1]
R=0.1143; RW=0.1093; XSPEC=0.1163; ZSPEC=0.0381; YCAP=0.00135
# grande salto de posicao = evento
D=np.linalg.norm(np.diff(pos,axis=0),axis=2)
ev=[]
for f in range(NF-1):
    for i in range(N):
        if not np.isfinite(D[f,i]): continue
        if D[f,i]>0.002:
            ev.append((f,i,D[f,i],vel[f+1,i],pos[f,i],pos[f+1,i]))
print("eventos (salto>2mm):",len(ev))
def gap_info(p):
    x,y,z=p
    r=np.hypot(x,z)
    # folga radial ate a OD da roda (0.1143) e ate a face interna da casca (0.1093)
    g_od=r-0.1143
    # sobreposicao com a cap (|y| entre 0.00135 e 0.00635) dentro de r<0.1143
    cap = (r<0.1143) and (abs(y)>YCAP)
    # distancia ao plano da amostra x=0.1163
    g_spec=(XSPEC-x)-rad[i]/2 if False else None
    return r,g_od,cap
print()
print(" f    p    d(mm) |dp|(m)  v_final   r_ini    folga_OD   |y|_ini   dentro_cap   dist_plano_esp(m)")
for f,i,d,v,p0,p1 in ev:
    if not np.isfinite(v): continue
    r0,g_od,_=gap_info(p0)
    r1,g1,cap1=gap_info(p1)
    print("%4d %4d  %4.2f  %7.4f  %8.1f  %7.4f  %+8.4f  %+8.5f  %s  %8.4f"%(f,i,2*rad[i]*1000,d,v,r0,g_od,p0[1],cap1,abs(p0[0]-XSPEC)))
