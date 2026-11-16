"""Innoviz's Q3 2026 results (§B3, §C3a, §C3c, §G2, Appendix 2).

Sources, both read in full: the Q3 2026 results release (6-K of 12 Nov 2026, Exhibit 99.1, also on PR Newswire,
11 Nov 2026) and the Q3 operating and financial review (6-K of 12 Nov 2026, Exhibit 99.2). Facts used: Q3 revenue
$12.098 M against $15.278 M, mainly from a customer's delay of NRE revenue expected in 2027; gross loss $1.241 M against
a $2.298 M profit; FY2026 targets cut to $44-46 M of revenue with Perciz (defense and homeland security, launched July
2026) at about 6-7%; realignment in Q4 2026, about 20% of the workforce, about $17.5 M of annualized savings, said to
support the runway into 2028; July 2026 registered direct offering of 66,666,667 shares at $0.45 ($30.0 M gross,
$27.6 M net); liquidity $54.4 M at 30 Sep 2026, expected to last at least 12 months; remaining performance obligations
$17.3 M; Q3 operating cash use $19.707 M; VW and Daimler Truck programmes progressing; first defense orders delivered.

Usage: innoviz_q3_edit.py <report.md> <expected sha256 prefix> [--write]
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

EDITS = [
    # ---- §B3 table row
    (r"| **Innoviz** | 905 nm, MEMS | FY25 revenue \$55.1 M; FY26 guidance \$67–73 M; VW ID. Buzz AD and Daimler "
     r"Truck/Torc programmes; reverse split authorized [P] (note 2) |",
     r"| **Innoviz** | 905 nm, MEMS | FY25 revenue \$55.1 M; Q3 2026 revenue \$12.1 M (−21%), and FY26 guidance cut "
     r"to \$44–46 M from \$67–73 M; about 20% of staff to go; \$54.4 M of liquidity at end-Sep after a \$30 M share "
     r"sale; VW ID. Buzz AD and Daimler Truck/Torc programmes; first defense deliveries under the Perciz brand; reverse "
     r"split authorized [P] (note 2) |"),
    # ---- §B3 note 2
    (r"and the deadline for meeting Nasdaq's minimum bid-price requirement was extended to 22 Mar 2027." + "\n",
     r"and the deadline for meeting Nasdaq's minimum bid-price requirement was extended to 22 Mar 2027. In Q3 2026 "
     r"revenue fell to \$12.1 M from \$15.3 M a year earlier, mainly because a customer moved the timing of its "
     r"programmes and so delayed engineering (NRE) revenue, which Innoviz expects to realize in 2027; the quarter "
     r"ended with a gross loss of \$1.2 M, against a gross profit of \$2.3 M a year earlier [P]. Innoviz cut its 2026 "
     r"targets to \$44–46 M of revenue, with about 6–7% of it from defense and homeland security under the Perciz "
     r"brand launched in July 2026, and announced a realignment in Q4 2026 that cuts about 20% of the workforce for "
     r"about \$17.5 M of annualized savings [P]. In July 2026 it sold 66.7 M new shares at \$0.45 (\$30.0 M gross, "
     r"\$27.6 M net), and it held \$54.4 M of liquidity at 30 Sep 2026, which it expects to last at least 12 months "
     r"and says, with the realignment, supports its runway into 2028; its remaining performance obligations were "
     r"\$17.3 M, mostly to be recognized within 12 months [P]. At the quarter's operating cash use of \$19.7 M, "
     r"\$54.4 M covers $54.4/19.7=2.8$ quarters, or $54.4/(19.7-17.5/4)=3.5$ quarters with the full savings, so "
     r"reaching 2028 also needs receipts such as the delayed NRE, defense orders or further share sales under its "
     r"at-the-market programme [E]." + "\n"),
    # ---- §C3a share-price bullet
    (r"Shareholders authorised a 1:5–1:20 reverse split on 16 Sep 2026; it has not been effected [P].",
     r"Shareholders authorised a 1:5–1:20 reverse split on 16 Sep 2026; it has not been effected [P]. In July 2026 it "
     r"sold 66.7 M new shares at \$0.45 in a registered direct offering (§B3) [P]."),
    # ---- §C3c row
    (r"Share price −98%; Nasdaq bid-price extension to Mar 2027 (§C3a) |",
     r"Share price −98%; Nasdaq bid-price extension to Mar 2027 (§C3a); 2026 revenue guidance cut to \$44–46 M and "
     r"about 20% of staff cut (Nov 2026, §B3) |"),
    # ---- §G2: pressure bullet
    (r"MicroVision about \$1 M per quarter; Innoviz approved a reverse split (merging shares to lift the share price, "
     r"typically to keep a stock-exchange listing).",
     r"MicroVision about \$1 M per quarter; Innoviz cut its 2026 revenue guidance (its own forecast) to \$44–46 M "
     r"from \$67–73 M, below its \$55.1 M of FY25, is cutting about 20% of its staff, and approved a reverse split "
     r"(merging shares to lift the share price, typically to keep a stock-exchange listing)."),
    # ---- §G2: survivors bullet, and a new bullet for the programmes that continue
    (r"Valeo (>€1 B in SCALA orders); Innoviz (guiding, i.e. forecasting, \$67–73 M for 2026); Aeva (Daimler, a "
     r"European OEM L3 programme, and LG Innotek as an investor)." + "\n",
     r"Valeo (>€1 B in SCALA orders); Aeva (Daimler, a European OEM L3 programme, and LG Innotek as an investor)."
     + "\n" +
     r"- **Programmes that continue:** Innoviz's VW ID. Buzz AD and Daimler Truck programmes are progressing, and it "
     r"has begun delivering its first defense orders under the Perciz brand (§B3)." + "\n"),
    # ---- Appendix 2
    ("- Innoviz Q2 2026 (6-K): https://www.sec.gov/Archives/edgar/data/0001835654/000117891326003861/exhibit_99-1.htm\n",
     "- Innoviz Q2 2026 (6-K): https://www.sec.gov/Archives/edgar/data/0001835654/000117891326003861/exhibit_99-1.htm\n"
     "- Innoviz Q3 2026 results (6-K of 12 Nov 2026, Exhibit 99.1): "
     "https://www.sec.gov/Archives/edgar/data/0001835654/000117891326005172/exhibit_99-1.htm\n"
     "- Innoviz Q3 2026 operating and financial review (6-K of 12 Nov 2026, Exhibit 99.2; July 2026 offering, "
     "liquidity, realignment, remaining performance obligations): "
     "https://www.sec.gov/Archives/edgar/data/0001835654/000117891326005176/exhibit_99-2.htm\n"),
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
