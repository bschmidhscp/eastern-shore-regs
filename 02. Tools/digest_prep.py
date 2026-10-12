"""Prepare digest batches for AI agents: pre-filter long minutes to land-use passages, then batch.

Council/Commissioner minutes are mostly not about land use. This keeps only paragraphs that mention
land-use terms (plus one paragraph of context each side), so digest agents read ~half as much.
Planning Commission minutes, appeals decisions and pre-app agendas are passed through whole.

Work files go OFF Drive in ~/.cache/esl/<County>/digest/ :
  filtered/<file>.md     filtered copies (for council minutes)
  <group>-<n>.txt        batch lists (one absolute path per line) for digest agents
  parts/                 where agents write their CSVs; merge with merge_digests.py --parts <that dir>

Usage: python -I "02. Tools/digest_prep.py" --county Kent [--max-kb 230]
"""
import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from common import county_dir, county_name  # noqa: E402

LAND_USE = re.compile(
    r"subdivi|zoning|rezon|variance|special exception|critical area|sewer|water and sewer|wastewater|"
    r"comprehensive (water|plan)|\bCWSP\b|growth allocation|annex|site plan|plat\b|text amendment|"
    r"\bbill\b|ordinance|resolution|impact fee|excise|septic|density|development rights|"
    r"planning commission|land use|map amendment|PUD|planned unit|moratorium|preservation|easement|"
    r"service area|\bTDR\b|forest conservation|buffer|development", re.I)

MAX_DOC = 120_000  # characters per document sent to a digest agent

# group key -> (folder under Meeting Minutes, filter?)
GROUPS = {
    "pc": ("Planning Commission", False),
    "boa": ("Board of Appeals Decisions", False),
    "boam": ("Board of Appeals", False),
    "preapp": ("Pre-Application Meetings", False),
    "tac": ("Technical Advisory Committee", False),
    "council": ("County Council", True),
    "commissioners": ("County Commissioners", True),
}


def filter_text(text):
    head, _, body = text.partition("\n---\n")
    paras = [p for p in re.split(r"\n\s*\n", body) if p.strip()]
    keep = set()
    for i, p in enumerate(paras):
        if LAND_USE.search(p) or p.lstrip().startswith("<!-- page"):
            keep.update({i - 1, i, i + 1} if LAND_USE.search(p) else {i})
    out = [paras[i] for i in sorted(k for k in keep if 0 <= k < len(paras))]
    return head + "\n---\n" + "\n\n".join(out), len(body), sum(len(p) for p in out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--county", required=True)
    ap.add_argument("--max-kb", type=int, default=230)
    a = ap.parse_args()
    cname = county_name(a.county)
    mm = county_dir(cname) / "Meeting Minutes"
    work = Path.home() / ".cache" / "esl" / cname / "digest"
    (work / "parts").mkdir(parents=True, exist_ok=True)
    (work / "filtered").mkdir(exist_ok=True)
    for old in work.glob("*.txt"):
        old.unlink()
    total_in = total_out = 0
    for g, (folder, filt) in GROUPS.items():
        files = sorted((mm / folder).glob("*.md"))
        # skip meeting packets, and agendas for dates that also have minutes
        dated_minutes = {re.match(r"\d{4}-\d\d-\d\d", f.name)[0] for f in files
                         if "minute" in f.name.lower() and re.match(r"\d{4}-\d\d-\d\d", f.name)}
        files = [f for f in files if "packet" not in f.name.lower() and not (
            "agenda" in f.name.lower() and re.match(r"\d{4}-\d\d-\d\d", f.name)
            and re.match(r"\d{4}-\d\d-\d\d", f.name)[0] in dated_minutes)]
        if not files:
            continue
        use = []
        for f in files:
            if f.stat().st_size > MAX_DOC:  # cap very long documents (first part holds the decisions)
                dest = work / "filtered" / f.name
                dest.write_text(f.read_text(errors="replace")[:MAX_DOC] + "\n\n[... truncated for digest ...]")
                f = dest
            if filt:
                t, n_in, n_out = filter_text(Path(f).read_text(errors="replace"))
                total_in += n_in
                total_out += n_out
                dest = work / "filtered" / f.name
                dest.write_text(t)
                use.append(dest)
            else:
                use.append(f)
        batch, kb, n = [], 0, 0
        for f in use + [None]:
            k = f.stat().st_size // 1024 if f else 0
            if batch and (f is None or kb + k > a.max_kb):
                n += 1
                (work / f"{g}-{n}.txt").write_text("\n".join(str(x.resolve()) for x in batch))
                print(f"{g}-{n}: {len(batch)} files, {kb} KB")
                batch, kb = [], 0
            if f:
                batch.append(f)
                kb += k
    if total_in:
        print(f"council/commissioner minutes filtered: {total_in//1024} KB -> {total_out//1024} KB "
              f"({100 - 100*total_out//max(total_in,1)}% less to read)")
    print(f"batch lists in {work}")


if __name__ == "__main__":
    main()
