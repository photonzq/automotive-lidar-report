"""Insert C0 subsection 10.8 (benchmark), move the limits part to 10.9, add the Pointcloud no-blooming
measurement to 10.7, update the intro and 10.1 pointers, append sources, and renumber equations globally."""
import hashlib
import re
import sys
from pathlib import Path

REPORT = Path(r"<report folder>\automotive_perception_report_2026-09-27.md")
SCR = Path(r"<scratch>")
SNAP = SCR / "rewrite" / "report_after_peer_round2.md"
NEW = SCR / "mech" / "c0_10_8_benchmark.md"
OUT_SNAP = SCR / "rewrite" / "report_after_c0_10_8.md"
DRY = "--dry" in sys.argv

raw = REPORT.read_bytes()
assert hashlib.sha256(raw).digest() == hashlib.sha256(SNAP.read_bytes()).digest(), "report changed since the snapshot"
s = raw.decode("utf-8")
sec = NEW.read_text(encoding="utf-8").rstrip("\n") + "\n\n"
assert "\r" not in s + sec and "\t" not in sec

edits = [
    ("10.8 lists what the model leaves out.",
     "10.8 tests the model against published systems, and 10.9 lists what the model leaves out.", 1),
    ("| 10.8 Limits of the model | What is left out? | — |",
     "| 10.8 Benchmark | Does the model reproduce published systems? | — |\n"
     "| 10.9 Limits of the model | What is left out? | — |", 1),
    ("and why China's lidar standard tests high-reflectivity ghosts.\n\n**Figures and data.**",
     "and why China's lidar standard tests high-reflectivity ghosts.\n"
     "- **The model agrees with published systems** (10.8). Its coherent link equation reproduces Waymo's design "
     "point to 0.1 dB and Pointcloud's measured SNR to about 1 dB, and three measured systems show its flat near field. "
     "Its weakest input is efficiency: measured coherent chains reach 0.06–0.17, against the 0.25 used. For ToF no "
     "product publishes both laser energy and aperture; the published research sensors are consistent with the model "
     "given f/1-class lenses of 10–30 mm.\n\n**Figures and data.**", 1),
    ("10.8 notes what changes when they fail.", "10.9 notes what changes when they fail.", 1),
    ("computed value (10.8).", "computed value (10.9).", 1),
    ("although the retroreflector was 37.7 dB brighter [P].\n",
     "although the retroreflector was 37.7 dB brighter [P].\n"
     "  - In their reply to the reviewers, the same authors measured a 52 cm wide retroreflective sheet at about 10 m "
     "as 51–52.8 cm wide with three different lenses, i.e. without measurable widening [P, Peer Review File]. Both "
     "Pointcloud results are the developers' own.\n", 1),
    ("#### 10.8 What the model leaves out\n", sec + "#### 10.9 What the model leaves out\n", 1),
]
for old, new, n in edits:
    c = s.count(old)
    assert c == n, (old[:70], c)
    s = s.replace(old, new)

NEW_SOURCES = (
    " ; https://doi.org/10.1109/ISSCC42613.2021.9365961 (Kumagai et al., Sony, ISSCC 2021)"
    " ; https://toshiba.semicon-storage.com/content/dam/toshiba-ss-v3/master/en/company/technical-review/pdf/technical-review-9_e.pdf (Yoshioka et al., Toshiba, ISSCC 2018, with the comparison to Niclass et al. 2013)"
    " ; https://doi.org/10.3390/s18113642 (Hirose et al., Panasonic, Sensors 2018)"
    " ; https://doi.org/10.1007/s44275-025-00030-7 (Wang et al., SUSTech and RoboSense, Moore and More 2025)"
    " ; https://www.indie.inc/wp-content/uploads/2025/01/IND-0124-Microtech-Ventures-Whitepaper-LiDAR.pdf (indie Semiconductor and MicroTech Ventures whitepaper, 2023)"
    " ; https://www.analogphotonics.com/wp-content/uploads/2025/07/LiDAR-FS-4S-RevA.pdf (Analog Photonics FS-4S datasheet, as quoted in the Settembrini et al. Peer Review File)"
    " ; https://data.ouster.io/downloads/datasheets/datasheet-rev7-v2p5-os2.pdf (Ouster OS2 Rev7 datasheet)"
    " ; https://www.hesaitech.com/product/at128/ (Hesai AT128)"
)
anchor = "(Harris 1978, window sidelobes)\n"
assert s.count(anchor) == 1, s.count(anchor)
s = s.replace(anchor, anchor[:-1] + NEW_SOURCES + "\n")

tags = [int(x) for x in re.findall(r"\\tag\{(\d+)\}", s)]
assert len(tags) == len(set(tags)), "duplicate tags"
mapping = {old: i for i, old in enumerate(tags, 1)}
print("tags", len(tags), "| map", {k: mapping[k] for k in (54, 911, 55, 187) if k in mapping})
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
a = s.index("#### 10.8 Benchmark")
print("10.8 tags:", re.findall(r"\\tag\{(\d+)\}", s[a:s.index("#### 10.9 What the model")]))
print("h4:", [l for l in s.split("\n") if l.startswith("#### 10.")])
print("bytes", len(s.encode("utf-8")), "(was", len(raw), ")")
if not DRY:
    REPORT.write_bytes(s.encode("utf-8"))
    OUT_SNAP.write_bytes(s.encode("utf-8"))
    print("written; snapshot", OUT_SNAP.name)
