# Operations Manual

*How the Eastern Shore Land system runs, what to do when something breaks, and where every account and key lives.
For the project itself see Start Here; for what happened when, the Project Log. Secrets are never written here.*

## What runs when

| When | What | Where it runs | You hear about it |
|---|---|---|---|
| 1st of the month, ~6 AM ET | **Regs refresh**: re-pulls county codes, minutes, legislation and fees; new originals go to the archive; changed text back to Drive; Change History | GitHub Actions, "Regs refresh" (scheduled once the variable `ESL_CLOUD_REGS` is `on`; until then the Mac's scheduled task) | GitHub issue "Regs refresh <date>" + Project Log entry |
| 2nd of the month, ~6 AM ET | **Deal Board refresh**: re-downloads parcel and sales data, refits models, prices every parcel, deploys the board, writes reports to Drive | GitHub Actions, "Monthly refresh" (scheduled once `ESL_CLOUD_RUN` is `on`) | GitHub issue "Monthly refresh <date>" + Project Log entry + the board's **Model → System status** panel |
| Mondays, ~7 AM ET | **Site health check**: from outside with no sign-in, confirms the board, its data and originals ask for sign-in, icons load, and the guest address refuses everything without a pass | GitHub Actions, "Site health check" | Only on failure: GitHub issue "Site health check failed" |
| Any time | Any of them by hand | github.com/bschmidhscp/eastern-shore-screener → **Actions** → pick the workflow → **Run workflow** | Same |

A full Deal Board run takes about an hour; the regs refresh 1–3 hours. GitHub emails repository watchers when an issue
is opened, so both partners should **Watch** the screener repo (top right of the repo page → Watch → All activity).

## Where things live

| What | Where |
|---|---|
| Deal Board | https://deals.highsidecapitalpartners.com (Cloudflare Pages behind Cloudflare Access) |
| Deal tracker, notes, quotes | The site's database (Cloudflare D1); each run backs it up to R2 and writes `Screener/Deal Tracker.csv` |
| Reports, deal lists, digests, summaries | This shared drive (`Screener/`, `Docs + Regs/`) |
| Original downloads (PDFs, web pages) | Cloudflare R2 bucket `esl-originals`; open `https://deals.highsidecapitalpartners.com/originals/<path from Manifest.csv>` |
| Data cache between runs, archived old deal lists, tracker backups | Cloudflare R2 bucket `esl-screener` |
| Code | GitHub `bschmidhscp/eastern-shore-screener` (screener, board, both workflows); `bschmidhscp/eastern-shore-regs` mirrors the regs text |
| Domain | Registered at Squarespace Domains; DNS runs on Cloudflare (website on Squarespace, email on Google Workspace) |

## When something fails

1. Open the GitHub issue for the run; it links to the run log.
2. Common causes:
   - **A county or state site was down**: the run kept last month's copy and says so ("kept the previous copy";
     the System status panel shows it as stale). Nothing to do; next month refreshes it.
   - **"BOARD WAS PUBLIC"**: the run found the board served without sign-in and put the holding page up. Check
     Cloudflare → Zero Trust → Access → Applications → Deal Board, then redeploy (step 3).
   - **Drive or R2 errors**: a key may have expired or been removed; see Keys below.
   - **"publish plan not ready"**: a model check failed (see `Screener/00. Summary.md`); the board was not deployed.
3. Re-run: Actions → the workflow → Run workflow. Untick "deploy"/"push" for a dry run that changes nothing.
4. Or ask Claude in a session on this drive: "the monthly refresh failed, here's the issue link".

## Common tasks

- **Share the board with someone for 2 hours**: on the board, tap **Share** (top right; partners only), pick the
  contact in Messages. The link opens a read-only board at `guest.highsidecapitalpartners.com` on the first phone or
  computer that opens it (another device can take it over only in the first 5 minutes, e.g. Messages → Safari). Guests
  never see the tracker, notes, quotes, max bid, the owner's expectation or assessment, offer credibility, seller
  signals, or High Side's share (GP returns, promote, waterfall terms); the build refuses to publish if a new column
  looks like that kind of data (`screener/site.py`, GUEST_DROP).
  **Pipeline → Guest links** shows each link: opened or not, on what device, roughly where, how many views, with
  **Revoke** and **Turn off all**. Emergency off for every guest link: set `GUEST_LINKS_OFF = "1"` in
  `site/wrangler.toml` and redeploy (or ask Claude).
- **Add or remove someone's sign-in**: Cloudflare dashboard → Zero Trust → Access → Applications → Deal Board →
  Policies → Partners → edit the emails. (Or ask Claude; it keeps a token that can do this.)
- **Open an original document**: take its path from the county's `Manifest.csv` and open
  `https://deals.highsidecapitalpartners.com/originals/<path>`. Bring a county's originals back to Drive:
  `~/.venvs/esl/bin/python -I "Docs + Regs/02. Tools/archive_originals.py" --restore <County>`.
- **Propose a change (either partner's AI)**: a pull request on the screener repo. It's merged only when the tests
  pass; the next run uses it.
- **Republish the board without a full run**: `python -m screener.site` from a Mac with the repo, or Actions →
  Monthly refresh → Run workflow with "re-download data" unticked.

## Accounts

| Account | Used for | Owner |
|---|---|---|
| Google Workspace (highsidecapitalpartners.com) | Email, this shared drive | Brian (admin) |
| Squarespace Domains | Domain registration | Brian |
| Cloudflare (account "Brian@highsidecapitalpartners.com's Account"; sign-in page branded High Side Capital Partners) | DNS, the board site, its database, R2 storage, sign-in (Access) | Brian; add Ben as a member |
| GitHub (`bschmidhscp`) | Code, both workflows, run reports | Brian; Ben as collaborator |
| Google Cloud project `eastern-shore-deal-board` | The robot user `deal-board-runner` that reads and writes this drive for the workflows | Brian |
| RentCast | Property listings (40 requests/month cap in code) | Brian |

## Keys (what they can do, where they're stored, how to replace them)

| Key | Can do | Stored in | Replace by |
|---|---|---|---|
| Cloudflare API token "Deal Board Access" | Edit Access, DNS, Pages, D1, R2 (R2 storage keys are derived from it) | GitHub secret `CLOUDFLARE_API_TOKEN`; Brian's Mac `~/.config/esl/cloudflare_access.token` | Cloudflare → My Profile → API Tokens → Roll; update both places. If it's a new token, also its id in GitHub variable `CLOUDFLARE_API_TOKEN_ID` |
| Google service account key (`deal-board-runner`) | Read/write this shared drive only | GitHub secret `GOOGLE_SERVICE_ACCOUNT_JSON` | Cloud console → Service accounts → Keys → add a new JSON key, paste it into the secret, delete the old key |
| RentCast API key | Listing searches | GitHub secret `RENTCAST_API_KEY`; Mac `~/.config/esl/rentcast.key` | RentCast dashboard; update both |
| Wrangler login (Mac only) | Deploying the site from the Mac | Mac `~/Library/Preferences/.wrangler/` | `npx wrangler login` in `site/` |
| *Pending:* Claude token | Lets the regs refresh write its AI review | GitHub secret `CLAUDE_CODE_OAUTH_TOKEN` | `claude setup-token` on a computer, paste into the secret |
| Regs deploy key | Lets the regs refresh push the GitHub mirror (that repo only) | GitHub secret `REGS_DEPLOY_KEY` + the regs repo's Deploy keys | Settings → Deploy keys on `eastern-shore-regs`: delete, then ask Claude for a new one |
| Guest-link sealing key | Seals guest passes so they can't be forged | Cloudflare Pages secret `GUEST_SECRET` | `npx wrangler pages secret put GUEST_SECRET` in `site/` with a new random value (ends every live guest link) |

## Costs

All free tiers at our size: Cloudflare (Pages, D1, Access for up to 50 people; R2 ~10.5 GB ≈ 1–2¢/month above the
10 GB free tier), GitHub Actions (2,000 free minutes/month on private repos; the two monthly runs use ~4 hours),
Google Cloud (service account and Drive API are free). RentCast is the only paid data source.
