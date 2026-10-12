"""Texts for the public version (10 Oct 2026; applied with ../gapfill_2026-10/edits_partB_definitive.py
--texts publish_texts --name publish). The author asked to remove every "read in full" mention, to drop the pointers
to the private refs/ folder of press copies, and to give public links where possible.

Entries are (id, unique start of the report line, change); see ../gapfill_2026-10/partB_definitive_texts.py.
The per-article links of Appendix 2 are added by add_press_links.py.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "gapfill_2026-10"))

SAHA_DOI = "https://doi.org/10.1038/s41586-025-10038-6"
ISSCC_DOI = "https://doi.org/10.1109/ISSCC42613.2021.9365961"

EDITS = [
    ("isscc-7-3", "- **Measured** [P, ISSCC 2021 paper 7.3, read in full; curve",
     ("sub", "[P, ISSCC 2021 paper 7.3, read in full; curve values E]",
      f"[P, [ISSCC 2021 paper 7.3]({ISSCC_DOI}); curve values E]")),
    ("park-predecessor", "- **The device class**, from the group's open-access predece",
     ("sub", "from the group's open-access predecessor, read in full [P;", "from the group's open-access predecessor [P;")),
    ("saha-case-study", '**Case study: the "photonic ski-jump"** [P: M. Saha',
     ("sub", "open access; read in full; copy in `refs/`].", f"open access, {SAHA_DOI}].")),
    ("saha-sources", "Sources: https://doi.org/10.1038/s41586-025-10038-6 (copy: `",
     ("sub", " (copy: `refs/2026-03-12_Nature_Saha-et-al_Nanophotonic-waveguide-chip-to-world-beam-scanning.pdf`)", "")),
    ("g7-sample", "These judgements come from reading the 43 press printouts in",
     ("sub", "These judgements come from reading the 43 press printouts in `refs/INDEX.md` in date order (FT, WSJ, NYT, "
             "The Economist, Nikkei Asia, The Washington Post).",
      "These judgements come from 43 press articles taken in date order (FT, WSJ, NYT, The Economist, Nikkei Asia, "
      "The Washington Post), listed with links in Appendix 2.")),
    ("appx1-sony-yonsei", "- **Sony and Yonsei papers:** Sony's ISSCC 2021 paper 7.3 is",
     ("sub", "Sony's ISSCC 2021 paper 7.3 is read in full (§C5a). The VLSI 2025 T1-2 and C27-2 papers, the JSSC 2026 "
             "paper and Yonsei's VLSI 2025 T5-4 are closed access and were read only as abstracts.",
      "Sony's ISSCC 2021 paper 7.3 is covered in §C5a. The VLSI 2025 T1-2 and C27-2 papers, the JSSC 2026 paper and "
      "Yonsei's VLSI 2025 T5-4 are closed access, and only their abstracts are public.")),
    ("appx2-press-heading", "**Paywalled press read in full (printouts supplied by the re",
     "**Press articles (paywalled).** Each title links to the publisher's page."),
]
