"""Replace short quoted source fragments in the findings file with paraphrases.

Usage: python -I dequote.py FILE
Each pair is applied once; the script reports any pair it could not find.
"""
import sys

sys.stdout.reconfigure(encoding="utf-8")
path = sys.argv[1]
t = open(path, encoding="utf-8").read()

pairs = [
    ('(the Edge AI and Vision Alliance reprints Yole Group articles "with the permission of the Yole Group", as each reprint states at its top)',
     "(the Edge AI and Vision Alliance states at the top of each reprint that it republishes the Yole Group article with Yole's permission)"),
    ('says that Iris, "like the Hesai AT128", uses a self-developed receiver ASIC',
     'says that Iris, like the Hesai AT128, uses a self-developed receiver ASIC'),
    ('The summary also gives "Price: \\$4,847", which',
     'The summary also gives a price of \\$4,847, which'),
    ('Texas Instruments ICs and "2D MEMS mirrors", with range',
     'Texas Instruments ICs and two-axis MEMS mirrors, with range'),
    ('the Xueling summary only says the transceiver modules were "greatly simplified".',
     'the Xueling summary only says that the transceiver modules were greatly simplified.'),
    ('the release gives its rating as 75 W "in 150ns".',
     'the release gives its rating as 75 W together with a 150 ns figure.'),
    ('(TechInsights writes "light emitting diodes")',
     '(TechInsights calls them light-emitting diodes)'),
    ('consistent with "about 100,000 effective" plus unused edge cells.',
     "consistent with Sony's figure of about 100,000 effective pixels plus unused edge cells."),
    ('offers "a complimentary report of the Huawei 192 Line Lidar" through',
     'offers a free TechInsights report on the Huawei 192-line lidar through'),
    ('citing "industry analysis"',
     'citing unnamed industry analysis'),
    ('consistent with "over 100" mesas at one mesa per spot.',
     "consistent with Yole's count of more than 100 mesas at one mesa per spot."),
    ('and "optical fiber (unusual application)" listed as the innovation',
     'and optical fibre listed as an unusual design choice'),
    ('which is Yole\'s "1.9 times".',
     "which matches Yole's factor of 1.9."),
    ('The Yole text says "erbium-doped fibre";',
     'The Yole text says erbium-doped fibre;'),
    ('of which "modules, discretes and connectors" (which would include the fibre laser module) is 53%.',
     'of which the category of modules, discretes and connectors (which would include the fibre laser module) is 53%.'),
    ('The single verbatim quotation in this file is the Yole figure label in the AT128 entry.',
     'Apart from titles, section names, chip markings and bill-of-materials item names, the single verbatim quotation in this file is the Yole figure label in the AT128 entry.'),
]
missing = []
for old, new in pairs:
    if old in t:
        t = t.replace(old, new, 1)
    else:
        missing.append(old)
open(path, "w", encoding="utf-8", newline="\n").write(t)
print("applied", len(pairs) - len(missing), "of", len(pairs))
for m in missing:
    print("NOT FOUND:", m)
