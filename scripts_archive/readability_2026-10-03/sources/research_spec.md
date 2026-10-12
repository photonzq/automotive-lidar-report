# Round 4 source research: specification for each research agent

## Task

You are given one items file: `sources/<group>_items.md`. Each item is a claim in the report that needs a source, a check, or a number.

- Research every item now, on the web, from the best source you can reach.
- Read the source itself, not a summary of it.
- Write your findings to `sources/<group>_findings.md`.
- Do not edit the report or any file outside `sources/`.

Paths:
- Report (Markdown, about 1.86 MB, read-only for you): `<report folder>\automotive_perception_report_2026-09-27.md`
- Folder for your output: `<report folder>\scripts_archive\readability_2026-10-03\sources\`

The quoted "Where" text in an item may predate an edit made since. Find the current wording in the report, for example with a text search. Copy it verbatim into your proposed edit.

## How to research

1. **Prefer primary sources.** These are:
   - company datasheets, filings and releases;
   - standards and regulations;
   - the paper itself, rather than a survey quoting it.

   Use independent sources next: peer-reviewed papers, government statistics, independent tests. Use trade press and secondary relays only when nothing better exists, and say so.
2. **Download PDFs freely.** To read one, render its pages to PNG with PyMuPDF at 160 dpi and read the images. Interpreter: `python`. Put the images in your own temporary folder.
   - Use `page.get_text()` only to locate the right page. Never rely on it alone for tables, figures or numbers.
3. **Do not bypass paywalls.** If the original is paywalled, look for an author copy, an arXiv version or the abstract, and say which one you read.
4. **Use no email address anywhere.** Not in HTTP headers, not as a `mailto` parameter, not in Crossref or Unpaywall "polite pool" requests, and not in forms.
5. **Archive every script you write** in `sources/scripts/`, with one line per script in `sources/scripts/INDEX.md`.
   - Remove user names from paths; use placeholders such as `<report>`.
   - No credentials of any kind.
6. **Keep quotations short.** At most about 15 words, and only where the exact wording matters; otherwise paraphrase.

## Output format: `sources/<group>_findings.md`

One section per item, using the item's id as the heading. Each section has these fields:

- **Question:** one sentence.
- **Answer:** the fact or number, with its unit and any condition. If the item asks for a calculation, show the equation, the inputs, the substitution and the result.
- **Source:** full citation, with title, author or organization, date, URL, and the page, table or figure number. Say which version you read: the full text, the abstract, or an archived copy.
- **Evidence tag**, from the report's legend:
  - [P] a primary document (the company's own, a regulator's or a standard's);
  - [I] an independent source (peer-reviewed or academic, government statistics, independent test);
  - [T] trade press;
  - [S] a secondary relay, such as Wikipedia or a survey quoting the original;
  - [MR] market research;
  - [U] unverified, only when nothing was found.
- **Confidence:** high, medium or low, with one clause of reason.
- **Proposed edit:**
  - `old`: the exact current text, copied verbatim from the report and long enough to be unique;
  - `new`: the replacement.
  - Write the replacement in the report's style:
    - full sentences;
    - math in `$...$`;
    - currency as `\$`;
    - the evidence tag in square brackets after the claim;
    - no versioning words ("corrected", "updated", "revised", "now", "newly", "added");
    - no notes to the reader about the editing.
  - Change only the sentence or table cell concerned.
- **Appendix 2 entry:** one line in the format of the report's Appendix 2, with the URL. Write "none" if the source is already listed.

If nothing usable is found after a reasonable search:
- list what you searched;
- propose the smallest wording change that marks the claim [U], or drop the claim if it cannot stand.

## Finish

When every item is answered:
- check that each `old` string occurs exactly once in the report;
- reply in three lines: how many items were sourced, how many were tagged [U], and how many were blocked, with the reason for each blocked one.
