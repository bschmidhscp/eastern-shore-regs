"""List and download meeting agendas/minutes from a Granicus video archive (ViewPublisher pages).

Many Maryland counties publish Planning Commission / Council meetings on <county>.granicus.com.
Each listing row has a meeting name, date, and links to Agenda / Minutes (often PDFs behind redirects).

Usage:
  python -I "02. Tools/granicus.py" --county Talbot --host talbot-md.granicus.com --view 6 \
      --body "Planning Commission" [--since 2023-10-01] [--download]
Writes <County>/Originals/Other/Granicus <body>.csv (always) and, with --download, saves files to
<County>/Originals/Meeting Minutes/<body>/<YYYY-MM-DD> <Agenda|Minutes>.<ext> and records them in the manifest.
"""
import argparse
import csv
import datetime as dt
import re
import sys
from pathlib import Path

from bs4 import BeautifulSoup
from curl_cffi import requests as _req

sys.path.insert(0, str(Path(__file__).parent))
from common import CORPUS, TODAY, clean_name, county_dir, get, read_manifest, sha256, upsert_manifest  # noqa: E402

EXT = {"application/pdf": ".pdf", "text/html": ".html",
       "application/vnd.openxmlformats-officedocument.wordprocessingml.document": ".docx",
       "application/msword": ".doc"}


def parse_date(s):
    m = re.search(r"([A-Z][a-z]{2})\s+(\d{1,2}),\s+(\d{4})", s)
    return dt.datetime.strptime(" ".join(m.groups()), "%b %d %Y").date() if m else None


def listing(host, view):
    soup = BeautifulSoup(get(f"https://{host}/ViewPublisher.php?view_id={view}").text, "lxml")
    out = []
    for tr in soup.select("tr.listingRow"):
        tds = tr.find_all("td")
        name = " ".join(tds[0].get_text(" ").split()) if tds else ""
        date = parse_date(" ".join(tr.get_text(" ").split()))
        links = {}
        for a in tr.find_all("a", href=True):
            label = a.get_text(strip=True).lower()
            href = a["href"]
            if href.startswith("//"):
                href = "https:" + href
            if label in ("agenda", "minutes", "agenda packet", "packet"):
                links[label] = href
        out.append(dict(name=name, date=date.isoformat() if date else "",
                        agenda=links.get("agenda", ""), minutes=links.get("minutes", ""),
                        packet=links.get("agenda packet") or links.get("packet", "")))
    return out


def fetch(url):
    """Follow redirects manually (Granicus sends relative Location headers); return (bytes, ext) or None."""
    for _ in range(5):
        r = _req.get(url, impersonate="chrome", allow_redirects=False, timeout=60)
        if r.status_code in (301, 302, 303, 307, 308):
            loc = r.headers.get("location", "")
            url = loc if loc.startswith("http") else ("https:" + loc if loc.startswith("//")
                                                     else re.match(r"https://[^/]+", url).group(0) + loc)
            continue
        if r.status_code != 200 or len(r.content) < 500:
            return None
        ctype = r.headers.get("content-type", "").split(";")[0].strip()
        return r.content, EXT.get(ctype, ".bin"), url
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--county", required=True)
    ap.add_argument("--host", required=True)
    ap.add_argument("--view", required=True)
    ap.add_argument("--body", required=True, help="board name used for folders, e.g. 'Planning Commission'")
    ap.add_argument("--since", default="2000-01-01")
    ap.add_argument("--download", action="store_true")
    a = ap.parse_args()

    rows = listing(a.host, a.view)
    cdir = county_dir(a.county)
    inv = cdir / "Originals" / "Other" / f"Granicus {a.body}.csv"
    inv.parent.mkdir(parents=True, exist_ok=True)
    with open(inv, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["name", "date", "agenda", "minutes", "packet"])
        w.writeheader()
        w.writerows(rows)
    print(f"{len(rows)} meetings listed -> {inv.name}")
    if not a.download:
        return

    got = miss = kept = 0
    outdir = cdir / "Originals" / "Meeting Minutes" / a.body
    outdir.mkdir(parents=True, exist_ok=True)
    # Already downloaded (on disk or in the originals archive, per the manifest): skip, except the last 60 days, when
    # counties sometimes replace draft minutes under the same name. The extension is only known after the download,
    # so match on the name without it.
    recent = (dt.date.fromisoformat(TODAY) - dt.timedelta(days=60)).isoformat()
    rel = str(outdir.relative_to(CORPUS)) + "/"
    have_stems = {Path(k).stem for k in read_manifest(a.county) if k.startswith(rel)}
    for r in rows:
        if not r["date"] or r["date"] < a.since:
            continue
        for kind in ("minutes", "agenda", "packet"):
            if not r[kind]:
                continue
            extra = "" if re.match(rf"^{re.escape(a.body)}\s*$", r["name"], re.I) else f" - {clean_name(r['name'])[:60]}"
            if r["date"] < recent and f"{r['date']} {kind.title()}{extra}" in have_stems:
                kept += 1
                continue
            res = fetch(r[kind])
            if not res:
                miss += 1
                continue
            data, ext, final = res
            dest = outdir / f"{r['date']} {kind.title()}{extra}{ext}"
            dest.write_bytes(data)
            upsert_manifest(a.county, [dict(path=str(dest.relative_to(CORPUS)),
                                            category="minutes" if kind == "minutes" else "agenda",
                                            title=f"{a.body} {kind} {r['date']} — {r['name']}",
                                            source_url=final, effective=r["date"], sha256=sha256(dest),
                                            bytes=dest.stat().st_size, notes=f"Granicus view {a.view}")])
            got += 1
    print(f"downloaded {got} files; {kept} already had; {miss} links empty or broken on the county's side")


if __name__ == "__main__":
    main()
