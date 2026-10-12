import re
from collections import Counter
p = r"<report folder>\automotive_perception_report_2026-09-27.md"
s = open(p, encoding="utf-8").read()
t = re.sub(r"\{\\rm\s*([^{}]*?)\}", r"{\\mathrm{\1}}", s)
c = Counter()
for m in re.finditer(r"\{\\rm", t):
    c[t[m.start():m.start() + 30]] += 1
print(sum(c.values()))
for k, v in c.most_common(60):
    print(repr(k), v)
