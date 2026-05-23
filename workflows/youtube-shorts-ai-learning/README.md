# YouTube Shorts AI Learning Video Workflow

Goal: convert any AI concept into a premium educational YouTube Short for a broad non-developer global audience.

This workflow was extracted from the `AI Tool Calling` sample that improved a rejected 2/10 draft into an 8.7-9.0/10 candidate by changing the production system:

- from generic SVG/vector slides
- to cinematic key visuals + per-scene Supertonic narration + strict contact-sheet QA

## Use when

- User gives an AI concept and asks for a YouTube Short.
- Accuracy matters and claims must be researched.
- The audience is non-developer or broad/global.
- The video must feel premium, not like a generic AI slideshow.

## Quick command flow

```bash
# 1. write research + storyboard
# workflows/youtube-shorts-ai-learning/templates/v3_scenes.example.json

# 2. generate one TTS file per scene with local Supertonic
cd /Users/danny/ai-shorts-workflow/supertonic-tts
node bin/supertonic.mjs -f scene_01.txt -o scene_01.wav --lang en --voice F1 --speed 1.10 --steps 10 --silence 0.18 --no-play

# 3. render with image-based v3 renderer
python3 scripts/render_short_v3.py

# 4. inspect preview contact sheet before upload
ffprobe -v error -show_entries format=duration,size -of default=nw=1 video/final_v3.mp4
```

## Core quality rule

If the user says “too AI”, “voice/content mismatch”, or scores it low, do not keep polishing the same slide system. Re-storyboard from scratch and align:

1. exact narration line
2. exact caption
3. image prompt
4. camera motion
5. scene duration from measured audio

## Files in this workflow

- `workflow.md` — full production playbook.
- `templates/v3_scenes.example.json` — sample scene spec.
- `prompts/key-visual-style.md` — reusable image prompt style clause.
- `scripts/render_short_v3.py` — renderer template from the sample.
- `examples/ai-tool-calling/` — sample narration and QA report.
