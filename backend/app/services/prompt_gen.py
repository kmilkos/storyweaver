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
    return response.text.strip()


def generate_image_prompt(narration: str, existing_prompt: str = "") -> str:
    prompt = f"""You are a prompt engineer for AI image generation. Rewrite the following image prompt to be safe and effective.

Rules:
- Do NOT use real celebrity names, public figures, brand names, or copyrighted characters
- Describe people by their appearance and role instead of names
- Keep the visual style: cinematic, 16:9 aspect ratio, epic, detailed
- Return ONLY the rewritten prompt, no explanations or markdown

Scene narration:
{narration}

"""
    if existing_prompt:
        prompt += f"Original prompt (rewrite this to be safe):\n{existing_prompt}\n"
    else:
        prompt += "Generate a vivid image prompt based on this narration.\n"

    result = _call_gemini(prompt)
    result = result.removeprefix("```").removeprefix("json").removesuffix("```").strip()
    return result
