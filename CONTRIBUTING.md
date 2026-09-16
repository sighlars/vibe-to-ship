# Contributing to vibe-to-ship

Thanks for wanting to improve the skill. It's small on purpose — contributions that keep it
small, sharp, and verified are the ones that land.

## Ground rules

1. **The loop is the product.** Changes that add steps, dashboards, or config surface are
   unlikely to land. Changes that make an existing beat faster, clearer, or harder to fake are welcome.
2. **Every script must survive a fresh repo.** Test your change against a repo with zero
   commits, a repo mid-branch with dirty files, and a clean repo. Fresh repos already bit us once (`quiet ?d`).
3. **No network calls.** The scripts run offline, everywhere, always.
4. **ShellCheck clean.** CI runs shellcheck on `scripts/*.sh`. If your change adds a warning, it fails the build.

## How to submit

1. Fork, then create a branch from `main`.
2. Make the change. If it touches a script, run the three-repo test above.
3. Open a pull request with:
   - **What** changed
   - **Why** — which beat it improves, or which failure you hit
   - **How you tested it** — the actual commands, not "tested manually"

PRs that show their test evidence get merged fast. PRs that say "should work" get looked at
eventually.

## Reporting bugs

Open an issue with:
- The exact command you ran and its full output
- What you expected vs. what happened
- Your git version and OS (the scripts lean on POSIX sh — Windows users are on Git Bash)

## Scope notes

- **Agent instructions** (`SKILL.md`): changes welcome, but keep every instruction actionable
  and checkable. "Be thorough" is not an instruction; "run `scripts/verify.sh` and quote the
  output" is.
- **New beats**: probably not. Five beats is the whole idea. Propose it in an issue first.
- **Other agent platforms**: the skill is agent-agnostic by design (plain markdown + sh).
  Port notes are welcome as docs, not as code forks.

## License

By contributing, you agree your contributions are licensed under the repository's license.
