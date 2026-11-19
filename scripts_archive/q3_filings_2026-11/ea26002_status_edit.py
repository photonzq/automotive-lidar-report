"""Status of NHTSA's EA26002 on 18 Nov 2026, the due date of Tesla's complete answer to question 9 (§E12, §F8,
Appendix 1, Appendix 2).

Sources, read in full: the investigation's record on NHTSA's site (NHTSA ID search; open investigation, 19 associated
documents with their titles); the posting date of each document (Last-Modified of static.nhtsa.gov; the last ones on
25 Sep 2026); the memo granting the Q9 extension (22 Sep 2026, INRE-EA26002-17279: Tesla's request of 14 Sep, Q9 to
18 Nov 2026); the ODI-Tesla correspondence on that request (INRE-EA26002-17277: ODI's request of 22 Sep for a partial
Q9 answer by 23 Sep, with the VINs identified so far and the documents of the incidents already reviewed, and its
statement that the "available documents" of Q9 include every document for each incident, such as tickets and
internal assessments; the portal page of the first extension, Q3, Q4, Q5, Q9, Q10, Q11, Q13 and Q16 to 23 Sep); and
the Q9 placeholder created 24 Sep (INCCS-EA26002-17721: the documents responsive to Q9 carry a request for
confidential treatment of the entirety of each document). Placeholders exist for questions 1-3, 5, 9-11, 13, 16, 19,
21, 22 and 24; none for Q4.

Usage: ea26002_status_edit.py <report.md> <expected sha256 prefix> [--write]
"""
import hashlib
import sys
from pathlib import Path

report, expected = Path(sys.argv[1]), sys.argv[2]
raw = report.read_bytes()
sha = hashlib.sha256(raw).hexdigest()
assert sha.startswith(expected), f"report changed: sha {sha[:12]} != {expected}"
text = raw.decode("utf-8")
assert "\r" not in text

ODI = "https://static.nhtsa.gov/odi/inv/2026/"
EDITS = [
    # ---- §E12: the status bullet under Information Request EA26002-01
    ("- No recall or closure had appeared by 3 Oct 2026 [P, NHTSA recall data and ODI file]. NHTSA extended most of "
     "Tesla's answers to 23 Sep 2026 and the crash-by-crash question (Q9, which asks whether \"Vision Failsafe Ranker\" "
     "and \"Direct Photon Count Capability\" were installed) to 18 Nov 2026. Tesla filed its answers with requests for "
     "confidential treatment of each whole document, and the file holds no entry for the \"Radar Saves Us\" question "
     "(Q4) [P, ODI file] ([IR letter](https://static.nhtsa.gov/odi/inv/2026/INIM-EA26002-14414.pdf)).\n",
     "- On 18 Nov 2026 the investigation was still open, with no recall in its record, and its public file held 19 "
     "documents, the last of them posted on 25 Sep [P, ODI file]. NHTSA extended most of Tesla's answers to 23 Sep "
     "2026 and, at Tesla's request of 14 Sep, the crash-by-crash question (Q9, which asks whether \"Vision Failsafe "
     "Ranker\" and \"Direct Photon Count Capability\" were installed) to 18 Nov 2026 [P, extension memo of 22 Sep]. "
     "When it processed that extension, ODI asked for a partial answer to Q9 by 23 Sep, with the VINs identified so "
     "far and the documents of the incidents Tesla had already reviewed, and wrote that the \"available documents\" "
     "of Q9 include every document for each incident, such as tickets and internal assessments [P, ODI–Tesla "
     "correspondence].\n"
     "- Tesla filed its answers with requests for confidential treatment of each whole document. The file holds such "
     "placeholders for questions 1–3, 5, 9–11, 13, 16, 19, 21, 22 and 24, the Q9 one dated 24 Sep, but none for the "
     "\"Radar Saves Us\" question (Q4), and no part of the complete Q9 answer due on 18 Nov had been posted by that "
     "day [P, ODI file] ([IR letter](" + ODI + "INIM-EA26002-14414.pdf); [extension memo](" + ODI +
     "INRE-EA26002-17279.pdf); [Q9 correspondence](" + ODI + "INRE-EA26002-17277.pdf); [Q9 placeholder](" + ODI +
     "INCCS-EA26002-17721.pdf)).\n"),
    # ---- §F8 signpost 1
    ("later extended to 23 Sep and, for the crash-by-crash answers, 18 Nov 2026; answers filed as confidential; no "
     "recall or closure by 3 Oct 2026)",
     "later extended to 23 Sep and, for the crash-by-crash answers, 18 Nov 2026; answers filed as confidential, a "
     "partial crash-by-crash answer of 24 Sep included; still open, with no recall, on 18 Nov 2026)"),
    # ---- Appendix 1
    ("- **NHTSA EA26002:** the investigation is open with no recall. Tesla's answers were filed with requests for "
     "confidential treatment, and NHTSA extended the crash-by-crash question to 18 Nov 2026 [P]. It bears on "
     "confidence in Tesla's camera-only design (§F7, §F8 signpost 1).\n",
     "- **NHTSA EA26002:** the investigation was still open on 18 Nov 2026, with no recall in its record. Tesla filed "
     "its answers, a partial crash-by-crash answer (Q9) of 24 Sep included, with requests for confidential treatment "
     "of each whole document, and the complete Q9 answer due on 18 Nov had not been posted that day [P]. Unknown: "
     "what the Q9 answers show about the \"Vision Failsafe Ranker\" and \"Direct Photon Count Capability\" features, "
     "and whether ODI will make any of them public. It bears on confidence in Tesla's camera-only design (§F7, §F8 "
     "signpost 1).\n"),
    # ---- Appendix 2
    ("- NHTSA EA26002 information request, including \"Radar Saves Us\": " + ODI + "INIM-EA26002-14414.pdf\n",
     "- NHTSA EA26002 information request, including \"Radar Saves Us\": " + ODI + "INIM-EA26002-14414.pdf\n"
     "- NHTSA EA26002, memo granting the Q9 extension to 18 Nov 2026 (22 Sep 2026): " + ODI + "INRE-EA26002-17279.pdf\n"
     "- NHTSA EA26002, ODI–Tesla correspondence on the Q9 extension and partial answer (11–22 Sep 2026): " + ODI +
     "INRE-EA26002-17277.pdf\n"
     "- NHTSA EA26002, placeholder for the confidential Q9 documents (24 Sep 2026): " + ODI +
     "INCCS-EA26002-17721.pdf\n"),
]

new = text
for old, rep in EDITS:
    n = new.count(old)
    assert n == 1, f"anchor found {n} times: {old[:90]!r}"
    new = new.replace(old, rep, 1)
assert "\r" not in new
print(f"{len(EDITS)} edits; sha256 before {sha[:12]}, after {hashlib.sha256(new.encode('utf-8')).hexdigest()[:12]}")
if "--write" in sys.argv[3:]:
    report.write_bytes(new.encode("utf-8"))
    print("written")
