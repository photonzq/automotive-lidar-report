from pathlib import Path
here = Path(__file__).resolve().parent
rp = Path(r"<report folder>\automotive_perception_report_2026-09-27.md")
raw = rp.read_bytes(); assert raw == (here / "report_after_audit_b.md").read_bytes(), "report changed since last write"
s = raw.decode("utf-8"); missing = []
def rep(old, new):
    global s
    if s.count(old) != 1: missing.append((s.count(old), old[:80])); return
    s = s.replace(old, new, 1)
rep(r"and Kodiak's 10 hauling sand on rural Permian Basin routes (§B4).",
    r"and Kodiak's 35 at end-Q2 2026 (10 in Mar 2026), mostly hauling frac sand on Permian Basin lease roads (§B4).")
rep(r"would need ≈60× the AT128's power × aperture × efficiency product (§C10.6)",
    r"would need ≈55× the AT128's power × aperture × efficiency product (§C10.6: $(300/210)^2\times41.04/1.536\approx55$)")
rep(r"The 1550 nm eye-safety allowance (§C4c) can pay for this optical energy. Items (b) and (c) give its electrical and thermal cost.",
    r"The ≈4× ratio splits into collection (7.7×), speckle fading (1.2×), photon energy (0.61×) and efficiency (0.74×). §C7b subsection 1 derives each factor. "
    r"It also explains why pulsing matters to ToF (sunlight in the timing bin) but not to coherent detection, and extends the same budget to linear-APD ToF and to full-cell FMCW coverage."
    "\n\n"
    r"The 1550 nm eye-safety allowance (§C4c) can pay for this optical energy. Items (b) and (c) give its electrical and thermal cost.")
print("missing", missing); assert not missing
assert "\t" not in s and "\r\n" not in s
rp.write_bytes(s.encode("utf-8")); (here / "report_after_followups.md").write_bytes(s.encode("utf-8")); print("ok", len(s))
