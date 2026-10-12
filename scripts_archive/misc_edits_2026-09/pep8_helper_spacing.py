import re
from pathlib import Path

BFIG = Path(r"<report folder>\build\figures")
for p in sorted(BFIG.glob("*.py")):
    t = p.read_text(encoding="utf-8")
    new = re.sub(r"(\S)\n+(def _output_dir\(\) -> Path:)", r"\1\n\n\n\2", t, count=1)
    if new != t:
        p.write_text(new, encoding="utf-8", newline="\n")
        print("spaced", p.name)
