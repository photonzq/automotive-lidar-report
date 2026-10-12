"""Check a rewritten chunk against its original: nothing factual may be lost.

Usage: python check_chunk.py NN
"""
import re
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent

TAG_RE = re.compile(r"\[(P|I|T|E|U|MR|S|D|NT|R)(?=[\]:,/ ;])")
URL_RE = re.compile(r"https?://[^\s)\]>;,]+")
IMG_RE = re.compile(r"!\[[^\]]*\]\([^)]*\)")
NUM_RE = re.compile(r"(?<![A-Za-z_\\])\d+(?:[.,]\d+)*")
BANNED = ["updated", "corrected", "revised", "previous version", "now shows", "rewrite", "rewritten", "audit", "reviewer"]


def strip_urls(s: str) -> str:
    return URL_RE.sub(" ", s)


def numbers(s: str) -> Counter:
    s = strip_urls(s)
    s = s.replace("{,}", ",").replace("\\,", "")
    out = Counter()
    for m in NUM_RE.finditer(s):
        tok = m.group(0).replace(",", "")
        tok = tok.rstrip(".")
        if tok.startswith("0") and "." not in tok and len(tok) > 1:
            tok = tok.lstrip("0") or "0"
        out[tok] += 1
    return out


def tables(lines):
    """Return list of (start_line, n_rows, n_cols_first_row)."""
    res, i = [], 0
    while i < len(lines):
        if lines[i].lstrip().startswith("|"):
            j = i
            while j < len(lines) and lines[j].lstrip().startswith("|"):
                j += 1
            ncols = [lines[k].count("|") - lines[k].count("\\|") for k in range(i, j)]
            res.append((i + 1, j - i, ncols))
            i = j
        else:
            i += 1
    return res


def main(cid: str) -> int:
    d = HERE / f"chunk{cid}"
    orig = (d / f"chunk{cid}_original.md").read_text(encoding="utf-8")
    new = (d / f"chunk{cid}.md").read_text(encoding="utf-8")
    ol, nl = orig.split("\n"), new.split("\n")
    problems = []

    # 1. numbers: every number in the original must still appear (at least once)
    on, nn = numbers(orig), numbers(new)
    missing = sorted(k for k in on if nn.get(k, 0) == 0)
    if missing:
        problems.append(f"numbers missing ({len(missing)}): " + ", ".join(missing[:80]))

    # 2. evidence tags: counts per tag must not fall
    ot, nt = Counter(TAG_RE.findall(orig)), Counter(TAG_RE.findall(new))
    for k, v in ot.items():
        if nt.get(k, 0) < v:
            problems.append(f"tag [{k}] count fell {v} -> {nt.get(k, 0)}")

    # 3. URLs: all original URLs present
    ou, nu = set(URL_RE.findall(orig)), set(URL_RE.findall(new))
    lost = sorted(ou - nu)
    if lost:
        problems.append(f"URLs missing ({len(lost)}): " + " ; ".join(lost[:10]))
    added = sorted(nu - ou)
    if added:
        problems.append(f"new URLs ({len(added)}) - no new sources allowed: " + " ; ".join(added[:10]))

    # 4. headings identical and in order
    oh = [l for l in ol if re.match(r"^#{1,4} ", l)]
    nh = [l for l in nl if re.match(r"^#{1,4} ", l)]
    if oh != nh:
        a, b = set(oh), set(nh)
        problems.append(f"headings changed: removed {sorted(a - b)[:5]} added {sorted(b - a)[:5]}"
                        + ("" if a != b else " (order changed)"))

    # 5. Sources lines identical
    os_, ns_ = [l for l in ol if l.startswith("Sources:")], [l for l in nl if l.startswith("Sources:")]
    if os_ != ns_:
        problems.append(f"Sources: lines changed ({len(os_)} -> {len(ns_)})")

    # 6. images
    if Counter(IMG_RE.findall(orig)) != Counter(IMG_RE.findall(new)):
        problems.append("image links changed")

    # 7. tables: same number of tables, same row counts, consistent columns
    ot_, nt_ = tables(ol), tables(nl)
    if len(ot_) != len(nt_):
        problems.append(f"table count {len(ot_)} -> {len(nt_)}")
    else:
        for (a, ra, ca), (b, rb, cb) in zip(ot_, nt_):
            if ra != rb:
                problems.append(f"table at original line {a}: rows {ra} -> {rb} (new line {b})")
            if len(set(cb)) != 1:
                problems.append(f"table at new line {b}: inconsistent column counts {sorted(set(cb))}")
            elif ca and cb and ca[0] != cb[0]:
                problems.append(f"table at new line {b}: columns {ca[0]} -> {cb[0]}")

    # 8. conventions per line
    for i, l in enumerate(nl, 1):
        t = l.replace("\\$", "")
        if t.count("$") % 2:
            problems.append(f"odd $ on line {i}: {l[:90]}")
        for m in re.finditer(r"\$(?=[0-9])", t):
            if t[:m.start()].count("$") % 2 == 1 and not t[:m.start()].endswith("$"):
                problems.append(f"digit right after closing $ on line {i}: {t[max(0, m.start() - 20):m.start() + 6]}")
        if l.lstrip().startswith("|"):
            for seg in re.findall(r"\$[^$]*\$", t):
                if "|" in seg:
                    problems.append(f"'|' inside math in a table row, line {i}")
        if "\t" in l:
            problems.append(f"tab on line {i}")
    low = new.lower()
    olow = orig.lower()
    for w in BANNED:
        if low.count(w) > olow.count(w):
            problems.append(f"banned word added: '{w}'")

    # 9. display equations: each must carry \tag{eq:...}; labels unique; references resolve
    disp = re.findall(r"\$\$(.+?)\$\$", new, flags=re.S)
    untagged = [x[:60] for x in disp if "\\tag{eq:" not in x]
    if untagged:
        problems.append(f"display equations without \\tag{{eq:...}} ({len(untagged)}): {untagged[:3]}")
    labels = re.findall(r"\\tag\{(eq:[^}]+)\}", new)
    dup = [k for k, v in Counter(labels).items() if v > 1]
    if dup:
        problems.append(f"duplicate equation labels: {dup}")
    bad_prefix = [x for x in labels if not x.startswith(f"eq:c{cid}-") and not x.startswith(f"eq:{cid}-")]
    if bad_prefix:
        problems.append(f"labels without chunk prefix eq:c{cid}-...: {bad_prefix[:5]}")
    refs = set(re.findall(r"Eq\.\s*\((eq:[^)]+)\)", new))
    unresolved = sorted(refs - set(labels))
    if unresolved:
        problems.append(f"unresolved equation references: {unresolved}")
    vague = re.findall(r"(?i)\b(the (?:first|second|third|last|previous|above) equation|equation above)\b", new)
    if vague:
        problems.append(f"vague equation references remain: {vague[:5]}")

    growth = len(new.encode()) / max(1, len(orig.encode()))
    print(f"chunk {cid}: {len(orig.encode())} -> {len(new.encode())} bytes (x{growth:.2f}); "
          f"display equations {len(disp)}, labels {len(labels)}, references {len(refs)}")
    if problems:
        print(f"{len(problems)} problem(s):")
        for p in problems:
            print(" -", p)
        return 1
    print("OK: no problems found")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
