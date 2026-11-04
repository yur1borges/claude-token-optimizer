import numpy as np
D=r"C:\Users\yuri\OneDrive\Desktop\MESTRADO PPGTIM\DEM\TriboDEM_Studio\testes\realidade\resultados_v9\V9_calibracao_G65_virtual\gpu_malhas"
for f in ['g0.obj','g1.obj','g2.obj']:
    v=[];tris=[]
    for line in open(D+"\\"+f,encoding='utf-8',errors='ignore'):
        if line.startswith('v '): v.append([float(x) for x in line.split()[1:4]])
        elif line.startswith('f '): tris.append([int(x.split('/')[0]) for x in line.split()[1:4]])
    v=np.array(v); T=v[np.array(tris)-1]
    E=np.stack([np.linalg.norm(T[:,1]-T[:,0],axis=1),np.linalg.norm(T[:,2]-T[:,1],axis=1),np.linalg.norm(T[:,0]-T[:,2],axis=1)],1)
    a=np.linalg.norm(np.cross(T[:,1]-T[:,0],T[:,2]-T[:,0]),axis=1)/2
    s=E.max(1)/(2*np.sqrt(a/np.sqrt(3)))  # aspecto
    print(f,"tris",len(tris))
    print("   aresta mm: min %.3f p1 %.2f med %.2f max %.1f"%(E.min()*1000,np.percentile(E,1)*1000,E.mean()*1000,E.max()*1000))
    print("   area mm2: min %.4f med %.2f  | tri com area<0.05mm2: %d (%.1f%%)"%(a.min()*1e6,np.median(a)*1e6,(a<5e-8).sum(),100*(a<5e-8).mean()))
    print("   aspecto max/min: med %.1f p95 %.1f max %.1f"%(np.median(s),np.percentile(s,95),s.max()))
