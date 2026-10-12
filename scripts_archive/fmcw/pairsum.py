import numpy as np
from scipy import stats, optimize, integrate
PD=0.9; Nr=2000; Nv=1350; p=1e-3/(Nr*Nv)
def need(L):
    # statistic: sum over L looks x 2 ramps of |s+n|^2 ; fading common to both ramps within a look
    x=stats.gamma.isf(p, 2*L)                    # noise-only: Gamma(2L,1)
    if L==0:
        x=stats.gamma.isf(p,2)
        f=lambda nt: stats.ncx2.sf(2*x,4,2*nt)-PD
    else:
        def f(nt):
            g=lambda S: stats.ncx2.sf(2*x,4*L,2*nt*S/L)*stats.gamma.pdf(S,L)
            return integrate.quad(g,0,np.inf,limit=400)[0]-PD
    return optimize.brentq(f,1,1e5), x
for name,L in [("steady",0),("4-look",4),("1-speckle",1)]:
    nt,x=need(L); print(f"pair-sum 2-D search ({Nr*Nv:.1e} hypotheses): {name:9s} total {nt:6.1f}  (threshold {x:.1f})")
# FFT straddle loss, rectangular window, offset uniform in [-0.5,0.5] bin
d=np.linspace(-0.5,0.5,200001); g=np.sinc(d)**2
print("rect FFT straddle: mean power", g.mean().round(4), f"({10*np.log10(g.mean()):.2f} dB), worst {10*np.log10(g.min()):.2f} dB")
d2=np.linspace(-0.25,0.25,200001); g2=np.sinc(d2)**2
print("2x zero-padded: mean", f"{10*np.log10(g2.mean()):.2f} dB, worst {10*np.log10(g2.min()):.2f} dB")
