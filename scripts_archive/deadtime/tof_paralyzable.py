"""ToF numbers with the paralyzable dead-time model (Sony passive recharge): live fraction exp(-r tau)."""
import math
from scipy import stats, optimize

TAU, NSPAD = 6e-9, 9
BG_PER_PDE = 5.93e8 / 0.3


def live(pde, scene):
    r = BG_PER_PDE * pde * scene
    x = r / NSPAD * TAU
    return r, x, math.exp(-x)


def need(b, p, pd=0.9):
    k = 0
    while stats.poisson.sf(k - 1, b) > p:
        k += 1
    s = optimize.brentq(lambda s: stats.poisson.sf(k - 1, s + b) - pd, 1e-6, 500)
    return k, s


print("=== live fractions (paralyzable) vs non-paralyzable")
for lab, pde, sc in [("2026 central", 0.37, 0.5), ("2026 full sun", 0.37, 1.0), ("2032 central", 0.45, 0.5),
                     ("2032 full sun", 0.45, 1.0), ("C6(d) 940/10nm PDE0.3 rho0.9", 0.30, 1.0)]:
    r, x, L = live(pde, sc)
    b = r * 1e-9 * 10 * L
    ev = r * 20.8e-6 * L
    print(f"{lab:30s} r_bg {r:.4g} rtau {x:.4f} live {L:.4f} (nonpar {1/(1+x):.4f}) dead {1-L:.3f}  b {b:.3f}  events {ev:.0f}")
for lab, rbg in [("905/20nm", 2.2e9), ("905/40nm", 4.4e9), ("940/10nm", 5.93e8)]:
    x = rbg / 9 * TAU
    print(f"C6(d) table {lab}: rtau {x:.3f} dead paralyzable {1-math.exp(-x):.3f} nonpar {x/(1+x):.3f}")

print("\n=== ToF detection at 1e-3 false points per point, 2,000 bins (p = 5e-7)")
p = 1e-3 / 2000
r, x, L = live(0.37, 0.5)
b = r * 1e-9 * 10 * L
for lab, bb in [("night", 0.01), ("central sun", b), ("full sun", live(0.37, 1.0)[0] * 1e-8 * live(0.37, 1.0)[2]),
                ("2-bin central", 2 * b), ("3-bin central", 3 * b)]:
    k, s90 = need(bb, p)
    k5, s50 = need(bb, p, 0.5)
    print(f"{lab:14s} b {bb:6.3f} n_th {k:2d}  P(N>=n_th|b) {stats.poisson.sf(k-1,bb):.2e}  P(N>=n_th-1|b) {stats.poisson.sf(k-2,bb):.2e}"
          f"  s50 {s50:5.1f} s90 {s90:5.1f}  P_D(25) {stats.poisson.sf(k-1, 25+bb):.3f}  P_D(120) {stats.poisson.sf(k-1,120+bb):.3f}")
for lab, pp in [("tracking 20 bins", 1e-3 / 20), ("relaxed 1e-2/pt", 1e-2 / 2000), ("known bin", 1e-3)]:
    k, s90 = need(b, pp)
    print(f"  central sun {lab:18s} n_th {k} s90 {s90:.1f}")
k, s90 = need(b, p)
print(f"worked: s+b = {s90+b:.2f}; P(N>={k}|{s90+b:.2f}) = {stats.poisson.sf(k-1, s90+b):.3f}")

print("\n=== ToF energy")
Eph, R, rho, A = 2.1133e-19, 200.0, 0.1, math.pi * 0.0125**2
for yr, pde, wpe, efix, eev in [("2026", 0.37, 0.20, 40e-9, 5e-12), ("2032", 0.45, 0.25, 20e-9, 3.5e-12)]:
    rr, xx, LL = live(pde, 0.5)
    eta = 0.5 * pde * LL
    eo = 25 * Eph * math.pi * R**2 / (rho * A * eta)
    ev = rr * 20.8e-6 * LL + 25
    tot = eo / wpe + efix + ev * eev
    print(f"{yr}: eta {eta:.4f} E_opt {eo*1e9:.1f} nJ laser {eo/wpe*1e9:.0f} nJ events {ev:.0f} elec {(efix+ev*eev)*1e9:.1f} nJ total {tot*1e9:.0f} nJ")
