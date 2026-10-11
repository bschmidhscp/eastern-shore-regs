"""Shared helpers for the Eastern Shore regulatory corpus.

Every downloaded file gets one row in <county>/manifest.csv so we always know
where a document came from, when it was pulled, and whether it has changed.
Run tools with:  ~/.venvs/esl/bin/python -I "02. Tools/<script>.py" ...

Folder layout (see "00. Index/Start Here.md"):
  <County>/Originals/<Kind>/...   files exactly as downloaded
  <County>/Code/Chapter N/...     one markdown file per code section
  <County>/Documents/<Kind>/...   searchable text of PDFs etc.
  <County>/Meeting Minutes/...    minutes text + summaries
  <County>/Data/...               tables as CSV
  <County>/Manifest.csv           one row per downloaded file
"""
import csv
import fcntl
import datetime as dt
import hashlib
import os
import re
import threading
import time
from pathlib import Path

from curl_cffi import requests as _req

CORPUS = Path(__file__).resolve().parent.parent  # .../Docs + Regs
TODAY = dt.date.today().isoformat()
_LOCK = threading.Lock()  # manifest writes from worker threads

MANIFEST_FIELDS = [
    "path",          # relative to CORPUS
    "county",        # slug, or "state"
    "category",      # code | fees | plan | map | minutes | agenda | staff-report | law | other
    "title",
    "source_url",
    "retrieved",     # ISO date
    "effective",     # effective / adopted / meeting date if known
    "sha256",
    "bytes",
    "text_path",     # converted markdown (relative to CORPUS), if any
    "notes",
]


# county argument (any case / slug) -> folder name
COUNTIES = {
    "caroline": "Caroline", "cecil": "Cecil", "dorchester": "Dorchester", "kent": "Kent",
    "queen-annes": "Queen Anne's", "queenannes": "Queen Anne's", "queen anne's": "Queen Anne's",
    "somerset": "Somerset", "talbot": "Talbot", "wicomico": "Wicomico", "worcester": "Worcester",
    "state": "01. Maryland", "maryland": "01. Maryland", "01. maryland": "01. Maryland",
}

# manifest category -> folder name under Originals/ and Documents/
KIND_FOLDER = {
    "code": "Code", "fees": "Fees", "plan": "Plans", "map": "Maps", "minutes": "Meeting Minutes",
    "agenda": "Meeting Minutes", "staff-report": "Meeting Minutes", "law": "Legislation",
    "other": "Other",
}


def county_name(county):
    return COUNTIES.get(county.strip().lower(), county)


def county_dir(county):
    return CORPUS / county_name(county)


def clean_name(s, maxlen=120):
    """Readable, properly-cased file/folder name: keeps spaces and case, drops illegal characters."""
    s = re.sub(r'[\\/:*?"<>|\x00-\x1f]+', " ", s)
    s = re.sub(r"\s+", " ", s).strip(" .")
    return s[:maxlen].rstrip(" .") or "Untitled"


def slug(s, maxlen=80):
    s = re.sub(r"[^A-Za-z0-9]+", "-", s.lower()).strip("-")
    return s[:maxlen].rstrip("-") or "untitled"


def get(url, retries=3, **kw):
    """GET with a real-browser TLS fingerprint (gets past Cloudflare on eCode360 etc.)."""
    last = None
    for i in range(retries):
        try:
            r = _req.get(url, impersonate="chrome", timeout=kw.pop("timeout", 120), **kw)
            if r.status_code == 200:
                return r
            last = RuntimeError(f"HTTP {r.status_code} for {url}")
        except Exception as e:  # network hiccup
            last = e
        time.sleep(2 * (i + 1))
    raise last


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def manifest_path(county):
    return county_dir(county) / "Manifest.csv"


def read_manifest(county):
    p = manifest_path(county)
    if not p.exists():
        return {}
    with open(p, newline="") as f:
        return {row["path"]: row for row in csv.DictReader(f)}


def upsert_manifest(county, rows):
    """Insert or replace rows keyed by path. Writes atomically (Drive-sync safe)."""
    # thread lock + cross-process lock (lock file kept off Drive; flock is unreliable on synced folders)
    with _LOCK, open(f"/tmp/esl-manifest-{slug(county_name(county))}.lock", "w") as lf:
        fcntl.flock(lf, fcntl.LOCK_EX)
        _upsert(county, rows)


def _upsert(county, rows):
    data = read_manifest(county)
    for r in rows:
        full = {k: "" for k in MANIFEST_FIELDS}
        full.update({k: v for k, v in r.items() if k in MANIFEST_FIELDS})
        full["county"] = county_name(full["county"] or county)
        full["retrieved"] = full["retrieved"] or TODAY
        data[full["path"]] = full
    p = manifest_path(county)
    p.parent.mkdir(parents=True, exist_ok=True)
    tmp = p.with_suffix(".csv.tmp")
    with open(tmp, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=MANIFEST_FIELDS)
        w.writeheader()
        for k in sorted(data):
            w.writerow(data[k])
    os.replace(tmp, p)


def download(url, dest, county, category, title="", effective="", notes="", force=False):
    """Download url to dest (absolute or CORPUS-relative) and record it. Returns manifest row."""
    dest = Path(dest)
    if not dest.is_absolute():
        dest = CORPUS / dest
    dest.parent.mkdir(parents=True, exist_ok=True)
    if force or not dest.exists():
        r = get(url)
        tmp = dest.with_name(dest.name + ".part")
        tmp.write_bytes(r.content)
        os.replace(tmp, dest)
    row = dict(
        path=str(dest.relative_to(CORPUS)), county=county, category=category,
        title=title or dest.stem, source_url=url, effective=effective,
        sha256=sha256(dest), bytes=dest.stat().st_size, notes=notes,
    )
    upsert_manifest(county, [row])
    return row


def write_md(path, meta, body):
    """Write a markdown file with YAML-ish front matter."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = ["---"]
    for k, v in meta.items():
        v = str(v).replace("\n", " ").replace('"', "'")
        lines.append(f'{k}: "{v}"')
    lines += ["---", "", body.strip(), ""]
    path.write_text("\n".join(lines))
