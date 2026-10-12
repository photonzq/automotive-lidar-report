"""Round 2, agent R2D_C7b: every number of section C7b that depends on the ToF background (0.05 x 0.05 deg
macro-pixel), the ToF n_req (x1.45 margin), the FMCW dwell T_dwell = T_int + 2 tau (ungated central case) and the
parity arithmetic of subsection 5 on that basis.

Imports the installed model build/figures/fmcw_tof_system_budget.py (read only) and prints each quantity with its
inputs. Writes nothing.

Run from the report folder:
    python scripts_archive/readability_2026-10-03/round2/scripts/r2d_c7b_numbers.py
"""
import sys
from pathlib import Path

import numpy as np
from scipy.stats import poisson

REPORT_DIR = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(REPORT_DIR / "build" / "figures"))
import fmcw_tof_system_budget as m  # noqa: E402

R = m.R_TARGET
TAU = 2 * R / m.C


def head(t):
    print(f"\n=== {t}")


# ------------------------------------------------------------------ ToF 2026 central
head("ToF 2026 central: background, dead time, counts per bin, events")
s = m.TOF["2026"]
r_bg, f_dead, b = m.tof_background(s, 1)
live = 1 - f_dead
r1 = r_bg / m.N_SPAD
print(f"r_bg = {r_bg:.5g} /s (2.965e8 x 0.37/0.3 x 0.5 = {2.965e8*0.37/0.3*0.5:.5g}); r per SPAD = {r1:.5g}; "
      f"r tau = {r1*m.TAU_DEAD:.5f}; dead = {f_dead:.5f}; live = {live:.5f}")
print(f"rounded inputs: 1.83e8/9 = {1.83e8/9:.4g}; x6 ns = {1.83e8/9*6e-9:.4f}; 1-exp(-0.122) = {1-np.exp(-0.122):.4f}")
print(f"b = r_bg x 1 ns x 10 x live = {b:.4f}; rounded 1.83e8 x 1e-9 x 10 x 0.885 = {1.83e8*1e-9*10*0.885:.4f}")
ev_bg = r_bg * s["t_listen"] * live
print(f"background events in 20.8 us = {ev_bg:.1f}; rounded 1.83e8 x 20.8e-6 x 0.885 = {1.83e8*20.8e-6*0.885:.1f}")
print(f"events / 2,080 bins = {ev_bg/2080:.4f}; 3,370/2,080 = {3370/2080:.4f}")
k = 1
while poisson.sf(k - 1, b) > m.P_FA_BIN:
    k += 1
print(f"threshold k = {k}: P(N>={k-1}|b) = {poisson.sf(k-2, b):.3g}, P(N>={k}|b) = {poisson.sf(k-1, b):.3g}")
ideal = m.n_ideal(b)
nreq = m.tof_n_req(s, 1)
print(f"ideal = {ideal:.4f}; n_req = {nreq:.4f}; margin = {nreq/ideal:.4f}; events incl. signal = {ev_bg+nreq:.1f}")
sq = np.sqrt(3370)
print(f"CW spread: sqrt(3,370) = {sq:.2f}; 5 sqrt = {5*sq:.1f}; / 21.7 = {5*sq/21.7:.2f}; exact bg: "
      f"5 sqrt({ev_bg:.0f}) = {5*np.sqrt(ev_bg):.1f}, / n_req = {5*np.sqrt(ev_bg)/nreq:.2f}")
print(f"APD 890 / 21.7 = {890/21.7:.2f}")

tof = m.tof_energy(s, 1)
eta_t = s["optics"] * s["pde"] * live
print(f"eta = 0.5 x 0.37 x {live:.4f} = {eta_t:.5f}")
num = 21.7 * 2.11e-19 * 1.26e5
den = 0.1 * 4.91e-4 * 0.164
print(f"E_pt (rounded inputs) = {num:.4g}/{den:.4g} = {num/den:.4g} J; model = {tof['e_opt']*1e9:.3f} nJ; "
      f"points per J = {1/tof['e_opt']:.4g} (1/7.2e-8 = {1/7.2e-8:.4g})")
print(f"ToF laser = {tof['e_laser']*1e9:.2f} nJ; electronics = {tof['e_elec']*1e9:.2f} nJ; total = {tof['e_total']*1e9:.2f} nJ")
e_t = tof["e_opt"]

# ------------------------------------------------------------------ FMCW
head("FMCW 2026 and 2032 central")
d = m.fmcw_digitization(m.FMCW["2026"])
f26 = [m.fmcw_energy(m.FMCW["2026"], kk) for kk in range(3)]
f32 = [m.fmcw_energy(m.FMCW["2032"], kk) for kk in range(3)]
print(f"tau = {d['tau']*1e6:.4f} us, T_int = {d['t_int']*1e6:.1f} us, T_dwell = {d['t_dwell']*1e6:.4f} us, "
      f"factor = {d['t_dwell']/d['t_int']:.5f}, N_samp = {d['n_samples']:.1f}")
for yr, rr in (("2026", f26), ("2032", f32)):
    c = rr[1]
    print(f"{yr}: E_pt {c['e_opt']*1e9:.2f} nJ, emitted {c['e_emit']*1e9:.2f}, laser {c['e_laser']*1e9:.2f}, "
          f"E_rx {c['e_elec']*1e9:.2f}, total {c['e_total']*1e9:.2f}, e_s {c['e_sample']*1e12:.3f} pJ, "
          f"P_ch = E_pt/T_int = {c['e_opt']/d['t_int']*1e3:.3f} mW")
c = f26[1]
print(f"E_rx 2026 (12,300 x 37.3 pJ + 10 mW x 12.67 us) x 4 = 4 x ({12300*37.3e-12*1e6:.4f} + {10e-3*12.667e-6*1e6:.4f}) "
      f"= {4*(12300*37.3e-12+10e-3*12.667e-6)*1e6:.4f} uJ")
print(f"E_rx searched to 200 m: 4 x (8,900 x 37.3 pJ + 0.1267 uJ) = 4 x ({8900*37.3e-12*1e6:.4f} + 0.1267) = "
      f"{4*(8900*37.3e-12+0.1267e-6)*1e6:.4f} uJ")
c32 = f32[1]
print(f"E_rx 2032 = 4 x (12,300 x 10.1 pJ + 3 mW x 12.67 us) = 4 x ({12300*10.1e-12*1e6:.4f} + {3e-3*12.667e-6*1e6:.4f}) = "
      f"{4*(12300*10.1e-12+3e-3*12.667e-6)*1e6:.4f} uJ")

# ------------------------------------------------------------------ ratios
head("Ratios at 200 m and 300 m")
e_f = c["e_opt"]
coll = 491 / 255
det = 120 / 21.7
phot = 940 / 1550
eff = 0.164 / 0.25
print(f"Eq. (104) factors: {coll:.4f} x {det:.4f} x {phot:.4f} x {eff:.4f} = {coll*det*phot*eff:.4f}; "
      f"rounded 1.93 x 5.53 x 0.606 x 0.656 = {1.93*5.53*0.606*0.656:.4f}; model ratio = {e_f/e_t:.4f}")
print(f"emitted ratio = {c['e_emit']/e_t:.4f}; 0.384/0.072 = {0.384/0.072:.3f}; per emitted J = {1/c['e_emit']:.4g}")
print(f"detection ideal 88.5/14.98 = {88.5/14.98:.3f}; 21.9/15.0 = {21.9/15.0:.4f}; 1.46 x 1.79 x 2.26 = {1.46*1.79*2.26:.3f}")
print(f"per cell: 14.6 uJ / 72 nJ = {14.6e-6/72e-9:.1f}; / model {14.6e-6/e_t:.1f}")
for eta_m in (0.168, 0.112, 0.057):
    print(f"measured eta {eta_m}: x{0.25/eta_m:.3f}; gap = {e_f*0.25/eta_m/e_t:.2f}")
print(f"10 m: 72 x (10/200)^2 = {72*(10/200)**2:.3f} nJ")
e300f = 0.30e-6 * 300 / 200
e300t = 72e-9 * (300 / 200) ** 2
print(f"300 m: FMCW 0.30 x 1.5 = {e300f*1e6:.3f} uJ; ToF 72 x 2.25 = {e300t*1e9:.1f} nJ; ratio = {e300f/e300t:.3f}; "
      f"model {e_f*1.5/(e_t*2.25):.3f}; 0.45/0.16 = {0.45/0.16:.3f}")
print(f"10 Mpts/s at 300 m: ToF light = {e300t*1e7:.3f} W; FMCW 4.5 W; ratio = {4.5/(e300t*1e7):.3f}")

# ------------------------------------------------------------------ 2(i) eye safety and 300 m ToF sensor
head("Subsection 2(i)")
print(f"ToF emits {72e-9*1e7:.3f} W at 10 Mpts/s, {72e-9*2.5e7:.3f} W at 25 Mpts/s; per shot {72/10:.1f} nJ; "
      f"model {e_t*1e7:.3f} / {e_t*2.5e7:.3f} W")
print(f"ToF at 600 m: 72 x 9 = {72*9:.0f} nJ, x 1e7 = {72e-9*9*1e7:.2f} W; / 0.26 W = {72e-9*9*1e7/0.26:.1f}; "
      f"/0.24 = {72e-9*9*1e7/0.24:.1f}, /0.28 = {72e-9*9*1e7/0.28:.1f}")
laser300 = 72e-9 * 2.25 / 0.20
tot300 = laser300 + 57e-9
p300 = 3 + 1e7 * tot300
print(f"ToF 300 m sensor: 72 x 2.25/0.20 = {laser300*1e9:.1f} nJ; + 57 = {tot300*1e9:.1f} nJ; 3 + 1e7 x = {p300:.3f} W; "
      f"model: 3 + 1e7 x ({tof['e_laser']*2.25*1e9:.1f} + {tof['e_elec']*1e9:.1f}) nJ = "
      f"{3+1e7*(tof['e_laser']*2.25+tof['e_elec']):.3f} W")
print(f"gated floor 49.4 / {p300:.2f} = {49.4/p300:.3f}; 49 / 11.7 = {49/11.7:.3f}")
print(f"ungated emission at 10 / 25 Mpts/s (model) = {1e7*c['e_emit']:.3f} / {2.5e7*c['e_emit']:.3f} W")

# ------------------------------------------------------------------ subsection 3
head("Subsection 3: channels and per-channel power")
n_tof = 15e6 * 20.8e-6
print(f"ToF macro-pixels at 15 Mpts/s = {n_tof:.0f}")
print(f"ToF receive 15e6 x 57 nJ = {15e6*57e-9:.3f} W, per pixel {15e6*57e-9/n_tof*1e3:.2f} mW; "
      f"laser 15e6 x 0.36 uJ = {15e6*0.36e-6:.2f} W, per pixel {15e6*0.36e-6/n_tof*1e3:.2f} mW; "
      f"model: {15e6*tof['e_elec']/n_tof*1e3:.2f} + {15e6*tof['e_laser']/n_tof*1e3:.2f} = "
      f"{15e6*tof['e_total']/n_tof*1e3:.2f} mW")
n_ch = 15e6 * d["t_dwell"]
rx = 15e6 * 2.34e-6
print(f"FMCW channels at 15 Mpts/s = {n_ch:.2f}; receive 15e6 x 2.34 uJ = {rx:.2f} W, per channel {rx/190*1e3:.1f} mW, "
      f"per receiver {rx/190/4*1e3:.1f} mW; model E_rx/T_dwell = {c['e_elec']/d['t_dwell']*1e3:.1f} mW")
light = 0.030 / 0.15
print(f"light per channel 0.030/0.15 = {light*1e3:.0f} mW; model emitted/T_dwell/0.15 = "
      f"{c['e_emit']/d['t_dwell']/0.15*1e3:.1f} mW; total per channel = {(rx/190+light)*1e3:.1f} mW")
tof_ch = 15e6 * tof["e_total"] / n_tof
print(f"ratio FMCW/ToF per channel = {(rx/190+light)/tof_ch:.2f} (ToF {tof_ch*1e3:.2f} mW); with 385/20 = {385/20:.2f}")
for rate in (2e6, 10e6, 15e6, 41e6, 41.04e6):
    print(f"{rate/1e6:6.2f} Mpts/s: 6.67 us -> {rate*(4e-6+2*TAU):.1f}; 12.67 us -> {rate*d['t_dwell']:.1f}")
d4 = m.fmcw_digitization(dict(m.FMCW["2026"], t_chirp=2e-6))
f200 = 2.5 * (1e9 * (2 * 200 / 3e8) / 2e-6 + 90e6)
print(f"4 us integration: T_u = 2 us, T_c = {2+TAU*1e6:.3f} us, dwell = {4+2*TAU*1e6:.3f} us; f_s at 200 m = "
      f"{f200/1e9:.3f} GS/s; 0-300 m search f_s = {d4['f_s']/1e9:.3f} GS/s; P_ch = 0.303/4 us = {0.303e-6/4e-6*1e3:.1f} mW, "
      f"0.15/4 = {0.15e-6/4e-6*1e3:.1f} mW")
print(f"P_opt 15 Mpts/s: useful {0.30e-6*15e6:.2f} W, emitted 190 x 30 mW = {190*0.030:.2f} W, "
      f"model {15e6*c['e_emit']:.3f} W")
p520 = 3 + 12.5e6 * 0.415e-6
print(f"520-line ToF unit at 12.5 Mpts/s: 3 + 12.5 x 0.415 = {p520:.3f} W; receivers 35.1 / {p520:.2f} = {35.1/p520:.2f}")

# ------------------------------------------------------------------ subsection 5: parity on the ungated basis
head("Subsection 5: parity table, ungated, T_int = 10 us unless stated")
P_OH, NDOT = 3.0, 15e6
budget = (15 - P_OH) / NDOT
print(f"budget (15 - 3)/15e6 = {budget*1e6:.3f} uJ; ToF reference total {tof['e_total']*1e6:.4f} uJ -> "
      f"P_ToF(15 Mpts/s) = {P_OH+NDOT*tof['e_total']:.3f} W; 0.8/0.415 = {0.8/0.415:.3f}; 15/9.2 = {15/9.2:.3f}")


def case(e_pt, wpe, e_rx, p_ch=None, gated=False):
    t_int = e_pt / p_ch if p_ch else 10e-6
    t_dw = t_int + 2 * TAU
    emit = e_pt if gated else e_pt * t_dw / t_int
    las = emit / wpe
    tot = las + e_rx
    return dict(t_int=t_int, t_dw=t_dw, emit=emit, las=las, tot=tot, P=P_OH + NDOT * tot, nch=NDOT * t_dw,
                pch=e_pt / t_int, rx_ch=e_rx / t_dw)


rows = [
    ("ToF 2026 reference", None),
    ("2026 central", (c["e_opt"], 0.15, c["e_elec"])),
    ("2032 optimistic", (c32["e_opt"], 0.22, c32["e_elec"])),
    ("all three (15 mW, 190 ch)", (0.15e-6, 0.30, 0.10e-6)),
    ("eta_wp 15%", (0.15e-6, 0.15, 0.10e-6)),
    ("E_rx 0.30", (0.15e-6, 0.30, 0.30e-6)),
    ("E_rx today", (0.15e-6, 0.30, c["e_elec"])),
    ("E_pt 0.30", (c["e_opt"], 0.30, 0.10e-6)),
]
for name, args in rows:
    if args is None:
        print(f"{name:28s}: E_pt {tof['e_opt']*1e9:.1f} nJ, laser {tof['e_laser']*1e9:.1f}, rx {tof['e_elec']*1e9:.1f}, "
              f"total {tof['e_total']*1e9:.1f} nJ, P {P_OH+NDOT*tof['e_total']:.2f} W")
        continue
    r = case(*args)
    print(f"{name:28s}: E_pt {args[0]*1e6:.3f} uJ, P_ch {r['pch']*1e3:.1f} mW, emitted {r['emit']*1e6:.4f}, "
          f"laser {r['las']*1e6:.4f}, E_rx {args[2]*1e6:.4f}, total {r['tot']*1e6:.4f} uJ, P = {r['P']:.2f} W, "
          f"x ToF {r['tot']/tof['e_total']:.2f}, channels {r['nch']:.0f}, rx per channel {r['rx_ch']*1e3:.2f} mW")
for name, kw in (("all three, 30 mW ungated", dict(p_ch=0.030)), ("all three, 30 mW gated", dict(p_ch=0.030, gated=True)),
                 ("all three, 22.5 mW ungated", dict(p_ch=0.0225))):
    r = case(0.15e-6, 0.30, 0.10e-6, **kw)
    print(f"{name:28s}: T_int {r['t_int']*1e6:.3f} us, T_dwell {r['t_dw']*1e6:.3f} us, emitted {r['emit']*1e6:.4f}, "
          f"total {r['tot']*1e6:.4f}, P {r['P']:.2f} W, channels {r['nch']:.1f}, rx per channel {r['rx_ch']*1e3:.2f} mW "
          f"({r['rx_ch']/4*1e3:.2f} per receiver)")
fac_max = (budget - 0.10e-6) * 0.30 / 0.15e-6
pch_max = (fac_max - 1) * 0.15e-6 / (2 * TAU)
print(f"ungated limit: T_dwell/T_int <= ({budget*1e6:.2f} - 0.10) x 0.30/0.15 = {fac_max:.4f}; "
      f"P_ch <= {fac_max-1:.4f} x 0.15 uJ / {2*TAU*1e6:.4f} us = {pch_max*1e3:.2f} mW; channels = "
      f"{NDOT*(0.15e-6/pch_max+2*TAU):.1f}")
erx_max = budget - 0.19e-6 / 0.30
print(f"receiver limit with the other two met (ungated, 15 mW): {erx_max*1e6:.4f} uJ; today/limit = "
      f"{c['e_elec']/erx_max:.2f}; today/0.30 = {c['e_elec']/0.30e-6:.2f}")
for eta_m in (0.168, 0.112, 0.057):
    ep = c["e_opt"] * 0.25 / eta_m
    em = ep * d["t_dwell"] / d["t_int"]
    tot = em / 0.15 + c["e_elec"]
    print(f"measured eta {eta_m}: E_pt {ep*1e6:.4f}, emitted {em*1e6:.4f}, total {tot*1e6:.4f} uJ, P {P_OH+NDOT*tot:.2f} W")
print(f"rounded check eta 0.112: 0.303 x 0.25/0.112 = {0.303*0.25/0.112:.4f}; x 1.267 = {0.303*0.25/0.112*1.267:.4f}; "
      f"3 + 15 x (0.86/0.15 + 2.34) = {3+15*(0.86/0.15+2.34):.2f}")
rx_ch_today = c["e_elec"] / d["t_dwell"] / 4
print(f"today's receiver = {rx_ch_today*1e3:.2f} mW; vs 0.10 uJ over 190/140/115 channels: "
      + ", ".join(f"{0.10e-6*NDOT/n*1e3:.2f} mW ({0.10e-6*NDOT/n/4*1e3:.2f}/rx, ratio {rx_ch_today/(0.10e-6*NDOT/n/4):.1f})"
                  for n in (190, 140, 115)))
print(f"signpost: 64/190 = {64/190:.2f}, 64/115 = {64/115:.2f}; 5/2.0 = {5/1.97:.2f}, 5/3.3 = {5/3.26:.2f}; "
      f"10 W / 1,024 = {10/1024*1e3:.1f} mW")
print(f"parity light at 15 Mpts/s: useful 0.15 x 15 = {0.15*15:.2f} W, emitted 190 x 15 mW = {190*0.015:.2f} W")
gated12 = P_OH + NDOT * (0.15e-6 / 0.30 + 0.10e-6)
print(f"gated all three = {gated12:.2f} W; x ToF energy = {(0.15/0.30+0.10)/0.415:.2f}; ungated 0.733/0.415 = {0.733/0.415:.2f}")
need = tof["e_total"] - 0.10e-6
print(f"to match ToF with E_rx 0.10, gated, eta_wp 0.30: E_pt <= {need*0.30*1e6:.4f} uJ -> eta = 0.25 x 0.303/E_pt = "
      f"{0.25*c['e_opt']/(need*0.30):.3f}")
