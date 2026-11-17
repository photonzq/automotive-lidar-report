"""Make the series-production status of flash lidar agree across sections C3c, C3d and B7.1.

Section C3c called the Continental HFL110 the only flash lidar confirmed in a series car, while section B7.1 records
Chinese solid-state blind-spot lidars in series cars: Zeekr's own units on Fortsense's flash-lidar SPAD-SoC (17,568
installed in 2025, NE Times) and Hesai's FTX, whose first mass-production use Hesai names as the Li Auto L9 Livis
(2026). The C3c statement is limited to Western lidars and points to B7.1, and the C3d table adds the same pointer to
Yole's dated statement. The "here"-scoped statements of section C3a refer to that section's own table and stay.

Usage: flash_series_fix.py <report.md> <expected sha256 prefix> [--write]
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
    ("[P/I]. It is the only flash lidar confirmed in a series car |",
     "[P/I]. It is the only Western flash lidar confirmed in a series car. Chinese solid-state blind-spot lidars have "
     "followed, among them Zeekr's own units on Fortsense's flash-lidar SPAD-SoC (17,568 installed in 2025) and "
     "Hesai's FTX on the Li Auto L9 Livis (2026) [T/P] (§B7.1) |"),
    ("Yole called it in Dec 2023 the only commercialized fully solid-state automotive lidar [I] |",
     "Yole called it in Dec 2023 the only commercialized fully solid-state automotive lidar [I]; Chinese solid-state "
     "blind-spot lidars have reached series cars since (§B7.1, §C3c) |"),
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
