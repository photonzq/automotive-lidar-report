"""§C4 and Appendix 2: what teardowns and patents show of the erbium-fibre sources in 1,550 nm ToF lidars, with links to
photographs and figures.

Each item was read or viewed at its source:
- Yole SystemPlus, "What's in the box? Chinese automotive LiDARs at a glance" (19 Dec 2023): Seyond's Falcon couples a
  1550 nm seed fiber laser with a 940 nm pump laser and about 6 m of erbium-doped fiber; 28 W, 1.9 times RoboSense's
  M1 (15 W on the comparison slide); bill of materials 1.7 times; the teardown slide shows the closed unit, the opened
  unit with the fibre coiled in trays, and a labelled cutaway (prism, diffuser, mirror, optical fiber).
- TechInsights' summary of its Luminar Iris teardown: optical fibres carry the laser light; two fibre-laser tips emit at
  1550 nm; the version on the Volvo EX90.
- Luminar's US 9,812,838 B2 (abstract; Figs. 5-7 on sheet 4, Fig. 16 on sheet 9, Figs. 17-18 on sheet 10) and
  Innovusion's US 11,614,521 B2 (FIG. 4 on sheet 4), read from the USPTO copies.
- Wikimedia Commons photographs: two of the Luminar lidar on a Volvo EX90 roof (CC0) and one of a NIO ET7 at IAA
  Mobility 2023 (Matti Blume, CC BY-SA 4.0); licences and sizes from the Commons API.
- Seyond's Falcon K product page.

Usage: fibre_lidar_refs_edit.py <report.md> <expected sha256 prefix> [--write]
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

MOPA_END = ("the Seyond Robin E1X at 6 W [P] and the Hesai ATX at 8 W in its spec table or 10 W typical in its manual "
            "[P] (§C3b, §E9).\n")
C4_ADD = (
    "  - *What the teardowns and patents show.* Yole SystemPlus's teardown of Seyond's Falcon found a 1,550 nm seed "
    "fibre laser coupled with a 940 nm pump laser and about 6 m of erbium-doped fibre; its photographs show the fibre "
    "coiled in trays beside the scanner. The unit drew 28 W, 1.9 times the 15 W of the RoboSense M1 it was compared "
    "with, and its bill of materials came to about 1.7 times the M1's [I, Yole SystemPlus, Dec 2023]. TechInsights "
    "found that Luminar's Iris, in the version on the Volvo EX90, likewise carries its light in optical fibres, from "
    "two fibre-laser tips at 1,550 nm [I, TechInsights]. The companies' patents draw the same chain. Luminar's US "
    "9,812,838 B2 describes a seed laser at 1,400–2,050 nm followed by two amplifiers with a filter between them that "
    "removes amplified spontaneous emission; it shows one laser feeding several sensor heads through fibres (Figs. "
    "5–7), a double-pass fibre amplifier with its pump, gain fibre and reflector (Fig. 16), and the cross-sections of "
    "erbium and erbium–ytterbium fibre (Figs. 17–18). Innovusion's US 11,614,521 B2 shows a seed, a pre-amplifier and "
    "a booster, each amplifier stage fed by its own pump (FIG. 4) [P]. Appendix 2 lists photographs of both lidars, "
    "the teardown images and these patent figures.\n")

AUMOVIO = ("- AUMOVIO, Optical sensors and windshield cleaning systems (camera and lidar nozzles with liquid and air): "
           "https://www.aumovio.com/en/solutions/driver-assistance/optical-sensors-and-windshield-cleaning-systems.html\n")
YOLE_IMG = "https://medias.yolegroup.com/uploads/2023/12/img-automotive-teardown-tracks_lidar-innovusion-and-robosense_"
APPX2 = (
    "\n**1,550 nm fibre-laser lidars: teardowns, patents and photographs (§C4)**\n"
    "- Yole SystemPlus, What's in the box? Chinese automotive LiDARs at a glance (19 Dec 2023; Seyond's Falcon: seed "
    "fibre laser, 940 nm pump and about 6 m of erbium-doped fibre, 28 W): "
    "https://www.yolegroup.com/strategy-insights/whats-in-the-box-chinese-automotive-lidars-at-a-glance/\n"
    "- Yole SystemPlus, teardown image of Seyond's Falcon: the closed unit, the opened unit with its coiled fibre, and a "
    "labelled cutaway (3,482 × 2,250 px; © Yole SystemPlus 2023): " + YOLE_IMG + "2-1_ysp_november_2023.jpg\n"
    "- Yole SystemPlus, comparison of Seyond's Falcon and RoboSense's M1 (wavelength, power, field of view; © Yole "
    "SystemPlus 2023): " + YOLE_IMG + "1-3_ysp_november_2023.jpg\n"
    "- TechInsights, Deep Dive Teardown of the Luminar Technologies Iris LiDAR (summary: fibre-delivered light, two "
    "fibre-laser tips at 1,550 nm): https://www.techinsights.com/ja/node/53479\n"
    "- Luminar Technologies, US 9,812,838 B2, Pulsed laser for lidar system (2017; seed and two amplifiers, abstract; "
    "one laser feeding several sensor heads through fibres, Figs. 5–7, sheet 4; double-pass fibre amplifier, Fig. 16, "
    "sheet 9; Er and Er/Yb cross-sections, Figs. 17–18, sheet 10): https://patents.google.com/patent/US9812838B2\n"
    "- Innovusion, US 11,614,521 B2, LiDAR scanner with pivot prism and mirror (2023; seed, pumps, pre-amplifier and "
    "booster, FIG. 4, sheet 4): https://patents.google.com/patent/US11614521B2\n"
    "- Wikimedia Commons, the Luminar lidar on the roof of a Volvo EX90, two photographs (CC0, 4,080 × 3,072 px): "
    "https://commons.wikimedia.org/wiki/File:Volvo_EX90_LiDAR_by_Luminar.jpg ; "
    "https://commons.wikimedia.org/wiki/File:Volvo_EX90_LiDAR_developed_by_Luminar.jpg\n"
    "- Wikimedia Commons, NIO ET7 with its roof lidar pod, IAA Mobility 2023 (Matti Blume, CC BY-SA 4.0, 4,608 × "
    "3,072 px): https://commons.wikimedia.org/wiki/File:Nio_ET7%2C_IAA_Mobility_2023%2C_Munich_%28P1110356%29.jpg\n"
    "- Seyond, Falcon K product page (1,550 nm, Class 1; 500 m, 250 m at 10%; more than 250,000 Falcon K1 delivered): "
    "https://seyond.com/products/falcon-k/\n")

EDITS = [(MOPA_END, MOPA_END + C4_ADD), (AUMOVIO, AUMOVIO + APPX2)]
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
