# Eastern Shore Land — Project Log

*Newest entries first. Every work session (human or AI) adds a dated entry: what was done, what
was decided, what was learned, and what's next. Background and layout are in **Start Here**.*

## Current status

| Area | Status |
|---|---|
| Talbot — county code | ✅ Complete (eCode360; includes bills through 1624, Mar 2026; 3 later bills listed in Code/00. Amendments Not Yet in Code.md) |
| Talbot — map data | ✅ 30 layers downloaded; point lookup tool working |
| Talbot — fee schedules | ⚠️ FY2026 only — county hasn't posted FY27; FY27 impact fees rose automatically (waiver failed 2-2, 2026-07-14) |
| Talbot — plans | ✅ 2016 Comp Plan + 12 village plans + 2 master plans; ⚠️ 2026 update not yet adopted/posted; no current CWSP document online (amendments only) |
| Talbot — legislation | ✅ 141 bills + 208 resolutions (2022–2026), indexed |
| Talbot — meetings & decisions | ✅ PC minutes (36, Oct 2023–), Council minutes (79), 159 Board of Appeals decisions, 26 pre-app agendas — all digested |
| Talbot — summary (layer 1) | ✅ `Talbot/00. Summary.md` |
| Statewide rules (COMAR etc.) | ⏳ Not started |
| Other 8 counties | ⏳ After Talbot pilot is reviewed |
| County comparison table | ⏳ After counties are collected |

## Open questions / watch items

- **Talbot 2026 Comprehensive Plan update** — drafts in work sessions Aug–Sep 2026; adoption not yet
  found. May change growth areas and densities.
- **FY27 fee schedules** — not posted; impact fees rose by the automatic ENR adjustment.
- **Septic Tier IV ceiling** — code implies max 7 lots on septic (small-scale); confirm with staff.
- **Minor-subdivision timelines** — decided by the Planning Director, not minuted; ask staff/engineers.

## Key findings so far

- **Soils:** NRCS rates almost every Talbot soil "Very limited" for septic. Lots outside sewer service
  areas depend on perc results and BAT (nitrogen-removing) septic — a real cost and timing factor.
- **Zoning source:** Use the county zoning layer. The state SDAT parcel `ZONING` field is blank for ~88%
  of Talbot parcels and stale where filled.
- **Ownership:** State parcel maps omit owner names; SDAT records give the prior owner and deed reference.
- **Water/sewer:** No statewide W&S GIS exists; each county must be checked. Talbot's S-/W- service areas
  are downloaded.
- **Minor subdivision in Talbot (Ch. 190):** no more than 3 new lots, **cumulatively** no more than 3
  lots ever divided from the original parcel, and **no new or modified road** (§ 190-78 definition).
  Decided by the Planning Director, not the Planning Commission (§ 190-66.2), though the Director may
  refer it to the Commission for a public forum; preliminary approval can include final plat approval.
  Fees: $400 base + $300/lot (non-Critical Area) or $350/lot (Critical Area), FY2026 schedule.
- **Impact fees (FY2026, single-family detached):** $9,356 outside municipalities, $8,080 inside.

## Log

### 2026-10-11 (later) — Talbot documents, digests and summary (Brian + Claude)
- Found Talbot's open upload-folder index (1,830 files) and its Granicus meeting archive; pulled 715
  documents: 141 bills, 208 resolutions, 79 Council minutes, 36 PC minutes, 159 Board of Appeals
  decisions, 26 pre-app agendas, comp/village/master plans, fees, septic/BRF, application forms.
- Converted all to text; OCR'd 246 scanned PDFs; search index now 1,629 files.
- Built layered access so nobody needs to read raw documents: `Talbot/00. Summary.md` (layer 1) and
  `Talbot/01. Digests/` (layer 2: legislation index, 211 PC actions, 151 appeals, 305 council
  land-use actions, 112 pre-app projects). Digests made by Haiku agents; summary by Sonnet, spot-checked.
- Findings: Board of Appeals granted 147/151 (123 with conditions); PC approved/recommended 129 items vs
  4 denials, 43 continuances; 66 water-sewer plan amendments in 3 years (many for existing homes, not
  new lots); only 9 major subdivisions at PC in 3 years; Bill 1627 enacted (eff. 2026-09-12).
- **Next:** statewide rules (`01. Maryland/`), then review the Talbot pilot with Brian/Ben before
  fanning out to the other 8 counties — each in a fresh session.

### 2026-10-11 — Corpus setup and Talbot pilot (Brian + Claude)
- Decided scope: all 9 Eastern Shore counties; towns deferred. Talbot as pilot to settle format and cost.
- Built the corpus structure in `Docs + Regs/` with clean, capitalized, numbered folder names.
- Downloaded the full Talbot County Code (55 chapters) from eCode360 and split it into one file per
  section, with tables saved as CSV and figures/attachments saved alongside.
- Converted Brian's FY2026 fee and impact-fee schedules to searchable text (tables preserved).
- Built the full-text search index and search tool.
- Cataloged 33 statewide/federal/county map layers; downloaded 30 Talbot layers (parcels, zoning,
  Critical Area, septic tiers, PFA, W&S service areas, easements, protected lands, etc.); built a
  one-point parcel lookup tool.
- Created the private GitHub repo for version history of text and tools.
- Created these guides so Ben and his AI can work from the drive directly; added an automatic
  Change History (word-level regulation changes) published at the top of the drive.
- Made the GitHub mirror public (github.com/bschmidhscp/eastern-shore-regs) so any AI can open it from
  a link; history was cleaned so it contains no personal emails.
- Found Talbot's open upload-folder listings: inventoried 1,830 files in seconds (141 Council bills,
  124 Council minutes, 138 transcripts, 208 resolutions, 159 Board of Appeals decisions since 2016–2022).
- **Next:** finish Talbot documents (comp plan + 2026 draft, W&S plan, FY2027 fees, 2026 bills,
  2–3 years of Planning Commission / Board of Appeals minutes), then statewide rules, then review the
  pilot before fanning out to the other 8 counties.
