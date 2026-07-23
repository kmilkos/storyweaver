from __future__ import annotations

from fastapi import APIRouter, HTTPException

from app.config import PROJECTS_DIR
from app.db.json_db import (
    get_character,
    get_project,
    list_characters,
    list_scenes,
    save_project,
    save_scene,
)
from app.models.project import ProjectStatus
from app.models.scene import CameraMotion, Scene, SceneStatus, SceneUpdate
from app.services.extractor import split_scenes
from app.services.parser import extract_text

router = APIRouter(prefix="/api/projects", tags=["scenes"])


@router.get("/{project_id}/scenes")
def api_list_scenes(project_id: str, chapter_id: str | None = None):
    return list_scenes(project_id=project_id, chapter_id=chapter_id)


@router.get("/{project_id}/scenes/{scene_id}")
def api_get_scene(project_id: str, scene_id: str):
    from app.db.json_db import get_scene

    scene = get_scene(scene_id)
    if not scene or scene.project_id != project_id:
        raise HTTPException(404, "Scene not found")
    return scene


@router.put("/{project_id}/scenes/{scene_id}")
def api_update_scene(project_id: str, scene_id: str, body: SceneUpdate):
    from app.db.json_db import get_scene

    scene = get_scene(scene_id)
    if not scene or scene.project_id != project_id:
        raise HTTPException(404, "Scene not found")

    if body.narration is not None:
        scene.narration = body.narration
    if body.image_prompt is not None:
        scene.image_prompt = body.image_prompt
    if body.voice_id is not None:
        scene.voice_id = body.voice_id
    if body.camera_motion is not None:
        scene.camera_motion = body.camera_motion
    if body.character_ids is not None:
        scene.character_ids = body.character_ids
    if body.video_path is not None:
        scene.video_path = body.video_path

    save_scene(scene)
    return scene


@router.post("/{project_id}/scenes/split")
def api_split_scenes(project_id: str, chapter_id: str | None = None):
    project = get_project(project_id)
    if not project:
        raise HTTPException(404, "Project not found")

    project_dir = PROJECTS_DIR / project.slug
    files = list(project_dir.glob("*.txt")) + list(project_dir.glob("*.pdf"))
    if not files:
        raise HTTPException(400, "No source file found.")

    text = extract_text(files[0])
    characters = list_characters(project_id)
    char_dicts = [
        {"name": c.name, "description": c.description} for c in characters
    ]

    try:
        scene_proposals = split_scenes(text, char_dicts)
    except ValueError as e:
        raise HTTPException(400, str(e))

    char_name_map = {c.name: c.id for c in characters}

    scenes = []
    for i, sp in enumerate(scene_proposals):
        char_ids = [
            char_name_map.get(n, "")
            for n in sp.get("character_names", [])
            if char_name_map.get(n, "")
        ]

        scene = Scene(
            project_id=project_id,
            chapter_id=chapter_id or project.chapters[0].id if project.chapters else "",
            order=i + 1,
            narration=sp.get("narration", ""),
            image_prompt=sp.get("image_prompt", ""),
            character_ids=char_ids,
            camera_motion=CameraMotion.slow_zoom,
            voice_id="kore",
            status=SceneStatus.draft,
        )
        save_scene(scene)
        scenes.append(scene)

    if not project.chapters and scenes:
        from app.models.project import Chapter

        chapter = Chapter(title="Chapter 1", order=1)
        project.chapters.append(chapter)
        for s in scenes:
            s.chapter_id = chapter.id
            save_scene(s)

    project.status = ProjectStatus.scenes_split
    save_project(project)

    return scenes
