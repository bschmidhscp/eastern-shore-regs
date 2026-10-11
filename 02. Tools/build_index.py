"""Build the full-text search index index/corpus.db from every markdown file in the corpus.

Chunks: code sections are one chunk each (long ones split ~6k chars);
documents are split on page markers into ~4k-char chunks that remember their page range.
The DB is built in a local temp dir and copied into Drive in one step, because SQLite
files that are written while Google Drive syncs them can be corrupted. Readers should open
it read-only (search.py does).

Usage: python -I "02. Tools/build_index.py"
"""
import os
import re
import shutil
import sqlite3
import tempfile
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).parent))
from common import CORPUS  # noqa: E402

FM = re.compile(r"^---\n(.*?)\n---\n", re.S)
PAGE = re.compile(r"<!-- page (\d+) -->")
SKIP_DIRS = {"02. Tools", "00. Index", "Originals"}


def front_matter(txt):
    m = FM.match(txt)
    meta = {}
    if m:
        for line in m.group(1).splitlines():
            if ":" in line:
                k, v = line.split(":", 1)
                meta[k.strip()] = v.strip().strip('"')
        txt = txt[m.end():]
    return meta, txt


def chunks_for(meta, body, limit):
    """Yield (page_from, page_to, text) chunks."""
    if not PAGE.search(body):
        paras, buf = body.split("\n\n"), ""
        for p in paras:
            if buf and len(buf) + len(p) > limit:
                yield None, None, buf
                buf = ""
            buf += p + "\n\n"
        if buf.strip():
            yield None, None, buf
        return
    pieces = PAGE.split(body)  # [pre, n, text, n, text, ...]
    buf, start, end = pieces[0], None, None
    for i in range(1, len(pieces), 2):
        n, t = int(pieces[i]), pieces[i + 1]
        if buf.strip() and len(buf) + len(t) > limit and start is not None:
            yield start, end, buf
            buf, start = "", None
        start = start or n
        end = n
        buf += t
    if buf.strip():
        yield start, end, buf


def main():
    tmpdir = Path(tempfile.mkdtemp())
    db = tmpdir / "corpus.db"
    con = sqlite3.connect(db)
    con.executescript("""
        CREATE TABLE docs(id INTEGER PRIMARY KEY, path TEXT, county TEXT, category TEXT,
                          title TEXT, section TEXT, source_url TEXT, effective TEXT, retrieved TEXT);
        CREATE TABLE chunks(id INTEGER PRIMARY KEY, doc_id INT, page_from INT, page_to INT, chars INT);
        CREATE VIRTUAL TABLE fts USING fts5(text, title, tokenize='porter unicode61');
    """)
    nd = nc = 0
    for md in sorted(CORPUS.rglob("*.md")):
        rel = md.relative_to(CORPUS)
        if rel.parts[0] in SKIP_DIRS or any(p in SKIP_DIRS for p in rel.parts[:-1]) or md.name == "00. Contents.md":
            continue
        txt = md.read_text(errors="replace")
        meta, body = front_matter(txt)
        county = meta.get("county") or rel.parts[0]
        category = meta.get("category") or ("code" if "Code" in rel.parts[:2] else rel.parts[1].lower() if len(rel.parts) > 2 else "")
        cur = con.execute(
            "INSERT INTO docs(path,county,category,title,section,source_url,effective,retrieved) VALUES(?,?,?,?,?,?,?,?)",
            (str(rel), county, category, meta.get("title", md.stem), meta.get("section", ""),
             meta.get("url") or meta.get("source_url", ""), meta.get("effective", ""), meta.get("retrieved", "")))
        doc_id = cur.lastrowid
        nd += 1
        limit = 6000 if category == "code" else 4000
        for pf, pt, t in chunks_for(meta, body, limit):
            c = con.execute("INSERT INTO chunks(doc_id,page_from,page_to,chars) VALUES(?,?,?,?)",
                            (doc_id, pf, pt, len(t)))
            con.execute("INSERT INTO fts(rowid,text,title) VALUES(?,?,?)",
                        (c.lastrowid, t, meta.get("title", "")))
            nc += 1
    con.commit()
    con.execute("INSERT INTO fts(fts) VALUES('optimize')")
    con.commit()
    con.close()
    out = CORPUS / "00. Index" / "corpus.db"
    out.parent.mkdir(exist_ok=True)
    tmp_out = out.with_suffix(".db.part")
    shutil.copy(db, tmp_out)
    os.replace(tmp_out, out)
    shutil.rmtree(tmpdir)
    print(f"indexed {nd} files, {nc} chunks -> {out} ({out.stat().st_size/1e6:.1f} MB)")


if __name__ == "__main__":
    main()
