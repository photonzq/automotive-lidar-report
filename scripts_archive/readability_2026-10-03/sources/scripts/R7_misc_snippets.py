"""R7 helper snippets run inline during the research, collected here for the archive.

  python R7_misc_snippets.py clip <file.pdf> <page_1based> <x0> <y0> <x1> <y1> <dpi> <out.png>
      Render a rectangle of one page (PDF points) at high dpi, to read small table text.
  python R7_misc_snippets.py text <saved.html> <regex>
      Strip tags from a saved web page and print the lines matching a regex
      (used for the KrASIA interview, The Robot Report and Huawei pages).
  python R7_misc_snippets.py utc2local
      Convert the times Tesla filed in the SGO records listed in the report's §E12.2 table
      from UTC to local civil time, over every day of the recorded month (US DST rules).
Pages were saved with curl and a generic browser User-Agent; no e-mail or credentials.
"""
import calendar
import html
import re
import sys
from datetime import datetime, timedelta


def clip(pdf, page, x0, y0, x1, y1, dpi, out):
    import pymupdf
    d = pymupdf.open(pdf)
    d[page - 1].get_pixmap(dpi=dpi, clip=pymupdf.Rect(x0, y0, x1, y1)).save(out)
    print(out)


def text(path, pattern):
    t = open(path, encoding="utf-8", errors="replace").read()
    txt = html.unescape(re.sub(r"<[^>]+>", "\n", t))
    rg = re.compile(pattern, re.I)
    seen = set()
    for line in (s.strip() for s in txt.split("\n")):
        if line and rg.search(line) and line not in seen and len(line) < 900:
            seen.add(line)
            print("-", line)


def _dst(day):
    y = day.year
    mar = [d for d in range(8, 15) if calendar.weekday(y, 3, d) == 6][0]
    nov = [d for d in range(1, 8) if calendar.weekday(y, 11, d) == 6][0]
    return datetime(y, 3, mar, 2) <= day < datetime(y, 11, nov, 2)


ROWS = [  # report id, place, year, month, filed time, standard UTC offset, observes DST
    ("13781-8004", "Rimrock AZ", 2023, 11, "00:03", -7, 0),
    ("13781-7381", "Red Mills VA", 2024, 3, "19:19", -5, 1),
    ("13781-7767", "Collinsville OH", 2024, 5, "10:16", -5, 1),
    ("13781-7964", "Fullerton CA", 2024, 6, "07:03", -8, 1),
    ("13781-8977", "Issaquah WA", 2024, 10, "20:40", -8, 1),
    ("13781-9267", "Stockton CA", 2024, 11, "11:30", -8, 1),
    ("13781-11937", "Barrington IL", 2025, 10, "03:23", -6, 1),
    ("13781-13211", "Sunol CA", 2025, 11, "00:36", -8, 1),
    ("13781-13569", "Seattle WA", 2025, 12, "15:53", -8, 1),
    ("13781-13633", "Kansas City MO", 2026, 1, "14:09", -6, 1),
    ("13781-13693", "Claremore OK", 2026, 1, "15:50", -6, 1),
    ("13781-13788", "Bentonville VA", 2026, 1, "21:49", -5, 1),
]


def utc2local():
    for rid, place, y, m, t, off, obs in ROWS:
        hh, mm = map(int, t.split(":"))
        out = set()
        for d in range(1, calendar.monthrange(y, m)[1] + 1):
            u = datetime(y, m, d, hh, mm)
            lc = u + timedelta(hours=off + (1 if obs and _dst(u) else 0))
            out.add((lc.strftime("%H:%M"), "same day" if lc.day == u.day else "previous day"))
        print(f"{rid:12s} {place:16s} {y}-{m:02d} filed {t} -> local {sorted(out)}")


if __name__ == "__main__":
    c = sys.argv[1]
    if c == "clip":
        a = sys.argv[2:]
        clip(a[0], int(a[1]), *map(float, a[2:6]), int(a[6]), a[7])
    elif c == "text":
        text(sys.argv[2], sys.argv[3])
    elif c == "utc2local":
        utc2local()
