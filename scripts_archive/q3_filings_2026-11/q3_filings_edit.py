"""Fold the Q3 2026 SEC filings of Ouster, Aeva, MicroVision, Aurora, Kodiak, Tesla and Serve into the report.

Sources (SEC EDGAR, 21 Oct - 6 Nov 2026): Ouster 8-K Ex. 99.1 (3 Nov); Aeva 8-K Ex. 99.1 (4 Nov); MicroVision 8-K
Ex. 99.1 (28 Oct); Aurora Q3 shareholder letter (8-K, 28 Oct) and 424B5 amendment of its at-the-market sales
agreement (28 Oct); Kodiak 8-K Ex. 99.1 (5 Nov); Tesla Q3 update (8-K Ex. 99.1, 21 Oct); Serve 8-K Ex. 99.1 (5 Nov).
- Aurora: the Q3 letter expects to pass 200 driverless trucks by the end of February 2027 (it was "fully allocated"
  for year-end 2026 at the 23 Sep investor day); more than 20 driverless trucks built and entering the fleet; a
  Charger Logistics memorandum for 500 trucks (2027-28); Volvo plans more than 300 driverless trucks in 2027; Q3
  revenue $3 M, cost of revenue $8 M, operating loss $257 M, cash and short-term investments about $1.03 B.
  Updated in §0 (two places), §B2, §B4 (bullet, count, table, near-term test), §C3c, §C4, §C7 (two places), §C7a.
- Kodiak: 37 customer-owned driverless trucks at Atlas, DTL Transport 75 trucks, IKEA Supply, International LT,
  >58,000 paid driverless hours, nearly 30,000 loads, Q3 revenue $2.97 M (+286%), cash $113.6 M, Q3 operating cash
  use $35.2 M (§0, §B2, §B4).
- Tesla: nearly 2 M cumulative unsupervised robotaxi miles by 30 Sep, Cybercab in the Austin fleet, FSD (Supervised)
  in nine EU countries (§0, §B2, §E1 table, the fatality expectation recomputed: 2e6 x 1.2e-8 = 0.024, RAND 1.09
  gives 0.022).
- Ouster, Aeva, MicroVision: Q3 figures in §B3's table; Ouster's Q3 list in §B8; Aeva's Q3 in §C7; a new §C7 bullet
  on two FMCW makers moving into data-centre optics (Aeva's first optical-connectivity revenue; MicroVision's FMCW
  unit Scantinel).
- Serve: 2026 guidance raised to $12 M and its first city outside the US (§B8 table and sources).
- Appendix 2: the seven filings.
No display equations are added.

Usage: q3_filings_edit.py <report.md> <expected sha256 prefix> [--write]
Each anchor must match exactly once and the starting hash must match; the file keeps its LF line endings.
"""
import hashlib
import sys
from pathlib import Path

report, expected = Path(sys.argv[1]), sys.argv[2]
raw = report.read_bytes()
sha = hashlib.sha256(raw).hexdigest()
assert sha.startswith(expected), f"report changed: sha {sha[:12]} != {expected}"
text = raw.decode("utf-8")
assert "\r" not in text

OUSTER = "https://www.sec.gov/Archives/edgar/data/1816581/000162828026069487/exhibit991-9302026.htm"
AEVA = "https://www.sec.gov/Archives/edgar/data/1789029/000119312526447222/aeva-ex99_1.htm"
MVIS = "https://www.sec.gov/Archives/edgar/data/65770/000149315226048989/ex99-1.htm"
AURORA = "https://www.sec.gov/Archives/edgar/data/1828108/000182810826000092/aurora26q3shareholderlet.htm"
KODIAK = "https://www.sec.gov/Archives/edgar/data/1853138/000162828026071058/exhibit991_financialresults.htm"
TESLA = "https://www.sec.gov/Archives/edgar/data/1318605/000162828026066738/exhibit9914.htm"
SERVE = "https://www.sec.gov/Archives/edgar/data/1832483/000183248326000048/serv-20260930_ex991earning.htm"
CALL2 = ("https://www.investing.com/news/transcripts/"
         "earnings-call-transcript-hesai-posts-record-q3-2026-revenue-as-robotics-gains-traction-93CH-5015371")

PAIRS = [
    # §0, FMCW summary
    (r"""Aurora (about 20–25 driverless trucks, 200 that Aurora describes as "fully allocated" for year-end 2026) and Aeva with Daimler Truck (2027).""",
     r"""Aurora (about 20–25 driverless trucks, with 200 now expected by the end of February 2027) and Aeva with Daimler Truck (2027)."""),
    (r"""Aurora runs ≈20–25 driverless trucks (200 targeted by year-end) and Kodiak 35 in the Permian Basin oil fields;""",
     r"""Aurora runs ≈20–25 driverless trucks (200 now targeted for the end of February 2027) and Kodiak 37 in the Permian Basin oil fields;"""),
    (r"""Tesla's roughly 1 M unsupervised miles cannot support a comparable rare-outcome claim.""",
     r"""Tesla's nearly 2 M unsupervised miles (to 30 Sep 2026) cannot support a comparable rare-outcome claim."""),
    # §B3 supplier table
    (r"""| FY25 revenue \$169 M, more than 25k sensors; mostly industrial and infrastructure.""",
     r"""| FY25 revenue \$169 M, more than 25k sensors; Q3 2026 revenue \$59.3 M (+50%) on more than 27,000 sensors, about 27% of them lidars, with Q4 guidance of \$61–64 M; mostly industrial and infrastructure."""),
    (r"""| FY25 revenue \$18.1 M; H1 2026 \$12.4 M; cash \$177.9 M; Daimler C-samples; LG Innotek stake of about 6% [P] |""",
     r"""| FY25 revenue \$18.1 M; H1 2026 \$12.4 M; Q3 2026 \$6.7 M, including its first optical-connectivity revenue (chips for AI data centres); \$272.5 M of liquidity at end-Sep (\$147.5 M cash and securities plus a \$125 M facility); Daimler C-samples; US Air Force and Navy airborne-autonomy selection; LG Innotek stake of about 6% [P] |"""),
    (r"""| Q1 2026 revenue \$0.9 M; cash about \$46 M; industrial and defense focus [P] |""",
     r"""| Q3 2026 revenue \$2.4 M and 2026 guidance of \$10–15 M; cash \$28.9 M at end-Sep after \$13.6 M of Q3 operating cash use, with 2027 burn targeted near \$40 M; MOVIA Pro in production from Oct 2026; industrial and defense focus [P] |"""),
    # §B2 Tesla
    (r"""Tesla discloses no fleet number. Installed Cybercab capacity is >125,000 a year [T, WSJ].""",
     r"""Tesla discloses no fleet number. Installed Cybercab capacity is >125,000 a year [T, WSJ]. Its Q3 2026 update (21 Oct) says that Cybercab deployment into the Austin robotaxi fleet has begun, that the service reached nearly 2 M cumulative unsupervised miles by 30 Sep, and that FSD (Supervised) is approved in nine EU countries, where more than 100,000 customers use it [P]."""),
    # §B2 Aurora and Kodiak bullets
    (r"""200 trucks "fully allocated" for year-end [P]. **Caveat:**""",
     r"""200 trucks "fully allocated" for year-end at the 23 Sep investor day [P]. Its Q3 letter (28 Oct) moved the 200-truck milestone to the end of February 2027, with more than 20 driverless trucks built and entering the fleet [P]. **Caveat:**"""),
    (r"""plus 10 driverless trucks hauling sand on rural Permian Basin routes for Atlas Energy Solutions [T, NYT].""",
     r"""plus 10 driverless trucks hauling sand on rural Permian Basin routes for Atlas Energy Solutions [T, NYT]. By the end of Q3, Atlas's customer-owned driverless fleet had 37 trucks. Kodiak had also signed a binding agreement to put its driving system in 75 trucks owned by DTL Transport, named IKEA Supply as its first long-haul launch partner and added International LT as its third truck platform, with unsupervised operation from H2 2027 [P]."""),
    # §B4 count, table, near-term test
    (r"""[E: Aurora's ≈20–25 plus Kodiak's 35, many of which run on private lease roads, give at most $25+35=60$, and Bot Auto adds a handful]""",
     r"""[E: Aurora's ≈20–25 plus Kodiak's 37, many of which run on private lease roads, give at most $25+37=62$, and Bot Auto adds a handful]"""),
    (r"""| Q2 2026 revenue \$2 M against \$7 M cost of revenue; FY2026 guidance \$14–16 M; ≈\$1.2 B cash [P] | 200 trucks "fully allocated" for year-end; Q4 builds capped near 250 [P/E]; Hirschbach 500 trucks (2027–28) [P]; breakeven at ≈500 trucks [T] |""",
     r"""| Q3 2026 revenue \$3 M against \$8 M cost of revenue, and \$6 M in Jan–Sep against the \$14–16 M guided for 2026 in Q2; ≈\$1.03 B of cash and short-term investments; at-the-market share-sale agreement amended on 28 Oct [P] | 200 trucks by the end of Feb 2027, the date in the Q3 letter ("fully allocated" for year-end in Sep); Q4 builds capped near 250 [P/E]; Hirschbach 500 trucks (2027–28) and a Charger Logistics memorandum for 500 (2027–28); Volvo plans more than 300 driverless trucks in 2027 [P]; breakeven at ≈500 trucks [T] |"""),
    (r"""| **35 customer-owned driverless trucks** at end-Q2 2026; >40,000 paid driverless hours; >20,000 loads. Mainly frac-sand haulage for Atlas Energy, largely on private lease roads [P/U] | Q2 revenue \$3.5 M (+91% on Q1), 56% from Atlas; \$151 M cash against \$34 M quarterly operating burn [P] | Driverless long-haul highway operation "by year-end" [P] |""",
     r"""| **37 customer-owned driverless trucks** at Atlas at end-Q3 2026; >58,000 paid driverless hours; nearly 30,000 loads. Mainly frac-sand haulage for Atlas Energy, largely on private lease roads [P/U] | Q3 revenue \$3.0 M (+286% year on year, including a one-time defence contribution); \$113.6 M cash against \$35.2 M of Q3 operating cash use [P] | Unsupervised long-haul launch targeted for year-end, with IKEA Supply as first partner; 75 trucks for DTL Transport; International LT as third platform from H2 2027 [P] |"""),
    (r"""- **The near-term test** is whether Aurora goes from ≈25 to 200 driverless trucks in Q4 2026.""",
     r"""- **The near-term test** is whether Aurora goes from ≈25 to 200 driverless trucks by the end of February 2027, the date its Q3 letter gives."""),
    # §B8 Serve and its sources
    (r"""2026 revenue guidance cut to \$9–10 M (6 Aug 2026) [P] |""",
     r"""2026 revenue guidance cut to \$9–10 M (6 Aug 2026), then raised to \$12 M (5 Nov 2026); first city outside the US, in Australia, in Oct 2026 [P] |"""),
    (r"""https://www.pitneybowes.com/content/dam/pitneybowes/us/en/shipping-index/dmr-5127-parcel-shipping-index-report-2026-ebook.pdf""",
     r"""https://www.pitneybowes.com/content/dam/pitneybowes/us/en/shipping-index/dmr-5127-parcel-shipping-index-report-2026-ebook.pdf ; """ + SERVE + r""" (Serve Q3 2026 results)"""),
    # §B8 Ouster: Q3 list
    (r"""Ouster bought Stereolabs (stereo cameras) in Feb 2026 [T]. Its Q2 2026 results [P]:
    - revenue was \$55 M (+56% year on year), at a GAAP gross margin (under US generally accepted accounting principles) of 49%;
    - it shipped >17,000 lidar and camera sensors, ≈53% of them lidar (≈9,000 lidars [E: $0.53\times17{,}000\approx9{,}000$]);
    - product-revenue growth was "primarily driven by" industrial and smart-infrastructure customers.""",
     r"""Ouster bought Stereolabs (stereo cameras) in Feb 2026 [T]. Its Q3 2026 results [P]:
    - revenue was \$59.3 M (+50% year on year), at a GAAP gross margin (under US generally accepted accounting principles) of 43%, against \$55 M and 49% in Q2;
    - it shipped >27,000 lidar and camera sensors, ≈27% of them lidar (≈7,300 lidars [E: $0.27\times27{,}000\approx7{,}300$]), against ≈53% of >17,000 (≈9,000 lidars) in Q2;
    - product-revenue growth was "primarily driven by" industrial and robotics customers (warehouse automation, defense, construction, mapping and data collection);
    - Ouster says hundreds of customers have chosen Rev8, its colour-lidar generation (§C5b), while initial production ramps, with deliveries accelerating into 2027; it guides Q4 revenue at \$61–64 M."""),
    # §C3c and §C4 tables
    (r"""200 trucks "fully allocated" for end-2026 [P] (§B4, §C7)""",
     r"""200 trucks expected by the end of Feb 2027 (Q3 letter) [P] (§B4, §C7)"""),
    (r"""Aurora's driverless trucks (≈20–25, with 200 "fully allocated" for end-2026, §B4) [D]""",
     r"""Aurora's driverless trucks (≈20–25, with 200 expected by the end of Feb 2027, §B4) [D]"""),
    # §C7 Aurora
    (r"""At its 23 Sep 2026 investor day Aurora said it is "fully allocated" to exit 2026 with 200 driverless trucks.""",
     r"""At its 23 Sep 2026 investor day Aurora said it is "fully allocated" to exit 2026 with 200 driverless trucks; its Q3 letter (28 Oct) expects to pass 200 by the end of February 2027, and adds a Charger Logistics memorandum to own and operate 500 trucks (2027–28) and Volvo's plan for more than 300 driverless trucks in 2027 [P]."""),
    (r"""    - In Q2 2026 Aurora reported \$2 M of revenue, a \$270 M net loss and about \$1.2 B of cash [P].""",
     r"""    - In Q2 2026 Aurora reported \$2 M of revenue, a \$270 M net loss and about \$1.2 B of cash [P]. In Q3 it reported \$3 M of revenue, a \$257 M operating loss and about \$1.03 B of cash and short-term investments [P]."""),
    # §C7 Aeva
    (r"""    - It also works with **Bendix** on L2+ truck ADAS (advanced driver-assistance systems at level 2+, where the driver still supervises).""",
     r"""    - It also works with **Bendix** on L2+ truck ADAS (advanced driver-assistance systems at level 2+, where the driver still supervises).
    - In Q3 2026 it reported growing shipments of production-intent Atlas sensors to Daimler Truck, completion of the Bendix development programme, and a passed VDA process audit (the German automotive industry's supplier audit) for its top-10 European passenger-car customer [P]."""),
    # §C7 new bullet before Attrition
    (r"""- **Attrition:**
  - **Mobileye** ended its FMCW programme""",
     r"""- **Optics beyond lidar.** Two FMCW makers are taking their coherent photonics into data-centre optics. Aeva booked its first optical-connectivity revenue in Q3 2026, delivering ultra-high-power chipsets to a joint-development customer for AI data centres, and MicroVision's FMCW unit Scantinel announced its entry into high-speed optical connectivity for AI data centres [P].
- **Attrition:**
  - **Mobileye** ended its FMCW programme"""),
    # §C7a
    (r"""Aeva's Q2 2026 product revenue was \$2.5 M [P]; Aurora runs about 20–25 driverless trucks and plans 200 by end-2026, which it describes as "fully allocated" [P/T].""",
     r"""Aeva's Q2 2026 product revenue was \$2.5 M, and its Q3 revenue of \$6.7 M already included chips for data-centre optics [P]; Aurora runs about 20–25 driverless trucks and now expects 200 by the end of February 2027 [P/T]."""),
    # §E1 table
    (r"""**1 M unsupervised miles** (3 Sep 2026) [P].""",
     r"""**1 M unsupervised miles** (3 Sep 2026) and nearly 2 M by 30 Sep, with Cybercab deployment into the Austin fleet begun [P]."""),
    # fatality expectation
    (r"""Tesla's 1 M unsupervised miles (to 3 Sep 2026, §E1) imply an expected 0.012 fatalities at human rates ($10^{6}\times1.2\times10^{-8}=0.012$, assuming the recent US rate of about 1.2 fatalities per 100 M miles; RAND's 1.09 gives 0.011)""",
     r"""Tesla's nearly 2 M unsupervised miles (to 30 Sep 2026, §E1) imply an expected 0.024 fatalities at human rates ($2\times10^{6}\times1.2\times10^{-8}=0.024$, assuming the recent US rate of about 1.2 fatalities per 100 M miles; RAND's 1.09 gives 0.022)"""),
    # Appendix 2
    ("- Hesai Q3 2026 call transcript (Investing.com): " + CALL2,
     "- Hesai Q3 2026 call transcript (Investing.com): " + CALL2
     + "\n- Ouster Q3 2026 results: " + OUSTER
     + "\n- Aeva Q3 2026 results: " + AEVA
     + "\n- MicroVision Q3 2026 results: " + MVIS
     + "\n- Aurora Q3 2026 shareholder letter: " + AURORA
     + "\n- Kodiak Q3 2026 results: " + KODIAK
     + "\n- Tesla Q3 2026 update: " + TESLA
     + "\n- Serve Robotics Q3 2026 results: " + SERVE),
]

new = text
for old, rep in PAIRS:
    n = new.count(old)
    assert n == 1, f"anchor found {n} times: {old[:90]!r}"
    new = new.replace(old, rep, 1)
assert "\r" not in new and "\t" not in new
print(f"{len(PAIRS)} replacements; sha256 before {sha[:12]}, after {hashlib.sha256(new.encode('utf-8')).hexdigest()[:12]}")
if "--write" in sys.argv[3:]:
    report.write_bytes(new.encode("utf-8"))
    print("written")
else:
    print("check only (add --write to apply)")
