"""Add China's export controls on thermal imaging to §A3 item 6, next to the US controls, and their sources to Appendix 2.
Usage: china_thermal_controls_edit.py <report .md> <expected sha256 prefix> [--write]
Each anchor must match exactly once and the starting hash must match; writes LF line endings."""
import hashlib
import sys
from pathlib import Path

report, expected = Path(sys.argv[1]), sys.argv[2]
raw = report.read_bytes()
sha = hashlib.sha256(raw).hexdigest()
assert sha.startswith(expected), f"report changed: sha {sha[:12]} != {expected}"
text = raw.decode("utf-8")
assert "\r" not in text


def insert_after_line(anchor, new):
    global text
    assert text.count(anchor) == 1, f"anchor count {text.count(anchor)}: {anchor[:70]!r}"
    i = text.index("\n", text.index(anchor)) + 1
    text = text[:i] + new + text[i:]


def replace(old, new):
    global text
    assert text.count(old) == 1, f"count {text.count(old)}: {old[:70]!r}"
    text = text.replace(old, new)


CHINA = r"""  - **China** has no comparable control on thermal detectors or cameras. Its dual-use export control list, in force since 1 Dec 2024 (MOFCOM Announcement 2024 No. 51; consolidated text as republished in June 2026), numbers its entries in the Wassenaar style but has no counterpart of the sensor entries 6A002 and 6A003, and no entry for focal-plane arrays, microbolometers or thermal cameras as such [P; E]. China does not take part in the Wassenaar Arrangement [P, Wassenaar Arrangement]. The list controls infrared imaging equipment only as a drone payload: entry 9A012.c.1 covers imagers specially designed for the drones and unmanned airships of entry 9A012.a that work between 780 and 30,000 nm and have an IFOV below 2.5 mrad (list, pp. 101–102), carried over from MOFCOM Announcement 2024 No. 31 on drones [P]. The IFOV threshold alone would catch most thermal cameras, since a 640 × 512 core behind a 24° lens has $24^\circ\times(\pi/180)/640=0.65$ mrad by Eq. \eqref{eq:thermal-ifov}, so the drone qualifier decides, and a Chinese automotive, security or thermography core needs no export licence as an item [E]. The list does control the materials of cooled infrared detectors, tellurium and crystals of cadmium telluride, cadmium zinc telluride and mercury cadmium telluride (entry 6C002, p. 92), and China's catalogue of technologies restricted from export covers the know-how for space-borne high-resolution infrared imaging and for making the electro-optical and infrared payloads of drones (MOFCOM/MOST Announcement 2023 No. 57, restricted items 70.4 and 71.4, not changed by the adjustment of July 2025) [P]. Lidar technology, gallium and germanium, and the bans on dual-use exports to US military end users and for Japanese military end use are covered in §D2.
  - The difference shaped China's industry. Because of US export restrictions, Chinese thermal-camera makers used French detectors in the 2000s: Dali's 2008 prospectus says the Chinese market used ULIS/Sofradir detectors only, and Guide's 2010 prospectus credits France's "relatively open" licensing policy and puts imported focal-plane arrays at 49–71% of its purchases in 2007–2009 (pp. 1-1-326 and 1-1-22–23) [P]. Chinese detectors and cores can now be exported for civil use without an item licence, whereas a US detector array is a controlled item under ECCN 6A002.a.3.f [E].
"""
insert_after_line("  - An automotive thermal camera that runs faster than 9 Hz therefore needs this vehicle lock to escape the stricter "
                  "control, a design and validation item that a visible-light camera does not need [E].", CHINA)

replace("- Dali Technology, IPO prospectus (2008), p. 1-1-324 (Maxtech International's 2004 civil market shares): ",
        "- Dali Technology, IPO prospectus (2008), pp. 1-1-324 and 1-1-326 (Maxtech International's 2004 civil market "
        "shares; ULIS/Sofradir detectors in China because of US export restrictions): ")

SOURCES = r"""- Guide Infrared, IPO prospectus (2010), pp. 1-1-22–23 (imported focal-plane arrays, Sofradir/ULIS supply, French export licensing): http://static.cninfo.com.cn/finalpage/2010-07-02/58123502.PDF
- MOFCOM, MIIT, GAC and State Cryptography Administration, Dual-Use Items Export Control List (Announcement 2024 No. 51, in force 1 Dec 2024; consolidated text as republished by the Fujian Department of Commerce, Jun 2026; pp. 49, 92 and 101–102): https://swt.fujian.gov.cn/mqchzhfwpt/tzfwcpch/fwch/lywxhjsjckfw/202607/t20260716_7179034.htm ; https://mqch.vdian.cc/profile/cms/1/2026/06/27/75886ce64764424ca7ac8d9bd5643cf6_20260627111553A020.pdf
- MOFCOM, GAC and CMC Equipment Development Department, Announcement 2024 No. 31 on drone export controls (31 Jul 2024, in force 1 Sep 2024): https://www.mofcom.gov.cn/zwgk/zcfb/art/2024/art_db6e21907d69404fb473ddb0b248d3d7.html
- MOFCOM and MOST, Catalogue of Technologies Prohibited or Restricted from Export (Announcement 2023 No. 57; restricted part from p. 8, items 70, 71 and 73 on pp. 24–25): https://www.most.gov.cn/tztg/202312/W020231221620858841394.pdf ; adjustment, Announcement 2025 No. 28 (15 Jul 2025; battery and lithium items): https://www.mofcom.gov.cn/zcfb/blgg/gg/2025/art/2025/art_aaaf4e92c93b4809a1edc45d8ab9c070.html
- Wassenaar Arrangement, participating states: https://www.wassenaar.org/about-us/
"""
insert_after_line("- Raytron Technology, IPO prospectus (2019), pp. 174 and 186: ", SOURCES)

new = text.encode("utf-8")
odd = sorted({c for c in text if ord(c) > 127} - {c for c in raw.decode("utf-8") if ord(c) > 127})
print("old sha", sha[:12], "new sha", hashlib.sha256(new).hexdigest()[:12], "bytes", len(raw), "->", len(new))
print("non-ASCII characters new to the report:", [f"U+{ord(c):04X}" for c in odd])
if "--write" in sys.argv:
    report.write_bytes(new)
    print("written")
