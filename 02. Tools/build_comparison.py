"""Build the cross-county comparison table from each county's 01. Digests/Key Metrics.json.

Writes 00. Index/County Comparison.md and .csv — one column per county, one row per metric, so the
narrowing decision is a single table. Run whenever a county summary is (re)written.

Usage: python -I "02. Tools/build_comparison.py"
"""
import csv
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from common import CORPUS  # noqa: E402

ROWS = [
    ("governing_body", "Governing body"),
    ("minor_sub_max_lots", "Minor subdivision: max lots"),
    ("minor_sub_cumulative", "Minor cap cumulative from original parcel?"),
    ("minor_sub_decider", "Minor decided by"),
    ("ag_density", "Agricultural density"),
    ("rural_residential_density", "Rural residential density"),
    ("max_lots_on_septic_tier_iv", "Max lots on septic (Tier IV)"),
    ("septic_tier_iv_share", "Tier IV share of county"),
    ("bat_septic_cost", "BAT septic cost"),
    ("planning_fee_3_lot_minor", "Planning fees, 3-lot minor ($)"),
    ("impact_fee_per_home_outside_towns", "Impact/excise fee per home, outside towns ($)"),
    ("impact_fee_per_home_inside_towns", "Impact/excise fee per home, inside towns ($)"),
    ("fees_fiscal_year", "Fee schedule year"),
    ("water_sewer_amendments_3yr", "Water & sewer plan amendments (3 yr)"),
    ("pc_actions_3yr", "Planning Commission actions (3 yr)"),
    ("pc_denials_3yr", "Planning Commission denials (3 yr)"),
    ("major_subdivisions_at_pc_3yr", "Major subdivisions at PC (3 yr)"),
    ("appeals_grant_rate", "Board of Appeals grant rate"),
    ("comp_plan", "Comprehensive plan"),
    ("code_current_through", "Code current through"),
    ("key_risks", "Key risks"),
    ("key_opportunities", "Key opportunities"),
    ("summary", "Summary file"),
    ("updated", "Updated"),
]


def main():
    data = []
    for p in sorted(CORPUS.glob("*/01. Digests/Key Metrics.json")):
        try:
            data.append(json.loads(p.read_text()))
        except json.JSONDecodeError as e:
            print("  ! bad JSON", p, e)
    if not data:
        print("no Key Metrics.json files yet")
        return
    names = [d.get("county", "?") for d in data]
    out = CORPUS / "00. Index"
    with open(out / "County Comparison.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["metric"] + names)
        for key, label in ROWS:
            w.writerow([label] + [d.get(key, "") for d in data])
    fmt = lambda v: ("yes" if v is True else "no" if v is False else f"{v:,}" if isinstance(v, int) else str(v)).replace("|", "/")
    L = ["# County Comparison", "",
         f"*{len(data)} counties. Built from each county's `01. Digests/Key Metrics.json` (written with its "
         "`00. Summary.md`). Use this to narrow; open a county's summary for the cited details.*", "",
         "| Metric | " + " | ".join(names) + " |", "|---|" + "---|" * len(names)]
    L += [f"| {label} | " + " | ".join(fmt(d.get(key, "")) for d in data) + " |" for key, label in ROWS]
    (out / "County Comparison.md").write_text("\n".join(L) + "\n")
    print(f"County Comparison: {len(data)} counties -> {out / 'County Comparison.md'}")


if __name__ == "__main__":
    main()
