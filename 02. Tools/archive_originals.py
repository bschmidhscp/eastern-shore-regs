"""Move original downloads off Google Drive into the private originals archive (Cloudflare R2 bucket esl-originals).
Every text copy, digest, summary and manifest stays on Drive; only <County>/Originals/ moves. Each folder is copied,
checked file by file (size and MD5) and only then removed from Drive. Originals stay one click away, behind the Deal
Board's sign-in:

    https://deals.highsidecapitalpartners.com/originals/<manifest path>
    e.g. https://deals.highsidecapitalpartners.com/originals/Kent/Originals/Code/Unified Development Ordinance.pdf

Fetchers skip archived files (common.have checks the manifest), so a monthly refresh never downloads them again; new
downloads land in Originals/ as before and refresh_all.sh archives them at the end.

    ~/.venvs/esl/bin/python -I "02. Tools/archive_originals.py"                    # every county + 01. Maryland
    ~/.venvs/esl/bin/python -I "02. Tools/archive_originals.py" --county Kent --dry-run
    ~/.venvs/esl/bin/python -I "02. Tools/archive_originals.py" --restore Kent      # bring originals back (re-extract text)

Needs rclone (brew install rclone) and the Cloudflare token in ~/.config/esl/cloudflare_access.token (R2 edit).
"""
import argparse
import hashlib
import os
import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from common import CORPUS  # noqa: E402

ACCOUNT = "c2d241c63ba8d6efcf2acf4f7d1ada63"
TOKEN_ID = "04a72b844dc13605138847486d02cd77"          # the token's id is its R2 access key id
TOKEN = Path.home() / ".config/esl/cloudflare_access.token"
BUCKET = "r2:esl-originals"


def env():
    """rclone's r2 remote: R2 S3 keys come from the Cloudflare API token (secret = SHA-256 of the token)."""
    secret = hashlib.sha256(TOKEN.read_text().strip().encode()).hexdigest()
    return {**os.environ, "RCLONE_CONFIG_R2_TYPE": "s3", "RCLONE_CONFIG_R2_PROVIDER": "Cloudflare",
            "RCLONE_CONFIG_R2_ENDPOINT": f"https://{ACCOUNT}.r2.cloudflarestorage.com", "RCLONE_CONFIG_R2_NO_CHECK_BUCKET": "true",
            "RCLONE_CONFIG_R2_ACCESS_KEY_ID": TOKEN_ID, "RCLONE_CONFIG_R2_SECRET_ACCESS_KEY": secret,
            "PATH": "/opt/homebrew/bin:" + os.environ.get("PATH", "")}


def rclone(*args, check=True):
    r = subprocess.run(["rclone", *map(str, args), "--transfers", "8", "--fast-list"], env=env(), text=True, capture_output=True)
    if check and r.returncode:
        raise SystemExit(f"rclone {args[0]} failed:\n{r.stderr[-2000:]}")
    return r


def folders(county=None):
    return [d for d in sorted(CORPUS.glob("*/Originals")) if d.is_dir() and (not county or d.parent.name == county)]


def archive(src, dry):
    rel = src.relative_to(CORPUS)
    files = [p for p in src.rglob("*") if p.is_file() and not p.name.startswith(".")]
    if not files:
        return 0, 0
    size = sum(p.stat().st_size for p in files)
    print(f"{rel}: {len(files)} files, {size / 1e6:,.0f} MB", flush=True)
    if dry:
        return len(files), size
    rclone("copy", src, f"{BUCKET}/{rel}", "--exclude", ".*")
    r = rclone("check", src, f"{BUCKET}/{rel}", "--one-way", "--exclude", ".*", check=False)
    if r.returncode:                                    # anything missing or different: keep the Drive copy
        raise SystemExit(f"{rel}: check failed, nothing removed:\n{r.stderr[-1500:]}")
    for p in files:
        p.unlink()
    for d in sorted((d for d in src.rglob("*") if d.is_dir()), key=lambda d: -len(d.parts)):
        if not any(d.iterdir()):
            d.rmdir()
    print("  archived and verified; removed from Drive", flush=True)
    return len(files), size


def restore(county):
    for src in [CORPUS / county / "Originals"]:
        rel = src.relative_to(CORPUS)
        rclone("copy", f"{BUCKET}/{rel}", src)
        print(f"restored {rel}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--county")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--restore", metavar="COUNTY")
    a = ap.parse_args()
    if os.environ.get("ESL_NO_ARCHIVE") and not a.restore:     # cloud test runs leave originals where they are
        return print("archive skipped (ESL_NO_ARCHIVE)")
    if not shutil.which("rclone", path=env()["PATH"]):
        raise SystemExit("rclone not found: brew install rclone")
    if a.restore:
        return restore(a.restore)
    n = b = 0
    for src in folders(a.county):
        k, s = archive(src, a.dry_run)
        n, b = n + k, b + s
    print(f"{'would archive' if a.dry_run else 'archived'} {n} files, {b / 1e9:.2f} GB")


if __name__ == "__main__":
    main()
