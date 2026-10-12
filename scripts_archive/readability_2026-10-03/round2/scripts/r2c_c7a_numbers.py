"""Round 2 numbers for the C7a/C7/F6/D7/executive-summary edits (FMCW vs ToF system budget).

Imports the installed model build/figures/fmcw_tof_system_budget.py (read only; nothing is written)
and prints every derived number the edits quote: ToF background, dead and live fractions, counts per
bin, ideal and model requirements; energies per point; FMCW dwell, emitted energy, channels, receivers,
raw ADC data; sensor power; ratios; per-channel CW power with range for the fixed 20 mm aperture;
measured-efficiency sensitivities; the 520-line worked example; the F6 power-envelope sizing.

Run from the report folder:  python scripts_archive/readability_2026-10-03/round2/scripts/r2c_c7a_numbers.py
"""
import sys
from pathlib import Path

import numpy as np
from scipy.stats import poisson

REPORT_DIR = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(REPORT_DIR / "build" / "figures"))
import fmcw_tof_system_budget as m  # noqa: E402

H, C = m.H, m.C
R = m.R_TARGET


def p(label, value, fmt="{:.6g}"):
    print(f"{label}: {fmt.format(value)}")


print("=== ToF background, dead time, counts per bin ===")
for yr in ("2026", "2032"):
    s = m.TOF[yr]
    for k, name in enumerate(("night", "central", "full sun")):
        r_bg, f_dead, b = m.tof_background(s, k)
        r = r_bg / m.N_SPAD
        print(f"ToF {yr} {name}: r_bg={r_bg:.5g}/s, r per SPAD={r:.5g}/s, r*tau={r*m.TAU_DEAD:.5g}, "
              f"dead={f_dead*100:.3f}%, live={1-f_dead:.5f}, b per 1 ns bin over 10 shots={b:.4f}, "
              f"eta=0.5*pde*live={0.5*s['pde']*(1-f_dead):.5f}")

print("\n=== Ideal requirement (threshold, tail) ===")
for yr in ("2026", "2032"):
    s = m.TOF[yr]
    b = m.tof_background(s, 1)[2]
    n = 1
    while poisson.sf(n - 1, b) > m.P_FA_BIN:
        n += 1
    ideal = m.n_ideal(b)
    print(f"ToF {yr}: b={b:.4f}, threshold k={n}, tail at k-1={poisson.sf(n-2, b):.3g}, tail at k={poisson.sf(n-1, b):.3g}, "
          f"ideal signal={ideal:.4f}, margins={[round(x,4) for x in s['margin']]}, "
          f"n_req={[round(m.tof_n_req(s,k),3) for k in range(3)]}")

print("\n=== Energies per point (nJ), low/central/high ===")
res = {}
for name, scen, fn in [("ToF", m.TOF, m.tof_energy), ("FMCW", m.FMCW, m.fmcw_energy)]:
    for yr, s in scen.items():
        rr = [fn(s, k) for k in range(3)]
        res[(name, yr)] = rr
        for key in ("e_opt", "e_emit", "e_laser", "e_elec", "e_total"):
            print(f"{name} {yr} {key}: " + " / ".join(f"{x[key]*1e9:.3f}" for x in rr))
        if name == "ToF":
            print(f"{name} {yr} events per point: " + " / ".join(f"{x['n_events']:.1f}" for x in rr))

print("\n=== ToF E_pt worked (2026 central) ===")
s = m.TOF["2026"]
r_bg, f_dead, b = m.tof_background(s, 1)
nreq = m.tof_n_req(s, 1)
eph = m.photon_energy(s["lam"])
a = np.pi * (s["aperture_d"] / 2) ** 2
eta = s["optics"] * s["pde"] * (1 - f_dead)
num = nreq * eph * np.pi * R**2
den = m.RHO * a * eta
p("n_req", nreq); p("E_ph 940", eph); p("pi R^2", np.pi * R**2); p("A_rx", a); p("eta", eta)
p("numerator n*Eph*piR2", num); p("denominator rho*A*eta", den); p("E_pt", num / den)
for k, name in ((0, "night"), (2, "full sun")):
    rb, fd, bb = m.tof_background(s, k)
    print(f"  {name}: n_req={m.tof_n_req(s,k):.3f}, eta={0.5*0.37*(1-fd):.5f}, E={res[('ToF','2026')][k]['e_opt']*1e9:.3f} nJ")
s32 = m.TOF["2032"]
rb32, fd32, b32 = m.tof_background(s32, 1)
e26 = res[("ToF", "2026")][1]["e_opt"]
n26, n32 = m.tof_n_req(s, 1), m.tof_n_req(s32, 1)
print(f"2032 scaling: 72*(n32/n26)*(0.37*live26)/(0.45*live32) = {e26*1e9:.3f}*({n32:.3f}/{n26:.3f})*({0.37*(1-f_dead):.5f}/{0.45*(1-fd32):.5f}) = "
      f"{e26*1e9*(n32/n26)*(0.37*(1-f_dead))/(0.45*(1-fd32)):.3f} nJ")
print(f"ToF events 2026 central: r_bg*t_listen*live + n = {r_bg:.5g}*20.8e-6*{1-f_dead:.5f}+{nreq:.3f} = {r_bg*20.8e-6*(1-f_dead)+nreq:.2f}")
print(f"  Poisson spread sqrt(bg events) = {np.sqrt(r_bg*20.8e-6*(1-f_dead)):.2f}")
rbH, fdH, _ = m.tof_background(s, 2)
print(f"ToF events 2026 full sun: {rbH*20.8e-6*(1-fdH)+m.tof_n_req(s,2):.2f}; elec = 60 nJ + events*7 pJ = {60+ (rbH*20.8e-6*(1-fdH)+m.tof_n_req(s,2))*7e-3:.3f} nJ")
print(f"ToF events 2032 central: {rb32*20.8e-6*(1-fd32)+n32:.2f}; elec = 20 + events*3.5 pJ = {20+(rb32*20.8e-6*(1-fd32)+n32)*3.5e-3:.3f} nJ")

print("\n=== FMCW geometry and dwell ===")
for RR in (200.0, 250.0, 300.0):
    am, w = m.a_mode_monostatic(RR)
    print(f"A_mode({RR:.0f} m) = {am*1e6:.3f} mm^2, w = {w*1e3:.3f} mm; t^2 = {(1-np.exp(-2*(0.5/0.45)**2))**2:.5f}; "
          f"optimum t^2 lambda R/4 = {(1-np.exp(-2*(0.5/0.45)**2))**2*1550e-9*RR/4*1e6:.2f} mm^2")
d = m.fmcw_digitization(m.FMCW["2026"])
for key in ("f_beat", "f_dopp", "f_s", "t_int", "tau", "t_dwell", "n_samples"):
    p(key, d[key])
f26 = res[("FMCW", "2026")]
f32 = res[("FMCW", "2032")]
p("T_dwell/T_int", d["t_dwell"] / d["t_int"])
p("e_sample 2026 central (pJ)", f26[1]["e_sample"] * 1e12)
p("e_sample 2032 central (pJ)", f32[1]["e_sample"] * 1e12)
for yr, rr in (("2026", f26), ("2032", f32)):
    s = m.FMCW[yr]
    for k in range(3):
        es = rr[k]["e_sample"]
        samp = d["n_samples"] * es
        an = s["p_analog"][k] * d["t_dwell"]
        print(f"E_rx {yr} case{k}: 4*({d['n_samples']:.0f}*{es*1e12:.3f} pJ + {s['p_analog'][k]*1e3:.0f} mW*{d['t_dwell']*1e6:.3f} us) "
              f"= 4*({samp*1e6:.4f}+{an*1e6:.4f}) uJ = {4*(samp+an)*1e6:.4f} uJ; with 12,300: {4*(12300*es+an)*1e6:.4f}")

print("\n=== Ratios (central) ===")
t26, t32 = res[("ToF", "2026")][1], res[("ToF", "2032")][1]
p("FMCW/ToF total 2026", f26[1]["e_total"] / t26["e_total"])
p("FMCW/ToF total 2032", f32[1]["e_total"] / t32["e_total"])
p("useful optical 2026", f26[1]["e_opt"] / t26["e_opt"])
p("emitted optical 2026", f26[1]["e_emit"] / t26["e_opt"])
coll = (np.pi * 12.5**2) / (4 * m.a_mode_monostatic(R)[0] * 1e6)
det = 120 / m.tof_n_req(m.TOF["2026"], 1)
phot = 940 / 1550
eff = (0.5 * 0.37 * (1 - f_dead)) / 0.25
print(f"factors: collection {coll:.4f}, detection {det:.4f}, photon {phot:.4f}, efficiency {eff:.4f}, product {coll*det*phot*eff:.4f}")

print("\n=== Measured-efficiency sensitivity (2026 central) ===")
for eta_m in (0.168, 0.112, 0.057):
    fac = 0.25 / eta_m
    eopt = f26[1]["e_opt"] * fac
    elas = f26[1]["e_laser"] * fac
    tot = elas + f26[1]["e_elec"]
    print(f"eta={eta_m}: x{fac:.3f}, E_opt={eopt*1e6:.3f} uJ, emitted={f26[1]['e_emit']*fac*1e6:.3f} uJ, laser={elas*1e6:.3f}, "
          f"total={tot*1e6:.3f} uJ, ratio to ToF={tot/t26['e_total']:.2f}, P at 15 Mpts/s={3+15e6*tot:.1f} W")

print("\n=== Sensor power (W) ===")
for rate in (1e6, 2e6, 5e6, 10e6, 12.48e6, 12.5e6, 15e6, 25e6, 40e6):
    print(f"{rate/1e6:6.2f} Mpts/s: " + ", ".join(f"{k[0]} {k[1]} {3+rate*res[k][1]['e_total']:.2f}" for k in res))

print("\n=== Channels, receivers, raw data, optical power (2026 central chirp) ===")
for rate in (1e6, 2e6, 4e6, 5e6, 10e6, 12.48e6, 12.5e6, 15e6, 25e6, 40e6):
    nch = rate * d["t_dwell"]
    n4 = rate * (4e-6 + 2 * d["tau"])
    raw = 4 * rate * d["n_samples"] * 10
    print(f"{rate/1e6:6.2f} Mpts/s: N_ch={nch:.2f} (4 us integration: {n4:.2f}), receivers={4*nch:.1f} ({4*n4:.1f}); "
          f"raw={raw/1e12:.3f} Tb/s (running through round trips {raw*d['t_dwell']/d['t_int']/1e12:.3f}); "
          f"useful={rate*f26[1]['e_opt']:.3f} W, emitted={rate*f26[1]['e_emit']:.3f} W, heat={rate*(f26[1]['e_laser']-f26[1]['e_emit']):.3f} W, "
          f"receivers {rate*f26[1]['e_elec']:.3f} W")
d4 = m.fmcw_digitization(dict(m.FMCW["2026"], t_chirp=2e-6))
print(f"2 us chirps: f_b={d4['f_beat']/1e6:.1f} MHz, f_s={d4['f_s']/1e9:.3f} GS/s, N_samp={d4['n_samples']:.0f}, dwell={d4['t_dwell']*1e6:.3f} us")
agg = 10e6 * 4 * d["n_samples"]
print(f"Surya: aggregate {agg:.4g} samples/s -> {agg/4e9:.1f} devices at 4x1 GS/s; per-receiver ADCs: {4*10e6*d['t_dwell']/4:.1f} devices; "
      f"8x500 MS/s: {4*10e6*d['t_dwell']/8:.1f}; average rate per converter = f_s*T_int/T_dwell = {d['f_s']*d['t_int']/d['t_dwell']/1e9:.3f} GS/s")
print(f"min dwell 2 tau at 200 m = {2*d['tau']*1e6:.3f} us; at 250 m = {2*2*250/C*1e6:.3f} us; tau(250) = {2*250/C*1e6:.3f} us")

print("\n=== Per-channel CW power E_pt/T_int ===")
e200 = f26[1]["e_opt"]
a200 = m.a_mode_monostatic(200.0)[0]
for RR in (200.0, 250.0, 300.0):
    aR = m.a_mode_monostatic(RR)[0]
    eR = e200 * (RR / 200) ** 2 * a200 / aR
    print(f"{RR:.0f} m fixed 20 mm: E_pt={eR*1e6:.4f} uJ, P_ch={eR/d['t_int']*1e3:.3f} mW, emitted per point {eR*d['t_dwell']/d['t_int']*1e6:.4f} uJ; "
          f"proportional to R: {e200*RR/200/d['t_int']*1e3:.3f} mW")
print(f"central P_ch={e200/d['t_int']*1e3:.3f} mW; high case {f26[2]['e_opt']/d['t_int']*1e3:.3f} mW; low {f26[0]['e_opt']/d['t_int']*1e3:.3f} mW; "
      f"2032 central {f32[1]['e_opt']/d['t_int']*1e3:.3f} mW")
print(f"with rounded 30 mW: 250 m {30*(250/200)**2*63.7/74.5:.3f}, 300 m {30*(300/200)**2*63.7/82.0:.3f}; with 30.3: "
      f"{30.3*(250/200)**2*63.7/74.5:.3f}, {30.3*(300/200)**2*63.7/82.0:.3f}")

print("\n=== Worked example 520 x 2400 x 10 Hz ===")
for rate in (1.248e7, 1.25e7):
    print(f"rate {rate:.4g}: N_ch={rate*d['t_dwell']:.2f}, receivers={4*rate*d['t_dwell']:.1f}, useful={rate*f26[1]['e_opt']:.3f} W, "
          f"emitted={rate*f26[1]['e_emit']:.3f} W, heat={rate*(f26[1]['e_laser']-f26[1]['e_emit']):.3f} W, "
          f"receivers {rate*f26[1]['e_elec']:.3f} W, total={3+rate*f26[1]['e_total']:.3f} W, ToF={3+rate*t26['e_total']:.3f} W")

print("\n=== F6 envelope sizing ===")
per_ch = f26[1]["e_elec"] / d["t_dwell"]
p("receive power per channel (W) = E_rx/T_dwell", per_ch)
for P in (10.0, 15.0):
    print(f"{P:.0f} W: free light channels={(P-3)/per_ch:.2f}, rate={(P-3)/f26[1]['e_elec']/1e6:.3f} Mpts/s; "
          f"light paid: rate={(P-3)/f26[1]['e_total']/1e6:.3f} Mpts/s, channels={(P-3)/f26[1]['e_total']*d['t_dwell']:.2f}")
print(f"\nToF optical power at 25 Mpts/s = {25e6*t26['e_opt']:.4f} W; at 10 Mpts/s {10e6*t26['e_opt']:.4f} W")
print(f"FMCW per-channel electrical for light: emitted P_ch/eta_wp = {e200/d['t_int']*d['t_dwell']/d['t_dwell']/0.15*1e3:.1f} mW (P_ch 30 mW over the whole dwell)")
