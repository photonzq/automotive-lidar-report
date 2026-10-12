"""List every occurrence of numbers and phrases that the Round 2 model changes retired, in a (merged) report copy.

Each pattern is a literal string; a hit prints the line number, the nearest heading and the text around the hit,
so that each one can be judged by hand (several values stay valid in other cases, e.g. 0.784 is the live
fraction of the fully sunlit high case).
Usage: python grep_stale_numbers.py <report copy.md> [group ...]
"""
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

GROUPS = {
    # §C7a totals and ratios before the ungated dwell and the 0.05° ToF pixel
    "totals": ["0.536", "0.54 µJ", "0.53 µJ", "≈0.53", "4.25", "4.3 µJ", "≈8×", "7.9", "1.48 µJ", "0.368",
               "≈4×", "4.0;", "≈67", "67 W", "56 W", "≈9.7", "8.4 W", "46 W", "109 W", "2.23", "2.2 µJ", "0.47 µJ",
               "2.02", "0.61 µJ", "0.32 µJ", "0.86 µJ", "19.5", "≈12 W", "44 W", "33.4", "3.4 times", "≈376", "≈26 mW",
               "≈176", "≈44 mW", "10–13×", "≈21×", "5.2–6.7", "≈11 µJ"],
    # ToF background, counts and energy before the 0.05° pixel and n_req 21.7
    "tof": ["93 nJ", "≈93", "0.093", "17.3", "17.26", "2.87", "5,960", "5,970", "5,990", "5{,}960", "5{,}970",
            "5{,}990", "4.06\\times10^{7}", "5.93\\times10^{8}", "5.93e8", "7.31\\times10^{8}", "0.614", "0.145",
            "≈22%", "21.6%", "0.244", "3.66\\times10^{8}", "n_{\\rm req}=25", "25 counts", "≈17 counts", "96 nJ",
            "≈70 nJ", "70 nJ", "126 nJ", "58–167", "≈160×", "≈15×", "390 counts", "\\approx77", "1.1\\times10^{7}",
            "0.23 nJ", "0.21 µJ", "0.93 W", "9.3 nJ", "0.84 µJ", "14.2", "3.2×", "3.25", "3.1 at 200"],
    # FMCW dwell, channels and receivers before the dwell T_int + 2 tau
    "dwell": ["10 µs dwell", "dwell}=2T", "dwell}\\approx", "T_{\\rm up}+T_{\\rm down}", "≈100 channels",
              "100 channels", "400 receivers", "≥150", "150 channels", "50–100 mW", "≈125 channels", "500 receivers",
              "24–120", "1.28\\times10^{6}", "6.4\\times10^{6}", "2,400–12,000", "1,200–5,800", "0.048°",
              "0.012^\\circ", "≥100 mW", "100 mW per channel", "20 channels", "40 for 4"],
    # eye-safety allowance and coherent link budget
    "eye_coh": ["≈9 W", "3.5–9.6", "8.6–9.6", "34–100 W", "2.58", "9.8 detected", "98 photons", "540",
                "1,590", "0.5–1.6 kW", "45–132", "≈700×", "677", "≈340×"],
}


def heading_before(lines, i):
    for k in range(i, -1, -1):
        if lines[k].startswith("#"):
            return lines[k][:70]
    return ""


text = Path(sys.argv[1]).read_text(encoding="utf-8")
lines = text.split("\n")
groups = sys.argv[2:] or list(GROUPS)
for g in groups:
    print(f"######## {g}")
    for pat in GROUPS[g]:
        hits = [(i, l) for i, l in enumerate(lines) if pat in l]
        if not hits:
            continue
        print(f"=== {pat!r}: {len(hits)} line(s)")
        for i, l in hits:
            j = l.find(pat)
            print(f"  L{i+1} [{heading_before(lines, i)}] …{l[max(0, j-110):j+90]}…")
