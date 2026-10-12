"""Search the corpus. Returns compact hits (file, section/pages, short snippet) — open only what you need.

Usage:
  python -I "02. Tools/search.py" "minor subdivision" [--county Talbot] [--category code] [-n 10] [--full]
Query syntax is SQLite FTS5: words are ANDed; use "exact phrase", OR, NOT, prefix*  e.g.
  '"minor subdivision" AND (lots OR parcels)'      'septic NEAR(tier, 10)'
--full prints the entire matching chunk instead of a snippet.
"""
import argparse
import sqlite3
import sys
from pathlib import Path

DB = Path(__file__).resolve().parent.parent / "00. Index" / "corpus.db"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("query")
    ap.add_argument("--county")
    ap.add_argument("--category")
    ap.add_argument("-n", type=int, default=10)
    ap.add_argument("--full", action="store_true")
    a = ap.parse_args()

    con = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
    where, args = ["fts MATCH ?"], [a.query]
    if a.county:
        where.append("d.county = ? COLLATE NOCASE")
        args.append("01. Maryland" if a.county.lower() in ("maryland", "state") else a.county)
    if a.category:
        where.append("d.category = ? COLLATE NOCASE")
        args.append(a.category)
    text_expr = "fts.text" if a.full else "snippet(fts, 0, '«', '»', ' … ', 40)"
    sql = f"""SELECT d.path, d.title, d.section, c.page_from, c.page_to, d.county, d.category, {text_expr}
              FROM fts JOIN chunks c ON c.id = fts.rowid JOIN docs d ON d.id = c.doc_id
              WHERE {' AND '.join(where)} ORDER BY bm25(fts, 1.0, 3.0) LIMIT ?"""
    try:
        rows = con.execute(sql, args + [a.n]).fetchall()
    except sqlite3.OperationalError as e:
        sys.exit(f"query error: {e}  (quote phrases; hyphenated terms like 190-36 must be in double quotes)")
    for path, title, sec, pf, pt, county, cat, text in rows:
        loc = f"pp.{pf}-{pt}" if pf and pt != pf else (f"p.{pf}" if pf else "")
        print(f"## {path} {loc}  [{county}/{cat}] {title}")
        print(" ".join(text.split()) if not a.full else text.strip())
        print()
    if not rows:
        print("no hits")


if __name__ == "__main__":
    main()
