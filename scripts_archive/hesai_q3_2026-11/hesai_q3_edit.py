"""Bring Hesai's colour-ETX status and design wins up to its Q3 2026 results (10 Nov 2026).

§C5b: the Hesai row of the products table and a new passage "Where the colour ETX stands" (KargoBot's exclusive
design win, May; the Picasso SoC ready for production and the colour ETX in customer validation with RFI/RFQ, Aug;
still in customer validation on the Q3 call, and the JD.com colour-lidar partnership, Nov; Great Wall's ETX
nomination, Jul; the five ET-series main-lidar wins with an order book above 1 million units, Q3), plus sources.
§B2 note 5 (Mercedes): the Q3 call's statement that development and validation follow Mercedes' timeline.
§C3 route table, Hesai row: Jan-Sep 2026 shipments, the September 2026 share and the ET-series wins.
Appendix 1: the Picasso item (status as of the Q3 call; colour use of the ET-series wins not stated) and the GM
item (Cadillac among the ET-series wins, market not named). Appendix 2: the Q3 results and call transcript.
No display equations are added, so no equation numbers change.

Usage: hesai_q3_edit.py <report.md> <expected sha256 prefix> [--write]
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

Q1 = "https://www.sec.gov/Archives/edgar/data/0001861737/000110465926063803/tm2615071d1_ex99-1.htm"
Q2 = "https://www.sec.gov/Archives/edgar/data/0001861737/000110465926098050/tm2623467d1_ex99-1.htm"
Q3 = ("https://www.globenewswire.com/news-release/2026/11/10/3399191/0/en/"
      "hesai-group-reports-third-quarter-2026-unaudited-financial-results.html")
CALL = "https://www.benzinga.com/news/26/11/63086544/hesai-gr-q3-2026-earnings-call-transcript"
GW = "https://www.ithome.com/0/984/269.htm"

STANDS = (
    "\n\n**Where the colour ETX stands.** Hesai's quarterly results trace its progress [P]:\n"
    "- *Q1 results (May 2026).* KargoBot gave Hesai an exclusive design win for its Space 2.0 transport robots, "
    "which run on commercial vehicles: the first production use of the colour 4,320-channel ETX, as primary lidar.\n"
    "- *Q2 results (Aug 2026).* The Picasso SoC was ready for start of production, and the colour ETX was in "
    "customer validation, moving into requests for information and for quotation with robotaxi operators and global "
    "carmakers.\n"
    "- *Q3 results (10 Nov 2026).* On the call Hesai still described the Picasso-equipped ET series as in customer "
    "validation, with talks progressing toward potential programmes [T, call transcript]. The release also announced "
    "a partnership with JD.com to use Hesai's colour lidar in JD's robot fleet; JD plans to deploy more than 4 million "
    "robots, robovans and other machines over five years, a plan of JD's rather than an order to Hesai [E].\n"
    "\n"
    "The car wins name the ETX or the ET series without saying whether the colour channels are used. Great Wall "
    "nominated the over-1,000-line ETX for a new model, with production from the end of 2026 (Jul 2026) [P]. By Q3, "
    "five carmakers had chosen the ET series as main lidar, with an order book above 1 million units: a top European "
    "carmaker, Cadillac, Geely, Great Wall and a leading electric-car maker [P]. Hesai's in-cabin lidar already "
    "equips the China-built Cadillac VISTIQ (§B6), so the Cadillac win may be a programme of GM's Chinese joint "
    "venture [E]."
)

PAIRS = [
    # §C5b products table, Hesai row
    ("| Mass production planned for H2 2026; the ETX was in customer validation in Aug 2026 [P] |",
     "| One production win, KargoBot's transport robots (May 2026) [P]; still in customer validation with robotaxi "
     "operators and global carmakers in Nov 2026 [P/T] |"),
    # §C5b, after the Hesai paragraph
    ("Hesai has published no colour SNR, dynamic range or colour accuracy.",
     "Hesai has published no colour SNR, dynamic range or colour accuracy." + STANDS),
    # §C5b sources
    ("https://en.wikipedia.org/wiki/Lux (illuminance table)",
     f"https://en.wikipedia.org/wiki/Lux (illuminance table) ; {Q1} (Hesai Q1 2026 results) ; {Q2} (Hesai Q2 2026 "
     f"results) ; {Q3} (Hesai Q3 2026 results) ; {CALL} (Hesai Q3 2026 call transcript) ; {GW} (the ETX's Great Wall "
     "nomination)"),
    # §B2 note 5, Mercedes
    ("Reuters (Mar 2025) reported an exclusive multi-year deal through 2030.",
     "Reuters (Mar 2025) reported an exclusive multi-year deal through 2030. On its Q3 2026 call (10 Nov) Hesai said "
     "the Mercedes programmes remain on track, with development and validation following Mercedes' timeline "
     f"[T, [call transcript]({CALL})]."),
    # §C3 route table, Hesai row
    ("| 1.62 M in 2025; ATX >1 M delivered, >6 M backlog; Mercedes L3; VW China JVs; Toyota JVs; NVIDIA Hyperion 10 |",
     "| 1.62 M in 2025 and 1.83 M in Jan–Sep 2026; 43% of China's long-range ADAS lidar in Sep 2026 (Gasgoo) [P]; "
     "ATX >1 M delivered, >6 M backlog; ET series chosen by five carmakers, >1 M units (Q3 2026) [P]; Mercedes L3; "
     "VW China JVs; Toyota JVs; NVIDIA Hyperion 10 |"),
    # Appendix 1, GM
    ("whether flush-mounted units also exist cannot be judged from the images.",
     "whether flush-mounted units also exist cannot be judged from the images. Hesai's Q3 2026 results list Cadillac "
     "among the five carmakers that chose its ET series as main lidar, without naming the market [P]; Hesai's in-cabin "
     "lidar already equips the China-built Cadillac VISTIQ (§B6), so the win may belong to GM's Chinese joint venture "
     "and does not identify the US supplier [E]."),
    # Appendix 1, Picasso: status
    ("by Aug 2026 the Picasso-equipped ETX was still in customer validation [P].",
     "on its Q3 2026 call (10 Nov 2026) Hesai still described the Picasso-equipped ET series as in customer validation, "
     "with one production win, KargoBot's transport robots [P/T]."),
    # Appendix 1, Picasso: colour use of the car wins
    ("nor is whether its depth pixels range through colour filters, which would cost range in sunlight (§C5b).",
     "nor is whether its depth pixels range through colour filters, which would cost range in sunlight (§C5b). Whether "
     "the five carmakers that had chosen the ET series by Q3 2026 use its colour channels is not stated either (§C5b)."),
    # Appendix 2
    ("- Hesai–Mercedes L3: https://www.hesaitech.com/hesai-announced-as-strategic-lidar-partner-and-confirmed-supplier-"
     "for-mercedes-benz-l3-enabled-models/",
     "- Hesai–Mercedes L3: https://www.hesaitech.com/hesai-announced-as-strategic-lidar-partner-and-confirmed-supplier-"
     f"for-mercedes-benz-l3-enabled-models/\n- Hesai Q3 2026 results: {Q3}\n- Hesai Q3 2026 call transcript "
     f"(Benzinga): {CALL}"),
]

new = text
for old, rep in PAIRS:
    n = new.count(old)
    assert n == 1, f"anchor found {n} times: {old[:80]!r}"
    new = new.replace(old, rep, 1)
assert "\r" not in new
print(f"{len(PAIRS)} replacements; sha256 before {sha[:12]}, after {hashlib.sha256(new.encode('utf-8')).hexdigest()[:12]}")
if "--write" in sys.argv[3:]:
    report.write_bytes(new.encode("utf-8"))
    print("written")
else:
    print("check only (add --write to apply)")
