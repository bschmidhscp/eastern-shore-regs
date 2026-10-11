# Eastern Shore Land — Project Log

*Newest entries first. Every work session (human or AI) adds a dated entry: what was done, what
was decided, what was learned, and what's next. Background and layout are in **Start Here**.*

## Current status

| Area | Status |
|---|---|
| Talbot — county code | ✅ Complete (eCode360, legislation through 2025-12-09; 905 sections) |
| Talbot — map data | ✅ 30 layers downloaded; point lookup tool working |
| Talbot — fee schedules | ⚠️ Have FY2026 only; FY2027 (effective 2026-07-01) still to find |
| Talbot — comprehensive plan, W&S plan | ⏳ In progress (county website being inventoried) |
| Talbot — 2026 Council bills | ⏳ In progress |
| Talbot — meeting minutes | ⏳ Not started |
| Statewide rules (COMAR etc.) | ⏳ Not started |
| Other 8 counties | ⏳ After Talbot pilot is reviewed |
| County comparison table | ⏳ After counties are collected |

## Open questions / watch items

- **Talbot 2026 Comprehensive Plan update** — Council action was scheduled for October 2026. Confirm
  whether adopted; the new plan may change growth areas and densities.
- **Bill 1627** (amends Ch. 190, release of reserved land agreements for MALPF) — hearing 2026-06-30;
  outcome unknown. Not in the eCode360 text.
- Any other 2026 Council bills amending Ch. 190 after 2025-12-09.

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
