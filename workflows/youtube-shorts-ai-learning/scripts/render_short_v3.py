#!/usr/bin/env python3
"""Render v3 premium image-based YouTube Short.

Uses generated key visuals + exact Supertonic scene audio timings.
"""
from __future__ import annotations

import html
import json
import math
import shlex
import subprocess
import textwrap
from pathlib import Path

W, H = 1080, 1920
FPS = 30

KEYFRAME_GLOBS = [
    "01_step1*.png",
    "02_step2*.png",
    "03_step3_tool_islands_no_text.png",
    "04_step4*.png",
    "05_step5*.png",
    "06_step6*.png",
    "07_step7*.png",
]


def run(cmd: list[str]) -> str:
    return subprocess.check_output(cmd, text=True).strip()


def duration(path: Path) -> float:
    return float(run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=nw=1:nk=1", str(path)]))


def wrap(text: str, width: int) -> list[str]:
    return textwrap.wrap(text, width=width, break_long_words=False, break_on_hyphens=False)


def tspans(lines: list[str], x: int, y: int, size: int, leading: int, color: str, weight: str, anchor="middle") -> str:
    out = [f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-family="Arial, Helvetica, sans-serif" font-size="{size}" font-weight="{weight}" fill="{color}">']
    for i, line in enumerate(lines):
        dy = 0 if i == 0 else leading
        out.append(f'<tspan x="{x}" dy="{dy}">{html.escape(line)}</tspan>')
    out.append('</text>')
    return "\n".join(out)


def svg_for_scene(img: Path, caption: str, idx: int, total: int) -> str:
    cap_lines = wrap(caption, 22)
    size = 74 if len(cap_lines) <= 2 else 62
    lead = 88 if len(cap_lines) <= 2 else 74
    progress = int(820 * idx / total)
    accent = ["#38bdf8", "#22d3ee", "#facc15", "#34d399", "#f59e0b", "#67e8f9", "#a78bfa"][idx-1]
    href = img.as_uri()
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  <defs>
    <filter id="blur"><feGaussianBlur stdDeviation="32"/></filter>
    <filter id="shadow" x="-30%" y="-30%" width="160%" height="160%"><feDropShadow dx="0" dy="24" stdDeviation="28" flood-color="#000" flood-opacity="0.70"/></filter>
    <linearGradient id="shade" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#000000" stop-opacity="0.10"/>
      <stop offset="55%" stop-color="#000000" stop-opacity="0.10"/>
      <stop offset="100%" stop-color="#000000" stop-opacity="0.72"/>
    </linearGradient>
    <clipPath id="round"><rect x="78" y="218" width="924" height="924" rx="56"/></clipPath>
    <radialGradient id="glow" cx="50%" cy="39%" r="60%">
      <stop offset="0%" stop-color="{accent}" stop-opacity="0.22"/>
      <stop offset="100%" stop-color="{accent}" stop-opacity="0"/>
    </radialGradient>
  </defs>
  <rect width="1080" height="1920" fill="#030712"/>
  <image href="{href}" x="-420" y="0" width="1920" height="1920" preserveAspectRatio="xMidYMid slice" filter="url(#blur)" opacity="0.65"/>
  <rect width="1080" height="1920" fill="#02040A" opacity="0.48"/>
  <rect width="1080" height="1920" fill="url(#glow)"/>
  <rect width="1080" height="1920" fill="url(#shade)"/>

  <g filter="url(#shadow)">
    <rect x="74" y="214" width="932" height="932" rx="60" fill="#050912" opacity="0.82"/>
    <image href="{href}" x="78" y="218" width="924" height="924" preserveAspectRatio="xMidYMid slice" clip-path="url(#round)"/>
    <rect x="78" y="218" width="924" height="924" rx="56" fill="none" stroke="#ffffff" stroke-opacity="0.18" stroke-width="2"/>
  </g>

  <rect x="130" y="96" width="820" height="14" rx="7" fill="#ffffff" opacity="0.15"/>
  <rect x="130" y="96" width="{progress}" height="14" rx="7" fill="{accent}" opacity="0.96"/>
  <text x="540" y="172" text-anchor="middle" font-family="Arial, Helvetica, sans-serif" font-size="34" font-weight="900" fill="#E5E7EB" letter-spacing="4">AI TOOL CALLING</text>

  <g filter="url(#shadow)">
    <rect x="82" y="1248" width="916" height="360" rx="50" fill="#030712" opacity="0.82" stroke="#ffffff" stroke-opacity="0.15"/>
    <rect x="132" y="1295" width="816" height="5" rx="2.5" fill="{accent}" opacity="0.95"/>
    {tspans(cap_lines, 540, 1410 if len(cap_lines)<=2 else 1380, size, lead, "#ffffff", "900")}
  </g>

  <text x="540" y="1740" text-anchor="middle" font-family="Arial, Helvetica, sans-serif" font-size="37" font-weight="900" fill="#ffffff">Brain chooses. Software guards. Tools act.</text>
  <text x="540" y="1794" text-anchor="middle" font-family="Arial, Helvetica, sans-serif" font-size="25" font-weight="700" fill="#CBD5E1" opacity="0.84">Tool calling in 40 seconds</text>
</svg>'''


def main() -> None:
    ep = Path("/Users/danny/ai-shorts-workflow/episodes/tool-calling-101")
    scenes = json.loads((ep / "script/v3_scenes.json").read_text(encoding="utf-8"))["scenes"]
    kdir = ep / "video/v3_keyframes"
    out_dir = ep / "video/v3_render"
    out_dir.mkdir(parents=True, exist_ok=True)

    stills = []
    for i, glob in enumerate(KEYFRAME_GLOBS, 1):
        matches = sorted(kdir.glob(glob))
        if not matches:
            raise SystemExit(f"missing keyframe {glob}")
        still = out_dir / f"scene_{i:02d}.png"
        svg = svg_for_scene(matches[0], scenes[i-1]["caption"], i, len(scenes))
        subprocess.run(["magick", "svg:-", str(still)], input=svg, text=True, check=True)
        stills.append(still)

    # Scene durations = narration segment duration + silence tail used in concatenated audio.
    seg_dir = ep / "audio/v3_segments"
    seg_durs = []
    for i in range(1, len(stills)+1):
        seg_durs.append(duration(seg_dir / f"{i:02d}.wav") + 0.18)

    segment_videos = []
    for i, (still, d) in enumerate(zip(stills, seg_durs), 1):
        frames = max(1, int(math.ceil(d * FPS)))
        seg = out_dir / f"seg_{i:02d}.mp4"
        # Alternate slight push-in and push-out to avoid repetitive motion.
        if i % 2:
            z = f"1+0.055*on/{frames}"
        else:
            z = f"1.055-0.045*on/{frames}"
        fade_out_start = max(0, d - 0.18)
        vf = f"zoompan=z='{z}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={frames}:s=1080x1920:fps={FPS},fade=t=in:st=0:d=0.12,fade=t=out:st={fade_out_start:.3f}:d=0.16,format=yuv420p"
        subprocess.check_call([
            "ffmpeg", "-y", "-loop", "1", "-i", str(still), "-frames:v", str(frames),
            "-vf", vf, "-an", "-c:v", "libx264", "-preset", "slow", "-crf", "16", str(seg)
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        segment_videos.append(seg)

    concat = out_dir / "concat_video.txt"
    concat.write_text("".join(f"file {shlex.quote(str(p))}\n" for p in segment_videos), encoding="utf-8")
    video_only = out_dir / "video_only.mp4"
    subprocess.check_call(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(concat), "-c", "copy", str(video_only)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    final = ep / "video/final_v3.mp4"
    subprocess.check_call([
        "ffmpeg", "-y", "-i", str(video_only), "-i", str(ep / "audio/narration_v3.wav"),
        "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", str(final)
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(final)


if __name__ == "__main__":
    main()
