from __future__ import annotations

import json
import re

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


def extract_characters(text: str) -> list[dict]:
    prompt = f"""You are a literary analyst. Extract all named characters from the following text.
For each character, provide:
- name: full name
- description: 1-2 sentence physical/personality description
- role: protagonist / antagonist / supporting / minor

Return ONLY a JSON array of objects with keys: name, description, role.
No markdown, no code fences, just raw JSON.

TEXT:
{text[:8000]}"""

    raw = _call_gemini(prompt)
    raw = _clean_json(raw)

    try:
        chars = json.loads(raw)
        if isinstance(chars, dict) and "characters" in chars:
            chars = chars["characters"]
        return chars if isinstance(chars, list) else []
    except json.JSONDecodeError:
        return []


def split_scenes(chapter_text: str, characters: list[dict]) -> list[dict]:
    char_list = "\n".join(
        f"- {c['name']}: {c.get('description', '')}" for c in characters
    )

    prompt = f"""You are a screenwriter. Break the following chapter text into visual scenes.
For each scene provide:
- narration: 2-4 sentences of voiceover narration (present tense, vivid)
- image_prompt: a detailed visual prompt for generating an image (include character appearances, setting, lighting, mood, style — cinematic)
- character_names: list of character names appearing in this scene

Rules:
- Each scene should be a single location/moment
- Make narration conversational and suitable for voiceover
- Image prompts must be safe for AI image generation — do NOT use real celebrity names, public figures, brand names, or copyrighted characters. Describe people by their appearance and role instead.
- Image prompts: 16:9 cinematic, epic, detailed
- Return ONLY a JSON array of objects with keys: narration, image_prompt, character_names
- No markdown, no code fences, just raw JSON

Characters in this story:
{char_list}

CHAPTER TEXT:
{chapter_text[:10000]}"""

    raw = _call_gemini(prompt)
    raw = _clean_json(raw)

    try:
        scenes = json.loads(raw)
        if isinstance(scenes, dict) and "scenes" in scenes:
            scenes = scenes["scenes"]
        return scenes if isinstance(scenes, list) else []
    except json.JSONDecodeError:
        return []


def _clean_json(text: str) -> str:
    text = re.sub(r"```(?:json)?", "", text).strip()
    start = text.find("[")
    end = text.rfind("]")
    if start != -1 and end != -1:
        text = text[start : end + 1]
    return text
