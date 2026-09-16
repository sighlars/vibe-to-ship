# Quickstart — 5 minutes to your first triage

> **Stop prompting. Design the graph.**

## 1. Install the skill (60s)

The repo **is** the skill — clone it straight into your agent's skills directory.

**Claude Code:**
```bash
git clone https://github.com/sighlars/vibe-to-ship.git ~/.claude/skills/vibe-to-ship
```

**opencode:**
```bash
git clone https://github.com/sighlars/vibe-to-ship.git .opencode/skills/vibe-to-ship
```

Updates are one command: `git -C ~/.claude/skills/vibe-to-ship pull`.

## 2. Run triage (report-only, safe)

In Claude Code:
```
/vibe-to-ship triage
```

In opencode:
```bash
opencode run "Run vibe-to-ship triage"
```

Or just tell any agent: **“Run vibe-to-ship triage on this repo”**

You'll get a `High / Watch / Noise` list — no files changed.

## 3. Graph engineering in 60 seconds

- **Bounded nodes:** one agent, one task, defined in/out schemas (no free-text walls)
- **Fake-Edge Test:** B only waits for A if B *actually* reads A's output — otherwise they run in parallel
- **Diamond:** Fan-out (worktrees) → Reduce (dedupe, zero tokens) → Verify (fresh-context skeptics) → Synthesize

That's it. The skill handles the rest.

## 4. Optional: pair with OpenLotus for memory

```bash
npx openlotus pair
```

Or tell your agent **“set up OpenLotus”** — it writes `mcp.json` + `.openlotus/config.json` + `AGENTS.md` stub.

See [`references/openlotus-engine.md`](../references/openlotus-engine.md).
