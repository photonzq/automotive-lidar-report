"""Section D7: rewrite the Hesai row with the evidence on its in-house FMCW programme, fix the RoboSense
inventor wording, extend the Judgement clause, and append sources."""
import hashlib
import re
import sys
from pathlib import Path

REPORT = Path(r"<report folder>\automotive_perception_report_2026-09-27.md")
SCR = Path(r"<scratch>")
SNAP = SCR / "rewrite" / "report_after_d7.md"
OUT_SNAP = SCR / "rewrite" / "report_after_d7_hesai.md"
DRY = "--dry" in sys.argv

raw = REPORT.read_bytes()
assert hashlib.sha256(raw).digest() == hashlib.sha256(SNAP.read_bytes()).digest(), "report changed since the snapshot"
s = raw.decode("utf-8")
a = s.index("## D7. Chinese FMCW and coherent lidar")
b = s.index("\n## ", a + 10)
d7 = s[a:b]

OLD_HESAI = ("| **Hesai** | CEO Li Yifan (Apr 2024): developing FMCW, \"no external product line\". \"FMCW products depend on "
             "suppliers; whether the underlying technology is mature decides whether the product is\" | No FMCW in any SEC "
             "filing. A May 2026 driving-dataset paper with four Hesai co-authors uses a forward-facing 4D FMCW lidar whose "
             "vendor is not named: a hint of an in-house unit, not evidence [U] | [R] |")
NEW_HESAI = (
    "| **Hesai** | **In-house programme since 2018**, set out in its draft prospectus for a Shanghai STAR Market listing "
    "(data to Sep 2020; Hesai listed on Nasdaq instead) [P]: a completed 1,550 nm coherent-detection lidar project "
    "(¥4.7 M in 2018–19); an FMCW lidar project (¥3.2 M in 2019, ¥8.4 M in Jan–Sep 2020, 2020 budget ¥14 M) aimed at a "
    "small, long-range, automotive-grade unit; a completed FMCW prototype; a 1,550 nm external-cavity laser with a "
    "linewidth under 5 kHz and more than 20 mW, rated to 70 °C; and research on silicon-photonic coherent chips. "
    "**The patents continue:** about two dozen Hesai patent publications with 2023–25 priority concern FMCW, among them "
    "narrow-linewidth external-cavity lasers, linear swept sources, an FMCW transceiver chip (CN120215021A) and an FMCW "
    "scanning lidar (US 2025/0306188 A1, co-invented by CTO 向少卿) [P]. A 2023 campus job advertisement sought a "
    "silicon-photonics PhD to design devices for FMCW [P]. CEO Li Yifan (Apr 2024): developing FMCW, \"no external "
    "product line\". \"FMCW products depend on suppliers; whether the underlying technology is mature decides whether the "
    "product is\" | No FMCW product, and no mention of FMCW in any of its SEC filings of 2021–26 (full-text search). "
    "**Probably on the road as a prototype** [E]: the May 2026 4DLidarOpen dataset (Tsinghua with Hesai) uses a "
    "forward-facing 4D FMCW lidar whose maker is not named, although every ToF lidar in it is named by its Hesai model, "
    "and that lidar detects cars and pedestrians about as well as the AT128 beside it. Two of the paper's four Hesai "
    "authors, 潘政清 (Zhengqing Pan) and 孙恺 (Kai Sun, probably Hesai's co-founder and chief scientist), are inventors "
    "on Hesai's FMCW patents, and Tsinghua and Hesai jointly filed a patent on correcting target velocity from radial-"
    "velocity point clouds (CN121613433A, Dec 2025) with the paper's team. No source states that the lidar is Hesai's "
    "| [R] |")

E = [
    (OLD_HESAI, NEW_HESAI),
    ("US patents 12025739B1 (SiPh multi-transceiver FMCW; CEO a co-inventor),",
     "US patents 12025739B1 (SiPh multi-transceiver FMCW; inventors 王静, lead author of the papers below, and "
     "co-founders 邱纯鑫, CEO when it was filed and chairman and chief scientist since March 2024, and 刘乐天, the CTO),"),
    ("Hesai and RoboSense already hold FMCW patents and in-house programmes; RoboSense's is visible in its papers with "
     "SUSTech, including the 200 m, 10% system test of 2025.",
     "Hesai and RoboSense already hold FMCW patents and in-house programmes. RoboSense's is visible in its papers with "
     "SUSTech, including the 200 m, 10% system test of 2025. Hesai's dates from 2018, continues in its patents through "
     "2025 and has probably reached a road-going prototype, the FMCW lidar of a 2026 dataset."),
    ("https://arxiv.org/html/2605.18074 (dataset paper with Hesai co-authors)",
     "https://arxiv.org/abs/2605.18074 (4DLidarOpen dataset, Tsinghua and Hesai, 2026)"),
]
for old, new in E:
    c = d7.count(old)
    assert c == 1, (old[:90], c)
    d7 = d7.replace(old, new)

NEW_SOURCES = (
    " ; http://qxb-pdf-osscache.qixin.com/AnBaseinfo/5e2cf343d24252785d548b8e65847b14.pdf (Hesai, draft STAR Market prospectus, 2020)"
    " ; https://patents.google.com/patent/US20250306188A1/en (Hesai, FMCW lidar and scanning method)"
    " ; https://patents.google.com/patent/CN120215021A/en (Hesai, FMCW transceiver chip)"
    " ; https://patents.google.com/patent/CN121613433A/en (Tsinghua and Hesai, velocity correction)"
    " ; https://www.career.zju.edu.cn/jyxt/sczp/zpztgl/ckZpgwXq.zf?dwxxid=JG1206802&zpxxbh=05EECCF5E53C2077E0653A68DD0E9B18 (Hesai campus job advertisement, Sep 2023)"
    " ; https://efts.sec.gov/LATEST/search-index?q=%22FMCW%22&ciks=0001861737 (SEC full-text search of Hesai filings)"
    " ; https://me.sjtu.edu.cn/xy-dt/66815.html (孙恺, Hesai co-founder and chief scientist)"
    " ; https://patents.google.com/patent/US12025739B1/en (RoboSense patent and inventors)"
    " ; https://basic.10jqka.com.cn/176/HK2498/manager.html (RoboSense executives)"
)
src_lines = [l for l in d7.split("\n") if l.startswith("Sources: ")]
assert len(src_lines) == 1, len(src_lines)
d7 = d7.replace(src_lines[0], src_lines[0].rstrip() + NEW_SOURCES)

s = s[:a] + d7 + s[b:]
tags = re.findall(r"\\tag\{(\d+)\}", s)
assert [int(t) for t in tags] == list(range(1, len(tags) + 1))
odd = [i for i, l in enumerate(s.split("\n"), 1) if l.replace("\\$", "").count("$") % 2]
assert not odd, odd[:5]
pipes = [i for i, l in enumerate(s.split("\n"), 1)
         if l.startswith("|") and any("|" in sp for sp in re.findall(r"\$([^$]+)\$", l.replace("\\$", "")))]
assert not pipes, pipes[:5]
# the Hesai row must still have the table's four columns
row = [l for l in d7.split("\n") if l.startswith("| **Hesai** |")]
assert len(row) == 1 and row[0].count(" | ") + 2 == 5, (len(row), row[0].count(" | ") if row else None)
hdr = [l for l in d7.split("\n") if l.startswith("| Company | Product / claim | Status | Tag |")]
assert len(hdr) == 1, len(hdr)
print("tags", len(tags), "| bytes", len(s.encode("utf-8")), "(was", len(raw), ")")
if not DRY:
    REPORT.write_bytes(s.encode("utf-8"))
    OUT_SNAP.write_bytes(s.encode("utf-8"))
    print("written; snapshot", OUT_SNAP.name)
