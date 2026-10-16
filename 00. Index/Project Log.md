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
| Kent, Cecil, Queen Anne's, Caroline, Dorchester, Wicomico, Worcester, Somerset | ✅ Documents, digests, Fee Findings, summary (layer 1), Key Metrics — 2026-10-11/12 |
| County comparison table | ✅ `00. Index/County Comparison.md` — all 9 counties |
| Deal pro forma + Deal Board | ✅ all 9 counties re-priced 2026-10-14 on builder-residual lot prices, raw-land purchase (before-and-after), engineer-style test-fit layouts, public-road frontage only: **86 Pursue / 338 Diligence** (2026-10-16: development rights priced from MALPF easements) |
| By-right playbooks | ✅ all 9 counties — `<County>/03. By-Right Playbook.md` + `Playbook Metrics.json` (2026-10-13) |
| Screener restructure | ✅ Done — all 5 steps merged (PRs #13–#17, 2026-10-15/16); no deal number changed. Assumption impact ranking in `Screener/18.` |

## Open questions / watch items

- **Approval outcomes (2026-10-16):** the board's Pipeline now has Plat submitted / approved / recorded / Denied / Perc failed (live at the next publish). Record outcomes as they happen; at 10, `python -m screener.evaluate` tests our approval odds.
- **Low-confidence numbers that move results most (2026-10-16):** 1-ac septic lot floor, waterfront depth limit, whole-parcel remainder threshold, ag transfer tax share, rights floor (`Screener/18. Assumption Impact.md`).
- **Re-screen drift (2026-10-15; corrected 2026-10-16):** the screen's local lot comps use a rolling 36-month window, so each re-screen moves some deals (Caroline and Kent since 2026-10-14). The monthly refresh does re-screen (`run_all --refresh-data` implies `--screen`), so this is expected month to month — not a decision; the 2026-10-15 note saying otherwise was wrong.
- **Agricultural transfer tax is charged on lot sales (5%, median $27K on 91% of Pursue deals).** If it's computed on
  what we pay the owner for the land, it's ~$4.5K. Ask the land-use attorney which transfer triggers it in a carve-out
  closing at the plat (owner → us → builder at one table) and whether it can be computed on the raw-land consideration.
- **Builders may take lots down in phases** rather than all 3 months after the plat — ask when getting builder quotes.
- **Worcester BAT:** the 2026 Comp Plan (hearing 2026-10-06) says all new septic will require BAT (~$15K per lot to
  the builder). Not yet priced into Worcester lot prices; watch adoption and the code change. Other rewrites reviewed
  and low/no risk — `00. Index/Pending Rule Changes.md`.

- **The Deal Board is shared "Anyone with the link"** and now carries the deal tracker (offers, notes) and builder
  price checks — any signed-in person with the link can read them. Restrict it to invited people (Ben as Editor so he
  can write to the tracker) from the board's Share menu.
- **The builder package discount for 3+ lot sets is thin evidence** (17 packages, 80% range 2–45%; we underwrite 26%).
  Builder price checks logged on the board are the test; if builders quote near the model, lower it in deal.yaml.
- **Lot layouts are screening test fits** (drawn on every board aerial): have the civil engineer test-fit each Pursue
  deal before an offer. Private-road cost ($350/ft + $35K turnaround) is our estimate — get an engineer's number.
- **Builder construction cost ($150/sf, NAHB) drives every lot price** — get 2–3 Eastern Shore builder quotes
  (Screener/07. Lot Pricing Model.md shows the sensitivity).
- **Deal assumptions are mostly estimates (L):** engineering, survey, attorney, perc, private road, the carve-out
  premium over raw land, and the waterfall terms. Get 2–3 local quotes per county (Queen Anne's,
  Worcester, Cecil first) and the real term sheet; change `assumptions/deal.yaml`, re-run, republish.
- **Vacant land values are ±38%** (median model error) — check each Pursue deal's comps and range before an offer; the
  max bid, not the model value, is the price discipline.
- **Playbook open questions** (each county's § 7) — call staff before relying on a county: Cecil minor density,
  Queen Anne's delegation of minors to the Director, Talbot/Kent access caps, Wicomico 20-ac remainder.
- **Fees not posted for FY27** in Cecil (latest 2/2024), Kent (9/2024), Wicomico (planning section 2012–15), Worcester
  (FY26), Queen Anne's (FY27 impact fee inferred from a State fiscal note) — confirm with each county before underwriting.
- **Septic/perc fees, sewer connection charges and BAT costs** were not found for any county except Talbot (BAT) and
  Kent/Cecil (sewer allocation) — call county health departments.
- **Planning Commission / Board of Appeals records in Caroline, Dorchester and Cecil are mostly agendas** (no outcomes),
  so approval rates there are unknown.
- **Worcester never adopted septic tier maps:** Commissioners say a major subdivision on private septic is not
  eligible (2025-11-04) — 6+ lots need public sewer there. Confirm.
- **Somerset Subdivision Ordinance is not in the corpus** (zoning ordinance only refers to it); minor = 1–7 lots per
  the 2025 application form. Somerset zoning amendments had a hearing 2026-10-06 (outcome not found).
- **Pending local changes:** Dorchester Bill 2026-9 (RR lot sizes, not codified); Wicomico Critical Area rewrite
  (Bill 2026-02) and comp plan update; Worcester 2026 comp plan (hearing 2026-10-06); Caroline 2026 comp plan (final
  draft July 2026); Queen Anne's Res. 25-12 sewer moratorium (Kent Island) and Chapter 18:1 rewrite.

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

**Across counties (details in `00. Index/County Comparison.md` and each `<County>/00. Summary.md`):**
- **Minor-subdivision size differs a lot:** 3 lots (Talbot, Wicomico), 4 (Caroline), 5 (Cecil, Worcester), 7 (Kent,
  Dorchester, Queen Anne's, Somerset). All are decided by staff (Dorchester: Planning Commission chairman signs).
- **Impact / excise fee per new home:** none in Kent, Cecil, Somerset, Wicomico, Worcester; $5,000 in Caroline (schools) and
  Dorchester (excise, suspended in some years); Talbot $9,356; Queen Anne's ~$5.99/sf (≈ $15,000 for 2,500 sf).
- **Planning fees for a 3-lot minor are small everywhere** ($200–$1,375); impact fees and septic/BAT dominate.
- **Rural density is the real limiter:** Cecil allows 1 unit/acre in minor subdivisions (NAR/SAR/RR) — the most
  generous; Caroline 1/acre gross but only 4 lots; Kent 1 per 30 ac; Queen Anne's sliding scale 1 per 100 ac; Wicomico
  1 per 15 ac (3-lot minor right preserved); Dorchester 3 + 1 per 15 ac; Somerset AR sets only a 1-acre minimum lot
  (no per-acre cap) — septic/Tier IV and the Critical Area (~42% of the county) are the limits there.
- **Boards of Appeals grant almost everything** where decisions are recorded: 85–97% (Kent, Queen Anne's, Talbot,
  Wicomico, Worcester, Cecil).

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

### 2026-10-16 (day) — Hardening after the restructure: outages, as-of date, board outcomes, end-to-end test (Brian + Claude)
- Brian asked for all the follow-ups and to merge each on green CI. Screener PRs #18–#23. No deal number changed.
- **Monthly refresh fixed and outage-proof (#18).** A simulated outage (every download failing) showed `run_all
  --refresh-data` — what the monthly task runs — would have **crashed at its first stage on Nov 2 even with every server
  up** (a restructure step reordered stages). Fixed. Now each download keeps last month's copy if a server fails, a
  server that is down is asked once per run (an outage costs about a minute, not hours of retries), county zoning stays
  county zoning, and the run lists every input that isn't this month's. Tested end to end: the full refresh finished in
  13 minutes with every download failing.
- **As-of date (#19).** Every calculation counts back from one run date instead of the computer's clock, so the same data
  and `run_all --as-of <date>` give the same numbers on any later day. Parity snapshots record their date. CI now fails
  if any calculation reads the clock directly.
- **Approval outcomes on the board (#21)** — takes effect at the next publish: Pipeline statuses Plat submitted, Plat
  approved, Plat recorded, Denied, Perc failed, and an "Approval outcomes" tile. Once 10 are recorded, the evaluation
  harness tests our approval odds against them (`python -m screener.evaluate`).
- **End-to-end test in CI (#22):** the real screen and pro forma run on every code change against a 1,340-parcel slice of
  Kent (its Diligence deal prices exactly as in production); a planted pricing change fails it.
- **Assumption ranking 2.5x faster (#20)** (66 → 26 min) with identical results.
- **Tested, not changed (#23):** one definition of water distance and neighborhood value for both price models. Out of
  time it's a tie (lot-price error 31.80% either way), so nothing moved; recorded in the screener's Restructure Brief.
- **Correction:** the monthly refresh *does* re-screen (`--refresh-data` implies it), so the Caroline/Kent screen drift
  is normal month to month (watch item corrected).
- **Board:** not republished today (the outcome statuses and 4 date-drift files are pending); the Nov 2 monthly run
  publishes them through the checked plan, or publish on request.

### 2026-10-16 (overnight) — Restructure finished: steps 2–5 merged, no deal number changed (Brian + Claude)
- Brian asked to finish the restructure overnight and merge each step on green CI. Screener PRs #14 (step 2), #15
  (step 3), #16 (step 4) and #17 (step 5) — all checked the strict way (feature caches deleted, models refit, full run).
- **Step 2 — the pro forma is four stages.** `proforma.py` (1,012 lines) is now a short driver over `feasibility.py`
  (candidates, test fit, rights, timeline, odds), `valuation.py` (lot and land prices, carve-out cost), `finance.py`
  (soft costs, cash flows, tiers, downside / retail / sensitivity / Monte Carlo cases) and `reports.py` (explanations,
  flags, audit, outputs), each with its own tests. All 55 pro forma outputs byte-identical.
- **Step 3 — one evaluation harness** (`screener/evaluate.py`): every model is tested the same way (5-fold CV,
  out-of-time, year by year, assessor ratio study, accuracy gates, drift history). `python -m screener.evaluate` prints
  the scorecard in seconds; experiments are short files in the code repo's `experiments/` folder, results in the
  database (`evaluation_runs`). First experiment: widening the lot model's local adjustment from 3 to 5 km looked better
  in cross-validation but **worse out of time** (31.8% → 32.1%), so 3 km stays — hyperlocal wins again. An approval-odds
  slot will score our odds against real outcomes once 10 exist — **the board's Pipeline needs outcome statuses (plat
  recorded / approved / denied / perc failed) before any can be recorded** (a board change; Brian's call).
- **Step 4 — publishing is automated** (`screener/publish.py`, last `run_all` stage): a checked plan (model checks,
  file limits, aerials), batches of ≤255 with removals first, and a verify step that records the publish only when every
  file is on the board with the right size. Checked against the live board: 174 of 174 files match. The monthly task
  now follows it.
- **Step 5 — which assumptions matter** (`Screener/18. Assumption Impact.md`): every numeric deal.yaml number moved ±20%
  and every county re-priced. 93 of 163 move profit or tiers; the other 70 still feed something shown on each deal
  (investor split, max bid, Monte Carlo range, odds, the builder cross-check), so none is dead. **Firm up first — they
  move results most and are low-confidence:** the 1-acre septic lot floor, the waterfront lot depth limit, the
  whole-parcel remainder threshold, the ag transfer tax share, the $6,500 rights floor. Removed the two settings no code
  read (cul-de-sac radius; the unused downside gate — the downside case stays shown, not a gate).
- **Found along the way:** (1) parity snapshots only hold on the day they're taken — the models count months from today,
  so re-running unchanged code the next day moved ~20 of 11,987 land prices (board unaffected); branches are now checked
  against main run the same day. (2) The schools download timed out and failed a whole run; it now keeps the cached
  schools (same fix as soils). (3) Full run ~115 s (was 148 s).
- **Board not republished tonight:** nothing in the restructure changed a board number; today's 4 changed board files
  are date drift plus the two removed assumption rows. The Nov 2 monthly run publishes through the new flow (or publish
  on request).

### 2026-10-15 (late night) — Restructure step 1 done: every per-parcel fact in one place (Brian + Claude)
- Finished step 1 and opened screener PR #13 (merge into `main` on green CI, per Brian). **No output changed**: parity vs
  `pre-restructure` OK after a forced rebuild; the screen and the deals CSVs are byte-identical to the previous code in
  all nine counties; the board has 0 files to republish.
- **Now in the parcel tables (database `parcel_features`, one row per parcel, keyed by county + account):** everything
  from the earlier entry plus the screen's facts (zoning code, septic tier, sewer, PFA, town, Critical Area, protected
  land, wetland/flood), location value and schools, development rights already used (deed chain + SDAT), perc evidence
  (old lots nearby still vacant) and comps density (recent vacant-lot sales within 3 and 6 miles). The screen, the lot and
  land models (their training rows too) and the pro forma all read them. One location-value/schools function now.
- **Found:** re-running the screen today would change Caroline and Kent deals, because the local lot comps use a rolling
  36-month window and have moved since the 2026-10-14 screen. Not a bug, but it means the monthly refresh (which doesn't
  re-screen) and a re-screen can disagree; worth deciding whether the screen should re-run monthly. Also two parcel
  "points" are in use (the pro forma's and the models'); unifying them is a small model change for after the restructure.
- Full run ~110 s (was 148 s). Next: step 2 — split the pro forma into feasibility / valuation / finance / presentation.

### 2026-10-15 (night) — Restructure step 1 under way: one parcel site table (Brian + Claude)
- Resumed the restructure on branch `restructure` (screener repo; not yet pushed or PR'd). Parity vs `pre-restructure`
  holds at **zero differences** after every change, checked the strict way: feature caches deleted, land and lot models
  refit from scratch, full pipeline run (a plain run mostly replays cached fits, so it proves little).
- **New `screener/sites.py` + `run_all` stage `sites`:** every geometric fact about a parcel (water and shoreline, town
  distance, density, sewer/growth area, woods/fields/developed, assessor marsh/ag acres, wetland, flood, soils,
  broadband, Critical Area class) computed once for all 269,937 parcels. Cached; rebuilt only when county layers or the
  feature code change (~5 min, split across 8 cores). The database table `parcel_features` now carries all of it.
- **Switched to read it:** the pro forma (lot- and land-model inputs for candidates), the lot model's training sales,
  the package-discount measurement, and the lot-sale site detail. The land model's multi-parcel farm sales use the same
  functions on tract geometry. Duplicate feature code deleted from `lotprice.py`, `landvalue.py`, `proforma.py`.
- **Found:** (1) the lot and land models define "the same" features differently (water distance from the parcel's point
  to *tidal* shore vs. from its edge to *any* shoreline; neighborhood value needs 5+ homes in the land model only). Kept
  both (`lot_*` / `land_*` columns) since the restructure may not change outputs; unifying them is a model decision for
  after. (2) Database table `lot_sales_site` had no stage that rebuilt it — now rebuilt every run. (3) The soils step
  called USDA's service on every run and failed the run when it returned an error — now falls back to the cached survey.
- **Faster:** full run 148 s → 98 s (pro forma 39 → 19 s, packages and paper lots 13 → 4 s each).
- **Next in step 1:** the screener's own wetland/flood/Critical Area/PFA columns, zoning district, rights used / cap, perc
  evidence and comps density into the table; location value and schools (still computed per model). Then step 2 (split
  the pro forma). Merge before the monthly refresh on Nov 2 or pause it.

### 2026-10-16 (late) — PR #12 merged; restructure paused (Brian + Claude)
- Merged screener PR #12 (hyperlocal models, development rights, entitlement spread, parity tool, restructure brief)
  into `main`. The restructure has **not started** — it is paused at Brian's call. When resumed, start from
  `docs/Restructure Brief.md` in the screener repo and the saved `pre-restructure` parity snapshot.

### 2026-10-16 (evening) — Architecture review; restructure handed to a new session (Brian + Claude)
- Decision: **restructure the plumbing, not the models** — (1) one parcel feature table as the source of truth (every
  per-parcel fact computed once, in the database), (2) split the 1,000-line pro forma into feasibility / valuation /
  finance / presentation, (3) one model-evaluation harness (CV, out-of-time, IAAO, gates, history; a slot for approval
  odds), (4) automated publishing, (5) prune deal.yaml. No output may change: `python -m screener.parity --check
  pre-restructure` must show zero differences (snapshot saved; pipeline verified deterministic).
- Brief for the new session: code repo `docs/Restructure Brief.md` (architecture map, problems, target, rules,
  definition of done). Base: PR #12 (`hyperlocal-models`) — merge before starting.
- Data to pursue in parallel (Brian): owner responses, builder and engineer quotes (tracker); Bright MLS sold-land data
  through a broker; health department perc/septic records (MPIA request); county building permits.

### 2026-10-16 (afternoon) — Valuing development rights (Brian + Claude)
- **Sales can't price rights.** Re-fit the land model on by-right lots actually remaining at each sale (cumulative
  cap minus lots already carved from the original tract, from SDAT): no premium (vacant land with any remaining −8%,
  per extra lot ~0) — subdivision potential is lost in the noise of rural land sales.
- **Easements can.** MALPF Board of Public Works charts (Jun 2024 – Feb 2026, database table `malpf_easements`): the
  State paid per acre to retire ALL of a farm's rights — Cecil ~$5,700, Kent ~$5,700, Talbot ~$4,700, Queen Anne's
  ~$4,100, Somerset ~$3,900, Caroline ~$3,500, Dorchester ~$3,400, Wicomico ~$3,400, Worcester ~$2,300 (1 purchase).
  Cross-check: the land model's protected-land discount ≈ $3,100/ac on a Talbot farm — same range, a bit low.
- **Rule now in the model** (`deal.yaml development_rights`): rights cost per lot = easement $/acre × acres per right
  on the parcel, capped at the owner's share (50%) of the value the lot creates (lot price − raw acreage − soft costs;
  no buyer pays more), floored at $6,500 (Calvert TDR price; QA/Talbot TDR markets thin). The carve-out's land cost =
  carved acres at the farm's per-acre value + rights + any reserved-land discount. Median per lot on Pursue/Diligence
  carve-outs: Queen Anne's ~$33.5K (easement-implied), Talbot ~$39K and Kent ~$45K (half-spread cap), Cecil and
  Worcester at the $6.5K floor (plentiful rights per acre). Shown on each deal.
- **Result: 86 Pursue / 338 Diligence** (Queen Anne's 41, Cecil 28, Worcester 14, Talbot 3). Sensitivity to the owner's
  share: 25% → 115 Pursue, 50% → 86, 75% → 85. What owners accept for rights is now the biggest swing factor — the
  first owner responses in the tracker should calibrate `owner_share_of_spread`.

### 2026-10-16 (midday) — Correction: "raw land costs more than entitled land in Talbot" was wrong (Brian + Claude)
- Brian challenged the spread map. Two errors found and fixed:
  1. **Reserved land.** Talbot (AC/CP/WRC) and Queen Anne's (AG) require cluster subdivisions with permanently
     protected reserved land / open space — real law (Talbot § 190-73: "permanently protected", "perpetually restricts
     land development"; farming allowed). But it is a **per-lot slice**, not the whole farm: Talbot § 190-8.8.C.1 —
     lot + reserved land ≥ original acres ÷ development rights (a 137-ac farm with 9 rights: ~15 ac per lot); QA cluster
     1 lot per 8 ac with 85% open space. The model had treated the owner's entire remainder as protected, overstating the
     carve-out land cost. Now: the remainder is valued as one farm and the reserved share takes the land model's
     protection discount (−18%). Example: 137-ac Talbot AC farm, 2 lots — 28.5 ac reserved, rights cost $95K (was
     $354K); land per lot ~$52K vs. builder lot $67K.
  2. **Spread map:** whole-parcel deals with a house counted the house in "raw land"; the house lot is now netted out.
- Also found: the land model gives development rights **no value** — in rural land sales the "extra lots" term comes
  out negative and is dropped (assessments and site features already carry it). Public TDR benchmark: Calvert pays
  ~$6,500/right; QA and Talbot TDR markets are thin. The owner's by-right allowance is now reduced by our lots in the
  "after" valuation (correct, though the model doesn't price it). Expect owners to ask for more than raw value on
  farms with by-right lot potential — the offer-credibility panel and the 10% premium are the guard.
- **Result: 166 Pursue / 523 Diligence** (Queen Anne's 82, Cecil 54, Worcester 24, Talbot 4, Kent 2). Talbot now:
  raw land ~$66K/lot vs. paper lot $88K (gross +$17K/lot; about break-even after Talbot's higher soft costs on a 4-lot
  deal); its ~3-lot by-right cap keeps most Talbot deals under the $200K bar. Entitlement spread by county (net per lot,
  4-lot deal): Cecil +$21.6K, Worcester +$9.7K, Queen Anne's +$8.5K, Caroline −$7.6K, Talbot −$9.6K, Kent −$40K.

### 2026-10-16 (late morning) — Entitlement spread map (Brian + Claude)
- `Screener/17. Entitlement Spread.md` and board Map tab → "Entitlement spread": for all 11,987 parcels that pass the
  by-right screen (not only profitable deals), per lot: paper lot to a builder − the land's raw cost per lot (the
  deal's land price: before-and-after for carve-outs) − soft costs at a standard 4-lot deal (soft costs are mostly
  fixed per deal, so this compares places, not parcel sizes). Gross spread (before soft costs) is the pure location
  signal. Database table `entitlement_spread`.
- **Where entitlement adds the most:** Worcester (median net +$4K/lot, 54% positive; Newark, Berlin, Bishopville,
  Whaleyville +$15–21K/lot: cheap farmland, resort-area lot prices), then parts of Caroline and Cecil (Earleville,
  Warwick). **Least:** Talbot (raw land per lot $148K vs. paper lot $88K), Kent, Dorchester. Cecil and Queen Anne's are
  parcel-by-parcel (34–44% positive) — and they hold most Pursue deals because larger, pricier lots clear the $200K bar.
- Use: aim owner outreach at high-spread areas, including parcels the deal tiers don't pass today.

### 2026-10-16 (morning) — Land vs. home growth spread; like-for-like comps (Brian + Claude)
- **Growth since 2019, quality-adjusted:** paper lots +90% (~9.6%/yr), raw vacant land ~+60% (~7.6%/yr), homes +56%
  (~6.6%/yr). Lots have outgrown homes by ~22% (land leverage — the lot is the residual of the home's value — mostly in
  2025–26 as homes flattened) and outgrown raw land by ~2 pts/yr, so the entitlement spread has been widening. Raw
  lot price ÷ home value at the spot stayed ~18–21% because the mix of lots selling shifted cheaper. Year-to-year lot
  growth is volatile (−1% to +20%), so it isn't a timing signal; deals are underwritten at today's prices (no
  appreciation assumed), which leaves the widening spread as upside.
- **Like-for-like comps tested:** borrowing lot sales from areas with similar home values (beyond 3 km) did worse than
  the 4 nearest sales within 3 km (all lots 32.7–33.9% vs 31.8%; thin-comp lots 34.6–35.8% vs 33.6%). Proximity beats
  similarity — kept as is.
- **The heat map's role:** absolute home value at ~500 m is one of the strongest inputs to the lot and land models;
  local appreciation differences aren't detectable (three tests). No model change today.

### 2026-10-16 (early morning) — Assessments, Monte Carlo, repeat sales, accuracy gates (Brian + Claude)
- **Assessments** (Brian: "a bad way to value land vs sales data"): they never set a value — every price is fit to
  sales. Tested removing them as model inputs: lot out-of-time 31.8% → 32.7%, land 30.6% → 32.5% (bias −3% → −5%);
  as a non-market screen 31.8% vs 32.2% without. So they stay only in those two roles, re-tested on each refit. The
  "value vs. assessed" review flag was replaced with a sales-only check (land model vs. adjusted comparable sales).
- **Monte Carlo per deal** (board: "Simulated outcomes"): lot price, builder discount, land, soft costs, approval and a
  missed perc season drawn together, 2,000 runs. Typical Pursue: profit −$56K (P10) / $62K (median) / $426K (P90);
  chance of a loss 44% overall — almost all approval risk (lose deposit + soft spent) — and **6% if approved**.
- **Repeat sales:** 23,435 same-house resale pairs since 2008. Same houses up ~70% since 2019 (hedonic index, size/age
  held fixed: +59%; gap ≈ renovations). Local appreciation beyond the Shore trend does **not** predict at 0.5–5 km
  (9.6% unexplained either way) — property-specific, not neighborhood-level, in this period. Re-tested monthly.
- **Accuracy gates:** lot out-of-time ≤36%, bias ±10%; land ≤35%, ±10%; lot CV ≤34% (now 32/−3, 31/−3, 30) — a breach
  is a ❌ and the monthly refresh won't publish. Drift history kept (table `backtest_history`). Database: 38 tables.
- 128 Pursue (unchanged). All checks pass. PR #12.

### 2026-10-16 (overnight) — Model improvements #1-3: clean data, lot detail, ensembles and confidence (Brian + Claude)
- **Where the lot model misses:** mid-priced lots ($45K–$170K) ~25% typical miss, unbiased. "Tail" errors (cheapest
  sales +48%, priciest −32% when grouped by sale price) are mostly individual noisy sales — grouped by *predicted*
  value (assessor practice) the tiers are near even. Distances to the Bay Bridge, Salisbury, Ocean City, Wilmington
  and Easton don't explain misses (the 500 m home-value surface already does).
- **#1 Clean data (adopted):** lot sales judged against the assessor's land value *at the time of sale* (not today's
  higher one) and bank / estate / government sellers dropped. An upper cut was tested and removed — farm-use land is
  assessed far below market, so 10x+ ratios are normal and a 4x cap threw out good sales. Assessor-standard ratio study
  now in `10. Backtest.md`: COD 53, PRD 1.67 (single rural lot sales are noisy), tiers by predicted value near even.
- **#2 Lot-level detail (tested, not adopted):** each sale's own wetland, floodplain, wooded, soils share and broadband
  providers (MD iMAP, 32,749 census blocks). Effects are sensible (wetland −28%, wooded −21%, hydric −23%, well-drained
  +14%) but out-of-time accuracy didn't improve — the 500 m location and nearest-sale adjustment already carry it.
  Broadband data is coarse (1–4 providers/block). Kept in the database; perc odds already use soils/wetlands.
- **#3 Ensemble + confidence:** a gradient-boosted model alone did worse (30.7% vs 28.2%); a 25% blend gained 0.2 pts
  (noise) — not adopted. **Adopted:** each deal's lot price range and confidence are calibrated on what actually
  happened to similar lots out of time — waterfront 38% typical miss, inland with ≤6 lot sales within 3 km 33%, 7–15
  28%, 15+ 23%. Board shows confidence (high/medium/low), lot sales within 3 km and the middle-half range per lot.
- **Result: 128 Pursue / 482 Diligence** (27 moved up from Diligence on a ~3% higher builder price; package
  discount 22%). Lot confidence on Pursue: 16 high, 105 medium, 7 low (waterfront). All checks pass.
- Not yet built from the plan: repeat-sales price index, Monte Carlo deal outcomes, CI accuracy gates; poultry houses
  (no state layer — would need building-footprint detection or MDE permit records).

### 2026-10-16 (late night) — Hyperlocal (Brian: "real estate is a hyperlocal game") (Brian + Claude)
- **PR #11 merged.** New work on PR #12.
- **Location at ~500 m.** Fit on pre-2025 home sales and tested on 2025-26 sales, a 500 m location scale beat 750 m,
  1, 1.5 and 2.5 km (median miss 14.0% vs. 15.1% at 2.5 km). Lot model: CV 29.2%, out-of-time 31.9% (was 29.8% /
  32.7%). Somerset's persistent-bias correction is no longer needed — the model now sees its location value.
- **Recorded prices ≠ market prices:** home sales outside 0.5x–3x the assessment at the time of sale dropped (~6%;
  gifts, family/tax transfers, data errors), on top of the arm's-length filter and outlier trimming.
- **Land model** now uses home values from sales (both segments) and schools (land with a house): CV with local
  adjustment vacant 29.6% → 29.0%, improved 13.8% → 13.1%.
- **Builder cross-check** prices the specific house for each lot (local new-home size, new, this lot, these schools,
  today) with the joint home model; e.g. a new 2,400 sf house near Easton on 1.1 ac: $627K inland, $1.11M waterfront.
- **Local appreciation** (Brian: likely varies far more very locally than by county): county indexes ≈ Shore-wide
  (16.33% vs 16.37% CV); 2019–24 local trends didn't predict 2025–26 (corr 0.06); a recency-weighted local trend
  layer on top of the 500 m level made held-out 2025–26 predictions worse (14.4–14.7% vs 14.2%). The 500 m level —
  built from each spot's own sales — already absorbs most local appreciation; re-test as sales accumulate.
- **Result: 101 Pursue / 427 Diligence** (Cecil 40, Queen Anne's 33, Worcester 22, Talbot 4, Kent 2). All checks pass.

### 2026-10-16 (night) — Home value map, schools, one feature store (Brian + Claude)
- **Home value surface** (`Screener/16. Home Value Map.md`; board Map tab → "Home values"): 37,330 arm's-length home
  sales since 2019, fit jointly — living area (+57% per doubling), lot size (+6% per doubling, after separating it
  from location), age, waterfront (×1.75), **school proficiency (+9% per 10 points)**, and a **quarterly price index**
  (every past sale brought to today: prices +59% since mid-2019, flat over the last year). Location smoothed at
  ~10 km and ~2.5 km. Standard home (2,000 sf, 1 ac, built 2000–14) at the typical Shore location: ~$470K.
- **New vs. resale:** a brand-new home sells about the same as a recently built (2015+) resale of the same size and
  place (×0.98); new is ~9% over a 2000–14 home, ~13% over 1980–99, ~28% over pre-1980. The "new premium" is age.
- **Schools** (`screener/schools.py`): 181 Shore public schools (MD iMAP) matched to 2026 MCAP English + math
  proficiency (MSDE Report Card); nearest elementary/middle/high in the county.
- **Lot model** now uses home values from sales and school proficiency (CV 30.5% → 29.8%; out-of-time unchanged
  32.7%): ×1.15 per +10% home values, ×1.12 per +10 points proficiency.
- **Builder cross-check:** new-home comps are now escalated to today's prices (they weren't).
- **Parcel feature store** (`parcel_features` table, 269,937 parcels, builds in ~4 s): location value incl. schools,
  school scores, record data, last sale escalated to today — the shared base everything joins to on ACCTID. Database
  now 33 tables (home sales, price index, schools, value grid, lot sales/packages/listings, old lots, lot buyers).
- **Result: 90 Pursue / 416 Diligence** (11 new, 15 dropped). Package discount underwritten 29%; county corrections
  Dorchester ×0.93, Somerset ×0.93, Worcester ×1.07. All checks pass.

### 2026-10-16 (evening) — What's in the rule rewrites; a land-pricing bug; forest replacement (Brian + Claude)
- **Rewrites reviewed** (minutes, digests, legislation, posted drafts) → `00. Index/Pending Rule Changes.md`. None cuts
  rural minor subdivisions; several are pro-housing. Worcester **medium** (2026 plan: BAT on all new septic, 5-year
  pump-outs; zoning rewrite later; rights vest at recording). Somerset medium-low (rezoning contract awarded
  2026-10-06; tier review only at town fringes). Talbot low (Land Use draft 2026-09-03 keeps 1/20 RC/WRC, Tier IV,
  clustering — same text as 2016). Wicomico low/upside (Bill 2026-03 removed minors' 50% set-aside; plan 2027).
  Caroline low/upside. Queen Anne's low (school APFO only >7 lots). Kent, Cecil low. Dorchester none (smaller lots
  only with water/sewer). Tier remaps don't hurt minors — Tier IV allows minors everywhere. Talbot's Land Use draft
  added to the corpus. Each deal's Approval watch now carries its county's assessment.
- **Bug fixed:** the land model wasn't given candidates' woods/fields shares (vacant land: fully wooded −26%, all
  fields +15%), so farm-field tracts were priced ~12% low and wooded tracts ~25% high.
- **Forest replacement priced:** since 1 Jul 2026 every acre of forest cleared is replaced 1:1 (Ch. 457 of 2024):
  0.5 ac cleared per lot × wooded share × fee-in-lieu; median $5.3K on Pursue.
- **Result: 94 Pursue** (1 new, 15 dropped — mostly field tracts whose land now costs more; dropped deals' median
  profit $194K vs. the $200K bar). Kept deals: profit −$11.8K median. All checks pass.

### 2026-10-16 (later) — Owner extensions, approval watch, schedule/disapproval risks (Brian + Claude)
- **Owner extension payments** added as an expected soft cost on carve-outs: chance of missing a wet season × $2,500 per
  lot (deal.yaml, L). Median $0 on Pursue (most are on year-round soils), up to ~$5.6K. One Talbot deal dropped to
  Diligence: **108 Pursue**.
- **IRR shown as ">100%"** where it isn't meaningful (carve-outs: equity is mostly soft costs); headline shows median
  profit instead of median IRR.
- **Diligence pack:** owner-as-applicant and lender partial-release steps; how long approvals stay valid vs. the perc
  season.
- **Approval watch on every deal** (from each playbook's off-ramps, cited): pending rule changes (8 of 9 counties have a
  comp plan / zoning / forest rewrite in progress; Worcester rights vest only at recording), approvals that lapse
  (Talbot 12 months; Kent plat must record within 6 months; Dorchester final within 1 year of preliminary), and
  discretionary bumps to a public process (director referral to PC in Talbot/Kent/Wicomico; Worcester DRP "major
  impact"; Kent 30-day appeal window; Cecil staff treating a minor as major — LaPointe).
- Checked and not a risk for our product: Queen Anne's Res. 25-12 moratorium (sewered projects over 1,750 gpd only);
  other 2025–26 moratoria are on data centers, solar, cannabis. No Pursue deal fronts a state highway (SHA entrance
  permits not on the critical path).

### 2026-10-16 — Why platting takes so long; calendar-aware timelines (Brian + Claude)
- **Finding:** on a minor subdivision the planning review is quick (staff-approved; Worcester code: 30 days); the
  bottleneck is the **Health Department's septic approval, gated by the wet-season perc window** (Feb–Apr on most
  Shore soils, Nov–Mar in Wicomico; COMAR 26.04.02.04B). Somerset Board of Health minutes show the yearly cycle;
  Wicomico PC minutes (2026-05-21) record the planning director's frustration with Health/MDE, a 2026 state exception
  for off-season perc tests, and Health approval now required on letterhead before final plats. A Wicomico minor
  (Basch, lots 3–4) had PC approval Jan 2024 and Health final approval Sep 2026. The 33-month SDAT figure was
  inflated by crash-era holds, commercial parcels and family splits; the SDAT account-date lag is only months.
- **Model:** each deal now has its own months to plat. Season-gated deals (well-drained share < 50%) wait for the next
  window: 8–11 months if signed Aug–Nov (May–Aug in Wicomico), up to ~17 otherwise, plus a 15–42% chance (by hydric
  share) of missing a window (+12). Year-round deals: prep + review, ~8 months. Board: timeline row on each deal,
  "Perc any month" filter. Pursue unchanged at 109 (89% of Pursue are on soils testable year-round; carve-outs carry no
  land, so time moves IRR, not profit). Median Pursue months to plat 10 (8–17).
- One-lot-at-a-time pace raised from 8 to 20 months per lot (evidence; Brian approved).
- Diligence packs now ask the Health Department for the application deadline, backlog, off-season policy and letterhead
  approval; owner letters carry each deal's signing window (mail spring/summer, sign by fall, 24-month term with a perc
  contingency).

### 2026-10-15 (late night) — Calibration loop: every input tracked to its evidence (Brian + Claude)
- **Paper lots measured** (`Screener/14. Paper Lots Measured.md`): 143 lots from recent small subdivisions, sold one at
  a time, went for a **median 116% of the lot model** (refit without them); random vacant lots priced the same way come
  in at ~90%. New, surveyed, perc-approved lots sell at a premium. Not stacked on the price, because 3+ lot packages
  (−40%) are largely the same kind of lots: one at a time ~116%, a set to one buyer ~60%; we underwrite ~74%.
  Builder quotes decide where takedowns land.
- **Sell-out:** subdividers selling lots one by one averaged ~20 months between sales (26 projects) vs. the 8 months
  our "one at a time" side case assumes.
- **Purchase to recorded lots:** median 33 months (53 projects; Queen Anne's 11, Wicomico 19, Cecil 30, Worcester 35,
  Talbot 49) vs. ~9 months underwritten — see Open questions.
- **Lot listings ledger:** 228 vacant-lot listings (0.3–10 ac) logged with the model's price; asking runs 110% of model.
  Sales are matched from SDAT monthly — a free, growing out-of-sample test.
- **Cost quotes on the board:** each deal has a Cost quotes log (survey, civil, perc, topo, forest plan, wetlands,
  Critical Area report, attorney, title). A deal's own quote replaces our line; 3+ quotes for a line rescale it on
  every deal. Exported monthly to `Screener/Cost Quotes.csv`.
- **Calibration scorecard** (`Screener/15. Calibration Scorecard.md`, board Model tab): 15 inputs with evidence,
  status (Estimate → Measured → Quoted → Actual), impact and next step. 8 are still estimates — all soft-cost lines
  and builder construction cost.
- Pursue unchanged at 109 (nothing quoted yet). PR #11 updated.

### 2026-10-15 (night) — Lot price calibrated to the market; deal tracker on the board (Brian + Claude)
- **Builder package discount, measured** (`Screener/13. Package Discount.md`, `screener/packages.py`): 94 package sales
  (one seller, one date, 2–30 vacant lots, since 2019) vs. the lot model's price for one buildable lot that day.
  All packages: **14%** (80% range 7–24%) — mostly 2-lot sales. **3+ lot sets (what our deals sell): 40%** (2–45%,
  only 17 packages). Underwritten: **26%** (3+ blended toward all-package by count; deal.yaml). Package sales no
  longer count as single-lot sales in the lot model (multi-lot deeds record the total on each lot).
- **County bias:** tested year by year (2022, 2023, 2024, 2025+); most counties flip sign — noise, not corrected.
  Corrected only where the miss repeats 3 of 4 years by 10%+: Somerset ×0.94, Dorchester ×0.93, Queen Anne's ×1.03
  (`10. Backtest.md`). Recent-trend and regional fixes were tested and rejected.
- **Perc evidence from the ground** (`screener/perc.py`): rural lots recorded 1995–2014 within 2 km still without a
  house vs. the county rate. Tested on 14,826 lots: a lot's own buildout tracks this ~1:1 beyond its soils. Deal odds
  ×0.75–1.10 (half weight). Shown on each deal and in diligence packs.
- **Deal tracker + builder price checks on the board:** Pipeline tab; each deal has status (letter sent → in talks →
  offer → under contract), next step and date, offer, history; and a log of builder quotes vs. our lot price. Stored
  in the board's shared database; the monthly refresh copies them to `Screener/Deal Tracker.csv` and
  `Screener/Builder Quotes.csv` (`screener/tracker.py`). Nothing tracked yet.
- **Result: Pursue 241 → 109** (Diligence 447). Perc evidence + county corrections alone: 241 → 203; the 26% discount:
  203 → 109. Typical Pursue profit $269K, 3.6×, odds 62%. All checks pass.
- Board cleanup: 371 stale aerials removed (the board had hit its 512-file limit); publishes now remove stale files.
- **Next:** builder price checks on 3–5 Pursue deals (settles the discount); restrict board sharing; PR #11.

### 2026-10-15 (late) — Who buys lots, what moves each deal, diligence packs, owner outreach (Brian + Claude)
- **Who buys lots (`Screener/12. Who Buys Lots.md`):** traced from SDAT chains (vacant lot sale → house built → new home
  sold: the home's seller bought the lot). 796 lots, 275 buyers, 49 bought 3+: NVR/Ryan Homes 86 (median lot $165K),
  CMH/Clayton 62 ($44K), MD Residential by LaCrosse 48 ($68K), Gemcraft 40 ($99K), Davidson Development 26 ($55K).
  Each deal lists the most active lot buyers within 15 miles (last 6 years) — the builders to line up before the plat.
- **What moves this deal** on every deal: profit with lots −20%, owner's price +25%, soft costs +25%, one lot failing
  perc, and a 6-month delay (shown as IRR: carve-outs carry no land, so a delay costs time, not money). Typical
  Pursue: one lot failing perc −$112K, lots −20% −$92K, land +25% −$26K, soft +25% −$23K.
- **Diligence pack on request** (`python -m screener.diligence --acct …` → `Screener/Diligence/`) and **owner outreach**
  (`python -m screener.outreach` → `Screener/Outreach/<date>/`: mail-merge CSV + letter template, most-likely sellers
  first; opening price and walk-away kept internal; nothing is sent automatically). Owner names aren't published.
- **Lot model sharpened:** the local adjustment now uses the 4 nearest sales within 3 km — out-of-time error ±33%
  (was ±35%), CV 30.2%; Cecil no longer runs high (Somerset +21%, Wicomico +11% still do). Regional price indexes
  were tested and rejected (no improvement). Side effect: 53 deals entered and 53 left Pursue (borderline deals moved
  with closer comps) — see `Screener/11. What Changed.md`.
- **Historical replay:** no public archive of past parcel maps (MDP iMAP serves current boundaries only); MDP's
  Property Mapping Unit (410-767-4500) would have to supply older MdProperty View editions.

### 2026-10-15 (night) — Trust layer and monthly autopilot (Brian + Claude)
- **Automatic checks ("Check" badge + filter on the board):** a deal is flagged when our numbers disagree sharply with
  independent evidence — non-farm value vs. assessment; for farms (assessed at farm-use value) the land model vs. five
  adjusted comparable sales; asking price vs. our value; lot price vs. nearby lot sales; returns over 8×; layouts that
  fit few lots for their frontage. 19 of 241 Pursue flagged.
- **Backtest (`Screener/10. Backtest.md`):** fit before 2025, tested on 2025–26 sales never seen. Lots ±35%, bias 0%
  (priced as proven-buildable, as we price ours); raw land ±31%, bias −2%. By county the lot model ran high in Cecil
  (+12%), Somerset (+20%), Wicomico (+10%) and low in Dorchester (−29%) — treat those as optimistic/conservative.
  (A first version showed −46%; that was a bug in the backtest's frozen index, found and fixed.) A full replay of which
  tracts we'd have flagged years ago needs archived parcel/zoning maps (MDP MdProperty View editions).
- **Sell one lot at a time:** every deal now shows the case where lots go to end users one by one (full lot price, 6%
  commission, first sale 3 months after the plat, one every 8 months — history says 13; carve-outs close at the plat).
  Typical Pursue: profit $313K vs. $255K selling the set to a builder, but equity $175K vs. $96K and 24 vs. 12 months;
  every Pursue deal still clears 1.5×.
- **Live accuracy (`screener/calibration.py`):** listed board parcels and our values are logged (11 so far); when SDAT
  records the sale, the comparison is added to the backtest file.
- **What changed (`Screener/11. What Changed.md`)** since the last publish; **monthly autopilot** — scheduled task
  "Eastern Shore Deal Board — monthly refresh" (2nd of each month, 6 AM, after the regs refresh on the 1st): refresh
  data and listings (within the RentCast budget), re-run, publish only what changed, update this log, notify Brian.
  Runs while the Claude app is open; click "Run now" once to pre-approve its tools.
- **Tests + GitHub Actions** (9 fast tests; money math, builder math, layout, data rules) on every push/PR.

### 2026-10-15 (evening) — Which deals are listed for sale (Brian + Claude)
- RentCast key added (Brian's, stored only at `~/.config/esl/rentcast.key`). First sweep: 3,786 active listings
  (2,899 land, 887 homes on 3+ ac). **Pursue:** 1130 Old Love Point Rd, Stevensville listed (36.7 ac, ask $1.9M, 154 days; our
  max bid $911K); QA 1802011093 listed as part of a 162-ac sale ("Sparks Mill at Route 213", ask $2.43M, 891 days);
  841 Greenville Rd: a 6-ac piece (Damsontown Rd, $300K) is listed, not the 105-ac farm — Brian caught the first
  version reading it as the whole farm at $300K; listings now must match the parcel's acreage to count as the parcel.
  **Diligence:** 4 listed, 1 part listed.
- Cost controls (Brian: "don't crush me with costs"): monthly cap 40 requests (free plan = 50), counted before every
  call, no retries, 30-day reuse, resumable sweeps. 23 requests used this month (15 lost to two RentCast timeouts and
  a save bug, since fixed and tested offline). Off-market (past-year) sweeps time out on RentCast at Shore-wide
  radius — left off by default.

### 2026-10-15 (later) — Market tab; are lot prices falling?; full-freight lot comps (Brian + Claude)
- **Lot prices aren't falling.** The raw median lot price fell ~10% in the last 12 months because smaller, cheaper
  lots sold (median 1.24 vs 1.53 ac, fewer waterfront, more Somerset/Dorchester). Like-for-like lots rose ~9% (±9%);
  restated as a 1.5-acre lot, +13%. Volume is up 15% (416 vs 361 sales). Home prices are flat on a per-sf basis
  (+3% all counties; Talbot −5% is the one soft spot). Caroline's "drop": prior year's lots were twice the size and
  included three $300K–$1.35M outliers — per acre +28%, size-adjusted +16%.
- **New Market tab on the board** (`screener/market.py`, every run): lot sales, size-adjusted lot price, like-for-like
  change with its uncertainty, home $/sf, quarterly over three years, by county with sale counts.
- **Lot comps are now full freight and in the right setting:** sales under half the assessed land value (6.5% —
  family / distressed / troubled lots recorded as arm's-length) are dropped; a sewer-service / growth-area factor
  separates town-style lots with utilities; our lots are priced as rural, existing-road, septic, proven-buildable
  paper lots. 2,410 sales, CV error 31%. Comps are recorded vacant lots (paper lots), not finished subdivision lots.
- **Listings → `screener/listings.py`:** RentCast's licensed listings API (MLS-sourced; terms allow internal analytics,
  storage and display) — land and 3+ ac home listings, active and off-market in the past year, matched to parcels by
  location then address. Board: "Listed $X" badge, "Listed for sale" filter, listing panel (asking price, days on
  market, MLS #, agent, asking vs. our max bid). Needs Brian's RentCast key in `~/.config/esl/rentcast.key`; free plan
  (50 requests/month) covers a monthly sweep. Web search was tested and rejected (misses unindexed listings).

### 2026-10-15 — Who already does this (Brian + Claude)
- **`screener/developers.py` → `Screener/09. Who Does This.md`** (+ `Subdivision projects <date>.csv`, `Subdividers <date>.csv`):
  every rural tract split into new lot accounts since 2010, from SDAT transfer chains (seller names, prices, dates).
- **Findings:** 408 rural subdivisions since 2010 across nine counties: 187 sold as finished homes by a builder,
  107 family splits, **only 26 sold paper lots**, and in **only 6 did the subdivider buy the land and entitle it
  within 6 years** (Cecil ×2, Kent, QA, Wicomico, Worcester; LLCs). Those 6: land $11–63K per lot; lots sold
  $64–213K; revenue ÷ land 1.0–18×; but lot sales were slow — typically 6 of 14–37 lots sold, over 2–10+ years.
  Paper lots exist as a business here, but it's thin and absorption is the risk, not the spread.
- **Limits:** SDAT keeps three transfers per account; lots given new parcel numbers are missed; owners (buyers)
  aren't published. LLC principals: no free bulk source — Maryland's Business Express is per-entity only (state
  site use policy bars scripts); bulk = the SDAT Corporate Master File licensee or a commercial API.

### 2026-10-15 — Efficiency pass (Claude)
- **Pipeline 7–8 min → 55 s** when only costs/financing/tiers change (~3.5 min after code or data changes); results
  verified identical. Biggest fix: the lot layout was buffering whole road lines ~95,000 times per county; roads are
  now clipped to the parcel and each parcel's geometry is computed once. Per-parcel test fits, both price models,
  the land-sales table and the aerials are reused until something they depend on changes (README "Speed").
- **Board 10.2 MB → 1.9 MB** (faster on phones): only displayed columns are embedded; budget breakdowns load from
  `audit.json` the first time a deal is opened, with each source text stored once.
- **Publishing sends only changed files** (`publish_delta.json`, then `python -m screener.dashboard --mark-published`).

### 2026-10-14 (night) — Site constraints, per-lot septic, automated development rights, low-lot-price case (Claude)
- **Lots stay off wet ground:** wetlands and the 100-year floodplain (FEMA A/AE/AO/VE) don't count toward a lot's
  minimum area; every lot needs a 20,000 sf buildable envelope outside them and the tidal Critical Area buffer
  (100 ft; 200 ft in the RCA). Drawn in blue on the aerials. Several waterfront layouts shrank (e.g. the QA cove
  parcel: 2 waterfront lots, not 4–5 — most of its shore is marsh and buffer).
- **Septic per lot:** each lot's envelope must hold 10,000 sf on soils USDA rates suitable for septic; the share of
  lots that pass drives the perc odds (was a parcel-wide soil share).
- **Development rights already used — automated** (`screener/rights.py`): SDAT open data records the year each tax
  account was created and its tax-map parcel number; accounts carved from the same parcel since the county's cap base
  date (ever, where the rule has no date, e.g. QA sliding scale) count as rights used — with the deed-chain screen,
  the larger count wins. Lots are capped at what the county's cumulative cap has left (721 candidates capped); a MALPF
  preservation area on the account removes the parcel. No MDLandRec use.
- **Low-lot-price case on every deal:** profit and MOIC if every lot sells at the 25th percentile of the lot model.
- **Results:** 219 Pursue (Cecil 118, QA 75, Worcester 18, Talbot 5, Kent 2, Dorchester 1), 636 Diligence; candidates
  fell to 11,988 (constraints + rights). Typical Pursue: 4-lot carve-out, ~$96K equity, ~$260K profit if approved,
  3.7× MOIC, 56% odds. All checks pass.
- **Access options discussed (Brian):** Bright MLS has a RESO Web API but needs a data license via a Bright subscriber;
  MDLandRec automation would need a written bulk agreement with the State Archives (bulk subscriptions existed until
  FY24); MDP may have archived MdProperty View editions for parcel genealogy.

### 2026-10-14 (evening) — Lot price model: what a recorded, buildable lot actually sells for (Brian + Claude)
- **Brian: "I think we're drastically undervaluing paper lots."** Right. The production-builder residual on national
  (NAHB, $150/sf) costs said inland lots were worth ~$0–40K, yet buildable lots sell for $30–160K and builders keep
  building. Backing out what construction cost would reconcile them gives ~$90–125/sf, and scattered rural lots mostly
  sell to end users / custom builders at cost-plus, not to spec builders.
- **New lot price model** (`screener/lotprice.py`, card `Screener/08. Lot Price Model.md`): 2,579 arms-length
  vacant-lot sales (0.3–10 ac, 2019–2026, nine counties); drivers: size (+25% per doubling), tidal waterfront (×2.9),
  near water (×1.16), proven buildable — a house was built after the sale (×1.2), assessor non-perc (×0.6), value of
  homes around it, subdivision density, town distance, county, and a **year-by-year price index** (2019 = 100 → 2026
  = 197; used only to bring old sales to today — no future appreciation is assumed). Local adjustment from the nearest
  sales. **Cross-validated median error 32%.** Guardrails: neighborhood value held to the county's sales range; no lot
  above the county's 90th-percentile buildable-lot sale (inland / waterfront separately).
- **Underwritten lot price** = the model's value for our lot (planned size, proven buildable, location) − 15% package
  discount. The builder residual stays on every deal as a cross-check ("home prices support X% of the lot price").
- **Results:** 140 Pursue (QA 64, Cecil 49, Worcester 16, Wicomico 7, Kent 2, Dorchester 2), 696 Diligence; typical
  Pursue = 4-lot carve-out, ~$108K equity, ~$267K profit if approved, 3.6× MOIC. Median net lot price by county:
  Talbot $104K, QA $100K, Cecil $99K, Worcester $71K, Kent $56K, Caroline $52K, Wicomico $51K, Dorchester $40K,
  Somerset $27K. All checks pass.
- **Caution:** the Pursue list selects the parcels the model values highest, where its error is largest — confirm
  lot value with a local broker or two builder calls before an offer.
- **One-pagers are now on request** (`python -m screener.onepager --acct <account>`; or ask Claude), not rendered on
  every run; the board links only one-pagers made after the latest pricing.

### 2026-10-14 (day) — Builder-residual lot pricing, raw-land purchase, real lot layouts, auditable budgets (Brian + Claude)
- **Lot price = what a builder can pay** (Brian): nearby new-home price − construction ($150/sf NAHB) − rural lot
  development (well, septic/BAT, drive, power, stormwater, any private road) − permits/impact fee − overhead, selling,
  financing and the builder's 11% profit; capped at what comparable vacant lots sell for (a builder won't pay more for
  a paper lot than for a lot it can buy). Method, inputs, worked example and calibration: `Screener/07. Lot Pricing
  Model.md`. Finding: inland rural lots are worth ~$0–90K to a builder; waterfront lots $150–350K.
- **We buy raw land** (Brian: "the whole point is we add value via entitlements"). Whole parcel = the tract's raw
  market value. Carve-out (large tracts: contract for just the lot land, close at the recorded plat) = **before-and-after**:
  the tract's value today − what the owner's remaining land is worth after our lots use its development rights (open
  space where clustering is required), + 10%. Paying owners "lot value" leaves no margin by construction.
- **No demolition, no leftover-land sales** (Brian): an existing house stays on its own lot; we never resell acreage.
  Option / lots-only structures retired.
- **Real lot layouts** (`screener/layout.py`, drawn on every aerial): waterfront lots first (shore split so lots fan
  around coves); flag lots only where the code allows them (Talbot, QA, Worcester, Caroline, Cecil); a new private
  road only where the county allows one in a minor subdivision (QA, Kent, Caroline, Wicomico, Dorchester, Worcester —
  not Talbot, where any road makes it a Planning Commission "small scale" subdivision, nor Cecil, where it needs the
  major process + a variance) and only when it pays — the test fit tries one straight road + cul-de-sac from several
  frontage points and keeps the layout worth the most net of road cost. Lots never overlap, meet the zoning minimum
  and at least 1 ac without sewer (well + septic + reserve area), and lots are capped at what physically fits.
- **Frontage = public roads only** (US, MD, county, municipal, other public). Unnamed farm lanes ("LL") and private
  roads were counting as frontage — that inflated several waterfront Pursue deals.
- **Every budget line is clickable** on the board: formula with the deal's inputs, the source (deal.yaml key with its
  basis, county rule, model), and confidence H/M/L. No cross-deal totals anywhere (Brian: one deal at a time).
- **Assessor non-perc flag** (SDAT) now cuts the odds when >25% of a parcel is recorded non-perc.
- **MDLandRec:** the Archives' Acceptable Use Policy bars scripts/bots and re-posting images or data on third-party
  sites, so plat-history lookups stay manual (Plat History Worksheet); nothing from it goes on the board or GitHub.
- **Results:** 2 Pursue (Worcester 1, Queen Anne's 1 — both 5-lot carve-outs), 49 Diligence (Talbot 20, Worcester
  15, QA 11); typical Pursue: equity ~$108K, profit if approved ~$218K, 3.0× MOIC, 70% odds. Waterfront deals sit in
  Diligence on lower odds (Critical Area, flag lots, wetlands). All model checks pass.
- **Next:** engineer test fits + road cost on the Diligence waterfront deals; 2–3 builder construction quotes; a
  county zoning-verification letter and title/plat search on the two Pursue deals; confirm QA's delegation of minors.

### 2026-10-14 (overnight) — Waterfront lots, aerials, new map, investor one-pagers, redesign, cleanup (Claude)
- **Waterfront lots now priced from waterfront sales.** Tidal waterfront vacant lots (shoreline in the Critical Area)
  sell 2–4× inland lots: Talbot $575K vs $140K, Queen Anne's $420K vs $128K, Worcester $400K vs $128K. A parcel's
  new lots count as waterfront when its tidal shoreline gives each the district's minimum width (flagged "confirm the
  layout"); priced from waterfront lot sales within 10 km (else the county median), and the Critical Area buffer
  planting is budgeted (100 ft; 200 ft in RCA). Ponds and non-tidal streams don't count.
- **Aerial snapshot on every Pursue + top Diligence deal** (Maryland 6-inch imagery, parcel outlined, scale + north
  arrow). The first one exposed a false positive — an HOA common-area ring around a built subdivision — so
  **subdivision common areas are now excluded** (residential land assessed ~$0, or strip/ring-shaped parcels wrapping
  5+ small lots), in the screen and the pro forma.
- **Road names** for every parcel's frontage; Google Maps satellite/directions and property-record links per deal.
- **New board design** (High Side Brand Standards v1.2 · Digital addendum): app bar, KPI strip, segmented filters,
  slide-in deal panel (full-screen on phones) with aerial, returns (Deal / Investors / High Side), total budget,
  owner's view, site/approvals/title; real pan-and-zoom map (shoreline, routes, towns, parcel outlines, tap a deal).
- **Investor one-pagers** (`Screener/One Pagers/`, linked from each deal): Letter PDF — opportunity, by-right path,
  business plan, uses/sources/exit, projected Deal / Investor / High Side returns, risks. Confidential by default
  (town and county only); never shows our max bid or the owner's expectation. `python -m screener.onepager --reveal`
  adds the address.
- **Brand:** `My Drive/Logo/HSCP-Brand-Standards-Digital-Addendum-v1.2.pdf` — Geist / Geist Mono for screens and
  generated PDFs (Arial/Georgia stay for Office), screen neutrals, components, map/exhibit and one-pager specs.
- **Cleanup:** one command for everything (`python -m screener.run_all`, ~2 min); `proforma.py` split into
  `assumptions` / `finance` / `reports`; `checks.py` invariants (all pass — budget ties out, LP+GP = deal, …; they
  caught a real issue: tiny land loans cost more than they save → loans under $100K are dropped); retired the old
  per-parcel soils step; old dated outputs pruned; lint clean; README rewritten with the architecture.
- **Results:** Pursue 46 (Queen Anne's 31, Worcester 11, Cecil 2, Dorchester 1, Talbot 1), Diligence 244; 186 lots
  in Pursue (43 on tidal water), $19.0M equity, $18.6M profit if approved, median levered MOIC 1.92×.

### 2026-10-14 (early) — Owner's-view comps, land cover, deal / LP / GP returns, total budget, mobile (Brian + Claude)
- **Land cover:** wooded and cropland/pasture shares per tract (MDP land use/land cover 2010) added to the land model —
  vacant land 32% → 30% median error; land with a house 12% on 2–5 ac.
- **Comps the owner would recognize:** for each parcel, the 5 most similar recent sales nearby (houses vs houses, land vs
  land; similar size, woods, waterfront), each adjusted to the subject with the model's measured effects. Land price =
  reconciliation (geometric mean) of the model and the adjusted comps — tested best (14% / 11% on 2–5 ac with a house).
- **Owner's view on every deal:** assessment notice, what they paid (today's dollars), adjusted comps → owner's likely
  expectation (highest of the three) vs our max bid → credible / stretch / unlikely (`deal.yaml` land_value.credibility).
- **Returns:** one MOIC and one IRR (if approved) for the chosen financing; three rows — Deal, Investors (LP),
  High Side (GP) — check size, profit, MOIC, IRR, all from the same monthly cash flows. **Total budget** table:
  revenue, land, closing, soft costs, demolition, property tax, upkeep, farm lease, loan interest, selling costs.
- **Defaults (Brian):** levered and Pursue only. Tiers = levered projected MOIC + odds (Pursue ≥ 1.5×, ≥ 55%,
  ≥ $200k profit; Diligence ≥ 1.3×, ≥ 40%, ≥ $100k). Max bid targets a 1.5× unlevered MOIC.
- **Fixed:** leftover land now gets the same reconciliation as the purchase and can't exceed the land we paid for
  (a mismatch had inflated big-farm profits).
- **Phone and iPad:** deal cards on phones, collapsible filters, single-column details; trimmed columns on tablets.
- **Results:** Pursue 31 (Queen Anne's 19, Worcester 11, Cecil 1), Diligence 219; 27 of 31 Pursue offers credible.

### 2026-10-13 (night) — Why land values are hard; land model v2; Eastern Shore Land database (Brian + Claude)
- **Land model v2** (`Screener/06. Land Value Model.md`): added the assessor's full-market land value (at the sale;
  non-farm only), actual shoreline frontage and distance to water (state shoreline layer), marsh / ag-class shares
  (assessor CAMA land lines), value of surrounding homes, assessor valuation neighborhoods (micro-market pooling).
  Fixed: sales now classed by what they were **at the sale** (75 vacant lots with houses built since were mis-filed);
  commercial land and developer purchases (tracts subdivided after the sale) dropped. Result: land with a house
  **±14% median error (±12% on 2–5 ac)**; vacant land **±32%**.
- **Diagnosis:** vacant lots in the same subdivision sell within ~12% of each other, so the market isn't random — but
  most vacant sales are acreage tracts (median 2 sales per assessor neighborhood) whose price turns on things no
  public table records: perc/buildability, woods vs tillable, access and shape, timber, buyer type (neighbor, hunter,
  farmer). Better land data (MLS sold land with remarks, perc records) is what closes the rest.
- **Underwriting stance (Brian):** optimism — leftover land at the central estimate; the downside land case is shown
  on each deal but does not demote it. Results: Pursue 14 (Queen Anne's 8, Worcester 5, Cecil 1), Diligence 64.
- **Fixed:** farm-assessed land is taxed on its farm-use (preferential) value in carry; the state's "land value" for
  farms is full market (the old screen note was wrong).
- **Eastern Shore Land database:** `Eastern Shore Land/Database/Eastern Shore Land.duckdb` + `Data Dictionary.md` —
  23 tables (parcels, assessments, transfers/deed chain, assessor land lines, land sales, candidates, deals, builders,
  playbooks, rules, assumptions, land model, small map layers). Rebuild: `python -m screener.database` (~40 s).
- **Faster refreshes:** state map/records downloads now run 8 pages in parallel at the server's max page size
  (286k assessor records in 38 s); shoreline frontage vectorized (model rebuild 3.6 min → 14 s).

### 2026-10-13 (late) — Land value model for purchases and leftover land (Brian + Claude)
- **Why:** purchase price was a county $/acre bucket and leftover land was "our $/acre less 15%" — not how land trades.
- **Built `screener/landvalue.py`:** a model fit to ~4,700 actual arms-length rural sales (≥ 2 ac, last 5 years, outside
  towns, all 9 counties; multi-parcel farm sales grouped). Two segments: vacant **land** and **improved** (with a house).
  Factors: county, size (price per acre falls with size), Critical Area/water, RCA, wetlands, floodplain, easements,
  PFA, distance to town, soils, farm assessment, platted lot, time (≈ +6%/yr). 5-fold cross-validated.
  Model card with every coefficient and error: `Screener/06. Land Value Model.md`. Settings: `deal.yaml` → `land_value`.
- **Accuracy (honest):** improved rural property ±19% median error (±16% on 2–5 ac); vacant land ±38%. The vacant market
  is noisy (perc, woods, access, motivated sellers) — every deal now shows a likely range and its 5 nearest comps.
- **Finding:** raw land here carries **no measurable premium for unapproved development rights** (the sales gave those
  terms negative signs, so they were dropped). The approval is what creates the value — supports the strategy.
- **How deals use it:** purchase price = land value of the whole tract + what a house adds (1.21 × assessed
  improvements, measured from improved sales); a recent arms-length sale (≤ 36 months, time-adjusted) is used when
  within ±35% of the model, else averaged and flagged. Leftover land = same land model at its acres and remaining
  rights (none left → priced like easement-restricted farmland), at the 35th percentile, never above the whole tract.
- **Results:** Pursue 9 (Queen Anne's 4, Worcester 4, Cecil 1), Diligence 38. Large farms dropped out — the old method
  overstated leftover land on them.
- **Next:** shoreline frontage and woods/cleared land as factors; MLS or broker data on land listings would tighten the
  vacant-land error most.

### 2026-10-13 (later) — By-right playbooks, financing, plat history, sellers, builders (Brian + Claude)
- **County by-right playbooks (all 9):** `Docs + Regs/<County>/03. By-Right Playbook.md` + `01. Digests/Playbook
  Metrics.json` — eligibility checklist, step-by-step path to a recorded plat, public notice, county fees, off-ramps,
  staff call list. Written by Sonnet agents from the corpus with the shared prompt `02. Tools/Prompts/By-Right Playbook
  Prompt.md` (re-run per county when codes change). Review times are estimates (minors aren't minuted).
  - **Public notice on the by-right path:** none in Talbot, Cecil, Worcester, Wicomico, Caroline, Somerset;
    **adjoining-owner letters** in Queen Anne's and Kent; Dorchester's preliminary plat goes on a Planning Commission
    agenda (no hearing).
  - **Traps found:** Talbot allows only 2 lots off an original parcel onto an existing road (§ 190-35.2.B.5) — now
    modeled, Talbot drops out; Kent AZD same (2 lots); Cecil minor density disputed (1/ac in text vs 1 per 10 ac applied
    by staff in 2026) — modeled as a 0.7 odds factor until staff confirm; Wicomico's 3-lot right needs a ≥20-ac remainder.
- **Financing, month by month:** buy-structure cash flows (close, soft costs over the approval period, demolition,
  property tax at the actual assessment and county rate, insurance/upkeep, farm-lease income, loan interest, sale).
  Unlevered and levered (raw-land loan = lower of 50% of value / 60% of cost, 8.5% interest-only, 1% + $6k fees) —
  equity invested, profit, MOIC, IRR, expected MOIC. Timeline per county = playbook typical + 3 months prep, minimum 9.
  Tiers stay on unlevered expected MOIC (Pursue ≥ 1.40×, Diligence ≥ 1.20×). Board now shows MOIC (was profit ÷ equity).
- **Land price:** our estimate of what the land costs today — the last arms-length sale if within 5 years and
  plausible, else acres × market $/acre (higher of assessed land $/ac and nearby raw-land sale comps) + improvements.
  Shown with its basis on every deal, plus a **max bid** (price at which expected unlevered MOIC = 1.40×).
- **Plat history (automated screen):** deed-chain test from SDAT (`screener/history.py`) — parcels deeded out of the
  owner's deed and the prior owner's deed since the county's cap base date; feeds the odds and
  `Screener/04. Plat History Worksheet.md` (owner deed liber/folio for MDLandRec confirmation).
- **Seller signals:** absentee, inherited/estate transfer, no mortgage at last transfer, held 20+ years,
  not owner-occupied (0–5; filter on the board). **Builders:** entity sellers of new homes by county
  (`Screener/05. Builders.md`); each deal lists the three most active within 12 miles.
- **Conservatism added:** leftover land resold at a 15% discount to our basis.
- **Results:** Pursue 12 (Queen Anne's 7, Worcester 4, Cecil 1), Diligence 70, Watch 319 of 20,420 candidates.
- **Next:** call county staff with each playbook's open questions (Queen Anne's, Worcester, Cecil first); confirm the
  Pursue list's plat history on MDLandRec; local quotes; real term sheet and a bank quote for land loans.

### 2026-10-13 — Deal pro forma, Eastern Shore Deal Board, local soils (Brian + Claude)
- **Goal restated (Brian):** a formulaic way to take Eastern Shore projects to *final* approval by right — no public
  hearing or public notice — then sell the approved paper lots to a home builder. Buy (or option) the land, hire a
  civil engineer + land-use attorney, get approval, sell. No building permits. Existing houses get demolished.
- **Deal terms (Brian):** equity waterfall with outside investors; buying land cheaply is the base plan (options TBD);
  no debt by default (≤7 lots). So tiers and ranking use the **buy** structure; option and lots-only are shown as upside.
- **Every parcel is now priced as a deal** (`python -m screener.proforma`, 14 s for all 9 counties, no AI tokens):
  builder price per lot = lower of nearby lot comps less a 15% package discount and the builder residual (new homes
  nearby × 22% lot share − well/septic/BAT/driveway/electric/stormwater − impact fee); soft costs to final approval
  (survey, perc, civil, forest conservation plan + fee-in-lieu, wetlands/Critical Area, attorney, county fees, 15%
  contingency); demolition; ag transfer tax; three structures; odds of approval (soils, zoning source, plat-history
  risk, wetlands/flood, Critical Area, clustering, outlier comps); expected profit; investor/sponsor waterfall split.
- **Assumptions live in one file:** `assumptions/deal.yaml` (GitHub `eastern-shore-screener`), each with basis and
  confidence; county taxes/fees in `rules/<County>.yaml`. Readable copy: `Screener/03. Deal Assumptions.md`. Most cost
  items are our estimates (L) until we get local quotes. Waterfall terms (90% investor capital, 8% pref, 20% promote to
  15% IRR, 30% above) are placeholders.
- **Soils for every candidate, locally:** each county's USDA soil map is downloaded once (Web Soil Survey, ~25 MB) and
  overlaid on all parcels (`screener/soils.py`) — replaces per-parcel USDA queries (40+ min, top 150 only).
- **Results (buy, unlevered):** Pursue 22 / Diligence 115 / Watch 567 of 20,420 candidates. Queen Anne's 14 / 37,
  Worcester 6 / 26, Cecil 2 / 40, Wicomico 0 / 9, Kent 0 / 2, Talbot 0 / 1; Caroline, Dorchester, Somerset none.
  Shortlist: `Screener/02. Deal Shortlist.md`.
- **Eastern Shore Deal Board:** https://claude.ai/artifact/CBZiWuVtS4vecCcgEGvHxL — ranked deals with filters (county,
  tier, structure, odds, equity, land cost/lot price, status), map, county view, assumptions, and shared status + notes
  per parcel. Brian shares it with Ben by email as **Editor**.
- **Learned:** buying at market only works with 5+ lots or a cheap entry; Talbot's 3-lot cap leaves ~1 deal. Whole-farm
  buys assume the remainder resells at our cost basis — stress-test before relying on them. Lot comps far above the
  county median (waterfront) are blended down and flagged.
- **Next:** local quotes (engineer, surveyor, attorney) for Queen Anne's, Worcester, Cecil to replace L assumptions;
  plat history on the Pursue list; real waterfall terms; county by-right approval playbooks (see Roadmap).

### 2026-10-12 (later) — Screener v1.1 (Brian + Claude)
- Lot values now come from vacant-lot sales within 3–6 miles of each candidate (60–100% coverage by county;
  county median fallback marked *). Waterfront pockets now show far higher uplift (top Talbot/Worcester
  parcels ≈ $2.2–2.5M), and Wicomico (228) and Caroline (145) gained buy-list candidates in strong local pockets.
- Owner mailing address + absentee-owner flag (15–43% of candidates). Owner names stay manual: the SDAT site
  blocks automated lookups — use each candidate's SDAT link.
- Sewer: only septic Tier 1 or Talbot S-1 count as sewered; Tier 2 / Wicomico urban service districts flagged
  as planned and priced on septic (v1 was too generous).
- Still needed from Brian/Ben: per-county engineering/survey cost quotes (default $25k/lot), plat/title checks
  on shortlisted parcels, GIS zoning files from Kent, Dorchester, Somerset, Worcester.

### 2026-10-12 — Paper-lot screener v1 (Brian + Claude)
- Built a parcel screener for the lowest-risk model: staff-approved subdivisions only (no public hearing),
  lots on existing road frontage, engineering as the remaining risk; sell recorded lots to builders.
- Runs locally from statewide data (parcels, SDAT sales/values, zoning, Critical Area, septic tiers, easements,
  flood, wetlands, roads) + per-county rules distilled from the county summaries; USDA soils for the shortlist.
  No AI tokens per run. Results in `Screener/` (Drive); code in private repo `eastern-shore-screener`.
- Talbot: 22,368 parcels → 1,561 candidates (3,344 possible lots); vacant-lot comps $105k (0.5–2 ac) /
  $180k (1.5–4 ac); raw land ≈ $16.9k/ac. Most soils "very limited" for septic — drainage class used as perc proxy.
- All 9 counties screened (rules files distilled from each county summary; Cecil set conservatively to 4 lots).
  Buy-the-parcel candidates: Worcester 1,294, Cecil 1,051, Queen Anne's 842, Talbot 376, Dorchester 181, Kent 81;
  **Caroline, Wicomico, Somerset: none** — vacant-lot prices ($30–54k) don't cover ~$25k/lot soft costs.
  Strongest: Queen Anne's (5-lot staff minors, $140k lots, county zoning map) and Talbot; Worcester looks strong
  but its zoning is from the generalized map — verify before acting.
- Guards added: parcels on recorded plats in cumulative-cap counties are kept off the buy list (cap likely used);
  nominal "arms-length" prices ignored; acquisition floored at one lot value.
- Key gap: cumulative minor-subdivision caps need plat history per parcel (manual at MDLandRec for shortlist).
  See `Screener/01. Inputs and Roadmap.md`. Re-run any time: `python -m screener.run_all` (no AI cost).

### 2026-10-12 — Somerset finished; all 9 counties summarized (Claude)
- Somerset's first pipeline run got 0 documents (the site uses `<base href>`; crawler fixed in the other session) and
  was re-run: 805 documents. Then the same AI steps as the other counties: fees-and-gaps (added Res. 1218 FY26 and
  Res. 1181 fee schedules), 8 Haiku digest batches (two re-run after a usage-limit stop, resuming from partial CSVs),
  merge (Somerset's governing-body digest is "County Commissioners Land-Use Actions" and includes Sanitary Commission
  items), Sonnet summary + Key Metrics. Spot-checked the 7-lot minor and $225 + $25/lot fee (2025 application, Res.
  1218) and the AR lot standards (ZO § 6.2).
- Rebuilt the search index (12,062 files) and `00. Index/County Comparison.md` — now all 9 counties.
- Somerset highlights: no impact fee; 3-lot minor ≈ $300 in county fees; AR has only a 1-acre minimum lot; Critical
  Area ≈ 42% of the county; 61 of 64 decided zoning appeals granted; only 2 major subdivisions at PC in 3 years.
- **Next:** review the comparison with Brian/Ben and pick 2–3 counties; call county staff to fill the fee/septic gaps
  listed under *Open questions*; parcel screener (separate session).

### 2026-10-11 (late night 2) — County digests, fee research and summaries for 7 counties (Brian + Claude)
- Finished the AI steps for Kent, Cecil, Queen Anne's, Caroline, Dorchester, Wicomico and Worcester, matching the
  Talbot pilot: ~110 Haiku digest agents → `<County>/01. Digests/` (PC actions, Council/Commissioners land-use actions,
  Board of Appeals decisions/actions); a Sonnet **fees-and-gaps** agent per county → new
  `<County>/01. Digests/Fee Findings.md`; a Sonnet summary agent per county → `00. Summary.md` + `Key Metrics.json`.
  Spot-checked 3 load-bearing claims per county against the code (minor-subdivision threshold, density, impact fee):
  all matched.
- `00. Index/County Comparison.md` now covers 8 counties. Headline differences are under *Key findings → Across counties*.
- New prompt `02. Tools/Prompts/Fees and Gaps Prompt.md`; the summary prompt now uses Fee Findings and counts
  approval rates only from rows with a decision. `merge_digests.py` routes Board of Appeals parts by header (schema C
  `case_no` → Decisions table), so either schema merges correctly.
- Learned: subagents launched by a subagent share the same 20-agent limit, so the County Coordinator prompt only
  helps when the orchestrator isn't already running agents. A usage-limit stop mid-run left partial CSVs; agents were
  re-run with a "resume from existing CSV" instruction.
- Gaps: see *Open questions* (unposted FY27 fees; septic/sewer charges; agenda-only PC/BOA records in Caroline,
  Dorchester, Cecil; long Worcester Commissioner packets truncated in digest prep).
- **Next:** Somerset (pipeline re-running), then build_index, comparison, publish, sync.

### 2026-10-11 (late) — All 8 counties collected; monthly refresh scheduled (Brian + Claude)
- Automated runs finished for Cecil, Queen Anne's, Caroline, Dorchester, Wicomico, Worcester (Kent earlier).
  Fixes during the batch: eCode360 rate-limit backoff (Caroline re-run: 1,098 sections), crawler honors
  `<base href>` (Somerset's first run got 0 of 571 documents — re-running), 404s fail fast.
- Statewide rules completed in a separate session (`01. Maryland/00. Summary.md`).
- Monthly refresh scheduled (1st of month, 6 AM; `02. Tools/refresh_all.sh` + Project Log notes).
- Digests & summaries for the 8 counties run in a separate session (Brian), using
  `02. Tools/Prompts/County Coordinator Prompt.md` / `Session - County Digests and Summaries.md`.

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
- Fixed `sync_repo.sh`: it exited silently without committing whenever a changed file's diff exceeded 60 lines
  (`head` + `pipefail`). If an earlier sync printed nothing, it didn't push — re-run it.
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
