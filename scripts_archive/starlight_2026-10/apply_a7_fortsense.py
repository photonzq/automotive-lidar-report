"""Insert section A7 ("starlight" cameras) and the Fortsense additions into the report.

Hash-guarded: refuses to write unless the report's SHA-256 starts with EXPECT. Every anchor must occur exactly
once. New equations carry placeholder tags 9013-9021; run renumber_equations.py --allow-reorder afterwards.
Usage: python apply_a7_fortsense.py [--dry]
"""
import hashlib
import sys
from pathlib import Path

REPORT = Path(r"<report folder>\automotive_perception_report_2026-09-27.md")
HERE = Path(__file__).resolve().parent
EXPECT = "7d73cf7910b5"
DRY = "--dry" in sys.argv

raw = REPORT.read_bytes()
h0 = hashlib.sha256(raw).hexdigest()
assert h0.startswith(EXPECT), f"report changed since reading: {h0[:12]}"
text = raw.decode("utf-8")
a7 = (HERE / "a7_section.md").read_text(encoding="utf-8").strip()

EDITS = []


def edit(old, new, label):
    EDITS.append((old, new, label))


# 1. reading guide
edit("- **Part A, Thermal night vision:** the factory history of thermal cameras, adoption numbers, why they stayed "
     "niche, what could change that, how thermal compares with lidar, and what better headlights can and cannot do.",
     "- **Part A, Thermal night vision:** the factory history of thermal cameras, adoption numbers, why they stayed "
     "niche, what could change that, how thermal compares with lidar, what better headlights can and cannot do, and "
     "whether low-light (\"starlight\"), active near-infrared or photon-counting cameras could do thermal's job.",
     "guide: Part A line")

# 2. executive summary, point 1
edit("Mercedes, whose system was near-infrared (a camera viewing the road under invisible infrared lamps), and Lexus "
     "dropped out.",
     "Mercedes, whose system was near-infrared (a camera viewing the road under invisible infrared lamps) until it "
     "added a thermal camera in 2013, and Lexus dropped out.",
     "summary: Mercedes")
edit("as of 2025 only Rivian offered fully compliant ADB there (§A6).\n2. **Lidar has captured far more",
     "as of 2025 only Rivian offered fully compliant ADB there (§A6).\n"
     "   - **\"Starlight\" cameras do not replace thermal (§A7).** Beyond the low beam's cutoff a dark-clothed "
     "pedestrian gives a 3 µm automotive CMOS pixel only about 0.1–1 photoelectron per 30 ms frame, so a camera "
     "that relies on the scene's light is limited by photons, not by its sensor. Photon-counting SPAD sensors remove "
     "read noise but add no photons. At equal pixel size they stretch an ideal detector's range by about a fifth to "
     "a third (to roughly 150–180 m) and a pixel-level image's by about an eighth (to roughly 50 m), short of "
     "stopping distance at highway speed [E]. A thermal pixel sees the same pedestrian with an SNR of about 20–100. "
     "Active near-infrared night vision (Toyota from 2002, Mercedes from 2005) worked but was dropped, and Canon "
     "targets 2031 for mass production of an automotive SPAD sensor [T].\n"
     "2. **Lidar has captured far more",
     "summary: new sub-bullet")

# 3. Part A introduction
edit("§A5 compares thermal with lidar, and §A6 asks how far better headlights can close the same night-visibility "
     "gap.",
     "§A5 compares thermal with lidar, §A6 asks how far better headlights can close the same night-visibility gap, "
     "and §A7 asks whether low-light (\"starlight\") cameras, active near-infrared imaging or photon-counting sensors "
     "could do thermal's job instead.",
     "Part A intro")

# 4. A1 table, Mercedes row
edit("| 2005/06 | Mercedes S-Class W221 Night View Assist | Active NIR | Pedestrian detection 2009; spotlight 2011; "
     "animal detection 2013; **not offered on W223 (2021→)** |",
     "| 2005/06 | Mercedes S-Class W221 Night View Assist | Active NIR; NIR plus FIR from 2013 | Pedestrian detection "
     "2009; spotlight 2011; more than half of S-Class buyers ordered it (Daimler, Dec 2010); on the W222 (2013) Night "
     "View Assist Plus added a thermal camera, which also detects animals; **not offered on W223 (2021→)** (§A7.5) |",
     "A1 Mercedes row")

# 5. the new section A7, after A6.5
edit("That slightly strengthens the case for active or thermal night sensing in the US market.\n\n---\n\n"
     "# Part B — Lidar markets",
     "That slightly strengthens the case for active or thermal night sensing in the US market.\n\n" + a7 +
     "\n\n---\n\n# Part B — Lidar markets",
     "insert A7")

# 6. B7.1, Zeekr blind-spot units
edit("Zeekr has not published the blind-spot units' detailed specifications (Appendix 1).",
     "Their receiver chip is Fortsense's FL6031 SPAD-SoC, one per unit (§C5). Fortsense says so and relays Zeekr's "
     "requirement of a 150° × 112° field of view and 15 m of range [P, company], and an Aug 2026 regulatory filing "
     "by its new investor, Shandong Xintong Electronics, confirms that Fortsense's vehicle-grade SPAD-SoC is in "
     "volume production on Zeekr and other brands [P]. Zeekr has not published the units' other specifications "
     "(Appendix 1).",
     "B7.1 Zeekr")

# 7. consumer-volume path, Chinese SPAD start-ups
edit("They do so alongside consumer and robotics dToF [U on their consumer volumes], which gives them a volume base.",
     "They do so alongside consumer and robotics dToF [U on their consumer volumes], which gives them a volume base. "
     "Fortsense, for example, began with under-display fingerprint and 3D face-recognition chips; its SPAD-SoCs, in "
     "production for Zeekr's blind-spot lidars, made 4% of its revenue in 2025 and 22% in H1 2026 [P, investor's "
     "filing] (§C5).",
     "B8 consumer path")

# 8. C0 subsection 10.7 pointer
edit("**How strong returns fail in ToF lidars, and how it is tested.** Range walk, blooming, ghosting and blinding in "
     "ToF receivers, and the standards, open benchmarks and vendor fixes that address them, are surveyed in §C4b.",
     "**How strong returns fail in ToF lidars, and how it is tested.** Range walk, blooming, ghosting and blinding in "
     "ToF receivers, and the standards, open benchmarks and vendor fixes that address them, are surveyed in §C4b. "
     "The fixes there include one built into the receiver architecture: two-dimensional addressing, in which only "
     "the pixels facing the emitter block that is firing are counting (Fortsense, a Chinese SPAD-SoC maker).",
     "C0 10.7 pointer")

# 9. C4b vendor fixes
edit("  - Hesai (ETX, 2025) claims 95% fewer false positives on highly reflective objects.\n\nSources: "
     "https://arxiv.org/abs/2605.24753",
     "  - Hesai (ETX, 2025) claims 95% fewer false positives on highly reflective objects.\n"
     "  - Fortsense, a merchant SPAD-SoC maker (§C5), attributes blooming from signs, number plates and retroreflective "
     "film to receiver saturation, pixel crosstalk and signal spreading. It claims a fix across the whole chain of "
     "emitter, optics, SPAD array, time-to-digital converter, histogram and signal processing (2026), and presented on "
     "the problem at AutoSens Europe 2026.\n"
     "    - Its second-generation chips (FL6032Q, FL8132Q) add fine-grained two-dimensional illumination addressing: a "
     "block of VCSEL emitters fires together with only the matching block of SPAD pixels. Its first-generation FL6031 "
     "addresses in one dimension and corrects pile-up on chip.\n"
     "    - Its patent filings add staggered firing of two-dimensional emitter groups, random per-block delays that "
     "spread crosstalk across histogram bins, large and small sub-pixels in which the small one resists saturation, "
     "and polysilicon deep-trench isolation between SPADs [P, CN121186745A, CN121385913A, CN117956308A, "
     "CN121001427A].\n"
     "    - It demonstrated a second-generation prototype on retroreflective boards at CIOE 2026 (the China "
     "International Optoelectronic Exposition), but has published no halo size, crosstalk fraction or dynamic "
     "range.\n"
     "- **Why addressing helps** [E]. With two-dimensional addressing, stray light from a bright return falls mostly "
     "on pixels that are not counting at that moment, and when their own block fires, the bright object is not lit. "
     "Only the stray light that stays inside the active block, or that reaches the object through the edge of the "
     "emitter's own beam, still counts toward the criterion under item 2 above. Velodyne's one-laser-at-a-time "
     "firing (item 2) is the scanning form of the same idea.\n\nSources: https://arxiv.org/abs/2605.24753",
     "C4b vendor fixes")
edit("302549128.html (Hesai ETX)\n\n### Other dimensions",
     "302549128.html (Hesai ETX) ; https://www.fortsense.com/News/show?status=1&id=141 (Fortsense, blooming, "
     "AutoSens Europe 2026) ; https://www.fortsense.com/News/show?status=1&id=140 (Fortsense, CIOE 2026 "
     "retroreflector tests) ; https://www.fortsense.com/News/show?status=1&id=134 (Fortsense second-generation "
     "chips) ; https://patents.google.com/patent/CN121385913A/en (Fortsense, block-paired emission)"
     "\n\n### Other dimensions",
     "C4b sources")

# 10. C5 table row, Fortsense
edit("| Adaps ADS6311 | 256×192, 297 ps bins, Cu–Cu hybrid-bonded, AEC-Q102 [P] | Foundry unnamed; one commentator "
     "says domestic SPAD startups mostly use **Tower** (Israel) [T] |",
     "| Adaps ADS6311 | 256×192, 297 ps bins, Cu–Cu hybrid-bonded, AEC-Q102 [P] | Foundry unnamed; one commentator "
     "says domestic SPAD startups mostly use **Tower** (Israel) [T] |\n"
     "| Fortsense FL6031 / FL6031Q (merchant chip) | 360 × 150 output pixels (more than 50k) from binned SPADs, about "
     "2 M points/s, on-chip time-to-digital converters and histogramming; AEC-Q100 claimed [P, company]. Built on "
     "**Tower Semiconductor's 65 nm stacked BSI platform with pixel-level hybrid bonding** (joint press release, Sep "
     "2023) [P] | The only Chinese lidar SPAD-SoC with a publicly named foundry. Tower makes this process in its "
     "300 mm fab at Uozu, Japan [P, Tower, Sep 2019], so the wafers are probably Japanese-made [E]; Fortsense says "
     "it uses both overseas and domestic fabs [P]. PDE not published. Receiver of the Zeekr 9X's four blind-spot "
     "lidars (§B7.1) |",
     "C5 table row")

# 11. C5 Fortsense paragraph, before the foundry check
FORTSENSE = (
    "**Fortsense: the merchant SPAD-SoC inside Zeekr's blind-spot lidars.** Fortsense (阜时科技, founded in Shenzhen "
    "in Nov 2017 and now registered in Linhai, Zhejiang) designs SPAD-SoCs for flash lidar. Its founder and "
    "chairman, 莫良华 (Michael Mo), controls 49.5% [P]. It began with under-display fingerprint and 3D "
    "face-recognition chips and has worked on SPADs since 2019 [P, company]. Unless marked otherwise, the facts "
    "below come from the Aug 2026 regulatory filing of its new investor, Shandong Xintong Electronics [P], or from "
    "Fortsense's own releases [P, company].\n"
    "- **Products** [P, company]. The FL6031 (2023) is described in the table above; in 2022 an earlier Fortsense "
    "receiver chip was qualified to AEC-Q102 Grade 1. The second generation (2026) comprises the FL6032Q for "
    "blind-spot lidar and the FL8132Q (576 × 576, claimed 300 m range) for a long-range lidar with Fortsense's "
    "solid-state beam steering. It adds two-dimensional addressing (§C4b), a \"telescope\" mode with 250 ps "
    "timing bins over 75 m, and binning that can differ by region within one frame. A third generation (FL5023Q "
    "for parking and blind spots) was first shown in Sep 2026. No Fortsense chip has been described in a "
    "peer-reviewed paper; the company's only lidar publication is a review of SPAD dToF chip design (Discover "
    "Nano, 2026) [I].\n"
    "- **Customers.** Each Zeekr 9X H9 carries four FL6031 chips, one in each of Zeekr's in-house blind-spot lidars "
    "(§B7.1), and the FL6031 is also on the Zeekr 8X. Fortsense claims \"hundreds of thousands\" of FL6031s "
    "delivered on these cars [P, company, unverified]. The Xintong filing confirms volume production on Zeekr and "
    "other brands [P]. Lidar makers that have shown FL6031-based units or signed agreements with Fortsense include "
    "Wanji, Tanway, LeiShen, Joyson's PIA and O-Film [P, company].\n"
    "- **Finances** [P, unaudited]. Revenue was ¥214.0 M in 2025 and ¥112.7 M in H1 2026, with net losses of "
    "¥139.7 M and ¥48.8 M.\n"
    "  - SPAD-SoC chips made 3.64% of revenue in 2025 and 21.84% in H1 2026, i.e. about ¥7.8 M and ¥24.6 M "
    "[E: $0.0364\\times214.0$ and $0.2184\\times112.7$]. The rest came from short-range 3D machine-vision chips and "
    "from automotive-electronics integration services.\n"
    "  - Xintong (listed in Shenzhen) is paying ¥160 M for 5.63% at the latest round's price, which values "
    "Fortsense at ¥2.84 bn after the investment [E: $160/0.0563\\approx2{,}840$ M].\n"
    "  - Funds linked to the carmakers Chery (1.1%) and BAIC (0.4%) are shareholders. Xintong can require the "
    "founders to buy its stake back, at cost plus 8% a year, if Fortsense has not applied to list by the end of "
    "2028.\n"
    "- **Scale check** [E]. NE Times counted 17,568 Zeekr blind-spot units in 2025 (§B7.1). If all of Fortsense's "
    "2025 SPAD-SoC revenue had come from those units, it would amount to about ¥440 per unit "
    "[E: $7.79\\times10^{6}/17{,}568\\approx443$]. The chip business was still small in 2025 and has grown since.\n"
    "- **Position.** Fortsense's foothold is flash blind-spot and parking lidar and robotics. Hesai and RoboSense now "
    "make their own SPAD-SoCs for main lidars (§C5a, item 6), and Adaps and the Hubble-backed VisionICs compete with "
    "Fortsense as merchant suppliers [T]."
)
edit("\n\n**Foundry check.** English and Chinese press releases",
     "\n\n" + FORTSENSE + "\n\n**Foundry check.** English and Chinese press releases",
     "C5 Fortsense paragraph")

# 12. C5 foundry check, the Tower claim
edit("- The claim that Chinese SPAD startups use Tower Semiconductor is **not verified**.",
     "- For merchant start-ups the claim that they use Tower Semiconductor is verified for one: Tower and Fortsense "
     "announced in Sep 2023 that Fortsense's FL6031 is built on Tower's 65 nm stacked BSI platform [P]. For Adaps "
     "and VisionICs it remains unverified.",
     "C5 Tower claim")

# 13. D chokepoint table
edit("Adaps, Fortsense, VisionICs | **In transition** (§C5)",
     "Adaps, Fortsense (wafers on Tower's 65 nm stacked process, made in Japan [P/E]; §C5), VisionICs | "
     "**In transition** (§C5)",
     "D table SPAD row")

# 14. Appendix 1 items
edit("- **Foundries:** none is publicly named for any Chinese SPAD-SoC.",
     "- **Foundries:** only one is publicly named for a Chinese SPAD-SoC: Tower's 65 nm stacked BSI process for "
     "Fortsense's merchant FL6031 [P] (§C5). None is named for the lidar makers' in-house chips.",
     "App1 foundries")
edit("- **Zeekr 9X blind-spot lidar (§B7.1).** The four near-field units are Zeekr's own design [T]. Unknown: their "
     "field of view, range, minimum range, point rate and chip suppliers; one trade article gives 150° × 112° and "
     "15 m, with Fushi SPAD receivers and Ruixi VCSEL emitters [U].",
     "- **Zeekr 9X blind-spot lidar (§B7.1).** The four near-field units are Zeekr's own design [T], each with one "
     "Fortsense FL6031 SPAD-SoC as receiver; Fortsense relays a 150° × 112° field of view and 15 m of range [P, "
     "company]. (\"Fushi\" in one trade article is Fortsense's Chinese name, 阜时.) Unknown: their minimum range, "
     "point rate and emitter supplier (the same article names Ruixi VCSELs [U]).",
     "App1 Zeekr")
APP1_A7 = (
    "**Night vision beyond thermal (§A7)**\n"
    "- **Automotive SPAD cameras.** Canon has not published the pixel pitch, power, temperature range, AEC-Q "
    "qualification or price of its 2.1-megapixel automotive SPAD sensor, and its 2031 production target comes from "
    "trade press. AUMOVIO has published nothing on the SPAD imaging it presented at AutoSens Europe 2026; the claim "
    "of an A-sample rests on a partner's social-media post, and the sensor supplier is unknown. These decide whether "
    "a SPAD camera can matter for the night pedestrian-AEB rules of 2029 and later (§A4).\n"
    "- **Chip temperature at night.** No published measurement gives the chip temperature of a windshield camera "
    "at night. It sets both CMOS dark current and SPAD dark counts, and with them the photon-counting gain of "
    "§A7.2.\n"
    "- **Gated and SWIR imaging.** BrightWay names no carmaker for its claimed serial production, no TriEye series "
    "programme is public, and whether coated windshields pass 1,375 nm light is not documented (§A7.5).\n"
    "- **Export classification.** No published classification places a SPAD image sensor under ECCN 6A002.a.3.g or "
    "outside it (§A7.6).\n"
    "- **Fortsense's receiver performance (§C4b, §C5).** Fortsense has published no PDE at 905 or 940 nm and no "
    "measured blooming halo, crosstalk fraction or dynamic range for its two-dimensional addressing, and its unit "
    "volumes are unaudited."
)
edit("\n\n**Regulation, standards and investigations**\n",
     "\n\n" + APP1_A7 + "\n\n**Regulation, standards and investigations**\n",
     "App1 new group")

out = text
for old, new, label in EDITS:
    n = out.count(old)
    assert n == 1, f"{label}: anchor found {n} times"
    out = out.replace(old, new)
    print(f"ok  {label}")
print(f"{len(text):,} -> {len(out):,} characters; tags 9013-9021 present:",
      all(f"\\tag{{{k}}}" in out for k in range(9013, 9022)))
if DRY:
    print("dry run: nothing written")
    sys.exit(0)
assert hashlib.sha256(REPORT.read_bytes()).hexdigest() == h0, "report changed during the run"
REPORT.write_bytes(out.encode("utf-8"))
print("written; new sha", hashlib.sha256(out.encode("utf-8")).hexdigest()[:12])
