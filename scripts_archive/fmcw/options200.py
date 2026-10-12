import numpy as np
from scipy import stats, optimize, integrate, special
PD=0.9; pfa_pt=1e-3
def pd_pair(nr,L,x1,x2):
    if L==0:
        return stats.ncx2.sf(2*x1,2,2*nr)*stats.ncx2.sf(2*x2,2,2*nr)
    g=lambda S: stats.ncx2.sf(2*x1,2*L,2*nr*S/L)*stats.ncx2.sf(2*x2,2*L,2*nr*S/L)*stats.gamma.pdf(S,L)
    return integrate.quad(g,0,np.inf,limit=400)[0]
def thr(L,p): return -np.log(p) if L==0 else stats.gamma.isf(p,L)
def two_stage(L,Nb,Nw):
    best=None
    for lp1 in np.linspace(-8,-3.5,19):
        p1=10**lp1; p2=pfa_pt/(Nb*p1*Nw)
        if p2>=0.5: continue
        x1,x2=thr(L,p1),thr(L,p2)
        nr=optimize.brentq(lambda n: pd_pair(n,L,x1,x2)-PD,0.5,1e5)
        if best is None or nr<best[0]: best=(nr,p1,p2)
    return best
for R in (200.0,300.0):
    for Tu in (5e-6,10e-6,20e-6):
        Nb=R/0.15+90e6*Tu; Nw=2*90e6*Tu
        row=[]
        for L in (0,1,2,4):
            nr,p1,p2=two_stage(L,Nb,Nw); row.append(2*nr)
        print(f"R={R:.0f} m Tu={Tu*1e6:4.0f} us Nb={Nb:5.0f} Nw={Nw:5.0f} | total pe (both ramps): steady {row[0]:5.1f}  L=1 {row[1]:6.1f}  L=2 {row[2]:6.1f}  L=4 {row[3]:6.1f}")
