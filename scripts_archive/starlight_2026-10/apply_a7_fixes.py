"""Two corrections after checking the rendered PDF and the Fortsense releases. Hash-guarded.
Usage: python apply_a7_fixes.py <expected sha prefix>
"""
import hashlib
import sys
from pathlib import Path

REPORT = Path(r"<report folder>\automotive_perception_report_2026-09-27.md")
raw = REPORT.read_bytes()
h0 = hashlib.sha256(raw).hexdigest()
assert h0.startswith(sys.argv[1]), f"report changed: {h0[:12]}"
text = raw.decode("utf-8")
EDITS = [
    ("block of VCSEL emitters fires together with only the matching block of SPAD pixels. Its first-generation FL6031 "
     "addresses in one dimension and corrects pile-up on chip.",
     "block of VCSEL emitters fires together with only the matching block of SPAD pixels. O-Film markets a "
     "short-range lidar built on the first-generation FL6031 with \"true two-dimensional addressing\" against "
     "blooming [P, company]."),
    ("| Image intensifier | Reflected light, amplified | Yes | Cost, export controls, analog output | None |",
     "| Image intensifier | Reflected light, amplified | Yes | Export controls; an analog image that must be relayed to "
     "a camera | None |"),
]
out = text
for old, new in EDITS:
    assert out.count(old) == 1, (out.count(old), old[:60])
    out = out.replace(old, new)
REPORT.write_bytes(out.encode("utf-8"))
print("written; sha", hashlib.sha256(out.encode("utf-8")).hexdigest()[:12])
