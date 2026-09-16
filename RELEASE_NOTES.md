# vibe-to-ship v1.0.0 — Graph Engineering for AI Agents

> Your agent doesn't need more prompts. It needs a graph.

First stable release. A single drop-in skill that turns any coding agent —
Claude Code, opencode, Codex, Cursor — into a disciplined, parallel,
self-verifying builder. Works standalone; supercharged with OpenLotus memory.

## What's inside

- **6 beats, 5 principles** — nodes with bounded contracts, the Fake-Edge Test,
  the Diamond Pattern (fan out → reduce → verify → synthesize), fresh-context
  verifiers, and tree memory that lives outside the model.
- **6 MCP tools** (`get_reality`, `get_drift`, `get_memory`, `create_project`,
  `switch_project`, `record_decision`) — shared ProgressMap your whole team sees.
- **Agent-created projects** — `create_project` + `switch_project` let the agent
  spin up a new cloud project (same data as the web `/new-project` flow) and
  point the repo at it, no browser round-trip.
- **3-attempt cap, human-gated shipping** — bounded, never brittle. No auto-push,
  no silent fourth attempts.
- **POSIX shell helpers** — `scripts/install.sh`, `scripts/doctor.sh`,
  `scripts/triage.sh` (`--json` for CI). Read-only except install, which never
  overwrites your `mcp.json`.
- **Safety denylist baked in** — `.env`, `auth/`, `payments/`, `secrets/`,
  `credentials/`, `migrations/` are off-limits without explicit approval.

## Install

```bash
cp -r vibe-to-ship ~/.claude/skills/      # Claude Code
cp -r vibe-to-ship .opencode/skills/      # opencode
npx skills add https://github.com/sighlars/vibe-to-ship  # any agent
```

Then: `"Run vibe-to-ship triage on this repo"` — you get High / Watch / Noise
and a plan you can trust. No files change until you say go.

## Tags

`graph-engineering` `ai-agents` `claude-code` `opencode` `mcp`
`agent-loop` `developer-productivity` `open-source` `vibe-coding` `verification`
