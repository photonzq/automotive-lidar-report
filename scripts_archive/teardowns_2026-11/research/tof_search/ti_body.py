"""Print the main body of saved TechInsights pages (text after the page title
heading, stopping at the 'latest insights' teaser block).

Usage: python -I ti_body.py NAME [NAME ...]   (reads ../raw/NAME.txt)
"""
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")
here = os.path.dirname(os.path.abspath(__file__))
rawdir = os.path.join(os.path.dirname(here), "raw")

STOP_MARKERS = [
    "The Authoritative Information Platform",
    "Learn More \n",
]

for name in sys.argv[1:]:
    t = open(os.path.join(rawdir, name + ".txt"), encoding="utf-8").read()
    # main content follows the second occurrence of "Free Sign Up"
    k = t.find("Free Sign Up")
    k2 = t.find("Free Sign Up", k + 10)
    start = k2 if k2 > 0 else 0
    end = len(t)
    for m in STOP_MARKERS:
        j = t.find(m, start)
        if 0 < j < end:
            end = j
    print("=" * 30, name, "=" * 30)
    print(t[start:end][:6000])
