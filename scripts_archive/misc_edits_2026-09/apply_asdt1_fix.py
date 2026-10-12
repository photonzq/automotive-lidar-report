from pathlib import Path

here = Path(__file__).resolve().parent
rp = Path(r"<report folder>\automotive_perception_report_2026-09-27.md")
raw = rp.read_bytes()
assert raw == (here / "report_after_phone2lidar.md").read_bytes(), "report changed since last write"
s = raw.decode("utf-8")
missing = []


def rep(old, new):
    global s
    n = s.count(old)
    if n != 1:
        missing.append((old[:90], n))
        return
    s = s.replace(old, new)


# --- C5a table rows ---
rep("| 576 points (24 × 24); horizontal field \"30° or more\"; 30 fps, or 15 fps in maximum-range mode [P/T] |",
    "| 576 points over 35.5° × 28.2° (±2°); 30 fps in the 20 m and 30 m modes, 15 fps in the 30 m and 40 m modes [P, spec sheet] |")
rep("| 40 m indoors and 20 m outdoors at 50% reflectivity. Accuracy at 10 m \"±5 cm\" on Sony's page (some press reports give ±5 mm); "
    "distance resolution ≈2–2.5 cm; outdoor operation to 100 klx [P/T] |",
    "| Modes to 20, 30 and 40 m from 0.3 m. Press: 40 m indoors and 20 m outdoors at 50% reflectivity, to 100 klx [T]; the spec "
    "sheet tabulates outdoor figures out to 40 m in its 40 m mode, ambient level unstated [P]. At 10 m: accuracy +10/−25 mm (20 m "
    "mode) to +45/−55 mm (40 m mode) indoors, up to +100/−120 mm outdoors; precision 5 mm indoors and 20–40 mm outdoors; output "
    "step 0.25 mm [P]. The \"±5 mm\" in some press is the indoor precision |")
rep("| 940 nm, 28% | 940 nm | 905 nm, 24% / 940 nm, 37% |",
    "| 940 nm, 28% | 940 ± 6 nm; \"8x24pix VCSEL laser diodes\" (192 emitters) [P] | 905 nm, 24% / 940 nm, 37% |")
rep("| ≈350 mW for the module [T] |", "| Max 2.5 W (spec sheet) [P]; ≈350 mW in one press report [T] |")
rep("| Consumer | Industrial: drones, AMRs, service robots | AEC-Q100 Grade 2, ASIL-B(D) |",
    "| Consumer | Industrial (drones, AMRs, service robots); Class 1 under IEC 60825-1:2014; operating 0–40 °C [P] | AEC-Q100 Grade 2, ASIL-B(D) |")
rep("| ¥1,000 sample | Not published; availability Spring 2026 [T] |",
    "| ¥1,000 sample | Not published (\"call for pricing\"); US availability announced Apr 2026 [P] |")

# --- where the points come from ---
rep("**Where the 576 points may come from.** 24 × 24 = 576 resembles the 576-dot pattern reported for Apple's 2020 LiDAR, a "
    "64-emitter VCSEL behind a 3 × 3 diffractive splitter [U]. Whether the AS-DT1 uses an IMX611-class sensor is not disclosed [U]. "
    "The estimates below assume an IMX611-class array, to show the mechanism [E].",
    "**Where the 576 points come from.** The spec sheet lists \"8x24pix VCSEL laser diodes\", i.e. 192 emitters, so each emitter "
    "probably feeds three dots through a diffractive splitter [E/U]. The sensor is described only as \"a SPAD sensor\"; whether it is "
    "IMX611-class is not disclosed [U]. The estimates below assume an IMX611-class array (23,800 SPADs, ≈2.4 mm²) to show the "
    "mechanism [E].")

# --- parallax ---
rep("3. **Parallax.** A dot's image shifts on the sensor by $\\Delta x=f\\,b/R$. With $f\\approx3.2$ mm (30° across 1.71 mm) and an "
    "assumed 10 mm baseline, the shift is 64 µm (≈6 SPADs) at 0.5 m, 16 µm at 2 m and 3 µm at 10 m. Each dot needs a strip about 6 "
    "SPADs long just to be caught at close range.",
    "3. **Parallax.** A dot's image shifts on the sensor by $\\Delta x=f\\,b/R$. With $f\\approx2.7$ mm (35.5° across 1.71 mm) and an "
    "assumed 10 mm baseline, the shift is ≈90 µm (≈9 SPADs) at the 0.3 m minimum range, 54 µm (≈5) at 0.5 m, 14 µm at 2 m and 3 µm "
    "at 10 m. Each dot needs a strip about 5–9 SPADs long just to be caught at close range.")

# --- memory ---
rep("4. **Histogram memory.** 40 m needs a 267 ns window, or ≈2,000 bins at 2 cm.",
    "4. **Histogram memory.** 40 m needs a 267 ns window: ≈2,000 bins if each bin were 2 cm. The true bin width is not published; "
    "the 0.25 mm output step is interpolated.")

# --- radar comparison ---
rep("- **Matched window.** Over ≈30° × 30°, the AS-DT1's 576 points (≈1.25° pitch, 24 lines) compare with a high-end radar's "
    "≈450–1,800 cells.",
    "- **Matched window.** Over its 35.5° × 28.2° field, the AS-DT1's 576 points (≈1.5° × 1.2° pitch, 24 lines) compare with "
    "≈500–2,000 cells for a high-end radar at 1° × 2° to 0.5° × 1° in the same window.")
rep("- **Range precision is similar,** a few centimetres for both.",
    "- **Range:** the AS-DT1's precision at 10 m is 5 mm indoors and 20–40 mm outdoors, with accuracy of a few centimetres; an "
    "imaging radar resolves a few centimetres to ≈15 cm in range.")
rep("- **watts of laser:** 6.5–13.5 W against ≈0.35 W for the whole AS-DT1;",
    "- **power:** 6.5–13.5 W against at most 2.5 W for the whole AS-DT1;")

# --- C3b range-weighted table and bullet ---
rep("| ≈11 m outdoors [E, from 20 m at 50%] | ≈1 × 10⁶ | ≈0.35 W (module) | ≈3 × 10⁶ |",
    "| ≈11 m outdoors [E, from 20 m at 50%] | ≈1 × 10⁶ | ≤2.5 W maximum (spec sheet); ≈0.35 W in one press report | ≈4 × 10⁵–3 × 10⁶ |")
rep("Per watt the gap is ≈16× (Mid-360) to ≈10³–10⁴× (AT128, ATX).",
    "Per watt the gap is ≈20–100× (Mid-360) to ≈10³–10⁵× (AT128, ATX), depending on the AS-DT1's actual draw.")

# --- E2 row and B8 ladder row ---
rep("| Sony AS-DT1 lidar (flash dot pattern over ≈30°; §C5a) | 24 × 24 | 576 |",
    "| Sony AS-DT1 lidar (dot pattern over 35.5° × 28.2°; §C5a) | 24 × 24 | 576 |")
rep("| Sony AS-DT1 | Complete lidar module (≤50 g, ≈0.35 W) |", "| Sony AS-DT1 | Complete lidar module (≈46 g, ≤2.5 W) |")

# --- C5a sources: add the spec sheet ---
rep("Sources: https://www.sony-semicon.com/en/news/2023/2023030601.html ; https://www.image-sensing-solutions.eu/AS-DT1_feature.html ;",
    "Sources: https://www.sony-semicon.com/en/news/2023/2023030601.html ; AS-DT1 spec sheet (Sony, via Aegis Electronic Group, "
    "PDF of Feb–Apr 2026): https://aegis-elec.com/mwdownloads/download/link/id/7568 ; "
    "https://www.image-sensing-solutions.eu/AS-DT1_feature.html ;")

# --- Appendix 1 ---
rep("- Sony AS-DT1 (§C5a): which SPAD sensor and dot projector it uses; its price; whether its 10 m accuracy is ±5 cm (Sony's page) "
    "or ±5 mm (press reports); and the IMX611's maximum histogram window.\n",
    "- Sony AS-DT1 (§C5a): which SPAD sensor it uses; its price and typical power (the spec sheet gives only a 2.5 W maximum); the "
    "ambient conditions behind the spec sheet's outdoor figures to 40 m; and the IMX611's maximum histogram window.\n")

assert "\t" not in s and "\r\n" not in s
if missing:
    print("NOT WRITTEN; missing/ambiguous:", missing)
    raise SystemExit(1)
rp.write_bytes(s.encode("utf-8"))
(here / "report_after_asdt1fix.md").write_bytes(s.encode("utf-8"))
print("report written; size", len(s.encode("utf-8")))
