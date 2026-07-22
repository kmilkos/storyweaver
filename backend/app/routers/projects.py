from __future__ import annotations

from pathlib import Path
from uuid import uuid4

from fastapi import APIRouter, HTTPException, UploadFile

from app.config import PROJECTS_DIR
from app.db.json_db import (
    delete_project,
    get_project,
    list_projects,
    save_project,
)
from app.models.project import (
    Chapter,
    Project,
    ProjectCreate,
    ProjectSummary,
    ProjectStatus,
)
from app.services.parser import extract_text, guess_title_from_filename

router = APIRouter(prefix="/api/projects", tags=["projects"])


@router.get("")
def api_list_projects():
    projects = list_projects()
    return [
        ProjectSummary(
            id=p.id,
            title=p.title,
            author=p.author,
            status=p.status,
            chapter_count=len(p.chapters),
            character_count=len(p.character_ids),
            created_at=p.created_at,
        )
        for p in projects
    ]


@router.post("", status_code=201)
def api_create_project(body: ProjectCreate):
    slug = body.title.lower().replace(" ", "-").replace("/", "-")[:48]
    project = Project(title=body.title, author=body.author, slug=slug)
    save_project(project)

    project_dir = PROJECTS_DIR / slug
    project_dir.mkdir(parents=True, exist_ok=True)
    (project_dir / "characters").mkdir(exist_ok=True)
    (project_dir / "scenes").mkdir(exist_ok=True)
    (project_dir / "audio").mkdir(exist_ok=True)
    (project_dir / "exports").mkdir(exist_ok=True)

    return project


@router.get("/{project_id}")
def api_get_project(project_id: str):
    project = get_project(project_id)
    if not project:
        raise HTTPException(404, "Project not found")
    return project


@router.delete("/{project_id}")
def api_delete_project(project_id: str):
    if not delete_project(project_id):
        raise HTTPException(404, "Project not found")
    return {"ok": True}


@router.post("/upload", status_code=201)
async def api_upload_project(file: UploadFile):
    ext = Path(file.filename or "file.txt").suffix.lower()
    if ext not in (".txt", ".pdf"):
        raise HTTPException(400, "Only .txt and .pdf files are supported")

    title = guess_title_from_filename(file.filename or "Untitled")
    slug = f"{title.lower().replace(' ', '-')[:48]}-{uuid4().hex[:6]}"

    project_dir = PROJECTS_DIR / slug
    project_dir.mkdir(parents=True, exist_ok=True)

    file_path = project_dir / (file.filename or "upload.txt")
    content = await file.read()
    file_path.write_bytes(content)

    project = Project(title=title, slug=slug)
    save_project(project)

    (project_dir / "characters").mkdir(exist_ok=True)
    (project_dir / "scenes").mkdir(exist_ok=True)
    (project_dir / "audio").mkdir(exist_ok=True)
    (project_dir / "exports").mkdir(exist_ok=True)

    return project
