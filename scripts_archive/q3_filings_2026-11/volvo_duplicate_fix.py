"""Remove the Volvo truck plan that q3_filings_edit.py added to Aurora's §B4 row and §C7 bullet.

The §B4 table's Waabi / Volvo row already gives Volvo's ">300 driverless trucks" for 2027, with the caveat that
Aurora's letter does not split them between Aurora and Waabi; repeating the figure under Aurora would credit it to
Aurora alone.

Usage: volvo_duplicate_fix.py <report.md> <expected sha256 prefix> [--write]
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

PAIRS = [
    ("and a Charger Logistics memorandum for 500 (2027–28); Volvo plans more than 300 driverless trucks in 2027 [P];",
     "and a Charger Logistics memorandum for 500 (2027–28) [P];"),
    ("a Charger Logistics memorandum to own and operate 500 trucks (2027–28) and Volvo's plan for more than 300 "
     "driverless trucks in 2027 [P].",
     "a Charger Logistics memorandum to own and operate 500 trucks (2027–28) [P]."),
]
new = text
for old, rep in PAIRS:
    n = new.count(old)
    assert n == 1, f"anchor found {n} times: {old[:80]!r}"
    new = new.replace(old, rep, 1)
print(f"sha256 before {sha[:12]}, after {hashlib.sha256(new.encode('utf-8')).hexdigest()[:12]}")
if "--write" in sys.argv[3:]:
    report.write_bytes(new.encode("utf-8"))
    print("written")
