from __future__ import annotations

from datetime import datetime
from enum import Enum
from uuid import uuid4

from pydantic import BaseModel, Field


class ProjectStatus(str, Enum):
    draft = "draft"
    characters_extracted = "characters_extracted"
    scenes_split = "scenes_split"
    in_progress = "in_progress"
    complete = "complete"


class AspectRatio(str, Enum):
    landscape = "16:9"
    portrait = "9:16"


class CompileMode(str, Enum):
    slideshow = "slideshow"
    video = "video"


class Chapter(BaseModel):
    id: str = Field(default_factory=lambda: uuid4().hex[:12])
    title: str
    order: int


class Project(BaseModel):
    id: str = Field(default_factory=lambda: uuid4().hex[:12])
    title: str
    author: str = ""
    slug: str
    status: ProjectStatus = ProjectStatus.draft
    chapters: list[Chapter] = []
    character_ids: list[str] = []
    aspect_ratio: AspectRatio = AspectRatio.landscape
    compile_mode: CompileMode = CompileMode.slideshow
    created_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    updated_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())


class ProjectCreate(BaseModel):
    title: str
    author: str = ""
    aspect_ratio: AspectRatio = AspectRatio.landscape
    compile_mode: CompileMode = CompileMode.slideshow


class ProjectSummary(BaseModel):
    id: str
    title: str
    author: str
    status: ProjectStatus
    chapter_count: int
    character_count: int
    aspect_ratio: AspectRatio
    compile_mode: CompileMode
    created_at: str
