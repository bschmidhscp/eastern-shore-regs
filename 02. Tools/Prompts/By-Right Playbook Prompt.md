# By-right playbook prompt (give to a Sonnet subagent; replace {COUNTY})

High Side's strategy on the Eastern Shore: take small residential subdivisions to **final, recorded approval by
right** — staff approval, no public hearing, and ideally **no public-notice process of any kind** (no adjoining-owner
letters, sign posting, published notice, or Planning Commission agenda) — on existing road frontage (no new road),
then sell the approved lots to a home builder. Buy or option the land, hire a civil engineer and a land-use
attorney, get the plat recorded, sell. We never pull building permits.

Write the **by-right playbook** for {COUNTY} County, MD: the exact, repeatable path from first call to recorded plat,
what it costs in county fees, how long it takes, and every trigger that knocks a project off the path. It must be
usable as a checklist by an engineer we hire, and its numbers feed our deal model.

Corpus root (quote paths; spaces): "/Users/brianschmid/Library/CloudStorage/GoogleDrive-brian@highsidecapitalpartners.com/Shared drives/Eastern Shore Land/Docs + Regs"
Outputs (write both):
1. "<root>/{COUNTY}/03. By-Right Playbook.md"
2. "<root>/{COUNTY}/01. Digests/Playbook Metrics.json"

Start from "<root>/{COUNTY}/00. Summary.md" (layer 1; most answers are there with citations) and
"<root>/01. Maryland/00. Summary.md" (state rules: septic tiers, perc, forest conservation, Critical Area, stormwater —
reference it, don't re-explain). Then verify and fill gaps in the county code — read only the sections you need:
- Search: `~/.venvs/esl/bin/python -I "<root>/02. Tools/search.py" '"minor subdivision" notice' --county "{COUNTY}" -n 8`
  (FTS5; quote phrases; try: "adjoining", "adjacent property owners", "posting", "notice", "sketch plat",
  "final plat", "percolation", "perc", "health department", "forest conservation", "stormwater", "recordation",
  "frontage", "private road", "access", "panhandle", "flag lot", "remaining lands", "original tract").
- Code: one file per section under "<root>/{COUNTY}/Code/" (each chapter folder has "00. Contents.md");
  "<root>/{COUNTY}/Code/00. Amendments Not Yet in Code.md" if present.
- Fees: "<root>/{COUNTY}/01. Digests/Fee Findings.md"; forms and fee schedules in "<root>/{COUNTY}/Documents/".
- Timing evidence: "<root>/{COUNTY}/01. Digests/" (Planning Commission / pre-application digests) — use only if minors
  appear there; otherwise say timing is an estimate.
Do NOT read whole folders or minutes. Cite every rule as (§ number or document + page). Mark estimates as estimates.

## 03. By-Right Playbook.md — required headings
1. **Bottom line** — 3–5 sentences: the by-right path's name, max lots, who decides, whether ANY public notice is
   required (be precise: none / adjoining-owner letters / sign / agenda), typical months to a recorded plat.
2. **Eligibility test** — a checklist a parcel must pass to stay on the path: zoning districts and density, lot
   minimums/width/frontage, the cumulative cap (count from which date / original tract), septic tier limits,
   Critical Area (RCA/LDA/IDA) limits, no new road, access rules (flag/panhandle lots, shared driveways), anything
   else that converts a minor into a major or sends it to the Planning Commission or Board of Appeals.
3. **Step-by-step path** — numbered steps from pre-application to recorded plat. For each: who (planning staff,
   health dept, DPW/stormwater, forest conservation, Critical Area Commission, soil conservation district, surveyor),
   what we submit, what they check, fee, and typical duration (cite or label "estimate"). Include the perc-test
   season and wet-season rules, the forest conservation plan, stormwater (ESD) for minors, plat signatures, and
   recording at the Circuit Court.
4. **Public notice** — exactly what notice (if any) applies to this path, with citations. If notice is required, say
   whether any variant of the path avoids it.
5. **Costs we pay** — county fees for a 3-lot and a 5-lot (or max-lot) minor, itemized, with FY and citation; list the
   consultant studies required (survey, perc/soils, FCP/FSD, wetland delineation, stormwater plan, CA report).
6. **Off-ramps** — every trigger that ends by-right status (variance, special exception, rezoning, growth allocation,
   W&S plan amendment, new road, more lots than the cap, etc.), and how to design around each.
7. **Open questions to ask staff** — the 3–6 things the code leaves unclear (call list for Brian/Ben).

## Playbook Metrics.json — exact keys (null when unknown; numbers as numbers)
{
  "county": "{COUNTY}",
  "path_name": "Minor subdivision",
  "max_lots": 0,
  "decider": "Planning Director",
  "public_hearing": false,
  "public_notice": {"required": false, "type": "none | adjoining-owner letters | sign posting | published | PC agenda", "cite": ""},
  "cumulative_cap": {"applies": true, "base_date": "YYYY-MM-DD or null", "counted_from": "original tract as of ...", "cite": ""},
  "months_to_recorded_plat": {"low": 0, "typical": 0, "high": 0, "basis": "cited | estimate"},
  "perc_season": {"months": "e.g. Feb-Apr", "cite": ""},
  "county_fees": {"lots_3": 0, "lots_max": 0, "fiscal_year": "", "cite": ""},
  "forest_conservation": {"applies_to_minor": true, "fee_in_lieu_psf": null, "cite": ""},
  "studies_required": ["boundary survey", "..."],
  "access": {"min_frontage_ft": null, "flag_lots_allowed": null, "shared_driveway_max_lots": null, "cite": ""},
  "off_ramps": ["..."],
  "open_questions": ["..."]
}

Finish with a 3-line reply: path, max lots, public notice (yes/no + type), typical months.
