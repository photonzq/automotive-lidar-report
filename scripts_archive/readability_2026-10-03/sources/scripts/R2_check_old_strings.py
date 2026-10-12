"""R2 check: every `old` block in a findings file must occur exactly once in the report.

Usage (Anaconda interpreter):
  python R2_check_old_strings.py <report.md> <findings.md>

A block is the fenced ```text ... ``` code block that follows a list line starting with "- `old`".
Prints the occurrence count for each block, the report's sha256 prefix, and exits with
status 1 if any count differs from 1. Reads files only; no network access.
"""
import hashlib
import re
import sys


def main(report_path, findings_path):
    report = open(report_path, encoding="utf-8").read()
    sha = hashlib.sha256(open(report_path, "rb").read()).hexdigest()[:12]
    text = open(findings_path, encoding="utf-8").read()
    lines = text.split("\n")
    blocks = []
    current_item = None
    i = 0
    while i < len(lines):
        line = lines[i]
        m = re.match(r"^## (\S+)", line)
        if m:
            current_item = m.group(1)
        if re.match(r"^\s*- `old`", line):
            j = i + 1
            while j < len(lines) and not lines[j].startswith("```"):
                j += 1
            k = j + 1
            while k < len(lines) and not lines[k].startswith("```"):
                k += 1
            blocks.append((current_item, i + 1, "\n".join(lines[j + 1:k])))
            i = k
        i += 1
    bad = 0
    print(f"report sha256 prefix: {sha}; old blocks: {len(blocks)}")
    for item, lineno, block in blocks:
        n = report.count(block)
        flag = "ok" if n == 1 else "CHECK"
        if n != 1:
            bad += 1
        print(f"{flag:5s} {item} (findings line {lineno}): {n} occurrence(s): {block[:70]!r}")
    print("all unique" if bad == 0 else f"{bad} block(s) not unique or missing")
    return 1 if bad else 0


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    sys.exit(main(sys.argv[1], sys.argv[2]))
