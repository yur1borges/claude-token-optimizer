import numpy as np
D=r"C:\Users\yuri\OneDrive\Desktop\MESTRADO PPGTIM\DEM\TriboDEM_Studio"
# STL do anel: normal de cada triangulo -> caps?
b=open(D+r"\testes\realidade\montagens\g65_virtual\01_G65_rubber_wheel.stl",'rb').read()
n=int(np.frombuffer(b[80:84],'<u4')[0])
d=np.frombuffer(b[84:84+n*50],dtype=np.uint8).reshape(n,50)
tri=d[:,12:48].copy().view('<f4').reshape(n,3,3)
nr=d[:,0:12].copy().view('<f4').reshape(n,3)
e=np.linalg.norm(np.cross(tri[:,1]-tri[:,0],tri[:,2]-tri[:,0]),axis=1)/2
print("STL wheel: tris",n,"area total m2",round(e.sum(),6))
# normais: radiais (no plano xz) vs caps (normais em y)
nrm=nr/np.linalg.norm(nr,axis=1,keepdims=True)
radial=np.abs(nrm[:,1])<1e-3
print("triangulos com normal radial (superficie cilindrica):",radial.sum())
print("outros (caps):",(~radial).sum())
ar=e*1e4
print("area por triangulo mm2: min %.1f max %.1f mean %.1f"%(ar.min(),ar.max(),ar.mean()))
# arestas
E=np.stack([np.linalg.norm(tri[:,1]-tri[:,0],axis=1),np.linalg.norm(tri[:,2]-tri[:,1],axis=1),np.linalg.norm(tri[:,0]-tri[:,2],axis=1)],1)*1000
print("aresta STL mm: min %.1f max %.1f mean %.1f"%(E.min(),E.max(),E.mean()))
# caps: existem? pontos com |y|==max
V=tri.reshape(-1,3)
print("y range",V[:,1].min(),V[:,1].max(),"  pontos no plano y=+-0.00635:",np.sum(np.abs(np.abs(V[:,1])-0.00635)<1e-6))
