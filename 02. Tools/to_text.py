"""Convert downloaded documents (PDF, DOCX, XLSX) to searchable markdown.

For every manifest row of a county whose file is a document and has no text_path yet
(or --force), writes a markdown copy that mirrors the Originals folder:
  <County>/Originals/<Sub>/<name>.pdf                 -> <County>/Documents/<Sub>/<name>.md
  <County>/Originals/Meeting Minutes/<Body>/<name>   -> <County>/Meeting Minutes/<Body>/<name>.md
with front matter and "<!-- page N -->" markers, and records text_path in the manifest.

Pages with almost no extractable text are flagged needs_ocr (scanned) so they can be OCR'd later.

Usage: python -I "02. Tools/to_text.py" --county Talbot [--force] [--only <substring of path>] [--workers 8]
"""
import argparse
from concurrent.futures import ProcessPoolExecutor
import subprocess
import sys
from pathlib import Path

import pymupdf as fitz
import pymupdf4llm

sys.path.insert(0, str(Path(__file__).parent))
from common import CORPUS, KIND_FOLDER, county_dir, county_name, read_manifest, upsert_manifest, write_md  # noqa: E402

DOC_EXT = {".pdf", ".docx", ".doc", ".xlsx", ".xls", ".rtf", ".txt", ".html"}
LAYOUT_MAX_PAGES = 60  # table-aware conversion is slow; long plans use plain text


def pdf_text(p):
    """Table-aware markdown via pymupdf4llm; plain text fallback for very long or odd PDFs."""
    doc = fitz.open(p)
    n = len(doc)
    try:
        if n > LAYOUT_MAX_PAGES:
            raise ValueError("too long for layout mode")
        chunks = pymupdf4llm.to_markdown(doc, page_chunks=True, show_progress=False)
        texts = [c["text"].strip() for c in chunks]
    except Exception:
        texts = [page.get_text("text").strip() for page in doc]
    empty = sum(1 for t in texts if len(t) < 40)
    parts = [f"<!-- page {i} -->\n{t}" for i, t in enumerate(texts, 1)]
    return "\n\n".join(parts), n, empty


def office_text(p):
    if p.suffix.lower() in (".xlsx", ".xls"):
        try:
            import openpyxl
        except ImportError:
            return "*(spreadsheet — install openpyxl to convert)*", 0, 0
        wb = openpyxl.load_workbook(p, data_only=True, read_only=True)
        out = []
        for ws in wb.worksheets:
            out.append(f"## Sheet: {ws.title}")
            for row in ws.iter_rows(values_only=True):
                if any(c is not None for c in row):
                    out.append(" | ".join("" if c is None else str(c) for c in row))
        return "\n".join(out), 0, 0
    if p.suffix.lower() == ".txt":
        return p.read_text(errors="replace"), 0, 0
    if p.suffix.lower() == ".html":
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(p.read_text(errors="replace"), "lxml")
        for t in soup(["script", "style"]):
            t.decompose()
        return "\n".join(l.strip() for l in soup.get_text("\n").splitlines() if l.strip()), 0, 0
    r = subprocess.run(["pandoc", str(p), "-t", "gfm", "--wrap=none"], capture_output=True, text=True)
    return (r.stdout if r.returncode == 0 else f"*(conversion failed: {r.stderr[:200]})*"), 0, 0


def target_for(row):
    parts = Path(row["path"]).parts  # <County>/Originals/<Sub...>/<file>
    base, name = CORPUS / parts[0], Path(row["path"]).stem
    sub = Path(*parts[2:-1]) if len(parts) > 3 and parts[1] == "Originals" else Path(
        KIND_FOLDER.get(row["category"] or "other", "Other"))
    if sub.parts and sub.parts[0] == "Meeting Minutes":
        return base / sub / f"{name}.md"
    return base / "Documents" / sub / f"{name}.md"


class _Timeout(Exception):
    pass


def _alarm(*_):
    raise _Timeout()


def convert(item):
    """Worker: convert one document; returns (path, updated_row or None, flagged, error).
    Each document gets 120 s for table-aware conversion, then falls back to plain text (30 s)."""
    import signal
    path, row = item
    src = CORPUS / path
    signal.signal(signal.SIGALRM, _alarm)
    try:
        signal.alarm(120)
        if src.suffix.lower() == ".pdf":
            text, pages, empty = pdf_text(src)
        else:
            text, pages, empty = office_text(src)
    except _Timeout:
        try:
            signal.alarm(30)
            doc = fitz.open(src)
            texts = [p.get_text("text").strip() for p in doc]
            text = "\n\n".join(f"<!-- page {i} -->\n{t}" for i, t in enumerate(texts, 1))
            pages, empty = len(texts), sum(1 for t in texts if len(t) < 40)
        except Exception as e:
            return path, None, False, f"timeout: {e}"
    except Exception as e:
        return path, None, False, str(e)
    finally:
        signal.alarm(0)
    needs_ocr = pages > 0 and empty / pages > 0.5
    dest = target_for(row)
    meta = dict(county=row["county"], category=row["category"], title=row["title"],
                source_url=row["source_url"], effective=row["effective"],
                retrieved=row["retrieved"], original=path, pages=pages,
                needs_ocr="yes" if needs_ocr else "no")
    write_md(dest, meta, f"# {row['title']}\n\n{text}")
    notes = row.get("notes", "")
    if needs_ocr and "needs_ocr" not in notes:
        notes = (notes + "; needs_ocr").strip("; ")
    return path, {**row, "text_path": str(dest.relative_to(CORPUS)), "notes": notes}, needs_ocr, None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--county", required=True)
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--only")
    ap.add_argument("--workers", type=int, default=8)
    a = ap.parse_args()

    rows = read_manifest(a.county)
    todo = []
    for path, row in rows.items():
        src = CORPUS / path
        if src.suffix.lower() not in DOC_EXT or not src.exists():
            continue
        if a.only and a.only not in path:
            continue
        if row.get("text_path") and not a.force and (CORPUS / row["text_path"]).exists():
            continue
        todo.append((path, row))
    print(f"{len(todo)} documents to convert", flush=True)

    updated, flagged, done = [], [], 0
    with ProcessPoolExecutor(a.workers) as ex:
        for path, new, ocr, err in ex.map(convert, todo, chunksize=2):
            done += 1
            if err:
                print("  ! failed", path, err, flush=True)
                continue
            updated.append(new)
            if ocr:
                flagged.append(path)
            if done % 50 == 0:
                print(f"  {done}/{len(todo)}", flush=True)
                upsert_manifest(a.county, updated)
                updated = []
    if updated:
        upsert_manifest(a.county, updated)
    print(f"converted {done - 0} documents; {len(flagged)} look scanned (needs_ocr)")
    for f in flagged:
        print("   needs_ocr:", f)


if __name__ == "__main__":
    main()
