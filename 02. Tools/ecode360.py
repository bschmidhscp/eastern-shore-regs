"""Download a county code from eCode360 and split it into one markdown file per section.

Usage:
  python -I "02. Tools/ecode360.py" --county Talbot --code TA0795 --guid 11765065
    --guid  the eCode360 node to print (the "The Code" node = whole code; a chapter id = one chapter)

Outputs (under <County>/):
  Originals/Code/eCode360 <code> <date>.html   original print view (archival)
  Originals/Code/Attachments/*                 figures, image-tables, linked PDFs
  Code/Chapter <N>/<section>.md                one file per section, front matter + text
  Code/Chapter <N>/00. Contents.md             chapter outline (cheap navigation)
  Code/00. Contents.md                         list of chapters
  Data/Code Tables/Table <section> <n>.csv     every HTML table, machine-readable
"""
import argparse
import csv
import re
import shutil
import sys
from pathlib import Path
from urllib.parse import urljoin

from bs4 import BeautifulSoup, NavigableString, Tag

sys.path.insert(0, str(Path(__file__).parent))
from common import CORPUS, TODAY, clean_name, county_dir, county_name, download, get, read_manifest, slug, upsert_manifest, write_md  # noqa: E402

BASE = "https://ecode360.com/"


def clean(s):
    return re.sub(r"\s+", " ", s).strip()


# ---------- HTML -> markdown ----------

def table_grid(tbl):
    """Expand colspan/rowspan into a rectangular grid of strings."""
    grid, pending = [], {}
    for tr in tbl.find_all("tr"):
        row, col = [], 0
        cells = tr.find_all(["td", "th"], recursive=False)
        ci = 0
        while ci < len(cells) or (col in pending):
            if col in pending:
                txt, left = pending[col]
                row.append(txt)
                if left <= 1:
                    del pending[col]
                else:
                    pending[col] = (txt, left - 1)
                col += 1
                continue
            c = cells[ci]
            ci += 1
            txt = clean(c.get_text(" "))
            cs, rs = int(c.get("colspan", 1) or 1), int(c.get("rowspan", 1) or 1)
            for k in range(cs):
                row.append(txt if k == 0 else "")
                if rs > 1:
                    pending[col] = (txt if k == 0 else "", rs - 1)
                col += 1
        grid.append(row)
    w = max((len(r) for r in grid), default=0)
    return [r + [""] * (w - len(r)) for r in grid]


def grid_md(grid):
    if not grid:
        return ""
    esc = lambda s: s.replace("|", "\\|")
    out = ["| " + " | ".join(esc(c) for c in grid[0]) + " |",
           "|" + "---|" * len(grid[0])]
    out += ["| " + " | ".join(esc(c) for c in r) + " |" for r in grid[1:]]
    return "\n".join(out)


class Converter:
    def __init__(self, county, att_dir, struct_dir, md_dir_for):
        self.county, self.att_dir, self.struct_dir = county, att_dir, struct_dir
        self.md_dir_for = md_dir_for
        self.attachments = {}  # url -> local path
        self.cur_section = ""
        self.cur_md_dir = None
        self.tables = 0

    def attach(self, href):
        url = urljoin(BASE, href)
        if url not in self.attachments:
            from urllib.parse import unquote
            fp = Path(unquote(url.split("?")[0]))
            stem = re.sub(r"\.tif$", "", fp.stem, flags=re.I)
            name = clean_name(re.sub(r"^TA\d+-", "", stem)) + fp.suffix.lower()
            dest = self.att_dir / name
            try:
                download(url, dest, self.county, "code", title=f"Attachment to § {self.cur_section}",
                         notes="eCode360 attachment")
            except Exception as e:
                print("  ! attachment failed", url, e)
                return None
            self.attachments[url] = dest
        return self.attachments[url]

    def rel(self, p):
        return Path(*[".."] * len(self.cur_md_dir.relative_to(CORPUS).parts)) / p.relative_to(CORPUS)

    def block(self, el, depth=0):
        """Convert an element's children to markdown lines."""
        out = []
        for ch in el.children:
            if isinstance(ch, NavigableString):
                t = clean(str(ch))
                if t:
                    out.append(t)
                continue
            if not isinstance(ch, Tag):
                continue
            cls = ch.get("class", [])
            if "litem" in cls:
                num = ch.find("a", class_="litem_number", recursive=False)
                body = ch.find("div", class_="litem_content", recursive=False)
                inner = self.block(body, depth + 1) if body else []
                lead = clean(num.get_text()) if num else ""
                pad = "  " * depth
                if inner:
                    out.append(f"{pad}{lead} {inner[0].lstrip()}")
                    out.extend(inner[1:])
                else:
                    out.append(f"{pad}{lead}")
            elif "level" in cls:
                out.extend(self.block(ch, depth))
            elif "para" in cls:
                t = self.inline(ch)
                if t:
                    out.append("  " * depth + t)
            elif ch.name == "section" and "definition" in cls:
                term = ch.find("dfn")
                d = ch.find("div", class_="deftext")
                t = self.inline(d) if d else ""
                out.append(f"**{clean(term.get_text()) if term else ''}** {t}".strip())
                for extra in ch.find_all(recursive=False):  # figures/tables beside the definition
                    if extra is not d and extra.name != "dfn" and not extra.find("dfn"):
                        out.extend(self.block_one(extra, depth))
            elif ch.name == "section" and "defitem" in cls:
                num = ch.find("a", class_="defitem_number", recursive=False)
                body = ch.find("div", class_="defitem_content", recursive=False)
                inner = self.block(body, depth + 1) if body else []
                lead = clean(num.get_text()) if num else ""
                out.append(f"{'  ' * depth}{lead} {inner[0].lstrip() if inner else ''}")
                out.extend(inner[1:])
            elif ch.name == "a" and "/attachment/" in ch.get("href", ""):
                p = self.attach(ch["href"])
                label = ch.get("data-title") or clean(ch.get_text(" ")) or "attachment"
                if p:
                    out.append(f"- Attachment: {label} → {self.rel(p)}")
            elif ch.name == "table":
                out.append(self.table(ch))
            elif "footnotes" in cls:
                t = clean(ch.get_text(" "))
                if t:
                    out.append(f"> Note: {t}")
            elif "history" in cls:
                out.append(f"*{clean(ch.get_text(' '))}*")
            elif ch.name == "img":
                out.append(self.img(ch))
            else:
                out.extend(self.block(ch, depth))
        return out

    def block_one(self, el, depth):
        wrap = BeautifulSoup("<div></div>", "lxml").div
        wrap.append(el.__copy__())
        return self.block(wrap, depth)

    def inline(self, el):
        parts = []
        for d in el.descendants:
            if isinstance(d, NavigableString):
                if d.parent.name not in ("script", "style"):
                    parts.append(str(d))
            elif d.name == "img":
                parts.append(" " + self.img(d) + " ")
            elif d.name == "a" and "/attachment/" in d.get("href", "") and d.find("img") is None:
                p = self.attach(d["href"])
                if p:
                    parts.append(f" [PDF: {self.rel(p)}] ")
        return clean("".join(parts))

    def img(self, im):
        src = im.get("src", "")
        if not src or src.startswith("/images/"):
            return ""  # ui icons
        par = im.find_parent("a")
        if par is not None and "/attachment/" in par.get("href", ""):
            src = par["href"]  # full-size image rather than thumbnail
        p = self.attach(src)
        return f"![figure]({self.rel(p)}) *(image; see file — content not in text)*" if p else ""

    def table(self, tbl):
        grid = table_grid(tbl)
        if not any(c for r in grid for c in r) and tbl.find("img"):
            return "\n".join(x for x in (self.img(i) for i in tbl.find_all("img")) if x)
        self.tables += 1
        name = f"Table {self.cur_section} ({self.tables}).csv"
        p = self.struct_dir / name
        with open(p, "w", newline="") as f:
            csv.writer(f).writerows(grid)
        # pdf / image links inside tables
        for a in tbl.find_all("a", href=True):
            if "/attachment/" in a["href"] and a.find("img") is None:
                self.attach(a["href"])
        for im in tbl.find_all("img"):
            self.img(im)
        return f"\n{grid_md(grid)}\n\n*(table also saved as {self.rel(p)})*\n"


# ---------- splitting ----------

SEC_RE = re.compile(r"^(?:§|SECTION)\s*((?:[A-Z]{1,3}\s)?[0-9A-Z:]+-[0-9A-Z]+(?:\.[0-9A-Z]+)*)")
CH_RE = re.compile(r"^(?:Chapter|Title|Article)\s+([0-9A-Z:]+)\.?\s*(.*)$")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--county", required=True)
    ap.add_argument("--code", required=True, help="eCode360 municipality code, e.g. TA0795")
    ap.add_argument("--guid", required=True, nargs="+",
                    help="node(s) to print: the whole-code node, or several Part/chapter nodes in order")
    ap.add_argument("--html", help="use an already-downloaded print html instead of fetching (single guid)")
    a = ap.parse_args()

    a.county = county_name(a.county)
    cdir = county_dir(a.county)
    raws = []
    for i, guid in enumerate(a.guid):
        suffix = "" if len(a.guid) == 1 else f" part {i + 1}"
        raw = cdir / "Originals" / "Code" / f"eCode360 {a.code} {TODAY}{suffix}.html"
        url = f"{BASE}print/{a.code}?guid={guid}"
        title = f"{a.county} County Code (eCode360 {a.code}) print view{suffix}"
        if a.html and len(a.guid) == 1:
            raw.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy(a.html, raw)
            download(url, raw, a.county, "code", title=title)
        else:
            download(url, raw, a.county, "code", title=title, force=True)
        raws.append(raw)

    # "Includes legislation through MM-DD-YYYY" lives on the code's table-of-contents page
    try:
        m = re.search(r"Includes legislation through ([0-9-]+)", get(f"{BASE}{a.code}").text)
        through = m.group(1) if m else "unknown"
    except Exception:
        through = "unknown"
    man = read_manifest(a.county)
    upsert_manifest(a.county, [{**man[str(r.relative_to(CORPUS))], "effective": f"legislation through {through}"}
                               for r in raws])

    # parse all parts as one document (chapter/article/section headings are siblings in each print view)
    soup = BeautifulSoup("<html><body>" + "".join(
        str(BeautifulSoup(r.read_text(), "lxml").body or "") for r in raws) + "</body></html>", "lxml")
    code_dir = cdir / "Code"
    if code_dir.exists():
        shutil.rmtree(code_dir)  # regenerate cleanly so repealed sections disappear
    struct = cdir / "Data" / "Code Tables"
    if struct.exists():
        shutil.rmtree(struct)
    struct.mkdir(parents=True)
    conv = Converter(a.county, cdir / "Originals" / "Code" / "Attachments", struct, None)

    heads = soup.select("h2.chapterTitle, h2.articleTitle, h3.title, h4.sectionTitle")
    chapter = article = ""
    ch_num = "misc"
    chapters = {}  # ch_num -> {"title":..., "items": [(sec, title, relpath)]}
    nfiles = 0
    for h in heads:
        title = clean(h.get_text(" "))
        hid = h.get("id")
        content = h.find_next_sibling(lambda t: isinstance(t, Tag) and t.get("id") == hid)
        if "chapterTitle" in h.get("class", []):
            m = CH_RE.match(title)
            ch_num = m.group(1) if m else slug(title)
            chapter, article = title, ""
            chapters[ch_num] = {"title": title, "id": hid, "items": []}
            sec_key, fname = f"ch{ch_num}", "00. History"
        elif "sectionTitle" in h.get("class", []):
            m = SEC_RE.match(title)
            sec_key = m.group(1) if m else slug(title)
            fname = sec_key
        else:  # article / subarticle heading
            article = title
            m = SEC_RE.match(title)
            if not m:
                chapters.setdefault(ch_num, {"title": chapter, "id": "", "items": []})["items"].append(
                    (None, title, None))
                # articles with no own text are just headings
                if content is None or not clean(content.get_text(" ")):
                    continue
                sec_key = fname = slug(title)
            else:
                sec_key = fname = m.group(1)
        if content is None:
            continue
        conv.cur_section = sec_key
        md_dir = code_dir / f"Chapter {ch_num}"
        conv.cur_md_dir = md_dir
        conv.tables = 0
        body = "\n\n".join(x for x in conv.block(content) if x.strip())
        if not body.strip() and fname != "00. History":
            body = "*(no text — heading only or reserved)*"
        path = md_dir / f"{fname}.md"
        meta = dict(county=a.county, source="eCode360 " + a.code, chapter=chapter, article=article,
                    section=sec_key, title=title, url=f"{BASE}{hid}", retrieved=TODAY,
                    current_through=through)
        write_md(path, meta, f"# {title}\n\n{body}")
        nfiles += 1
        if fname != "00. History":
            chapters[ch_num]["items"].append((sec_key, title, path.name))

    # indexes
    top = [f"# {a.county} County Code — chapter index", "",
           f"**Includes legislation through {through}** (eCode360 {a.code}, retrieved {TODAY}). "
           "Amendments adopted after that date are NOT in these files — check Originals/Legislation.", "",
           "One file per section under 'Chapter <N>/'.", ""]
    for ch, info in chapters.items():
        top.append(f"- [{info['title']}](<Chapter {ch}/00. Contents.md>) — {sum(1 for i in info['items'] if i[0])} sections")
        lines = [f"# {info['title']}", "", "[Chapter history/references](<00. History.md>)", ""]
        for sec, t, fn in info["items"]:
            lines.append(f"- [{t}](<{fn}>)" if fn else f"\n**{t}**\n")
        (code_dir / f"Chapter {ch}" / "00. Contents.md").write_text("\n".join(lines) + "\n")
    (code_dir / "00. Contents.md").write_text("\n".join(top) + "\n")
    print(f"{nfiles} section files, {len(chapters)} chapters, {len(conv.attachments)} attachments")


if __name__ == "__main__":
    main()
