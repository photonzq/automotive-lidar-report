"""Draft candidate-selection rules for lidar-relevant SBIR/STTR awards (superseded).

Purpose
    First pass at the keyword rules: strong lidar terms (lidar/ladar compounds, laser
    radar, detection-and-ranging expansions, laser altimeter, optical radar, laser
    ranging) plus conditional rules (FMCW with optical context, optical phased array,
    3-D laser imaging with range/depth, single-photon or SPAD with ranging, Geiger-mode,
    time-of-flight with depth excluding mass spectrometry, frequency comb with ranging,
    DIAL, laser remote sensing, laser scanning with 3-D/terrain, range-gated imaging,
    laser vibrometry, laser rangefinders, laser point clouds). Output is a candidate
    index for manual review.

Status
    Superseded by sbir_lidar_trends.py. The run was stopped because the leading
    character class in the lidar-compound pattern backtracks badly on long abstracts.
    The conditional rules are kept for the manual-review stage, which is still open.

Inputs
    <data_dir>/award_data_current.csv (SBIR.gov award file with abstracts)
Outputs
    <data_dir>/cand_idx.csv  (row index, strong-term count, strong and conditional rule names)

Usage:
    python sbir_candidate_rules_draft.py <data_dir>
"""
import os
import re
import sys

import pandas as pd

I = re.I
STRONG = [("lidar", re.compile(r"l[ai]dars?", I)),
          ("laser_radar", re.compile(r"laser[\s\-]+radars?", I)),
          ("expansion", re.compile(r"light detection and ranging|laser detection and ranging|"
                                   r"laser imaging,? detection,? and ranging", I)),
          ("laser_altimeter", re.compile(r"laser[\s\-]+altimet\w*", I)),
          ("optical_radar", re.compile(r"optical[\s\-]+radars?", I)),
          ("laser_ranging", re.compile(r"(?:laser|optical)[\s\-]+rang(?:ing|efind\w*|e[\s\-]+find\w*)", I))]


def has(p, t):
    return re.search(p, t, I) is not None


COND = {
    "fmcw": lambda t: has(r"\bFMCW\b|frequency[\s\-]modulated[\s\-]continuous[\s\-]wave", t) and has(r"laser|optical|photonic", t),
    "opa": lambda t: has(r"optical[\s\-]+phased[\s\-]+arrays?|photonic[\s\-]+phased[\s\-]+arrays?", t),
    "3d_laser": lambda t: has(r"3[\s\-]?d[\s\-]+(?:laser[\s\-]+)?imag", t) and has(r"laser", t) and has(r"\brang(?:e|es|ing)\b|time[\s\-]of[\s\-]flight|depth|point[\s\-]cloud", t),
    "single_photon": lambda t: has(r"single[\s\-]photon|photon[\s\-]counting", t) and has(r"\brang(?:e|ing)\b|altimet|time[\s\-]of[\s\-]flight", t),
    "geiger": lambda t: has(r"geiger[\s\-]mode|\bGM[\s\-]?APD", t),
    "spad": lambda t: has(r"\bSPADs?\b|single[\s\-]photon[\s\-]avalanche", t) and has(r"\brang(?:e|ing)\b|time[\s\-]of[\s\-]flight|depth|3[\s\-]?d\b", t),
    "tof": lambda t: has(r"time[\s\-]of[\s\-]flight|\bToF\b", t) and has(r"depth|3[\s\-]?d\b|\brang(?:e|ing)\b", t)
                     and not has(r"mass[\s\-]spectr|TOF[\s\-]?MS|\bSIMS\b|neutron|positron|\bPET\b|ultrason|acoustic", t),
    "comb": lambda t: has(r"frequency[\s\-]combs?|micro[\s\-]?combs?|dual[\s\-]comb", t) and has(r"\brang(?:e|ing)\b|distance", t),
    "dial": lambda t: has(r"differential[\s\-]absorption", t) and has(r"laser|lidar", t),
    "laser_remote": lambda t: has(r"(?:laser|optical)[\s\-]+remote[\s\-]+sens", t),
    "laser_scan": lambda t: has(r"laser[\s\-]+scann(?:er|ers|ing)", t) and has(r"3[\s\-]?d\b|terrain|mapping|point[\s\-]cloud", t),
    "range_gated": lambda t: has(r"range[\s\-]gat(?:ed|ing)|gated[\s\-]+(?:viewing|imag\w*)", t) and has(r"laser", t),
    "vibrometry": lambda t: has(r"laser[\s\-]+(?:doppler[\s\-]+)?vibromet\w*", t),
    "pointcloud_laser": lambda t: has(r"point[\s\-]clouds?", t) and has(r"laser", t),
}


def main(data_dir):
    c = pd.read_csv(os.path.join(data_dir, "award_data_current.csv"), dtype=str, keep_default_na=False)
    c["AY"] = pd.to_numeric(c["Award Year"], errors="coerce")
    s = c[c["AY"].between(2005, 2026)].reset_index(drop=True)
    txt = s["Award Title"] + " || " + s["Abstract"]
    rows = []
    for i, t in enumerate(txt):
        st = {k: len(p.findall(t)) for k, p in STRONG}
        cd = [k for k, f in COND.items() if f(t)]
        if sum(st.values()) or cd:
            rows.append((i, sum(st.values()), ";".join(k for k, v in st.items() if v), ";".join(cd)))
    pd.DataFrame(rows, columns=["i", "n_strong", "strong", "cond"]).to_csv(os.path.join(data_dir, "cand_idx.csv"), index=False)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    main(sys.argv[1])
