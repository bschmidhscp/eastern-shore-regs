# Opening message for the "Statewide rules" session

Paste into a new Claude Code session started in the "Eastern Shore Land" shared drive folder:

---

Read CLAUDE.md, then `Docs + Regs/00. Index/Start Here.md` and `Project Log.md`. Task: build the statewide
layer in `Docs + Regs/01. Maryland/` — the Maryland rules that apply in all 9 Eastern Shore counties to small
residential subdivisions, so county summaries can reference them instead of repeating them.

Collect (official sources: COMAR via dsd.maryland.gov / regs.maryland.gov, statutes via mgaleg.maryland.gov,
agency guidance from MDE, DNR Critical Area Commission, MDP):
1. Chesapeake & Atlantic Coastal Bays Critical Area — Natural Resources Art. §8-1801 ff.; COMAR 27.01 (IDA/LDA/RCA
   density, buffer, lot coverage, growth allocation). Also Atlantic Coastal Bays (Worcester).
2. Septic — SB 236 Sustainable Growth & Agricultural Preservation Act (tiers; minor-subdivision limits in Tier IV;
   Land Use Art. / Env. Art. provisions); COMAR 26.04.02 (on-site sewage, perc testing); BAT requirements
   (COMAR 26.04.02.07) and Bay Restoration Fund (Env. §9-1605.2; COMAR 26.03.13).
3. Forest Conservation Act — Natural Resources Art. §5-1601 ff.; COMAR 08.19.
4. Stormwater — Env. Art. §4-201 ff.; COMAR 26.17.02; 2000 Design Manual (ESD).
5. Wetlands & waterways — COMAR 26.23 (nontidal), 26.24 (tidal); 26.17.04.
6. Land Use Article basics — comprehensive plan requirements, Priority Funding Areas, county water & sewer plans
   (Env. §9-501 ff.; COMAR 26.03.01), Maryland Agricultural Land Preservation Foundation (MALPF) and its
   effect on subdivision.
7. Real property transfer / recordation basics only if they affect entitlement cost (skip otherwise).

Method: use the tools in `02. Tools/` (fetch_list.py, to_text.py, build_index.py); save originals to
`01. Maryland/Originals/<Topic>/`, text to `01. Maryland/Documents/<Topic>/`, record in `01. Maryland/Manifest.csv`
(county "Maryland"). Use Sonnet subagents for bulk collection; keep raw text out of the main context.
Then write `01. Maryland/00. Summary.md` (~2 pages, every claim cited: [COMAR 27.01.02.05], [Nat. Res. §8-1808.1])
focused on what changes the cost, timing, or lot count of a 1–20 lot subdivision, and which choices are left to
counties (so county summaries know what to describe locally).
Finish per CLAUDE.md: Project Log entry, publish guides, sync repo.
