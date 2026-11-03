"""Update the equation numbers that figure scripts and their table output quote by hand, after equations were inserted.
Each quoted "Eq. (N)" is mapped to the label that number had in the old report and then to that label's number in the
new report, using build/eqlabels.py. Usage:
    renumber_figure_quotes.py <report folder> <old report .md> <file> [<file> ...] [--write]
Only the quoted numbers change; each file keeps its line endings (git stores them as LF either way)."""
import re
import sys
from pathlib import Path

args = [a for a in sys.argv[1:] if a != "--write"]
folder, old_md, files = Path(args[0]), Path(args[1]), [Path(a) for a in args[2:]]
sys.path.insert(0, str(folder / "build"))
import eqlabels  # noqa: E402

old_num = eqlabels.numbering(old_md.read_text(encoding="utf-8"))
new_num = eqlabels.numbering((folder / "automotive_perception_report_2026-09-27.md").read_text(encoding="utf-8"))
label_of_old = {n: lab for lab, n in old_num.items()}
QUOTE = re.compile(r"\b(Eqs?\.\s*)\((\d+)\)")

for f in files:
    raw = f.read_bytes()
    text = raw.decode("utf-8")
    changes = []

    def swap(m):
        lab = label_of_old[int(m.group(2))]
        new = new_num[lab]
        changes.append(f"{m.group(2)}->{new} ({lab})")
        return f"{m.group(1)}({new})"

    out = QUOTE.sub(swap, text)
    print(f"{f.name}: {len(changes)} quotes; " + ", ".join(sorted(set(changes))))
    if "--write" in sys.argv and out != text:
        f.write_bytes(out.encode("utf-8"))
