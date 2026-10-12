# Opening message for the "County digests & summaries" session

Paste into a new Claude Code session started in the "Eastern Shore Land" shared drive folder (after the
automated county runs have finished — check `~/.cache/esl/<County>-console.log`):

---

Read CLAUDE.md, then `Docs + Regs/00. Index/Start Here.md` and `Project Log.md`. The automated pipeline
(`02. Tools/run_county.py`) has already downloaded, converted and indexed Kent, Cecil, Queen Anne's, Caroline,
Dorchester, Wicomico, Somerset and Worcester. For each county, finish the AI steps — following the Talbot pilot:

1. Review `<County>/02. Coverage Report.md`; fix obvious gaps (a missing key document listed in
   `02. Tools/County Configs/<County>.json` → add it with fetch_list.py). Note what can't be found.
2. Digests: batch lists are in `~/.cache/esl/<County>/digest/*.txt` (pc = Planning Commission minutes,
   boa/boam = Board of Appeals decisions/minutes, council/commissioners = filtered governing-body minutes,
   preapp, tac). Launch one Haiku subagent per batch with `02. Tools/Prompts/Digest Instructions.md`
   (Schema A for pc/council/commissioners/boam, B for preapp/tac, C for boa), writing CSVs to
   `~/.cache/esl/<County>/digest/parts/<batch>.csv`. Never read their transcripts. Then run
   `merge_digests.py --county <County> --parts ~/.cache/esl/<County>/digest/parts`.
   (Each batch list name = CSV name: pc-1.txt → parts/pc-1.csv, boam-2.txt → parts/boam-2.csv, etc.)
3. Summary: one Sonnet subagent per county with `02. Tools/Prompts/County Summary Prompt.md` ({COUNTY}
   replaced) → `<County>/00. Summary.md` + `01. Digests/Key Metrics.json`. Spot-check 3 load-bearing claims
   against the source sections yourself.
4. `build_comparison.py` → `00. Index/County Comparison.md`.
Run 2–3 counties' agents at a time. Finish per CLAUDE.md: Project Log entry (with the comparison's headline
differences), publish guides, sync repo.
