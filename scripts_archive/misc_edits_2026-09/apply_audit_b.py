import json
from pathlib import Path
here = Path(__file__).resolve().parent
aud = here.parent / "audit"
rp = Path(r"<report folder>\automotive_perception_report_2026-09-27.md")
raw = rp.read_bytes(); assert raw == (here / "report_after_audit_a.md").read_bytes(), "report changed since last write"
s = raw.decode("utf-8")
missing = []; n = 0
for a in [6, 7]:
    for k, e in enumerate(json.load(open(aud / f"agent{a}" / "edits.json", encoding="utf-8"))):
        if s.count(e["old"]) != 1:
            missing.append((a, k, s.count(e["old"]), e["note"])); continue
        s = s.replace(e["old"], e["new"], 1); n += 1
print("applied", n, "missing", missing)
assert not missing
assert "\t" not in s and "\r\n" not in s
rp.write_bytes(s.encode("utf-8")); (here / "report_after_audit_b.md").write_bytes(s.encode("utf-8"))
print("ok", len(s))
