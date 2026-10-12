"""Convert saved HTML files under raw/ to plain text under text/ for reading.

Usage (run from the eic_fund folder):
    python scripts/html2text.py raw/file1.html [raw/file2.html ...]
Scripts, styles and navigation boilerplate are dropped; link targets are kept
inline as [text](href) so that source URLs can be traced.
"""
import sys
from pathlib import Path

from bs4 import BeautifulSoup

OUT = Path("text")
OUT.mkdir(exist_ok=True)


def convert(path: Path) -> Path:
    soup = BeautifulSoup(path.read_bytes(), "html.parser")
    for tag in soup(["script", "style", "noscript", "svg"]):
        tag.decompose()
    for a in soup.find_all("a"):
        href = a.get("href")
        txt = a.get_text(" ", strip=True)
        if href and txt:
            a.replace_with(f"[{txt}]({href})")
    text = soup.get_text("\n", strip=True)
    lines = [ln for ln in text.splitlines() if ln.strip()]
    out = OUT / (path.stem + ".txt")
    out.write_text("\n".join(lines), encoding="utf-8")
    return out


if __name__ == "__main__":
    for p in sys.argv[1:]:
        o = convert(Path(p))
        print(o, o.stat().st_size)
