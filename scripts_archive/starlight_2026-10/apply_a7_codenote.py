"""Add a pointer to the code behind section A7's numbers, after the Figure A7.1 caption. Hash-guarded."""
import hashlib
import sys
from pathlib import Path

REPORT = Path(r"<report folder>\automotive_perception_report_2026-09-27.md")
EXPECT = sys.argv[1]
raw = REPORT.read_bytes()
h0 = hashlib.sha256(raw).hexdigest()
assert h0.startswith(EXPECT), f"report changed: {h0[:12]}"
text = raw.decode("utf-8")
old = ("- Where a data curve lies below its sensor's noise floor, one frame of one pixel cannot show the target; a "
       "detector must then add up many pixels or frames (Eq. (16)).\n")
new = old + ("\n*Code.* The numbers in §A7's tables and in Figure A7.1 are computed by `build/figures/"
             "night_photon_budget.py`, which also prints the calibration checks above and writes everything to "
             "`night_photon_budget_tables.txt`.\n")
assert text.count(old) == 1, text.count(old)
out = text.replace(old, new)
REPORT.write_bytes(out.encode("utf-8"))
print("written; sha", hashlib.sha256(out.encode("utf-8")).hexdigest()[:12])
