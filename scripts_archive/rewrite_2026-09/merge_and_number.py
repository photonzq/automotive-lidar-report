"""Merge rewritten chunks, number display equations globally (1)..(N), resolve Eq. references,
run whole-document safety checks, and (with --write) write the report.

Usage: python merge_and_number.py [--write]
"""
import json
import re
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPORT = Path(r"<report folder>\automotive_perception_report_2026-09-27.md")
sys.path.insert(0, str(HERE))
from check_chunk import IMG_RE, TAG_RE, URL_RE, numbers, tables  # noqa: E402

ORDER = [f"{i:02d}" for i in range(1, 17)] + ["TAIL"]


def load(cid: str, rewritten: bool = True) -> str:
    d = HERE / f"chunk{cid}"
    if cid == "TAIL" or not rewritten:
        return (d / f"chunk{cid}_original.md").read_text(encoding="utf-8")
    return (d / f"chunk{cid}.md").read_text(encoding="utf-8")


def number_equations(text: str):
    labels, n = {}, 0
    out, pos = [], 0
    for m in re.finditer(r"\$\$(.+?)\$\$", text, flags=re.S):
        body = m.group(1)
        n += 1
        tm = re.search(r"\\tag\{(eq:[^}]+)\}", body)
        if tm:
            if tm.group(1) in labels:
                raise SystemExit(f"duplicate label {tm.group(1)}")
            labels[tm.group(1)] = n
            body = body[:tm.start()].rstrip() + f" \\tag{{{n}}}" + body[tm.end():]
        elif re.search(r"\\tag\{\d+\}", body):
            body = re.sub(r"\\tag\{\d+\}", f"\\\\tag{{{n}}}", body)
        else:
            body = body.rstrip() + f" \\tag{{{n}}}"
        out.append(text[pos:m.start()])
        out.append("$$" + body + "$$")
        pos = m.end()
    out.append(text[pos:])
    text = "".join(out)

    unresolved = set()

    def ref(mm):
        lab = "eq:" + mm.group(1)
        if lab not in labels:
            unresolved.add(lab)
            return mm.group(0)
        return f"({labels[lab]})"

    text = re.sub(r"\(eq:([a-z0-9][a-z0-9\-]*)\)", ref, text)
    return text, labels, n, unresolved


def main(write: bool) -> None:
    base = (HERE / "base_report.md").read_text(encoding="utf-8")
    live = REPORT.read_bytes()
    if live != (HERE / "base_report.md").read_bytes():
        raise SystemExit("ABORT: the live report changed since the chunks were split; merge by hand")
    parts = [load(c) for c in ORDER]
    merged = "\n".join(parts)
    merged, labels, neq, unresolved = number_equations(merged)
    problems = []
    if unresolved:
        problems.append(f"unresolved equation references: {sorted(unresolved)}")
    if "eq:" in merged:
        left = re.findall(r".{0,30}eq:[a-z0-9\-]+.{0,10}", merged)
        problems.append(f"leftover eq: labels: {left[:5]}")

    # whole-document safety checks against the base
    bn, mn = numbers(base), numbers(merged)
    missing = sorted(k for k in bn if mn.get(k, 0) == 0)
    if missing:
        problems.append(f"numbers missing ({len(missing)}): {missing[:60]}")
    bt, mt = Counter(TAG_RE.findall(base)), Counter(TAG_RE.findall(merged))
    for k, v in bt.items():
        if mt.get(k, 0) < v:
            problems.append(f"tag [{k}] fell {v} -> {mt.get(k, 0)}")
    if set(URL_RE.findall(base)) - set(URL_RE.findall(merged)):
        problems.append("URLs lost")
    bh = [l for l in base.split("\n") if re.match(r"^#{1,4} ", l)]
    mh = [l for l in merged.split("\n") if re.match(r"^#{1,4} ", l)]
    if bh != mh:
        problems.append("headings differ")
    if [l for l in base.split("\n") if l.startswith("Sources:")] != [l for l in merged.split("\n") if l.startswith("Sources:")]:
        problems.append("Sources lines differ")
    if Counter(IMG_RE.findall(base)) != Counter(IMG_RE.findall(merged)):
        problems.append("images differ")
    bt_, mt_ = tables(base.split("\n")), tables(merged.split("\n"))
    if [r for _, r, _ in bt_] != [r for _, r, _ in mt_]:
        problems.append("table row structure differs")
    for i, l in enumerate(merged.split("\n"), 1):
        t = l.replace("\\$", "")
        if t.count("$") % 2:
            problems.append(f"odd $ line {i}: {l[:80]}")
        if "\t" in l or "\r" in l:
            problems.append(f"tab/CR line {i}")
    print(f"merged: {len(base.encode())} -> {len(merged.encode())} bytes; display equations numbered 1..{neq}; "
          f"labels {len(labels)}")
    (HERE / "merged_preview.md").write_text(merged, encoding="utf-8")
    (HERE / "equation_labels.json").write_text(json.dumps(labels, indent=1), encoding="utf-8")
    if problems:
        print(f"{len(problems)} problem(s):")
        for p in problems:
            print(" -", p)
        if write:
            raise SystemExit("not written")
        return
    print("OK")
    if write:
        assert REPORT.read_bytes() == live, "report changed during merge"
        REPORT.write_bytes(merged.encode("utf-8"))
        (HERE / "report_after_rewrite.md").write_bytes(merged.encode("utf-8"))
        print("written", REPORT)


if __name__ == "__main__":
    main("--write" in sys.argv)
