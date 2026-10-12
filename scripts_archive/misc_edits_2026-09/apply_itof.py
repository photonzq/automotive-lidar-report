from pathlib import Path

here = Path(__file__).resolve().parent
rp = Path(r"<report folder>\automotive_perception_report_2026-09-27.md")
raw = rp.read_bytes()
assert raw == (here / "report_before_itof.md").read_bytes(), "report changed since snapshot"
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


# ---------- B8 consumer table rows ----------
rep("| **Smartphone / tablet dToF** (Apple \"LiDAR Scanner\", iPad Pro 2020 onward, iPhone Pro) | Sony 150 × 200 SPAD array (0.03 MP, "
    "10 µm pitch) hybrid-bonded to logic; Lumentum VCSEL; TI VCSEL driver | Annual Pro-model volumes, tens of millions [U] | Sony, "
    "Lumentum, TI [I, System Plus/Yole teardown] |",
    "| **Smartphone / tablet dToF** (Apple \"LiDAR Scanner\", iPad Pro 2020 onward, iPhone Pro) | 2020 iPad Pro: Sony 150 × 200 SPAD "
    "array (0.03 MP, 10 µm pitch) hybrid-bonded to logic; Lumentum VCSEL; TI VCSEL driver [I]. iPhone 15 Pro: all active dies from "
    "Sony; 116 × 92 SPADs at 10.1 µm (90 nm SPAD wafer on 28 nm logic); a VCSEL with 112 individually addressed cavities, bumped to "
    "its driver ASIC, projecting an 8 × 14 dot pattern; ≈\\$6.60 manufacturing cost (module-cost table below) [I, Bonanno 2024] | "
    "Annual Pro-model volumes, tens of millions [U] | Sony, Lumentum, TI (2020); all-Sony dies (iPhone 15 Pro) [I, System Plus/Yole "
    "teardowns] |")
rep("110 mW at 8 m (30 fps); sample price ¥1,000 | — | Sony (§C5a) |",
    "110 mW at 8 m (30 fps); sample price ¥1,000 for the **receiver chip only** (a module adds the VCSEL, its driver and the optics) "
    "| — | Sony (§C5a) |")

# ---------- B8 ToF block: ST row ----------
rep("| **STMicroelectronics** (FR/IT) | SPAD dToF, single-zone to multizone (FlightSense) | Phones (proximity, autofocus), PCs, robots "
    "| More than 2 billion shipped (table above) |",
    "| **STMicroelectronics** (FR/IT) | Both architectures. SPAD dToF from single zone to multizone (FlightSense; the complete 8 × 8-zone "
    "VL53L8CX sells for \\$3.60 in 1,000-unit trays [T]). Demodulating iToF: **VD55H1**, 672 × 804 (0.54 MP) back-illuminated pixels "
    "at 4.6 µm on ST's 40 nm stacked wafers, 200 MHz modulation with >85% demodulation contrast at 940 nm, ≈5 m at full resolution, "
    "up to 120 fps, <100 mW in some modes; sampling from Feb 2022 [T] | Phones (proximity, autofocus), PCs, robots; VD55H1 for AR/VR "
    "room mapping, face authentication and robotics [T] | More than 2 billion FlightSense devices shipped (table above) |")

# ---------- B8 ToF block: module cost, maturity bullet, robots bullet, meet block ----------
rep("\n**Signs of maturity:**\n", "\n" + rd("modcost_b8.md") + "\n\n**Signs of maturity:**\n")
rep("  - Apple's dToF LiDAR and structured-light Face ID remain the anchor customers.\n",
    "  - Apple's dToF LiDAR and structured-light Face ID remain the anchor customers.\n"
    "  - Yole's teardown team puts Apple's LiDAR module at more than ten times the cost of a multizone ranger, which \"helps explain "
    "the abandoning of 3D imaging by Android smartphones\" [I, Bonanno 2024].\n")
rep("   - Hybrid iToF and phone dToF are pushing up from below.\n",
    "   - Hybrid iToF and phone dToF push up from below, but only within about 10 m (module costs above; next block).\n")
rep("\n\nSources (ToF cameras): ", "\n\n" + rd("meet_b8.md") + "\n\nSources (ToF cameras): ")
old_tail = "http://image-sensors-world.blogspot.com/2021/05/opnous-raises-15m-investment.html\n"
extra_b8 = (" ; https://www.imagesensors.org/Past%20Workshops/2024%20ISSW/Papers/R06.1.pdf"
            " ; https://www.hackster.io/news/daylight-is-no-barrier-for-stmicro-s-new-flightsense-vl53l8cx-multi-zone-time-of-flight-sensor-8536d98c8010"
            " ; https://www.eenewseurope.com/en/time-of-flight-depth-image-sensor-has-0-5-megapixels/"
            " ; https://www.electronicsonline.net.au/content/sensors/microsite-product/stmicroelectronics-vd55h1-time-of-flight-sensor-721933645"
            " ; https://blog.arducam.com/time-of-flight-camera-raspberry-pi/"
            " ; https://openelab.io/blogs/news/orbbec-femto-bolt-applications-comprehensive-guide"
            " ; https://www.aliexpress.com/s/wiki-ssr/article/livox-mid-360-price-usd-2025"
            " ; https://aifitlab.com/products/hesai-jt16-lidar"
            " ; https://www.alibaba.com/product-detail/HESAI-JT128-Hyper-Hemispherical-360-X_1601618900874.html"
            " ; https://mowscout.com/guides/rtk-vs-lidar-vs-vision"
            " ; https://www.gminsights.com/industry-analysis/robotic-lawn-mower-market\n")
i = s.find("Sources (ToF cameras): ")
j = s.find(old_tail, i)
if i < 0 or j < 0 or s[i:j].count("\n") != 0:
    missing.append(("ToF sources tail", j))
else:
    s = s[:j] + old_tail.rstrip("\n") + extra_b8 + s[j + len(old_tail):]

# ---------- C0 subsection 9 ----------
rep("Sony DepthSense, Infineon/pmd REAL3, Melexis, ADI (§B8) |",
    "Sony DepthSense, Infineon/pmd REAL3, Melexis, ST VD55H1, ADI (§B8) |")
rep("About 10–200 MHz; MLX75023 up to 40 MHz [T]",
    "About 10–200 MHz: MLX75023 up to 40 MHz; ST VD55H1 200 MHz at >85% contrast [T]")
rep("In-pixel demodulators run at tens to about 200 MHz with contrast below one.",
    "In-pixel demodulators run at tens of MHz up to about 200 MHz, with contrast below one; ST's VD55H1 claims more than 85% at "
    "200 MHz [T].")
rep("Examples: Sony DepthSense, Infineon/pmd REAL3, Melexis, ADI, and Microsoft's Kinect v2 and Azure Kinect.",
    "Examples: Sony DepthSense, Infineon/pmd REAL3, Melexis, ST VD55H1, ADI, and Microsoft's Kinect v2 and Azure Kinect.")
rep("**What counts as lidar.** In physics", rd("arch_c0.md") + "\n\n**What counts as lidar.** In physics")
old_src = "Sources: https://www.ti.com/lit/ug/sbau219d/sbau219d.pdf ;"
rep(old_src,
    r"The companion report on precision ranging and 3D sensing (`..\precision_ranging_3d_sensing_report\`, Parts A and D) treats "
    "these instruments and the consumer market in more depth.\n\n"
    "Sources: https://www.ti.com/lit/ug/sbau219d/sbau219d.pdf ; https://thinklucid.com/tech-briefs/sony-depthsense-how-it-works/ ; "
    "https://www.eenewseurope.com/en/time-of-flight-depth-image-sensor-has-0-5-megapixels/ ; "
    "https://www.imagesensors.org/Past%20Workshops/2024%20ISSW/Papers/R06.1.pdf ;")

# ---------- C5a note ----------
rep("sold as ¥1,000 samples.", "sold as ¥1,000 samples (the sensor chip alone; a module adds the VCSEL, driver and optics, §B8).")

# ---------- Appendix 1 ----------
old_a1 = "- ToF cameras and sensors (§B8): supplier shares from a primary or independent source (only market-research figures exist).\n"
rep(old_a1, old_a1 +
    "- ToF and robotics-lidar prices (§B8): volume prices for ST's VD55H1 and Sony's IMX611; Hesai's and RoboSense's robotics-lidar "
    "prices by segment at OEM volume (mowers, humanoids, AMRs).\n")

assert "\t" not in s and "\r\n" not in s
if missing:
    print("NOT WRITTEN; missing/ambiguous:", missing)
    raise SystemExit(1)
rp.write_bytes(s.encode("utf-8"))
(here / "report_after_itof.md").write_bytes(s.encode("utf-8"))
print("report written; size", len(s.encode("utf-8")))
