"""Crawl a website (same host only) and inventory every document link.

Writes <County>/Originals/Other/Site Inventory <host>.csv with columns:
  page_url, link_url, anchor_text, ext
Only HTML pages are followed; documents (pdf, doc, xls, zip, ...) are listed, not downloaded.
This lets us choose what to download from a compact list instead of reading pages.

Usage: python -I "02. Tools/crawl_links.py" --county Talbot --start https://talbotcountymd.gov/ [--max-pages 3000]
"""
import argparse
import csv
import re
import sys
from collections import deque
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from urllib.parse import urldefrag, urljoin, urlparse

from bs4 import BeautifulSoup

sys.path.insert(0, str(Path(__file__).parent))
from common import county_dir, get  # noqa: E402

DOC_EXT = {".pdf", ".doc", ".docx", ".xls", ".xlsx", ".csv", ".zip", ".ppt", ".pptx", ".kmz", ".kml", ".txt", ".rtf"}
SKIP = re.compile(r"(calendar\?|/calendar/|login|logout|\.(jpg|jpeg|png|gif|svg|css|js|mp4|mp3|ico)$|mailto:|tel:|javascript:)", re.I)


def norm_host(h):
    return h.lower().removeprefix("www.")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--county", required=True)
    ap.add_argument("--start", required=True, nargs="+")
    ap.add_argument("--max-pages", type=int, default=3000)
    ap.add_argument("--extra-hosts", nargs="*", default=[], help="other hosts to treat as same site")
    ap.add_argument("--label", help="name for the inventory file (default: host)")
    ap.add_argument("--max-depth", type=int, default=99, help="link hops from the start pages")
    ap.add_argument("--workers", type=int, default=4, help="pages fetched at once (same host; keep it polite)")
    ap.add_argument("--skip", default="press-release|calendar|news|/events?/|election|sheriff|animal|aging|parks|tourism|library|job|employment",
                    help="regex of page URLs not to follow")
    a = ap.parse_args()

    hosts = {norm_host(urlparse(u).netloc) for u in a.start} | {norm_host(h) for h in a.extra_hosts}
    skip_pages = re.compile(a.skip, re.I) if a.skip else None
    q, seen, docs = deque((u, 0) for u in a.start), set(a.start), {}
    pages = 0
    rows = []
    pool = ThreadPoolExecutor(a.workers)

    def fetch(item):
        try:
            return item, get(item[0], retries=2, timeout=40)
        except Exception as e:
            print("  ! ", item[0], e, file=sys.stderr)
            return item, None

    # Fetch the next batch from the front of the queue in parallel, then handle the pages in queue order, so the
    # result is the same as a one-at-a-time crawl (only faster).
    ahead = deque()
    while (q or ahead) and pages < a.max_pages:
        if not ahead:
            batch = [q.popleft() for _ in range(min(len(q), max(a.max_pages - pages, a.workers)))]
            ahead.extend(pool.map(fetch, batch))
        (url, depth), r = ahead.popleft()
        if r is None or "html" not in r.headers.get("content-type", ""):
            continue
        pages += 1
        if pages % 25 == 0:
            print(f"{pages} pages, {len(docs)} docs, queue {len(q)}", flush=True)
        soup = BeautifulSoup(r.text, "lxml")
        base_tag = soup.find("base", href=True)  # pages may set <base href> for relative links
        base = urljoin(url, base_tag["href"]) if base_tag else url
        for el in soup.find_all(["a", "iframe"]):
            href = el.get("href") or el.get("src")
            if not href or SKIP.search(href):
                continue
            link = urldefrag(urljoin(base, href.strip()))[0]
            pu = urlparse(link)
            if pu.scheme not in ("http", "https"):
                continue
            ext = Path(pu.path).suffix.lower()
            text = " ".join(el.get_text(" ").split())[:200]
            if ext in DOC_EXT or "/uploads/" in pu.path or "DocumentCenter" in pu.path:
                rows.append((url, link, text, ext))
                docs.setdefault(link, text)
            elif norm_host(pu.netloc) in hosts and link not in seen:
                seen.add(link)
                if depth + 1 <= a.max_depth and not (skip_pages and skip_pages.search(link)):
                    q.append((link, depth + 1))
            elif norm_host(pu.netloc) not in hosts:
                rows.append((url, link, text, "external"))

    host = sorted(hosts)[0]
    out = county_dir(a.county) / "Originals" / "Other" / f"Site Inventory {a.label or host}.csv"
    out.parent.mkdir(parents=True, exist_ok=True)
    with open(out, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["page_url", "link_url", "anchor_text", "ext"])
        w.writerows(sorted(set(rows)))
    print(f"crawled {pages} pages; {len(docs)} unique documents; queue left {len(q) + len(ahead)} -> {out}")


if __name__ == "__main__":
    main()
