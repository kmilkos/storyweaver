import re

from app.config import get_env


def generate_video_prompt(
    narration: str,
    image_prompt: str,
    character_names: list[str],
    character_descriptions: list[str],
    camera_motion: str,
    target_seconds: int = 10,
) -> str:
    api_key = get_env("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY not configured")

    from google import genai

    chars_block = "\n".join(
        f"- {name}: {desc}"
        for name, desc in zip(character_names, character_descriptions)
    ) or "No characters defined."

    prompt = f"""You are an expert video prompt writer for AI video generation (Veo, Sora, etc.).
Given a scene's details, produce a single rich video generation prompt.
It must describe the visual scene, character actions, and camera motion.
It MUST also include the exact narration/dialogue text that will be spoken,
tagged as [NARRATION: ...] at the end of the prompt.
IMPORTANT: Do NOT use character names directly. Instead, refer to each character
by their role or a descriptive phrase (e.g. "the astronaut", "the captain",
"the chemist", "the engineer"). This avoids content policy restrictions.

Target video duration: {target_seconds} seconds.
The [NARRATION: ...] text MUST be speakable within {target_seconds} seconds
(approximately {int(target_seconds * 2.5)} words max at a normal pace).
If the provided narration is too long, condense it to fit the time limit
while preserving the core meaning and dialogue.

Characters (use their roles, not names):
{chars_block}

Scene narration:
{narration}

Visual description / image prompt:
{image_prompt}

Camera motion: {camera_motion}

Return ONLY the prompt text, no markdown, no code fences, no extra commentary."""

    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
    )
    text = response.text.strip()

    for name in sorted(character_names, key=len, reverse=True):
        text = text.replace(f"@{name}", name)

    return text
