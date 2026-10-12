import hashlib, sys, time
from pathlib import Path

here = Path(__file__).parent
rp = Path(r"<report folder>\automotive_perception_report_2026-09-27.md")

raw = rp.read_bytes()
h0 = hashlib.sha256(raw).hexdigest()
s = raw.decode("utf-8")
assert "\r\n" not in s
lines = s.split("\n")
missing = []

def line_idx(prefix):
    idx = [i for i, l in enumerate(lines) if l.startswith(prefix)]
    if len(idx) != 1:
        missing.append((prefix, len(idx)))
        return None
    return idx[0]

def replace_line(prefix, new_lines):
    i = line_idx(prefix)
    if i is not None:
        lines[i:i + 1] = new_lines

def sub_in_line(prefix, old, new):
    i = line_idx(prefix)
    if i is None:
        return
    if lines[i].count(old) != 1:
        missing.append((prefix + " :: " + old, lines[i].count(old)))
        return
    lines[i] = lines[i].replace(old, new)

# ---------- §C5 Fastree3D timeline ----------
replace_line("| Sep 2013 / 2014 | Fastree3D SA incorporated", [
    lines[line_idx("| Sep 2013 / 2014 | Fastree3D SA incorporated")] if True else "",
    r"| 2013–2020 | **Capital, from the Vaud commercial register:** CHF 100 k at founding (statutes 1 Jul 2013, seat Ecublens; board Charbon, Florin and André Borowski, whose 2011 SPAD-imager patents the company later held), rising to **CHF 429,444** by Aug 2020, mostly through six conversions of loans into shares totalling ≈CHF 3.3 M. Implied conversion prices: ≈CHF 27 per share (2016), ≈44 (2018), 48 (2019) and ≈29.8 (Aug 2020, a down-round) | [P, register; E arithmetic] |",
])
replace_line("| 2014–2017 | Venture Kick stage-3 winner", [
    r"| 2014–2017 | Venture Kick stage-3 winner (2014; CHF 130 k in total [S]); CTI project 18345 and an EPFL Enable grant; two Dutch STW/NWO projects, ToF-3D (13244) and L3SPAD (13916, a TU Delft grant with Charbon as PI, 2015–19, so Fastree3D was probably a user partner [U]); Top-15 Swiss startups (2016); European Photonics Venture Forum winner (2016, 2017) | [P, company page; NWO] |",
    r"""| 2018–2021 | **EU grants:** H2020 SME Instrument Phase 1 *F3D-Fastsight-PoC* (816417), €50 k (Jun–Oct 2018); ECSEL *SECREDAS* (783119, coordinated by NXP, May 2018 – Oct 2021), €183.6 k to the Dutch subsidiary Fastree3D BV. SECREDAS probably explains the reported "joint R&D with NXP" [E] | [P, CORDIS] |""",
])
i = line_idx("| 2020 | Joint R&D with **Bosch and NXP** reported")
if i is not None:
    lines[i + 1:i + 1] = [
        r"""| Apr 2022 | "Falcon" hardware kit (2 kpixel) for selected partners: 40 m at 10% reflectivity in 60 klux sunlight, 10 ms latency; roadmap to 3D-stacked SPADs (EPFL/TSMC prototypes). No shipped product with Fastree3D silicon was found | [P, EPIC deck] |""",
    ]
replace_line("| Total funding | Only about **\\$5.9 M**", [
    r"| Total funding | Only about **\$5.9 M** (A3 Angels, Basel Area Business & Innovation, Delft Enterprises and others) [T, Crunchbase/Dealroom], largely as convertible loans (≈CHF 3.3 M converted by 2020 [P, register]), plus ≈€0.23 M of EU grants and Swiss grants | [T/P] |",
])
replace_line("| **Late 2023** | **Acquired by Hesai**", [
    r"""| **15 Dec 2023** | **Hesai buys the company, not just its patents.** Hesai's FY2023 20-F: it acquired a Swiss company that designed "image sensors for spatial awareness for industrial and automotive applications", paying **RMB 54.45 M net of RMB 0.57 M cash acquired (\$7.67 M)**. It booked the acquired **patent rights at RMB 59.35 M (≈\$8.4 M), amortized over 8 years**, and assumed a CHF 299 k loan from 2020 (repaid by 2025). Its 2025 annual report lists **Fastree3D SA** (Switzerland, Sep 2013, capital CHF 429,444) as a 100% subsidiary for "Development of LiDAR" | [P, Hesai 20-F FY2023; 2025 annual report] |""",
    r"| Jan–Mar 2024 | Florin, Charbon and Arnaud Béglé leave the board; Hesai co-founder and Chief Scientist **Sun Kai** becomes sole director. New statutes add group cash-pooling and financing clauses, and the seat moves to the EPFL Innovation Park. Older EPFL SPAD-array and TDC patents appear to have been assigned to Fastree3D around the closing [S] | [P, Vaud register] |",
    r"| Oct 2024 → 2026 | Patents keep issuing in Fastree3D SA's name (e.g. US 12,130,387, Oct 2024: decision-tree pulse selection with a TDC; inventors Ximenes, Padmanabhan, Charbon); no reassignment to Hesai seen. The register shows the company active in Sep 2026 | [P, USPTO via Justia; register] |",
    r"""| 27 Feb 2025 | **Hesai discloses the deal** ("In late 2023, Hesai acquired Fastree3D", under a headline calling it an IP acquisition). It says Fastree3D's SPAD patents are built into its 4th-generation platform (production from 2025) and the FTX solid-state lidar (492k pts/s; the release pairs 180°×140° with 30 m @10%, the product page gives 30 m for 140°×105° and 20 m for 180°×140°). Hesai says it had researched SPADs since 2016. The release says nothing about staff | [P, Hesai PR] |""",
])
i = line_idx("**Why it matters** [E]:")
if i is not None:
    assert lines[i + 1].startswith("- **World-class European SPAD and TDC know-how**")
    assert lines[i + 2].startswith("- A Chinese lidar maker with the volume")
    assert lines[i + 3].startswith("- It mirrors the wider pattern in Parts B and D")
    lines[i:i + 4] = [
        r"**Was it a success?** It depends on the yardstick [E]:",
        r"- **Capital efficiency: the best European lidar exit relative to money raised.** About \$7.7 M of cash for a company that raised about \$5.9 M (≈1.3×). Blickfeld sold for €10.4 M after more than €60 M, Scantinel's assets went for \$0.4 M after a €10 M round, and Ibeo went for ≈€20 M out of insolvency (§C3a).",
        r"- **Per share, a soft landing rather than a win.** About CHF 6.7 M over 429,444 shares is ≈CHF 15–16 per share, below every 2016–20 conversion price (CHF 27–48). Unless liquidation preferences or earn-outs changed the split (not public), money invested from 2016 lost value while founders' shares at par and the earliest money gained [U on terms].",
        r"- **Technology: the strongest case.** Hesai valued the patents above the cash it paid and says they sit in its 4th-generation platform, and Hesai ships >1 M lidars a year. No public evidence yet shows Fastree3D circuits in a shipping chip, as distinct from its patents protecting Hesai's own designs [P/E].",
        r"- **Team: unknown.** The founders left the board, no other Hesai entity exists in Switzerland, and the press release is silent on staff. The company's own goal of a series SoC by 2022 was missed.",
        r"- **Reading.** World-class European SPAD and TDC know-how (the Canesta→Kinect lineage, EPFL AQUA, TU Delft) could not reach automotive scale on about \$6 M, but it did not die: a Chinese maker with volume bought it as a going concern at roughly the capital invested. The disclosed IP lineage supports treating Hesai's FTX and Picasso as **distinct designs**, though public information does not expose die or wafer provenance.",
        r"- It mirrors the wider pattern in Parts B and D, Western lidar IP consolidating into buyers with scale (Luminar, Scantinel and Ibeo into MicroVision), except that here the buyer was Chinese and the price covered the capital.",
    ]
i = line_idx("- Crunchbase: https://www.crunchbase.com/organization/fastree3d")
if i is not None:
    lines[i + 1:i + 1] = [
        r"- Hesai FY2023 20-F (acquisition, patent rights, assumed loan): https://www.sec.gov/Archives/edgar/data/1861737/000110465924051452/hsai-20231231x20f.htm",
        r"- Hesai 2025 annual report (subsidiary list; 6-K exhibit 99.1): https://www.sec.gov/Archives/edgar/data/1861737/000110465926048075/tm2612222d1_ex99-1.pdf",
        r"- Vaud commercial register, Fastree3D SA (CHE-291.330.490): https://prestations.vd.ch/pub/101266/extract?lang=FR&companyOfsUid=CHE-291.330.490",
        r"- CORDIS F3D-Fastsight-PoC: https://cordis.europa.eu/project/id/816417 ; SECREDAS: https://cordis.europa.eu/project/id/783119",
        r"- NWO/STW L3SPAD 13916: https://www.nwo.nl/en/projects/13916",
        r"- Fastree3D patents (USPTO data): https://patents.justia.com/assignee/fastree3d-s-a",
        r"- Florin, EPIC talk (Apr 2022): https://epic-photonics.com/wp-content/uploads/2021/12/Claude-Florin-Fastree3D.pdf",
    ]

# ---------- §C3a ----------
sub_in_line("| **Scantinel Photonics** | 2019, Ulm (ZEISS Ventures)",
            "Series A 2021 (Scania); €10 M extension 2022 [P] |",
            "Series A 2021 (Scania); €10 M extension 2022 [P]; ≈€2.4 M of public grants, including an ECSEL share of €0.34 M [P/T] (public-money block below) |")
sub_in_line("| **Pointcloud** | Coherent focal-plane array",
            "no public grants found [I]",
            "no public grants found; only an unfunded partner on UK EPSRC grants [P] (below)")
sub_in_line("*Pointcloud* (Pointcloud Inc., San Francisco",
            "Pointcloud Europe Ltd, UK, 2017)",
            "Pointcloud Europe Ltd, UK, 2017, dissolved Mar 2026)")
replace_line("- **Public money: none found.** There are no US federal awards", [
    r"- **Public money: none found going to the company.** There are no US federal awards (USAspending), no CORDIS project, and no listing in the Innosuisse Swiss Accelerator (2022–23) or start-up innovation project (2023–24) lists [I/P]. Its only public-funding records are as an unfunded project partner on three EPSRC grants held by Southampton [P]. The ARAMIS database and Innosuisse years before 2023 were not checked. Swiss firms could not be EIC beneficiaries in 2021–24 (next block).",
])
i = line_idx("### 2. Time-of-flight casualties and Tier-1 exits")
if i is not None:
    assert lines[i - 1] == "", repr(lines[i - 1])
    block = (here / "public_money_c3a.md").read_text(encoding="utf-8").rstrip("\n").split("\n")
    lines[i:i] = block + [""]
sub_in_line("| **Blickfeld** (Munich) | MEMS-mirror lidar; moved from automotive",
            "the higher figures probably include a €15 M European Investment Bank facility (2022) [T] |",
            "the higher figures probably include a €15 M European Investment Bank facility (2022) [P]. Public grants ≈€3.0 M, led by an EIC Accelerator-pilot grant of €1.84 M (2020–22) [P/T] (§C3a, subsection 1) |")

# ---------- Appendix 1 ----------
replace_line("- Pointcloud's Tier 1 customer and any Innosuisse funding", [
    r"- Pointcloud's Tier 1 customer and any pre-2023 Innosuisse funding (ARAMIS); Analog Photonics' subawards, checked award by award.",
    r"- Whether EIC Fund equity was actually invested in VoxelSensors and Hybrid Lidar; the funder of Scantinel's POVOS project; Fastree3D's exit terms per share (preferences, earn-outs) and whether its staff joined Hesai.",
])

if missing:
    print("MISSING/AMBIGUOUS:", missing)
    sys.exit(1)

out = "\n".join(lines)
assert ("\t" not in out) or ("\t" in s)
assert out.count("\\\"") == s.count("\\\"")
# concurrency guard: file must not have changed since read
now = rp.read_bytes()
if hashlib.sha256(now).hexdigest() != h0:
    print("ABORT: report changed during processing")
    sys.exit(2)
rp.write_bytes(out.encode("utf-8"))
(here / "report_after_funding.md").write_bytes(out.encode("utf-8"))
print("written", len(raw), "->", len(out.encode("utf-8")), "sha0", h0[:12])
