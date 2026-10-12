"""Grep the downloaded source pages for the vendor claims used in section A7, printing context for each."""
import html
import re
import sys
from pathlib import Path

import pymupdf

sys.stdout.reconfigure(encoding="utf-8")
BASE = Path(__file__).resolve().parent.parent
LL = BASE / "agents_lowlight"
SP = BASE / "agents_spadimaging"


def text_of(p: Path) -> str:
    if p.suffix.lower() == ".pdf":
        return re.sub(r"\s+", " ", " ".join(pg.get_text() for pg in pymupdf.open(p)))
    s = p.read_text(encoding="utf-8", errors="replace")
    if p.suffix.lower() in (".html", ".htm", ".xml"):
        s = re.sub(r"<script.*?</script>|<style.*?</style>", " ", s, flags=re.S)
        s = html.unescape(re.sub(r"<[^>]+>", " ", s))
    return re.sub(r"\s+", " ", s)


CHECKS = [
    (LL / "sony_security_tech.html", [r"2,?000 ?mV", r"706", r"F5\.6"]),
    (LL / "hik_darkfighters.html", [r"0\.0003", r"F1\.0"]),
    (LL / "sony_IMX490_flyer.pdf", [r"120 ?dB", r"AEC-Q100", r"Grade", r"LED flicker|LFM"]),
    (LL / "ovt_OX08B40-PB-v1.1-WEB.pdf", [r"140 ?dB", r"LFM|flicker"]),
    (LL / "ovt_nyxel.html", [r"850 ?nm", r"940 ?nm", r"thick", r"textur|scatter", r"DTI|trench"]),
    (LL / "eav_nyxel2.html", [r"50 ?%|50 percent", r"70 ?%|70 percent", r"2\.9"]),
    (LL / "trieye_news.html", [r"Porsche", r"Denso", r"Hitachi"]),
    (LL / "trieye_sedar.html", [r"1375|1,375", r"Coherent"]),
    (LL / "ham_V7090U-71.html", [r"370", r"920", r"30 ?%", r"4 ?[x×] ?10|40000|40 000"]),
    (SP / "canonjp_ms500_spec.txt", [r"0\.001", r"23\.7", r"2\.2 ?kg|約2\.2"]),
    (SP / "canonjp_ms510_spec.txt", [r"0\.0006", r"84"]),
    (SP / "canon_20250612_en.html", [r"75", r"156", r"120 ?m|120 meters|120 metres", r"0\.1 ?lux|0\.1 lx", r"mass production"]),
    (SP / "canon_tech_spad.txt", [r"100 ?%", r"fill factor", r"charge focusing"]),
    (SP / "polarisic_news_252.txt", [r"PCM7200", r"0\.001", r"1000|1,000", r"150 ?dB", r"8 ?μm|8μm|8 µm"]),
    (SP / "ubi_products_evaluation.txt", [r"0\.05", r"160", r"1314|1,314"]),
    (SP / "ubi_products_toolkit_spad.txt", [r"0\.05", r"140"]),
    (SP / "as_session_christmann.txt", [r"Cameras That Count", r"24", r"Christmann"]),
    (SP / "autosens_blog_cutting-edge-technologies-on-display_.txt", [r"Ubicept", r"AUMOVIO|Aumovio", r"Far Sensing"]),
    (SP / "scaling_law_PMC8156442.txt", [r"fill factor", r"10 ?µm|10 μm"]),
    (SP / "pi_about_.txt", [r"ZEISS|Zeiss"]),
    (SP / "pi_spad-alpha_.txt", [r"1024|1,024", r"16 ?µm|16 μm|16µm"]),
]

for path, pats in CHECKS:
    if not path.exists():
        print(f"== {path.name}: MISSING")
        continue
    t = text_of(path)
    print(f"== {path.name} ({len(t)} chars)")
    for pat in pats:
        ms = list(re.finditer(pat, t))
        if not ms:
            print(f"   [{pat}] NOT FOUND")
            continue
        m = ms[0]
        print(f"   [{pat}] x{len(ms)}: ...{t[max(0, m.start() - 150):m.end() + 150]}...")
