#!/usr/bin/env python3
"""Capture the OpenLotus product demo: real CLI + a real agent TUI session
reading the live map over MCP. Every command actually runs.

Presentation-only cleanup (documented, content untouched): strip ANSI escape
sequences, carriage-return redraws, and npm launcher notice lines — the same
cleanup any terminal recorder applies. Command text and outputs are verbatim.
"""
import json
import re
import subprocess

OPENLOTUS = "/home/sighlars/Desktop/openlotus"
OP = "/home/sighlars/.opencode/bin/opencode"
ANSI = re.compile(r"\x1b\[[0-9;?]*[a-zA-Z]|\x1b\][^\x07]*\x07|\x1b[()][0-9A-Z]|\r")


def clean(text: str) -> list[str]:
    lines = []
    for raw in text.replace("\t", "  ").split("\n"):
        seg = raw.split("\r")[-1]
        seg = ANSI.sub("", seg).rstrip()
        if seg.startswith("npm notice"):
            continue
        lines.append(seg)
    while lines and lines[-1] == "":
        lines.pop()
    while lines and lines[0] == "":
        lines.pop(0)
    return lines


def run(cmd: str, timeout: int = 600):
    p = subprocess.run(cmd, shell=True, cwd=OPENLOTUS, capture_output=True, text=True, timeout=timeout)
    out = clean((p.stdout or "") + (p.stderr or ""))
    print(f"[cmd exit={p.returncode}] {cmd[:70]} ({len(out)} lines)")
    return {"kind": "cmd", "cmd": cmd, "output": out[:150], "exit": p.returncode}


AGENT_PROMPT = (
    "Using ONLY the openlotus MCP tools get_memory and get_drift, read this "
    "project's shared ProgressMap and report drift as High, Watch, or Noise. "
    "Do not edit files. Do not run shell commands. Do not record anything. "
    "Under 12 lines."
)

steps = [
    {"kind": "title", "lines": ["openlotus — memory that survives sessions", "the same map, in your terminal and your agent"]},
    {"kind": "cmd", "cmd": "npx openlotus --help"},
    {"kind": "title", "lines": ["push reality to the map", "one command after real work"]},
]
out_steps = [steps[0]]
r = subprocess.run("npx openlotus --help", shell=True, cwd=OPENLOTUS, capture_output=True, text=True, timeout=120)
o = clean((r.stdout or "") + (r.stderr or ""))
out_steps.append({"kind": "cmd", "cmd": "npx openlotus --help", "output": o[:150], "exit": r.returncode})
print(f"[cmd exit={r.returncode}] npx openlotus --help ({len(o)} lines)")
out_steps.append(steps[2])

for cmd in ["npx openlotus sync", "npx openlotus status"]:
    out_steps.append(run(cmd, timeout=180))

out_steps.append({"kind": "title", "lines": ["your agent reads the same map — live", "a real coding agent, over MCP, right now"]})
agent_cmd = (
    f"{OP} run --agent researcher --model opencode/ling-3.1-flash-free "
    f'--title "openlotus-map-check" "{AGENT_PROMPT}"'
)
out_steps.append(run(agent_cmd, timeout=590))
out_steps.append({"kind": "end", "lines": [
    "openlotus.io — memory that survives sessions",
    "docs: openlotus.io/docs#pairing",
    "vibe first: github.com/sighlars/vibe-to-ship",
]})

with open("/tmp/demo-pipeline/transcript2.json", "w") as f:
    json.dump({"steps": out_steps}, f, indent=1)
print("wrote /tmp/demo-pipeline/transcript2.json")
