"""Check that every `old` string in a findings file occurs exactly once in the report.

Usage:
  python R4_check_old_strings.py <findings.md> <report.md>

A findings file lists edits as
    - `old`:
        ```text
        <verbatim text>
        ```
The fenced block's own indentation is removed from each of its lines before
matching. Prints, per item heading (## ...), the number of occurrences of each
`old` string and flags any count other than 1; also flags `old` strings that
overlap each other in the report. Paths come from the command line
(e.g. <report>); no network access.
"""
import re
import sys


def extract(findings_text):
    items, current = [], None
    lines = findings_text.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        h = re.match(r"^##\s+(\S.*)$", line)
        if h:
            current = h.group(1).strip()
        if "`old`:" in line:
            # next fenced block
            j = i + 1
            while j < len(lines) and not lines[j].lstrip().startswith("```"):
                j += 1
            if j >= len(lines):
                break
            indent = len(lines[j]) - len(lines[j].lstrip())
            k = j + 1
            body = []
            while k < len(lines) and not lines[k].lstrip().startswith("```"):
                body.append(lines[k][indent:] if lines[k][:indent].strip() == "" else lines[k])
                k += 1
            items.append((current, "\n".join(body)))
            i = k
        i += 1
    return items


def main(fpath, rpath):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    findings = open(fpath, encoding="utf-8").read()
    report = open(rpath, encoding="utf-8").read()
    items = extract(findings)
    spans, bad = [], 0
    for head, old in items:
        n = report.count(old)
        flag = "OK" if n == 1 else "CHECK"
        if n != 1:
            bad += 1
        print(f"[{flag}] {head}: {n} occurrence(s); starts: {old[:70]!r}")
        if n == 1:
            s = report.find(old)
            spans.append((s, s + len(old), head))
    spans.sort()
    for (a0, a1, ha), (b0, b1, hb) in zip(spans, spans[1:]):
        if b0 < a1:
            bad += 1
            print(f"[OVERLAP] {ha} and {hb}")
    print(f"{len(items)} old strings checked; {bad} problem(s)")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
