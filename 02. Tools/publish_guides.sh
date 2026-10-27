#!/bin/bash
# Publish the two guides as Word files at the top of the shared drive, where any person or AI
# (including ones that only read Drive through a connector, which can't read .md) sees them first.
#   00. Index/Start Here.md   -> <shared drive>/00. Start Here.docx
#   00. Index/Project Log.md  -> <shared drive>/01. Project Log.docx
#   00. Index/Change History.md -> <shared drive>/02. Change History.docx
# Files are overwritten in place so their Drive links never change.
set -euo pipefail
CORPUS="$(cd "$(dirname "$0")/.." && pwd)"
ROOT="$(dirname "$CORPUS")"
TMP="$(mktemp -d)"

publish() {
  pandoc "$CORPUS/00. Index/$1" -f gfm -t docx -o "$TMP/out.docx"
  if [ -f "$ROOT/$2" ]; then
    cat "$TMP/out.docx" > "$ROOT/$2"   # rewrite contents, keep the same Drive file (and link)
  else
    cp "$TMP/out.docx" "$ROOT/$2"
  fi
  echo "Published $2"
}

publish "Start Here.md" "00. Start Here.docx"
publish "Project Log.md" "01. Project Log.docx"
[ -f "$CORPUS/00. Index/Change History.md" ] && publish "Change History.md" "02. Change History.docx"
[ -f "$CORPUS/00. Index/Operations Manual.md" ] && publish "Operations Manual.md" "03. Operations Manual.docx"
rm -rf "$TMP"
