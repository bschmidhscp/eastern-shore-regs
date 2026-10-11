"""Walk open web-server folder listings ("Index of /...") and inventory every file.

Many county sites expose their upload folders this way; walking them is far faster and more
complete than crawling pages. Writes <County>/Originals/Other/File Inventory <host>.csv with
columns: url, folder, name, modified, size. Progress is printed as it goes.

Usage: python -I "02. Tools/list_dirs.py" --county Talbot --start https://talbotcountymd.gov/uploads/File/ [--workers 6]
"""
import argparse
import csv
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from urllib.parse import unquote, urljoin, urlparse

from bs4 import BeautifulSoup

sys.path.insert(0, str(Path(__file__).parent))
from common import county_dir, get  # noqa: E402


def list_one(url):
    """Return (subfolders, files) for one index page."""
    try:
        soup = BeautifulSoup(get(url, retries=2, timeout=40).text, "lxml")
    except Exception as e:
        print(f"  ! {url}: {e}", flush=True)
        return [], []
    if not (soup.title and "Index of" in soup.title.get_text()):
        return [], []
    folders, files = [], []
    for tr in soup.find_all("tr"):
        a = tr.find("a", href=True)
        if not a or a["href"].startswith("?") or "Parent Directory" in a.get_text():
            continue
        tds = [td.get_text(" ", strip=True) for td in tr.find_all("td")]
        link = urljoin(url, a["href"])
        if not link.startswith(url):
            continue
        if a["href"].endswith("/"):
            folders.append(link)
        else:
            modified = tds[2] if len(tds) > 2 else ""
            size = tds[3] if len(tds) > 3 else ""
            files.append((link, unquote(urlparse(url).path), unquote(a["href"]), modified, size))
    return folders, files


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--county", required=True)
    ap.add_argument("--start", required=True, nargs="+")
    ap.add_argument("--workers", type=int, default=6)
    a = ap.parse_args()

    todo, rows, n = list(a.start), [], 0
    with ThreadPoolExecutor(a.workers) as ex:
        while todo:
            batch, todo = todo, []
            for folders, files in ex.map(list_one, batch):
                todo += folders
                rows += files
            n += len(batch)
            print(f"{n} folders listed, {len(rows)} files, {len(todo)} folders queued", flush=True)

    host = urlparse(a.start[0]).netloc.removeprefix("www.")
    out = county_dir(a.county) / "Originals" / "Other" / f"File Inventory {host}.csv"
    out.parent.mkdir(parents=True, exist_ok=True)
    with open(out, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["url", "folder", "name", "modified", "size"])
        w.writerows(sorted(rows, key=lambda r: (r[1], r[2])))
    print(f"done: {len(rows)} files in {n} folders -> {out}")


if __name__ == "__main__":
    main()
