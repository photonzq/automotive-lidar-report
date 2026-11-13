"""§E4.1: automatic camera washing on the market, and corrected labels of the Tesla manual pages in Appendix 2.

The countermeasures bullet of §E4.1 is split in two. The first keeps the windshield measures (Toyota's heater, Denso's
hood) and adds Tesla's service cleaning of the inside of the windshield at the camera. The second covers automatic
washing of cameras outside the wiped glass, each read on its source page: Tesla's front-facing camera sprayer, which may
run by itself at the start of a drive (Model 3 manual, Cleaning); the Polestar 5's automatic rear parking camera washer
(manual, Activating washers); Nissan's self-cleaning camera of 2013 (two Nissan Europe release titles; their bodies are
licensed downloads and were not read); AUMOVIO's camera and lidar nozzles with liquid and air (product page); and
Valeo's camera cleaning system with warm water and an optional air blower (SoilingNet, p. 2 and Fig. 2).

Appendix 2: the Tesla entry labelled the Cleaning page (GUID-65384C1F...) as camera alerts and the Troubleshooting
Alerts page (GUID-9A3F0F72...) as cleaning; the labels now match the pages' titles. Three sources are added and the
SoilingNet entry names its page and figure.

Usage: glare_washing_edit.py <report.md> <expected sha256 prefix> [--write]
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

TESLA = "https://www.tesla.com/ownersmanual/model3/en_us/"
EDITS = [
    ("- **Countermeasures address parts of the problem.** Toyota heats the windshield around the camera when it may be "
     "fogged, Tesla's manual describes a washer nozzle on the front bumper camera, Denso's camera hood blocks cabin "
     "light reflected by the inner windshield (US 10,272,849 B2), and soiling detectors such as Valeo's SoilingNet flag "
     "a dirty lens on surround-view cameras (arXiv:1905.01492) [P, I]. Nothing removes the veil of a dirty windshield "
     "in front of a low sun except cleaning it, which takes an average windshield's halved-contrast zone from 22° back "
     "to about 10°.",
     "- **Countermeasures address parts of the problem.** Toyota heats the windshield around the camera when it may be "
     "fogged, and Denso's camera hood blocks cabin light reflected by the inner windshield (US 10,272,849 B2) [P]. "
     "Tesla has the inside of the windshield in front of the camera cleaned at a service appointment when the car's "
     "maintenance summary asks for it [P]. Nothing removes the veil of a dirty windshield in front of a low sun except "
     "cleaning its outside, which takes an average windshield's halved-contrast zone from 22° back to about 10°; for "
     "the forward camera behind the windshield, that is the job of the ordinary wipers and washer.\n"
     "- **Automatic washing is marketed for cameras outside the wiped glass.** Tesla's front-facing bumper camera, "
     "where fitted, has a sprayer that may run by itself at the start of a drive to clear dust and dirt, and the "
     "Polestar 5 washes its rear parking camera automatically after the front wipers have run a number of times [P]. "
     "Nissan advertised a self-cleaning camera for winter driving as early as 2013 [P]. Suppliers sell the hardware: "
     "AUMOVIO (Continental's former automotive business, §A7.6) offers camera and lidar nozzles that wash the lens "
     "with pressurized liquid and blow droplets and dust off with air [P], and Valeo describes a surround-view camera "
     "cleaning system that clears ice with warm water, some versions adding an air blower (SoilingNet, p. 2 and "
     "Fig. 2) [P]. Such a system has to know when to wash: SoilingNet detects a soiled lens, and its false alarms "
     "matter because each needless wash draws on a washer tank that must be refilled (arXiv:1905.01492) [P]."),
    (f"- Tesla, Model 3 owner's manual (US): limitations and warnings, {TESLA}GUID-E5FF5E84-6AAC-43E6-B7ED-EC1E9AEB17B7"
     f".html; cleaning, {TESLA}GUID-9A3F0F72-71F4-433D-B68B-0A472A9359DF.html; camera alerts, "
     f"{TESLA}GUID-65384C1F-86F2-44E8-A8BC-8A12E7E00A40.html\n",
     f"- Tesla, Model 3 owner's manual (US): Self-Driving Limitations and Warnings, "
     f"{TESLA}GUID-E5FF5E84-6AAC-43E6-B7ED-EC1E9AEB17B7.html; Cleaning (camera sprayer that may run automatically, "
     f"inside of the windshield at the camera), {TESLA}GUID-65384C1F-86F2-44E8-A8BC-8A12E7E00A40.html; "
     f"Troubleshooting Alerts (camera alerts), {TESLA}GUID-9A3F0F72-71F4-433D-B68B-0A472A9359DF.html\n"),
    ("- Uřičář et al., SoilingNet: soiling detection on automotive surround-view cameras, arXiv:1905.01492 (ITSC 2019): "
     "https://arxiv.org/abs/1905.01492\n",
     "- Uřičář et al. (Valeo), SoilingNet: soiling detection on automotive surround-view cameras, arXiv:1905.01492 "
     "(ITSC 2019; Valeo's camera cleaning system, p. 2 and Fig. 2): https://arxiv.org/abs/1905.01492\n"
     "- Polestar, Polestar 5 (2026) owner's manual, Activating washers (automatic rear parking camera washer): "
     "https://www.polestar.com/au/manual/polestar-5/2026/article/d6cfcf50d422fa2ac0a8cc37796a4b5f-8823b5b9d90e8ebac0a8"
     "cc3775a73843-8664b2fa77a7e089c0a8296870d1a409/\n"
     "- Nissan Europe, Nissan's self-cleaning camera is the clear choice for winter driving (16 Dec 2013): "
     "https://europe.nissannews.com/en-GB/releases/nissan-s-self-cleaning-camera-is-the-clear-choice-for-winter-driving\n"
     "- AUMOVIO, Optical sensors and windshield cleaning systems (camera and lidar nozzles with liquid and air): "
     "https://www.aumovio.com/en/solutions/driver-assistance/optical-sensors-and-windshield-cleaning-systems.html\n"),
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
