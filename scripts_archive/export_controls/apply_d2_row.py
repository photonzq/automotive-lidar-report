"""Section D2 timeline row for China's Dec 2023 technology catalogue: any-one-of thresholds, pulse-width caveat. Hash-guarded.

  python apply_d2_row.py --dry   # check the anchor and print the new row; nothing is written
  python apply_d2_row.py         # write the live report (aborts if it changed after being read)
"""
import hashlib
import sys
from pathlib import Path

REPORT = Path(r"<report folder>\automotive_perception_report_2026-09-27.md")
OLD = ("| 21 Dec 2023 | Technology export catalogue: **lidar system technology restricted** above extreme thresholds "
       "(e.g. >2 km range, <20 µrad resolution) | In force; automotive lidar falls below the thresholds |")
NEW = ("| 21 Dec 2023 | Technology export catalogue: **lidar system technology restricted** if any one of six thresholds "
       "is met (e.g. >2 km range, <20 µrad resolution, <1 ns pulses) | In force; automotive lidar falls below all "
       "thresholds except possibly pulse width (§D7) |")

raw = REPORT.read_bytes()
h0 = hashlib.sha256(raw).hexdigest()
text = raw.decode("utf-8")
assert "\r\n" not in text, "report has CRLF line endings"
lines = text.split("\n")
hits = [i for i, x in enumerate(lines) if x == OLD]
if len(hits) != 1:
    sys.exit(f"anchor found {len(hits)} times; nothing written")
assert OLD.count("|") == NEW.count("|"), "column count changed"
lines[hits[0]] = NEW
out = "\n".join(lines).encode("utf-8")
print(f"line {hits[0] + 1}: anchor found once; sha {h0[:12]}; size {len(raw)} -> {len(out)} bytes")
if "--dry" in sys.argv:
    print("dry run; nothing written\n" + NEW)
    sys.exit(0)
if hashlib.sha256(REPORT.read_bytes()).hexdigest() != h0:
    sys.exit("report changed after it was read; nothing written")
REPORT.write_bytes(out)
print("written; new sha", hashlib.sha256(out).hexdigest()[:12])
