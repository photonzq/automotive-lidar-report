"""Insert the new C0 subsection 10.7 (dynamic range), move 'What the model leaves out' to 10.8, add the
FMCW efficiency caveat to 10.1, extend the intro, and renumber equations globally."""
import hashlib
import re
import sys
from pathlib import Path

REPORT = Path(r"<report folder>\automotive_perception_report_2026-09-27.md")
SCR = Path(r"<scratch>")
SNAP = SCR / "rewrite" / "report_after_peer_rebaseline.md"
NEW = SCR / "mech" / "c0_10_7_dynamic_range.md"
OUT_SNAP = SCR / "rewrite" / "report_after_c0_10_7.md"
DRY = "--dry" in sys.argv

raw = REPORT.read_bytes()
assert hashlib.sha256(raw).digest() == hashlib.sha256(SNAP.read_bytes()).digest(), "report changed since the snapshot"
s = raw.decode("utf-8")
sec = NEW.read_text(encoding="utf-8").rstrip("\n") + "\n\n"
assert "\r" not in s + sec and "\t" not in sec

ETA_NOTE = ("  - **The FMCW value, 0.25, is a design value at the optimistic end of what has been measured.** "
            "Waymo's lab chain measured 0.112 end to end, or 0.168 without its Hann window (Piggott et al. 2025, App. A), "
            "and Pointcloud's integrated array 0.057 once its amplifier noise is counted (Settembrini et al. 2026). "
            "With those values FMCW needs 1.5–2.2× (discrete fibre chain) or about 4.4× (integrated array) the energy "
            "per point quoted in this report.\n")

edits = [
    # intro: applications paragraph
    ("(Figure C0.10d). 10.7 lists what the model leaves out. Before all of this, 10.1 states the assumptions and defines the symbols.",
     "(Figure C0.10d). 10.7 turns that question around: it asks how much stronger than the weakest return the strongest "
     "returns get, and what that dynamic range does to each receiver. 10.8 lists what the model leaves out. Before all of "
     "this, 10.1 states the assumptions and defines the symbols.", 1),
    # intro: table of parts
    ("| 10.7 Limits of the model | What is left out? | — |",
     "| 10.7 Dynamic range | How strong can returns get, and what do they break? | — |\n"
     "| 10.8 Limits of the model | What is left out? | — |", 1),
    # intro: main results, new bullet after the aperture/energy bullet
    ("What FMCW keeps in fog is its rejection of the backscatter from droplets near the sensor.\n\n**Figures and data.**",
     "What FMCW keeps in fog is its rejection of the backscatter from droplets near the sensor.\n"
     "- **The same flat near field shrinks FMCW's dynamic-range burden** (10.7). Between a 10% target at 200 m and a "
     "retroreflective sign or white target at short range, the ToF design must span 56–82 dB of optical signal, twice "
     "that in its electronics. The best FMCW design must span about 45 dB, and field detection keeps that figure "
     "electrically. This is why ToF vendors publish fixes for retroreflector blooming, ghosts and range bias, and why "
     "China's lidar standard tests high-reflectivity ghosts.\n\n**Figures and data.**", 1),
    # 10.1 pointers to the limits part
    ("**Assumptions.** Every result below rests on the following conditions; 10.7 notes what changes when they fail.",
     "**Assumptions.** Every result below rests on the following conditions; 10.8 notes what changes when they fail.", 1),
    ("Real beams and misalignment lower the coherent signal below the computed value (10.7).",
     "Real beams and misalignment lower the coherent signal below the computed value (10.8).", 1),
    # 10.1 eta: sensitivity note
    ("The coherent receiver's mode and polarization factors are kept out of $\\eta$ and put into $A_{\\rm mode}$.\n",
     "The coherent receiver's mode and polarization factors are kept out of $\\eta$ and put into $A_{\\rm mode}$.\n" + ETA_NOTE, 1),
    # insert 10.7, rename the limits part
    ("#### 10.7 What the model leaves out\n", sec + "#### 10.8 What the model leaves out\n", 1),
]
for old, new, n in edits:
    c = s.count(old)
    assert c == n, (old[:80], c)
    s = s.replace(old, new)

NEW_SOURCES = (
    " ; https://www.nature.com/articles/s41586-026-10183-6 (Settembrini et al. 2026, coherent array, calibrated targets and retroreflector)"
    " ; https://arxiv.org/abs/2605.24753 (Gump et al., CVPR 2026, glare in SPAD lidar)"
    " ; https://arxiv.org/html/2512.05932v1 (Dudzik et al. 2025, blooming simulation)"
    " ; https://ouster.com/insights/blog/new-lidar-firmware-v112 (Ouster firmware 1.12, retroreflector range bias and blooming)"
    " ; https://ouster.com/insights/blog/improved-3-1-firmware (Ouster firmware 3.1)"
    " ; https://patents.google.com/patent/US20250189670A1/en (Ouster, pile-up and matched filters)"
    " ; https://www.imeko.org/publications/tc4-2014/IMEKO-TC4-2014-292.pdf (Kurtti et al. 2014, walk and receiver linearity)"
    " ; https://www.semanticscholar.org/paper/A-Wide-Dynamic-Range-CMOS-Laser-Radar-Receiver-With-Kurtti-Nissinen/cfae82db5979654436ddef2520d36a17fec57dc3 (Kurtti et al. 2017, walk compensation)"
    " ; https://www.ti.com/product/LMH32401 (TI LMH32401 amplifier)"
    " ; https://www.analog.com/media/en/technical-documentation/data-sheets/max40660-max40661.pdf (MAX40660 amplifier)"
    " ; https://www.jstage.jst.go.jp/article/jsaprev/2023/0/2023_230402/_pdf (Sony automotive SPAD)"
    " ; https://patents.google.com/patent/US7969558B2/en (Velodyne, one laser at a time)"
    " ; https://patents.google.com/patent/US11536845B2/en (Waymo, window ghosts)"
    " ; https://patents.google.com/patent/US12560716B2/en (SiPM blind zone after the window reflection)"
    " ; https://patents.google.com/patent/US12013497B2/en (Aeva, frequency-domain gain control)"
    " ; https://www.normsplash.com/Samples/ASTM/112464169/ASTM-D4956-19-en.pdf (ASTM D4956 sheeting)"
    " ; https://2019.tae-conference.cz/proceeding/TAE2019-047-Mariia-Khrapova.pdf (measured EN 12899-1 sheeting)"
    " ; https://cdn.standards.iteh.ai/samples/14380/8625afeb8e7a4801be0e685baeac6ac7/ISO-7591-1982.pdf (ISO 7591 licence plates)"
    " ; https://www.hesaitech.com/cn/news/1298 (GB/T 45500-2025 test items)"
    " ; https://user.guancha.cn/main/content?id=1435473 (GB/T 45500-2025, secondary summary)"
    " ; https://iss.rs/en/project/show/iso:proj:84347 (ISO/FDIS 13228)"
    " ; https://www.persival.de/post/quantifying-lidar-sensor-performance-through-din-sae-spec-91471-testing-methods (DIN SAE SPEC 91471)"
    " ; https://www.spiedigitallibrary.org/journals/optical-engineering/volume-62/issue-3/031211/Toward-open-benchmark-tests-for-automotive-lidars-year-1/10.1117/1.OE.62.3.031211.full (SPIE/SAE benchmark, year 1)"
    " ; https://www.spiedigitallibrary.org/journals/optical-engineering/volume-63/issue-8/085102/Toward-standardized-testing-of-automotive-lidars-year-two-results/10.1117/1.OE.63.8.085102.full (SPIE/SAE benchmark, year 2)"
    " ; https://tsapps.nist.gov/publication/get_pdf.cfm?pub_id=956735 (NIST 2024)"
    " ; https://www.robosense.ai/en/tech-show-55 (RoboSense M1)"
    " ; https://www.prnewswire.com/news-releases/hesai-showcases-next-gen-high-performance-lidars-at-iaa-mobility-2025-mass-production-expected-in-2026-302549128.html (Hesai ETX)"
    " ; https://www.aeva.com/press/aeva-to-showcase-high-performance-automotive-4d-lidar-at-iaa-mobility-2023/ (Aeva 2023)"
    " ; https://www.mobileye.com/blog/radar-lidar-next-generation-active-sensors/ (Mobileye)"
    " ; https://www.laserfocusworld.com/test-measurement/article/55253453/the-battle-of-lidar-sensor-technologies-fmcw-vs-tof (Voyant)"
    " ; https://doi.org/10.1109/PROC.1978.10837 (Harris 1978, window sidelobes)"
)
anchor = "(WMO: no agreed international definition of rain intensity)\n"
assert s.count(anchor) == 1
s = s.replace(anchor, anchor[:-1] + NEW_SOURCES + "\n")

# renumber equations in order of appearance; remap every Eq. reference
tags = [int(x) for x in re.findall(r"\\tag\{(\d+)\}", s)]
assert len(tags) == len(set(tags)), "duplicate tags"
mapping = {old: i for i, old in enumerate(tags, 1)}
print("tags", len(tags), "| map sample", {k: mapping[k] for k in (41, 46, 51, 907, 908, 909, 52, 184) if k in mapping})
s = re.sub(r"\\tag\{(\d+)\}", lambda m: r"\tag{" + str(mapping[int(m.group(1))]) + "}", s)
EQREF = re.compile(r"\bEqs?\.\s*\(\d+\)(?:\s*(?:,|and|–|-|to|or)\s*\(\d+\))*")
bad, nref = [], [0]


def remap(m):
    def one(mm):
        k = int(mm.group(1))
        if k not in mapping:
            bad.append(k)
            return mm.group(0)
        nref[0] += 1
        return f"({mapping[k]})"
    return re.sub(r"\((\d+)\)", one, m.group(0))


s = EQREF.sub(remap, s)
print("refs remapped", nref[0], "| dangling", sorted(set(bad)))
assert not bad
t2 = [int(x) for x in re.findall(r"\\tag\{(\d+)\}", s)]
assert t2 == list(range(1, len(t2) + 1))
odd = [i for i, l in enumerate(s.split("\n"), 1) if l.replace("\\$", "").count("$") % 2]
assert not odd, odd[:5]
pipes = [i for i, l in enumerate(s.split("\n"), 1)
         if l.startswith("|") and any("|" in sp for sp in re.findall(r"\$([^$]+)\$", l.replace("\\$", "")))]
assert not pipes, pipes[:5]
print("h4 in C0.10:", [l for l in s.split("\n") if l.startswith("#### 10.")])
print("bytes", len(s.encode("utf-8")), "(was", len(raw), ")")
if not DRY:
    REPORT.write_bytes(s.encode("utf-8"))
    OUT_SNAP.write_bytes(s.encode("utf-8"))
    print("written; snapshot", OUT_SNAP.name)
