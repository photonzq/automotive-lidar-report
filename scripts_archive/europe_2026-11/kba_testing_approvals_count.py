"""Count the KBA's testing approvals for automated and autonomous driving (StVG § 1i with AFGBV § 16) by level,
validity and holder, from the KBA's published list, and compare the counts with those quoted in §B4b.

The list (English version) is published by the KBA at
https://www.kba.de/EN/Themen_en/Typgenehmigung_en/Autonomes_automatisiertes_Fahren_en/Erprobungsgenehmigung_en/
dl_liste_erprobungsgenehmigungen_en.pdf?__blob=publicationFile ; the counts in §B4b come from the list dated
05.11.2026 (19 pages). Each row is one approval, and each approval covers one vehicle (the KBA's testing FAQ: a
separate application is needed for each vehicle). An approval counts as in force if its limitation date is on or
after the list date. Two rows carry impossible limitation dates in the KBA's own list (32.12.2024 and 31.11.2025);
both are earlier than the list date in any reading, so they count as expired.

Usage: kba_testing_approvals_count.py <list.pdf> [<list date dd.mm.yyyy>]
Needs PyMuPDF (import pymupdf).
"""
import re
import sys
from collections import Counter
from datetime import datetime

import pymupdf

pdf = sys.argv[1]
list_date = datetime.strptime(sys.argv[2] if len(sys.argv) > 2 else "05.11.2026", "%d.%m.%Y")

HEADER = {"Approval Holder", "Approval Number", "Type", "Date of the Approval", "Degree of Automation", "Limitation",
          "Geographical Restriction of the", "Testing Area*"}
lines = []
for page in pymupdf.open(pdf):
    for ln in page.get_text().splitlines():
        s = ln.replace("\xa0", " ").strip()
        if (not s or s in HEADER or s.startswith("Date: ") or s.startswith("List of the granted")
                or s.startswith("AFGBV") or s.startswith("*") or s.startswith("Seite ")):
            continue
        lines.append(s)

rows, holder = [], []
i = 0
while i < len(lines):
    if re.fullmatch(r"EPG\d{5}\*\d{2}", lines[i]):
        kind, granted, level, limit, geo = lines[i + 1:i + 6]
        rows.append({"holder": " ".join(holder), "number": lines[i], "type": kind, "granted": granted,
                     "level": level, "limit": limit, "geo": geo})
        holder = []
        i += 6
    else:
        holder.append(lines[i])
        i += 1
assert not holder, f"unparsed text after the last row: {holder}"


def in_force(row):
    try:
        return datetime.strptime(row["limit"], "%d.%m.%Y") >= list_date
    except ValueError:  # an impossible date in the list (see the docstring)
        return False


level4 = [r for r in rows if r["level"] == "Level 4"]
level3 = [r for r in rows if r["level"] == "Level 3"]
l4_now = [r for r in level4 if in_force(r)]
l3_now = [r for r in level3 if in_force(r)]
l4_now_nationwide = [r for r in l4_now if r["geo"] == "no"]
holders_l4 = Counter(r["holder"] for r in l4_now)
holders_l3 = Counter(r["holder"] for r in l3_now)
zf = sum(n for h, n in holders_l4.items() if h.startswith("ZF "))

CHECKS = [
    ("approvals listed", len(rows), 287),
    ("Level 4 approvals listed", len(level4), 114),
    ("Level 3 approvals listed", len(level3), 173),
    ("Level 4 approvals in force", len(l4_now), 108),
    ("Level 3 approvals in force", len(l3_now), 109),
    ("Level 4 in force without geographic restriction", len(l4_now_nationwide), 87),
    ("Level 4 in force, Volkswagen AG", holders_l4["Volkswagen AG"], 55),
    ("Level 4 in force, ZF (both companies)", zf, 10),
    ("Level 4 in force, HOLON GmbH", holders_l4["HOLON GmbH"], 8),
    ("Level 4 in force, DB Regio Bus Mitte GmbH", holders_l4["DB Regio Bus Mitte GmbH"], 8),
    ("Level 4 in force, MAN Truck & Bus SE", holders_l4["MAN Truck & Bus SE"], 4),
    ("Level 4 in force, Momenta Europe GmbH", holders_l4["Momenta Europe GmbH"], 3),
    ("Level 4 in force, Motor AI GmbH", holders_l4["Motor AI GmbH"], 3),
    ("Level 4 in force, Stadtwerke München GmbH", holders_l4["Stadtwerke München GmbH"], 3),
    ("Level 4 in force, Einride Technologies Germany GmbH", holders_l4["Einride Technologies Germany GmbH"], 1),
    ("Level 3 in force, Mercedes-Benz AG", holders_l3["Mercedes-Benz AG"], 51),
    ("Level 3 in force, Audi AG", holders_l3["Audi AG"], 36),
    ("Level 3 in force, Wayve Technologies (Expansion) Ltd", holders_l3["Wayve Technologies (Expansion) Ltd"], 12),
]
print(f"list date {list_date:%d.%m.%Y}; {len(rows)} rows parsed")
for name, value, quoted in CHECKS:
    print(f"{name:<55} computed {value:>4}   quoted in §B4b {quoted:>4}   {'ok' if value == quoted else 'DIFFERS'}")
print("\nLevel 4 approvals in force, by holder:")
for h, n in holders_l4.most_common():
    print(f"  {n:3d}  {h}")
