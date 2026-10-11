# Eastern Shore Land — Start Here

*For Brian, Ben, and any AI assistant working on this shared drive. Read this first, then read the
**Project Log** (next to this file) for current status, decisions and findings, and the
**Change History** for exact wording changes in the regulations. Everything needed is on this drive —
no other account or link is required.*

## What this project is

We're evaluating how to make **small-scale residential land entitlements** (minor subdivisions and
similar) profitable on **Maryland's Eastern Shore**. Step one is a reliable, current corpus of every
rule that affects cost, timing and feasibility: zoning and subdivision codes, fee and impact-fee
schedules, comprehensive and water/sewer plans, state rules (Critical Area, septic, wetlands, forest
conservation, stormwater), map data, and Planning Commission / Board of Appeals / Council records.
Step two is comparing counties and narrowing to the best two or three.

- **Counties in scope:** Caroline, Cecil, Dorchester, Kent, Queen Anne's, Somerset, Talbot, Wicomico,
  Worcester. Talbot is the pilot. Incorporated towns have their own zoning and come later.
- **People:** Brian Schmid and Ben (partners; both manage this shared drive).

## Where things are

| What | Location | Link |
|---|---|---|
| Everything | `Docs + Regs/` | [folder](https://drive.google.com/drive/folders/1xlT-7qCx-VOBHL8NK7gUUAQ23kffB6Mf) |
| Guides, search database, comparisons | `Docs + Regs/00. Index/` | [folder](https://drive.google.com/drive/folders/1Hmh04fW_U-otCfBGBq1IXts_SRcYUnGG) |
| Statewide rules and map catalog | `Docs + Regs/01. Maryland/` | [folder](https://drive.google.com/drive/folders/1U2XjhPHcu4hHoiLThtfmgDpeyP2HKBsl) |
| Map source catalog (33 layers, parcel lookup recipe) | `01. Maryland/GIS/SOURCES.md` | [folder](https://drive.google.com/drive/folders/1zGPRpFAaVTJJ-9PRVBNBJqtJKoDImFyI) |
| Scripts | `Docs + Regs/02. Tools/` | [folder](https://drive.google.com/drive/folders/172WAqBPpqKkTDGqbKkT7QmDEmNVDIGGN) |
| Talbot County | `Docs + Regs/Talbot/` | [folder](https://drive.google.com/drive/folders/14_TrTThEqTsvNu_1JJpwaeoztYALTRkJ) |
| Talbot zoning & subdivision code (Ch. 190) | `Talbot/Code/Chapter 190/` | [folder](https://drive.google.com/drive/folders/1nodfjD4q-NmbaWZ2XWCSqdbcjO3k3jcK) |
| What changed in the regulations, word for word | `02. Change History.docx` (top of drive) | — |
| Backup with full version history (optional; needs repo access) | GitHub, private | [bschmidhscp/eastern-shore-regs](https://github.com/bschmidhscp/eastern-shore-regs) |

Each county folder has the same layout:

```
<County>/
  Code/            county code, one markdown file per section (e.g. Chapter 190/190-36.md);
                   each chapter folder has "00. Contents.md" (outline) and "00. History.md"
  Documents/       searchable text of PDFs (fees, plans, legislation…), with <!-- page N --> markers
  Meeting Minutes/ minutes and agendas as text, plus short summaries
  Data/            tables as CSV (e.g. the Table of Land Uses)
  Originals/       files exactly as downloaded — PDFs (readable directly), web pages, map layers (GeoJSON)
  Manifest.csv     one row per downloaded file: source URL, retrieved date, effective date, SHA-256
```

## How an AI should read this drive

**If you access Drive through a connector (e.g. Claude or ChatGPT with Google Drive):**
- Word, PDF and Google Docs files can be read directly.
- **Markdown (.md) files return empty when read directly.** Read them through search instead:
  search with `title = '190-36.md'` and the **maximum snippet length** (in Claude's Drive connector:
  `search_files` with `snippetVerbosity: MAX_ALLOWED`). The snippet contains the whole file for
  files up to ~25 KB, which covers nearly every code section.
- **Find things with Drive full-text search:** `fullText contains 'minor subdivision'` (add
  `parentId = '<folder id>'` from the table above to stay inside one county or chapter).
- Start from a chapter's `00. Contents.md` to see every section title, then open only what you need.
- Original PDFs (fee schedules, plans, minutes) are readable directly from `Originals/`.

**If you run locally with Google Drive for desktop (e.g. Claude Code):**
- Python env (once): `python3 -m venv ~/.venvs/esl && ~/.venvs/esl/bin/pip install pymupdf pymupdf4llm beautifulsoup4 lxml curl_cffi openpyxl`
- Ranked full-text search with page numbers and snippets:
  `~/.venvs/esl/bin/python -I "02. Tools/search.py" '"minor subdivision" AND lots' --county Talbot`
- Everything a parcel is subject to, from one point:
  `~/.venvs/esl/bin/python -I "02. Tools/gis_point_lookup.py" --lat 38.765 --lon -76.08`

**Either way:**
- Cite sections (`§ 190-36.2`) and documents with page numbers.
- **Check currency.** `Manifest.csv` has retrieved/effective dates. The Talbot code includes legislation
  through the date stated in `Talbot/Code/00. Contents.md`; later bills live in `Originals/Legislation`.
  Fee schedules turn over every July 1.
- After meaningful work, **add a dated entry to the Project Log** so the other person's AI stays current.

## Conventions

- Folder names are clean and properly capitalized; important shared folders are pinned with
  numbers (`00. Index`, `01. Maryland`, `02. Tools`). No underscore-prefixed names.
- `Originals/` is never edited by hand. Everything else is generated by the scripts in `02. Tools`
  and can be rebuilt from `Originals/`.
- The guides (this one, the Project Log and the Change History) are written in `00. Index/*.md` and
  published as Word copies at the top of the shared drive by `02. Tools/publish_guides.sh`. Edit the .md,
  then publish. The Change History is generated automatically by `02. Tools/sync_repo.sh`.
