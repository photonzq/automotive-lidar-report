from pathlib import Path

here = Path(__file__).resolve().parent
rp = Path(r"<report folder>\automotive_perception_report_2026-09-27.md")
raw = rp.read_bytes()
assert raw == (here / "report_after_asdt1fix.md").read_bytes(), "report changed since last write"
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


# ===== new sections / blocks =====
rep("## C8. Chip-size and reticle limits across architectures\n", rd("c7b.md") + "\n\n## C8. Chip-size and reticle limits across architectures\n")
rep("  - **Torc/Daimler:** Aeva long-range + Innoviz short-range.\n",
    "  - **Torc/Daimler:** Aeva long-range + Innoviz short-range.\n\n" + rd("trucking_b4.md") + "\n")
old_ap_row = ("| **Analog Photonics** | OPA plus tunable lasers on SiPh | Mainly government R&D | No automotive programme (§C10.2b) |\n")
new_ap_row = ("| **Analog Photonics** | OPA plus tunable lasers on SiPh | ≈\\$45 M of US federal contracts and grants, mostly DARPA and ONR; "
              "SBIR only ≈\\$4.3 M [I] | No automotive programme; two unnamed Tier 1 JDAs (2018, 2020) [P]; defence FSOC and lasers "
              "(below; §C10.2b) |\n")
rep(old_ap_row, new_ap_row + "\n" + rd("coherent_c3a.md") + "\n")
rep("| **Pointcloud** | Coherent focal-plane array | Undisclosed | Research stage (*Nature* 2026) |",
    "| **Pointcloud** | Coherent focal-plane array | ≈\\$4.3 M disclosed (aggregators) [S]; no public grants found [I] | *Nature* 2026; "
    "claims a Tier 1 contract (2022); engineering samples 2025–26 [P] (below) |")

# ===== executive summary and scope =====
old_ex = "     - Series production in trucks or L3 by 2030 is plausible (≈50–60%). Matching ToF's point rate per watt by 2032 is not (≈5–10%).\n"
rep(old_ex, old_ex +
    "     - **Better beam steering would not change this (§C7b).** The binding cost is the channel tax: each simultaneous coherent "
    "sample needs its own receiver chain and tens of mW of CW light, and delivers only ≈0.1–0.25 Mpts/s at 200 m. Existing mirrors "
    "already steer faster than that. Parity needs three things together: a ≥150-channel coherent receiver chip at ≤10–20 mW per "
    "channel, ≥30% wall-plug CW light at 105 °C, and ≈0.15 µJ optical per point.\n"
    "     - **Driverless trucking, FMCW's only market, is real but tiny (§B4).** Aurora runs ≈20–25 driverless trucks (200 targeted "
    "by year-end) and Kodiak 35 in the Permian; Gatik and Bot Auto are small. FMCW truck demand is ≈1–5k units in 2027.\n")
old_sc = "  - FMCW and beam steering, including whether FMCW can match ToF on point rate, pixels, readout and power (§C7a);\n"
rep(old_sc, old_sc +
    "  - whether FMCW can win at all, what would have to change, and whether better beam steering would help, with the 2026 "
    "\"photonic ski-jump\" as a test case (§C7b);\n")

# ===== C7, F6 pointers =====
rep("at 35 W (§C10.2b).\n- **Pivots to industrial and security**",
    "at 35 W (§C10.2b). It is funded mainly by US defence contracts (≈\\$45 M of federal prime awards, §C3a).\n"
    "- **Pivots to industrial and security**")
rep("Channel count leaves the fixed-power trade $n_{\\rm mode}c=K$ (§C10.3a) unchanged.",
    "Channel count leaves the fixed-power trade $n_{\\rm mode}c=K$ (§C10.3a) unchanged. Better beam steering alone does not remove "
    "the per-channel cost (§C7b).")

# ===== C3a rows: Pioneer, Blickfeld =====
rep("mass production from Dec 2020 [P]. No automotive series programme or formal exit found [U] | None found [U] |",
    "mass production from Dec 2020 [P]. Sales ended in Dec 2021, and in Feb 2022 Pioneer announced its withdrawal from 3D-LiDAR, "
    "citing the long time needed to recover the investment as autonomous driving advanced slowly; the subsidiary was dissolved "
    "[T, Nikkei] | Closed, not sold [T] |")
rep("[Pioneer](https://global.pioneer/en/corp/news/press/index/2557/) |",
    "[Pioneer](https://global.pioneer/en/corp/news/press/index/2557/); "
    "[Nikkei](https://www.nikkei.com/article/DGXZQOUC091R60Z00C22A2000000/) |")
rep("Raised >\\$64 M of venture capital [T]; another report gives >€45 M in total, including €7.5 M in Dec 2023 [T]",
    "Raised >\\$64 M of venture capital [T]; another report gives >€45 M in total, including €7.5 M in Dec 2023 [T]. Senstar cites "
    "\"over €60 million in technology investments since inception\" [P]; the higher figures probably include a €15 M European "
    "Investment Bank facility (2022) [T]")

# ===== C4d: ATX mirror =====
rep("Hesai ATX: an oscillating one-axis mirror [P/T].",
    "Hesai ATX: a one-axis mirror whose scan direction alternates every frame (even frames sweep toward increasing azimuth, odd "
    "frames back), i.e. an oscillating sweep. The Feb 2026 manual calls it a \"1-D rotating mirror (hybrid solid-state)\", refers to "
    "more than one mirror surface and lists 10 Hz [P, manual A07].")

# ===== B8 edits =====
rep("Meta Quest 3 markets a \"depth sensor\"; teardown accounts disagree on whether it is ToF or a patterned IR projector read by the "
    "front IR cameras [T, conflicting]",
    "Meta Quest 3's \"depth sensor\" is a patterned IR projector read by the front IR tracking cameras, i.e. active triangulation, "
    "not ToF [T, Road to VR on iFixit's teardown]; the Quest 3S drops the projector for IR floodlights [T]")
rep("Robotics was \"close to half\" of H1 2026 product revenue (RMB 958 M) and the main source of product gross profit, per management "
    "(results call) [T]",
    "Robotics was \"close to half\" of H1 2026 product revenue (RMB 958 M) and the main source of product gross profit, per management "
    "(results call) [T]. Q4 2025 \"robotics and other\" revenue was RMB 347 M, 49.0% of product revenue [P]")
rep("Camsense: >50% of 2024 vacuum-lidar shipments (CIC, indicative) [T]. LDROBOT, Slamtec, 3irobotix and in-house designs are not "
    "quantified [U]",
    "Camsense: >50% of 2024 vacuum-lidar shipments (CIC, indicative) [T]. LDROBOT's HKEX filing claims 720k dToF lidar units, "
    "\"global No. 1\" (2024 or 2025; summaries differ) [T]. Slamtec, 3irobotix and in-house designs are not quantified [U]")

# ===== B4 Tesla =====
rep("About 476–546 vehicles are registered in Texas by one count;",
    "TexasAVTracker counted 546 registered in Texas (420 Model Y, 126 Cybercab) on 26 Sep 2026, an upper bound on active "
    "vehicles [T];")
rep("Community trackers count about 85–200 active unsupervised vehicles in late Aug 2026;",
    "Community trackers counted about 85–200 active unsupervised vehicles in late Aug 2026, and ≈300 across Texas and Florida in "
    "late Sep [U];")

# ===== B6 JV suppliers =====
rep("Roof lidar in launch coverage [T]; supplier not named (a Hesai ATX attribution is unverified [U])",
    "Roof lidar in launch coverage [T]; supplier not named. Hesai announced an ATX win for a new-energy model of \"a joint venture of "
    "Toyota based in China\", mass production in 2026 (15 Aug 2025) [P]; the model is not named, so the bZ7 link is likely but "
    "unconfirmed [U]")
rep("**192-line lidar standard** on all three trims; supplier not named [T]",
    "**192-line lidar standard** on all three trims; supplier not named [T]. RoboSense's 192-beam EMX was chosen by \"a China-based "
    "joint venture vehicle brand of the largest Europe OEM\" (Apr 2025) [P, seen via search], so RoboSense is likely [U]")
rep("| Roof lidar [T]; supplier not named |", "| Roof lidar [T]; supplier not named (Hesai lists SAIC-GM among its customers [S]) |")

# ===== Appendix 1 =====
A = [
    ("- Outcomes of LeddarTech, Blickfeld, TetraVue and Pioneer's 3D-LiDAR.\n",
     "- TetraVue's fate (no shutdown, sale or dissolution record found; the California entity record would settle it), and what "
     "LeddarTech's bankruptcy trustee did with its IP.\n"),
    ("- Common-equity recovery in Luminar's Chapter 11.\n", ""),
    ("- Reasons for the Insight, Scantinel and Blickfeld insolvencies; Blickfeld's total funding (>\\$64 M vs >€45 M); whether Oryx "
     "attempted a sale.\n",
     "- The stated reason for Insight LiDAR's Chapter 11 (first-day filings, D. Colo. 24-13141); whether Oryx tried to sell itself "
     "before closing (reported only in a search summary).\n"
     "- Pointcloud's Tier 1 customer and any Innosuisse funding; Analog Photonics' subawards, checked award by award.\n"),
    ("- Hesai's Thailand plant volume start (guided early 2027).\n",
     "- Hesai's Thailand plant capacity (operations \"expected to begin in early 2027\"; no capacity given).\n"),
    ("- Aeva's European OEM identity *(not yet researched)*.\n",
     "- Aeva's European OEM identity (unnamed in the releases and filings found).\n"),
    ("- Hesai's and RoboSense's robotics revenue.\n",
     "- Hesai's robotics revenue (not disclosed; single reporting segment), and RoboSense's FY2025 and H1 2026 robotics revenue "
     "(only Q4 2025 is disclosed, §B8).\n"),
    ("- Delivery robots outside China (§B4a, subsection 4): Serve's lidars per robot; Gatik's current lidar supplier;",
     "- Delivery robots outside China (§B4a, subsection 4): Serve's lidars per robot (press implies one Ouster REV7); Gatik's "
     "current lidar supplier;"),
    ("- The share of robot vacuums with lidar navigation, and LDROBOT, Slamtec and 3irobotix volumes.\n",
     "- The share of robot vacuums with lidar navigation (AVC retail data, by subscription); Slamtec and 3irobotix volumes; whether "
     "LDROBOT's 720k counts only dToF units.\n"),
    ("- The Quest 3 depth-sensing principle.\n", ""),
    ("- A credible industrial-lidar and safety-scanner market size (SICK, Hokuyo).\n",
     "- A credible industrial-lidar and safety-scanner market size. Market-research figures for safety laser scanners range from "
     "≈\\$0.32 B to ≈\\$0.57 B (2025) [MR]; SICK (FY2025 sales €1.85 B [T]) reports no product split.\n"),
    ("the lidar suppliers for VW's 192-line units, the Toyota bZ7, Nissan N7 and Buick Electra E7;",
     "confirmed suppliers for VW's 192-line units (RoboSense EMX likely), the Toyota bZ7 (a Hesai ATX JV win likely), Nissan N7 "
     "(RoboSense likely) and Buick Electra E7;"),
    ("- Nissan (1 roof lidar, vendor unknown; possibly MicroVision via Luminar, unconfirmed).\n",
     "- Nissan (one roof lidar confirmed for next-generation ProPILOT, with 11 cameras and 5 radars [P]; vendor unknown; possibly "
     "MicroVision via Luminar, unconfirmed).\n"),
    ("- Lucid–Nuro robotaxi and Gravity.\n",
     "- Lucid–Nuro–Uber robotaxi (Gravity): \"solid-state lidar sensors\" in the body and a roof \"Halo\" [P]; count and supplier "
     "not disclosed.\n"),
    ("- Aurora's current (2025–26) count.\n",
     "- Aurora's current (2025–26) lidar count per truck (not in releases or filings found).\n"
     "- Autonomous trucking (§B4): how many PACCAR-built Aurora trucks still carry an observer; Gatik's fleet size; the lidar suites "
     "of Kodiak, Waabi, Plus, Gatik and Bot Auto.\n"),
    ("- Mercedes S-Class robotaxi lidar *(not yet researched)*.\n",
     "- Mercedes S-Class robotaxi (Abu Dhabi, with Momenta and Lumo): \"LiDAR, radar and cameras\" [T/S]; count and supplier not "
     "disclosed. Hesai's Mercedes L3 win is a different programme.\n"),
    ("- *(Not yet researched)* Aeva and Aurora gen-2 wavelength and points/s, and their production scanners (only patent evidence "
     "exists, §C3); Valeo SCALA 3 **Long Range** variant and InnovizTwo detector types (SCALA 3 Platform is documented as SPAD); "
     "Waymo lidar wavelength.\n",
     "- Aeva and Aurora gen-2 points/s, power and production scanners (Aurora states \"around the 1550nm wavelength band\"; only "
     "patent evidence exists for the scanners, §C3); Valeo SCALA 3 variants and detector (Valeo's page gives no wavelength or "
     "detector; SCALA 3 Platform is documented as SPAD); the InnovizTwo detector (filings say only \"high sensitivity detector\", "
     "with 2D MEMS mirrors at ≈905 nm); Waymo's lidar wavelength (a Waymo patent describes a 1,550 nm fibre laser for a long-range "
     "steerable unit; nothing ties a wavelength to a shipping product).\n"
     "- FMCW (§C7b): channel count and per-channel receive power of the next coherent FPA or column chip; a published SOA "
     "wall-plug efficiency at 105 °C.\n"),
    ("Seyond Falcon's polygon/galvo split, facet count and rpm (its K1 manual says only \"dual-dimensional\"); Hesai ATX's frame rate "
     "and mirror details beyond \"oscillating\"; whether Livox HAP is a Risley design; RoboSense M1's receive path and beams per "
     "module;",
     "Seyond Falcon's facet count, polygon rpm and galvo frequency (patents and a teardown summary indicate a polygon on the "
     "horizontal axis and a galvo on the vertical; TechInsights gives 1,500 scan lines per second at 10 fps); the ATX mirror's facet "
     "count (its manual gives 10 Hz and a sweep direction that alternates each frame); RoboSense M1's SiPM vendor and beams per "
     "module (Livox describes HAP as a rotating-mirror design, not Risley prisms [P]);"),
    ("- Whether the Ga/Ge/Sb suspension is extended past 27 Nov 2026.\n",
     "- Whether the Ga/Ge/Sb suspension is extended past 27 Nov 2026 (the US says the wider truce runs to 10 Jan 2027; no MOFCOM "
     "notice on Announcement 72 was found).\n"),
    ("- The outcome of NHTSA EA26002.\n",
     "- The outcome of NHTSA EA26002 (open; Tesla's reply to the Jul 2026 information request is not public).\n"),
    ("- **Tesla:** active unsupervised fleet size is contested (tracker vs Tesla-friendly outlets).\n",
     "- **Tesla:** active unsupervised fleet size. Registrations (546 in Texas on 26 Sep 2026) are an upper bound; crowdsourced "
     "counts suggest ≈300 active across Texas and Florida [U].\n"),
    ("- **Yole** technology split (rotating mirror 66% / MEMS 32% / 9xx about 90%): taken from a search extract of a paywalled page "
     "*(not yet researched)*.\n",
     "- **Yole** technology split (rotating mirror 66% and MEMS 32% of 2024E passenger-car volumes; 905/940 nm ≈90%): from search "
     "extracts of the page for Yole's *LiDAR for Automotive 2024*; the 2025 edition may revise it.\n"),
]
for a, b in A:
    rep(a, b)

assert "\t" not in s and "\r\n" not in s
if missing:
    print("NOT WRITTEN; missing/ambiguous:")
    for m in missing:
        print("  ", m)
    raise SystemExit(1)
rp.write_bytes(s.encode("utf-8"))
(here / "report_after_fill.md").write_bytes(s.encode("utf-8"))
print("report written; size", len(s.encode("utf-8")))

# refs index
ip = Path(r"<report folder>\refs\INDEX.md")
t = ip.read_bytes().decode("utf-8")
name = "2026-03-12_Nature_Saha-et-al_Nanophotonic-waveguide-chip-to-world-beam-scanning.pdf"
if name not in t:
    t = t.replace("and two papers read in full", "and three papers read in full", 1)
    if not t.endswith("\n"):
        t += "\n"
    t += ("| 2026-03-12 | Paper | Saha et al - Nanophotonic waveguide chip-to-world beam scanning (Nature 651, 356) | MITRE, MIT, Sandia "
          "and others; doi:10.1038/s41586-025-10038-6; open access | " + name + " | s41586-025-10038-6.pdf | §C7b |\n")
    ip.write_bytes(t.encode("utf-8"))
print("index ok")
