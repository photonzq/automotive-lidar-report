"""Convert a JATS full-text XML (e.g. from the Europe PMC REST API) to readable text.

Usage:
  python R4_jats_to_text.py <article.xml> <out.txt>

Keeps section titles, paragraphs, figure and table captions, table cells (one
row per line, cells separated by " | "), display formulas (as their TeX or
MathML text) and the reference list. Paths come from the command line
(e.g. <scratch>/r4); nothing is hard-coded. No network access.
"""
import sys
import xml.etree.ElementTree as ET


def text_of(el):
    return " ".join("".join(el.itertext()).split())


def walk(el, out, depth=0):
    tag = el.tag.split("}")[-1]
    if tag == "title":
        out.append("\n" + "#" * min(depth, 4) + " " + text_of(el))
        return
    if tag in ("p", "disp-formula"):
        out.append(text_of(el))
        return
    if tag in ("fig", "table-wrap"):
        cap = el.find(".//{*}caption")
        lab = el.find("{*}label")
        out.append(f"\n[{tag.upper()} {text_of(lab) if lab is not None else ''}] "
                   f"{text_of(cap) if cap is not None else ''}")
        for tr in el.iter():
            if tr.tag.split("}")[-1] == "tr":
                cells = [text_of(c) for c in tr if c.tag.split("}")[-1] in ("td", "th")]
                out.append(" | ".join(cells))
        foot = el.find(".//{*}table-wrap-foot")
        if foot is not None:
            out.append("[table foot] " + text_of(foot))
        return
    if tag == "ref":
        out.append("[ref] " + text_of(el))
        return
    for ch in el:
        walk(ch, out, depth + (1 if tag == "sec" else 0))


def first(node, name):
    """Return the first descendant called `name`, with or without a namespace."""
    hit = node.find(".//{*}" + name)
    return hit if hit is not None else node.find(".//" + name)


def main(src, dst):
    root = ET.parse(src).getroot()
    out = []
    front = first(root, "article-meta")
    if front is not None:
        t = first(front, "article-title")
        if t is not None:
            out.append("TITLE: " + text_of(t))
        ab = first(front, "abstract")
        if ab is not None:
            out.append("ABSTRACT: " + text_of(ab))
    for part in ("body", "back"):
        node = first(root, part)
        if node is not None:
            out.append(f"\n==== {part.upper()} ====")
            walk(node, out)
    with open(dst, "w", encoding="utf-8") as f:
        f.write("\n".join(out))
    print(f"wrote {dst}: {sum(len(x) for x in out)} characters")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
