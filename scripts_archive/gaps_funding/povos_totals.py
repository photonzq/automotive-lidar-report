"""Tabulate the POVOS (POV.OS) joint project from saved Foerderkatalog detail pages.

Reads raw/foekat_detail_19A22010*.html (saved by foekat_search.py with verbund=POVOS)
and prints, for each sub-project still listed in the federal funding catalogue: the
funding code, the federal share in euro, the recipient and the sub-project title. It
then prints the total federal share and the total including the two sub-projects that
the catalogue no longer lists but that a register aggregator recorded from it
(Scantinel Photonics GmbH, EUR 740,474; XKrug GmbH, EUR 230,093).
"""
import glob
import html
import os
import re
import sys

RAW = sys.argv[1] if len(sys.argv) > 1 else "raw"
DELISTED = {"Scantinel Photonics GmbH": 740474.0, "XKrug GmbH": 230093.0}


def main():
    total = 0.0
    for f in sorted(glob.glob(os.path.join(RAW, "foekat_detail_19A22010*.html"))):
        t = open(f, encoding="utf-8").read()
        x = re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", t)))
        amt = float(re.search(r"Anteil des Bundes\)\s*([\d.]+,\d\d)", x).group(1)
                    .replace(".", "").replace(",", "."))
        ze = re.search(r"Förderempfänger/Auftragnehmer (.*?) Ort", x).group(1)
        tv = re.search(r"Teilvorhaben: (.*?) Förder", x).group(1)
        per = re.search(r"Laufzeit (\S+ bis \S+)", x).group(1)
        code = re.search(r"Förderkennzeichen (19A22010\w)", x).group(1)
        total += amt
        print(f"{code} {amt:>14,.2f}  {per}  {ze} | {tv[:80]}")
    print(f"federal share, live records: {total:,.2f}")
    extra = sum(DELISTED.values())
    print(f"plus delisted sub-projects ({', '.join(DELISTED)}): {total + extra:,.2f}")


if __name__ == "__main__":
    main()
