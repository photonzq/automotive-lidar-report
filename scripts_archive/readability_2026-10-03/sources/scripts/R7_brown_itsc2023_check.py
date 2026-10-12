"""R7 item 06: consistency check of Brown et al., IEEE ITSC 2023 (OSTI 2311313).

Inputs are read from the paper's rendered pages (Tables I, III, IV) and from Kia's
2015 Soul EV overview (27 kWh pack). Run with the Anaconda interpreter.
"""

# Table IV: per-unit (theoretical W, actual W); Table I: quantity
items = {
    "ZED 2i stereo camera": (1.9, 1.22, 1),
    "Basler IMX273 camera": (3.3, 1.42, 6),
    "Aptiv ESR 2.5 radar": (12.0, 6.25, 2),
    "Ouster OS1": (23.0, 24.0, 1),
    "Ouster OS2": (28.0, 24.0, 1),
    "Swift Duro GNSS": (5.0, 6.25, 2),
    "Smartmicro UMRR-96": (5.0, 2.7, 1),
    "Lufft Marwis": (37.8, 16.2, 1),
    "Modem": (8.0, 5.0, 1),
    "LAN switches": (2.43, 2.2, 2),
    "Nuvo-8108GC XL (RTX 3060)": (325.0, 125.0, 1),
    "HP Omen laptop": (250.0, 200.0, 1),
    "Micro screen": (3.0, 1.2, 1),
    "Drive-kit": (25.0, 9.45, 1),
}
theo = sum(t * q for t, a, q in items.values())
act = sum(a * q for t, a, q in items.values())
act_noq = sum(a for t, a, q in items.values())
comp = items["Nuvo-8108GC XL (RTX 3060)"][1] + items["HP Omen laptop"][1]
print(f"Table IV totals with Table I quantities: theoretical {theo:.1f} W, actual {act:.1f} W "
      f"(paper: 765.4, 446.7); without quantities actual = {act_noq:.2f} W")
print(f"two computers actual = {comp:.0f} W; sensing+instrumentation actual = {act - comp:.1f} W")

# Table III: SoC drop per cycle (percentage points) and extrapolated range (mi)
dsoc = {"baseline": 10.36, "sensors": 11.05, "sensors+compute": 11.9}
rng = {"baseline": 127.5, "sensors": 120.4, "sensors+compute": 112.0}
d_cycle_mi, t_cycle_s = 17.71, 2149.0
t_h = t_cycle_s / 3600.0
v_kmh = d_cycle_mi * 1.609344 / t_h
print(f"cycle mean speed = {v_kmh:.2f} km/h")
for k in ("sensors", "sensors+compute"):
    loss_rng = 1 - rng[k] / rng["baseline"]
    loss_soc = 1 - dsoc["baseline"] / dsoc[k]
    print(f"{k}: range loss from Table III ranges = {100 * loss_rng:.2f}%; "
          f"if range were proportional to 1/dSoC = {100 * loss_soc:.2f}%")
for k in dsoc:
    print(f"implied SoC window for {k}: {rng[k] * dsoc[k] / d_cycle_mi:.2f} %-points")

E_bat = 27.0  # kWh, Kia 2015 Soul EV overview
P0 = dsoc["baseline"] / 100 * E_bat / t_h
print(f"baseline mean battery power = {P0 * 1000:.0f} W "
      f"({dsoc['baseline'] / 100 * E_bat / (d_cycle_mi * 1.609344) * 100:.2f} kWh/100 km)")
dP_s = (dsoc["sensors"] - dsoc["baseline"]) / 100 * E_bat / t_h
dP_c = (dsoc["sensors+compute"] - dsoc["sensors"]) / 100 * E_bat / t_h
print(f"extra mean battery power from dSoC: sensors {dP_s * 1000:.0f} W, compute increment "
      f"{dP_c * 1000:.0f} W, total {(dP_s + dP_c) * 1000:.0f} W")

# Report range-loss equation (Eq. (158) at report sha 51d60fa27199): loss = x/(e0+x), so an equivalent constant load dP = P0 * L/(1-L)
for k, L in (("sensors", 0.056), ("sensors+compute", 0.122)):
    print(f"range-loss eq.: constant load equivalent to {100 * L:.1f}% loss = {P0 * L / (1 - L) * 1000:.0f} W")
for name, dP in (("tabulated sensing 121.7 W", 0.1217), ("tabulated total 446.7 W", 0.4467)):
    print(f"range-loss eq.: loss for {name} at P0 = {P0 * 1000:.0f} W: {100 * dP / (P0 + dP):.2f}%")

# The report's own scaling check (x proportional to load, anchored at 12.2% for 447 W)
xr = 0.122 / (1 - 0.122)
xs = xr * 122 / 447
print(f"report check: x/e0 = {xr:.4f}; scaled to 122 W: {xs:.4f}; loss = {100 * xs / (1 + xs):.2f}%")
