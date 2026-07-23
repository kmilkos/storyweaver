from __future__ import annotations

from fastapi import APIRouter, HTTPException

from app.config import PROJECTS_DIR
from app.db.json_db import get_project, get_scene, save_scene
from app.models.scene import SceneStatus
from app.services.image_gen import generate_image
from app.services.prompt_gen import generate_image_prompt

router = APIRouter(prefix="/api/projects", tags=["images"])


@router.post("/{project_id}/scenes/{scene_id}/generate-image")
def api_generate_image(project_id: str, scene_id: str):
    project = get_project(project_id)
    if not project:
        raise HTTPException(404, "Project not found")

    scene = get_scene(scene_id)
    if not scene or scene.project_id != project_id:
        raise HTTPException(404, "Scene not found")

    prompt = scene.image_prompt
    if not prompt:
        raise HTTPException(400, "Scene has no image prompt. Split scenes first.")

    project_dir = PROJECTS_DIR / project.slug
    project_dir.mkdir(parents=True, exist_ok=True)
    (project_dir / "scenes").mkdir(exist_ok=True)

    output_path = project_dir / "scenes" / f"scene_{scene.order:03d}.png"

    try:
        generate_image(prompt, output_path)
    except ValueError as e:
        raise HTTPException(400, str(e))

    image_url = f"/projects/{project.slug}/scenes/{output_path.name}"
    scene.image_path = image_url
    scene.status = SceneStatus.image_generated
    save_scene(scene)

    return {"image_path": image_url, "status": scene.status.value}


@router.post("/{project_id}/scenes/{scene_id}/generate-image-prompt")
def api_generate_image_prompt(project_id: str, scene_id: str):
    project = get_project(project_id)
    if not project:
        raise HTTPException(404, "Project not found")

    scene = get_scene(scene_id)
    if not scene or scene.project_id != project_id:
        raise HTTPException(404, "Scene not found")

    if not scene.narration:
        raise HTTPException(400, "Scene has no narration.")

    try:
        new_prompt = generate_image_prompt(
            narration=scene.narration,
            existing_prompt=scene.image_prompt,
        )
    except ValueError as e:
        raise HTTPException(502, str(e))

    scene.image_prompt = new_prompt
    save_scene(scene)

    return {"image_prompt": new_prompt}
