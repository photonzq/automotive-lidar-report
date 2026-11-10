"""Convert the new Hesai per-unit figures at the report's RMB 7.1 per dollar (§B1), as its table note states.

hesai_q3_revenue_edit.py converted at the Q3 release's RMB 6.7045; the §B1 table note fixes the report's rate at
RMB 7.1. RMB 1,340 is therefore about $190 (1,340 / 7.1 = 189), RMB 837 about $120 (118) and RMB 4,840 about $680
(682). The car-lidar bound also says that it covers main and blind-spot units together.

Usage: hesai_q3_dollar_fix.py <report.md> <expected sha256 prefix> [--write]
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
    (r"Q3 2026 lidar revenue per unit about RMB 1.34k (about \$200), under RMB 0.84k (about \$125) for car lidars [E] |",
     r"Q3 2026 lidar revenue per unit about RMB 1.34k (about \$190), under RMB 0.84k (about \$120) for car lidars [E] |"),
    (r"At the RMB 6.7045 per dollar that the Q3 release uses, RMB 1,340 is $1{,}340/6.7045\approx200$ dollars.",
     r"At the report's RMB 7.1 per dollar, RMB 1,340 is $1{,}340/7.1\approx189$ dollars, i.e. about \$190."),
    (r"Car lidars therefore earned less than",
     r"Car lidars, main and blind-spot units together, therefore earned less than"),
    (r"\approx\text{RMB }837$ (about \$125) each.",
     r"\approx\text{RMB }837$ (about \$120) each."),
    (r"\approx\text{RMB }4{,}840$ (about \$720) each [E].",
     r"\approx\text{RMB }4{,}840$ (about \$680) each [E]."),
]

new = text
for old, rep in PAIRS:
    n = new.count(old)
    assert n == 1, f"anchor found {n} times: {old[:80]!r}"
    new = new.replace(old, rep, 1)
print(f"{len(PAIRS)} replacements; sha256 before {sha[:12]}, after {hashlib.sha256(new.encode('utf-8')).hexdigest()[:12]}")
if "--write" in sys.argv[3:]:
    report.write_bytes(new.encode("utf-8"))
    print("written")
else:
    print("check only (add --write to apply)")
