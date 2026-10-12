"""Download and extract the export-control texts behind the thermal-camera answer of 2026-10-02.

Sources: eCFR (Title 15, EAR) as of a fixed date, plus China's MOFCOM drone-payload notices.
Writes raw downloads and plain-text extracts to OUT (default ./export_controls_data).
Usage: python fetch_thermal_export_rules.py [out_dir] [ecfr_date]
"""
import html
import re
import subprocess
import sys
from pathlib import Path

from lxml import etree

OUT = Path(sys.argv[1] if len(sys.argv) > 1 else "export_controls_data")
DATE = sys.argv[2] if len(sys.argv) > 2 else "2026-09-24"
OUT.mkdir(parents=True, exist_ok=True)
ECFR = "https://www.ecfr.gov/api/versioner/v1/full/{date}/title-15.xml?part={part}"
MOFCOM = {
    "mofcom_2023_27": "https://www.mofcom.gov.cn/zcfb/dwmygl/art/2023/art_5df14ac418e94c3da748e9563364da3a.html",
    "mofcom_2024_31": "https://www.mofcom.gov.cn/zwgk/zcfb/art/2024/art_db6e21907d69404fb473ddb0b248d3d7.html",
    "mofcom_2024_31_commentary": "http://exportcontrol.mofcom.gov.cn/article/zjsj/202408/1025.html",
}


def fetch(url, path):
    # curl handles the compressed eCFR responses; no identifying headers are sent beyond a generic user agent.
    if not path.exists():
        subprocess.run(["curl", "-s", "-L", "--compressed", "-A", "Mozilla/5.0", "-o", str(path), url], check=True)
    return path


def flat(el):
    return " ".join("".join(el.itertext()).split())


def section(root, n):
    return "\n".join(flat(p) for p in root.xpath(f'//DIV8[@N="{n}"]')[0].iter("P"))


def eccn(text, code):
    # An entry runs from its own header line to the next ECCN header line ("6A004 Optical equipment ...").
    i = text.find(f"\n{code} ")
    m = re.compile(r"\n\d[A-E]\d{3} [A-Z“\"']").search(text, i + 1)
    return text[i + 1:m.start() if m else None]


parts = {p: etree.fromstring(fetch(ECFR.format(date=DATE, part=p), OUT / f"p{p}.xml").read_bytes())
         for p in (734, 738, 740, 742, 743, 744, 746, 774)}

# Commerce Control List entries (Supplement No. 1 to Part 774), as line-broken text.
# Entry headers sit in FP-2, item paragraphs in P/FP/FP-1, notes in HED, licence tables in TD/TH.
CCL_TAGS = ("P", "FP", "FP-1", "FP-2", "HED", "HD1", "HD2", "TD", "TH")
ccl = "\n".join(" ".join("".join(e.itertext()).split()) for e in parts[774].iter(*CCL_TAGS))
(OUT / "p774.txt").write_text(ccl, encoding="utf-8")
for code in ("6A002", "6A003", "6A993"):
    (OUT / f"e{code}.txt").write_text(eccn(ccl, code), encoding="utf-8")

# EAR sections quoted in the answer.
for sec, root in (("742.6", 742), ("743.3", 743), ("744.9", 744), ("744.21", 744), ("746.8", 746),
                  ("740.20", 740), ("734.4", 734)):
    (OUT / f"s{sec.replace('.', '_')}.txt").write_text(section(parts[root], sec), encoding="utf-8")


def rows(table):
    for tr in table.xpath(".//TR"):
        cells = []
        for c in tr:
            if c.tag in ("TD", "TH"):
                cells += [flat(c)] * int(c.get("colspan", "1"))
        yield cells


# Country Groups A:1, A:5, A:6 (Supplement No. 1 to Part 740).
groups = {"A:1": [], "A:5": [], "A:6": []}
sup740 = parts[740].xpath('//DIV9[@N="Supplement No. 1 to Part 740"]')[0]
for c in list(rows(sup740.xpath(".//TABLE")[0]))[1:]:
    if len(c) >= 7 and len(c[0]) < 40:
        for k, idx in (("A:1", 1), ("A:5", 5), ("A:6", 6)):
            if c[idx]:
                groups[k].append(c[0])
with open(OUT / "country_groups.txt", "w", encoding="utf-8") as f:
    for k, v in groups.items():
        f.write(f"{k} ({len(v)}): {', '.join(v)}\n")

# Commerce Country Chart columns NS2, RS1, RS2 (Supplement No. 1 to Part 738), plus footnote 7 on India.
sup738 = parts[738].xpath('//DIV9[contains(@N,"Supplement No. 1 to Part 738")]')[0]
chart = list(rows(sup738.xpath(".//TABLE")[0]))
cols = chart[1]
iNS2, iRS1, iRS2 = cols.index("NS 2") + 1, cols.index("RS 1") + 1, cols.index("RS 2") + 1
with open(OUT / "country_chart_ns2_rs1_rs2.txt", "w", encoding="utf-8") as f:
    for c in chart[2:]:
        if len(c) == 17 and not c[1].startswith("See"):
            f.write(f"{c[0]:<32} NS2={'X' if c[iNS2] else '-'} RS1={'X' if c[iRS1] else '-'} "
                    f"RS2={'X' if c[iRS2] else '-'}\n")
    t = flat(sup738)
    m = re.search(r"7 Note that a license is still required.*?India\.", t)
    f.write("\nFootnote: " + (m.group(0) if m else "(footnote 7 not found)") + "\n")

# MOFCOM notices: plain text.
for name, url in MOFCOM.items():
    raw = fetch(url, OUT / f"{name}.html").read_bytes().decode("utf-8", errors="replace")
    raw = re.sub(r"<script.*?</script>|<style.*?</style>", " ", raw, flags=re.S)
    txt = html.unescape(re.sub(r"<[^>]+>", "\n", raw))
    (OUT / f"{name}.txt").write_text("\n".join(x.strip() for x in txt.splitlines() if x.strip()), encoding="utf-8")

print("wrote", sorted(p.name for p in OUT.iterdir()))
print(open(OUT / "country_groups.txt", encoding="utf-8").read())
