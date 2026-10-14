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

**Deal screener:** the folder `Screener/` (next to `Docs + Regs/`) holds the parcel screener's results —
`00. Summary.md` (all counties), `01. Inputs and Roadmap.md`, `02. Deal Shortlist.md` (every parcel priced as a
deal, top 40), `03. Deal Assumptions.md` (every valuation/cost/risk/financing number with its source and confidence),
`04. Plat History Worksheet.md` (deed-chain evidence to confirm on MDLandRec), `05. Builders.md` (who builds in each
county), `06. Land Value Model.md` (how raw-land purchase prices are valued, with accuracy), `07. Lot Pricing Model.md`
(the builder-residual cross-check), `08. Lot Price Model.md` (what a recorded, buildable lot sells for — the price we
underwrite, with accuracy and guardrails), `09. Who Does This.md` (who already subdivides here and how they did),
`10. Backtest.md` (how accurate the price models were on sales they never saw), `11. What Changed.md` (since the
last board update; refreshed monthly by a scheduled task on the 2nd), `12. Who Buys Lots.md` (builders who bought vacant lots and built — the exit), `Diligence/` (pre-offer pack per deal, on request: `python -m screener.diligence --acct <account>`), `Outreach/<date>/` (owner mail-merge file + letter template, on request: `python -m screener.outreach`; nothing is sent automatically), `One Pagers/` (investor PDFs, made on request: `python -m screener.onepager --acct <account>`), one folder per county with candidate, deal and builder CSVs, and `Dashboard/` (the Deal Board and its data).
On the board, every deal's aerial shows its screening lot layout (waterfront lots brass, inland white, any new private
road grey), and every budget line opens to show how it was built, its source and its confidence (H/M/L).
Code: private GitHub repo `bschmidhscp/eastern-shore-screener` — **all deal assumptions live in
`assumptions/deal.yaml`**; county taxes/fees in `rules/<County>.yaml`. Change a number there and re-run; never
hand-edit the generated files.

**Eastern Shore Land database:** `Database/Eastern Shore Land.duckdb` (top of the drive) holds every dataset the
screener gathers — parcels, assessments, the deed chain, assessor land lines, land sales, deals, builders, playbooks,
rules and assumptions — in one file queryable with SQL (DuckDB). Tables, columns and joins: `Database/Data
Dictionary.md`. Rebuilt by `python -m screener.database`; never edited by hand.

**Eastern Shore Deal Board** (interactive, ranked, map, shared status + notes): [claude.ai/artifact/CBZiWuVtS4vecCcgEGvHxL](https://claude.ai/artifact/CBZiWuVtS4vecCcgEGvHxL) — private
claude.ai page; Brian invites Ben by email as **Editor** so he can mark parcels and add notes (Viewers can only
read; adding a public link would also make Ben read-only). Refresh everything: `python -m screener.run_all`
(~2 min; add `--screen` or `--refresh-data` for a full rebuild), then republish the board to the same link.
**Brand for screens and generated PDFs:** `My Drive/Logo/HSCP-Brand-Standards-Digital-Addendum-v1.2.pdf`.

| What | Location | Link |
|---|---|---|
| Everything | `Docs + Regs/` | [folder](https://drive.google.com/drive/folders/1xlT-7qCx-VOBHL8NK7gUUAQ23kffB6Mf) |
| Guides, search database, **County Comparison** | `Docs + Regs/00. Index/` | [folder](https://drive.google.com/drive/folders/1Hmh04fW_U-otCfBGBq1IXts_SRcYUnGG) |
| Statewide rules and map catalog | `Docs + Regs/01. Maryland/` | [folder](https://drive.google.com/drive/folders/1U2XjhPHcu4hHoiLThtfmgDpeyP2HKBsl) |
| **Statewide summary** (Critical Area, septic tiers/BAT, forest, stormwater, wetlands, PFAs, MALPF) | `01. Maryland/00. Summary.md` | — |
| Map source catalog (33 layers, parcel lookup recipe) | `01. Maryland/GIS/SOURCES.md` | [folder](https://drive.google.com/drive/folders/1zGPRpFAaVTJJ-9PRVBNBJqtJKoDImFyI) |
| Scripts | `Docs + Regs/02. Tools/` | [folder](https://drive.google.com/drive/folders/172WAqBPpqKkTDGqbKkT7QmDEmNVDIGGN) |
| Talbot County | `Docs + Regs/Talbot/` | [folder](https://drive.google.com/drive/folders/14_TrTThEqTsvNu_1JJpwaeoztYALTRkJ) |
| Talbot zoning & subdivision code (Ch. 190) | `Talbot/Code/Chapter 190/` | [folder](https://drive.google.com/drive/folders/1nodfjD4q-NmbaWZ2XWCSqdbcjO3k3jcK) |
| What changed in the regulations, word for word | `02. Change History.docx` (top of drive) | — |
| Same text and tools with full version history — public, no login needed | GitHub | [github.com/bschmidhscp/eastern-shore-regs](https://github.com/bschmidhscp/eastern-shore-regs) |

Each county folder has the same layout:

```
<County>/
  00. Summary.md   layer-1 summary for small subdivisions (start here for a county)
  01. Digests/     one-line-per-item tables (legislation, PC actions, appeals, council, pre-apps)
                   + Fee Findings.md (impact/excise fee, fee schedule and FY, septic/sewer charges, cited)
                   + Key Metrics.json (feeds the County Comparison)
  02. Coverage Report.md   what was found / missing for this county
  03. By-Right Playbook.md the repeatable path to a recorded plat with no hearing: eligibility, steps, notice, fees,
                   off-ramps, staff questions (+ 01. Digests/Playbook Metrics.json, read by the deal model)
  Code/            county code, one markdown file per section (e.g. Chapter 190/190-36.md);
                   each chapter folder has "00. Contents.md" (outline) and "00. History.md";
                   "Code/00. Amendments Not Yet in Code.md" lists newer bills to read alongside
  Documents/       searchable text of PDFs (fees, plans, legislation…), with <!-- page N --> markers
  Meeting Minutes/ minutes, agendas and decisions as text (Planning Commission, County Council,
                   Board of Appeals, pre-application meetings)
  Data/            tables as CSV (e.g. the Table of Land Uses)
  Originals/       files exactly as downloaded — PDFs (readable directly), web pages, map layers (GeoJSON)
  Manifest.csv     one row per downloaded file: source URL, retrieved date, effective date, SHA-256
```

## Read in this order (don't drown in documents)

Answer from the cheapest layer that can answer; go deeper only to verify.

| Layer | What | Where |
|---|---|---|
| 0 | Orientation, status, decisions | this guide, the Project Log |
| 1 | **County summary** — rules, fees, process, risks for small subdivisions, all cited (~2 pages) | `<County>/00. Summary.md` |
| 2 | **Digests** — one line per item: Legislation Index, Planning Commission Actions, Board of Appeals Decisions, County Council / Commissioners Land-Use Actions, Pre-Application Projects, **Fee Findings** | `<County>/01. Digests/` (.md and .csv) |
| 3 | Search — snippets with file + page | Drive full-text search or `02. Tools/search.py` |
| 4 | Full code sections and documents — only to confirm a citation | `<County>/Code/`, `Documents/`, `Meeting Minutes/` |

Digests are AI-generated from the source documents; verify anything decisive in the source file named in the row.

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

**From GitHub (any AI that can open a URL):** the repo mirrors everything here except `Originals/`
(PDFs, map files) and the search database. Browse it at the link above, read raw files at
`https://raw.githubusercontent.com/bschmidhscp/eastern-shore-regs/main/<path>` (spaces as `%20`),
or `git clone https://github.com/bschmidhscp/eastern-shore-regs` to get the tools and text locally.
The repo is public: never commit personal emails, credentials or confidential deal data.

**Either way:**
- Cite sections (`§ 190-36.2`) and documents with page numbers.
- **Check currency.** `Manifest.csv` has retrieved/effective dates. The Talbot code includes legislation
  through the date stated in `Talbot/Code/00. Contents.md`; later bills live in `Originals/Legislation`.
  Fee schedules turn over every July 1.
- After meaningful work, **add a dated entry to the Project Log** so the other person's AI stays current.

## Adding or refreshing a county (pipeline)

1. Config: `02. Tools/County Configs/<County>.json` (code host, website, meeting archive, key documents).
2. Automated: `~/.venvs/esl/bin/python -I "02. Tools/run_county.py" --county <County>` — code, inventories,
   meetings, document selection, download, text + OCR, legislation index, digest batches, coverage report,
   search index. Progress log: `~/.cache/esl/<County>/run.log`.
3. AI steps: Sonnet fees-and-gaps agent (`02. Tools/Prompts/Fees and Gaps Prompt.md`) → `01. Digests/Fee Findings.md`;
   Haiku digest agents per batch list (`02. Tools/Prompts/Digest Instructions.md`) →
   `merge_digests.py`; Sonnet summary agent (`02. Tools/Prompts/County Summary Prompt.md`) writes
   `00. Summary.md` + `01. Digests/Key Metrics.json`; then `build_comparison.py`.
4. Review `<County>/02. Coverage Report.md`, then publish guides and sync GitHub.

Cross-county comparison: `00. Index/County Comparison.md` (one column per county).

**Monthly refresh:** a scheduled task on Brian's machine (1st of each month, 6 AM) runs
`02. Tools/refresh_all.sh` for every county, then logs what changed in the Project Log and the
Change History. New minutes are downloaded but not digested until a digest pass is run.

**Statewide layer (`01. Maryland/`):** `00. Summary.md` (layer 1, cited) → `Documents/<Topic>/` (one markdown file
per COMAR chapter or statute range, plus agency guidance) → `Originals/<Topic>/`. Topics: Critical Area, Septic and
Sewage, Forest Conservation, Stormwater, Wetlands and Waterways, Land Use and Growth, Agricultural Preservation,
Transfer Taxes. Refresh the law with `02. Tools/statewide_fetch.py --targets "02. Tools/Statewide Targets.csv"`
(add rows there to collect more chapters or sections). County summaries should cite the statewide
summary rather than repeat it, and cover the county choices listed in its section 9.

## Conventions

- Folder names are clean and properly capitalized; important shared folders are pinned with
  numbers (`00. Index`, `01. Maryland`, `02. Tools`). No underscore-prefixed names.
- `Originals/` is never edited by hand. Everything else is generated by the scripts in `02. Tools`
  and can be rebuilt from `Originals/`.
- The guides (this one, the Project Log and the Change History) are written in `00. Index/*.md` and
  published as Word copies at the top of the shared drive by `02. Tools/publish_guides.sh`. Edit the .md,
  then publish. The Change History is generated automatically by `02. Tools/sync_repo.sh`.
