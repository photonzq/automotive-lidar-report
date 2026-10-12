"""Laser and lidar export-control texts behind the 2026-10-03 answer, and the emitter margin estimates.

Downloads (cached in OUT): eCFR Title 15 parts 744, 772 and 774 as of a fixed date, and the Wassenaar 2025 list.
Prints the ECCN 6A005, 6A995, 6A008 and 6A998 extracts (also written to OUT), the Part 772 laser definitions,
the 6A995 line of Supplement No. 2 to Part 744, and the Wassenaar 1,555 nm / 1,570 nm lines with the new
6.A.5.c.3 Note. Then it prints the average-power margins of typical lidar emitters against the nearest 6A005
threshold. The emitter values are illustrative class values (and the report's own FMCW/ToF budgets), not
data for specific products.
Usage: python laser_lidar_rules.py [out_dir] [ecfr_date]
"""
import math
import re
import subprocess
import sys
from pathlib import Path

import pymupdf
from lxml import etree

OUT = Path(sys.argv[1] if len(sys.argv) > 1 else "export_controls_data")
DATE = sys.argv[2] if len(sys.argv) > 2 else "2026-09-24"
OUT.mkdir(parents=True, exist_ok=True)
ECFR = "https://www.ecfr.gov/api/versioner/v1/full/{date}/title-15.xml?part={part}"
WA2025 = "https://www.wassenaar.org/app/uploads/2025/12/List-of-Dual-Use-Goods-and-Technologies-and-ML-2025.pdf"
CCL_TAGS = ("P", "FP", "FP-1", "FP-2", "HED", "HD1", "HD2", "TD", "TH")


def fetch(url, path):
    if not path.exists():
        subprocess.run(["curl", "-s", "-L", "--compressed", "-A", "Mozilla/5.0", "-o", str(path), url], check=True)
    return path


def flat(el):
    return " ".join("".join(el.itertext()).split())


parts = {p: etree.fromstring(fetch(ECFR.format(date=DATE, part=p), OUT / f"p{p}.xml").read_bytes())
         for p in (744, 772, 774)}

# CCL entries: header lines sit in FP-2; an entry runs to the next ECCN header.
ccl = "\n".join(flat(e) for e in parts[774].iter(*CCL_TAGS))
head = re.compile(r"\n\d[A-E]\d{3} [A-Z“\"']")
for code in ("6A005", "6A995", "6A008", "6A998"):
    i = ccl.find(f"\n{code} ")
    m = head.search(ccl, i + 1)
    entry = ccl[i + 1:m.start() if m else None]
    (OUT / f"e{code}.txt").write_text(entry, encoding="utf-8")
    print(f"--- {code}: {len(entry.splitlines())} lines written")
    for line in entry.splitlines():
        if re.search(r"1,555|1,570|1,400 nm and|Reason for Control|j\.2\.|monolithic|specially designed” for other", line):
            print("   ", line[:200])

# Part 772 definitions used in the answer.
defs = "\n".join(flat(p) for p in parts[772].xpath('//DIV8[@N="772.1"]')[0].iter("P", "FP", "FP-1"))
for key in ("Laser", "Tunable", "Pulsed Laser", "CW Laser", "Peak power", "Pulse duration"):
    m = re.search(rf"^[“\"]?{re.escape(key)}[”\"]?\. ?\(Cat[^\n]*", defs, re.M)
    print("DEF", (m.group(0) if m else f"{key}: not found")[:300])

# 6A995 on the military end-use list (Supplement No. 2 to Part 744).
sup2 = flat(parts[744].xpath('//DIV9[contains(@N,"Supplement No. 2 to Part 744")]')[0])
m = re.search(r"6A995[^.]{0,120}\.", sup2)
print("Supp. 2 to Part 744:", m.group(0) if m else "6A995 not found")

# Wassenaar 2025: the same wavelength boundaries, and the new tunable-laser Note.
wa = pymupdf.open(fetch(WA2025, OUT / "wa2025.pdf"))
wt = " ".join(" ".join(p.get_text() for p in wa).split())
for m in re.finditer(r".{0,90}(?:1,555|1,570) nm.{0,120}", wt):
    print("WA:", m.group(0))
m = re.search(r"Note 6\.A\.5\.c\.3\..{0,330}", wt)
print("WA:", m.group(0) if m else "6.A.5.c.3 Note not found")

# Emitter margins: average power P = P_peak * tau * f (or E_pulse * f) against the nearest 6A005 threshold.
rows = [
    # name, average power W, 6A005 threshold W, entry
    ("905 nm multi-junction EEL, 100 W peak, 5 ns, 100 kHz", 100 * 5e-9 * 1e5, 25, "6A005.d.1.b.1"),
    ("905 nm 4-channel EEL bar, 500 W peak, 5 ns, 100 kHz", 500 * 5e-9 * 1e5, 100, "6A005.d.1.c.1"),
    ("1,550 nm DFB seed, 50 mW CW (single-mode diode)", 0.05, 2.0, "6A005.d.1.a.1"),
    ("1,550 nm seed+SOA per channel, 100 mW (report C7b 2(i))", 0.10, 2.0, "6A005.d.1.a.1"),
    ("same above 1,570 nm", 0.10, 0.5, "6A005.d.1.a.2"),
    ("1,550 nm pulsed fiber MOPA, 2 uJ at 1 MHz", 2e-6 * 1e6, 20, "6A005.b.7.a.2"),
    ("same at 1,560 nm", 2e-6 * 1e6, 1, "6A005.b.8.b"),
    ("1,550 nm CW EDFA booster, 3.0 W (report FMCW, 200 m, 10 Mpts/s)", 3.0, 50, "6A005.a.7.a"),
    ("1,550 nm CW EDFA booster, 11.4 W (report FMCW, 300 m, 25 Mpts/s)", 11.4, 50, "6A005.a.7.a"),
    ("same 11.4 W at 1,560 nm", 11.4, 1, "6A005.a.8"),
]
print("\nemitter | average power | threshold | ratio threshold/average")
for name, p, thr, entry in rows:
    print(f"{name:<66} {p:8.3f} W  {entry} > {thr:g} W   {thr / p:8.1f}")

# Report's ToF transmit budget (93.3 nJ per point at 200 m, E ~ R^2) and a VCSEL power-density check.
for R, ndot in ((200, 1e7), (300, 2.5e7)):
    p = 93.3e-9 * (R / 200) ** 2 * ndot
    for area_mm2, fill in ((2.0, 1.0), (2.0, 0.2)):
        dens = p / (area_mm2 * fill * 1e-2)
        print(f"ToF {R} m, {ndot / 1e6:.0f} Mpts/s: {p:.2f} W; density over {area_mm2 * fill:.1f} mm2 = {dens:.0f} W/cm2 "
              f"(6A005.d.1.d.1.a line 500 W/cm2)")

# System level: 6A008.j.2 needs angular resolution finer than 20 urad.
for deg in (0.05, 0.1):
    urad = deg * math.pi / 180 * 1e6
    print(f"{deg} deg = {urad:.0f} urad = {urad / 20:.0f} x the 20 urad line")
# FMCW chirp excursion in wavelength: d_lambda = lambda^2 d_nu / c.
for dnu in (1e9, 10e9):
    print(f"chirp {dnu / 1e9:.0f} GHz at 1,550 nm = {1.55e-6 ** 2 * dnu / 3e8 * 1e12:.0f} pm")
