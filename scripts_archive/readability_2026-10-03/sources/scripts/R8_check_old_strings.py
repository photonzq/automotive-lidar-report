"""R8_C9a_inband: check a findings file against the report. For every fenced
block that follows an `old` line, count its exact occurrences in the report
(each must be 1); for every block that follows a `new` line, flag versioning
words. Also flag e-mail addresses anywhere in the findings file. Prints the
report's SHA-256 prefix. Files only, no network access.

Usage: python R8_check_old_strings.py <report.md> <findings.md>
"""
import hashlib
import re
import sys

VERSIONING = re.compile(r"\b(corrected|updated|revised|newly|added|now)\b", re.I)
EMAIL = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")


def blocks(text):
    """Yield (kind, body) for fenced blocks introduced by an `old`/`new` line."""
    lines = text.split("\n")
    i = 0
    while i < len(lines):
        m = re.match(r"\s*-?\s*`(old|new)[^`]*`", lines[i])
        if m:
            kind = m.group(1)
            j = i + 1
            while j < len(lines) and not lines[j].strip().startswith("```"):
                j += 1
            if j < len(lines):
                indent = len(lines[j]) - len(lines[j].lstrip())
                k = j + 1
                body = []
                while k < len(lines) and not lines[k].strip().startswith("```"):
                    body.append(lines[k][indent:] if lines[k][:indent].strip() == "" else lines[k])
                    k += 1
                yield kind, "\n".join(body)
                i = k
        i += 1


def main():
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    report = open(sys.argv[1], encoding="utf-8").read()
    findings = open(sys.argv[2], encoding="utf-8").read()
    print("report sha256 prefix:", hashlib.sha256(report.encode("utf-8")).hexdigest()[:12])
    bad = 0
    n_old = 0
    for kind, body in blocks(findings):
        if kind == "old":
            n_old += 1
            c = report.count(body)
            print(f"old #{n_old}: {c} occurrence(s); starts: {body[:70]!r}")
            if c != 1:
                bad += 1
        else:
            hits = sorted(set(w.lower() for w in VERSIONING.findall(body)))
            if hits:
                print(f"  new block after old #{n_old}: versioning words {hits}")
    for e in sorted(set(EMAIL.findall(findings))):
        print("e-mail address found:", e)
        bad += 1
    print("OK" if bad == 0 else f"{bad} problem(s)")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
