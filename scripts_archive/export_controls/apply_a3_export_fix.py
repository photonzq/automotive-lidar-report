"""Replace the thermal export-control bullet in section A3 item 6 (car exit Note 3.c, ECCN 6A993.a), hash-guarded.

  python apply_a3_export_fix.py --dry   # check the anchor and print the new line; nothing is written
  python apply_a3_export_fix.py         # write the live report (aborts if it changed after being read)
"""
import hashlib
import sys
from pathlib import Path

REPORT = Path(r"<report folder>\automotive_perception_report_2026-09-27.md")

OLD = ("- Uncooled microbolometers (the usual thermal sensor, an array of tiny resistors warmed by the absorbed infrared) "
       "running above 9 Hz frame rate are dual-use controlled, i.e. export-controlled because they also have military uses "
       "(export classification ECCN 6A003.b.4.b). Cameras built into civilian passenger vehicles are decontrolled under "
       "Note 3.b.4.c.")

NEW = ("- Thermal cameras built on uncooled microbolometers (the usual thermal sensor, an array of tiny resistors warmed by "
       "the absorbed infrared) are dual-use controlled, i.e. export-controlled because they also have military uses, when "
       "they run faster than 9 Hz (US export classification ECCN 6A003.b.4.b; the bare detector array is ECCN 6A002.a.3.f "
       "at any frame rate) [P]. Note 3.c to 6A003.b.4.b releases cameras specially designed for civilian passenger vehicles "
       "under 4,500 kg gross vehicle weight, placed solely to assist the driver, and built to stop working when removed "
       "from their vehicle. Such cameras are ECCN 6A993.a, controlled for anti-terrorism reasons only, at any frame rate. "
       "Teledyne FLIR classifies its Tura (640 × 512, up to 60 Hz) as 6A993.a with its authentication feature and "
       "6A003.b.4.b without it [P].")

raw = REPORT.read_bytes()
h0 = hashlib.sha256(raw).hexdigest()
text = raw.decode("utf-8")
assert "\r\n" not in text, "report has CRLF line endings"
lines = text.split("\n")
hits = [i for i, line in enumerate(lines) if line == OLD]
if len(hits) != 1:
    sys.exit(f"anchor found {len(hits)} times; nothing written")
for word in ("corrected", "updated", "revised", "added"):
    assert word not in NEW.lower(), f"versioning word in new text: {word}"
assert NEW.count("$") == 0, "new text should carry no math delimiters"

i = hits[0]
lines[i] = NEW
out = "\n".join(lines).encode("utf-8")
print(f"line {i + 1}: anchor found once; report sha {h0[:12]}; size {len(raw)} -> {len(out)} bytes")
if "--dry" in sys.argv:
    print("dry run; nothing written\n" + NEW)
    sys.exit(0)
if hashlib.sha256(REPORT.read_bytes()).hexdigest() != h0:
    sys.exit("report changed after it was read; nothing written")
REPORT.write_bytes(out)
print("written; new sha", hashlib.sha256(out).hexdigest()[:12])
