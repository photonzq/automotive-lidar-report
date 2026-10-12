"""After a merge, list every remaining use of a symbol that the report-wide scheme (fix_spec.md) replaces.

Each pattern is a regular expression on the Markdown source. A hit is not necessarily wrong (for example
$E_{\\rm opt}$ in §C0 subsection 10.6 is the best design's energy, not the optical energy per point), so every hit
is printed with its line number and the nearest heading for a human decision.
Usage: python post_merge_symbol_check.py [--file PATH]
"""
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
REPORT = Path(r"<report folder>\automotive_perception_report_2026-09-27.md")
if sys.argv[1:2] == ["--file"]:
    REPORT = Path(sys.argv[2])
text = REPORT.read_text(encoding="utf-8")
lines = text.split("\n")

PATTERNS = {
    "E_opt": r"E_\{\\rm opt\}",
    "E_tx": r"E_\{\\rm tx\}",
    "E_pulse": r"E_\{\\rm pulse\}",
    "E_point": r"E_\{\\rm point\}",
    "E_s (energy per sample)": r"E_s(?![a-z])",
    "Omega as a scan rate": r"\\Omega\s*(D|\\cdot|T_c|/\\theta|\\lesssim)|2R\s*\\Omega|R\\,\\Omega|\\theta_b/\\Omega|\\Omega_\{\\max\}",
    "omega as a scan rate": r"\\omega(?![a-z])",
    "eta_WPE": r"\\eta_\{\\rm WPE\}",
    "P_0 overhead": r"P_0(?![0-9])",
    "t_bin without Delta": r"(?<!\\Delta )t_\{\\rm bin\}",
    "theta_step": r"\\theta_\{\\rm step\}",
    "Delta theta_h/v": r"\\Delta\\theta_[hv](?![a-z])",
    "Q_M Marcum": r"Q_M\(",
    "M_0 margin": r"(?<!\\mathcal\{)M_0(?![0-9])",
    "v^2/(2a) bare a": r"v\^2/\(?2a\)?(?!_)|\\frac\{v\^2\}\{2a\}",
    "Delta t as delay": r"R=c\\,?\\Delta t/2|\\Delta t=2R/c",
    "f=S/2 bare f": r"(?<![a-z_])f=S/2",
    "time to contact tau (E12)": r"\\tau=\\varphi/\\dot\\varphi|\\tau=\\frac\{w\}",
    "R_max as grid half-width": r"2R_\{\\max\}\}\{\\Delta_\{\\rm cell\}",
    "Delta f as scan spread": r"\\Delta f\\approx\(?\\Omega|\\Delta f\s*\\approx\s*\\dot\\theta",
    "theta_wo": r"\\theta_\{\\rm wo\}",
    "S in Eq. (40) / lidar ratio": r"S=\\alpha/\\beta|e\^\{-S\}",
}


def heading_for(idx):
    for j in range(idx, -1, -1):
        if lines[j].startswith("#"):
            return lines[j][:70]
    return "(top)"


line_starts = [0]
for ln in lines[:-1]:
    line_starts.append(line_starts[-1] + len(ln) + 1)


def line_of(pos):
    lo, hi = 0, len(line_starts) - 1
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if line_starts[mid] <= pos:
            lo = mid
        else:
            hi = mid - 1
    return lo


for name, pat in PATTERNS.items():
    hits = list(re.finditer(pat, text))
    print(f"### {name}: {len(hits)}")
    for m in hits[:25]:
        i = line_of(m.start())
        a, b = max(0, m.start() - 90), min(len(text), m.end() + 90)
        print(f"  L{i + 1} [{heading_for(i)}]: …{text[a:b].replace(chr(10), ' ⏎ ')}…")
