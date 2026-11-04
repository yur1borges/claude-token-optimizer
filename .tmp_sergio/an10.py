import numpy as np
P=r"C:\Users\yuri\OneDrive\Desktop\MESTRADO PPGTIM\DEM\TriboDEM_Studio\testes\realidade\resultados_v9\V9_calibracao_G65_virtual\quadros.npz"
q=np.load(P); pos=q['pos']; vel=q['vel']; rad=q['radii']; t=q['t']
NF,N=pos.shape[0],pos.shape[1]
r=np.linalg.norm(pos[:,:,[0,2]],axis=2); y=pos[:,:,1]
st=np.isfinite(vel)&(np.abs(vel)<0.05)
# regiao interna da roda: r<0.1118 e |y|<0.00635
inner=st&(r<0.1118)&(np.abs(y)<0.0064)
ys=y[inner]
print("A) particulas ESTATICAS dentro de r<0.1118 e |y|<0.0064: n=%d"%len(ys))
h,e=np.histogram(ys,bins=24,range=(-0.0064,0.0064))
for i in range(24):
    if h[i]: print("   y=%.4f..%.4f : %d"%(e[i],e[i+1],h[i]))
print()
print("B) quantas tem |y| < 0.00135 (cavidade) :",np.sum(np.abs(ys)<0.00135))
print("   quantas tem |y| > 0.00135 (dentro do MATERIAL da roda):",np.sum(np.abs(ys)>0.00135))
print()
# estouro da linha de visada: densao de particulas por volume na regiao interna
print("C) r das particulas estaticas internas (mediana):",np.median(r[inner]))
print()
print("D) roda material: casca 5 mm sobre STL solido -> inner r=0.1118, outer r=0.1168; face da amostra x=0.1163")
print("   sobreposicao roda-amostra = %.4f m (%.1f mm)"%(0.1168-0.1163,(0.1168-0.1163)*1000))
