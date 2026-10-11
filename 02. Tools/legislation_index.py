"""Build a one-line-per-item index of County Council bills and resolutions (no AI needed).

Reads <County>/Documents/Legislation/{Bills,Resolutions}/*.md and writes
<County>/01. Digests/Legislation Index.md (and .csv): number, title, enacted/adopted, effective,
whether it amends the zoning chapter or the water & sewer plan, and the file to open.
Multiple versions of one bill (introduced / amended / enacted) collapse to one row (latest status).

Usage: python -I "02. Tools/legislation_index.py" --county Talbot [--zoning-chapter 190]
"""
import argparse
import csv
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from common import county_dir, county_name  # noqa: E402

DATE = r"([A-Z][a-z]+\.? ?\d{1,2},? ?\d{4})"


def find(pat, text):
    m = re.search(pat, text, re.I)
    return " ".join(m.group(1).split()) if m else ""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--county", required=True)
    ap.add_argument("--zoning-chapter", default="190")
    a = ap.parse_args()
    cdir = county_dir(a.county)
    base = cdir / "Documents" / "Legislation"
    items = {}
    for kind in ("Bills", "Resolutions"):
        for p in sorted((base / kind).glob("*.md")):
            name = p.stem
            text = p.read_text(errors="replace")
            body = text.split("\n---\n", 1)[-1]
            m = re.search(r"\b(?:Bills?|Res\.?|Resolution)\s*(?:Nos?\.?\s*)?(\d{3,4})", name, re.I)
            num = m.group(1) if m else name
            key = (kind, num)
            status = ("enacted" if re.search(r"enacted|enrolled|adopted|approved", name, re.I)
                      else "introduced" if re.search(r"introduced", name, re.I) else "posted")
            title = re.sub(r"^(Bills?|Res\.?|Resolution)\s*(Nos?\.?\s*)?[\d\- ]+\s*", "", name, flags=re.I)
            title = re.sub(r"\s*(As (Amended,? )?(Enacted|Introduced)[^)]*|as enrolled)\s*$", "", title, flags=re.I).strip(" ()-")
            row = dict(
                kind=kind[:-1], number=num, title=title[:140], status=status,
                enacted=find(r"(?:ENACTED|ADOPTED|Date of Passage)\s*:?\s*" + DATE, body),
                effective=find(r"EFFECTIVE DATE\s*:?\s*" + DATE, body),
                zoning="yes" if re.search(rf"Ch(apter|\.)\s*{a.zoning_chapter}\b|{a.zoning_chapter}-\d", name, re.I)
                or re.search(rf"TO AMEND[^.]{{0,120}}CHAPTER {a.zoning_chapter}\b", body[:4000], re.I) else "",
                water_sewer="yes" if re.search(r"CWSP|water and sewer|sewer service|wastewater", name, re.I) else "",
                file=str(p.relative_to(cdir)),
            )
            rank = {"enacted": 2, "introduced": 1, "posted": 0}
            if key not in items or rank[status] >= rank[items[key]["status"]]:
                items[key] = row

    rows = sorted(items.values(), key=lambda r: (r["kind"], -int(r["number"]) if r["number"].isdigit() else 0))
    out = cdir / "01. Digests"
    out.mkdir(exist_ok=True)
    fields = ["kind", "number", "title", "status", "enacted", "effective", "zoning", "water_sewer", "file"]
    with open(out / "Legislation Index.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)
    lines = [f"# {county_name(a.county)} — Legislation Index", "",
             f"*One row per bill/resolution (latest version). Zoning = amends Chapter {a.zoning_chapter}; "
             "W&S = water & sewer plan amendment. Open the file only if you need the text.*", ""]
    for kind in ("Bill", "Resolution"):
        sub = [r for r in rows if r["kind"] == kind]
        lines += [f"## {kind}s ({len(sub)})", "", "| No. | Title | Status | Enacted | Effective | Zoning | W&S |",
                  "|---|---|---|---|---|---|---|"]
        lines += [f"| {r['number']} | {r['title']} | {r['status']} | {r['enacted']} | {r['effective']} | "
                  f"{'✓' if r['zoning'] else ''} | {'✓' if r['water_sewer'] else ''} |" for r in sub]
        lines.append("")
    (out / "Legislation Index.md").write_text("\n".join(lines))
    z = sum(1 for r in rows if r["zoning"])
    ws = sum(1 for r in rows if r["water_sewer"])
    print(f"{len(rows)} items ({z} zoning, {ws} water/sewer) -> {out / 'Legislation Index.md'}")


if __name__ == "__main__":
    main()
