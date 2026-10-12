"""R6_C10_part2: check a findings file against the report before hand-off.

Usage: python R6_check_old_strings.py <findings.md> <report.md>

For every `old` text block (a line containing `old` followed by a ```text fence) it prints how
often the string occurs in the report; each must occur exactly once. It also flags:
- e-mail addresses anywhere in the findings file;
- versioning words in `new` blocks ("corrected", "updated", "revised", "now", "newly", "added").
No network access.
"""
import re
import sys


def blocks(text, label):
    out = []
    for m in re.finditer(r"`%s`[^\n]*\n\s*```text\n(.*?)\n\s*```" % label, text, re.S):
        body = "\n".join(line.strip() for line in m.group(1).split("\n"))
        out.append(body)
    return out


def main(findings_path, report_path):
    text = open(findings_path, encoding="utf-8").read()
    report = open(report_path, encoding="utf-8").read()
    olds, news = blocks(text, "old"), blocks(text, "new")
    print(f"{len(olds)} old blocks, {len(news)} new blocks")
    bad = 0
    for i, s in enumerate(olds, 1):
        n = report.count(s)
        flag = "OK" if n == 1 else "FAIL"
        bad += n != 1
        print(f"  old {i:2d}: {n} occurrence(s) {flag} | {s[:90]}")
    vers = re.compile(r"\b(corrected|updated|revised|now|newly|added)\b", re.I)
    for i, s in enumerate(news, 1):
        hits = vers.findall(s)
        if hits:
            print(f"  new {i:2d}: versioning words {hits}")
    emails = re.findall(r"[\w.+-]+@[\w-]+\.[\w.-]+", text)
    print("e-mail addresses in findings:", emails or "none")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
