from __future__ import annotations

from app.config import get_env


def _call_gemini(prompt: str) -> str:
    api_key = get_env("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY not configured")
    from google import genai
    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
    )
    return response.text


def generate_story(
    theme: str,
    target_seconds: int,
    aspect_ratio: str = "16:9",
    compile_mode: str = "slideshow",
) -> dict:
    scenes_count = max(3, target_seconds // 12)

    prompt = f"""You are a creative writer. Write a short, vivid story based on the following theme.

Theme: {theme}
Target video length: {target_seconds} seconds
Aspect ratio: {aspect_ratio}
Compile mode: {compile_mode}

Guidelines:
- The story must be self-contained and complete.
- Narrate at approximately 2.5 words per second (max {int(target_seconds * 2.5)} words total).
- Divide the story into exactly {scenes_count} clearly separated scenes.
- Each scene should have a distinct setting, visual moment, or narrative beat.
- Write in a style that is easy to narrate and visualize.

Return ONLY valid JSON with this exact structure:
{{
  "title": "A short story title",
  "scenes": [
    {{
      "order": 1,
      "narration": "Narration text for scene 1. This should be vivid and descriptive, around 30 words.",
      "image_description": "A detailed visual description of what this scene looks like, for image generation."
    }}
  ]
}}

No markdown, no code fences, just raw JSON."""
    raw = _call_gemini(prompt)
    import json, re
    match = re.search(r"\{.*\}", raw, re.DOTALL)
    if match:
        raw = match.group()
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        raise ValueError(f"Failed to parse story JSON from Gemini response: {raw[:500]}")

    if "title" not in data:
        data["title"] = theme[:48]
    return data
