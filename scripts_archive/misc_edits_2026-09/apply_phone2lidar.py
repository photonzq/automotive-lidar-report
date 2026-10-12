from pathlib import Path

here = Path(__file__).resolve().parent
rp = Path(r"<report folder>\automotive_perception_report_2026-09-27.md")
raw = rp.read_bytes()
assert raw == (here / "report_after_itof.md").read_bytes(), "report changed since last write"
s = raw.decode("utf-8")
missing = []


def rep(old, new):
    global s
    n = s.count(old)
    if n != 1:
        missing.append((old[:90], n))
        return
    s = s.replace(old, new)


def rd(name):
    return (here / name).read_text(encoding="utf-8").rstrip("\n")


# 1. C3b: range-weighted point rate block before the checklist, plus checklist item 10
rep("**A checklist for reading any lidar spec sheet** [E]:",
    rd("fom_c3b.md") + "\n\n**A checklist for reading any lidar spec sheet** [E]:")
old9 = "9. **Independent evidence:** teardowns, benchmark datasets or customer field data outrank spec sheets.\n"
rep(old9, old9 +
    "10. **Range-weighted point rate:** multiply points/s by the square of the range at 10%. Binning, ROI and dot modes trade one "
    "factor for the other and leave the product nearly unchanged (table above).\n")

# 2. C5a: new subsection before "Who uses them"
rep("### Who uses them\n", rd("phone2lidar_c5a.md") + "\n\n### Who uses them\n")

# 3. E2 radar-lines table: AS-DT1 row
rep("| Velodyne VLP-16 lidar (2014) | 1,800 × 16 | ≈29,000 |",
    "| Sony AS-DT1 lidar (flash dot pattern over ≈30°; §C5a) | 24 × 24 | 576 |\n"
    "| Velodyne VLP-16 lidar (2014) | 1,800 × 16 | ≈29,000 |")

# 4. B8 low-end ladder: AS-DT1 row after the IMX611 chip
old_imx = "| Sony IMX611 | Receiver chip only | SPAD dToF | 8 m specification point | ¥1,000 sample | [P] |\n"
rep(old_imx, old_imx +
    "| Sony AS-DT1 | Complete lidar module (≤50 g, ≈0.35 W) | SPAD dToF, 576 points, 940 nm | 40 m indoors / 20 m outdoors at 50% "
    "(§C5a) | Not published | [P/T] |\n")

# 5. Appendix 1
old_a1 = "prices by segment at OEM volume (mowers, humanoids, AMRs).\n"
rep(old_a1, old_a1 +
    "- Sony AS-DT1 (§C5a): which SPAD sensor and dot projector it uses; its price; whether its 10 m accuracy is ±5 cm (Sony's page) "
    "or ±5 mm (press reports); and the IMX611's maximum histogram window.\n")

assert "\t" not in s and "\r\n" not in s
if missing:
    print("NOT WRITTEN; missing/ambiguous:", missing)
    raise SystemExit(1)
rp.write_bytes(s.encode("utf-8"))
(here / "report_after_phone2lidar.md").write_bytes(s.encode("utf-8"))
print("report written; size", len(s.encode("utf-8")))
