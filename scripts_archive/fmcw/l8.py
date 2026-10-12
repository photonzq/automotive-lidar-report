import numpy as np
from scipy import stats, optimize, integrate
PD=0.9; pfa_pt=1e-3; Nb=2233; Nw=1800
def pd_pair(nr,L,x1,x2):
    g=lambda S: stats.ncx2.sf(2*x1,2*L,2*nr*S/L)*stats.ncx2.sf(2*x2,2*L,2*nr*S/L)*stats.gamma.pdf(S,L)
    return integrate.quad(g,0,np.inf,limit=400)[0]
for L in (8,):
    best=None
    for lp1 in np.linspace(-8,-3.5,19):
        p1=10**lp1; p2=pfa_pt/(Nb*p1*Nw)
        if p2>=0.5: continue
        x1,x2=stats.gamma.isf(p1,L),stats.gamma.isf(p2,L)
        nr=optimize.brentq(lambda n: pd_pair(n,L,x1,x2)-PD,0.5,1e5)
        best=nr if best is None else min(best,nr)
    print("L=8 total both ramps:",round(2*best,1))
# sensor power at 15 Mpts/s, 200 m, L receivers per channel, n_tot two-ramp with 1.25 margin
Nd=15e6; RdR=1333; tau=1.333e-6; eta=0.15; Pan=0.01; es=37e-12; fD=9e7; P0=3
for L,n in [(1,258.3),(2,120.0),(4,88.2),(8,None)]:
    if n is None: n=2*best
    E=0.30e-6*(1.25*n/30)/L   # A_eff grows xL with diversity (polarization/spatial)
    useful=Nd*E/eta; samp=L*Nd*5*RdR*es; fixed=Nd*2*tau*L*Pan
    sq=2*Nd*np.sqrt(2*tau*E*L*(Pan+2.5*fD*es)/eta)
    Pch=np.sqrt(eta*E*(Pan+2.5*fD*es)/(2*tau*L)) if False else np.sqrt(eta*E*L*(Pan+2.5*fD*es)/(2*tau))
    tot=useful+samp+fixed+sq+P0
    print(f"L={L}: n={1.25*n:6.1f} pe, E_opt={E*1e6:5.2f} uJ, useful {useful:5.1f} W, samples {samp:5.1f}, fixed {fixed:4.1f}, channel terms {sq:5.1f}, total {tot:5.1f} W")
