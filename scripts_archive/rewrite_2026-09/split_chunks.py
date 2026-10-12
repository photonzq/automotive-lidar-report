"""Split the report into rewrite chunks at fixed heading boundaries (1-based start lines)."""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPORT = Path(r"<report folder>\automotive_perception_report_2026-09-27.md")

# (chunk id, first heading text that starts the chunk)
BOUNDS = [
    ("01", "# Automotive Night Vision, Lidar and the Sensor Debate"),
    ("02", "# Part B — Lidar markets: China vs outside China"),
    ("03", "## B8. Beyond cars"),
    ("04", "# Part C — Technology routes and physics"),
    ("05", "## C1. Taxonomy"),
    ("06", "## C3b. Reading flagship spec sheets"),
    ("07", "## C4c. Wavelength selection in numbers"),
    ("08", "## C5a. Sony's automotive SPAD sensors"),
    ("09", "## C7. FMCW and non-mechanical beam steering"),
    ("10", "## C7b. Can FMCW win?"),
    ("11", "## C9. Lidar-to-lidar interference"),
    ("12", "### C10.3a Physical background"),
    ("13", "# Part D — Supply chain and geopolitics"),
    ("14", "# Part E — Can camera-only"),
    ("15", "## E11. Does lidar help or hinder"),
    ("16", "# Part F — Projections"),
    ("TAIL", "# Appendix 2 — Selected sources"),
]


def main() -> None:
    raw = REPORT.read_bytes()
    text = raw.decode("utf-8")
    lines = text.split("\n")
    starts = []
    for cid, head in BOUNDS:
        idx = [i for i, l in enumerate(lines) if l.startswith(head)]
        assert len(idx) == 1, (cid, head, idx)
        starts.append((cid, idx[0]))
    assert [s for _, s in starts] == sorted(s for _, s in starts)
    meta = {}
    for k, (cid, s) in enumerate(starts):
        e = starts[k + 1][1] if k + 1 < len(starts) else len(lines)
        body = "\n".join(lines[s:e])
        d = HERE / f"chunk{cid}"
        d.mkdir(exist_ok=True)
        (d / f"chunk{cid}_original.md").write_text(body, encoding="utf-8")
        if cid != "TAIL":
            (d / f"chunk{cid}.md").write_text(body, encoding="utf-8")
        meta[cid] = dict(start_line=s + 1, end_line=e, bytes=len(body.encode("utf-8")))
    (HERE / "chunks.json").write_text(json.dumps(meta, indent=1), encoding="utf-8")
    (HERE / "base_report.md").write_bytes(raw)
    # the split must reassemble exactly
    re_joined = "\n".join((HERE / f"chunk{cid}" / f"chunk{cid}_original.md").read_text(encoding="utf-8")
                          for cid, _ in starts)
    assert re_joined == text, "split does not reassemble"
    for cid, m in meta.items():
        print(cid, m)


if __name__ == "__main__":
    main()
