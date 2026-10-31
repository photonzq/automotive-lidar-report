"""Give the gas-conduction figures of the §A4 vacuum-packaging block for both leg conductances (6 and 10 nW/K),
as bolometer_vacuum.py prints them: gas at 1 atm is 150 to 250 times the legs, and gas adds 10% at 2 to 3 Pa.
Usage: packaging_fix.py <report.md> <expected sha256 prefix> [--write]
Each (old, new) pair must match exactly once and the starting hash must match; writes LF line endings."""
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
    ("=1.5\\ \\mu$W/K, about 150 times the legs, and the responsivity, which scales as $1/G$, would fall about a "
     "hundredfold.",
     "=1.5\\ \\mu$W/K, 150 to 250 times the legs, and the responsivity, which scales as $1/G$, would fall by the "
     "same factor."),
    ("that is 0.34 nW/K per pascal, so gas adds 10% to the leg conductance at about 3 Pa (0.03 mbar).",
     "that is 0.34 nW/K per pascal, so gas adds 10% to the leg conductance at 2 to 3 Pa (0.02 to 0.03 mbar)."),
]
for old, new in PAIRS:
    n = text.count(old)
    assert n == 1, f"found {n} times: {old[:80]!r}"
    text = text.replace(old, new)
new = text.encode("utf-8")
print("old sha", sha[:12], "new sha", hashlib.sha256(new).hexdigest()[:12], "bytes", len(raw), "->", len(new))
if "--write" in sys.argv:
    report.write_bytes(new)
    print("written")
