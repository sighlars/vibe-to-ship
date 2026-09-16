# vibe-to-ship

<p align="center">
  <img src="assets/demo-loop.gif" alt="The vibe-to-ship 5-beat loop running in a terminal: triage, act, verify, learn" width="100%">
</p>

**Your agent ships. This skill makes sure it ships the truth.**

AI coding agents are relentless builders and unreliable narrators. They declare "authentication is complete" while 14 files sit uncommitted, 6 tests are missing, and half the planned flows don't exist. The gap between what your agent *says* and what your repository *shows* is where projects die quietly.

vibe-to-ship is a drop-in skill that closes that gap. It installs a 5-beat operating loop — **boot, triage, act, verify, learn** — into Claude Code, OpenCode, Cursor, or any MCP-capable agent, backed by three shell scripts that check reality instead of trusting narration:

```bash
# Claude Code
git clone https://github.com/CyberTycoon/vibe-to-ship.git ~/.claude/skills/vibe-to-ship

# opencode
git clone https://github.com/CyberTycoon/vibe-to-ship.git .opencode/skills/vibe-to-ship
```

The repo **is** the skill (`SKILL.md` at the root) — cloning it into your agent's skills directory is the whole install. Updates are one command: `git -C ~/.claude/skills/vibe-to-ship pull`. Then, from inside **your project**, run:

```bash
bash ~/.claude/skills/vibe-to-ship/scripts/install.sh   # writes the rules block to YOUR project (idempotent)
bash ~/.claude/skills/vibe-to-ship/scripts/loop.sh boot # readiness check
```

<p align="center">
  <img src="assets/demo-install.gif" alt="Installing vibe-to-ship: clone, install.sh, doctor.sh returning READY" width="100%">
</p>

No account. No API key. No cloud. The skill runs entirely in your repository — install takes under three minutes and every beat is a plain POSIX shell script you can read before you run it.

---

## Why developers keep it installed

**1. It converts agent confidence into evidence.** Every "done" claim must survive `verify.sh`: build passes, tests pass, the diff stays inside the declared scope, and no new TODO debt was smuggled in. The verdict is computed from your repository, not from your agent's self-assessment.

**2. It makes drift visible the moment it starts.** Triage compares your plan against observable reality — branch state, dirty files, TODO density, quiet days — and prints **High / Watch / Noise** findings. Nothing gets to "surprised you at the end of the sprint."

<p align="center">
  <img src="assets/demo-drift.gif" alt="Drift detection: the agent claims authentication is complete, get_reality shows two of three planned flows missing" width="100%">
</p>

**3. It gives every session a memory.** The `learn` beat appends a structured summary — branch, decisions, next bounded task — to `MEMORY.md`. Your next session starts from written state, not from a context window that forgot everything.

**4. It is honest about scope.** One task per loop, a declared file scope, an explicit stop condition. When the work needs a second deliverable, that is a second loop. This is the discipline that keeps agent speed from becoming agent chaos.

## The 5-beat loop

| Beat | Command | What it does | Fails when |
|---|---|---|---|
Run every beat from inside **your project**, invoking the script by its installed path (shown here as `VTS=$HOME/.claude/skills/vibe-to-ship`):

| Beat | Command | What it checks | Fails when |
|---|---|---|---|
| **Boot** | `bash "$VTS/scripts/loop.sh" boot` | Environment readiness: git, node, MCP config, pairing, standing rules | a High finding blocks the run |
| **Triage** | `bash "$VTS/scripts/loop.sh" triage` | Reality check before planning; plan-vs-repo reconciliation | never (findings are data) — add `--fail-on-high` for a CI gate |
| **Act** | `bash "$VTS/scripts/loop.sh" act` | Prints the bounded-task contract: TASK / SCOPE / DONE / STOP | n/a — it is the handoff to real work |
| **Verify** | `bash "$VTS/scripts/loop.sh" verify --scope src/x.ts` | Build, tests, scope violations, new drift markers | build or tests fail, or the diff escapes scope |
| **Learn** | `bash "$VTS/scripts/loop.sh" learn` | Session summary appended to MEMORY.md | never |

The loop is deliberately boring. Boring loops survive contact with real projects.

## What gets installed

```
vibe-to-ship/
├── scripts/
│   ├── loop.sh        # single dispatcher for the 5 beats
│   ├── boot.sh → doctor.sh   # readiness check (High/Watch/Noise)
│   ├── triage.sh      # reality check, --json for CI, --fail-on-high gate
│   ├── verify.sh      # post-act verification: build, tests, scope, drift
│   └── install.sh     # idempotent setup of rules + MCP config hints
├── references/        # agent-facing docs: the engine, the loop, OpenLotus MCP
├── patterns/          # named solutions to recurring agent-coordination problems
└── examples/          # worked triage reports and session transcripts
```

`install.sh` appends a standing-rules block to `AGENTS.md` (or `.cursor/rules/openlotus.mdc`) so every future session inherits the loop. It never overwrites existing config, and re-running it is a no-op.

vibe-to-ship is plain shell + markdown, so it pairs with every environment your agent runs in — **Claude Code, OpenCode, Cursor, VS Code, Neovim** — and anything else that reads `AGENTS.md` or speaks MCP. No plugins, no per-editor glue.

## Optional: persistent memory with OpenLotus MCP

The loop works fully offline. Pair it with [OpenLotus](https://www.openlotus.io) when you want the loop's memory to become **persistent, cross-session, and agent-queryable**:

```bash
npx openlotus pair          # links this repo to your OpenLotus project
```

Your agent then gets five MCP tools — `get_memory`, `get_reality`, `get_drift`, `record_decision`, `create_project` — so the next session starts by reading what actually happened last time, not by guessing. File *shapes* and signals only; your code never leaves your machine.

## CI integration

Both reality scripts are CI-first citizens:

```yaml
- name: Triage (fail on High findings)
  run: ./scripts/triage.sh --fail-on-high

- name: Verify (post-agent reality gate)
  run: ./scripts/verify.sh --scope "src/" --build-cmd "pnpm build" --test-cmd "pnpm test"
```

`triage.sh --json` emits a single machine-readable line for dashboards and agents.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). The short version: POSIX `sh`, `shellcheck` clean, and every PR explains why the change matters. The scripts in `scripts/` are the product — treat them like a parachutist treats a backpack.

## License

MIT
