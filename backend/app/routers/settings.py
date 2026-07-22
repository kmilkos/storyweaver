from __future__ import annotations

from fastapi import APIRouter
from pydantic import BaseModel

from app.config import BACKEND_DIR

router = APIRouter(prefix="/api/settings", tags=["settings"])

ENV_PATH = BACKEND_DIR / ".env"

KEYS = ["GEMINI_API_KEY", "STABILITY_API_KEY", "ELEVENLABS_API_KEY", "PROJECTS_DIR"]


class SettingsUpdate(BaseModel):
    gemini_api_key: str = ""
    stability_api_key: str = ""
    elevenlabs_api_key: str = ""
    projects_dir: str = ""


def _read_env() -> dict[str, str]:
    data = {}
    if ENV_PATH.exists():
        for line in ENV_PATH.read_text().splitlines():
            line = line.strip()
            if "=" in line and not line.startswith("#"):
                k, _, v = line.partition("=")
                data[k.strip()] = v.strip()
    return data


def _write_env(data: dict[str, str]) -> None:
    lines = []
    for key in KEYS:
        lines.append(f"{key}={data.get(key, '')}")
    lines.append("")
    ENV_PATH.write_text("\n".join(lines))


@router.get("")
def get_settings():
    env = _read_env()
    return {
        "gemini_api_key": env.get("GEMINI_API_KEY", ""),
        "stability_api_key": env.get("STABILITY_API_KEY", ""),
        "elevenlabs_api_key": env.get("ELEVENLABS_API_KEY", ""),
        "projects_dir": env.get("PROJECTS_DIR", ""),
        "gemini_configured": bool(env.get("GEMINI_API_KEY")),
    }


@router.put("")
def update_settings(body: SettingsUpdate):
    env = _read_env()
    if body.gemini_api_key:
        env["GEMINI_API_KEY"] = body.gemini_api_key
    if body.stability_api_key:
        env["STABILITY_API_KEY"] = body.stability_api_key
    if body.elevenlabs_api_key:
        env["ELEVENLABS_API_KEY"] = body.elevenlabs_api_key
    if body.projects_dir:
        env["PROJECTS_DIR"] = body.projects_dir
    _write_env(env)
    return get_settings()
