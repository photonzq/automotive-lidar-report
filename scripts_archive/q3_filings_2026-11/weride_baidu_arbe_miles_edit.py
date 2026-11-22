"""WeRide's and Baidu's Q3 2026 results, Arbe's Q3 2026 results, and the published mileage of ten robotaxi and
driverless fleets against Waymo's (§B4, §E1, §E2a, §F7 with Figure F7.1, Appendix 1, Appendix 2).

Sources, read at source:
- WeRide Q3 2026 results (6-K of 20 Nov 2026, Exhibit 99.1): Middle East fleet about 600, up about 50% from about 400
  on 31 Jul 2026, full coverage of core Abu Dhabi and Dubai targeted by year-end; Uber's largest AV partner outside
  the US by fully driverless robotaxis on its platform; global L4 fleet about 4,100 on 31 Oct 2026, more than 2,300
  robotaxis; robotaxi revenue above RMB 100 M for the first time, more than 90% overseas; Spain's first national L4
  passenger-vehicle permit (DGT), testing of the GXR and mapping of the Madrid region; public robotaxi service in the
  Canton of Zurich with SBB and Swiss Transit Lab; Robobus at Zurich Airport without an onboard safety operator;
  first robotaxis road-testing in Slovakia. No mileage is given.
- Baidu Q3 2026 results (6-K of 16 Nov 2026, Exhibit 99.1): Apollo Go widened its fully driverless commercial area in
  Dubai and doubled its fleet there, tested in London with Uber and Lyft and driverless on Hong Kong's Airport Island,
  reached 30 cities in Oct 2026, drove about 34 M autonomous km in Q3 2026 and more than 390 M km by 31 Oct 2026.
  Baidu's Q4 2025 release (26 Feb 2026) and Q2 2026 release (18 Aug 2026): more than 300 M and 350 M autonomous km,
  including more than 190 M and 240 M km fully driverless, "to date".
- Arbe Q3 2026 results (6-K of 19 Nov 2026, Exhibit 99.1): HiRain imaging radar on Arbe's chipset chosen by an unnamed
  large carmaker group for a multi-brand L3 programme in China, series deliveries from Q4 2027; defence framework with
  an unnamed integrator (three projects, initial orders delivered); Alerion counter-drone radar; revenue $0.752 M;
  2026 revenue guidance $2.3-3.0 M after two integration projects slipped to 2027; cash, cash equivalents and bank
  deposits $48.0 M on 30 Sep 2026 including $13.8 M net from the $15 M September offering; Q3 net cash used in
  operations $7.768 M; convertible bonds $24.273 M in current liabilities.
- Mileage: Waymo Safety Impact hub (271.3 M rider-only miles through June 2026, unchanged on 21 Nov 2026); Waymo blog of
  24 Jun 2026 (more than 220 M fully autonomous miles through March 2026; more than 4 M miles a week); Alphabet Q3 2026
  call, CEO remarks of 28 Oct 2026 (more than 300 M fully autonomous miles); Pony.ai and Verne release of 10 Sep 2026
  (more than 100 M km, including more than 40 M km fully driverless); WeRide's products page, read 21 Nov 2026 (more
  than 55,000,000 km of L4 driving on public roads); Zoox via TechCrunch of 24 Mar 2026 (close to 2 M autonomous
  miles) and Axios of 12 Aug 2026 (3 M miles); Motional's Voluntary Safety Self-Assessment 2026, section 2.2 (more than
  2 M autonomous miles); May Mobility's release of 12 Nov 2026 (more than 600,000 commercial autonomous rides across
  1.1 M miles); Tesla Q3 2026 update (nearly 2 M cumulative unsupervised Robotaxi miles at the end of the quarter,
  eightfold growth on the quarter); Cruise's chief executive on 11 Aug 2023, quoted by GM Authority (4 M driverless
  miles, more than 1 M a month). The conversions, rates and ratios are computed, with checks, by
  build/figures/robotaxi_weekly_miles.py, which also draws Figure F7.1.

Usage: weride_baidu_arbe_miles_edit.py <report.md> <expected sha256 prefix> [--write]
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

WERIDE = "https://www.sec.gov/Archives/edgar/data/1867729/000110465926130438/tm2630019d1_ex99-1.htm"
BAIDU = "https://www.sec.gov/Archives/edgar/data/1329099/000119312526462286/d767848dex991.htm"
BAIDU_Q4_2025 = "https://www.sec.gov/Archives/edgar/data/1329099/000119312526076505/d117608dex991.htm"
BAIDU_Q2_2026 = "https://www.sec.gov/Archives/edgar/data/1329099/000119312526355431/d112854dex991.htm"
ARBE = "https://www.sec.gov/Archives/edgar/data/1861841/000121390026121995/ea031250901ex99-1.htm"
WAYMO_BLOG = "https://waymo.com/blog/shorts/safetydata-june26/"
ALPHABET = "https://blog.google/company-news/inside-google/message-ceo/alphabet-earnings-q3-2026/"
PONY_VERNE = ("https://www.prnewswire.com/news-releases/ponyai-and-verne-kick-off-fully-driverless-robotaxi-test-rides-"
              "in-zagreb-302874840.html")
WERIDE_SITE = "https://weride.ai/products"
ZOOX_TC = "https://techcrunch.com/2026/03/24/zoox-brings-its-robotaxis-to-austin-and-miami/"
ZOOX_AXIOS = "https://www.axios.com/2026/08/12/zoox-robotaxi-safety-framework"
MOTIONAL_VSSA = "https://motional.com/sites/default/files/inline-files/Motional_Voluntary_Safety_Self-Assessment_2026.pdf"
MAY = ("https://www.prnewswire.com/news-releases/may-mobility-plans-to-bring-autonomous-volkswagen-id-buzz-vehicles-to-"
       "global-robotaxi-platforms-302936992.html")
CRUISE = "https://gmauthority.com/blog/2023/08/gms-cruise-racks-up-4-million-driverless-miles/"

MILES_BLOCK = (
    "**Robotaxi miles against Waymo's.** The operators publish mileage on different bases: rider-only miles (no human "
    "driver aboard) for Waymo; fully driverless kilometres within a larger autonomous total for Baidu and Pony.ai; "
    "autonomous totals that include driving with safety operators for WeRide, Motional and May Mobility; autonomous "
    "miles of purpose-built robotaxis for Zoox; and unsupervised miles for Tesla. The table converts each figure to "
    "miles, derives miles per week where two dated totals allow it, and compares both with Waymo's (Figure F7.1) [P for "
    "the published figures; E for the rates and ratios]. DiDi, Hello, CaoCao and Momenta's robotaxi unit in China, and "
    "Avride, Mobileye, Wayve and Nuro in the West, had published no current robotaxi mileage in the sources checked "
    "(Appendix 1) [U].\n"
    "\n"
    "| Operator | Published mileage (date) | What is counted | Miles per week [E] | Against Waymo [E] |\n"
    "|---|---|---|---|---|\n"
    "| **Waymo** | 271.3 M through Jun 2026 and more than 220 M through Mar 2026 (Safety Hub; Waymo's blog); more than "
    "300 M by 28 Oct 2026 (Alphabet) [P] | Rider-only miles | ≈3.95 M in Q2 2026; more than 4 M by late June, by "
    "Waymo's own account [P] | 1 |\n"
    "| **Baidu Apollo Go** | More than 190 M km fully driverless of more than 300 M km (26 Feb 2026); more than 240 M km "
    "(≈149 M miles) fully driverless of more than 350 M km (18 Aug 2026); ≈34 M km in Q3 2026 and more than 390 M km "
    "(≈242 M miles) in all by 31 Oct 2026 [P] | Fully driverless subset; the Q3 figure is all autonomous kilometres | "
    "≈1.26 M driverless, Feb–Aug 2026; ≈1.61 M all autonomous in Q3 2026 | Weekly 0.32 driverless, 0.41 all; "
    "driverless total 0.55 |\n"
    "| **Pony.ai** | More than 100 M km (≈62.1 M miles), including more than 40 M km (≈24.9 M miles) fully driverless, "
    "by 10 Sep 2026 [P] | Fully driverless subset | Not published | Driverless total 0.092 |\n"
    "| **WeRide** | More than 55 M km (≈34.2 M miles) of L4 driving on public roads, all products (website, read 21 Nov "
    "2026); no mileage in its Q3 2026 release [P] | All autonomous, without a driverless split | Not published | Not "
    "comparable |\n"
    "| **Zoox** | Close to 2 M autonomous miles on 24 Mar 2026 and 3 M on 12 Aug 2026, as told to the press [T] | "
    "Autonomous miles of its robotaxis, which have no manual controls | ≈0.050 M, Mar–Aug 2026 | Weekly 0.013; total "
    "0.011 |\n"
    "| **Motional** | More than 2 M autonomous miles across several platform generations (safety self-assessment, "
    "2026) [P] | All autonomous, without a driverless split | Not published | Not comparable |\n"
    "| **May Mobility** | More than 600,000 commercial autonomous rides across 1.1 M miles in the US and Japan (12 Nov "
    "2026) [P] | All autonomous rides, from three driver-out deployments and others with operators | Not published | "
    "Not comparable |\n"
    "| **Tesla** | Nearly 2 M unsupervised Robotaxi miles by 30 Sep 2026, eight times the end-June total [P]; 1 M on "
    "3 Sep [T] | Unsupervised miles of a camera-only fleet | ≈0.133 M in Q3 2026; at most ≈0.259 M in September | "
    "Weekly 0.034 in Q3, at most 0.066 in September; total 0.0074 |\n"
    "| **Cruise** (driverless service stopped in Oct 2023) | 4 M driverless miles on 10 Aug 2023, at more than 1 M a "
    "month [T] | Driverless miles | More than 0.23 M in Aug 2023 | Weekly 0.058; total 0.015 |\n"
    "| **Aurora** (trucks) | More than 500k driverless miles, May 2025 to late Sep 2026 (§B4) [P] | Driverless miles, "
    "with an observer in the cab (§B4) | ≈0.007 M | Total 0.0018 |\n"
    "\n"
    "The rates and ratios come from these figures [E]:\n"
    "- **Waymo:** $271.3-220=51.3$ M rider-only miles in the 13 weeks of Q2 2026, so $51.3/13\\approx3.95$ M a week, "
    "the reference for the weekly ratios; its 271.3 M total to June is the reference for the ratios of driverless "
    "totals. The March total is a lower bound (\"more than 220 M\"), so the Q2 rate is at most slightly high.\n"
    "- **Baidu:** its driverless total rose by $240-190=50$ M km, or $50\\times10^{6}/1.609\\approx31.1\\times10^{6}$ "
    "miles, in the 24.7 weeks from 26 Feb to 18 Aug 2026 (173 days), so $31.1/24.7\\approx1.26$ M miles a week and "
    "$1.26/3.95\\approx0.32$. Its total grew by the same 50 M km ($350-300$), so most of its recent kilometres were "
    "driverless. All four totals are lower bounds rounded to 10 M km, so the difference is uncertain by about ±20%. "
    "In Q3 2026 it drove $34\\times10^{6}\\ \\mathrm{km}/1.609\\approx21.1\\times10^{6}$ miles in all in 13.1 weeks (92 "
    "days), $21.1/13.1\\approx1.61$ M a week and $1.61/3.95\\approx0.41$, or $1.61\\times52\\approx84$ M miles a year; "
    "Baidu does not split that figure. Its driverless total of $240\\times10^{6}/1.609\\approx149\\times10^{6}$ miles "
    "is $149/271.3\\approx0.55$ of Waymo's.\n"
    "- **Pony.ai:** $40\\times10^{6}/1.609\\approx24.9\\times10^{6}$ fully driverless miles and "
    "$100\\times10^{6}/1.609\\approx62.1\\times10^{6}$ in all; $24.9/271.3\\approx0.092$, and less at equal dates, since "
    "Waymo's total is ten weeks older.\n"
    "- **WeRide, Motional and May Mobility:** $55\\times10^{6}/1.609\\approx34.2\\times10^{6}$ miles for WeRide; "
    "Motional's and May Mobility's figures are already in miles. None separates driverless from supervised driving, so "
    "none is set against Waymo's rider-only total.\n"
    "- **Zoox:** about $3-2=1$ M miles in the 20.1 weeks from 24 Mar to 12 Aug 2026 (141 days), so "
    "$1/20.1\\approx0.050$ M a week and $0.050/3.95\\approx0.013$; its total is $3/271.3\\approx0.011$ of Waymo's. Both "
    "totals are rounded, so the rate is an order of magnitude.\n"
    "- **Tesla:** an eightfold rise to nearly 2 M puts the end-June total at about $2/8=0.25$ M, so Q3 added about "
    "$2-0.25=1.75$ M, or $1.75/13.1\\approx0.133$ M a week, and $0.133/3.95\\approx0.034$; a year at that rate is "
    "$0.133\\times52\\approx6.9$ M miles. From 1 M on 3 Sep to nearly 2 M on 30 Sep (27 days, 3.86 weeks), the pace "
    "was at most $(2-1)/3.86\\approx0.259$ M a week, and $0.259/3.95\\approx0.066$. Its total is "
    "$2/271.3\\approx0.0074$ of Waymo's.\n"
    "- **Cruise:** more than 1 M a month is more than $1/4.35\\approx0.23$ M a week, $0.23/3.95\\approx0.058$ of "
    "Waymo's Q2 rate, and its 4 M total is $4/271.3\\approx0.015$ of Waymo's.\n"
    "- **Aurora:** $0.5/73\\approx0.007$ M a week over the 73 weeks since May 2025, and $0.5/271.3\\approx0.0018$ of "
    "Waymo's total.\n"
    "\n"
    "On these rates the lidar-based fleets drive at least 94% of the miles listed. Waymo and Zoox alone give "
    "$4.0/(4.0+0.259)\\approx0.94$ even against Tesla's September pace, and Baidu's driverless 1.26 M raises the share "
    "to $5.26/(5.26+0.259)\\approx0.95$, before Pony.ai, WeRide and the rest are counted [E]. Call 1's 85% threshold "
    "therefore has a margin today; whether it holds to 2028 depends on how fast Tesla's weekly miles grow from about 7% "
    "of Waymo's, a pace Cruise had already reached in 2023 [E]. By total driverless miles only Baidu is within a factor "
    "of two of Waymo; Pony.ai has about a tenth of Waymo's total and every other fleet less than 2% [E].\n"
    "\n"
    "::::: capside\n"
    "![Published totals and weekly miles of ten robotaxi and driverless fleets against Waymo's]"
    "(automotive_perception_report_figures/robotaxi_weekly_miles.png)\n"
    "\n"
    "::: capbody\n"
    "*Figure F7.1.* Published mileage of ten fleets, on logarithmic scales: (a) the latest published totals, with the "
    "driverless part darker where an operator gives it; (b) miles per week where two dated totals allow a rate, with "
    "the fraction of Waymo's ≈3.95 M a week in parentheses.\n"
    "- Dark blue is driverless miles of lidar-based fleets, and pale blue totals that include driving with safety "
    "operators, so Baidu's pale bar in (b) is an upper bound on its driverless rate. Red is Tesla's unsupervised, "
    "camera-only miles, and grey Cruise, whose driverless service stopped in Oct 2023.\n"
    "- ≤ marks an upper bound and > a lower bound. WeRide, Motional and May Mobility give no driverless split, and "
    "Pony.ai no quarterly figure, so (b) leaves them out (table above).\n"
    "- *Script:* `build/figures/robotaxi_weekly_miles.py` [E].\n"
    "\n"
    ":::\n"
    ":::::"
)

EDITS = [
    # ---- §B4: installed base, vehicle side
    ("- On the vehicle side, the fleets with published numbers (Waymo 4,000; Tesla 300–546, with no lidar; Zoox 100; "
     "Motional 109; Avride 200; WeRide ≈400) sum to ≈5.1–5.4k. VW/Mobileye, Pony, Baidu and the trucks make up the "
     "rest.\n",
     "- On the vehicle side, the fleets with published numbers (Waymo 4,000; Tesla 300–546, with no lidar; Zoox 100; "
     "Motional 109; Avride 200; WeRide ≈400 in the Middle East on 31 Jul) sum to ≈5.1–5.4k. VW/Mobileye, Pony, Baidu "
     "and the trucks make up the rest. WeRide's Middle East fleet had reached about 600 by its Q3 release of 20 Nov "
     "2026 [P], which raises the sum to ≈5.3–5.6k ($4{,}000+300+100+109+200+600=5{,}309$; with Tesla's 546, "
     "$5{,}555$).\n"),
    # ---- §B4: Chinese operators abroad, the parenthesis
    ("- **Chinese operators abroad** (WeRide about 400 in the Middle East; Pony and Baidu in Doha, Zagreb, Dubai and "
     "Switzerland)",
     "- **Chinese operators abroad** (WeRide about 600 in the Middle East by Nov 2026; Pony and Baidu in Doha, Zagreb, "
     "Dubai and Switzerland)"),
    # ---- §B4: Chinese operators abroad, WeRide and Baidu after Pony.ai
    ("and has signed a memorandum with inDrive and NVIDIA on Kazakhstan [P].\n",
     "and has signed a memorandum with inDrive and NVIDIA on Kazakhstan [P]. WeRide's Middle East fleet grew from about "
     "400 vehicles on 31 Jul 2026 to about 600 by its Q3 release of 20 Nov, and WeRide aims to cover the core urban "
     "areas of Abu Dhabi and Dubai by year-end; counted by fully driverless robotaxis on Uber's platform, it is Uber's "
     "largest autonomous-vehicle partner outside the US. Its global L4 fleet was about 4,100 vehicles on 31 Oct 2026, "
     "more than 2,300 of them robotaxis, and more than 90% of its Q3 robotaxi revenue, above RMB 100 M for the first "
     "time, came from outside China. In Europe it holds Spain's first national L4 permit for passenger vehicles, which "
     "allows testing of its GXR robotaxi and has started the mapping of the Madrid region; with SBB and Swiss Transit "
     "Lab it has opened a public robotaxi service in the Canton of Zurich, its Robobus at Zurich Airport runs with no "
     "safety operator aboard, and its first robotaxis are road-testing in Slovakia [P]. Baidu's Apollo Go widened its "
     "fully driverless commercial service area in Dubai and doubled its fleet there in Q3 2026, continued road testing "
     "in London with Uber and Lyft and fully driverless testing on Hong Kong's Airport Island, and was in 30 cities in "
     "Oct 2026 [P]; §F7 compares its mileage with Waymo's.\n"),
    # ---- §E1: Waymo row
    ("**271.3 M cumulative rider-only miles (to Jun 2026; still the latest Safety Hub figure in late Sep 2026)** [P]; "
     "more than 4,000 vehicles",
     "**271.3 M cumulative rider-only miles (to Jun 2026; still the latest Safety Hub figure on 21 Nov 2026)** [P], and "
     "more than 300 M fully autonomous miles by Alphabet's Q3 call of 28 Oct 2026 [P]; more than 4,000 vehicles"),
    # ---- §F7 Call 1: Waymo bullet
    ("- **Waymo** alone drives about 4 M+ miles a week, roughly 200 M a year ($4\\ {\\rm M}\\times52\\approx208$ M), "
     "and is growing. Baidu, Pony, WeRide and Zoox add to that.\n",
     "- **Waymo** alone drives about 4 M+ miles a week [P, Waymo, 24 Jun 2026], roughly 200 M a year "
     "($4\\ {\\rm M}\\times52\\approx208$ M), and is growing. Baidu, Pony, WeRide, Zoox and others add to that; the "
     "comparison after this call sets nine other fleets' published mileage beside Waymo's.\n"),
    # ---- §F7 Call 1: Tesla bullet
    ("- **Tesla** had about 1 M cumulative unsupervised miles (miles with no safety driver or monitor aboard) by Sep "
     "2026. A 10× annual growth scenario is **not sufficient by itself** to project 2028 annual miles from that "
     "*cumulative* figure.",
     "- **Tesla** had nearly 2 M cumulative unsupervised miles (miles with nobody in the driver's seat, §E1) by 30 Sep "
     "2026, eight times its end-June total [P, Q3 update]. That is about 0.13 M miles a week in Q3, or about 7 M a "
     "year (derived after this call). A 10× annual growth scenario is **not sufficient by itself** to project 2028 "
     "annual miles from a *cumulative* figure."),
    # ---- §F7: the comparison block, table and Figure F7.1, after Call 1
    ("about 2.7–4.3 times Waymo's current ≈208 M a year [E].\n\n**Call 2: Tesla operates thousands",
     "about 2.7–4.3 times Waymo's current ≈208 M a year [E].\n\n" + MILES_BLOCK + "\n\n**Call 2: Tesla operates "
     "thousands"),
    # ---- §F7 Call 2: the RAND bullet
    ("Tesla's unsupervised mileage is two orders of magnitude short (about $10^{6}$ cumulative miles against the "
     "$10^{8}$ needed, a factor of 100), and crash narratives were redacted until May 2026.",
     "Tesla's unsupervised mileage is far short (nearly $2\\times10^{6}$ cumulative miles by 30 Sep 2026 against the "
     "$10^{8}$ needed, a factor of about 50), and crash narratives were redacted until May 2026."),
    # ---- §E2a: Arbe under the chips bullet
    ("Bosch is ramping an in-house radar chipset, and Arbe and Mobileye are developing high-end imaging chipsets. No "
     "percentage shares are public.\n",
     "Bosch is ramping an in-house radar chipset, and Arbe and Mobileye are developing high-end imaging chipsets. No "
     "percentage shares are public.\n"
     "  - **Arbe's first series programme:** one of the world's largest carmaker groups, which Arbe does not name, "
     "chose HiRain's imaging radar built on Arbe's chipset for an L3 passenger-car programme across several of the "
     "group's brands in China, with series deliveries from Q4 2027 [P]. Arbe is also selling radars for defence: an "
     "unnamed integrator picked it for three projects, initial orders have shipped, and it has launched a counter-drone "
     "radar, Alerion [P].\n"
     "  - **Arbe's revenue is still small:** \\$0.75 M in Q3 2026, and it cut its 2026 guidance to \\$2.3–3.0 M after "
     "deliveries for two integration projects moved into 2027 [P]. Its \\$48.0 M of cash and bank deposits on 30 Sep "
     "2026, which include \\$13.8 M net from a \\$15 M share sale in September, would last about six quarters at Q3's "
     "\\$7.77 M of operating cash use ($48.0/7.77\\approx6.2$), without counting the \\$24.3 M of convertible bonds it "
     "lists as current liabilities [P/E].\n"),
    # ---- §E2a: Sources line
    ("https://www.arenaev.com/2026_xiaomi_su7_arrives_with_lidar_as_a_standard_feature_and_upgraded_chassis-news-"
     "5712.php\n",
     "https://www.arenaev.com/2026_xiaomi_su7_arrives_with_lidar_as_a_standard_feature_and_upgraded_chassis-news-"
     "5712.php ; " + ARBE + " (Arbe Q3 2026 results)\n"),
    # ---- Appendix 1: undisclosed suppliers and sensor counts
    ("Hesai's Mercedes L3 win is a different programme.\n\n**Sensor and chip specifications**",
     "Hesai's Mercedes L3 win is a different programme.\n"
     "- **HiRain–Arbe L3 imaging radar (§E2a):** Arbe names neither the carmaker group nor its brands [P]. Unknown: the "
     "number of these radars per car, whether the programme also carries lidar, and whether Arbe will need new money "
     "before series deliveries begin in Q4 2027.\n\n**Sensor and chip specifications**"),
    # ---- Appendix 1: contested or second-hand figures
    ("The number matters for §F7's calls on Tesla's fleet.\n",
     "The number matters for §F7's calls on Tesla's fleet.\n"
     "- **Robotaxi mileage (§F7).** The operators count different things. Baidu's latest driverless total is from 18 Aug "
     "2026 and its Q3 kilometres are not split; Pony.ai gives cumulative totals without a quarterly figure; WeRide's "
     "55 M km cover all its L4 products, and neither it nor Motional nor May Mobility separates driverless from "
     "supervised driving; Zoox's totals are rounded statements to the press [P/T]. DiDi, Hello, CaoCao and Momenta's "
     "robotaxi unit, and Avride, Mobileye, Wayve and Nuro, had published no current robotaxi mileage in the sources "
     "checked [U]. Waymo's Safety Hub still ended at June 2026 on 21 Nov 2026, so Waymo's Q3 rate is unknown. §F7's "
     "weekly rates, and the lidar-based share built on them, are estimates [E].\n"),
    # ---- Appendix 2: robotaxi and trucks
    ("- Pony.ai and Toyota, fully driverless commercial service with the bZ4X robotaxi in Guangzhou (16 Nov 2026): "
     "https://www.prnewswire.com/apac/news-releases/ponyai-and-toyota-launch-fully-driverless-commercial-services-"
     "with-gen-7-bz4x-robotaxi-302939914.html\n",
     "- Pony.ai and Toyota, fully driverless commercial service with the bZ4X robotaxi in Guangzhou (16 Nov 2026): "
     "https://www.prnewswire.com/apac/news-releases/ponyai-and-toyota-launch-fully-driverless-commercial-services-"
     "with-gen-7-bz4x-robotaxi-302939914.html\n"
     "- WeRide Q3 2026 results (6-K of 20 Nov 2026, Exhibit 99.1; Middle East and global fleets, Spain, Zurich and "
     "Slovakia, robotaxi revenue): " + WERIDE + "\n"
     "- Baidu Q3 2026 results (6-K of 16 Nov 2026, Exhibit 99.1; Apollo Go cities, Dubai, London and Hong Kong, "
     "autonomous kilometres): " + BAIDU + "\n"),
    # ---- Appendix 2: camera-only vs multimodal (mileage)
    ("- Tesla 1 M unsupervised miles: https://electrek.co/2026/09/03/tesla-announces-1-million-unsupervised-miles-"
     "driven-by-robotaxi/\n",
     "- Tesla 1 M unsupervised miles: https://electrek.co/2026/09/03/tesla-announces-1-million-unsupervised-miles-"
     "driven-by-robotaxi/\n"
     "- Waymo, safety data through March 2026 and weekly miles (24 Jun 2026): " + WAYMO_BLOG + "\n"
     "- Alphabet Q3 2026 earnings call, CEO remarks (Waymo above 300 M fully autonomous miles, 28 Oct 2026): "
     + ALPHABET + "\n"
     "- Baidu Q4 2025 results (6-K of 26 Feb 2026, Exhibit 99.1; Apollo Go autonomous and fully driverless kilometres): "
     + BAIDU_Q4_2025 + "\n"
     "- Baidu Q2 2026 results (6-K of 18 Aug 2026, Exhibit 99.1; Apollo Go autonomous and fully driverless kilometres): "
     + BAIDU_Q2_2026 + "\n"
     "- Pony.ai and Verne, fully driverless test rides in Zagreb, with Pony.ai's cumulative and driverless kilometres "
     "(PR Newswire, 10 Sep 2026): " + PONY_VERNE + "\n"
     "- WeRide products page, total L4 kilometres on public roads (read 21 Nov 2026): " + WERIDE_SITE + "\n"
     "- Zoox, close to 2 M autonomous miles (TechCrunch, 24 Mar 2026): " + ZOOX_TC + "\n"
     "- Zoox, 3 M miles (Axios, 12 Aug 2026): " + ZOOX_AXIOS + "\n"
     "- Motional, Voluntary Safety Self-Assessment 2026, section 2.2 (autonomous miles): " + MOTIONAL_VSSA + "\n"
     "- May Mobility, autonomous rides and miles (PR Newswire, 12 Nov 2026): " + MAY + "\n"
     "- GM Authority, Cruise passes 4 M driverless miles (14 Aug 2023): " + CRUISE + "\n"),
    # ---- Appendix 2: camera-only vs multimodal (radar)
    ("- Zhang *et al.*, Dual Radar dataset, *Sci. Data* 12, 439 (2025), Tables 2 and 4 (open access): "
     "https://pmc.ncbi.nlm.nih.gov/articles/PMC11907064/\n",
     "- Zhang *et al.*, Dual Radar dataset, *Sci. Data* 12, 439 (2025), Tables 2 and 4 (open access): "
     "https://pmc.ncbi.nlm.nih.gov/articles/PMC11907064/\n"
     "- Arbe Q3 2026 results (6-K of 19 Nov 2026, Exhibit 99.1; HiRain L3 programme, defence, revenue, guidance and "
     "cash): " + ARBE + "\n"),
]

new = text
for old, rep in EDITS:
    n = new.count(old)
    assert n == 1, f"anchor found {n} times: {old[:90]!r}"
    new = new.replace(old, rep, 1)
assert "\r" not in new
print(f"{len(EDITS)} edits; sha256 before {sha[:12]}, after {hashlib.sha256(new.encode('utf-8')).hexdigest()[:12]}")
if "--write" in sys.argv[3:]:
    report.write_bytes(new.encode("utf-8"))
    print("written")
