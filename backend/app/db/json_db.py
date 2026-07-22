from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from app.config import DB_PATH
from app.models.character import Character
from app.models.project import Project
from app.models.scene import Scene


def _read() -> dict[str, Any]:
    if not DB_PATH.exists():
        return {"projects": {}, "characters": {}, "scenes": {}}
    return json.loads(DB_PATH.read_text())


def _write(data: dict[str, Any]) -> None:
    DB_PATH.write_text(json.dumps(data, indent=2, default=str))


# -- Projects --

def list_projects() -> list[Project]:
    db = _read()
    return [Project(**p) for p in db["projects"].values()]


def get_project(project_id: str) -> Project | None:
    db = _read()
    p = db["projects"].get(project_id)
    return Project(**p) if p else None


def save_project(project: Project) -> None:
    db = _read()
    db["projects"][project.id] = project.model_dump(mode="json")
    _write(db)


def delete_project(project_id: str) -> bool:
    db = _read()
    if project_id not in db["projects"]:
        return False
    del db["projects"][project_id]
    for cid in list(db["characters"]):
        if db["characters"][cid]["project_id"] == project_id:
            del db["characters"][cid]
    for sid in list(db["scenes"]):
        if db["scenes"][sid]["project_id"] == project_id:
            del db["scenes"][sid]
    _write(db)
    return True


# -- Characters --

def list_characters(project_id: str) -> list[Character]:
    db = _read()
    return [Character(**c) for c in db["characters"].values()
            if c["project_id"] == project_id]


def get_character(char_id: str) -> Character | None:
    db = _read()
    c = db["characters"].get(char_id)
    return Character(**c) if c else None


def save_character(character: Character) -> None:
    db = _read()
    db["characters"][character.id] = character.model_dump(mode="json")
    _write(db)


def delete_character(char_id: str) -> bool:
    db = _read()
    if char_id not in db["characters"]:
        return False
    del db["characters"][char_id]
    _write(db)
    return True


# -- Scenes --

def list_scenes(project_id: str | None = None,
                chapter_id: str | None = None) -> list[Scene]:
    db = _read()
    scenes = [Scene(**s) for s in db["scenes"].values()]
    if project_id:
        scenes = [s for s in scenes if s.project_id == project_id]
    if chapter_id:
        scenes = [s for s in scenes if s.chapter_id == chapter_id]
    scenes.sort(key=lambda s: s.order)
    return scenes


def get_scene(scene_id: str) -> Scene | None:
    db = _read()
    s = db["scenes"].get(scene_id)
    return Scene(**s) if s else None


def save_scene(scene: Scene) -> None:
    db = _read()
    db["scenes"][scene.id] = scene.model_dump(mode="json")
    _write(db)


def delete_scene(scene_id: str) -> bool:
    db = _read()
    if scene_id not in db["scenes"]:
        return False
    del db["scenes"][scene_id]
    _write(db)
    return True
