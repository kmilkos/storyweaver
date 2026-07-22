from __future__ import annotations

from pathlib import Path

from app.config import VOICES_DIR

VOICES = [
    {"id": "kore", "name": "Kore", "gender": "Female", "style": "Warm, narrative", "source": "Gemini"},
    {"id": "puck", "name": "Puck", "gender": "Male", "style": "Energetic, bright", "source": "Gemini"},
    {"id": "charon", "name": "Charon", "gender": "Male", "style": "Deep, dramatic", "source": "Gemini"},
    {"id": "fenrir", "name": "Fenrir", "gender": "Male", "style": "Gruff, authoritative", "source": "Gemini"},
    {"id": "zephyr", "name": "Zephyr", "gender": "Neutral", "style": "Soft, atmospheric", "source": "Gemini"},
    {"id": "edge-en-US-JennyNeural", "name": "Jenny", "gender": "Female", "style": "Natural, US", "source": "Edge-TTS"},
    {"id": "edge-en-US-GuyNeural", "name": "Guy", "gender": "Male", "style": "Natural, US", "source": "Edge-TTS"},
    {"id": "edge-en-GB-SoniaNeural", "name": "Sonia", "gender": "Female", "style": "British", "source": "Edge-TTS"},
]


def list_voices() -> list[dict]:
    result = []
    for v in VOICES:
        sample_path = VOICES_DIR / f"{v['id']}.mp3"
        result.append({
            **v,
            "sample_url": f"/voices/{v['id']}.mp3" if sample_path.exists() else "",
        })
    return result


async def generate_speech(text: str, voice_id: str, output_path: Path) -> str:
    if voice_id.startswith("edge-"):
        return await _generate_edge_tts(text, voice_id, output_path)
    return await _generate_gemini_tts(text, voice_id, output_path)


async def _generate_gemini_tts(text: str, voice_id: str, output_path: Path) -> str:
    from app.config import get_env
    from google import genai

    api_key = get_env("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=text,
        config={
            "speech_config": {
                "voice_config": {
                    "prebuilt_voice_config": {
                        "voice_name": voice_id,
                    }
                }
            }
        },
    )
    audio_data = response.data
    if audio_data:
        output_path.write_bytes(audio_data)
    return str(output_path)


async def _generate_edge_tts(text: str, voice_id: str, output_path: Path) -> str:
    import edge_tts

    voice_name = voice_id.replace("edge-", "")
    communicate = edge_tts.Communicate(text, voice_name)
    await communicate.save(str(output_path))
    return str(output_path)
