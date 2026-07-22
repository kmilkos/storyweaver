from __future__ import annotations

from datetime import datetime
from uuid import uuid4

from pydantic import BaseModel, Field


class Character(BaseModel):
    id: str = Field(default_factory=lambda: uuid4().hex[:12])
    project_id: str
    name: str
    description: str = ""
    role: str = "unknown"
    reference_prompt: str = ""
    reference_image: str = ""
    color_tag: str = "#D946EF"
    created_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())


class CharacterProposal(BaseModel):
    name: str
    description: str
    role: str


class CharacterProposalList(BaseModel):
    characters: list[CharacterProposal]


class CharacterUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    role: str | None = None
    reference_prompt: str | None = None
