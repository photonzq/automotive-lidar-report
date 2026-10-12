"""R8_C9a_inband: wavelength shares of Chinese passenger-car lidar installations
(2025 and H1 2026), f_band for a 905 nm and a 940 nm victim, and the dependent
numbers of the report's §C9a item 2. No network access; all inputs are typed in
below from the sources named in the findings file.

Inputs
- NE Times (NE时代) monthly installation charts, units, domestic retail basis:
  2025 full year (article 37913) and Jan-Feb, Mar, Apr, May, Jun 2026
  (articles 38392, 38640, 38884, 39098, 39279), main (前视主) / blind-spot (补盲).
- Gasgoo (盖世汽车研究院) 2025 supplier shares (the report's §B1) and Hesai's
  2025 total = main-lidar count (1,143,162 = 114.3万 main).
- Seyond 2025 shipments 332.5k, of which Robin 137.8k (report §B1).
Wavelength classes: '905', '940', '1550', 'U' (undisclosed or disputed).
"""

P1 = 4.17e-3  # report Eq. (124), unrounded p1 = 200.3 s^-1 x 20.83 us

# ---------------- H1 2026: NE Times monthly charts (main, blind) -------------
h1 = {
    "Hesai":     [(175444, 194), (116454, 51), (131226, 117), (139160, 9247), (152618, 19901)],
    "Huawei":    [(94093, 118438), (37059, 42279), (45654, 52050), (65875, 69813), (82250, 99844)],
    "RoboSense": [(79388, 1433), (51620, 698), (63604, 576), (80836, 620), (80815, 1020)],
    "Seyond":    [(37901, 60656), (22825, 34568), (23019, 27292), (27863, 25840), (34552, 38148)],
    "Zeekr":     [(0, 34872), (0, 28616), (0, 27996), (0, 27428), (0, 18200)],
}
months = ["Jan-Feb", "Mar", "Apr", "May", "Jun"]
tot_h1 = 0
sums = {}
for s, rows in h1.items():
    m = sum(r[0] for r in rows)
    b = sum(r[1] for r in rows)
    sums[s] = (m, b)
    tot_h1 += m + b
print("H1 2026 NE Times sums (main, blind, total):")
for s, (m, b) in sums.items():
    print(f"  {s:10s} main {m:8,d}  blind {b:8,d}  total {m + b:8,d}  share {100 * (m + b) / tot_h1:5.2f}%")
print(f"  total {tot_h1:,d}")
monthly_tot = [sum(h1[s][i][0] + h1[s][i][1] for s in h1) for i in range(5)]
print("  monthly totals:", dict(zip(months, monthly_tot)))

# Huawei 896-line share of Huawei main units: SOP March 2026; NE Times: '>57%' in May.
hw_main = [r[0] for r in h1["Huawei"]]
hw896_lo = 0.57 * (hw_main[3] + hw_main[4])          # 0 in Mar-Apr, 57% in May-Jun
hw896_c = 0.57 * sum(hw_main[1:])                    # 57% in each of Mar-Jun
hw896_hi = float(sum(hw_main[1:]))                   # all of Mar-Jun
print(f"  Huawei 896-line units: low {hw896_lo:,.0f}, central {hw896_c:,.0f}, high {hw896_hi:,.0f}")

# Seyond: blind units = Robin W (2 per NIO ES8); main = Falcon + Robin E1X (E1X cars from Apr-May 2026)
sy = h1["Seyond"]
other_main = [m - b / 2 for (m, b) in sy]            # main units not on ES8
base = (other_main[0] / 2 + other_main[1]) / 2       # Jan-Feb is two months; mean monthly Jan-Mar
e1x_c = sum(max(0.0, x - base) for x in other_main[2:])
e1x_hi = sum(x for x in other_main[2:])               # all non-ES8 main units of Apr-Jun
print(f"  Seyond non-ES8 main by month: {[round(x) for x in other_main]}, Jan-Mar monthly base {base:,.0f}")
print(f"  Robin E1X estimate: central {e1x_c:,.0f}, high {e1x_hi:,.0f} (low 0)")


def pct(x, tot):
    return 100.0 * x / tot


T = tot_h1
hes_m, hes_b = sums["Hesai"]
hw_m, hw_b = sums["Huawei"]
rs_m, rs_b = sums["RoboSense"]
sy_m, sy_b = sums["Seyond"]
zk_b = sums["Zeekr"][1]


def h1_shares(y_em, hw896, e1x, em_band, und_band):
    """y_em: EM share of RoboSense main; em_band: '940' or '905' for EM units;
    und_band: '905' or '940' for Huawei blind-spot, Huawei 896-line and Zeekr units."""
    s = {"905": 0.0, "940": 0.0, "1550": 0.0}
    s["905"] += hes_m + (hw_m - hw896) + rs_m * (1 - y_em) + sy_b
    s["940"] += hes_b + rs_b + e1x
    s[em_band] += rs_m * y_em
    s["1550"] += sy_m - e1x
    s[und_band] += hw_b + hw896 + zk_b
    return {k: pct(v, T) for k, v in s.items()}


print("\nH1 2026 shares (%), scenarios:")
cases = {
    "905 max (EM at 905, undisclosed at 905, no E1X)": (0.0, hw896_lo, 0.0, "905", "905"),
    "905 min (EM all at 940, undisclosed at 940, E1X high)": (1.0, hw896_hi, e1x_hi, "940", "940"),
    "940 min (EM none, undisclosed at 905, E1X 0)": (0.0, hw896_lo, 0.0, "905", "905"),
    "940 max (EM all at 940, undisclosed at 940, E1X high)": (1.0, hw896_hi, e1x_hi, "940", "940"),
    "documented only, EM at 940 y=0.5, central 896 and E1X, undisclosed at 905": (0.5, hw896_c, e1x_c, "940", "905"),
    "same, undisclosed at 940": (0.5, hw896_c, e1x_c, "940", "940"),
}
for name, args in cases.items():
    r = h1_shares(*args)
    print(f"  {name}: 905 {r['905']:.1f}, 940 {r['940']:.1f}, 1550 {r['1550']:.1f}")

doc905_lo = pct(hes_m + (hw_m - hw896_hi) + 0 + sy_b, T)
doc905_hi = pct(hes_m + (hw_m - hw896_lo) + rs_m + sy_b, T)
doc940_lo = pct(hes_b + rs_b, T)
doc940_hi = pct(hes_b + rs_b + e1x_hi + rs_m, T)
und_lo = pct(hw_b + hw896_lo + zk_b, T)
und_hi = pct(hw_b + hw896_hi + zk_b, T)
print(f"  documented 905: {doc905_lo:.1f}-{doc905_hi:.1f}%; documented or reported 940: {doc940_lo:.1f}-{doc940_hi:.1f}%;"
      f" undisclosed: {und_lo:.1f}-{und_hi:.1f}%; 1550: {pct(sy_m - e1x_hi, T):.1f}-{pct(sy_m, T):.1f}%")

# ---------------- 2025: Gasgoo shares (report §B1) with NE Times splits -------
g = {"Huawei": 41.5, "Hesai": 33.8, "RoboSense": 17.0, "Seyond": 7.7}
hw_main_frac = 746198 / (746198 + 538707)            # NE Times 2025 Huawei main / total
falcon_frac = (332.5 - 137.8) / 332.5                # Seyond 2025 shipments (report §B1)
print(f"\n2025: Huawei main fraction {hw_main_frac:.4f}; Seyond Falcon fraction {falcon_frac:.4f}")
y25_hi = (609.0 - 220.5) / 609.0                     # RoboSense ADAS 2025 ~609k; H1 2025 ADAS ~220.5k (interim
#                                                      results, p.1), all M platform (EM4 SOP Q3 2025, EMX from 9 Sep 2025)
print(f"  RoboSense EM share hard upper bound (H2 2025 / 2025 ADAS): {y25_hi:.3f}")
hes905 = g["Hesai"]
hw905 = g["Huawei"] * hw_main_frac
hwU = g["Huawei"] * (1 - hw_main_frac)
sy1550 = g["Seyond"] * falcon_frac
syW = g["Seyond"] * (1 - falcon_frac)
for y in (0.0, y25_hi):
    s905 = hes905 + hw905 + g["RoboSense"] * (1 - y) + syW
    s940 = g["RoboSense"] * y
    print(f"  y={y:.2f}: documented 905 {s905:.1f}%, EM (reported 940) {s940:.1f}%, 1550 {sy1550:.1f}%, undisclosed (Huawei blind-spot) {hwU:.1f}%")
    print(f"           905 range {s905:.1f}-{s905 + hwU:.1f}%, 940 range {s940:.1f}-{s940 + hwU:.1f}%")

# NE Times 2025 basis for comparison
ne25 = {"Huawei": 1284905, "Hesai": 1060296, "RoboSense": 694541, "Seyond": 259058, "Zeekr": 17568}
T25 = sum(ne25.values())
print(f"  NE Times 2025 total {T25:,d}; shares " + ", ".join(f"{k} {100 * v / T25:.1f}%" for k, v in ne25.items()))
for y in (0.0, y25_hi):
    s905 = pct(ne25["Hesai"] + 746198 + ne25["RoboSense"] * (1 - y) + ne25["Seyond"] * (1 - falcon_frac), T25)
    s940 = pct(ne25["RoboSense"] * y, T25)
    und = pct(538707 + ne25["Zeekr"], T25)
    s1550 = pct(ne25["Seyond"] * falcon_frac, T25)
    print(f"  NE basis y={y:.2f}: 905 {s905:.1f}-{s905 + und:.1f}%, 940 {s940:.1f}-{s940 + und:.1f}%, 1550 {s1550:.1f}%, undisclosed {und:.1f}%")

# ---------------- f_band ranges and dependent numbers -------------------------
print("\nDependent numbers, F = f_ov f_band f_sd with f_ov 0.25-0.6 and f_sd 0.5-1:")


def frac_hit(F, n):
    return 1 - (1 - F * P1) ** n


for label, fb_lo, fb_hi in (("current report", 0.5, 0.9), ("905 nm victim", 0.44, 0.95),
                           ("940 nm victim", 0.01, 0.5)):
    F_lo = 0.25 * fb_lo * 0.5
    F_hi = 0.6 * fb_hi * 1.0
    print(f"  {label}: f_band {fb_lo}-{fb_hi} -> F {F_lo:.4g}-{F_hi:.4g}")
    print(f"     today n=3 F_lo: {100 * frac_hit(F_lo, 3):.3f}%  n=16 F_hi: {100 * frac_hit(F_hi, 16):.2f}%")
    print(f"     later n=10 F_lo: {100 * frac_hit(F_lo, 10):.3f}%  n=30 F_hi: {100 * frac_hit(F_hi, 30):.2f}%")
    print(f"     item 3 ghost scaling: 3-of-10 bright-sun 1.1e-5 x F -> {1.1e-5 * F_lo:.2g}-{1.1e-5 * F_hi:.2g}")

# ---------------- main (forward) lidars only ----------------------------------
print("\nMain lidars only:")
# 2025, NE Times: Hesai and RoboSense counted as main; Seyond main = Falcon share of its units
m25 = {"Hesai": 1060296, "Huawei": 746198, "RoboSense": 694541, "Seyond": 259058 * falcon_frac}
Tm25 = sum(m25.values())
for y in (0.0, y25_hi):
    s905 = pct(m25["Hesai"] + m25["Huawei"] + m25["RoboSense"] * (1 - y), Tm25)
    s940 = pct(m25["RoboSense"] * y, Tm25)
    print(f"  2025 (total main {Tm25:,.0f}) y={y:.2f}: 905 {s905:.1f}%, 940 {s940:.1f}%, 1550 {pct(m25['Seyond'], Tm25):.1f}%")
Tm26 = hes_m + hw_m + rs_m + sy_m
lo905 = pct(hes_m + (hw_m - hw896_hi), Tm26)
hi905 = pct(hes_m + (hw_m - hw896_lo) + rs_m, Tm26)
hi940 = pct(rs_m + e1x_hi, Tm26)
print(f"  H1 2026 (total main {Tm26:,d}): 905 {lo905:.1f}-{hi905:.1f}%, 940 0.0-{hi940:.1f}%, "
      f"896-line {pct(hw896_lo, Tm26):.1f}-{pct(hw896_hi, Tm26):.1f}%, 1550 {pct(sy_m - e1x_hi, Tm26):.1f}-{pct(sy_m, Tm26):.1f}%")

# ---------------- cross-check against Gasgoo, Q1 2026 ---------------------------
ne_q1 = {s: sum(r[0] + r[1] for r in h1[s][:2]) for s in h1}      # Jan-Feb + Mar
ga_q1 = {"Hesai": 328246, "Huawei": 303753, "Seyond": 158008, "RoboSense": 103761, "Zeekr/others": 46888}
print("\nQ1 2026, NE Times vs Gasgoo (Gasgoo total 940,656):")
for s, g_v in ga_q1.items():
    n_v = ne_q1["Zeekr"] if s == "Zeekr/others" else ne_q1[s]
    print(f"  {s:13s} NE {n_v:8,d}   Gasgoo {g_v:8,d}   NE/Gasgoo {n_v / g_v:.3f}")
print(f"  NE total {sum(ne_q1.values()):,d}; ratio to Gasgoo {sum(ne_q1.values()) / 940656:.4f}")

# ---------------- installed base at mid-2026 ------------------------------------
pre = 0.13 + 0.57 + 1.529          # 2022, 2023 (GGAI units) and 2024 (ResearchInChina) in M
for y25 in (3.21, 3.386):
    tot = pre + y25 + tot_h1 / 1e6
    print(f"\nInstalled base mid-2026 with 2025 = {y25} M: {tot:.2f} M; 2022-2024 share {100 * pre / tot:.0f}%")

# cross-band filter check (report's drift coefficients)
print("\nCross-band check (emitter 25 C nominal):")
eel = lambda T: 905 + 0.27 * (T - 25)       # noqa: E731  905 nm EEL, 0.27 nm/K (report §C9)
vc9 = lambda T: 905 + 0.07 * (T - 25)       # noqa: E731  905 nm VCSEL, 0.07 nm/K (report §C6(d'))
vc4 = lambda T: 940 + 0.07 * (T - 25)       # noqa: E731  940 nm VCSEL
print(f"  905 EEL  -40..105 C: {eel(-40):.1f}-{eel(105):.1f} nm")
print(f"  905 VCSEL -40..105 C: {vc9(-40):.1f}-{vc9(105):.1f} nm")
print(f"  940 VCSEL -40..105 C: {vc4(-40):.1f}-{vc4(105):.1f} nm")
c_eel = (eel(-40) + eel(105)) / 2
print(f"  EEL filter centred {c_eel:.1f} nm must be >= {2 * (vc4(-40) - c_eel):.1f} nm wide to reach a cold 940 nm VCSEL"
      f" ({2 * (vc4(-40) - 905):.1f} nm if centred at 905 nm)")
print(f"  940 nm filter must be >= {2 * (940 - eel(105)):.1f} nm wide to reach a 105 C 905 nm EEL;"
      f" >= {2 * (940 - vc9(105)):.1f} nm for a 105 C 905 nm VCSEL")
print(f"  20 nm 905 nm filter (895-915) holds an EEL source only for T in "
      f"{25 - 10 / 0.27:.0f} to {25 + 10 / 0.27:.0f} C")
