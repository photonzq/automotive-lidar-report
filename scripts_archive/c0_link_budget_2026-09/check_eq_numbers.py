import re
import shutil
from pathlib import Path

REPORT = Path(r"<report folder>\automotive_perception_report_2026-09-27.md")
SNAP = Path(r"<scratch>\rewrite\report_after_peer_round2.md")
shutil.copy2(REPORT, SNAP)
s = REPORT.read_text(encoding="utf-8")
print("bytes", len(s.encode("utf-8")), "tags", len(re.findall(r"\\tag\{(\d+)\}", s)))
a, b = s.index("### 10. Link budget"), s.index("## C1. Taxonomy")
c0 = s[a:b]
for m in re.finditer(r"\$\$(.{0,90}?)(?:.*?)\\tag\{(\d+)\}", c0, flags=re.S):
    print(f"  ({m.group(2)}) {m.group(1)[:90]!r}")
for probe in ("10.8 lists what the model leaves out.", "| 10.8 Limits of the model | What is left out? | — |",
              "10.8 notes what changes when they fail.", "computed value (10.8).", "#### 10.8 What the model leaves out",
              "and why China's lidar standard tests high-reflectivity ghosts.\n\n**Figures and data.**",
              "although the retroreflector was 37.7 dB brighter [P].\n",
              "(WMO: no agreed international definition of rain intensity) ; https://www.nature.com/articles/s41586-026-10183-6"):
    print(f"{s.count(probe)} x {probe[:70]!r}")
i = s.index("#### 10.8 What the model leaves out")
print(s[i:i + 1800])
