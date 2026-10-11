#!/usr/bin/env python3
"""Capture real demo beats into transcript.json. Every command actually runs;
outputs are verbatim. Run once — rendering replays the transcript offline."""
import json
import subprocess

VTS = "/home/sighlars/Desktop/vibe-to-ship/scripts"
OPENLOTUS = "/home/sighlars/Desktop/openlotus"
SAMPLE = "/tmp/demo-app"

steps = [
    {"kind": "title", "lines": ["a vibe-coded mess", "one dirty repo, two TODOs, no proof of done"]},
    {"kind": "cmd", "cwd": SAMPLE, "cmd": "git status --short"},
    {"kind": "title", "lines": ["beat 1/5 — boot", "is this repo even workable?"]},
    {"kind": "cmd", "cwd": SAMPLE, "cmd": f"sh {VTS}/loop.sh boot"},
    {"kind": "title", "lines": ["beat 2/5 — triage", "reality before planning"]},
    {"kind": "cmd", "cwd": SAMPLE, "cmd": f"sh {VTS}/loop.sh triage"},
    {"kind": "title", "lines": ["beat 3/5 — act", "one task, one scope, one definition of done"]},
    {"kind": "cmd", "cwd": SAMPLE, "cmd": f"sh {VTS}/loop.sh act"},
    {"kind": "title", "lines": ["beat 4/5 — verify", "done means proven — watch it fail"]},
    {"kind": "cmd", "cwd": SAMPLE, "cmd": f'sh {VTS}/loop.sh verify --scope "src/" --build-cmd "npm run build" --test-cmd "npm test"'},
    {"kind": "title", "lines": ["drift caught — file the scratch, do the work"]},
    {"kind": "cmd", "cwd": SAMPLE, "cmd": 'git add notes.txt && git -c user.email=demo@local -c user.name=demo commit -qm "chore: file scratch notes" && touch MEMORY.md && git status --short && echo "(ready)"'},
    {"kind": "cmd", "cwd": SAMPLE, "cmd": "cat > src/math.js <<'EOF'\nexport const BASE_BONUS = 42;\nexport const total = (a, b) => a + b + BASE_BONUS;\nEOF\ngit diff --stat"},
    {"kind": "cmd", "cwd": SAMPLE, "cmd": f'sh {VTS}/loop.sh verify --scope "src,MEMORY.md" --build-cmd "npm run build" --test-cmd "npm test"'},
    {"kind": "cmd", "cwd": SAMPLE, "cmd": 'git add -A && git -c user.email=demo@local -c user.name=demo commit -qm "fix: name the bonus, drop the TODOs" && git status --short && echo "(clean)"'},
    {"kind": "title", "lines": ["beat 5/5 — learn", "the session writes down what happened"]},
    {"kind": "cmd", "cwd": SAMPLE, "cmd": f"sh {VTS}/loop.sh learn && tail -n 7 MEMORY.md"},
    {"kind": "title", "lines": ["attach memory — pair once, then it persists", "vibe-to-ship works offline; OpenLotus keeps the record"]},
    {"kind": "cmd", "cwd": OPENLOTUS, "cmd": "npx openlotus sync"},
    {"kind": "cmd", "cwd": OPENLOTUS, "cmd": "npx openlotus status"},
    {"kind": "end", "lines": ["vibe-to-ship — your agent ships the truth", "github.com/sighlars/vibe-to-ship", "openlotus.io — memory that survives sessions"]},
]

out = []
for s in steps:
    if s["kind"] in ("title", "end"):
        out.append(s)
        print(f"[{s['kind']}] {' / '.join(s['lines'][:1])}")
        continue
    p = subprocess.run(s["cmd"], shell=True, cwd=s["cwd"], capture_output=True, text=True, timeout=180)
    text = (p.stdout or "") + (p.stderr or "")
    lines = text.replace("\t", "  ").split("\n")
    if lines and lines[-1] == "":
        lines.pop()
    out.append({"kind": "cmd", "cmd": s["cmd"], "output": lines[:120], "exit": p.returncode})
    print(f"[cmd exit={p.returncode}] {s['cmd'][:70]} ({len(lines)} lines)")

with open("/tmp/demo-pipeline/transcript.json", "w") as f:
    json.dump({"steps": out}, f, indent=1)
print("wrote /tmp/demo-pipeline/transcript.json")
