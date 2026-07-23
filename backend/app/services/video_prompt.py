import json
import re

from app.config import get_env


def _call_gemini(prompt: str) -> str:
    from google import genai

    api_key = get_env("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
    )
    return response.text.strip()


def _check_names_safe(names: list[str], narration: str) -> list[str]:
    names_list = "\n".join(f"- {n}" for n in names)
    check_prompt = f"""You are a content policy checker for AI video generation (Veo).
Given a list of character names and the scene narration, determine if using these
names directly in a video prompt could trigger Veo's "identifiable individuals" policy.
This policy typically blocks real public figures, celebrities, or well-known people.
Fictional character names and generic names are usually safe.

Names:
{names_list}

Scene narration:
{narration[:500]}

Return a JSON object with key "safe_names" containing only the names that are safe to use,
and key "unsafe_names" containing names that should be replaced with role descriptions.
Example: {{"safe_names": ["Dick Jarvis"], "unsafe_names": ["Elon Musk"]}}
Return ONLY valid JSON, no markdown, no code fences."""

    try:
        raw = _call_gemini(check_prompt)
        raw = re.sub(r'```(?:json)?\s*|\s*```', '', raw).strip()
        result = json.loads(raw)
        return result.get("safe_names", names)
    except (json.JSONDecodeError, KeyError):
        return names


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

    safe_names = _check_names_safe(character_names, narration)

    name_role_map = {n: desc for n, desc in zip(character_names, character_descriptions)}
    role_notes = []
    for name in character_names:
        if name in safe_names:
            role_notes.append(f"- {name}: {name_role_map.get(name, '')}")
        else:
            role_notes.append(f"- DO NOT USE THE NAME. Refer to them as: {name_role_map.get(name, 'a character')}")

    chars_block = "\n".join(role_notes) or "No characters defined."

    prompt_text = f"""You are an expert video prompt writer for AI video generation (Veo, Sora, etc.).
Given a scene's details, produce a single rich video generation prompt.
It must describe the visual scene, character actions, and camera motion.
It MUST also include the exact narration/dialogue text that will be spoken,
tagged as [NARRATION: ...] at the end of the prompt.

For characters marked "DO NOT USE THE NAME", you MUST refer to them by their
role/description instead (e.g. "the astronaut"). For other characters you may
use their name directly.

Target video duration: {target_seconds} seconds.
The [NARRATION: ...] text MUST be speakable within {target_seconds} seconds
(approximately {int(target_seconds * 2.5)} words max at a normal pace).
If the provided narration is too long, condense it to fit the time limit
while preserving the core meaning and dialogue.

Characters:
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
        contents=prompt_text,
    )
    text = response.text.strip()

    return text
