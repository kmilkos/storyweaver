from pathlib import Path

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    gemini_api_key: str = ""
    stability_api_key: str = ""
    elevenlabs_api_key: str = ""
    projects_dir: str = ""

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


settings = Settings()

BACKEND_DIR = Path(__file__).parent.parent
ENV_PATH = BACKEND_DIR / ".env"


def get_env(key: str, default: str = "") -> str:
    if ENV_PATH.exists():
        for line in ENV_PATH.read_text().splitlines():
            line = line.strip()
            if line.startswith("#") or "=" not in line:
                continue
            k, _, v = line.partition("=")
            if k.strip() == key:
                return v.strip()
    return default

if settings.projects_dir:
    PROJECTS_DIR = Path(settings.projects_dir)
    if not PROJECTS_DIR.is_absolute():
        PROJECTS_DIR = BACKEND_DIR / PROJECTS_DIR
else:
    PROJECTS_DIR = BACKEND_DIR / "projects"
PROJECTS_DIR.mkdir(parents=True, exist_ok=True)
DB_PATH = BACKEND_DIR / "db.json"
VOICES_DIR = BACKEND_DIR / "voices"
VOICES_DIR.mkdir(parents=True, exist_ok=True)
STATIC_DIR = BACKEND_DIR / "static"
STATIC_DIR.mkdir(parents=True, exist_ok=True)
