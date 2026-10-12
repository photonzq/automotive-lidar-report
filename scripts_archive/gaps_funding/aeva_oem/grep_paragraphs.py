"""Print every paragraph (line) of a text file that matches a regular expression.

Each hit is printed with its line number; long paragraphs are printed in full so
that the surrounding sentence context is preserved. Optional line window
limits the search to a section of the document.

Usage (run from the aeva_oem folder):
    python scripts/grep_paragraphs.py <file.txt> "<regex>" [start_line] [end_line]
"""
import re
import sys


def main():
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    path, pat = sys.argv[1], sys.argv[2]
    lo = int(sys.argv[3]) if len(sys.argv) > 3 else 1
    hi = int(sys.argv[4]) if len(sys.argv) > 4 else 10**9
    rx = re.compile(pat, re.I)
    with open(path, encoding="utf-8") as fh:
        for n, line in enumerate(fh, 1):
            if lo <= n <= hi and rx.search(line):
                print(f"[{n}] {line.strip()}\n")


if __name__ == "__main__":
    main()
