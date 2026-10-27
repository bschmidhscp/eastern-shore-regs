"""Download meeting minutes (or agendas when no minutes exist) from a CivicPlus AgendaCenter.

Lists each year via /AgendaCenter/UpdateCategoryList?year=YYYY&catID=N, then downloads
/AgendaCenter/ViewFile/Minutes/_MMDDYYYY-ID (or .../Agenda/... for meetings without minutes).

Usage: python -I "02. Tools/agendacenter.py" --county "Queen Anne's" --site https://www.qac.org \
           --category 3 --body "Board of Appeals" [--since 2023-10-01]
"""
import argparse
import datetime as dt
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from common import CORPUS, county_dir, get, have, sha256, upsert_manifest  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--county", required=True)
    ap.add_argument("--site", required=True)
    ap.add_argument("--category", required=True)
    ap.add_argument("--body", required=True)
    ap.add_argument("--since", default="2023-10-01")
    a = ap.parse_args()
    site = a.site.rstrip("/")
    since = dt.date.fromisoformat(a.since)
    meetings = {}  # id -> {"date":, "Minutes": bool, "Agenda": bool}
    for year in range(since.year, dt.date.today().year + 1):
        try:
            t = get(f"{site}/AgendaCenter/UpdateCategoryList?year={year}&catID={a.category}", retries=2).text
        except Exception as e:
            print("  ! list", year, e)
            continue
        for kind, mid in re.findall(r"/AgendaCenter/ViewFile/(Minutes|Agenda)/(_\d{8}-\d+)(?![?\w])", t):
            m = re.match(r"_(\d\d)(\d\d)(\d{4})-", mid)
            d = dt.date(int(m[3]), int(m[1]), int(m[2]))
            if d < since or d > dt.date.today():
                continue
            meetings.setdefault(mid, {"date": d})[kind] = True
    outdir = county_dir(a.county) / "Originals" / "Meeting Minutes" / a.body
    outdir.mkdir(parents=True, exist_ok=True)
    got = failed = n_min = 0
    for mid, info in sorted(meetings.items(), key=lambda x: x[1]["date"]):
        kind = "Minutes" if info.get("Minutes") else "Agenda"
        n_min += kind == "Minutes"
        dest = outdir / f"{info['date'].isoformat()} {kind}.pdf"
        if have(dest, a.county):
            dest = outdir / f"{info['date'].isoformat()} {kind} {mid[-4:]}.pdf"
            if have(dest, a.county):
                continue
        src = f"{site}/AgendaCenter/ViewFile/{kind}/{mid}"
        try:
            r = get(src, timeout=120)
        except Exception as e:
            print("  !", src, e)
            failed += 1
            continue
        if len(r.content) < 500 or b"%PDF" not in r.content[:1024]:
            failed += 1
            continue
        dest.write_bytes(r.content)
        upsert_manifest(a.county, [dict(path=str(dest.relative_to(CORPUS)),
                                        category="minutes" if kind == "Minutes" else "agenda",
                                        title=f"{a.body} {kind.lower()} {info['date']}", source_url=src,
                                        effective=info["date"].isoformat(), sha256=sha256(dest),
                                        bytes=dest.stat().st_size, notes=f"AgendaCenter category {a.category}")])
        got += 1
    print(f"{len(meetings)} meetings since {a.since} ({n_min} with minutes); downloaded {got}; {failed} failed")


if __name__ == "__main__":
    main()
