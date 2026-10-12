"""Download Maryland regulations (COMAR) and statutes into 01. Maryland/, one markdown file per chapter/range.

Targets file (CSV, header required): kind, ref, end, topic
  comar,   27.01        ,      , Critical Area     -> every chapter in subtitle 27.01
  comar,   26.04.02     ,      , Septic and Sewage -> one chapter
  statute, gnr 8-1801   , 8-1817, Critical Area    -> Natural Resources §8-1801 through §8-1817
Statute article codes are mgaleg's (gnr Natural Resources, gen Environment, glu Land Use, gag Agriculture,
gsf State Finance & Procurement, gtp Tax-Property). Sections are walked with mgaleg's "next section" API.

Writes:
  01. Maryland/Originals/<Topic>/COMAR 27.01.02/27.01.02.05.html     (each regulation page as downloaded)
  01. Maryland/Originals/<Topic>/Natural Resources 8-1801 to 8-1817/8-1801.html
  01. Maryland/Documents/<Topic>/COMAR 27.01.02 Development in the Critical Area.md
  01. Maryland/Documents/<Topic>/Natural Resources 8-1801 to 8-1817.md
and one manifest row per original (county "Maryland", category "law").

Usage: python -I "02. Tools/statewide_fetch.py" --targets "02. Tools/Statewide Targets.csv" [--force] [--workers 6]
"""
import argparse
import csv
import re
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from bs4 import BeautifulSoup

sys.path.insert(0, str(Path(__file__).parent))
from common import CORPUS, TODAY, clean_name, download, get, upsert_manifest, write_md  # noqa: E402

STATE = "01. Maryland"
COMAR = "https://regs.maryland.gov/us/md/exec/comar/"
MGA = "https://mgaleg.maryland.gov/mgawebsite"
ARTICLES = {"gnr": "Natural Resources", "gen": "Environment", "glu": "Land Use", "gag": "Agriculture",
            "gsf": "State Finance and Procurement", "gtp": "Tax-Property", "grp": "Real Property"}
FORCE = False  # --force: re-download pages that already exist (to pick up amendments)


def soup(html):
    return BeautifulSoup(html, "lxml")


LABEL = re.compile(r"\(?[A-Za-z0-9]{1,5}[.)]$")  # "A.", "(1)", "(iv)"


def lines(node):
    """Visible text, one paragraph per line: outline labels joined to their text, inline links rejoined."""
    out = []
    for l in (l.strip() for l in node.get_text("\n").splitlines()):
        if not l:
            continue
        if out and (LABEL.fullmatch(out[-1]) or re.match(r"[a-z,.;:)\]]", l) or out[-1].startswith("COMAR ")
                    and len(out[-1]) < 20 or re.fullmatch(r"(COMAR [\d.\-]+|Regulation [\w.\-]+ of this chapter)", l)):
            out[-1] += " " + l
        else:
            out.append(l)
    return "\n".join(out)


def comar_title(s):
    t = s.find("title")
    return t.get_text(" ", strip=True).split(" | ")[0].strip() if t else ""


def comar_children(code):
    """Codes one level below `code` (subtitle -> chapters, chapter -> regulations), in page order."""
    depth = code.count(".") + 1
    s = soup(get(COMAR + code).text)
    out = []
    for a in s.find_all("a", href=True):
        m = re.fullmatch(r"/us/md/exec/comar/([\d.\-]+)", a["href"])
        if m and m.group(1).startswith(code + ".") and m.group(1).count(".") == depth and m.group(1) not in out:
            out.append(m.group(1))
    return out, comar_title(s)


def comar_chapter(chapter, topic, workers):
    regs, title = comar_children(chapter)
    title = re.sub(r"^Chapter \d+\s*", "", title)
    odir = Path(STATE) / "Originals" / topic / f"COMAR {chapter}"

    def one(reg):
        row = download(COMAR + reg, odir / f"{reg}.html", "Maryland", "law", title=f"COMAR {reg}", force=FORCE)
        art = soup((CORPUS / row["path"]).read_text(errors="replace"))
        body = art.find("article") or art.body
        return reg, comar_title(art), lines(body), row

    with ThreadPoolExecutor(workers) as ex:
        parts = list(ex.map(one, regs))
    md = Path(STATE) / "Documents" / topic / f"{clean_name(f'COMAR {chapter} {title}')}.md"
    body = "\n\n".join(f"## COMAR {reg} {t.lstrip('.0123456789- ')}\n\n{txt}" for reg, t, txt, _ in parts)
    write_md(CORPUS / md, {"title": f"COMAR {chapter} {title}", "source": COMAR + chapter, "retrieved": TODAY,
                           "regulations": len(parts)}, f"# COMAR {chapter} — {title}\n\n{body}")
    upsert_manifest("Maryland", [dict(r, text_path=str(md)) for *_, r in parts])
    print(f"COMAR {chapter}: {len(parts)} regulations -> {md.name}")


def section_key(sec):
    return [(0, int(x), "") if x.isdigit() else (1, 0, x) for x in re.split(r"[-.]", sec)]


def statute_range(art, start, end, topic):
    name = ARTICLES.get(art, art)
    label = f"{name} {start} to {end}" if end else f"{name} {start}"
    odir = Path(STATE) / "Originals" / topic / clean_name(label)
    sec, parts, rows = start, [], []
    while sec and (sec == start or (end and section_key(sec) <= section_key(end))):
        url = f"{MGA}/Laws/StatuteText?article={art}&section={sec}&enactments=false"
        row = download(url, odir / f"{sec}.html", "Maryland", "law", title=f"{name} §{sec}", force=FORCE)
        node = soup((CORPUS / row["path"]).read_text(errors="replace")).find(id="StatuteText")
        txt = re.sub(r"^.*?\n(?:Previous\nNext\n)", "", lines(node), count=1, flags=re.S)
        txt = re.sub(r"\nPrevious\nNext\s*$", "", txt)
        parts.append(f"## {name} §{sec}\n\n{txt}")
        rows.append(row)
        if not end:
            break
        nxt = get(f"{MGA}/api/Laws/GetNext", params=dict(articleCode=art, sectionCode=sec, enactments="False")).text
        m = re.search(r">([^<]*)</string>", nxt)
        sec = m.group(1).strip() if m else ""
    md = Path(STATE) / "Documents" / topic / f"{clean_name(label)}.md"
    write_md(CORPUS / md, {"title": f"Md. Code, {label}", "source": f"{MGA}/Laws/Statutes", "retrieved": TODAY,
                           "sections": len(parts)}, f"# Annotated Code of Maryland — {label}\n\n" + "\n\n".join(parts))
    upsert_manifest("Maryland", [dict(r, text_path=str(md)) for r in rows])
    print(f"{label}: {len(parts)} sections -> {md.name}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--targets", required=True)
    ap.add_argument("--workers", type=int, default=6)
    ap.add_argument("--force", action="store_true", help="re-download existing pages")
    a = ap.parse_args()
    global FORCE
    FORCE = a.force
    for t in csv.DictReader(open(a.targets, newline="")):
        t = {k: (v or "").strip() for k, v in t.items()}
        try:
            if t["kind"] == "comar":
                chapters = [t["ref"]] if t["ref"].count(".") == 2 else comar_children(t["ref"])[0]
                for ch in chapters:
                    comar_chapter(ch, t["topic"], a.workers)
            else:
                art, start = t["ref"].split()
                statute_range(art, start, t["end"], t["topic"])
        except Exception as e:
            print(f"! {t}: {e}")


if __name__ == "__main__":
    main()
