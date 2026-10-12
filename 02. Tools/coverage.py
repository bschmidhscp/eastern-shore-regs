"""One-page coverage report for a county: what we have, what's missing, what needs attention.

Writes <County>/02. Coverage Report.md. Run after the pipeline (and again after digests/summary).

Usage: python -I "02. Tools/coverage.py" --county Kent
"""
import argparse
import csv
import datetime as dt
import json
import re
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from common import CORPUS, county_dir, county_name, read_manifest  # noqa: E402

EXPECTED = [  # (label, test on manifest rows / files, why it matters)
    ("County code (zoning + subdivision)", lambda m, c: any("/Code/" in p for p in m) and (c / "Code").exists(), "the rules"),
    ("Comprehensive plan", lambda m, c: any(re.search(r"comp(rehensive)?.?plan", p, re.I) for p in m), "growth areas, densities"),
    ("Water & sewer plan or amendments", lambda m, c: any(re.search(r"water.?(and|&).?sewer|cwsp|wastewater", p, re.I) for p in m), "where sewer can go"),
    ("Planning/zoning fee schedule", lambda m, c: any("/Fees/" in p for p in m), "application costs"),
    ("Impact or excise fees for new homes", lambda m, c: any(re.search(r"impact|excise", p, re.I) for p in m), "per-lot costs"),
    ("Planning Commission minutes", lambda m, c: any("Planning Commission/" in p for p in m), "how approvals go"),
    ("Board of Appeals decisions or minutes", lambda m, c: any("Board of Appeals" in p for p in m), "variance odds"),
    ("Council/Commissioner minutes", lambda m, c: any(re.search(r"County (Council|Commissioners)/", p) for p in m), "legislative signals"),
    ("Bills / ordinances", lambda m, c: any("Legislation/Bills" in p for p in m), "recent amendments"),
    ("Resolutions", lambda m, c: any("Legislation/Resolutions" in p for p in m), "W&S amendments, fees"),
    ("Map layers", lambda m, c: any("/Maps/" in p for p in m), "parcel screening"),
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--county", required=True)
    a = ap.parse_args()
    cname = county_name(a.county)
    cdir = county_dir(cname)
    man = read_manifest(cname)
    cfg_p = Path(__file__).parent / "County Configs" / f"{cname}.json"
    cfg = json.loads(cfg_p.read_text()) if cfg_p.exists() else {}

    by_folder = Counter("/".join(Path(p).parts[2:4]) if Path(p).parts[1] == "Originals" else Path(p).parts[1]
                        for p in man)
    ocr = sum(1 for r in man.values() if "needs_ocr" in r.get("notes", ""))
    no_text = sum(1 for p, r in man.items() if p.lower().endswith(".pdf") and not r.get("text_path"))
    code_through = next((r["effective"] for p, r in man.items() if "eCode360" in p or "/Originals/Code/" in p and r.get("effective")), "")
    digests = sorted(x.name for x in (cdir / "01. Digests").glob("*.md")) if (cdir / "01. Digests").exists() else []
    summary = (cdir / "00. Summary.md").exists()

    L = [f"# {cname} — Coverage Report", "", f"*Generated {dt.date.today()} by `02. Tools/coverage.py`.*", "",
         "## Checklist", "", "| Item | Status | Why it matters |", "|---|---|---|"]
    docs = cfg.get("documents") or {}
    for label, test, why in EXPECTED:
        if test(man, cdir):
            status = "✅"
        elif label.startswith("Impact") and re.match(r"(none|no )", str(docs.get("impact_fees", "")), re.I):
            status = "— none (county has no impact fee)"
        elif label == "Map layers":
            status = "— via statewide layers (`gis_point_lookup.py`)"
        else:
            status = "❌ missing"
        L.append(f"| {label} | {status} | {why} |")
    L += [f"| County summary (layer 1) | {'✅' if summary else '❌ not yet'} | read-first page |",
          f"| Digests (layer 2) | {', '.join(d[:-3] for d in digests) or '❌ none'} | one line per item |", "",
          "## Counts", "", f"- Files in manifest: {len(man)}",
          f"- Code currency: {code_through or 'unknown'}",
          f"- Scanned PDFs still needing OCR: {ocr}", f"- PDFs without text: {no_text}", "",
          "| Folder | Files |", "|---|---|"]
    L += [f"| {k} | {v} |" for k, v in sorted(by_folder.items(), key=lambda x: (-x[1], x[0]))[:25]]
    if cfg.get("notes") or cfg.get("documents"):
        L += ["", "## From the county config", ""]
        for k, v in (cfg.get("documents") or {}).items():
            if isinstance(v, str) and not v.startswith("http"):
                L.append(f"- {k}: {v}")
        if cfg.get("notes"):
            L.append(f"- Notes: {cfg['notes']}")
    (cdir / "02. Coverage Report.md").write_text("\n".join(L) + "\n")
    print("\n".join(L[:20]))


if __name__ == "__main__":
    main()
