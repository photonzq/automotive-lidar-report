"""Update the report's Chinese automotive thermal-camera facts: suppliers per model, Raytron's Horus 640D at 12 um,
Raytron's first 8 um automotive module (2026), Guide Infrared's Xuanyuan IDrive at M-Hero, and the 12 um correction in §F1.
Usage: china_thermal_edit.py <report.md> <expected sha256 prefix> [--write]
Each (old, new) pair must match exactly once and the starting hash must match; writes LF line endings."""
import hashlib
import sys
from pathlib import Path

report, expected = Path(sys.argv[1]), sys.argv[2]
raw = report.read_bytes()
sha = hashlib.sha256(raw).hexdigest()
assert sha.startswith(expected), f"report changed: sha {sha[:12]} != {expected}"
text = raw.decode("utf-8")
assert "\r" not in text

PAIRS = [
    # §A1 table row
    ("| 2025–26 | Fangchengbao Bao 8, Yangwang U8L, Zeekr 9X, M-Hero 817/917, HiPhi HL, Cadillac XT5 (China) | FIR | "
     "Mostly **Raytron** (about 74% China share, Jan–Sep 2025); Zeekr 9X claims the \"world's first thermal AEB\" "
     "(Raytron 640×512) |",
     "| 2025–26 | Fangchengbao Bao 8, Yangwang U8L, Zeekr 9X, M-Hero 817/917, Geely LEVC L380, HiPhi HL, Cadillac XT5 "
     "(China) | FIR | Mostly **Raytron** (about 74% China share, Jan–Sep 2025), which names the Bao 8, the Yangwang U8, "
     "the Zeekr 9X and the L380 among its customers [P]; Zeekr 9X claims the \"world's first thermal AEB\" with "
     "Raytron's Horus 640D module (640×512 at 12 µm) [P]; M-Hero's system comes from Guide Infrared's subsidiary "
     "Xuanyuan IDrive (§A2) [T] |"),
    # §A1 terms
    ("AEB is automatic emergency braking, and 640×512 is the thermal sensor's pixel count.",
     "AEB is automatic emergency braking, 640×512 is the thermal sensor's pixel count, and 12 µm is its pixel pitch "
     "(the centre-to-centre spacing of the pixels)."),
    # §A2 China bullets
    ("- **China:** 19,000 installs in Jan–Sep 2025, **+384.7% year on year** [T].",
     "- **China:** 19,000 installs in Jan–Sep 2025, **+384.7% year on year** [T]. The same source attributes the "
     "growth mainly to the Bao 8, the M-Hero M817 and Geely's LEVC L380 [T]."),
    ("  - Raytron held 73.8% and Xuanyuan IDrive 15.5%.",
     "  - Raytron held 73.8% and Xuanyuan IDrive 15.5%.\n"
     "  - Xuanyuan IDrive (轩辕智驾) is the wholly owned automotive subsidiary of Guide Infrared (高德红外). When "
     "Dongfeng's M-Hero brand launched its first model on 27 Aug 2022, it announced that a thermal system "
     "custom-developed by Xuanyuan IDrive would be standard across its range [T, China Securities Journal, 28 Aug and "
     "5 Sep 2022]. In Aug 2026 Guide said it held design-win notices for passenger-car projects at Geely, M-Hero and "
     "GAC Aion, without naming models or volumes [P, investor Q&A, 3 Aug 2026]."),
    # §A4 Zeekr bullet
    ("The Zeekr 9X uses a Raytron thermal camera (640×512) as an input to automatic emergency braking,",
     "The Zeekr 9X uses Raytron's Horus 640D module, built on a 640×512 detector with 12 µm pixels, as an input to "
     "automatic emergency braking,"),
    # §A4 pitch bullet
    ("(NDAA) [P]. Smaller pixels shrink the lens, and the optics are expensive (§A3, item 6).",
     "(NDAA) [P]. The cameras in Chinese production cars still use 12 µm pixels: the Horus 640D in the Zeekr 9X pairs "
     "a 640 × 512 detector at 12 µm with Raytron's own processing chip, and Raytron showed its first 8 µm automotive "
     "module, the Horus640-EN, at Auto China 2026, contrasting it with \"conventional 12μm and 17μm solutions\" [P]. "
     "Smaller pixels shrink the lens, and the optics are expensive (§A3, item 6)."),
    # §A4 block, floor bullet
    ("(Their Table 1 lists F/1.33 for a 3 µm mid-wave pixel at $F\\lambda/d=2$, where $F=2d/\\lambda$ gives 1.5.)",
     "(Their Table 1 lists F/1.33 for a 3 µm mid-wave pixel at $F\\lambda/d=2$, where $F=2d/\\lambda$ gives 1.5.) "
     "Today's automotive modules, at 12 µm, sit at $F\\lambda/d=0.83$ with an F/1 lens, and Raytron's 8 µm "
     "Horus640-EN moves to 1.25, which the table credits with 1.38 times the range behind the same lens [E]."),
    # §F1
    ("Raytron-class thermal modules (640×512 pixels at an 8 µm pixel pitch) are getting cheaper,",
     "Raytron-class thermal modules (640×512 pixels at 12 µm in today's cars, with Raytron's first 8 µm automotive "
     "module shown in 2026, §A4) are getting cheaper,"),
    # Appendix 1 item
    ("not on a test with an automotive classifier.",
     "not on a test with an automotive classifier. The pixel pitch of the thermal cameras in the Bao 8, the M-Hero "
     "models and the L380 is not published; of the Chinese production cameras, only the Zeekr 9X's Horus 640D is "
     "documented, at 12 µm."),
    # Appendix 2
    ("- Raytron–Zeekr thermal AEB: https://www.prnewswire.co.uk/news-releases/raytron-partners-with-zeekr-to-launch-"
     "the-worlds-first-thermal-aeb-302614080.html",
     "- Raytron–Zeekr thermal AEB (Horus 640D module; 13 Nov 2025): https://www.prnewswire.co.uk/news-releases/"
     "raytron-partners-with-zeekr-to-launch-the-worlds-first-thermal-aeb-302614080.html\n"
     "- Raytron, customers including the Bao 8, Yangwang U8, Zeekr 9X and LEVC L380 (Automotive World, 20 Oct 2025): "
     "https://www.automotiveworld.com/news/geely-deploys-automotive-thermal-imaging-on-levc-l380-to-reduce-night-"
     "collisions/\n"
     "- Raytron, Horus 640D with a 12 µm 640×512 detector (DiDi R2 robotaxi; Automotive World, 17 Mar 2026): "
     "https://www.automotiveworld.com/news/didi-r2-robotaxi-integrates-raytron-thermal-imaging-sensor/\n"
     "- Raytron at Auto China 2026 (Horus640-EN on an 8 µm detector; 14 May 2026): "
     "https://www.adnkronos.com/immediapress/eng/advancing-intelligent-driving-raytron-highlights-infrared-"
     "innovations-at-auto-china-2026_aXiH3plKdPvstGz433b6g\n"
     "- China Securities Journal on M-Hero and Xuanyuan IDrive (28 Aug and 5 Sep 2022): "
     "https://cs.com.cn/ssgs/gsxw/202208/t20220828_6294225.html ; https://cs.com.cn/qc/202209/t20220905_6296064.html\n"
     "- Guide Infrared investor Q&A on passenger-car design wins (10jqka, 3 Aug 2026): "
     "https://news.10jqka.com.cn/20260803/c678626991.shtml"),
]
for old, new in PAIRS:
    n = text.count(old)
    assert n == 1, f"found {n} times: {old[:80]!r}"
    text = text.replace(old, new)
assert "\n\n\n" not in text
new = text.encode("utf-8")
print("old sha", sha[:12], "new sha", hashlib.sha256(new).hexdigest()[:12], "bytes", len(raw), "->", len(new))
if "--write" in sys.argv:
    report.write_bytes(new)
    print("written")
