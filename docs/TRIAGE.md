# Example Triage Report

This is what a completed triage looks like when your agent runs Beat 1 (Triage) of the loop and writes the result to `STATE.md`. Copy the structure, not the content — your numbers will (and should) differ.

The rule: **triage is evidence, not vibes.** Every line below traces to a real command from `scripts/triage.sh` or `git`. If a line can't be traced, it doesn't belong in the report.

---

## Example: a mid-build state

```markdown
## Triage — 2026-09-16

**Branch:** `feat/email-verification`
**Dirty files:** 3 (auth-server.ts, email.ts, auth-provider.tsx)
**Last real commit:** 3 days ago
**Session gap:** quiet 3d

### Where the plan stands

| Plan claim | Reality | Verdict |
|---|---|---|
| Email verification flow ships this week | sendVerificationEmail wired, Resend 422 on `from` field unresolved | DRIFTING — one blocker |
| Auth pages redesigned | sign-in/sign-up/reset done, forgot-password pending | ON TRACK |
| Subdomain proxy for docs | not started | PARKED — not this week |

### The one thing that matters

The Resend `from` field 422 is blocking every signup since Tuesday. Nothing else on the
list matters until signup email works — new users literally cannot verify.

### Next bounded task

Fix `RESEND_FROM` env resolution so the `from` field is `OpenLotus <hello@openlotus.io>`.
Done when: a signup sends a real verification email in production. One task. Two hours max.
```

---

## Why this format

- **The table is the point.** Plan-vs-reality side by side is what exposes drift. A paragraph
  can hide "not started"; a table row can't.
- **One blocker, named.** A triage that lists five priorities has none.
- **The bounded task has a done-condition.** "Work on email" is not a task. "A signup sends
  a real email in production" is.
- **Verdicts are honest.** `PARKED` is a healthy verdict. Everything marked `ON TRACK`
  when it's drifting is how projects die quietly.

## Anti-patterns

- Copying last week's triage and changing the date. Your agent should re-run the commands.
- Listing what you did. Triage is about where the plan stands, not a diary.
- Verdicts without evidence. "Almost done" — says who? Which command shows it?
