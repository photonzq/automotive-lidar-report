"""§C5b: write the mean colour error as an angle-bracket mean instead of an overline.

In the built PDF the overline of \\overline{\\Delta E^*_{ab}} sat over the E alone, so the SMI line reads better with
\\langle\\Delta E^*_{ab}\\rangle. Both occurrences are in §C5b's colour-accuracy bullet.

Usage: c5b_mean_bracket_fix.py <report.md> <expected sha256 prefix> [--write]
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

OLD = r"\overline{\Delta E^*_{ab}}"
NEW = r"\langle\Delta E^*_{ab}\rangle"
assert text.count(OLD) == 2, f"found {text.count(OLD)} occurrences"
i = text.index("## C5b. Colour lidar")
j = text.index("## C6. How far can SPAD-SoC receivers scale?")
assert all(i < k < j for k in (text.find(OLD), text.rfind(OLD))), "outside §C5b"
new = text.replace(OLD, NEW)
print(f"sha256 before {sha[:12]}, after {hashlib.sha256(new.encode('utf-8')).hexdigest()[:12]}")
if "--write" in sys.argv[3:]:
    report.write_bytes(new.encode("utf-8"))
    print("written")
