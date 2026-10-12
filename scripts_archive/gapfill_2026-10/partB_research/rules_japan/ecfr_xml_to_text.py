"""Convert an eCFR versioner XML file to plain text (one paragraph per line).

Usage:
    python ecfr_xml_to_text.py INPUT.xml OUTPUT.txt
"""
import sys
import xml.etree.ElementTree as ET


def walk(el, out):
    tag = el.tag
    if tag in ("HEAD", "P", "FP", "HD1", "HD2", "HD3", "CITA", "AUTH", "SOURCE"):
        text = "".join(el.itertext()).strip()
        if text:
            out.append(("\n## " if tag == "HEAD" else "") + " ".join(text.split()))
        return
    for child in el:
        walk(child, out)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    root = ET.parse(sys.argv[1]).getroot()
    lines = []
    walk(root, lines)
    with open(sys.argv[2], "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print(f"wrote {len(lines)} paragraphs to {sys.argv[2]}")
