import numpy as np
from scipy import stats, optimize, special
PD=0.9
def tof(b,p):
    n=0
    while stats.poisson.sf(n-1,b)>p: n+=1
    s=optimize.brentq(lambda s: stats.poisson.sf(n-1,s+b)-PD,1e-6,500); return n,s
# background per 1 ns bin per point: r_bg * 1ns * 10 shots * 0.71 live; r_bg scales with scene reflectance (6e8 at rho=0.9)
print("ToF background per bin b = r_bg*1e-9*10*0.71, r_bg = 6.0e8*(rho_scene/0.9)")
for rho,label in [(0.0,"night (b=0.01 dark/ambient)"),(0.1,"sun, 10% scene fills pixel"),(0.45,"sun, report model (half of rho=0.9)"),(0.9,"sun, white scene rho=0.9")]:
    b=0.01 if rho==0 else 6.0e8*(rho/0.9)*1e-9*10*0.71
    for p,plab in [(1e-3/2000,"full 2,000-bin search"),(1e-3/20,"20-bin tracking window")]:
        n,s=tof(b,p); print(f"  {label:38s} b={b:5.2f}  {plab:24s} n_th={n:2d}  s={s:5.1f}")
print()
def coh(N,pfa_pt,kind,L=4):
    p=pfa_pt/N
    if kind=="steady":
        x=-np.log(p); return optimize.brentq(lambda n: stats.ncx2.sf(2*x,2,2*n)-PD,0.1,1e4)
    if kind=="1sp":
        x=-np.log(p); return x/(-np.log(PD))-1
    x=stats.gamma.isf(p,L); return optimize.brentq(lambda n: special.gammaincc(L,x/(1+n/L))-PD,0.1,1e4)
print("Coherent, one ramp (per look-sum), P_D=0.9")
for N,pfa,lab in [(2700,1e-3,"full search 2,700 bins, 1e-3/pt"),(2700,1e-2,"relaxed 1e-2/pt + neighbour pruning"),(20,1e-3,"20-bin tracking window, 1e-3/pt"),(1,1e-3,"known cell (ideal bound), 1e-3")]:
    print(f"  {lab:40s} steady {coh(N,pfa,'steady'):6.1f}  4-look {coh(N,pfa,'L'):6.1f}  1-speckle {coh(N,pfa,'1sp'):6.1f}")
