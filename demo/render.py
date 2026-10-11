#!/usr/bin/env python3
"""Render transcript.json to PNG frames (1280x720 @30fps), then ffmpeg assembles.
Deterministic: same transcript always yields the same video. Re-cut by editing
the transcript or this script's timing constants — no re-running commands."""
import json
import os
import random
import subprocess
from PIL import Image, ImageDraw, ImageFont

W, H, FPS = 1280, 720, 30
FRAMES = "/tmp/demo-pipeline/frames"
BG = (20, 18, 15)
HEADER_BG = (32, 28, 23)
TEXT = (236, 231, 223)
MUTED = (166, 160, 148)
GREEN = (143, 206, 126)
RED = (224, 112, 90)
AMBER = (216, 178, 106)
PROMPT_C = (126, 200, 210)
FONT = "/usr/share/fonts/TTF/JetBrainsMonoNerdFontMono-Regular.ttf"
FONT_B = "/usr/share/fonts/TTF/JetBrainsMonoNerdFontMono-Bold.ttf"
FS = 21
LH = 30
TOP = 78
MAX_LINES = 20

rng = random.Random(7)
font = ImageFont.truetype(FONT, FS)
font_b = ImageFont.truetype(FONT_B, FS)
font_big = ImageFont.truetype(FONT_B, 44)
font_mid = ImageFont.truetype(FONT, 26)


def colorize(line: str):
    s = line.strip()
    if s.startswith(("OK", "PASS", "VERDICT: PASSED", "Synced", "(clean)", "Result:")):
        return GREEN
    if s.startswith(("FAIL", "VERDICT: FAILED", "WARN", "Watch:")):
        return AMBER if s.startswith(("WARN", "Watch:")) else RED
    if s.startswith("=="):
        return TEXT
    return MUTED if s.startswith(("#", "drift:", "Drift:")) else TEXT


def base(title: str):
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, W, 46], fill=HEADER_BG)
    for i, c in enumerate([(224, 112, 90), (216, 178, 106), (143, 206, 126)]):
        d.ellipse([18 + i * 26, 15, 18 + i * 26 + 14, 29], fill=c)
    d.text([90, 12], title, font=font, fill=MUTED)
    return img, d


def draw_lines(d, lines, cursor_on: bool):
    """lines: list of (text, color, is_prompt_prefix_len)."""
    vis = lines[-MAX_LINES:]
    y = TOP
    for text, color in vis:
        d.text([36, y], text, font=font, fill=color)
        y += LH
    if cursor_on:
        last = vis[-1][0] if vis else ""
        w = d.textlength(last, font=font)
        x = 36 + w
        y0 = TOP + (len(vis) - 1) * LH + 3 if vis else TOP
        d.rectangle([x, y0, x + 12, y0 + 22], fill=TEXT)


def wrap_line(text: str, max_w: int = W - 72):
    """Greedy word-wrap to pixel width; hard-breaks overlong tokens."""
    words, lines, cur = text.split(" "), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if font.getlength(trial) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w
        while font.getlength(cur) > max_w:
            # hard-break an overlong token
            i = len(cur)
            while i > 0 and font.getlength(cur[:i]) > max_w:
                i -= 1
            i = max(i, 1)
            lines.append(cur[:i])
            cur = cur[i:]
    if cur or not lines:
        lines.append(cur)
    return lines


def push(shown, text, color):
    for ln in wrap_line(text):
        shown.append((ln, color))


def save(img, n):
    img.save(os.path.join(FRAMES, f"f{n:05d}.png"))
    return n + 1


def hold(img, n, seconds, blink=False):
    frames = int(seconds * FPS)
    if not blink:
        for _ in range(frames):
            n = save(img, n)
        return n
    base_img = img.copy()
    for i in range(frames):
        img = base_img.copy()
        if (i // 15) % 2 == 0:
            d = ImageDraw.Draw(img)
            # cursor appended by caller state; simplest: redraw last line cursor
            d.rectangle([36, TOP, 48, TOP + 22], fill=TEXT)
        n = save(img, n)
    return n


def main():
    os.makedirs(FRAMES, exist_ok=True)
    for f in os.listdir(FRAMES):
        os.remove(os.path.join(FRAMES, f))
    t = json.load(open("/tmp/demo-pipeline/transcript.json"))["steps"]
    n = 0
    shown: list = []  # (text, color)

    def paint(cursor=False):
        img, d = base("demo — vibe-to-ship × openlotus")
        draw_lines(d, shown, cursor)
        return img

    for s in t:
        if s["kind"] in ("title", "end"):
            # title card
            img = Image.new("RGB", (W, H), BG)
            d = ImageDraw.Draw(img)
            lines = s["lines"]
            tw = max(d.textlength(lines[0], font=font_big), 200)
            y0 = H // 2 - 60
            d.text([(W - tw) // 2, y0], lines[0], font=font_big, fill=TEXT)
            if len(lines) > 1:
                for j, sub in enumerate(lines[1:]):
                    sw = d.textlength(sub, font=font_mid)
                    d.text([(W - sw) // 2, y0 + 70 + j * 40], sub, font=font_mid, fill=MUTED)
            hold_s = 4.0 if s["kind"] == "end" else 2.2
            for _ in range(int(hold_s * FPS)):
                n = save(img, n)
            shown = []
            continue
        # command step (may span lines, e.g. heredocs — type line by line)
        full = f"$ {s['cmd']}"
        for li, raw_line in enumerate(full.split("\n")):
            buf = ""
            for ch in raw_line:
                buf += ch
                shown_tmp = shown + [(ln, TEXT) for ln in wrap_line(buf)]
                img, d = base("demo — vibe-to-ship × openlotus")
                draw_lines(d, shown_tmp, True)
                n = save(img, n)
                # ~2 frames per char at 30fps ≈ 65ms/char
                img2, d2 = base("demo — vibe-to-ship × openlotus")
                draw_lines(d2, shown_tmp, False)
                n = save(img2, n)
            push(shown, raw_line, TEXT)
        # pause, then output
        for _ in range(5):
            n = save(paint(True), n)
        for line in s["output"]:
            push(shown, line, colorize(line))
        img = paint(False)
        for _ in range(12):
            n = save(img, n)
        if s.get("exit"):
            push(shown, f"→ exit {s['exit']}", RED)
            img = paint(False)
            for _ in range(20):
                n = save(img, n)
        else:
            for _ in range(6):
                n = save(paint(False), n)

    print(f"frames: {n} (~{n / FPS:.0f}s)")


main()
