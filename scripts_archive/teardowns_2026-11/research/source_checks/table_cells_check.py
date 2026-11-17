"""Convert one section of the report to HTML with pandoc and print, for each table, the number of header cells and
the cell count of every body row, so that a row with a stray or missing cell shows up.

Usage: table_cells_check.py <report.md> <heading start, e.g. '## C3d.'> <pandoc exe>
"""
import subprocess
import sys

from bs4 import BeautifulSoup

md = open(sys.argv[1], encoding="utf-8").read()
start = md.index("\n" + sys.argv[2]) + 1
end = md.index("\n## ", start + 5)
section = md[start:end]
html = subprocess.run([sys.argv[3], "-f", "markdown", "-t", "html"], input=section.encode("utf-8"),
                      capture_output=True, check=True).stdout.decode("utf-8")
soup = BeautifulSoup(html, "html.parser")
for i, table in enumerate(soup.find_all("table"), 1):
    head = len(table.find("thead").find_all("th")) if table.find("thead") else 0
    rows = [len(tr.find_all("td")) for tr in table.find("tbody").find_all("tr")]
    bad = [r for r in rows if r != head]
    print(f"table {i}: {head} header cells, {len(rows)} rows, row cell counts {sorted(set(rows))}, mismatched {len(bad)}")
print("images:", [img.get("src") for img in soup.find_all("img")])
print("links:", len(soup.find_all("a")))
