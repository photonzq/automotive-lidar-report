import json
from pathlib import Path
here = Path(__file__).resolve().parent
aud = here.parent / "audit"
rp = Path(r"<report folder>\automotive_perception_report_2026-09-27.md")
raw = rp.read_bytes(); assert raw == (here / "report_after_c7b3.md").read_bytes(), "report changed since last write"
s = raw.decode("utf-8")
edits = {a: json.load(open(aud / f"agent{a}" / "edits.json", encoding="utf-8")) for a in [1, 2, 3, 4, 5, 8]}
# harmonize: Hesai 2026 plan (use the sourced 3.0-3.5 M of B1)
e = edits[2][12]
assert e["old"].count("(Hesai alone plans >4 M in 2026)") == 1, repr(e["old"])
e["new"] = e["old"].replace("(Hesai alone plans >4 M in 2026)", "(Hesai alone targets 3.0–3.5 M units in 2026, §B1)") + \
    r" [E: the 2028 upper end of ≈20k is $2\times10^{4}/(3.5\times10^{6})\approx0.6\%$ to $2\times10^{4}/(3.0\times10^{6})\approx0.7\%$ of that]"
# harmonize: truck stopping distance, use the F6 reconstruction (1.5 s, 3.5-2.0 m/s^2)
e = edits[8][32]
i = e["new"].index("- *Truck (165–255 m).*")
j = e["new"].index("\n", i)
e["new"] = e["new"][:i] + (r"- *Truck (165–255 m).* As reconstructed in §F6: at 105 km/h ($v=29.2$ m/s), a 1.5 s perception–reaction time "
    r"and an assumed average deceleration of 3.5 down to 2.0 m/s² for a loaded truck give "
    r"$29.2\times1.5+29.2^2/(2\times3.5)\approx165$ m and $29.2\times1.5+29.2^2/(2\times2.0)\approx257$ m.") + e["new"][j:]
missing = []; n = 0
for a, E in edits.items():
    for k, e in enumerate(E):
        if s.count(e["old"]) != 1:
            missing.append((a, k, s.count(e["old"]), e["note"])); continue
        s = s.replace(e["old"], e["new"], 1); n += 1
print("applied", n, "missing", missing)
assert not missing
# C7b probability table: same Hesai figure
old = "against >4 M ToF planned by Hesai alone in 2026 |"
assert s.count(old) == 1
s = s.replace(old, "against Hesai's own 2026 target of 3.0–3.5 M ToF units (§B1) |")
assert "\t" not in s and "\r\n" not in s
rp.write_bytes(s.encode("utf-8")); (here / "report_after_audit_a.md").write_bytes(s.encode("utf-8"))
print("ok", len(s))
