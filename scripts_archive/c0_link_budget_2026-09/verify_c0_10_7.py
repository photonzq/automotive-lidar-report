import re
from pathlib import Path

s = Path(r"<report folder>\automotive_perception_report_2026-09-27.md").read_text(encoding="utf-8")
a = s.index("#### 10.7 Dynamic range")
b = s.index("#### 10.8 What the model")
sec = s[a:b]
print("10.7 tags:", re.findall(r"\\tag\{(\d+)\}", sec))
print("10.7 Eq refs:", re.findall(r"\bEqs?\.\s*\(\d+\)(?:\s*(?:,|and|–|-|to|or)\s*\(\d+\))*", sec))
c0 = s[s.index("### 10. Link budget"):s.index("## C1. Taxonomy")]
print("10.6 tags:", re.findall(r"\\tag\{(\d+)\}", c0[c0.index("#### 10.6"):c0.index("#### 10.7")]))
print("margin eq line:", [l[:60] for l in c0.split("\n") if "M(R)=10\\log_{10}" in l])
for kw in [r"n_{\rm req}=30", "45/130", "b=2.2", r"n_{\rm th}=13", "10^{-6}", "generous"]:
    print(f"{kw!r} in new 10.7: {kw in sec}")
print("eta note present:", "The FMCW value, 0.25, is a design value" in s)
print("tags total:", len(re.findall(r"\\tag\{(\d+)\}", s)))
