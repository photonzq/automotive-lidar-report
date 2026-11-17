"""Proofreading of section C3d after reading it in place.

- TechInsights' lists are "major components" in descending order of estimated cost; the articles do not say that they
  are the ten costliest parts, so the wording follows the articles.
- The Huawei 96-line splits eight lasers into 96 beams, an exception to one laser per beam at 905 nm.
- In the Ouster OS1-64, processors and memory (35%) are also the largest single function, level with optics and
  housing together.
- Yole's statement that Continental's flash lidar is the only commercialized fully solid-state unit is dated (Dec 2023).
- Two summary lines say only what the teardowns show (fibre lasers in every 1,550 nm unit torn down; Luminar's and
  Continental's own receiver chips).

Usage: teardown_section_fix.py <report.md> <expected sha256 prefix> [--write]
"""
import hashlib
import sys
from pathlib import Path

report, expected = Path(sys.argv[1]), sys.argv[2]
raw = report.read_bytes()
sha = hashlib.sha256(raw).hexdigest()
assert sha.startswith(expected), f"report changed: sha {sha[:12]} != {expected}"
text = raw.decode("utf-8")
assert "\r" not in text

EDITS = [
    ("Seyond's Falcon and Luminar's Iris carry their light in optical fibre from a seeded, pumped fibre laser, and in "
     "the one",
     "Seyond's Falcon and Luminar's Iris carry their light in optical fibre from fibre lasers (in the Falcon, a seed, a "
     "pump and erbium-doped fibre), and in the one"),
    ("**The laser, optics, mirrors and housing cost more than the electronics** in six",
     "**The laser, optics, mirrors and housing cost more than the processors and memory** in six"),
    ("with board photographs, the chips found and the ten components with the highest estimated cost [I].",
     "with board photographs, the chips found and ten major components with TechInsights' estimated cost, in "
     "descending order [I]."),
    ("where 905 nm designs use one laser per beam (the M1's five, the AT128's 128 below) [I, CITIC].",
     "where 905 nm designs usually use one laser per beam (the M1's five, the AT128's 128 below) [I, CITIC]; the "
     "Huawei 96-line, which splits eight lasers into 96 beams (subsection 2), is the exception."),
    ("The rotating-mirror and prism units come first, then the MEMS, wedge-prism and oscillating-mirror designs, the "
     "spinning units and the one flash unit. All are pulsed time of flight.",
     "The table runs from the rotating-mirror and prism units, with Hesai's oscillating-mirror ATX beside its AT128, "
     "through the MEMS, wedge-prism and oscillating-mirror designs to the spinning units and the one flash unit. All "
     "are pulsed time of flight."),
    ("to 50 m [I, TechInsights]; the only commercialized fully solid-state automotive lidar [I, Yole] |",
     "to 50 m [I, TechInsights]; Yole called it in Dec 2023 the only commercialized fully solid-state automotive "
     "lidar [I] |"),
    ("list, for seven of the units above, the ten components with the highest estimated cost, or nine for the SCALA 2 "
     "[I].",
     "list, for seven of the units above, ten major components with TechInsights' estimated cost, in descending order "
     "(nine for the SCALA 2) [I]."),
    ("- Processors and memory lead only in the SCALA 2 (45%), whose Zynq UltraScale+ (\\$52.73) is the costliest chip "
     "in any of the seven lists; the ATX's FPGA costs \\$3.91.\n",
     "- Processors and memory are the largest single function only in the SCALA 2 (45%) and the OS1-64 (35%, as much "
     "as its optics and housing together). The SCALA 2's Zynq UltraScale+ (\\$52.73) is the costliest chip in any of "
     "the seven lists, and the ATX's FPGA costs \\$3.91.\n"),
    ("1. **Pulsed time of flight at 1,550 nm means a fibre laser,** because",
     "1. **Every 1,550 nm unit torn down uses a fibre laser,** because"),
    ("beside Hesai's 20 ASICs in the AT128, Luminar's receiver ASIC and Continental's own SPAD array (§D1a).",
     "beside Hesai's 20 ASICs in the AT128 and the receiver chips that Luminar and Continental designed themselves "
     "(§D1a)."),
]
new = text
for old, rep in EDITS:
    n = new.count(old)
    assert n == 1, f"anchor found {n} times: {old[:90]!r}"
    new = new.replace(old, rep, 1)
assert "\r" not in new
print(f"{len(EDITS)} edits; sha256 before {sha[:12]}, after {hashlib.sha256(new.encode('utf-8')).hexdigest()[:12]}")
if "--write" in sys.argv[3:]:
    report.write_bytes(new.encode("utf-8"))
    print("written")
