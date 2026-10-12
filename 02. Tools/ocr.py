"""OCR scanned PDFs (manifest rows flagged needs_ocr) and rewrite their markdown text.

Originals are never modified: OCR runs on a temp copy and only the extracted text is kept.
Requires ocrmypdf (brew install ocrmypdf).

Usage: python -I "02. Tools/ocr.py" --county Talbot [--workers 6]
"""
import argparse
import re
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from common import CORPUS, read_manifest, upsert_manifest, write_md  # noqa: E402
from to_text import target_for  # noqa: E402


def ocr_one(item):
    path, row = item
    src = CORPUS / path
    with tempfile.TemporaryDirectory() as td:
        side = Path(td) / "text.txt"
        r = subprocess.run(["ocrmypdf", "--force-ocr", "--output-type", "pdf", "-q", "--sidecar", str(side),
                            str(src), str(Path(td) / "out.pdf")], capture_output=True, text=True)
        if r.returncode != 0 or not side.exists():
            return path, None, r.stderr[-200:]
        pages = side.read_text(errors="replace").split("\f")
    pages = [p.strip() for p in pages if p.strip() or len(pages) > 1]
    text = "\n\n".join(f"<!-- page {i} -->\n{t}" for i, t in enumerate(pages, 1))
    dest = target_for(row)
    meta = dict(county=row["county"], category=row["category"], title=row["title"],
                source_url=row["source_url"], effective=row["effective"], retrieved=row["retrieved"],
                original=path, pages=len(pages), needs_ocr="no", ocr="yes (tesseract)")
    write_md(dest, meta, f"# {row['title']}\n\n{text}")
    notes = row.get("notes", "").replace("needs_ocr", "ocr").strip("; ")
    return path, {**row, "text_path": str(dest.relative_to(CORPUS)), "notes": notes}, None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--county", required=True)
    ap.add_argument("--workers", type=int, default=6)
    ap.add_argument("--max-pages", type=int, default=60, help="skip non-essential scans longer than this")
    ap.add_argument("--all", action="store_true", help="OCR everything, including packets and long scans")
    a = ap.parse_args()
    import pymupdf as fitz
    todo, deferred = [], []
    for p, r in read_manifest(a.county).items():
        if "needs_ocr" not in r.get("notes", "") or not p.lower().endswith(".pdf"):
            continue
        # Targeted OCR: always do decisions, minutes, plans, fees, code; skip meeting packets and
        # very long scans of anything else (searchable later with --all).
        try:
            n = len(fitz.open(CORPUS / p))
        except Exception:
            n = 0
        important = re.search(r"/(Plans|Fees|Code|Legislation)/|Decision|Minutes", p) and not re.search(r"packet", p, re.I)
        if a.all or (important and n <= 300) or n <= a.max_pages and not re.search(r"packet", p, re.I):
            todo.append((p, r))
        else:
            deferred.append((p, n))
    print(f"{len(todo)} scanned PDFs to OCR; {len(deferred)} deferred (packets/long scans; run with --all)", flush=True)
    done, failed = [], []
    with ThreadPoolExecutor(a.workers) as ex:
        for i, (path, new, err) in enumerate(ex.map(ocr_one, todo), 1):
            (failed if err else done).append((path, new, err))
            if i % 20 == 0:
                print(f"  {i}/{len(todo)}", flush=True)
    upsert_manifest(a.county, [n for _, n, _ in done])
    print(f"OCR'd {len(done)}; failed {len(failed)}")
    for p, _, e in failed:
        print("  !", p, e)


if __name__ == "__main__":
    main()
