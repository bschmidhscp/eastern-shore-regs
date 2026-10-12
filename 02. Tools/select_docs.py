"""Pick the documents worth downloading from a county's inventories (rules learned on the Talbot pilot).

Reads every inventory CSV in <County>/Originals/Other/ (File Inventory *.csv from list_dirs.py,
Site Inventory *.csv from crawl_links.py) and writes a pick list for fetch_list.py.

Usage: python -I "02. Tools/select_docs.py" --county Kent --out picks.csv [--since-minutes 2023-10-01]
"""
import argparse
import csv
import datetime as dt
import json
import re
import sys
from pathlib import Path
from urllib.parse import quote, unquote, urlparse

sys.path.insert(0, str(Path(__file__).parent))
from common import county_dir, county_name  # noqa: E402

DOC = re.compile(r"\.(pdf|docx?|xlsx?)$", re.I)
SKIP = re.compile(r"tax.?sale|election|liquor|alcohol|sheriff|animal|aging|senior|parks?.?(program|rec)|recycl|"
                  r"job|employ|personnel|hr/|bid.?tab|rfp|rfq|procurement|newsletter|calendar|library|tourism|"
                  r"health.?department|covid|emergency.?management|transcript|ballot|voter|budget.?book|"
                  r"electrical.?board|historic.?preservation.?comm|short.?term.?rental", re.I)
MONTHS = {m: i for i, m in enumerate(["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"], 1)}

# (category, subdir, pattern) — first match wins; tested on "path + anchor text"
RULES = [
    ("minutes", "Meeting Minutes/Board of Appeals Decisions", r"(board.?of.?(zoning.?)?appeals|BOA|zoning.?appeals).*(decision|order|opinion)|appeals/decisions|(decision|order)s?/"),
    ("minutes", "Meeting Minutes/Planning Commission", r"planning.?(and.?zoning.?)?commission.*minute|minute.*planning.?(and.?zoning.?)?commission|/pc.?minutes|p&z.*minute"),
    ("minutes", "Meeting Minutes/Board of Appeals", r"(board.?of.?(zoning.?)?appeals|zoning.?appeals).*minute|minute.*appeals"),
    ("minutes", "Meeting Minutes/County Council", r"(council|commissioners?).*minute|minute.*(council|commissioner)"),
    ("agenda", "Meeting Minutes/Pre-Application Meetings", r"pre.?app"),
    ("agenda", "Meeting Minutes/Technical Advisory Committee", r"technical.?advisory|/tac/"),
    ("law", "Legislation/Bills", r"\bbill\b|bills/|ordinance"),
    ("law", "Legislation/Resolutions", r"resolution|\bres\.? ?\d"),
    ("plan", "Plans", r"comprehensive.?plan|comp.?plan|master.?plan|water.?(and|&).?sewer|wastewater|cwsp|"
                      r"land.?preservation|priority.?preservation|sector.?plan|growth|village.?plan|small.?area.?plan"),
    ("fees", "Fees", r"fee|excise|impact"),
    ("other", "Planning Applications and Forms", r"(planning|zoning|p&z|subdivision).*(application|checklist|form|manual|guide|standards)|"
                                                  r"(application|checklist).*(subdivision|site.?plan|variance|special.?exception)"),
    ("other", "Septic and Bay Restoration Fund", r"septic|bay.?restoration|\bBAT\b|perc|on.?site.?(sewage|wastewater)"),
    ("code", "Code Related", r"zoning.?(ordinance|map|code)|subdivision.?regulation|design.?manual|critical.?area.?(program|ordinance)"),
]


def date_in(s):
    s = unquote(s)
    m = re.search(r"(20\d\d)[-_. ](\d{1,2})[-_. ](\d{1,2})", s)
    if m:
        return dt.date(int(m[1]), max(1, min(12, int(m[2]))), max(1, min(28, int(m[3]))))
    m = re.search(r"\b(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*\.?[ _-]*(\d{1,2})?,?[ _-]*(20\d\d)", s, re.I)
    if m:
        return dt.date(int(m[3]), MONTHS[m[1].lower()], int(m[2]) if m[2] and int(m[2]) <= 28 else 1)
    m = re.search(r"\b(\d{1,2})[-_.](\d{1,2})[-_.](\d{2,4})\b", s)
    if m:
        y = int(m[3]) + (2000 if len(m[3]) == 2 else 0)
        if 2000 <= y <= 2100 and 1 <= int(m[1]) <= 12:
            return dt.date(y, int(m[1]), max(1, min(28, int(m[2]))))
    m = re.search(r"\b(20[0-3]\d)\b", s)
    return dt.date(int(m[1]), 12, 31) if m else None  # year only: treat as end of year


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--county", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    cname = county_name(a.county)
    cfg_path = Path(__file__).parent / "County Configs" / f"{cname}.json"
    sel = json.loads(cfg_path.read_text()).get("selection", {}) if cfg_path.exists() else {}
    since = {"minutes": sel.get("minutes_since", "2023-10-01"), "appeals": sel.get("appeals_since", "2019-01-01"),
             "law": sel.get("legislation_since", "2022-01-01")}

    cands = {}
    for inv in sorted((county_dir(cname) / "Originals" / "Other").glob("*Inventory*.csv")):
        for r in csv.DictReader(open(inv, newline="", errors="replace")):
            url = r.get("url") or r.get("link_url") or ""
            if not url or r.get("ext") == "external":
                continue
            path = unquote(urlparse(url).path)
            i = path.find("/uploads/")  # fix links resolved relative to the page they sat on
            if i > 0:
                url = f"{urlparse(url).scheme}://{urlparse(url).netloc}{quote(path[i:])}"
                path = path[i:]
            if not (DOC.search(path) or "DocumentCenter/View" in url or "Archive.aspx?ADID" in url
                    or "AgendaCenter/ViewFile" in url):
                continue
            page = unquote(r.get("page_url", "")).replace("+", " ").replace("_", " ")
            text = f"{path} {r.get('anchor_text', '')} {r.get('name', '')} {r.get('folder', '')} [{page}]"
            if SKIP.search(text):
                continue
            modified = (r.get("modified") or "")[:10]
            cands.setdefault(url, (text, modified))

    picks, counts = [], {}
    for url, (text, modified) in cands.items():
        for cat, sub, pat in RULES:
            if re.search(pat, text, re.I):
                break
        else:
            continue
        d = date_in(text) or (dt.date.fromisoformat(modified) if re.match(r"\d{4}-\d\d-\d\d", modified) else None)
        cutoff = since["appeals"] if "Appeals" in sub else since["law"] if cat == "law" else since["minutes"] if cat in ("minutes", "agenda") else None
        if cutoff and d and d.isoformat() < cutoff:
            continue
        if cutoff and not d and cat in ("minutes", "agenda", "law"):
            continue  # undated minutes/legislation: can't place in the time window
        title = Path(unquote(urlparse(url).path)).stem
        picks.append(dict(url=url, category=cat, subdir=sub, title=title, effective=d.isoformat() if d else ""))
        counts[sub] = counts.get(sub, 0) + 1

    with open(a.out, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["url", "category", "subdir", "title", "effective"])
        w.writeheader()
        w.writerows(picks)
    for k, v in sorted(counts.items(), key=lambda x: -x[1]):
        print(f"{v:5d}  {k}")
    print(f"{len(picks)} picks from {len(cands)} candidate documents -> {a.out}")


if __name__ == "__main__":
    main()
