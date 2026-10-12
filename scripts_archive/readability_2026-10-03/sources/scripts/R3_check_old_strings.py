"""Check that every `old` string in a findings file occurs exactly once in the report.

Usage:
  python R3_check_old_strings.py <report.md> <findings.md>

The findings file gives each `old` string as a fenced ```text block on the lines after a line
containing "`old`:". The block's common indentation is removed before matching. Prints the count
for each block and exits with status 1 if any count differs from 1.
"""
import re
import sys
import textwrap

sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def old_blocks(findings_text):
    lines = findings_text.splitlines()
    i = 0
    while i < len(lines):
        if "`old`:" in lines[i]:
            j = i + 1
            while j < len(lines) and not lines[j].strip().startswith("```"):
                j += 1
            k = j + 1
            while k < len(lines) and not lines[k].strip().startswith("```"):
                k += 1
            block = textwrap.dedent("\n".join(lines[j + 1:k]))
            yield i + 1, block
            i = k
        i += 1


def main(report_path, findings_path):
    report = open(report_path, encoding="utf-8").read()
    findings = open(findings_path, encoding="utf-8").read()
    bad = 0
    section = ""
    sec_starts = [(m.start(), m.group(1)) for m in re.finditer(r"^## (\S+)", findings, re.M)]
    for line_no, block in old_blocks(findings):
        pos = sum(len(l) + 1 for l in findings.splitlines()[:line_no - 1])
        for start, name in sec_starts:
            if start <= pos:
                section = name
        n = report.count(block)
        flag = "OK " if n == 1 else "BAD"
        if n != 1:
            bad += 1
        print(f"{flag} count={n} [{section}] line {line_no}: {block[:90]!r}")
    print("blocks with count != 1:", bad)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1], sys.argv[2]))
