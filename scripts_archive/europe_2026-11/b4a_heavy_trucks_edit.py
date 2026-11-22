"""Chinese heavy trucks in §B4a subsection 3: closed sites (mines and ports), new operators, and the lidars that
filings and suppliers disclose (§0, §B4a, Appendix 1, Appendix 2).

Sources, read at source (PDF pages rendered and read):
- CiDi 2026 interim report (HKEX, 10 Aug 2026), pp. 7-8: more than 1,900 autonomous mining trucks deployed at 40 sites
  worldwide by 30 Jun 2026; seven sites with more than 100 trucks, the largest above 220; a 500-truck purchase order
  from Guangna Group (Feb 2026); non-binding commitments for more than 400 short-haul heavy trucks.
- CiDi prospectus (HKEX, 11 Dec 2025): p. 237 truck drawing with a forward lidar and 90 x 360 degree blind-spot
  lidars; p. 308 "Supplier K", lidar and lidar repair services, "Founded in 2014, registered in Shenzhen and listed on
  the Hong Kong Stock Exchange" (the identification with RoboSense is an inference).
- EACON 2026 interim report (HKEX, 23 Sep 2026), p. 5: about 6,000 active autonomous mining trucks in China on
  30 Jun 2026 by EACON's research, more than 3,100 of them EACON's (more than 1,600 a year earlier), 38 sites, the
  largest with 566 trucks, more than 1,000 on order, about 1,500 newly deployed industry-wide in H1 2026.
- EACON prospectus (HKEX, 29 Jun 2026), pp. 142-143: main, supplementary and rear lidars; 360 degree coverage.
- EACON and Tibet Julong Copper release (PR Newswire, 4 Nov 2026): all 60 battery-electric trucks at the Zhibula
  copper mine, above 5,400 m, in site-wide autonomous operation by the end of September 2026.
- Pony.ai release (PR Newswire, Hannover, 14 Sep 2026): Gen-4 truck on GAC Commercial Vehicle's T9 battery-electric
  platform; nine lidars, three millimetre-wave radars and 13 cameras; the Gen-7 robotaxi's domain controller; driving
  kit bill of materials 70% below the previous generation; cost per tonne-km expected to fall 30%; volume production
  later in 2026.
- Trunk Technology application proof (HKEX, 12 Jun 2026): p. 1 (1,283 trucks delivered, backlog RMB 236.0 M,
  driverless port solution), p. 124 (system drawing with a roof lidar), p. 135 (assisted driving with safety officers
  or platooned freight on demonstration routes), p. 216 (cost of sales: lidar RMB 32,987k, 17,301k and 24,358k in
  2023-2025 against totals of RMB 117,716k, 196,480k and 251,194k).
- Seyond annual report 2025 (HKEX, 27 Apr 2026), p. 4: Falcon 1,550 nm design nominations ("designated projects")
  from Pony.ai, EACON Mining and Inceptio Technology.
- Hesai releases: 21 Apr 2023 (KargoBot integrated five AT128 per truck; more than 100 trucks); 21 Apr 2025
  (AT1440 for KargoBot's platooning solution); 30 Jul 2024 (Westwell fits multiple XT32 and AT128 per vehicle).
- DeepWay: 科创板日报 (8 May 2026) and Sina (8 May 2026), both summarising its May 2026 Hong Kong listing application.
- China's Ministry of Transport, 自动驾驶汽车运输安全服务指南（试行）, 交办运〔2023〕66号, sections 3 and 6.
- Xinhua, 17 Jun 2026: a Shaanxi Automobile engineering executive on the two settings of commercial truck automation.

Usage: b4a_heavy_trucks_edit.py <report.md> <expected sha256 prefix> [--write]
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

CIDI_IR = "https://www1.hkexnews.hk/listedco/listconews/sehk/2026/0810/2026081000436.pdf"
CIDI_PR = "https://www1.hkexnews.hk/listedco/listconews/sehk/2025/1211/2025121100007.pdf"
EACON_IR = "https://www1.hkexnews.hk/listedco/listconews/sehk/2026/0923/2026092301671.pdf"
EACON_PR = "https://www1.hkexnews.hk/listedco/listconews/sehk/2026/0629/2026062900135.pdf"
EACON_ZHIBULA = ("https://www.prnewswire.com/apac/news-releases/60-autonomous-electric-haul-trucks-achieve-site-wide-"
                 "operation-at-5-400m-copper-mine-302929085.html")
PONY_GAC = ("https://www.prnewswire.com/news-releases/ponyai-unveils-new-gen-4-robotruck-in-collaboration-with-gac-"
            "commercial-vehicle-302877606.html")
TRUNK_AP = "https://www1.hkexnews.hk/app/sehk/2026/108635/documents/sehk26061201929.pdf"
SEYOND_AR = "https://www1.hkexnews.hk/listedco/listconews/sehk/2026/0427/2026042700628.pdf"
HESAI_KARGOBOT_2023 = "https://www.hesaitech.com/?p=1934"
HESAI_INFINITY_EYE = ("https://www.automotiveworld.com/news-releases/hesai-unveils-infinity-eye-lidar-solution-for-l2-"
                      "l3-and-l4-autonomous-driving-systems/")
HESAI_WESTWELL = ("https://www.hesaitech.com/hesai-and-westwell-partner-to-accelerate-global-expansion-in-autonomous-"
                  "driving-for-logistics/")
DEEPWAY_CLS = "https://www.cls.cn/detail/2366476"
DEEPWAY_SINA = "https://finance.sina.cn/2026-05-08/detail-inhxefhp4278869.d.html"
MOT_GUIDE = "https://xxgk.mot.gov.cn/2020/jigou/ysfws/202312/t20231205_3962490.html"
XINHUA = "https://www.news.cn/tech/20260617/501e62e20cb94c51be9a7a6d1c5b1489/c.html"

# ---- whole-line replacements, found by a unique line prefix
LINE_EDITS = [
    # §B4a subsection 3 table: Pony.ai row (GAC model, primary cost figures, lidar cell)
    ("| **Pony.ai** | Gen-4 heavy truck built with Sany",
     r"""| **Pony.ai** | Gen-4 heavy truck built with Sany, and a second Gen-4 heavy-duty model on GAC Commercial Vehicle's T9 battery-electric truck, shown at IAA Transportation in Hannover on 14 Sep 2026 for long-haul, fixed-route and port freight. A "1+4" platoon with Sinotrans: a human-driven lead truck and four autonomous followers. Robotrucks are being deployed at Jiangmen Port and Shenzhen's Mawan Port, with regular commercial operation planned, and fully driverless light-duty trucks have entered production, with first deployments for logistics clients in tier-one cities [P] | About 200 trucks (Nov 2025). Target of 500–1,000 Gen-4 trucks within two to three years (Aug 2026); the Gen-4 entered mass production on schedule in Q3 2026, and volume production of the GAC model was due to begin later in 2026 [P]. The bill of materials of the Gen-4 driving kit is 70% below the previous generation's, and Pony.ai expects freight costs per tonne-km to fall by 30% [P]. Robotruck revenue was \$18.0 M in Q3 2026, up 76.3%, mainly from freight services with Sinotrans [P] | Whether the followers carry safety staff is not stated [U] | Nine lidars, three radars and 13 cameras on the GAC model, which uses the Gen-7 robotaxi's domain controller [P]; the lidar supplier is not named. Seyond reports a design nomination for its 1,550 nm Falcon from Pony.ai without naming the vehicle [P]; the Gen-7 robotaxi carries four Hesai AT128 (§G1) |"""),
    # Mining row, preceded by two new rows (Trunk Technology, ports)
    ("| **Mining (off-road)** |",
     r"""| **Trunk Technology** (主线科技) | Driverless trucks in seaports, river and dry ports, border crossings and industrial zones ("Trunk Port"); road freight with safety officers, or in "1+N" platoons behind a human-driven truck on designated demonstration routes ("Trunk Pilot"); urban projects [P] | 1,283 trucks delivered by its Hong Kong listing application of 12 Jun 2026, with an order backlog of RMB 236.0 M on 30 Apr 2026. Revenue rose from RMB 134.1 M in 2023 to RMB 344.5 M in 2025, with a net loss each year (RMB 170.9 M in 2025) [P] | Driverless in ports; a safety officer or a human-led platoon on public roads [P] | One roof lidar in its system drawing. Lidar cost RMB 24.4 M in 2025, 9.7% of its cost of sales, against RMB 33.0 M and 28.0% in 2023 [P, application proof pp. 124, 216; E for the shares]; suppliers unnamed [P] |
| **Ports** | Cab-less electric container trucks inside terminals: Westwell's Q-Trucks, in Chinese ports and abroad, including a fleet of 100 at the UK's Port of Felixstowe (§B4b); Trunk's and Pony.ai's port trucks (above) [P] | Westwell publishes no fleet total [U] | Driverless within the terminal [D] | Westwell: "multiple" Hesai XT32 and AT128 per vehicle [P, Hesai, Jul 2024] |
| **Mining (off-road)** | Driverless haul trucks in open-pit coal and metal mines: CiDi, EACON, Huaneng with XCMG, Waytous, Tage Idriver, Boonray | About 6,000 autonomous mining trucks were active in China on 30 Jun 2026 by EACON's count, more than 3,100 of them EACON's (more than 1,600 a year earlier), at 38 sites, the largest with 566 trucks; more than 1,000 more were on order [P, EACON interim report, p. 5]. CiDi had deployed more than 1,900 at 40 sites worldwide, seven of them with more than 100 trucks and the largest with more than 220, and took a 500-truck order from Guangna Group in Feb 2026 [P, CiDi interim report, p. 7]; in its 2025 report one operator oversees 100 trucks [T, International Mining]. All 60 battery-electric trucks at Zijin's Zhibula copper mine, above 5,400 m, ran driverless across the site by end-Sep 2026 [P, EACON] | Driverless, but on closed sites [D] | CiDi: a forward lidar and hemispherical (90° × 360°) blind-spot lidars; its unnamed lidar supplier was "founded in 2014, registered in Shenzhen and listed on the Hong Kong Stock Exchange", which fits RoboSense [P, prospectus pp. 237, 308; E for the identification]. EACON: main, supplementary and rear lidars [P, prospectus p. 142]; Seyond reports a Falcon design nomination from EACON [P]. Counts per truck are not published [U] |"""),
    # "What this shows": highway trucking and the national rules
    ("- **Driverless public-highway trucking.** China's driverless public-highway operations",
     r"""- **Driverless public-highway trucking.** China's driverless public-highway operations are not clearly larger than those in the US. Its scale is in assisted line haul (Inceptio's billion km, with drivers) and in driverless trucks on closed sites, mines and ports. On public highways the leading pattern is a platoon led by a human driver. The national rules point the same way. The Ministry of Transport's 2023 service guide lets autonomous trucks carry freight on point-to-point trunk highways and on urban roads where traffic safety is controllable, bans dangerous goods, and says such trucks carry a safety officer "in principle"; it allows remote safety officers, at least one per three vehicles, only for fully driverless taxis [P, 交办运〔2023〕66号, sections 3 and 6]. A Shaanxi Automobile engineering executive described commercial truck automation to Xinhua in Jun 2026 in the same two settings: assisted driving on trunk highways, and autonomous haulage in ports, mines and logistics parks [T, Xinhua, 17 Jun 2026]."""),
    ("- **The US comparison.** The US has a handful of trucks with no driver at the controls",
     r"""- **The US comparison.** The US has a handful of trucks with no driver at the controls: Aurora's ≈20–25 on public highways, which carry an observer, and Kodiak's 37 at the end of Q3 2026, mostly hauling frac sand on Permian Basin lease roads (§B4). China's ≈6,000 driverless mining trucks are a different case: off-road, on private sites."""),
    ("- **Lidar on Chinese heavy trucks.** Counts and suppliers are not published [U].",
     r"""- **Lidar on Chinese heavy trucks.** Counts are published for two trucks: nine lidars on Pony.ai's GAC model and five Hesai AT128 on KargoBot's 2023 truck [P]. The mining trucks carry a main or forward lidar plus blind-spot, supplementary or rear units, in numbers their makers' prospectuses do not give [P].
  - **Installed base and annual flow** [E]. If each of the ≈6,000 active mining trucks carries two to four lidars, they hold ≈12–24k lidars ($6{,}000\times(2\text{–}4)=12\text{–}24\text{k}$), against ≈27–40k on all robotaxis and trucks outside China (§B4). About 1,500 mining trucks were newly deployed in China in H1 2026, by EACON's count [P], or ≈3,000 a year, which adds ≈6–12k lidars a year ($3{,}000\times(2\text{–}4)$), small next to the vans' ≈33–220k (subsection 2).
  - **Suppliers.** Seyond reports design nominations for its 1,550 nm Falcon from Inceptio, Pony.ai and EACON; Hesai supplies KargoBot and Westwell; and CiDi's unnamed lidar supplier fits RoboSense [P/E].
  - **Cost.** Trunk's filing gives a rare cost share: lidar was RMB 24.4 M in 2025, 9.7% of its cost of sales [P/E: $24.358/251.194\approx0.097$], down from 28.0% in 2023 ($32.987/117.716\approx0.280$)."""),
    # Appendix 1: the delivery-van item stays; a heavy-truck item follows it
    ("- **China's delivery vans (§B4a).**", None),
]

# ---- cells appended to existing table rows (the row must end with " |")
APPEND_CELLS = [
    ("| **Inceptio** | L2+ line-haul trucks",
     r"Seyond's 1,550 nm Falcon: Seyond reports a design nomination from Inceptio for L4 projects [P, Seyond annual "
     r"report 2025, p. 4]; units per truck are not published [U]"),
    ("| **KargoBot** (DiDi-backed) |",
     r"Hesai: five AT128 per truck in Apr 2023, when KargoBot ran more than 100 trucks [P]; the AT1440 for its "
     r"platooning solution (Apr 2025) [P]; and Hesai's colour ETX as primary lidar of its Space 2.0 transport robots, "
     r"an exclusive award (May 2026, §C5b) [P]"),
]

APPENDIX1_TRUCKS = (
    "- **Chinese heavy trucks (§B4a subsection 3).** Lidar counts are published only for Pony.ai's GAC truck (nine) "
    "and KargoBot's 2023 truck (five AT128) [P]. Unknown: the number of lidars per mining truck (CiDi's and EACON's "
    "prospectuses show the positions, not the number), per Inceptio truck and per Westwell truck; the identity of "
    "CiDi's lidar supplier, whose description fits RoboSense; any lidar on DeepWay's trucks; and Westwell's fleet "
    "total.")

# ---- substring replacements (each anchor must occur exactly once)
EDITS = [
    # §0, executive summary
    ("They are driverless at scale only in closed mines.\n",
     "They are driverless at scale only on closed sites: about 6,000 autonomous haul trucks in mines, by the leading "
     "supplier's count, and cab-less trucks in ports.\n"),
    # §B4a short answer
    ("Fully driverless heavy trucks run at scale only in closed mines [D]; on public roads they are in pilots [NT].",
     "Fully driverless heavy trucks run at scale only on closed sites: about 6,000 autonomous haul trucks were active "
     "in China's mines in mid-2026, and cab-less trucks run inside ports [D]. On public roads they are in pilots [NT], "
     "and the transport ministry still expects a freight truck to carry a safety officer [P]."),
    # §B4a subsection 3 opening
    ("This subsection lists the main operators and shows that fully driverless operation at scale is confined to "
     "closed mine sites.",
     "This subsection lists the main operators, shows that fully driverless operation at scale is confined to closed "
     "sites, mines and ports, and gathers what filings and suppliers disclose about the lidars on these trucks."),
    # table header gains a lidar column
    ("| Operator | What runs | Scale | Driver status |\n|---|---|---|---|\n| **Inceptio** |",
     "| Operator | What runs | Scale | Driver status | Lidar |\n|---|---|---|---|---|\n| **Inceptio** |"),
    # DeepWay before the reading notes; the notes gain three terms
    ("How to read the table. \"L2+\" denotes supervised driver assistance",
     "**DeepWay** (深向科技), an electric heavy-truck maker set up by Baidu and the logistics-finance group Lionbridge "
     "(狮桥) in Dec 2020, delivered 509, 3,002 and 8,020 trucks in 2023–2025 and 1,409 in Q1 2026. Its own "
     "assisted-driving system has been standard on every new truck since May 2025 and was on more than 6,000 trucks "
     "delivered by end-2025. Revenue was RMB 3.96 B in 2025, with a loss of RMB 649 M [T, 科创板日报, 8 May 2026]. "
     "Its platooning system, with a human-driven lead truck, was on 10 trucks delivered in 2025, and its single-truck "
     "L4 system is not yet commercial, in testing in Beijing, Tianjin and Hefei [T, Sina, 8 May 2026; both summarise "
     "its May 2026 Hong Kong listing application]. No source found names a lidar on its trucks [U].\n"
     "\n"
     "How to read the table. \"L2+\" denotes supervised driver assistance"),
    ("DiDi is a Chinese ride-hailing company, and Horizon Robotics a Chinese maker of driving chips.",
     "DiDi is a Chinese ride-hailing company, and Horizon Robotics a Chinese maker of driving chips. Cost of sales is "
     "the direct cost of the goods and services a company sold. A design nomination (Seyond's \"designated project\") "
     "is a customer's choice of a supplier for a programme, not a delivery. A cab-less truck has no driver's cab, so "
     "nobody can drive it from inside."),
    # §B4a subsection 3 sources
    ("tm2629888d1_ex99-1.htm (Pony.ai Q3 2026 results)\n",
     "tm2629888d1_ex99-1.htm (Pony.ai Q3 2026 results) ; " + CIDI_IR + " (CiDi 2026 interim report, pp. 7–8) ; "
     + CIDI_PR + " (CiDi prospectus, pp. 237, 308) ; " + EACON_IR + " (EACON 2026 interim report, p. 5) ; " + EACON_PR
     + " (EACON prospectus, pp. 142–143) ; " + EACON_ZHIBULA + " ; " + PONY_GAC + " ; " + TRUNK_AP
     + " (Trunk Technology application proof, pp. 1, 124, 135, 216) ; " + SEYOND_AR
     + " (Seyond annual report 2025, p. 4) ; " + HESAI_KARGOBOT_2023 + " ; " + HESAI_INFINITY_EYE + " ; "
     + HESAI_WESTWELL + " ; " + DEEPWAY_CLS + " ; " + DEEPWAY_SINA + " ; " + MOT_GUIDE + " ; " + XINHUA + "\n"),
    # Appendix 2, robotaxi and trucks group
    ("- NHTSA Standing General Order crash reports, ADS incidents (current file and 2021–2025 archive): ",
     "- CiDi 2026 interim report (HKEX, 10 Aug 2026; autonomous mining trucks deployed, sites and orders, pp. 7–8): "
     + CIDI_IR + "\n"
     "- EACON 2026 interim report (HKEX, 23 Sep 2026; active autonomous mining trucks in China and EACON's fleet, "
     "p. 5): " + EACON_IR + "\n"
     "- Trunk Technology application proof (HKEX, 12 Jun 2026; deliveries p. 1, safety officers and platoons p. 135, "
     "lidar in cost of sales p. 216): " + TRUNK_AP + "\n"
     "- Pony.ai Gen-4 truck with GAC Commercial Vehicle and its sensor set (PR Newswire, 14 Sep 2026): " + PONY_GAC + "\n"
     "- Seyond annual report 2025 (HKEX; Falcon design nominations from Pony.ai, EACON and Inceptio, p. 4): "
     + SEYOND_AR + "\n"
     "- China's Ministry of Transport, service guide for autonomous-vehicle transport (交办运〔2023〕66号; freight "
     "settings, section 3; safety officers, section 6): " + MOT_GUIDE + "\n"
     "- NHTSA Standing General Order crash reports, ADS incidents (current file and 2021–2025 archive): "),
]

new = text
lines = new.split("\n")
for prefix, rep in LINE_EDITS:
    hits = [i for i, ln in enumerate(lines) if ln.startswith(prefix)]
    assert len(hits) == 1, f"line prefix found {len(hits)} times: {prefix[:80]!r}"
    i = hits[0]
    if rep is None:  # the Appendix 1 van item: keep it and add the heavy-truck item after it
        lines[i] = lines[i] + "\n" + APPENDIX1_TRUCKS
    else:
        lines[i] = rep
for prefix, cell in APPEND_CELLS:
    hits = [i for i, ln in enumerate(lines) if ln.startswith(prefix)]
    assert len(hits) == 1, f"row prefix found {len(hits)} times: {prefix[:80]!r}"
    i = hits[0]
    assert lines[i].endswith(" |"), f"row does not end with a cell border: {prefix!r}"
    lines[i] = lines[i] + " " + cell + " |"
new = "\n".join(lines)
for old, rep in EDITS:
    n = new.count(old)
    assert n == 1, f"anchor found {n} times: {old[:90]!r}"
    new = new.replace(old, rep, 1)
assert "\r" not in new
print(f"{len(LINE_EDITS)} line edits, {len(APPEND_CELLS)} appended cells, {len(EDITS)} substring edits; "
      f"sha256 before {sha[:12]}, after {hashlib.sha256(new.encode('utf-8')).hexdigest()[:12]}")
if "--write" in sys.argv[3:]:
    report.write_bytes(new.encode("utf-8"))
    print("written")
