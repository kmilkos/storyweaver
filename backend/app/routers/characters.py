from __future__ import annotations

from fastapi import APIRouter, HTTPException

from app.db.json_db import (
    delete_character,
    get_character,
    get_project,
    list_characters,
    save_character,
    save_project,
)
from app.models.character import Character, CharacterUpdate
from app.models.project import ProjectStatus
from app.services.extractor import extract_characters
from app.services.parser import extract_text
from app.config import PROJECTS_DIR

router = APIRouter(prefix="/api/projects", tags=["characters"])


@router.get("/{project_id}/characters")
def api_list_characters(project_id: str):
    return list_characters(project_id)


@router.get("/{project_id}/characters/{char_id}")
def api_get_character(project_id: str, char_id: str):
    char = get_character(char_id)
    if not char or char.project_id != project_id:
        raise HTTPException(404, "Character not found")
    return char


@router.post("/{project_id}/characters", status_code=201)
def api_create_character(project_id: str, body: CharacterUpdate):
    project = get_project(project_id)
    if not project:
        raise HTTPException(404, "Project not found")
    char = Character(
        project_id=project_id,
        name=body.name or "New Character",
        description=body.description or "",
        role=body.role or "supporting",
        reference_prompt=body.reference_prompt or "",
    )
    save_character(char)
    project.character_ids.append(char.id)
    save_project(project)
    return char


@router.put("/{project_id}/characters/{char_id}")
def api_update_character(project_id: str, char_id: str, body: CharacterUpdate):
    char = get_character(char_id)
    if not char or char.project_id != project_id:
        raise HTTPException(404, "Character not found")
    if body.name is not None:
        char.name = body.name
    if body.description is not None:
        char.description = body.description
    if body.role is not None:
        char.role = body.role
    if body.reference_prompt is not None:
        char.reference_prompt = body.reference_prompt
    save_character(char)
    return char


@router.delete("/{project_id}/characters/{char_id}")
def api_delete_character(project_id: str, char_id: str):
    char = get_character(char_id)
    if not char or char.project_id != project_id:
        raise HTTPException(404, "Character not found")
    project = get_project(project_id)
    if project and char_id in project.character_ids:
        project.character_ids.remove(char_id)
        save_project(project)
    delete_character(char_id)
    return {"ok": True}


@router.post("/{project_id}/characters/extract")
def api_extract_characters(project_id: str):
    project = get_project(project_id)
    if not project:
        raise HTTPException(404, "Project not found")

    project_dir = PROJECTS_DIR / project.slug
    files = list(project_dir.glob("*.txt")) + list(project_dir.glob("*.pdf"))
    if not files:
        raise HTTPException(400, "No source file found. Upload a file first.")

    text = extract_text(files[0])

    try:
        proposals = extract_characters(text)
    except ValueError as e:
        raise HTTPException(400, str(e))

    chars = []
    for p in proposals:
        char = Character(
            project_id=project_id,
            name=p.get("name", "Unknown"),
            description=p.get("description", ""),
            role=p.get("role", "supporting"),
            reference_prompt=f"A portrait of {p.get('name', 'a character')}, {p.get('description', '')}",
        )
        save_character(char)
        chars.append(char)
        project.character_ids.append(char.id)

    project.status = ProjectStatus.characters_extracted
    save_project(project)

    return chars
