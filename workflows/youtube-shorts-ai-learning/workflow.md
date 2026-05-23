# AI Tools Learning Shorts Workflow

Goal: turn any AI concept into a globally understandable YouTube Short: researched, fact-checked, simple for non-developers, narrated with local Supertonic 3 English female voice, rendered as a 9:16 video, then uploaded after explicit approval.

## Default format

- Audience: non-developer, global English audience
- Length: 35-55 seconds
- Aspect ratio: 1080x1920 vertical
- Style: fast, clear, metaphor-first, no jargon unless immediately explained
- Voice: Supertonic 3 `F1` Mina by default, English, local generation
- Video: big captions, 5-8 visual beats, one key idea per scene
- Upload: never upload without explicit final approval

## One-concept production loop

1. Receive concept
   - Example: "tool calling", "RAG", "MCP", "AI agents", "function calling".
   - If no concept is provided, use a safe sample topic: "AI tool calling".

2. Research for accuracy
   - Prefer official docs first.
   - Minimum source mix:
     - 1 official vendor doc
     - 1 second authoritative source or competing vendor doc
     - optional: paper/blog only if needed
   - Extract only stable claims: definitions, workflow, limitations, and best practices.

3. Fact-check digest
   - Write 3-5 factual bullets.
   - Mark any claim as:
     - `verified` if directly supported by sources
     - `simplified` if made easier for the audience but still true
     - `avoid` if too nuanced or likely to mislead in a Short

4. Script
   - Use this structure:
     - 0-3s Hook: surprising analogy or problem
     - 3-12s Definition: one plain-language sentence
     - 12-30s Example: everyday analogy
     - 30-42s Safety/limitation: what it cannot do alone
     - 42-55s Takeaway: one sentence people remember
   - Reading level: middle-school-friendly English.
   - Avoid acronyms unless explained.

5. Verification pass
   - Check every technical claim against the research notes.
   - Remove hype like "the AI does everything".
   - Ensure the model/tool boundary is clear: the model requests; software executes.

6. Generate narration locally
   - Use the cloned CLI:
     ```bash
     cd /Users/danny/ai-shorts-workflow/supertonic-tts
     node bin/supertonic.mjs -f ../episodes/<slug>/script/narration.txt \
       -o ../episodes/<slug>/audio/narration.wav \
       --lang en --voice F1 --speed 1.08 --steps 8 --no-play
     ```

7. Premium visual generation
   - Do not rely on cheap SVG-only scenes for 9/10 work.
   - Build a 6-8 shot storyboard first: exact narration line, caption, key visual prompt, camera move, transition.
   - Generate consistent cinematic key visuals with Codex/Gemini Nano Banana image generation when available.
   - Avoid text inside generated images; all readable text should be added by the renderer.

8. Render video
   - Preferred v3 renderer: `scripts/render_short_v3.py`.
   - Use image-based cinematic scenes, subtle push-in/pull-out motion, burned-in captions, and exact per-scene Supertonic audio timings.
   - Keep subtitles large enough for phone viewing.

9. QA checklist / quality gate
   - ffprobe confirms: 1080x1920, h264, aac, duration < 60s.
   - Extract 5-8 preview frames and make a contact sheet.
   - Captions readable on phone size; no overflow or clipping.
   - Generated images contain no unwanted words, watermarks, malformed UI, or broken faces/hands.
   - Voice line, caption, and visual meaning must match scene by scene.
   - Internal score target before upload: visual polish 8.5+, voice/content sync 9+, non-dev clarity 9+, retention 8.5+, cheap-AI look low.

10. Upload
   - YouTube upload requires YouTube Data API OAuth setup or an already-authenticated uploader.
   - Google Drive review upload can use `gws drive files create --upload ...` when authenticated.
   - External upload is a side effect: only upload after user approval or an explicit active task to upload.
   - Suggested YouTube privacy for first pass: `unlisted`.

## Files per episode

```text
episodes/<slug>/
  research/notes.md
  script/narration.txt
  script/scenes.json
  audio/narration.wav
  video/final.mp4
  metadata/youtube.json
```

## Reusable prompt for future concepts

"Create a YouTube Short for a global non-developer audience about: <CONCEPT>. Research official sources, verify claims, simplify without misleading, write a 35-55 second English script, generate Supertonic 3 F1 narration locally, render a 1080x1920 video with large captions, then show me the file. Do not upload until I approve."
