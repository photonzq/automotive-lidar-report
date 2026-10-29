"""Equation labels for the report: LaTeX-style \\label and \\eqref, numbered when the report is built.

In the Markdown, each display equation carries one \\label{eq:name} (after "eq:", lower-case letters, digits and
hyphens), and the text cites it as Eq. \\eqref{eq:name}, or Eqs. \\eqref{eq:a}–\\eqref{eq:b} for several. resolve()
numbers the labels 1, 2, 3, ... in document order and replaces each \\label by \\tag{N} and each \\eqref by "(N)",
which is the form build_pdf.py turns into right-aligned equation numbers and links. The source therefore holds no
equation numbers: inserting, deleting or moving an equation renumbers everything at the next build.

Command line (read-only):
    python eqlabels.py <report.md> [--resolved <out.md>] [--figures <figures folder>]
checks the labels and references and prints a summary. --resolved writes the numbered Markdown, so that checks
written for "\\tag{N}" and "Eq. (N)" can run on it. --figures lists every "Eq. (N)" that a figure script quotes, with
the label that number belongs to now, because the scripts quote numbers by hand.
"""
import re
import sys
from pathlib import Path

LABEL = re.compile(r"\\label\{(eq:[a-z0-9-]+)\}")
EQREF = re.compile(r"\\eqref\{(eq:[a-z0-9-]+)\}")
ANY_LABEL = re.compile(r"\\label\{([^}]*)\}")
ANY_EQREF = re.compile(r"\\eqref\{([^}]*)\}")
TAG = re.compile(r"\\tag\{")
NUMREF = re.compile(r"\bEqs?\.\s*\(\d+\)")
DISPLAY = re.compile(r"\$\$(.+?)\$\$", re.S)


def problems(text):
    """List what would make resolve() fail or number wrongly; an empty list means the labels are consistent."""
    out = []
    labels = LABEL.findall(text)
    for bad in sorted(set(ANY_LABEL.findall(text)) - set(labels)):
        out.append(f"malformed label {bad!r}: use eq: followed by lower-case letters, digits and hyphens")
    for bad in sorted(set(ANY_EQREF.findall(text)) - set(EQREF.findall(text))):
        out.append(f"malformed reference {bad!r}")
    seen = set()
    for lab in labels:
        if lab in seen:
            out.append(f"label used twice: {lab}")
        seen.add(lab)
    for ref in sorted(set(EQREF.findall(text)) - seen):
        out.append(f"reference to a missing label: {ref}")
    in_displays = 0
    for d in DISPLAY.findall(text):
        k = len(LABEL.findall(d))
        in_displays += k
        if k != 1:
            out.append(f"display equation with {k} labels: {d.strip()[:80]!r}")
    if in_displays != len(labels):
        out.append(f"{len(labels) - in_displays} label(s) outside display equations")
    if TAG.search(text):
        out.append("a numbered \\tag{} in the source: give the display a \\label{eq:name} instead")
    for m in NUMREF.finditer(text):
        line = text.count("\n", 0, m.start()) + 1
        out.append(f"line {line}: numbered reference {m.group(0)!r}: cite Eq. \\eqref{{eq:name}} instead")
    return out


def numbering(text):
    """Map each label to its equation number (its position in document order)."""
    return {lab: i + 1 for i, lab in enumerate(LABEL.findall(text))}


def resolve(text):
    """Replace \\label{eq:x} by \\tag{N} and \\eqref{eq:x} by (N), numbering the labels in document order."""
    errs = problems(text)
    if errs:
        raise ValueError("equation labels: " + "; ".join(errs[:10]) + (" ..." if len(errs) > 10 else ""))
    num = numbering(text)
    text = LABEL.sub(lambda m: "\\tag{%d}" % num[m.group(1)], text)
    return EQREF.sub(lambda m: "(%d)" % num[m.group(1)], text)


def main(argv):
    text = Path(argv[1]).read_text(encoding="utf-8")
    errs = problems(text)
    num = numbering(text)
    print(f"{len(num)} labelled equations, {len(EQREF.findall(text))} references, {len(errs)} problem(s)")
    for e in errs:
        print("PROBLEM", e)
    if "--resolved" in argv and not errs:
        out = Path(argv[argv.index("--resolved") + 1])
        out.write_bytes(resolve(text).encode("utf-8"))
        print("numbered copy written to", out)
    if "--figures" in argv:
        by_num = {n: lab for lab, n in num.items()}
        for f in sorted(Path(argv[argv.index("--figures") + 1]).glob("*.py")):
            for i, ln in enumerate(f.read_text(encoding="utf-8").splitlines(), 1):
                for m in re.finditer(r"Eqs?\.\s*\((\d+)\)", ln):
                    print(f"{f.name}:{i}: Eq. ({m.group(1)}) is now {by_num.get(int(m.group(1)), 'no equation')}")
    return 1 if errs else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
