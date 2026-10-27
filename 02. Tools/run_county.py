"""Run the whole automated pipeline for one county from its config (02. Tools/County Configs/<County>.json).

Steps (each idempotent; pick with --steps, default all):
  code       county code -> <County>/Code (eCode360 / Municode / American Legal adapters)
  inventory  open folder listings (list_dirs) + targeted crawl of planning/council pages (crawl_links)
  meetings   meeting archives (Granicus, CivicPlus AgendaCenter) -> Originals/Meeting Minutes
  select     pick documents from the inventories (select_docs)
  fetch      download picks (fetch_list)
  text       convert to markdown (to_text) + OCR scans (ocr)
  index      legislation index, digest batches (digest_prep), coverage report, search index
Then an orchestrating AI runs the digest agents and the summary agent (see 02. Tools/Prompts/).

Usage: python -I "02. Tools/run_county.py" --county Kent [--steps code,inventory,...]
Logs go to ~/.cache/esl/<County>/run.log (progress lines also printed).
"""
import argparse
import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
sys.path.insert(0, str(TOOLS))
from common import county_dir, county_name  # noqa: E402

PY = [sys.executable, "-I"]
ALL = ["code", "inventory", "meetings", "select", "fetch", "text", "index"]


def run(log, *args, timeout=3600):
    cmd = PY + [str(TOOLS / args[0])] + [str(a) for a in args[1:]]
    t = time.time()
    p = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    out = (p.stdout + p.stderr).strip()
    log.write(f"\n$ {' '.join(map(str, args))}\n{out}\n")
    log.flush()
    tail = "\n".join(l for l in out.splitlines() if "deprecated" not in l)[-600:]
    print(f"  [{args[0]}] {'ok' if p.returncode == 0 else 'FAILED'} in {time.time()-t:.0f}s\n    " +
          tail.replace("\n", "\n    "), flush=True)
    return p.returncode == 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--county", required=True)
    ap.add_argument("--steps", default=",".join(ALL))
    a = ap.parse_args()
    cname = county_name(a.county)
    cfg = json.loads((TOOLS / "County Configs" / f"{cname}.json").read_text())
    steps = a.steps.split(",")
    work = Path.home() / ".cache" / "esl" / cname
    work.mkdir(parents=True, exist_ok=True)
    picks = work / "picks.csv"
    import fcntl
    lock = open(work / "run.lock", "w")
    try:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)  # one pipeline run per county at a time
    except BlockingIOError:
        sys.exit(f"{cname}: another run_county is already running — not starting a second one")
    log = open(work / "run.log", "a")
    county_dir(cname).mkdir(exist_ok=True)
    print(f"== {cname} ==", flush=True)

    if "code" in steps:
        c = cfg.get("code", {})
        host = (c.get("host") or "").lower()
        guids = [str(c["root_guid"])] if c.get("root_guid") else []
        for name, g in (c.get("part_guids") or {}).items():  # no whole-code node: print each Part
            if guids and c.get("root_guid"):
                break
            if "disposition" in name.lower():
                continue
            lo, _, hi = str(g).partition("-")
            guids += [str(x) for x in range(int(lo), int(hi) + 1)] if hi else [lo]
        if host == "ecode360" and c.get("id") and guids:
            run(log, "ecode360.py", "--county", cname, "--code", c["id"], "--guid", *guids)
        elif host == "municode" and (TOOLS / "municode.py").exists():
            run(log, "municode.py", "--county", cname, "--url", c.get("url", ""))
        elif host in ("amlegal", "american legal") and (TOOLS / "amlegal.py").exists():
            run(log, "amlegal.py", "--county", cname, "--url", c.get("url", ""))
        else:
            print(f"  [code] no adapter for host '{host}' — handle manually", flush=True)

    if "code" in steps:
        for key, label in (("zoning_ordinance", "Zoning Ordinance"), ("udo", "Unified Development Ordinance"),
                           ("subdivision_regs", "Subdivision Regulations")):
            url = (cfg.get("documents") or {}).get(key, "")
            # configs may annotate URLs: "https://… (verified 200 pdf)" — keep the URL, spaces included
            if isinstance(url, str) and url.startswith("http"):
                m = re.match(r"https?://.+?\.(?:pdf|docx?|xlsx?)\b", url, re.I)  # file URLs may contain spaces/parens
                url = m.group(0) if m else re.split(r"\s+[(\[]|\s+-\s|\s+\|", url)[0].strip()
            else:
                url = ""
            if url:
                run(log, "pdf_code.py", "--county", cname, "--url", url, "--name", label)

    if "inventory" in steps:
        if cfg.get("upload_listings"):
            run(log, "list_dirs.py", "--county", cname, "--start", *cfg["upload_listings"])
        if cfg.get("crawl_starts"):
            run(log, "crawl_links.py", "--county", cname, "--label", "Planning and Council Pages",
                "--max-depth", "2", "--max-pages", "800", "--start", *cfg["crawl_starts"])

    if "meetings" in steps:
        m = cfg.get("meetings", {})
        since = cfg.get("selection", {}).get("minutes_since", "2023-10-01")
        for body, spec in (m.get("bodies") or {}).items():
            if not isinstance(spec, dict):
                continue
            if m.get("platform") == "granicus" and spec.get("view_id"):
                run(log, "granicus.py", "--county", cname, "--host", m["host"], "--view", spec["view_id"],
                    "--body", body, "--since", since, "--download")
            elif m.get("platform") == "civicclerk" and spec.get("civicclerk_category_id"):
                run(log, "civicclerk.py", "--county", cname, "--api", m["api"],
                    "--category", spec["civicclerk_category_id"], "--body", body, "--since", since)
            elif "agendacenter" in (m.get("platform") or "") and spec.get("agendacenter_category_id"):
                run(log, "agendacenter.py", "--county", cname, "--site", "https://" + m["host"].removeprefix("https://"),
                    "--category", spec["agendacenter_category_id"], "--body", body, "--since", since)

    if "select" in steps:
        run(log, "select_docs.py", "--county", cname, "--out", picks)
    if "fetch" in steps and picks.exists():
        run(log, "fetch_list.py", "--county", cname, "--list", picks, "--workers", "6")
    if "text" in steps:
        run(log, "to_text.py", "--county", cname)
        run(log, "ocr.py", "--county", cname)
    if "index" in steps:
        zc = cfg.get("code", {}).get("zoning_chapter", "")
        run(log, "legislation_index.py", "--county", cname, *(["--zoning-chapter", zc] if zc else []))
        run(log, "digest_prep.py", "--county", cname)
        run(log, "coverage.py", "--county", cname)
        if not os.environ.get("ESL_SKIP_INDEX"):      # refresh_all.sh builds the index once, after every county
            run(log, "build_index.py")
    print(f"== {cname} done. Next: digest agents on ~/.cache/esl/{cname}/digest/*.txt, then "
          f"merge_digests.py, summary agent (02. Tools/Prompts/County Summary Prompt.md), build_comparison.py ==")


if __name__ == "__main__":
    main()
