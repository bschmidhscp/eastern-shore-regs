"""Convert downloaded documents (PDF, DOCX, XLSX) to searchable markdown.

For every manifest row of a county whose file is a document and has no text_path yet
(or --force), writes <County>/Documents/<Kind>/<name>.md (minutes go to <County>/Meeting Minutes/Text/)
with front matter and "<!-- page N -->" markers, and records text_path in the manifest.

Pages with almost no extractable text are flagged needs_ocr (scanned) so they can be OCR'd later.

Usage: python -I "02. Tools/to_text.py" --county Talbot [--force] [--only <substring of path>]
"""
import argparse
import subprocess
import sys
from pathlib import Path

import pymupdf as fitz
import pymupdf4llm

sys.path.insert(0, str(Path(__file__).parent))
from common import CORPUS, KIND_FOLDER, county_dir, county_name, read_manifest, upsert_manifest, write_md  # noqa: E402

DOC_EXT = {".pdf", ".docx", ".doc", ".xlsx", ".xls", ".rtf", ".txt"}


def pdf_text(p):
    """Table-aware markdown via pymupdf4llm; plain text fallback for very long or odd PDFs."""
    doc = fitz.open(p)
    n = len(doc)
    try:
        if n > 600:
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
    r = subprocess.run(["pandoc", str(p), "-t", "gfm", "--wrap=none"], capture_output=True, text=True)
    return (r.stdout if r.returncode == 0 else f"*(conversion failed: {r.stderr[:200]})*"), 0, 0


def target_for(row):
    base = CORPUS / Path(row["path"]).parts[0]
    cat = row["category"] or "other"
    name = Path(row["path"]).stem
    if cat in ("minutes", "agenda", "staff-report"):
        return base / "Meeting Minutes" / "Text" / f"{name}.md"
    sub = "Code Attachments" if cat == "code" else KIND_FOLDER.get(cat, cat.title())
    return base / "Documents" / sub / f"{name}.md"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--county", required=True)
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--only")
    a = ap.parse_args()

    rows = read_manifest(a.county)
    updated, flagged = [], []
    for path, row in rows.items():
        src = CORPUS / path
        if src.suffix.lower() not in DOC_EXT or not src.exists():
            continue
        if a.only and a.only not in path:
            continue
        if row.get("text_path") and not a.force and (CORPUS / row["text_path"]).exists():
            continue
        try:
            if src.suffix.lower() == ".pdf":
                text, pages, empty = pdf_text(src)
            else:
                text, pages, empty = office_text(src)
        except Exception as e:
            print("  ! failed", path, e)
            continue
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
            flagged.append(path)
        updated.append({**row, "text_path": str(dest.relative_to(CORPUS)), "notes": notes})
    if updated:
        upsert_manifest(a.county, updated)
    print(f"converted {len(updated)} documents; {len(flagged)} look scanned (needs_ocr)")
    for f in flagged:
        print("   needs_ocr:", f)


if __name__ == "__main__":
    main()
