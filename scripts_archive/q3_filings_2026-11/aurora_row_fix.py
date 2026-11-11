"""§B4 table, Aurora row, "Driverless today": the Q3 letter's status in place of the Q2 targets.

The Q3 shareholder letter (28 Oct 2026) says more than 20 driverless trucks are built and coming into the fleet, and
that the Aurora Driver passed 500,000 commercial driverless miles in September.

Usage: aurora_row_fix.py <report.md> <expected sha256 prefix> [--write]
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

OLD = ("| **Aurora** | 20–25 International LT trucks without an observer targeted by end-Q3 2026; ≈440k driverless miles "
       "by end-June; 12 routes [P].")
NEW = ("| **Aurora** | More than 20 driverless trucks built and entering the fleet (Q3 letter, 28 Oct); >500k driverless "
       "miles by September; 12 routes at mid-year [P].")
assert text.count(OLD) == 1, f"found {text.count(OLD)} times"
new = text.replace(OLD, NEW, 1)
print(f"sha256 before {sha[:12]}, after {hashlib.sha256(new.encode('utf-8')).hexdigest()[:12]}")
if "--write" in sys.argv[3:]:
    report.write_bytes(new.encode("utf-8"))
    print("written")
