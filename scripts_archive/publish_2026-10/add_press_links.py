"""Link each press article in Appendix 2 ("Press articles (paywalled)") to its publisher's page (10 Oct 2026),
hash-guarded. The links come from a JSON list of {"title", "url"} found by a search of the publishers' sites; a
quoted title in the appendix is matched to the closest listed title (difflib ratio >= 0.85) and wrapped as a link.
Titles without a match stay as plain text and are listed.

Usage:
    python add_press_links.py --report <report.md> --links <links.json> --expect <sha256 prefix> [--dry]
"""
import argparse
import difflib
import hashlib
import json
import re
import sys
from pathlib import Path

ap = argparse.ArgumentParser()
ap.add_argument("--report", required=True)
ap.add_argument("--links", required=True)
ap.add_argument("--expect", required=True)
ap.add_argument("--dry", action="store_true")
args = ap.parse_args()

RP = Path(args.report)
raw = RP.read_bytes()
h0 = hashlib.sha256(raw).hexdigest()
if not h0.startswith(args.expect):
    sys.exit(f"ABORT: report sha {h0[:12]} is not the expected {args.expect}")
links = json.loads(Path(args.links).read_text(encoding="utf-8"))


def norm(s):
    return re.sub(r"[^a-z0-9]+", " ", s.lower().replace("…", "...")).strip()


cands = {norm(x["title"]): x["url"] for x in links if x.get("url")}
L = raw.decode("utf-8").split("\n")
start = [i for i, l in enumerate(L) if l.startswith("**Press articles (paywalled).**")]
if len(start) != 1:
    sys.exit(f"ABORT: heading found {len(start)} times")
i = start[0] + 1
done, missing = 0, []
while i < len(L) and L[i].startswith("- "):
    def wrap(m):
        global done
        title = m.group(1)
        best = difflib.get_close_matches(norm(title), list(cands), n=1, cutoff=0.85)
        if not best:
            missing.append(title)
            return m.group(0)
        done += 1
        return f'["{title}"]({cands[best[0]]})'
    L[i] = re.sub(r'(?<!\[)"([^"]+)"(?!\]\()', wrap, L[i])
    i += 1
out = "\n".join(L).encode("utf-8")
print(f"{done} titles linked; {len(missing)} without a link: {missing}")
print(f"{h0[:12]} -> {hashlib.sha256(out).hexdigest()[:12]}")
if args.dry:
    sys.exit(0)
if hashlib.sha256(RP.read_bytes()).hexdigest() != h0:
    sys.exit("ABORT: report changed during processing")
RP.write_bytes(out)
print("written")
