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
| Statewide rules (COMAR etc.) | ✅ `01. Maryland/00. Summary.md` + 72 COMAR chapters / statute ranges and 69 agency guidance docs (retrieved 2026-10-11) |
| Other 8 counties | ⏳ Pipeline built; sources being scouted |
| County comparison table | 🟡 `00. Index/County Comparison.md` started (Talbot) |

## Open questions / watch items

- **Talbot 2026 Comprehensive Plan update** — drafts in work sessions Aug–Sep 2026; adoption not yet
  found. May change growth areas and densities.
- **FY27 fee schedules** — not posted; impact fees rose by the automatic ENR adjustment.
- **Septic Tier IV ceiling** — code implies max 7 lots on septic (small-scale); confirm with staff.
- **Forest Conservation Act overhaul (Ch. 457 of 2024) took effect 2026-07-01** — reforestation now 1:1 for all
  clearing (½:1 in PFAs). Check each county's FCA ordinance was updated; mgaleg still labels the old text "in effect".
- **Stormwater regulation rewrite** — MDE draft of COMAR 26.17.02 (Sept 2025) not yet adopted; watch.
- **SB 236 county snapshot is dated** (MDP maps 2012/2017): confirm each county's minor-subdivision number and
  whether Queen Anne's, Dorchester and Worcester have since adopted tier maps.
- **Minor-subdivision timelines** — decided by the Planning Director, not minuted; ask staff/engineers.

## Key findings so far

**Statewide (details and citations in `01. Maryland/00. Summary.md`):**
- **Septic tiers cap lot count:** Tier IV allows only a minor subdivision on septic, with no later re-subdivision.
  Kent, Queen Anne's, Talbot, Dorchester, Wicomico and Somerset raised the minor-subdivision number to **7 lots**;
  Caroline, Cecil and Worcester kept their older definitions. Kent has a Tier IV exemption (MDP, 2017).
- **Critical Area RCA:** 1 unit/20 ac (no variance), 15% lot coverage, 200-ft buffer for new subdivisions, and the
  buffer must be fully planted (fee-in-lieu ≥ $1.50/sf only if planting is infeasible). Growth allocation is the only
  route to more density.
- **BAT septic** is mandatory statewide only in the Critical Area. BRF grants cover part of the BAT cost on new
  construction too (100% eligibility ≤$300K household income; 50–75% for businesses), less $1,200.
- **Forest conservation got costlier on 2026-07-01:** 1:1 replacement of all forest cleared outside PFAs;
  fee-in-lieu 30.5¢/sf inside a PFA and 36.6¢/sf outside (COMAR figure, indexed yearly).
- **Perc testing:** wet-season testing on high-water-table soils; 10,000 sf disposal area per lot.
- **Ag transfer tax:** 3–5% plus a 25% surcharge when farm-assessed land leaves agricultural use.

**Talbot:**

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

### 2026-10-11 (late night) — Statewide rules layer (Brian + Claude)
- Built `01. Maryland/`: statutes (mgaleg) and COMAR (regs.maryland.gov) for Critical Area, septic/SB 236/BAT/BRF,
  Forest Conservation, stormwater and sediment control, nontidal/tidal wetlands, comprehensive plans, PFAs, county
  water & sewer plans, MALPF and the agricultural transfer tax — one markdown file per COMAR chapter or statute range
  in `Documents/<Topic>/`, originals in `Originals/<Topic>/`, 744 manifest rows. New tool `02. Tools/statewide_fetch.py`
  with target list `02. Tools/Statewide Targets.csv` (`--force` to refresh). `search.py --county Maryland` now works.
- Two Sonnet agents collected 69 guidance documents (CAC buffer guides and model ordinance, FCA Technical Manual and
  2026 model ordinance, MDE BAT lists, OSSD site-evaluation guidance, BRF FY27 grant guidance, SB 236 guidance and
  MDP tier maps, Stormwater Design Manual, 2011 ESC standards, 2025 draft SWM rules, MALPF lot-exclusion forms, SDAT
  ag transfer tax). The two scanned ones (Worcester Critical Area review, MDE site-evaluation manual) were OCR'd.
  Checked the public GitHub push: no originals/PDFs, no personal data (only vendor contacts from MDE's public BAT lists).
- Wrote `01. Maryland/00. Summary.md` (cited; section 9 lists what each county summary must cover).
- Findings: see Key findings (statewide) above.
- **Next:** county digests and summaries (`Session - County Digests and Summaries.md`), citing the statewide summary.

### 2026-10-11 (night) — Pipeline proven on Kent; 7 counties running; hand-off (Brian + Claude)
- Scouts mapped all 8 counties into `02. Tools/County Configs/` (code host, meeting archive, key docs).
  All codes are on eCode360 except Somerset (PDF only); Cecil zoning and Kent's 2025 UDO are standalone PDFs.
  Meetings: CivicClerk (Cecil, Kent), CivicPlus AgendaCenter (Queen Anne's, Caroline, Dorchester, Wicomico),
  website archives (Worcester, Somerset). Adapters added for each.
- Kent ran end to end (285 files, code + UDO, 188 minutes/decisions). Fixes from the test: per-document
  conversion time limit, one-run-per-county lock, targeted OCR (skip meeting packets / long scans), digest
  prep skips packets and caps long documents (Kent digest work 40 → 11 batches).
- Gaps known before digesting: no impact fees in Kent, Dorchester, Wicomico, Somerset, Worcester (per scouts —
  confirm); Queen Anne's/Caroline Planning Commission minutes not posted (agendas used); Dorchester fee
  schedule is a scanned image; several counties have no posted water & sewer plan document.
- **Next (new sessions):** `02. Tools/Prompts/Session - Statewide Rules.md` and
  `Session - County Digests and Summaries.md` — opening messages for the next two sessions.

### 2026-10-11 (evening) — Pipeline for the other 8 counties (Brian + Claude)
- Turned the Talbot process into a config-driven pipeline (`02. Tools/run_county.py`): automatic document
  selection (matches 94% of Talbot hand picks), minutes pre-filter (halves digest reading), coverage
  report, Key Metrics + `00. Index/County Comparison.md`, saved agent prompts in `02. Tools/Prompts/`.
- Scouting agents are mapping each county's code host, meeting archive and key documents into configs.
- **Next:** adapters for any non-eCode360 code hosts / non-Granicus meeting archives, statewide rules
  (fresh session), then run counties 3–4 at a time.

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
