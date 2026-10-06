---
name: vibe-to-ship
description: >
  Use when the user wants to ship a vibe-coded repo, rescue a codebase, set up
  OpenLotus (pair a project, connect the MCP server, add agent rules), or design
  how a fleet of agent jobs gets done. Applies graph engineering and loop engineering:
  eliminates fake edges, enforces node contracts, runs the diamond pattern with
  fresh-context verifiers, and anchors state against the OpenLotus interactive memory map via MCP.
user_invocable: true
---

# vibe-to-ship

Graph engineering and loop engineering for founders and engineers: design how a hundred jobs get done instead of doing one job at a time.

This skill is self-contained. Everything you need is in this file plus `references/`.
You do **not** need OpenLotus to use it — pairing adds shared memory, drift
checks, and a live progress map, but every beat below also has a local-only
fallback. Prefer the paired path when available; never block on it.

---

## 0. When to invoke (and when not to)

**Invoke when the user says (or means) any of these:**

- "Run vibe-to-ship triage", "triage this repo", "what should we do next"
- "Set up OpenLotus", "pair this project", "connect the MCP server"
- "Ship this feature", "fix this properly", "rescue this codebase"
- "Run these tasks in parallel", "why did this break", "verify before we merge"
- A vague build request spanning more than ~3 files ("build me an app", "add auth")

**Do NOT invoke for:**

- Single-file, single-question tasks ("what does this function do", "rename X")
- Pure explanations with no action requested
- Anything the user explicitly says to do quickly / without process — respect that,
  do the small thing, and mention the skill exists for bigger work

**How to announce yourself:** one line, then work. Example:
`Running vibe-to-ship triage — mapping the graph before touching code.`
Never dump this whole file into chat. Never explain the methodology up front;
demonstrate it through action and debrief in one line at the end (Beat 5).

---

## 1. Core Principles

These five rules override convenience. When in doubt, the principle wins.

1. **Nodes & Node Contracts**: A node is 1 agent doing 1 task. Every node MUST
   have a bounded contract before it runs — defined input schema, defined output
   schema, done-criteria. Output is structured data, never free-text walls.
   A node without a contract is not a node; it is a hope. Do not run hopes.

2. **The Fake-Edge Test**: Step B only waits for Step A if B *actually* consumes
   A's output. "Feels related" is not consumption. If no data passes along the
   edge, cut the dependency and run A and B in parallel. Apply this test to
   every arrow in every plan, including plans the user hands you.

3. **The Diamond Pattern**: Fan out (parallel workers) → Reduce (deterministic
   code deduplication — zero LLM tokens, use scripts not models) → Verify
   (fresh-context skeptics) → Synthesize (one final report). Never skip Reduce
   (you'll ship duplicates) and never skip Verify (you'll ship confident lies).

4. **Fresh-Context Verifier Rule**: A worker and its verifier MUST NEVER share a
   context window. Shared context = an agent nodding along to itself in a
   different font. In practice: spawn the verifier as a new agent invocation
   with only the output artifact + the contract, never the worker's transcript.

5. **Interactive Memory & Anchors**: AI chat context gets lost and siloed.
   OpenLotus replaces invisible chat context with a **tree-like interactive
   memory UI** (plans, decisions, actions, changes, state) accessed via MCP.
   Without OpenLotus paired, use a local `PROGRESS.md` in the repo root with
   the same shape (see §2). Either way: memory lives outside the model.

---

## 2. The Interactive Progress Map (Tree Memory)

OpenLotus keeps all project context in a structured tree-like memory UI,
eliminating AI context loss and drift. Without OpenLotus, keep the same shape
in `PROGRESS.md` so a later pairing imports cleanly.

```markdown
# Progress Graph (Tree Memory)

## Goal
<one sentence destination — the thing that, when true, means we're done>

## Active Nodes (Next Actions)
- [ ] node_id: <task name> | in: { schema } | out: { schema } | status: pending|active|done

## Tree Branches
- 📂 Plans (declared roadmap & specs)
- 📂 Decisions (immutable recorded choices via record_decision)
- 📂 Actions & Changes (parallel worker output)
- 📂 State & Context (observed reality via MCP get_reality / get_drift)
```

**Node contract template** (copy per node, fill every field — no blanks):

```markdown
### node: <short-id>
- task: <one sentence, verb first>
- in: { <exact inputs with types> }
- out: { <exact outputs with types> }
- done-when: <observable check — a test, a file existing, a command exit code>
- attempts: 0/3
```

**Worked example** (fixing a broken login form):

```markdown
### node: auth-form-validation
- task: Add client-side validation to the signup email field
- in: { file: "app/sign-up/page.tsx", rule: "RFC-5322-ish email regex" }
- out: { file: "app/sign-up/page.tsx", tests: "signup.test.tsx passes" }
- done-when: `pnpm test signup` exits 0
- attempts: 0/3
```

**Anti-patterns to reject on sight:**

- `out: { summary: "description of what was done" }` — free-text wall, untestable
- `done-when: looks good` — not observable
- A node whose `in` references "the above conversation" — that is shared context leaking in

---

## 3. The 6 Beats of the Loop

Every session executes these beats as graph operations, in order. Do not skip
ahead: each beat's output is the next beat's input.

### Beat 0: Setup (auto, if not already paired)

**When:** at session start, before anything else, every time — it takes seconds.
**Goal:** guarantee the three persistence files exist so nothing learned today is lost.

Check for setup, in this order:

1. **Pairing**: `.openlotus/config.json` exists with `projectId`?
2. **MCP server**: `mcp.json` (or `claude_desktop_config.json` / `.cursor/mcp.json`) launches `npx openlotus agent` (a local-checkout absolute path to `cli/mcp.mjs` also works)?
3. **Rules block**: `AGENTS.md` (and `CLAUDE.md` → `@AGENTS.md` stub for Claude Code) contains the standing-rules block from `references/agent-rules-snippet.md`?
4. **Map seeded**: `npx openlotus bootstrap` has run at least once (or `bootstrap_state` via MCP)?

**If any piece is missing, do it now — don't ask the user to do it by hand:**

1. Run `npx openlotus pair` (no flags). It opens the browser to `/pair`.
   - User logs in — or creates an account if they don't have one — then picks an
   existing project or creates a new one. The CLI writes the pairing file.
   - **No project yet?** The agent can create one itself over MCP once paired
   with any project: `create_project` (name required; stage, description, url,
   connectedTools optional) → `switch_project` with the returned projectId →
   `get_memory` to confirm the new map loads. Same data as the web
   `/new-project` flow, no browser round-trip.
   - **Failure mode:** browser doesn't open (headless/SSH) → print the URL and
     ask the user to open it manually, then wait for the pairing file. Never proceed unpaired without saying so.
   - **Failure mode:** user has no OpenLotus account and declines → continue in
     local-only mode (`PROGRESS.md` as the tree) and say so in one line.
2. Write `mcp.json` that launches `npx openlotus agent` (the MCP server; a
   local-checkout absolute path to `cli/mcp.mjs` also works — if you use the
   path, verify the file exists first with `ls`).
3. Append the standing-rules block to `AGENTS.md` (create the file if missing);
   for Claude Code repos also ensure `CLAUDE.md` contains the `@AGENTS.md` stub.
4. Prefer the skill's helper: run `install.sh` from the installed skill
   directory — it writes to your CURRENT directory (the user's project),
   never into the skill itself:
   `bash ~/.claude/skills/vibe-to-ship/scripts/install.sh`
   (or `.opencode/skills/vibe-to-ship/scripts/install.sh`). It is
   idempotent: skips what exists, never duplicates blocks.
5. Seed the map once with `npx openlotus bootstrap` (or the `bootstrap_state`
   MCP tool) so the ProgressMap starts from the repo's own README/PROGRESS/
   AGENTS instead of empty. Ongoing reality pushes: `npx openlotus sync`.
   `npx openlotus status` prints the latest drift without a new snapshot.

**Verify setup worked:** run the boot doctor from the skill path, again with
the project as your working directory:
`bash ~/.claude/skills/vibe-to-ship/scripts/loop.sh boot` (wraps `doctor.sh`;
or manually: `node --check` the mcp path exists, `JSON.parse` the mcp.json,
confirm the rules block string is present in `AGENTS.md`). Report
`Setup: OK (paired)` or `Setup: local-only`.

**Exact command sequence for this beat (run from the project root):**
```sh
bash ~/.claude/skills/vibe-to-ship/scripts/install.sh   # rules block + mcp.json hints
bash ~/.claude/skills/vibe-to-ship/scripts/loop.sh boot # doctor: exit 1 only on blocking High
```

You can also do these three files by hand — the skill supports both paths.
Setup is one-time; every future session then boots with memory.

**Path convention for the rest of this document:** `VTS` is the installed skill
root — `$HOME/.claude/skills/vibe-to-ship` for Claude Code,
`.opencode/skills/vibe-to-ship` for opencode. Every script is invoked by absolute
path (`bash "$VTS/scripts/loop.sh" ...`) with your **project** as the working
directory — the scripts read/write the project they run in, never the skill.

### Beat 1: Boot (Guardrails & MCP Connect)

**When:** every session, immediately after Beat 0. **Goal:** make the dangerous
things impossible and the expensive things visible.

1. Load the safety denylist into working constraints:
   `.env*`, `auth/`, `secrets/`, `payments/`, `migrations/`, `credentials/`.
   You do not read, write, or move these without explicit human approval — no
   exceptions, including "just to check".
2. Check token/cost budget. If the repo has `loop-budget.md`, read caps first;
   otherwise assume: stop and ask before any operation likely to exceed ~50k
   tokens (large refactors, whole-repo rewrites).
3. Connect to the OpenLotus MCP server (`get_reality`, `get_memory`).
   - **Failure mode:** MCP unreachable → continue local-only with `PROGRESS.md`
     + `git` commands, and say so in one line. Never fake memory contents.
   - Every record is timestamped at write time (`createdAt`, `capturedAt`,
     `lastReviewAt`) so the timeline is ordered. When you record, include *why*,
     not just *what* — a decision without reasoning is noise.

### Beat 2: Triage (Reconcile Tree Memory vs Reality)

**When:** before any plan, any code, any commit. **Goal:** a prioritized,
evidence-backed picture of what is actually true right now.

1. Pull observed reality: run `bash "$VTS/scripts/loop.sh" triage` (wraps `triage.sh`:
   branch, quiet days, dirty files, TODO/FIXME counts → High/Watch/Noise).
   Add `--json` when a machine will consume the output; add `--fail-on-high`
   only in CI gates, never in interactive sessions. No MCP? The script already
   runs the git equivalents locally: `git status --short`, `git log -1 --format=%ct`,
   `grep -rEn "TODO|FIXME|HACK"`.
2. Load declared state: MCP `get_memory` (or `PROGRESS.md` → Goal + Active Nodes).
3. Diff them. Every mismatch becomes a finding classified:
   - **High** — blocks the goal or contradicts a recorded decision. Act today.
   - **Watch** — real but not blocking. Monitor, re-check next session.
   - **Noise** — looked at, deliberately ignored (record *why* it's noise so the
     next session doesn't re-investigate).
4. Apply the **Fake-Edge Test** to the resulting work list: remove sequential
   arrows where no data is passed, converting them into parallel fan-out nodes.

**Good output looks like this** (paste this shape, filled in):

```markdown
## Triage — <repo> @ <branch> (<date>)
- Reality: quiet 2d · 3 dirty files (+48/−11) · 14 TODOs · TS 749 files
- High (2): [auth-form-validation] email regex missing — contradicts decision dec-2208a1; [ci-red] main failing on lint
- Watch (1): TODO count up 40% this week
- Noise (1): stale feature-flag comment in legacy/ (decided: leave until Q4 cleanup)
- Next: fan out [auth-form-validation] + [ci-red] in parallel (no shared files)
```

**Bad output — reject your own draft if it matches any of these:**

```markdown
- "Repo looks mostly fine, some cleanup needed"   ← no evidence, no counts, no ids
- "High: tech debt is accumulating"               ← not observable, not actionable
- "Watch: lots of TODOs"                           ← how many? where? since when?
- Three High items that are all the same root cause ← merge them; shrink the goal
```

**Failure modes:**
- *Everything is High.* → Your goal is too big. Shrink the goal, re-triage.
- *Everything is Noise.* → Either genuinely clean (say so, stop — do not invent
  work) or you're not looking (re-run reality with wider scope).
- *Reality tools fail* (no git? not a repo?) → say what you couldn't observe,
  triage from declared state only, mark findings `unverified`.

### Beat 3: Act (The Diamond Pattern)

**When:** only after triage produced at least one High or Watch item the user
approved. **Goal:** execute with parallelism and zero collisions.

0. **Contract first**: print the bounded-task contract before any edit —
   `bash "$VTS/scripts/loop.sh" act` renders the template (TASK / SCOPE / DONE / STOP).
   Fill every field. A blank STOP is a promise to drift.
1. **Fan Out**: one node per independent work item. Isolate file-writing nodes
   in git worktrees so two writers never touch the same checkout:
   ```bash
   git worktree add ../wt-<node-id> -b wip/<node-id>
   # ...agent works inside ../wt-<node-id>...
   git worktree remove --force ../wt-<node-id>   # after merge
   ```
   - **Failure mode:** worktree creation fails (bare repo? no git?) → fall back
     to sequential execution in the main tree, one node at a time, and say so.
2. **Reduce**: merge worker outputs with deterministic steps — `git apply`,
   dedupe repeated hunks with a script, run the formatter. Zero LLM tokens for
   mechanical merging. If two workers touched the same lines, that was a fake
   edge you missed: resolve by hand, note it in the debrief.
3. **Verify**: hand each output to a fresh-context skeptic (Beat 4). Do not
   merge anything unverified. Ever.

### Beat 4: Verify (Fresh-Context Skeptics & Anchors)

**When:** for every artifact before it merges or ships. **Goal:** catch what
confidence hides.

Spawn each verifier as a **new agent invocation** containing only: (a) the
output artifact, (b) its node contract, (c) the repo at the relevant commit.
Never the worker's transcript.

**Always anchor with the script first** — it computes, it doesn't opine:
```sh
bash "$VTS/scripts/loop.sh" verify --scope "src/payments/retry.ts,tests/retry.test.ts"
# options: --build-cmd "pnpm build"  --test-cmd "pnpm test"  (auto-detects by default)
```
Exit 0 = reality matches the plan; exit 1 = a FAIL line exists — read it, fix
it, re-run. The verifier then runs exactly 3 checks on top:

1. *Correctness*: does the code/finding hold up on its own merits?
2. *Currentness*: is it based on latest HEAD and current sources?
3. *Anchor Check*: did the compiler / test suite / linter *actually* pass —
   paste the command and its exit code, never a claim.

- Reject and retry on schema or test failure. Max **3 attempts** per node,
  then escalate to the human with: what was tried, what failed, and the exact
  error output. Never a fourth silent attempt.
- **Failure mode:** no test suite exists → the anchor becomes `tsc --noEmit`
  (or equivalent typecheck) + a smoke run of the changed path. Say which
  anchor you used; "no tests" is information, not an excuse to skip.

### Beat 5: Learn (Commit Tree Memory & Debrief)

**When:** after work merges (or is deliberately abandoned). **Goal:** the next
session starts smarter.

1. Record decision nodes (`record_decision` via MCP, or append to `PROGRESS.md`
   → Decisions with date + reasoning).
2. Update node statuses (`pending` → `done`, or `dropped` with reason).
3. Push updated state to the OpenLotus Web App dashboard & progress map
   (automatic on `record_decision` / `sync`; verify with `get_memory`).
4. Debrief in **1 line**: what survived, what failed, what changed.
   Example: `Shipped auth validation + ci lint fix; dropped legacy-flag cleanup (Q4); drift 0%.`
5. Clean up: remove merged worktrees, confirm `git status` is clean.

**Failure mode:** session ending mid-flight → record partial state honestly
(`status: active`, `attempts: n/3`, next step spelled out). A half-written truth
beats a clean lie.

---

## 4. Rules

- **Worker and verifier never share context.**
- **No free-text nodes.** Every node output must match its schema contract.
- **No fake edges.** If job B doesn't read job A's data, run B and A in parallel.
- **Isolate file writers.** Two nodes editing files run in separate git worktrees.
- **3-attempt cap.** Never loop indefinitely on a failing node.
- **No auto-push/merge.** Always require human approval before shipping.
- **Announce beats, don't narrate them.** One line per beat transition; details live in artifacts, not chat.
- **Timestamps on everything.** Every record carries `createdAt`; every sync carries `capturedAt`. Undated memory is unusable memory.

---

## 5. OpenLotus MCP & Web App Integration

OpenLotus provides the tree-like interactive memory UI and real-time state via MCP:

- MCP Tools: `get_reality` (sense repo) · `get_drift` (cloud reconciled drift) · `get_memory` (shared context tree) · `create_project` (new project setup) · `switch_project` (point pairing at a project id) · `record_decision` (immutable decision nodes).
  Full tool contract with parameters and examples: `references/openlotus-engine.md`.
- `create_project` — call when the founder wants a new project. Takes name (required) + description, stage (idea/launched/growing/scaling), url, connected tools. Returns the new project's id. Follow with `switch_project` so this repo's pairing points at it.
- Web App: view your interactive tree memory map at `/map`, weekly review at `/dashboard`, full guide at `/docs`, the skill's home at `/vibe-to-ship`.
- Pairing: `npx openlotus pair` (browser flow, no flags) or tell the agent "set up OpenLotus" — see Beat 0.

**Setup — two paths, same result:** *Agent does it* — tell your agent "set up OpenLotus" and Beat 0 does the three files for you; *Manual* — copy the `mcp.json` snippet and the rules block from `references/agent-rules-snippet.md` by hand, or run `bash "$VTS/scripts/install.sh"` from your project root. All paths are one-time; every future session then boots with memory. The landing and docs call this out as "manual or let your agent do it with vibe-to-ship."

**Persistence without per-prompt repetition:** after that one-time setup, no skill invocation is needed for everyday memory keeping — the rules handle `get_memory`/`record_decision` automatically. Invoke this skill for full triage/plan/verify cycles. Every action is timestamped in the shared map.

**Without OpenLotus:** the entire skill still works. `PROGRESS.md` is the tree, `git` commands are reality, worktrees still isolate, verifiers still verify. You lose shared visibility and drift computation — nothing else.

---

## 6. Script Reference (quick card)

| Command | Beat | Exit 1 when |
|---|---|---|
| `bash "$VTS/scripts/loop.sh" boot` | 1 | doctor finds a blocking High |
| `bash "$VTS/scripts/loop.sh" triage [--json] [--fail-on-high]` | 2 | only with `--fail-on-high` and a High exists |
| `bash "$VTS/scripts/loop.sh" act` | 3 | never (prints the contract template) |
| `bash "$VTS/scripts/loop.sh" verify [--scope a,b] [--build-cmd] [--test-cmd]` | 4 | build/test fail, scope violated |
| `bash "$VTS/scripts/loop.sh" learn` | 5 | never (appends session summary to MEMORY.md) |

All scripts are POSIX `sh`, `set -eu`, read-only except `learn` (appends) and
`install` (appends once). Tapes and frame sources for the README demos live in
`docs/tapes/`.
