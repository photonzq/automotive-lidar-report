"""Escape currency dollar signs in a Markdown file that also uses $...$ math.

Math spans are recognised as $...$ pairs on one line whose content contains a
LaTeX command (a backslash). Every other "$" that is directly followed by a
digit is a currency sign and becomes "\\$", so KaTeX-style renderers do not
treat prices as math delimiters. Prints the math spans it kept and the number
of escapes it made.

Usage: python -I escape_currency.py FILE
"""
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")
path = sys.argv[1]
text = open(path, encoding="utf-8").read()

math_re = re.compile(r"\$(?!\s)([^$\n]*?\\[A-Za-z]+[^$\n]*?)\$")
spans = []


def protect(m):
    spans.append(m.group(0))
    return f"\x00MATH{len(spans) - 1}\x00"


protected = math_re.sub(protect, text)
count = len(re.findall(r"(?<!\\)\$(?=\d)", protected))
protected = re.sub(r"(?<!\\)\$(?=\d)", r"\\$", protected)
leftover = re.findall(r"(?<!\\)\$", protected)
for i, s in enumerate(spans):
    protected = protected.replace(f"\x00MATH{i}\x00", s)
open(path, "w", encoding="utf-8", newline="\n").write(protected)
print("math spans kept:", len(spans))
for s in spans:
    print("   ", s)
print("currency signs escaped:", count)
print("unescaped $ left outside math:", len(leftover))
