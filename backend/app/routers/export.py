from __future__ import annotations

from pathlib import Path

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse

from app.config import PROJECTS_DIR
from app.db.json_db import get_project, list_scenes
from app.models.scene import SceneStatus
from app.services.video_compiler import compile_preview, compile_video

router = APIRouter(prefix="/api/projects", tags=["export"])


@router.post("/{project_id}/export/preview")
def api_export_preview(project_id: str):
    project = get_project(project_id)
    if not project:
        raise HTTPException(404, "Project not found")

    scenes = list_scenes(project_id=project_id)
    ready = [s for s in scenes if s.status != SceneStatus.draft]

    if not ready:
        raise HTTPException(400, "No scenes with generated assets. Generate images/audio first.")

    project_dir = PROJECTS_DIR / project.slug
    project_dir.mkdir(parents=True, exist_ok=True)
    (project_dir / "exports").mkdir(exist_ok=True)

    output_path = project_dir / "exports" / "preview.mp4"
    scene_dicts = [
        {
            "image_path": s.image_path,
            "audio_path": s.audio_path,
            "camera_motion": s.camera_motion.value,
        }
        for s in ready
    ]

    try:
        compile_preview(scene_dicts, output_path, max_scenes=3)
    except ValueError as e:
        raise HTTPException(400, str(e))

    return {"video_path": str(output_path), "url": f"/projects/{project.slug}/exports/preview.mp4"}


@router.post("/{project_id}/export/compile")
def api_export_full(project_id: str):
    project = get_project(project_id)
    if not project:
        raise HTTPException(404, "Project not found")

    scenes = list_scenes(project_id=project_id)
    ready = [s for s in scenes if s.status != SceneStatus.draft]

    if not ready:
        raise HTTPException(400, "No scenes with generated assets.")

    project_dir = PROJECTS_DIR / project.slug
    project_dir.mkdir(parents=True, exist_ok=True)
    (project_dir / "exports").mkdir(exist_ok=True)

    output_path = project_dir / "exports" / f"{project.slug}_full.mp4"
    scene_dicts = [
        {
            "image_path": s.image_path,
            "audio_path": s.audio_path,
            "camera_motion": s.camera_motion.value,
        }
        for s in ready
    ]

    try:
        compile_video(scene_dicts, output_path)
    except ValueError as e:
        raise HTTPException(400, str(e))

    return {"video_path": str(output_path), "url": f"/projects/{project.slug}/exports/{project.slug}_full.mp4"}


@router.get("/{project_id}/export/download")
def api_download_export(project_id: str):
    project = get_project(project_id)
    if not project:
        raise HTTPException(404, "Project not found")

    project_dir = PROJECTS_DIR / project.slug
    output_path = project_dir / "exports" / f"{project.slug}_full.mp4"

    if not output_path.exists():
        raise HTTPException(404, "No compiled video found. Run compile first.")

    return FileResponse(
        str(output_path),
        media_type="video/mp4",
        filename=f"{project.slug}.mp4",
    )


@router.get("/{project_id}/export/status")
def api_export_status(project_id: str):
    project = get_project(project_id)
    if not project:
        raise HTTPException(404, "Project not found")

    scenes = list_scenes(project_id=project_id)
    total = len(scenes)
    with_image = sum(1 for s in scenes if s.status in (
        SceneStatus.image_generated, SceneStatus.audio_generated, SceneStatus.complete
    ))
    with_audio = sum(1 for s in scenes if s.status in (
        SceneStatus.audio_generated, SceneStatus.complete
    ))

    project_dir = PROJECTS_DIR / project.slug
    compiled = (project_dir / "exports" / f"{project.slug}_full.mp4").exists()

    return {
        "total_scenes": total,
        "images_generated": with_image,
        "audio_generated": with_audio,
        "compiled": compiled,
    }
