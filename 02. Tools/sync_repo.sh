#!/bin/bash
# Commit and push the text layer of the corpus to GitHub, and record what changed in
# "00. Index/Change History.md" so people (and AIs) who only use the Drive see the same history.
# The git history lives OFF Google Drive (~/git/eastern-shore-regs.git) because Drive sync can
# corrupt .git folders; the work tree is the Drive folder itself. Ignore rules: $GIT_DIR/info/exclude.
#
# Usage: "02. Tools/sync_repo.sh" "commit message"     (no message = "Refresh <date>")
set -euo pipefail
export GIT_DIR="$HOME/git/eastern-shore-regs.git"
export GIT_WORK_TREE="$(cd "$(dirname "$0")/.." && pwd)"
cd "$GIT_WORK_TREE"
msg="${1:-Refresh $(date +%Y-%m-%d)}"
HIST="00. Index/Change History.md"
# lines that change on every refresh and aren't real content changes
NOISE=(-I '^retrieved: ' -I '^current_through: ' -I 'retrieved [0-9-]+\)')

# Line up with GitHub first: the cloud refresh and this Mac both push the mirror. Drive is the source of truth, so the
# commit is simply "Drive as it is now" on top of whatever GitHub has (a soft reset keeps the working tree as is).
if [ -z "${ESL_NO_PUSH:-}" ] && git fetch -q origin main 2>/dev/null; then
  git reset -q --soft FETCH_HEAD
fi
git add -A
if git diff --cached --quiet; then
  echo "No changes."
  exit 0
fi

# Substantive changes to regulation text (code sections, converted documents, tables)
changed=$(git diff --cached --name-only --diff-filter=M "${NOISE[@]}" -- '*/Code/*' '*/Documents/*' '*/Data/*' '*/Meeting Minutes/*' '01. Maryland/*' | grep -v '00. Contents.md$' || true)
added=$(git diff --cached --name-only --diff-filter=A -- '*/Code/*' '*/Documents/*' '*/Meeting Minutes/*' | wc -l | tr -d ' ')

{
  echo "## $(date +%Y-%m-%d) — $msg"
  echo
  if [ "${added}" != "0" ]; then echo "- New text files: ${added}"; fi
  if [ -n "$changed" ] && git rev-parse -q --verify HEAD >/dev/null; then
    echo "- Files whose content changed: $(echo "$changed" | wc -l | tr -d ' ')"
    echo
    echo "$changed" | while read -r f; do
      [ -n "$f" ] || continue
      [ "$(git diff --cached --name-status -- "$f" | cut -f1)" = "M" ] || continue
      echo "### $f"
      echo '```diff'
      git diff --cached -U1 "${NOISE[@]}" -- "$f" | grep -E '^[-+][^-+]' | head -60 || true
      echo '```'
    done
  fi
  echo
} > /tmp/esl-change-entry.md

# newest entry first, below the file header
if [ -f "$HIST" ]; then
  { sed -n '1,4p' "$HIST"; cat /tmp/esl-change-entry.md; sed '1,4d' "$HIST"; } > /tmp/esl-hist.md
else
  { echo "# Change History"; echo
    echo "*Generated on each sync. Shows which regulation text changed and the exact wording differences (\`-\` removed, \`+\` added). Narrative context is in the Project Log.*"; echo
    cat /tmp/esl-change-entry.md; } > /tmp/esl-hist.md
fi
cat /tmp/esl-hist.md > "$HIST"
git add "$HIST"

git diff --cached --stat | tail -1
git commit -q -m "$msg" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
if [ -n "${ESL_NO_PUSH:-}" ]; then     # cloud run without a key for the GitHub mirror: history is local only
  echo "Committed locally (not pushed): $msg"
else
  git push -q origin HEAD:main
  echo "Pushed: $msg"
fi
