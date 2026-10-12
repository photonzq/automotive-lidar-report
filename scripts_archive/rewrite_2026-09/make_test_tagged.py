import re
from pathlib import Path

here = Path(__file__).resolve().parent
s = (here / "base_report.md").read_text(encoding="utf-8")
n = [0]


def f(m):
    n[0] += 1
    return "$$" + m.group(1).rstrip() + r" \tag{" + str(n[0]) + "}$$"


s = re.sub(r"\$\$(.+?)\$\$", f, s, flags=re.S)
s = s.replace(r"Setting $\bar n=n_{\rm req}$ in the first equation", r"Setting $\bar n=n_{\rm req}$ in Eq. (31)")
assert "\t" not in s
(here / "test_tagged.md").write_text(s, encoding="utf-8")
print("tagged", n[0], "Eq. (31) present:", "Eq. (31)" in s)
