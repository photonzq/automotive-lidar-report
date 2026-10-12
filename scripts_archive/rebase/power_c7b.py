"""Section C7b subsection 2(h) with N_L receivers per channel, and assorted re-baseline numbers."""
import numpy as np
from scipy import stats, integrate, optimize

NDOT, R_DR, TAU, ETA, P_AN, E_S, F_D, P0, NL = 1e7, 2000, 2.0e-6, 0.15, 0.010, 37e-12, 90e6, 3.0, 4


def terms(Pch, E=0.45e-6, eta=ETA, Pan=P_AN, es=E_S, nl=NL, ndot=NDOT):
    Tu = E / (2 * Pch)
    nch = ndot * (E / Pch + 2 * TAU)
    nsamp = 5 * R_DR + 5 * F_D * Tu
    useful = ndot * E / eta
    dead = 2 * TAU * ndot * Pch / eta
    analog = nch * nl * Pan
    adc = ndot * nl * nsamp * es
    tot = useful + dead + analog + adc + P0
    btot = 1e9 * (1 + TAU / Tu)
    fs = 2.5 * (1e9 * TAU / Tu + F_D)
    return dict(Tu=Tu, nch=nch, nsamp=nsamp, useful=useful, dead=dead, analog=analog, adc=adc, tot=tot,
                btot=btot, fs=fs)


def popt(E=0.45e-6, eta=ETA, Pan=P_AN, es=E_S, nl=NL):
    return np.sqrt(eta * E * nl * (Pan + 2.5 * F_D * es) / (2 * TAU))


def pmin(E=0.45e-6, eta=ETA, Pan=P_AN, es=E_S, nl=NL, ndot=NDOT):
    return ndot * (E / eta + 5 * R_DR * nl * es + 2 * TAU * nl * Pan
                   + 2 * np.sqrt(2 * TAU * E * nl * (Pan + 2.5 * F_D * es) / eta)) + P0


print("=== (h) 10 Mpts/s, 300 m, 15 cm, E' = 0.45 uJ, N_L =", NL)
po = popt()
print(f"P_an + 2.5 f_D e_s = {(P_AN + 2.5*F_D*E_S)*1e3:.2f} mW per receiver; P_ch* = {po*1e3:.1f} mW")
for P in (0.016, po, 0.030, 0.100):
    t = terms(P)
    print(f"  P_ch {P*1e3:6.1f} mW: N_ch {t['nch']:5.0f} ({NL*t['nch']:5.0f} receivers)  T_u {t['Tu']*1e6:5.2f} us  "
          f"B_tot {t['btot']/1e9:.2f} GHz  f_s {t['fs']/1e9:.2f} GS/s  useful {t['useful']:.1f}  dead {t['dead']:.1f}  "
          f"analog {t['analog']:.1f}  ADC+FFT {t['adc']:.1f}  total {t['tot']:.1f} W")
t = terms(po)
chan = 2 * NDOT * np.sqrt(2 * TAU * 0.45e-6 * NL * (P_AN + 2.5 * F_D * E_S) / ETA)
print(f"  Eq.(115) min: {pmin():.2f} W; range samples {NDOT*5*R_DR*NL*E_S:.2f} W; fixed analog {NDOT*2*TAU*NL*P_AN:.2f} W; "
      f"channel terms {chan:.2f} W (each {chan/2:.2f}); share of useful light {30/pmin()*100:.0f}%")
print(f"  emitted light at optimum: {NDOT*(0.45e-6 + 2*TAU*po):.2f} W; T_c {(t['Tu']+TAU)*1e6:.1f} us; "
      f"kappa {1e9/t['Tu']:.2e} Hz/s; f_s {t['fs']/1e9:.2f} GS/s")
print("  levers:")
print(f"    halve E' -> {pmin(E=0.225e-6):.1f} W (saves {pmin()-pmin(E=0.225e-6):.1f} W); "
      f"check 15 + chan*(1-1/sqrt2) = {15 + chan*(1-1/np.sqrt(2)):.1f}")
for dnu, eta_c in [(10e3, np.exp(-2*np.pi*10e3*TAU)), (42e3, np.exp(-2*np.pi*42e3*TAU)), (100e3, np.exp(-2*np.pi*100e3*TAU))]:
    E = 0.45e-6 / eta_c
    ch = 2 * NDOT * np.sqrt(2 * TAU * E * NL * (P_AN + 2.5 * F_D * E_S) / ETA)
    print(f"    linewidth {dnu/1e3:5.0f} kHz: eta_coh {eta_c:.3f}, E' {E*1e6:.2f} uJ, P* {popt(E=E)*1e3:.1f} mW, "
          f"total {pmin(E=E):.1f} W (useful {NDOT*E/ETA:.1f}, channel terms {ch:.1f})")
print(f"    eta_WPE 0.30 -> {pmin(eta=0.30):.1f} W (saves {pmin()-pmin(eta=0.30):.1f})")
print(f"    halve P_an and e_s -> {pmin(Pan=0.005, es=18.5e-12):.1f} W (saves {pmin()-pmin(Pan=0.005, es=18.5e-12):.1f}); "
      f"parts: range samples {NDOT*5*R_DR*NL*E_S/2:.2f}, fixed analog {NDOT*2*TAU*NL*P_AN/2:.2f}, "
      f"channel {chan*(1-1/np.sqrt(2)):.2f}")
print(f"    100 mW per channel costs {terms(0.1)['tot']-pmin():.1f} W more; dead-time share {terms(0.1)['dead']-terms(po)['dead']:.1f}")
print(f"    one receiver per channel (N_L = 1) for comparison: P* {popt(nl=1)*1e3:.1f} mW, total {pmin(nl=1):.1f} W")
print(f"    ADC floor power E'/(2 T_ADC) at 1 GS/s: {0.45e-6/(2*6.45e-6)*1e3:.0f} mW")

print("\n=== subsection 3 channel tax, 15 Mpts/s, 200 m, 30 mW")
E_rx = 4 * (12300 * 37.3e-12 + 0.010 * 10e-6)
print(f"E_rx (4 receivers) = {E_rx*1e6:.3f} uJ (model 2.230)")
nd = 15e6
nch = nd * (0.30e-6 / 0.030 + 2 * 1.333e-6)
print(f"N_ch = {nch:.0f}; receive {nd*2.230e-6:.1f} W -> {nd*2.230e-6/nch*1e3:.0f} mW per channel "
      f"({nd*2.230e-6/nch/4*1e3:.0f} per receiver); light 200 mW; total per channel {nd*2.230e-6/nch*1e3+200:.0f} mW")
print(f"ToF: receive {nd*71e-9:.2f} W /312 = {nd*71e-9/312*1e3:.1f} mW; laser {nd*0.366e-6:.2f} W /312 = {nd*0.366e-6/312*1e3:.1f} mW; "
      f"sum {(nd*71e-9+nd*0.366e-6)/312*1e3:.1f} mW; ratio {(nd*2.230e-6/nch*1e3+200)/((nd*71e-9+nd*0.366e-6)/312*1e3):.1f}")
print(f"520-line ToF unit: {3 + 12.5e6*0.436e-6:.2f} W; FMCW receiver at 15 Mpts/s / ToF unit = {nd*2.230e-6/(3+12.5e6*0.436e-6):.1f}")

print("\n=== subsection 5 parity table")
for name, eo, wp, erx in [("2026 central", 0.303, 0.15, 2.230), ("2032 optimistic", 0.190, 0.22, 0.614),
                          ("all three", 0.15, 0.30, 0.10), ("wp 15%", 0.15, 0.15, 0.10),
                          ("E_rx 0.30", 0.15, 0.30, 0.30), ("E_opt 0.30", 0.30, 0.30, 0.10)]:
    tot = eo / wp + erx
    print(f"  {name:16s} laser {eo/wp:.2f} uJ  total {tot:.2f} uJ  P(15M) {3+15*tot:.1f} W")
for nch_ in (115, 190):
    print(f"  parity receive per channel at {nch_} channels: {0.10e-6*15e6/nch_*1e3:.1f} mW, per receiver {0.10e-6*15e6/nch_/4*1e3:.2f} mW")
print(f"  8 looks: E_opt = {0.303*(1.36*82.4/120)*(4/8):.3f} uJ")

print("\n=== §C7a numbers")
print(f"520-line: FMCW {3+12.5e6*4.253e-6:.1f} W; receiver {12.5e6*2.230e-6:.1f} W; laser heat {12.5e6*(2.023e-6-0.303e-6):.1f} W; "
      f"optical {12.5e6*0.303e-6:.2f} W; ToF {3+12.5e6*0.436e-6:.2f} W")
print(f"raw data 2/10/25 Mpts/s: {[round(4*r*10e-6*1.2265e9*10/1e12, 2) for r in (2e6, 10e6, 25e6)]} Tb/s")
print(f"Surya devices at 10 Mpts/s: {1e7*4*12265/4e9:.0f}; ops {12e6*4*12265*70:.2e} per s (one receiver path {12e6*12265*70:.2e})")
print(f"ratios: 2026 {4.253/0.436:.2f}, 2032 {1.476/0.286:.2f}; decomposition {491/254.8*120/25*(940/1550)*(0.185/0.25):.3f}")
print(f"optical energy high case per channel power: {0.885e-6/10e-6*1e3:.0f} mW")

print("\n=== OPA and §C10")
for n in (88.5, 259.3, 39.1):
    print(f"  n={n}: power per beam {n/9.8:.2f} W, x60 {60*n/9.8:.0f} W, energy {5*n/9.8:.1f} uJ, "
          f"cell-filling at eta 0.3 {20.4*n/10:.0f} W, at eta 0.1 {20.4*n/10*3:.0f} W")
for P in (1, 5, 20, 100, 200, 184):
    print(f"  coverage P={P} W: 30 photons {min(1,0.163*P/30)*100:.2f}%, 259 photons {0.163*P/259.3*100:.2f}%")
print(f"  full coverage at 259: {259.3/0.163:.0f} W")
print(f"  12 Mpts/s energy 45-132 uJ -> {45.2e-6*12e6:.0f}-{132.3e-6*12e6:.0f} W")

print("\n=== checks")
print(f"Poisson P(N>=16 | 21.34) = {stats.poisson.sf(15, 2.94+18.4):.3f}; P(N>=3 | 5.31) = {stats.poisson.sf(2, 5.31):.3f}")


def known_cell(L):
    p = 1e-3
    if L == 0:
        x = stats.gamma.isf(p, 2)
        return optimize.brentq(lambda n: stats.ncx2.sf(2 * x, 4, 2 * n) - 0.9, 0.5, 1e4)
    x = stats.gamma.isf(p, 2 * L)
    def f(n):
        g = lambda S: stats.ncx2.sf(2 * x, 4 * L, 2 * n * S / L) * stats.gamma.pdf(S, L)
        return integrate.quad(g, 0, np.inf, limit=400)[0] - 0.9
    return optimize.brentq(f, 0.5, 1e4)


print("FMCW known cell (both ramps summed, no search): steady %.1f, 4 looks %.1f, 1 look %.1f"
      % (known_cell(0), known_cell(4), known_cell(1)))
one = lambda x: x / (-np.log(0.9)) - 1
print(f"one look, one ramp, full search: x = {-np.log(1e-3/2450):.2f} -> {one(-np.log(1e-3/2450)):.1f}; "
      f"fade-only estimate 2x/0.105 = {2*11.10/0.10536:.0f}")
