"""Add a pointer to the SWIR side note at the start of the short-wave infrared block of §A7.5 in the report.
Usage: main_report_pointer.py <report.md> <expected sha256 prefix> [--write]
The anchor must occur exactly once and the starting hash must match; writes LF line endings."""
import hashlib
import sys
from pathlib import Path

report, expected = Path(sys.argv[1]), sys.argv[2]
raw = report.read_bytes()
sha = hashlib.sha256(raw).hexdigest()
assert sha.startswith(expected), f"report changed: sha {sha[:12]} != {expected}"
text = raw.decode("utf-8")
assert "\r" not in text

OLD = "**Short-wave infrared.**\n- **TriEye's sensor.**"
NEW = ("**Short-wave infrared.**\n"
       "- **Side note.** The separate side note *Short-Wave Infrared Image Sensors* surveys the sensor routes in depth "
       "and judges SWIR cameras unlikely to matter for cars at this stage: "
       "https://photonzq.github.io/automotive-lidar-report/swir_image_sensor_survey.html\n"
       "- **TriEye's sensor.**")
n = text.count(OLD)
assert n == 1, f"anchor found {n} times"
text = text.replace(OLD, NEW)
new = text.encode("utf-8")
print("old sha", sha[:12], "new sha", hashlib.sha256(new).hexdigest()[:12], "bytes", len(raw), "->", len(new))
if "--write" in sys.argv:
    report.write_bytes(new)
    print("written")
