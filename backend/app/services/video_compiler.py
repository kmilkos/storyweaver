from __future__ import annotations

from pathlib import Path

from moviepy import (
    AudioFileClip,
    ImageClip,
    concatenate_videoclips,
)
from moviepy.video.fx import Resize, Scroll


def compile_video(
    scenes: list[dict],
    output_path: Path,
    fps: int = 24,
    resolution: tuple[int, int] = (1920, 1080),
) -> str:
    clips = []
    for scene in scenes:
        img_path = scene.get("image_path", "")
        audio_path = scene.get("audio_path", "")

        if not img_path or not Path(img_path).exists():
            continue

        duration = _get_duration(audio_path)
        img_clip = ImageClip(str(img_path), duration=duration)

        img_clip = img_clip.resized(new_size=resolution)

        camera = scene.get("camera_motion", "slow-zoom")
        img_clip = _apply_motion(img_clip, camera)

        if audio_path and Path(audio_path).exists():
            audio = AudioFileClip(str(audio_path))
            img_clip = img_clip.with_audio(audio)

        clips.append(img_clip)

    if not clips:
        raise ValueError("No valid scenes to compile")

    final = concatenate_videoclips(clips, method="compose")

    final.write_videofile(
        str(output_path),
        fps=fps,
        codec="libx264",
        audio_codec="aac",
        preset="ultrafast",
        logger=None,
    )

    return str(output_path)


def compile_preview(
    scenes: list[dict],
    output_path: Path,
    max_scenes: int = 3,
    resolution: tuple[int, int] = (1920, 1080),
) -> str:
    return compile_video(
        scenes[:max_scenes],
        output_path,
        fps=24,
        resolution=resolution,
    )


def _get_duration(audio_path: str) -> float:
    if not audio_path or not Path(audio_path).exists():
        return 5.0
    try:
        return AudioFileClip(str(audio_path)).duration
    except Exception:
        return 5.0


def _apply_motion(clip: ImageClip, motion: str) -> ImageClip:
    duration = clip.duration
    if motion == "slow-zoom":
        return clip.with_effects([
            Resize(lambda t: 1.0 + 0.08 * (t / duration)),
        ])
    elif motion == "slow-pan":
        return clip.with_effects([
            Scroll(x_speed=100, y_speed=0),
        ])
    elif motion == "dolly":
        return clip.with_effects([
            Resize(lambda t: 1.0 + 0.12 * (t / duration)),
        ])
    return clip
