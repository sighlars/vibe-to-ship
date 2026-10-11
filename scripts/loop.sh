#!/bin/sh
# vibe-to-ship loop — single dispatcher for the 5-beat loop.
# Each beat is one command. The loop is the discipline; this script is the reminder.
#
# Usage: ./scripts/loop.sh [boot|triage|act|verify|learn]
#   boot    verify the environment is ready (delegates to doctor.sh)
#   triage  reality check before planning (delegates to triage.sh)
#   act     print the bounded-task contract, then hand off to the agent
#   verify  compare reality against the plan (delegates to verify.sh)
#   learn   append a session summary block to MEMORY.md (or stdout if absent)
#
# Exit codes: 0 = beat passed, 1 = beat failed (verify/boot), 2 = bad usage.
set -eu

SCRIPT_DIR="$(CDPATH="" cd -- "$(dirname -- "$0")" && pwd)"
BEAT="${1:-}"

if [ -z "$BEAT" ]; then
  echo "Usage: $0 [boot|triage|act|verify|learn]"
  echo ""
  echo "The 5-beat loop:"
  echo "  boot    - environment readiness (doctor)"
  echo "  triage  - reality check before planning"
  echo "  act     - bounded-task contract shown, then do ONE task"
  echo "  verify  - reality vs. plan (build, tests, drift)"
  echo "  learn   - session summary appended to MEMORY.md"
  exit 2
fi

case "$BEAT" in
  boot)
    echo "== BEAT 1/5: BOOT =="
    # sh-prefix: scripts ship 0644 (no exec bit), so never exec siblings
    # directly — a fresh clone would fail with Permission denied.
    exec sh "$SCRIPT_DIR/doctor.sh"
    ;;

  triage)
    echo "== BEAT 2/5: TRIAGE =="
    exec sh "$SCRIPT_DIR/triage.sh"
    ;;

  act)
    echo "== BEAT 3/5: ACT =="
    echo ""
    echo "Before writing code, state the bounded-task contract out loud:"
    echo ""
    echo "  TASK:   <one sentence, one deliverable>"
    echo "  SCOPE:  <files/dirs allowed to touch — anything else is drift>"
    echo "  DONE:   <the check that proves it, e.g. 'pnpm test passes'>"
    echo "  STOP:   <condition to halt and re-triage, e.g. 'if schema must change'>"
    echo ""
    echo "Rules while acting:"
    echo "  - One task per loop. Park everything else in the backlog."
    echo "  - If DONE needs a second deliverable, that is a second loop."
    echo "  - If you violate SCOPE, stop, run '$0 triage', re-contract."
    echo ""
    echo "Now act. When finished, run: $0 verify"
    exit 0
    ;;

  verify)
    echo "== BEAT 4/5: VERIFY =="
    shift # drop the beat name so flags (e.g. --scope) reach verify.sh
    if [ -f "$SCRIPT_DIR/verify.sh" ]; then
      exec sh "$SCRIPT_DIR/verify.sh" "$@"
    else
      echo "verify.sh not found — falling back to triage as reality check"
      exec sh "$SCRIPT_DIR/triage.sh" "$@"
    fi
    ;;

  learn)
    echo "== BEAT 5/5: LEARN =="
    MEM_FILE="MEMORY.md"
    if [ ! -f "$MEM_FILE" ]; then
      echo "No MEMORY.md found — printing the session summary to stdout instead."
      echo "(Create MEMORY.md and re-run to persist it.)"
      MEM_FILE=""
    fi
    SUMMARY="$(printf '%s\n' \
      "" \
      "## Session — $(date +%F' '%H:%M)" \
      "- Branch: $(git branch --show-current 2>/dev/null || echo '?')" \
      "- Dirty files at close: $(git status --short 2>/dev/null | wc -l | tr -d ' ')" \
      "- Last commit: $(git log -1 --format='%h %s' 2>/dev/null || echo 'none')" \
      "- Decisions: <fill in — what did you choose and why?>" \
      "- Next: <fill in — the single next bounded task>")"
    if [ -n "$MEM_FILE" ]; then
      printf '%s\n' "$SUMMARY" >> "$MEM_FILE"
      echo "Appended session summary to $MEM_FILE"
    else
      printf '%s\n' "$SUMMARY"
    fi
    exit 0
    ;;

  *)
    echo "Unknown beat: $BEAT (expected boot|triage|act|verify|learn)" >&2
    exit 2
    ;;
esac
