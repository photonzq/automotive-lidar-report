"""Old->new pairs that work the two §B8 note bullets ("Verification of dToF, 3 Oct 2026" and
"Scope of the 80% estimate") into the robot-vacuum row, the terms list and the Camsense list, and keep
the Appendix 1 robot-vacuum item consistent with them (4 Oct 2026).

Facts were checked against the filings themselves (page numbers are printed page numbers):
  LDROBOT prospectus, 30 Apr 2026: p. 3 (>4,000,000 dToF lidars in 2025), p. 28 (dToF definition),
    p. 131 (units by product; revenue by application), pp. 134-136 (Series 06/26/50/27), p. 140.
  LDROBOT application proof (Dec 2025): >720,000 dToF lidars in 2024.
  LDROBOT interim results, 24 Aug 2026: p. 3 (>4 M dToF lidars in 2025).
  Camsense prospectus, 22 Sep 2026: p. 10 (revenue and shipments by product), p. 78 (market sizes),
    p. 80 (CIC prices), p. 81 (ranking), p. 85 (commissioned CIC report), p. 135 (about 80% of robot
    vacuums produced in 2025 carried lidar), p. 149 (tiers), pp. 150-151 (D, PMA, PMB, PXA, PMF series).
  IDC blog, 10 Mar 2026: 32.72 M cleaning robots, 24.12 M smart vacuums, 2.37 M window, 1.99 M lawn.

The pairs are written as a JSON list of {"id", "old", "new"} to be applied
in a separate pass; every "old" is copied from the live report and occurs exactly once. A dry-run copy
with the pairs applied is written for checking and for a test build.

Usage:
    python edits_b8_integration.py --report <report.md> --out-dir <dir>
"""
import argparse
import hashlib
import json
import re
from pathlib import Path

ap = argparse.ArgumentParser()
ap.add_argument("--report", required=True)
ap.add_argument("--out-dir", required=True)
ap.add_argument("--expect", default="fedff6f54b80")
args = ap.parse_args()

RP = Path(args.report)
OUT = Path(args.out_dir)
raw = RP.read_bytes()
h0 = hashlib.sha256(raw).hexdigest()
assert h0.startswith(args.expect), h0
text0 = raw.decode("utf-8")
L = text0.split("\n")

CAMSENSE = "https://www.hkexnews.hk/listedco/listconews/sehk/2026/0922/2026092200005.pdf"
LD_AP = "https://www1.hkexnews.hk/listedco/listconews/sehk/2026/0511/sehk25120104096.pdf"
LD_PROS = "https://www1.hkexnews.hk/listedco/listconews/sehk/2026/0430/2026043000099.pdf"
LD_INT = "https://www1.hkexnews.hk/listedco/listconews/sehk/2026/0824/2026082400450.pdf"

ROW = (
    "| **Robot vacuums** | Spinning laser distance sensors (LDS), triangulation or dToF, for mapping: "
    "triangulation units in every price tier, mostly entry-level and mid-range, and dToF units mostly in "
    "mid-range and high-end models [P, Camsense]; camera/visual-SLAM (VSLAM) and solid-state ToF in others | "
    "**32.72 M home cleaning robots shipped in 2025 (+20.1%), of which 24.12 M robot vacuums (+17.1%)**; "
    "the other 8.60 M are window cleaners (2.37 M), lawn mowers (1.99 M) and pool cleaners; Chinese brands "
    "(Roborock, Ecovacs, Dreame, Xiaomi, Narwal) lead [T, IDC]. Camsense's prospectus, whose market data come "
    "from a report it commissioned from CIC (China Insights Industry Consultancy), states that about 80% of "
    "robot vacuums produced worldwide in 2025 carried lidar, triangulation units included, and puts the global "
    "robot-vacuum lidar market at RMB 1.7 B within RMB 3.1 B for all vacuum spatial sensors [MR]. Against "
    "IDC's 24.12 M vacuums that is about 19 M lidar-equipped robot vacuums in 2025 "
    "[E: $0.80\\times24.12\\text{ M}=19.3\\text{ M}$, taking 2025 production equal to shipments]. "
    "Camsense: see below | "
    "Camsense: >50% of 2024 vacuum-lidar shipments (CIC, indicative) [T]; its 10.47 M lidar units of 2025 "
    "are ≈54% of the 19.3 M above [E: $10.47/19.3=0.54$]. LDROBOT shipped more than 720,000 dToF lidars in "
    "2024 and more than 4 M in 2025, within 10.29 M sensors of all kinds; its filings give units by product, "
    "not by robot type, and by revenue household robots took 97% of its 2025 sensor and module sales "
    "(RMB 589.6 M of 606.5 M) [P]. By 2025 revenue, Camsense leads vacuum spatial sensing with ≈20%, ahead of "
    "a Hong Kong-listed peer matching LDROBOT with ≈14% [MR; E for the peer's identity]. Slamtec (factory "
    "capacity 200,000 lidars a year [P]), 3irobotix and in-house designs are not quantified [U] | "
    "[IDC](https://www.idc.com/resource-center/blog/global-home-cleaning-robot-market-2025/); "
    f"[Camsense prospectus]({CAMSENSE}); [LDROBOT application proof]({LD_AP}); "
    f"[LDROBOT prospectus]({LD_PROS}); [LDROBOT interim results]({LD_INT}); "
    "[Gelonghui/NetEase](https://www.163.com/dy/article/L6S51LHJ05198ETO.html); "
    "[Tencent](https://news.qq.com/rain/a/20260914A0CG1P00) |"
)

TERMS = (
    "- **Robot-vacuum sensors.** A *laser distance sensor* (LDS) is the small spinning turret on a robot "
    "vacuum, which maps the room in a 2D plane. *Triangulation* LDS units view the laser spot with an offset "
    "detector and infer distance from the spot's position; Camsense's D series pairs a VCSEL with a CMOS image "
    "sensor for this. *dToF* LDS units time each laser pulse's round trip instead: LDROBOT's filings define "
    "dToF this way, and Camsense's P series pairs a VCSEL with a SPAD receiver [P]. Both kinds are "
    "motor-driven 360° scanners, so the housing does not show which principle is inside; LDROBOT's Series 26 "
    "and Camsense's PXA are dToF units built to replace a triangulation unit without changes to the robot [P]. "
    "*SLAM* (simultaneous localization and mapping) builds a map while tracking the robot in it; *VSLAM* does "
    "so from camera images."
)

SOURCES = (
    "- **Company sources.** HKEX is the Hong Kong Stock Exchange; a prospectus or filing there is the "
    "disclosure document a company publishes to list its shares, and an *application proof* is the draft "
    "prospectus filed with the listing application. CIC and IDC are market-research firms."
)

HEADER = (
    "**Camsense (欢创科技) HKEX prospectus** [P, prospectus of 22 Sep 2026, linked in the robot-vacuum row]. "
    "Camsense had more than half of 2024 vacuum-lidar shipments by CIC's indicative count (table above), so "
    "its prospectus shows much of the robot-vacuum sensor market:"
)

SHARES = (
    "- Triangulation fell from 98.3% of revenue in 2023 to 65.7% in 2025 (RMB 403.3 M) and 47.1% in Q1 2026, "
    "as dToF lidar rose to 27.9% and line lasers (obstacle sensors that project a laser line and triangulate "
    "it) to 23%. Camsense's dToF lidars are motor-driven 360° scanners in retractable, top-mounted and in-body "
    "versions, not solid-state units."
)

APPX = (
    "- **Robot vacuums.** Mostly answered by the Camsense and LDROBOT Hong Kong filings (§B8): about 80% of "
    "robot vacuums produced in 2025 carried lidar, triangulation units included [MR, CIC data in Camsense's "
    "prospectus], about 19 M units against IDC's 24.12 M vacuum shipments [E]; Camsense shipped 9.31 M "
    "triangulation and 1.16 M dToF units in 2025, and LDROBOT more than 4 M dToF units across all robot types "
    "[P]. Unknown: retail data (AVC, paid), Slamtec's and 3irobotix's lidar units, in-house lidar volumes at "
    "Roborock, Ecovacs and others, and how LDROBOT's units divide among robot types."
)

# (id, 1-based line number in the live file, expected start of that line, new text; None deletes the line)
EDITS = [
    ("b8-row-robot-vacuums", 1343, "| **Robot vacuums** | Spinning laser distance sensors", ROW),
    ("b8-terms-robot-vacuum-sensors", 1351, "- **Robot-vacuum sensors.** A *laser distance sensor*", TERMS),
    ("b8-delete-dtof-note", 1352, "- **Verification of dToF, 3 Oct 2026.**", None),
    ("b8-terms-company-sources", 1354, "- **Company sources.** HKEX is the Hong Kong Stock Exchange", SOURCES),
    ("b8-camsense-header", 1356, "**Camsense (欢创科技) HKEX prospectus** [P, prospectus of 22 Sep 2026;", HEADER),
    ("b8-delete-80pct-note", 1357, "- **Scope of the 80% estimate.**", None),
    ("b8-camsense-revenue-shares", 1360, "- Triangulation fell from 98.3% of revenue (2023) to 47.1%", SHARES),
    ("b8-delete-consistency-check", 1362, "- The two reports are mutually consistent [E:", None),
    ("appx1-robot-vacuums", 9424, "- **Robot vacuums.** Mostly answered by the Camsense and LDROBOT", APPX),
]

pairs = []
for eid, n, start, new in EDITS:
    hits = [i for i, x in enumerate(L) if x.startswith(start)]
    assert len(hits) == 1, (eid, hits)
    if hits[0] != n - 1:
        print(f"{eid}: line moved from {n} to {hits[0] + 1}")
    line = L[hits[0]]
    old = line if new is not None else line + "\n"
    assert text0.count(old) == 1, (eid, text0.count(old))
    pairs.append({"id": eid, "old": old, "new": new if new is not None else ""})

# no overlaps between the "old" spans
spans = sorted((text0.index(p["old"]), text0.index(p["old"]) + len(p["old"]), p["id"]) for p in pairs)
for (a0, a1, ia), (b0, b1, ib) in zip(spans, spans[1:]):
    assert a1 <= b0, ("overlap", ia, ib)

text = text0
for p in pairs:
    assert text.count(p["old"]) == 1, p["id"]
    text = text.replace(p["old"], p["new"], 1)

# hygiene
assert "\t" not in text
assert '\\"' not in "".join(p["new"] for p in pairs), "backslash-quote in new text"
old_lines, new_lines = set(text0.split("\n")), text.split("\n")
changed = [l for l in new_lines if l not in old_lines]
for l in changed:
    if len(re.findall(r"(?<!\\)\$", l)) % 2:
        print("ODD $ in:", l[:120])
for w in ["corrected", "updated", "revised", "added", "now confirmed", "verification"]:
    a, b = text0.lower().count(w.lower()), text.lower().count(w.lower())
    if a != b:
        print(f"WORD COUNT CHANGE {w!r}: {a} -> {b}")
for i, l in enumerate(new_lines[1:], 1):
    prev = new_lines[i - 1]
    if l.startswith("**") and (prev.startswith("- ") or re.match(r"\d+\. ", prev)):
        print("BOLD PARAGRAPH GLUED TO A LIST ITEM at line", i + 1, l[:60])


def pipes(line):
    return len(re.findall(r"(?<!\\)\|", line))


block, bad = [], 0
for i, l in enumerate(new_lines + [""]):
    if l.startswith("|"):
        block.append((i, l))
    elif block:
        n0 = pipes(block[0][1])
        for j, r in block:
            if pipes(r) != n0:
                bad += 1
                print(f"TABLE ROW MISMATCH at line {j + 1}: {pipes(r)} vs {n0}")
        block = []
print(f"pairs {len(pairs)}; changed lines {len(changed)}; table mismatches {bad}")

OUT.mkdir(parents=True, exist_ok=True)
js = json.dumps(pairs, ensure_ascii=False, indent=1)
(OUT / "b8_integration_edits.json").write_bytes(js.encode("utf-8"))
(OUT / "report_b8_dry.md").write_bytes(text.encode("utf-8"))
print("source sha", h0[:12], "| dry-run sha", hashlib.sha256(text.encode("utf-8")).hexdigest()[:12],
      "| json sha", hashlib.sha256(js.encode("utf-8")).hexdigest()[:12])
