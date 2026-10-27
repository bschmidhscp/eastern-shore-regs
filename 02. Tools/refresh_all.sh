#!/bin/bash
# Monthly refresh: re-pull every county (and the search index), then record what changed.
# Runs the automated pipeline only (no AI). Afterwards an AI pass reads "00. Index/Change History.md"
# and updates the Project Log / county "Amendments Not Yet in Code" notes (see the scheduled task prompt).
#
# Usage: "02. Tools/refresh_all.sh"         Log: ~/.cache/esl/refresh-<date>.log
set -uo pipefail
CORPUS="$(cd "$(dirname "$0")/.." && pwd)"
cd "$CORPUS"
PY=~/.venvs/esl/bin/python
LOG=~/.cache/esl/refresh-$(date +%Y-%m-%d).log
mkdir -p ~/.cache/esl
echo "== refresh $(date) ==" >> "$LOG"

# counties = every config; 3 at a time; eCode360 rate limits are handled by common.get backoff
ls "02. Tools/County Configs/"*.json | sed 's|.*/||; s|\.json$||' | tr '\n' '\0' |
  xargs -0 -P 3 -n 1 sh -c '"$0" -I "02. Tools/run_county.py" --county "$1" --steps code,inventory,meetings,select,fetch,text,index >> "$2" 2>&1; echo "$1 refreshed" >> "$2"' "$PY" _ "$LOG"

# refresh each county's digest-ready legislation index and the comparison, then commit + record changes
"$PY" -I "02. Tools/build_comparison.py" >> "$LOG" 2>&1
"$PY" -I "02. Tools/build_index.py" >> "$LOG" 2>&1
# move this month's new downloads off Drive to the originals archive (R2; served behind the board's sign-in)
"$PY" -I "02. Tools/archive_originals.py" >> "$LOG" 2>&1
"02. Tools/sync_repo.sh" "Monthly refresh $(date +%Y-%m-%d)" >> "$LOG" 2>&1
"02. Tools/publish_guides.sh" >> "$LOG" 2>&1
echo "== done $(date) ==" >> "$LOG"
tail -5 "$LOG"
