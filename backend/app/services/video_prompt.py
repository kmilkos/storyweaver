from app.config import get_env


def generate_video_prompt(
    narration: str,
    image_prompt: str,
    character_names: list[str],
    character_descriptions: list[str],
    camera_motion: str,
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

Scene narration:
{narration}

Visual description / image prompt:
{image_prompt}

Characters in this scene:
{chars_block}

Camera motion: {camera_motion}

Return ONLY the prompt text, no markdown, no code fences, no extra commentary."""

    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
    )
    return response.text.strip()
