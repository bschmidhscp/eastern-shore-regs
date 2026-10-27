"""Download meeting minutes (or agendas when no minutes exist) from a CivicClerk portal API.

Usage: python -I "02. Tools/civicclerk.py" --county Cecil --api https://cecilcomd.api.civicclerk.com/v1 \
           --category 28 --body "Planning Commission" [--since 2023-10-01]
Saves to <County>/Originals/Meeting Minutes/<body>/<YYYY-MM-DD> <Minutes|Agenda>.pdf and records the manifest.
Agendas are kept only for meetings that have no minutes (they still show what applications came up).
"""
import argparse
import datetime as dt
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from common import CORPUS, clean_name, county_dir, get, have, sha256, upsert_manifest  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--county", required=True)
    ap.add_argument("--api", required=True)
    ap.add_argument("--category", required=True)
    ap.add_argument("--body", required=True)
    ap.add_argument("--since", default="2023-10-01")
    a = ap.parse_args()
    api = a.api.rstrip("/")
    now = dt.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    url = (f"{api}/Events?$filter=categoryId eq {a.category} and startDateTime lt {now} "
           f"and startDateTime ge {a.since}T00:00:00Z&$orderby=startDateTime desc&$top=50")
    events = []
    while url:
        d = get(url).json()
        events += d.get("value", [])
        url = d.get("@odata.nextLink")
    outdir = county_dir(a.county) / "Originals" / "Meeting Minutes" / a.body
    outdir.mkdir(parents=True, exist_ok=True)
    got = skipped = 0
    for e in events:
        if "cancel" in (e.get("eventName") or "").lower():
            continue
        files = e.get("publishedFiles") or []
        mins = [f for f in files if "minute" in (f.get("type") or "").lower()]
        pick = mins or [f for f in files if (f.get("type") or "").lower() == "agenda"][:1]
        date = e["startDateTime"][:10]
        for f in pick:
            kind = "Minutes" if f in mins else "Agenda"
            dest = outdir / f"{date} {kind}{'' if len(pick) == 1 else ' - ' + clean_name(f.get('name', ''))[:50]}.pdf"
            if have(dest, a.county):
                continue
            src = f"{api}/Meetings/GetMeetingFileStream(fileId={f['fileId']},plainText=false)"
            try:
                r = get(src, timeout=120)
            except Exception as ex:
                print("  !", date, ex)
                skipped += 1
                continue
            if len(r.content) < 500:
                skipped += 1
                continue
            dest.write_bytes(r.content)
            upsert_manifest(a.county, [dict(path=str(dest.relative_to(CORPUS)),
                                            category="minutes" if kind == "Minutes" else "agenda",
                                            title=f"{a.body} {kind.lower()} {date}", source_url=src, effective=date,
                                            sha256=sha256(dest), bytes=dest.stat().st_size,
                                            notes=f"CivicClerk category {a.category}")])
            got += 1
    print(f"{len(events)} meetings since {a.since}; downloaded {got} files; {skipped} empty/failed")


if __name__ == "__main__":
    main()
