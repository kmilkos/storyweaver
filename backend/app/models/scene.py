from __future__ import annotations

from datetime import datetime
from enum import Enum
from uuid import uuid4

from pydantic import BaseModel, Field


class SceneStatus(str, Enum):
    draft = "draft"
    image_generated = "image_generated"
    audio_generated = "audio_generated"
    complete = "complete"


class CameraMotion(str, Enum):
    static = "static"
    slow_zoom = "slow-zoom"
    slow_pan = "slow-pan"
    dolly = "dolly"


class Scene(BaseModel):
    id: str = Field(default_factory=lambda: uuid4().hex[:12])
    chapter_id: str
    project_id: str
    order: int
    narration: str = ""
    image_prompt: str = ""
    image_path: str = ""
    audio_path: str = ""
    voice_id: str = "kore"
    camera_motion: CameraMotion = CameraMotion.slow_zoom
    character_ids: list[str] = []
    status: SceneStatus = SceneStatus.draft
    created_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())


class SceneUpdate(BaseModel):
    narration: str | None = None
    image_prompt: str | None = None
    voice_id: str | None = None
    camera_motion: CameraMotion | None = None
    character_ids: list[str] | None = None


class SceneSplitRequest(BaseModel):
    chapter_id: str
    chapter_text: str
