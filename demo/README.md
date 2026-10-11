# Demo pipeline (automated terminal video)

Renders `../assets/demo-terminal.mp4` (100s, 1280x720): a messy sample repo
runs the real 5-beat loop (triage finds drift, verify FAILS on scope, fix,
verify PASSES, learn), then `npx openlotus sync` + `status` attaches memory.

Two phases — capture once, re-render freely:

1. **Capture** (runs real commands, writes `transcript.json`):
   `python3 demo/capture.py` — needs the sample repo at `/tmp/demo-app`
   (rebuild per the commands at the top of `capture.py` if deleted) and an
   OpenLotus pairing for the `sync` beat (writes one real snapshot).
2. **Render** (offline, deterministic — same transcript, same video):
   `python3 -m venv /tmp/demo-venv && /tmp/demo-venv/bin/pip install pillow`,
   then `/tmp/demo-venv/bin/python demo/render.py` writes PNGs to
   `/tmp/demo-pipeline/frames/`, then:
   `ffmpeg -framerate 30 -i /tmp/demo-pipeline/frames/f%05d.png -c:v libx264 -pix_fmt yuv420p -crf 20 assets/demo-terminal.mp4`

To re-cut: edit `transcript.json` (drop/reorder steps) or the timing
constants in `render.py` and re-run phase 2 only. Nothing here is faked —
every line on screen is verbatim output of a command that actually ran.
