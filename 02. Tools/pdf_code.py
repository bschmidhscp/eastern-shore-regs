"""Turn a code published as one big PDF (zoning ordinance, UDO, subdivision regulations) into per-article files.

Downloads the PDF to <County>/Originals/Code/<Name>.pdf, extracts text page by page, splits at
ARTICLE / CHAPTER headings (falls back to 10-page chunks), and writes
<County>/Code/<Name>/<NN> <heading>.md with page markers, plus 00. Contents.md.

Usage: python -I "02. Tools/pdf_code.py" --county Kent --url <pdf url> --name "Unified Development Ordinance"
"""
import argparse
import re
import shutil
import sys
from pathlib import Path

import pymupdf as fitz

sys.path.insert(0, str(Path(__file__).parent))
from common import TODAY, clean_name, county_dir, county_name, download, write_md  # noqa: E402

HEAD = re.compile(r"^\s*(ARTICLE|Article|CHAPTER|Chapter|PART|Part)\s+([0-9IVXLC]+[A-Z]?)\b[\s.:—–-]*(.{0,90})$")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--county", required=True)
    ap.add_argument("--url", required=True)
    ap.add_argument("--name", required=True)
    a = ap.parse_args()
    cname = county_name(a.county)
    cdir = county_dir(cname)
    pdf = cdir / "Originals" / "Code" / f"{clean_name(a.name)}.pdf"
    download(a.url, pdf, cname, "code", title=f"{cname} {a.name} (standalone PDF)")
    if not pdf.exists():     # downloaded before and since moved to the originals archive: its text is already built
        return print(f"{cname} {a.name}: already converted (original archived) — kept the current text")
    doc = fitz.open(pdf)
    pages = [p.get_text("text") for p in doc]

    # find article starts: a heading line near the top of a page, first occurrence of each number
    starts, seen = [], set()
    for i, t in enumerate(pages):
        if len(re.findall(r"\.{5,}|…{3,}", t)) >= 4:  # table-of-contents page
            continue
        for line in t.splitlines()[:8]:
            if re.search(r"\.{4,}|…", line):
                continue
            m = HEAD.match(line)
            if m and (m[1].upper(), m[2]) not in seen:
                title = m[3].strip() or next((l.strip() for l in t.splitlines()
                                              if l.strip() and not HEAD.match(l)), "")
                seen.add((m[1].upper(), m[2]))
                starts.append((i, f"{m[1].title()} {m[2]}", title[:70]))
                break
    if len(starts) < 3:  # no usable headings: fixed chunks
        starts = [(i, f"Pages {i + 1}-{min(i + 10, len(pages))}", "") for i in range(0, len(pages), 10)]
    elif starts[0][0] > 0:
        starts.insert(0, (0, "Front matter", ""))

    outdir = cdir / "Code" / clean_name(a.name)
    if outdir.exists():
        shutil.rmtree(outdir)
    outdir.mkdir(parents=True)
    contents = [f"# {cname} — {a.name}", "", f"*Split from the published PDF ({len(pages)} pages, retrieved {TODAY}). "
                f"Source: {a.url}*", ""]
    for n, (start, label, title) in enumerate(starts):
        end = starts[n + 1][0] if n + 1 < len(starts) else len(pages)
        fname = f"{n:02d} {clean_name(label + (' - ' + title if title else ''))[:90]}.md"
        body = "\n\n".join(f"<!-- page {p + 1} -->\n{pages[p].strip()}" for p in range(start, end))
        write_md(outdir / fname, dict(county=cname, category="code", source=f"{a.name} (PDF)", title=f"{label} {title}".strip(),
                                      pages=f"{start + 1}-{end}", url=a.url, retrieved=TODAY), f"# {label} {title}\n\n{body}")
        contents.append(f"- [{label} {title}](<{fname}>) — pp. {start + 1}–{end}")
    (outdir / "00. Contents.md").write_text("\n".join(contents) + "\n")
    empty = sum(1 for t in pages if len(t.strip()) < 40)
    print(f"{a.name}: {len(pages)} pages -> {len(starts)} files in {outdir.relative_to(cdir)}"
          + (f"; {empty} pages without text (scanned?)" if empty else ""))


if __name__ == "__main__":
    main()
