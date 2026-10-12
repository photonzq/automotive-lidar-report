from pathlib import Path
here = Path(__file__).resolve().parent
rp = Path(r"<report folder>\automotive_perception_report_2026-09-27.md")
raw = rp.read_bytes()
assert raw == (here / "report_after_fill.md").read_bytes(), "report changed since last write"
s = raw.decode("utf-8")
a = s.index("## C7b. Can FMCW win?")
b = s.index("## C8. Chip-size and reticle limits across architectures")
assert s.count("## C7b. Can FMCW win?") == 1 and a < b
new = (here / "c7b_v3.md").read_text(encoding="utf-8").rstrip("\n") + "\n\n"
s = s[:a] + new + s[b:]
# executive summary: keep per-channel rate consistent with the section
old = "and delivers only ≈0.1–0.25 Mpts/s at 200 m."
assert s.count(old) == 1
s = s.replace(old, "and delivers only ≈0.05–0.25 Mpts/s at 200 m.")
assert "\t" not in s and "\r\n" not in s
rp.write_bytes(s.encode("utf-8"))
(here / "report_after_c7b3.md").write_bytes(s.encode("utf-8"))
print("ok", len(s))
