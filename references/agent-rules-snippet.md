# OpenLotus Agent Rules — one-time paste, every session

Copy the block below into your repo's `CLAUDE.md` **or** `AGENTS.md`, commit it,
and every session in this repository — yours, your teammates', your agents' —
boots with the loop. **Never paste instructions into prompts again.**

## Where the file goes

| Agent | File | Location |
|-------|------|----------|
| Claude Code | `CLAUDE.md` | repo root (all sessions in that repo). Global option: `~/.claude/CLAUDE.md` |
| OpenCode | `AGENTS.md` | repo root (auto-loaded every run) |
| Cursor | `.cursor/rules/openlotus.mdc` | repo root `.cursor/rules/` |
| Both / either | `AGENTS.md` works too — Claude Code also reads it as a fallback | repo root |

> One file is enough. If you use both Claude Code and OpenCode in the same repo,
> put the block in `AGENTS.md` and make `CLAUDE.md` say `@AGENTS.md`.

## The snippet

```markdown
## OpenLotus loop (standing rules)

Shared memory lives in OpenLotus via MCP tools: get_memory, get_reality,
get_drift, record_decision, record_constraint, report_failure, record_lesson,
write_scratchpad, read_scratchpad, manage_tasks, dismiss_drift,
resolve_failure, resolve_risk. The founder sees the same data on the web
dashboard. These rules apply to EVERY action and every prompt, not just
session start.

CLI commands (local, run in your repo):
- npx openlotus pair       one-time: link this repo to a cloud project
- npx openlotus bootstrap  one-time: seed the map from README/PROGRESS/AGENTS
- npx openlotus sync       push a fresh reality snapshot to the dashboard
- npx openlotus status     print latest observed state + drift
- npx openlotus agent      MCP server over stdio (what your harness launches)
- npx openlotus version    print the installed CLI version

1. **Boot**: at the START of any work session or non-trivial prompt, call
   get_memory + get_drift before planning anything. If drift findings exist,
   surface them to the founder first. If the map has no goal yet, set one
   first (propose_changes on progressMap.goal, or confirm it with the
   founder) — a project without a goal is not set up.
2. **Decisions**: whenever a direction choice is made (stack, scope, schema,
   tradeoff), call record_decision immediately — title + why. Do not batch.
3. **Founder notes**: whenever the founder says something worth keeping that
   is not yet a decision, task, or constraint (a stray idea, a preference,
   something to check later), call write_scratchpad immediately. Check
   read_scratchpad before asking the founder something they may already
   have answered.
4. **Tasks**: track real work with manage_tasks — create on starting,
   update status as it moves (queued/running/done/failed/pending), set due
   dates, mark done the moment it is done. Never leave a finished task open.
5. **Reality check**: after completing meaningful work, call get_reality and
   mention surprises (unexpected dirty files, TODO spikes). npx openlotus
   sync pushes the same snapshot to the dashboard.
6. **Close the loop**: when a drift finding is addressed, call dismiss_drift
   so it stops resurfacing. When a recorded failure is fixed, call
   resolve_failure. When a risk is handled, resolve it. Fixed items must
   disappear from the record — never leave solved problems looking open.
7. **PROGRESS.md**: update after each milestone or plan change so the file
   matches the map. If they disagree, the map wins — fix the file.
8. **Failures and constraints**: when an approach fails, call report_failure
   (never retry the same strategy silently). When a boundary is set, call
   record_constraint. Never bury constraints or failures in decision prose.
9. **Stale > silent**: if context is missing, call get_memory again instead
   of guessing. Never invent project state from chat history alone.
```

## What happens after you commit it

Nothing runs by itself when you open the app — the rules load silently.
The effect: the **first thing your agent does when you give it any task** is
check memory and drift, and it logs decisions as it goes. You'll see the tool
calls happen in its transcript. If you want proof it's wired, ask:
*"what does memory say about this project?"*

## Optional enforcement (Claude Code hooks)

Hooks fire even if the model ignores the rules:

```json
{
  "hooks": {
    "SessionStart": [{ "type": "command", "command": "npx openlotus status" }],
    "Stop": [{ "type": "command", "command": "npx openlotus sync" }]
  }
}
```

- `SessionStart` prints drift/status at boot, so stale context is impossible to miss.
- `Stop` syncs an observed snapshot when a session ends, keeping the dashboard honest
  even if the agent skipped step 3.

## Why this works

| Layer | Mechanism | Per-prompt cost |
|-------|-----------|-----------------|
| Tools | MCP server in `mcp.json` | Zero — available in every session |
| Habits | This snippet in `CLAUDE.md`/`AGENTS.md` | Zero — auto-loaded at session start |
| Deep loops | `vibe-to-ship` skill | Only when you want full triage |
| Safety net | Drift engine (`get_drift`, sync findings) | Zero — surfaces forgetting as findings |

Every record OpenLotus stores is timestamped at write time: decisions carry
`createdAt`, evidence carries `createdAt`, milestones carry `createdAt`,
observed snapshots carry `capturedAt` (+ `syncCount`), reviews carry
`lastReviewAt`. The dashboard's weekly summary is built from those timestamps.
