"""Simple arithmetic on the values read from the sources (no simulation).
1) Gillette (1983) Eq. 3.11 with a = 0.21 / 0.32 / 0.53 (Navvab et al. 1983 design values), m = 1/sin h.
2) Solar altitudes for Kimball & Hand (1922) Table 7 entries at 42 N.
3) Ratio k = shaded vertical / direct normal from Kimball & Hand skylight values + isotropic ground term.
"""
import math

FC = 10.764  # lux per foot-candle
EVSC = 127.5  # klx, Gillette 1983 p23

print("1) E_DN = 127.5 exp(-a/sin h) klx (no Earth-Sun distance correction)")
for h in (5, 10, 15, 20, 25, 30, 45, 60, 90):
    s = math.sin(math.radians(h))
    vals = [EVSC * math.exp(-a / s) for a in (0.21, 0.32, 0.53)]
    print(f"  h={h:2d}  a=0.21: {vals[0]:6.1f}  a=0.32: {vals[1]:6.1f}  a=0.53: {vals[2]:6.1f}")

print("\n2) Kimball & Hand Table 7 entries: altitude at 42 N (declination on the 21st)")
lat = math.radians(42.0)
table7 = {
    "Dec21": (-23.44, [7600, 7300, 6640, 5190, 2460]),
    "Jan21": (-20.0, [8120, 7890, 7290, 6040, 3760]),
    "Mar21": (0.0, [9270, 9110, 8710, 7910, 6700, 4650, 720]),
    "Jun21": (23.44, [9080, 9000, 8740, 8220, 7430, 6420, 4880, 2160]),
    "Sep21": (0.0, [8910, 8760, 8510, 7710, 6500, 4590, 720]),
}
for day, (dec, vals) in table7.items():
    d = math.radians(dec)
    row = []
    for H, fc in enumerate(vals):
        sh = math.sin(lat) * math.sin(d) + math.cos(lat) * math.cos(d) * math.cos(math.radians(15 * H))
        h = math.degrees(math.asin(sh)) if sh > -1 else float("nan")
        model = EVSC * math.exp(-0.21 / sh) if sh > 0.01 else float("nan")
        row.append(f"H{H}: h={h:5.1f} E={fc * FC / 1000:5.1f} klx (a=.21 model {model:5.1f})")
    print(" ", day)
    for r in row:
        print("     ", r)

print("\n3) k from Kimball & Hand winter curves (Fig 6, read by eye) with E_DN range from BSS152 Fig 6.6 (read by eye)")
# h: (vertical 180 sky-only fc, horizontal sky-only fc, E_DN low klx, E_DN high klx)
rows = {
    5: (100, 220, 11.0, 25.0),
    10: (170, 375, 37.0, 52.0),
    15: (220, 530, 52.0, 66.0),
    20: (257, 683, 60.0, 72.0),
    30: (285, 830, 75.0, 92.0),
}
for h, (v180, hor, elo, ehi) in rows.items():
    s = math.sin(math.radians(h))
    ev = v180 * FC / 1000
    ed = hor * FC / 1000
    out = [f"h={h:2d}: Ev180={ev:4.2f} klx Edh={ed:4.2f} klx"]
    for edn in (ehi, elo):
        ksky = ev / edn
        kg = {rho: 0.5 * rho * (s + ed / edn) for rho in (0.04, 0.12, 0.20)}
        out.append(f"   E_DN={edn:5.1f}: k_sky={ksky:.3f}; +ground rho .04/.12/.20 -> "
                   f"{ksky + kg[0.04]:.3f}/{ksky + kg[0.12]:.3f}/{ksky + kg[0.20]:.3f}")
    print("\n".join(out))

print("\n4) Summer 20/40 deg and winter 40 deg from Table 4 with E_DN interpolated from Table 7 (my interpolation)")
# summer 20 deg: Jun21 H=5 (h~26.3, 6420 fc) and H=6 (h~15.4, 4880 fc)
e_s20 = 4880 + (20 - 15.4) / (26.3 - 15.4) * (6420 - 4880)
print(f"  summer 20deg: E_DN~{e_s20:.0f} fc; k_sky = 293/{e_s20:.0f} = {293 / e_s20:.3f}; Edh/Edn = {840 / e_s20:.3f}")
# winter 20 deg: Dec21 H=2 (h~18.9, 6640) and Jan21 H=2 (h~22.1, 7290)
e_w20 = 6640 + (20 - 18.9) / (22.1 - 18.9) * (7290 - 6640)
print(f"  winter 20deg: E_DN~{e_w20:.0f} fc; k_sky = 257/{e_w20:.0f} = {257 / e_w20:.3f}; Edh/Edn = {683 / e_w20:.3f}")

print("\n5) Mean solar disc luminance L = E_DN / Omega")
diam_as = 1919.0
r = math.radians(diam_as / 3600 / 2)
omega = 2 * math.pi * (1 - math.cos(r))
print(f"  Omega = {omega:.4e} sr (diameter {diam_as/3600:.4f} deg)")
for e in (127.5, 133.8, 109.0, 105.3, 100.0, 92.0, 75.0, 72.0, 60.0, 52.0, 37.0, 25.0, 11.0):
    print(f"  E_DN={e:6.1f} klx -> L={e * 1000 / omega:.3e} cd/m2")

print("\n6) Hagita & Mori Table 1: fraction of daytime by elevation band (Chiba 35.6N)")
tot_day = 8760 - 4365.5
print(f"  all year: el 0-10: {643.0 / tot_day:.3f}, 10-20: {667.2 / tot_day:.3f}, 20-30: {766.5 / tot_day:.3f}, 0-20: {(643.0 + 667.2) / tot_day:.3f}")
w_day = 2160 - 1252.7
s_day = 2208 - 925.4
print(f"  winter 0-20: {(168.5 + 190.1) / w_day:.3f};  summer 0-20: {(161.7 + 155.8) / s_day:.3f}")
for half in (20, 25):
    p = 2 * half / 360
    print(f"  uniform headings, |dAz|<{half}: p={p:.3f}; x year 0-20 -> {p * (643.0 + 667.2) / tot_day:.3f}")
