from __future__ import annotations

from pathlib import Path

from app.config import get_env


def generate_image(prompt: str, output_path: Path, width: int = 1920, height: int = 1080) -> str:
    gemini_key = get_env("GEMINI_API_KEY")
    stability_key = get_env("STABILITY_API_KEY")

    if gemini_key:
        try:
            return _generate_gemini(prompt, output_path)
        except Exception as e:
            raise ValueError(f"Gemini image generation failed: {e}")

    if stability_key:
        return _generate_stability(prompt, output_path, width, height)

    raise ValueError(
        "No image generation API configured. Set GEMINI_API_KEY or STABILITY_API_KEY."
    )


def _generate_gemini(prompt: str, output_path: Path) -> str:
    from google import genai
    from google.genai import types

    api_key = get_env("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    response = client.models.generate_content(
        model="gemini-2.5-flash-image",
        contents=prompt,
        config=types.GenerateContentConfig(
            response_modalities=["Text", "Image"],
        ),
    )

    if not response.candidates:
        raise ValueError("Gemini returned no candidates. The prompt may have been blocked.")

    for candidate in response.candidates:
        reason = candidate.finish_reason
        if reason and str(reason) != "FinishReason.STOP":
            hints = {
                "IMAGE_SAFETY": "The image was blocked by safety filters.",
                "IMAGE_PROHIBITED_CONTENT": "The image was blocked: prohibited content detected.",
                "IMAGE_RECITATION": "The image may resemble copyrighted material.",
                "IMAGE_OTHER": "Gemini's image model rejected this prompt.",
                "SAFETY": "The prompt was blocked by safety filters.",
                "PROHIBITED_CONTENT": "The prompt contains prohibited content.",
                "RECITATION": "The prompt resembles copyrighted material.",
            }
            hint = hints.get(str(reason).replace("FinishReason.", ""), "")
            raise ValueError(
                f"Gemini blocked this prompt (reason: {reason}). "
                f"{hint} Try rewording to avoid real names, brands, or copyrighted content."
            )
        if not candidate.content:
            continue
        for part in candidate.content.parts:
            if part.inline_data and part.inline_data.mime_type.startswith("image/"):
                output_path.write_bytes(part.inline_data.data)
                return str(output_path)

    raise ValueError("Gemini returned no image data in the response.")


def _generate_stability(prompt: str, output_path: Path, width: int, height: int) -> str:
    import httpx

    api_key = get_env("STABILITY_API_KEY")
    response = httpx.post(
        "https://api.stability.ai/v2beta/stable-image/generate/sd3",
        headers={
            "authorization": f"Bearer {api_key}",
            "accept": "image/*",
        },
        files={"none": ""},
        data={
            "prompt": prompt,
            "output_format": "png",
            "width": width,
            "height": height,
            "seed": 0,
        },
    )
    if response.status_code != 200:
        raise ValueError(f"Stability API error: {response.text}")
    output_path.write_bytes(response.content)
    return str(output_path)
