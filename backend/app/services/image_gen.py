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
        if candidate.finish_reason and candidate.finish_reason != 1:
            reason = getattr(candidate, "finish_reason", "unknown")
            raise ValueError(f"Gemini blocked the request (finish_reason={reason}). Try a different prompt.")
        if not candidate.content:
            continue
        for part in candidate.content.parts:
            if part.inline_data and part.inline_data.mime_type.startswith("image/"):
                output_path.write_bytes(part.inline_data.data)
                return str(output_path)

    raise ValueError("Gemini returned no image data in the response. The prompt may have been blocked by safety filters.")


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
