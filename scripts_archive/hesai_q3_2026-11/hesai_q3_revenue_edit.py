"""Hesai's Q3 2026 revenue against guidance, and revenue per unit on lidar revenue only (§B1, §B8, §F2, Appendix 2).

- §B1 table, Hesai row: Jan-Sep 2026 shipments, the Q3 revenue shortfall against the August guidance, and the Q3
  lidar revenue per unit with the bound for car lidars.
- §B1 notes: revenue per unit is now the lidar segment's revenue per lidar (Hesai has reported a separate segment for
  actuators and Kosmo since Q2 2026, which total revenue includes): RMB 977.8 M / 729,673 = 1,340 in Q3 against
  815.9 M / 628,275 = 1,299 in Q2. New bullets: car and robot lidars apart (from the call's statement that businesses
  other than car lidar brought in more than half of Q3 revenue: car lidars under RMB 837 each, robotics lidars over
  RMB 4,840), and Hesai's 2026 volume (Q4 guidance at Q3's revenue per unit implies about 2.53-2.64 M for 2026,
  against the 3.0-3.5 M target, which Hesai did not restate).
- §B8 robotics table, Hesai row: Q3 segment revenues and the call's statement.
- §F2 "ASP path": Q3 figures replace the Q2 one.
- Appendix 2: the Investing.com transcript, which confirms the call statement.
No display equations are added.

Usage: hesai_q3_revenue_edit.py <report.md> <expected sha256 prefix> [--write]
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

Q2 = "https://www1.hkexnews.hk/listedco/listconews/sehk/2026/0818/2026081800396.pdf"
Q3 = ("https://www.globenewswire.com/news-release/2026/11/10/3399191/0/en/"
      "hesai-group-reports-third-quarter-2026-unaudited-financial-results.html")
CALL = "https://www.benzinga.com/news/26/11/63086544/hesai-gr-q3-2026-earnings-call-transcript"
CALL2 = ("https://www.investing.com/news/transcripts/"
         "earnings-call-transcript-hesai-posts-record-q3-2026-revenue-as-robotics-gains-traction-93CH-5015371")

OLD_PER_UNIT = (
    r"- **Hesai revenue per unit.** Revenue per unit is quarterly revenue divided by quarterly shipments. In Q2 2026 "
    r"Hesai's net revenues were RMB 860.8 M on 628,275 lidars shipped, so revenue per unit was $860.8\text{ M}/628{,}275"
    r"\approx\text{RMB }1{,}370$ [P, [Q2 2026 results](" + Q2 + r"); E]. At RMB 7.1 per dollar, RMB 1,370 is "
    r"$1{,}370/7.1\approx193$ dollars, i.e. about \$200. For comparison, the 2025 average from this table is RMB 3.03 B "
    r"/ 1,620,406 ≈ RMB 1.87k per unit (§B8 gives ≈\$260 on lidar product revenue alone)."
)

NEW_PER_UNIT = "\n".join([
    r"- **Hesai revenue per unit.** Revenue per unit is quarterly lidar revenue divided by quarterly lidar shipments. "
    r"Since Q2 2026 Hesai has reported its robotic actuation modules and Kosmo data platform as a separate segment, "
    r"which total revenue includes, so the lidar segment's revenue is used here. In Q3 2026 that segment's revenue was "
    r"RMB 977.8 M on 729,673 lidars, so revenue per unit was $977.8\text{ M}/729{,}673\approx\text{RMB }1{,}340$, up "
    r"from $815.9\text{ M}/628{,}275\approx\text{RMB }1{,}299$ in Q2 [P, [Q3 2026 results](" + Q3 + r"), "
    r"[Q2 2026 results](" + Q2 + r"); E]. At the RMB 6.7045 per dollar that the Q3 release uses, RMB 1,340 is "
    r"$1{,}340/6.7045\approx200$ dollars. For comparison, the 2025 average from this table is RMB 3.03 B / 1,620,406 "
    r"≈ RMB 1.87k per unit (§B8 gives ≈\$260 on lidar product revenue alone).",
    r"- **Car and robot lidars apart.** The average mixes very different products. On the Q3 call Hesai said that "
    r"businesses other than car lidar brought in more than half of total revenue [T, [call transcript](" + CALL + r")]. "
    r"Car lidars therefore earned less than $0.5\times\text{RMB }1{,}068.3\text{ M}\approx\text{RMB }534.2\text{ M}$ on "
    r"638,055 units, under $534.2\text{ M}/638{,}055\approx\text{RMB }837$ (about \$125) each. Robotics lidars earned "
    r"more than $534.2-90.5=\text{RMB }443.7\text{ M}$, where RMB 90.5 M is the non-lidar segment's revenue, on 91,618 "
    r"units: over $443.7\text{ M}/91{,}618\approx\text{RMB }4{,}840$ (about \$720) each [E].",
    r"- **Hesai's 2026 volume.** Q3 revenue of RMB 1,068.3 M fell short of the RMB 1,100–1,150 M that Hesai had guided "
    r"in August; on the call it blamed weaker car demand, with several carmakers, some of them its customers, lowering "
    r"their 2026 sales targets [P/T]. Hesai did not restate its 2026 shipment target of 3.0–3.5 M, and its Q4 guidance "
    r"implies less [E]. The non-lidar segment, guided at RMB 200–300 M for 2026 after RMB 135.4 M in Q2 and Q3 "
    r"(44.9 + 90.5, none in Q1), would bring RMB 64.6–164.6 M in Q4. The Q4 revenue guidance of RMB 1,100–1,150 M then "
    r"leaves $1{,}100-164.6=935$ to $1{,}150-64.6=1{,}085$ M for lidar. At Q3's RMB 1,340 per unit that is "
    r"0.70–0.81 M lidars, so 2026 would end near $1.83+0.70=2.53$ to $1.83+0.81=2.64$ M.",
])

PAIRS = [
    # §B1 table, Hesai row
    (r"2026 target 3.0–3.5 M. Q2 2026 revenue per unit about RMB 1.37k (about \$200) [E] |",
     r"2026 target 3.0–3.5 M; 1.83 M shipped in Jan–Sep, and Q3 revenue of RMB 1,068 M fell short of the "
     r"RMB 1,100–1,150 M guided [P]. Q3 2026 lidar revenue per unit about RMB 1.34k (about \$200), under RMB 0.84k "
     r"(about \$125) for car lidars [E] |"),
    # §B1 notes
    (OLD_PER_UNIT, NEW_PER_UNIT),
    # §B8 robotics table, Hesai row
    (r"(ADAS and robotics combined, RMB 815.9 M in Q2) and a Strategic Growth Initiatives segment (actuators and the "
     r"Kosmo spatial-data platform, RMB 44.9 M) [P].",
     r"(ADAS and robotics combined, RMB 815.9 M in Q2 and 977.8 M in Q3) and a Strategic Growth Initiatives segment "
     r"(actuators and the Kosmo spatial-data platform, RMB 44.9 M and 90.5 M) [P]. In Q3 2026 Hesai shipped 91,618 "
     r"robotics lidars and said that robotics lidar, Kosmo and its actuators together brought in more than half of total "
     r"revenue (§B1) [P/T]."),
    # §F2 ASP path
    (r"fell from about ¥4.1k (Hesai, 2024) to about ¥1.37k (Q2 2026).",
     r"fell from about ¥4.1k (Hesai, 2024) to about ¥1.34k (Q3 2026, lidar revenue only), and Hesai's car lidars alone "
     r"earned under about ¥0.84k each in Q3 2026 (§B1)."),
    (r"The Q2 2026 figure is the §B1 estimate.",
     r"The Q3 2026 figures are the §B1 estimates."),
    # Appendix 2
    ("- Hesai Q3 2026 call transcript (Benzinga): " + CALL,
     "- Hesai Q3 2026 call transcript (Benzinga): " + CALL + "\n- Hesai Q3 2026 call transcript (Investing.com): "
     + CALL2),
]

new = text
for old, rep in PAIRS:
    n = new.count(old)
    assert n == 1, f"anchor found {n} times: {old[:80]!r}"
    new = new.replace(old, rep, 1)
assert "\r" not in new and "\t" not in new
print(f"{len(PAIRS)} replacements; sha256 before {sha[:12]}, after {hashlib.sha256(new.encode('utf-8')).hexdigest()[:12]}")
if "--write" in sys.argv[3:]:
    report.write_bytes(new.encode("utf-8"))
    print("written")
else:
    print("check only (add --write to apply)")
