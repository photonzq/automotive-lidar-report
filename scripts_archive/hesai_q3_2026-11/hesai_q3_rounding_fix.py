"""§B1 "Hesai's 2026 volume": write the two rounded differences with an approximate sign.

1,100 - 164.6 is 935.4 and 1,150 - 64.6 is 1,085.4, so the displayed 935 and 1,085 take an approximate sign.

Usage: hesai_q3_rounding_fix.py <report.md> <expected sha256 prefix> [--write]
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

OLD = r"$1{,}100-164.6=935$ to $1{,}150-64.6=1{,}085$ M for lidar."
NEW = r"$1{,}100-164.6\approx935$ to $1{,}150-64.6\approx1{,}085$ M for lidar."
assert text.count(OLD) == 1, f"found {text.count(OLD)} times"
new = text.replace(OLD, NEW, 1)
print(f"sha256 before {sha[:12]}, after {hashlib.sha256(new.encode('utf-8')).hexdigest()[:12]}")
if "--write" in sys.argv[3:]:
    report.write_bytes(new.encode("utf-8"))
    print("written")
