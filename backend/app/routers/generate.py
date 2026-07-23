from __future__ import annotations

from datetime import datetime
from pathlib import Path
from uuid import uuid4

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.config import PROJECTS_DIR
from app.db.json_db import save_project
from app.models.project import AspectRatio, CompileMode, Project
from app.services.story_generator import generate_story

router = APIRouter(prefix="/api/generate", tags=["generate"])


class GenerateRequest(BaseModel):
    theme: str
    target_seconds: int = 60
    aspect_ratio: AspectRatio = AspectRatio.landscape
    compile_mode: CompileMode = CompileMode.slideshow


@router.post("/story", status_code=201)
def api_generate_story(body: GenerateRequest):
    if not body.theme.strip():
        raise HTTPException(400, "Theme is required")

    slug = f"{body.theme.lower().replace(' ', '-')[:48]}-{uuid4().hex[:6]}"

    try:
        result = generate_story(
            theme=body.theme,
            target_seconds=body.target_seconds,
            aspect_ratio=body.aspect_ratio.value,
            compile_mode=body.compile_mode.value,
        )
    except ValueError as e:
        raise HTTPException(502, str(e))

    title = result.get("title", body.theme[:48])
    scenes_data = result.get("scenes", [])

    full_text = f"# {title}\n\n"
    for scene in scenes_data:
        full_text += f"Scene {scene.get('order', 1)}:\n{scene.get('narration', '')}\n\n"

    project_dir = PROJECTS_DIR / slug
    project_dir.mkdir(parents=True, exist_ok=True)
    (project_dir / "characters").mkdir(exist_ok=True)
    (project_dir / "scenes").mkdir(exist_ok=True)
    (project_dir / "audio").mkdir(exist_ok=True)
    (project_dir / "exports").mkdir(exist_ok=True)

    file_path = project_dir / "generated_story.txt"
    file_path.write_text(full_text)

    project = Project(
        title=title,
        slug=slug,
        aspect_ratio=body.aspect_ratio,
        compile_mode=body.compile_mode,
    )
    save_project(project)

    return {
        "project": project,
        "scenes_count": len(scenes_data),
    }
