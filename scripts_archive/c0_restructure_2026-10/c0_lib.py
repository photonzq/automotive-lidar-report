"""Assemble a restructured section from a plan of new text and exact copies of the old text.

A plan is a list of segments:
  NEW(text, tight=False)                      new Markdown, written for the restructure
  COPY(first, last=None, subs=(), dropcol=False, keepcols=None, dedent=0, tight=False)
      the old lines from the unique line starting with `first` (or equal to it, if `first` starts with "=")
      to the first line at or after it starting with `last` (inclusive; one line if `last` is None);
      `subs` are (old, new[, count]) replacements, each of which must occur exactly `count` times (default 1);
      `dropcol` drops the last column of every table row, `keepcols` keeps the first n columns;
      `dedent` removes up to n leading spaces from every line.
Segments are joined by a blank line, or by a single newline when `tight` (to continue a list or paragraph).
"""


def NEW(text, tight=False):
    return {"kind": "new", "text": text.strip("\n"), "tight": tight}


def COPY(first, last=None, subs=(), dropcol=False, keepcols=None, dedent=0, tight=False):
    return {"kind": "copy", "first": first, "last": last, "subs": subs, "dropcol": dropcol,
            "keepcols": keepcols, "dedent": dedent, "tight": tight}


def _match(line, key):
    return line == key[1:] if key.startswith("=") else line.startswith(key)


def _row(line, dropcol, keepcols):
    cells = line.strip().strip("|").split("|")
    cells = cells[:-1] if dropcol else cells[:keepcols]
    return "|" + "|".join(cells) + "|"


def render(seg, old):
    if seg["kind"] == "new":
        return seg["text"]
    hits = [i for i, l in enumerate(old) if _match(l, seg["first"])]
    if len(hits) != 1:
        raise SystemExit(f"COPY start {seg['first'][:60]!r} matches {len(hits)} lines")
    i = hits[0]
    j = i if seg["last"] is None else next((k for k in range(i, len(old)) if _match(old[k], seg["last"])), None)
    if j is None:
        raise SystemExit(f"COPY end {seg['last'][:60]!r} not found after {seg['first'][:40]!r}")
    text = "\n".join(old[i:j + 1])
    for s in seg["subs"]:
        a, b = s[0], s[1]
        n = s[2] if len(s) > 2 else 1
        if text.count(a) != n:
            raise SystemExit(f"in COPY {seg['first'][:40]!r}: {a[:70]!r} occurs {text.count(a)}x, expected {n}")
        text = text.replace(a, b)
    lines = text.split("\n")
    if seg["dedent"]:
        d = seg["dedent"]
        lines = [l[d:] if l.startswith(" " * d) else l.lstrip(" ") for l in lines]
    if seg["dropcol"] or seg["keepcols"]:
        lines = [_row(l, seg["dropcol"], seg["keepcols"]) if l.startswith("|") else l for l in lines]
    return "\n".join(lines)


def assemble(plan, old):
    out = ""
    used = []
    for seg in plan:
        piece = render(seg, old)
        if seg["kind"] == "copy":
            first = next(i for i, l in enumerate(old) if _match(l, seg["first"]))
            last = first if seg["last"] is None else next(k for k in range(first, len(old)) if _match(old[k], seg["last"]))
            used.append((first, last))
        out = piece if not out else out + ("\n" if seg["tight"] else "\n\n") + piece
    return out, used
