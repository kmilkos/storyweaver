from __future__ import annotations

from pathlib import Path

from fastapi import APIRouter, HTTPException, UploadFile

from app.config import PROJECTS_DIR
from app.db.json_db import (
    get_character,
    get_project,
    get_scene,
    list_characters,
    save_scene,
)
from app.models.scene import SceneStatus
from app.services.video_prompt import generate_video_prompt

router = APIRouter(prefix="/api/projects", tags=["video"])


@router.post("/{project_id}/scenes/{scene_id}/generate-video-prompt")
def api_generate_video_prompt(project_id: str, scene_id: str):
    project = get_project(project_id)
    if not project:
        raise HTTPException(404, "Project not found")

    scene = get_scene(scene_id)
    if not scene or scene.project_id != project_id:
        raise HTTPException(404, "Scene not found")

    characters = list_characters(project_id)
    char_map = {c.id: c for c in characters}

    char_names = []
    char_descs = []
    for cid in scene.character_ids:
        c = char_map.get(cid)
        if c:
            char_names.append(c.name)
            char_descs.append(c.description or "No description")

    try:
        prompt = generate_video_prompt(
            narration=scene.narration,
            image_prompt=scene.image_prompt,
            character_names=char_names,
            character_descriptions=char_descs,
            camera_motion=scene.camera_motion.value,
        )
    except ValueError as e:
        raise HTTPException(400, str(e))

    scene.video_prompt = prompt
    scene.status = SceneStatus.prompt_generated
    save_scene(scene)

    return {"video_prompt": prompt, "status": scene.status.value}


@router.post("/{project_id}/scenes/{scene_id}/upload-video")
async def api_upload_video(project_id: str, scene_id: str, file: UploadFile):
    project = get_project(project_id)
    if not project:
        raise HTTPException(404, "Project not found")

    scene = get_scene(scene_id)
    if not scene or scene.project_id != project_id:
        raise HTTPException(404, "Scene not found")

    if not file.content_type or not file.content_type.startswith("video/"):
        raise HTTPException(400, "Only video files are accepted")

    project_dir = PROJECTS_DIR / project.slug
    (project_dir / "videos").mkdir(parents=True, exist_ok=True)

    ext = Path(file.filename or "video.mp4").suffix or ".mp4"
    output_path = project_dir / "videos" / f"scene_{scene.order:03d}{ext}"

    content = await file.read()
    output_path.write_bytes(content)

    video_url = f"/projects/{project.slug}/videos/{output_path.name}"
    scene.video_path = video_url
    scene.status = SceneStatus.video_generated
    save_scene(scene)

    return {"video_path": video_url, "status": scene.status.value}
