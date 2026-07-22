from __future__ import annotations

from pathlib import Path

from app.config import get_env


def generate_image(prompt: str, output_path: Path, width: int = 1920, height: int = 1080) -> str:
    stability_key = get_env("STABILITY_API_KEY")
    gemini_key = get_env("GEMINI_API_KEY")

    if stability_key:
        return _generate_stability(prompt, output_path, width, height)

    if gemini_key:
        try:
            return _generate_imagen(prompt, output_path)
        except Exception:
            pass

    raise ValueError(
        "No image generation API configured. Set STABILITY_API_KEY or GEMINI_API_KEY."
    )


def _generate_imagen(prompt: str, output_path: Path) -> str:
    from google import genai

    api_key = get_env("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    response = client.models.generate_images(
        model="imagen-3.0-generate-002",
        prompt=prompt,
        config={"number_of_images": 1},
    )
    image_data = response.data[0].image_bytes
    output_path.write_bytes(image_data)
    return str(output_path)


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
