"""Download a list of documents and record them in the county manifest.

Input CSV columns: url, category, subdir, title, effective   (header required; subdir/title/effective optional)
  category: code | fees | plan | map | minutes | agenda | staff-report | law | other
  subdir:   folder under <County>/Originals/ (defaults to the category's folder, e.g. Fees, Plans)
Files keep the URL's own filename (readable, original capitalization). Already-downloaded files are skipped.

Usage: python -I "02. Tools/fetch_list.py" --county Talbot --list picks.csv [--workers 4]
"""
import argparse
import csv
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from urllib.parse import unquote, urlparse

sys.path.insert(0, str(Path(__file__).parent))
from common import KIND_FOLDER, clean_name, county_dir, download  # noqa: E402


def dest_for(county, row):
    p = Path(unquote(urlparse(row["url"]).path))
    ext = p.suffix.lower() or ".pdf"
    sub = row.get("subdir") or KIND_FOLDER.get(row["category"], row["category"].title())
    return county_dir(county) / "Originals" / sub / f"{clean_name(p.stem)}{ext}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--county", required=True)
    ap.add_argument("--list", required=True)
    ap.add_argument("--workers", type=int, default=4)
    a = ap.parse_args()
    rows = list(csv.DictReader(open(a.list, newline="")))

    def one(r):
        d = dest_for(a.county, r)
        try:
            download(r["url"], d, a.county, r["category"], title=r.get("title") or d.stem,
                     effective=r.get("effective", ""))
            return None
        except Exception as e:
            return f"{r['url']}: {e}"

    with ThreadPoolExecutor(a.workers) as ex:
        errs = [e for e in ex.map(one, rows) if e]
    print(f"{len(rows) - len(errs)} ok, {len(errs)} failed")
    for e in errs:
        print("  !", e)


if __name__ == "__main__":
    main()
