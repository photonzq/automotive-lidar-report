"""Build a work copy of the report: the elaborated phone-module range block (Part B, consumer electronics)
replaces the old one-line conclusion, and the Appendix 1 pair of camera_damage_2026-10 is applied. Nothing is written to the report.

Usage: python apply_phone_range.py <report.md> <new_block.md> <appendix1_pair.json> <work.md>
"""
import hashlib
import json
import sys
from pathlib import Path

report, block, pair, work = (Path(a) for a in sys.argv[1:5])
raw = report.read_bytes()
h = hashlib.sha256(raw).hexdigest()
assert h.startswith("ab87fee20ce6"), f"report changed: {h[:12]}"
text = raw.decode("utf-8")
assert "\r" not in text

old = ("  - **A \\$1–7 phone module cannot do a robotics lidar's 30–60 m in sunlight by swapping in a better chip.** "
       "The chip platform transfers (Sony's automotive SPADs grew from its phone SPAD, §C5a); the module economics do not.\n")
assert text.count(old) == 1, text.count(old)
new = block.read_text(encoding="utf-8")
assert "\r" not in new and new.endswith("\n")
text = text.replace(old, new)

for e in json.loads(pair.read_text(encoding="utf-8"))["edits"]:
    n = text.count(e["old"])
    assert n == 1, (e["id"], n)
    text = text.replace(e["old"], e["new"])
    print("applied", e["id"])

work.write_bytes(text.encode("utf-8"))
print("work copy", hashlib.sha256(text.encode("utf-8")).hexdigest()[:12], "lines", text.count("\n"))
