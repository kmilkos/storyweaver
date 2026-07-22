from pathlib import Path

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    gemini_api_key: str = ""
    stability_api_key: str = ""
    elevenlabs_api_key: str = ""
    projects_dir: str = "./projects"

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


settings = Settings()

PROJECTS_DIR = Path(settings.projects_dir)
PROJECTS_DIR.mkdir(parents=True, exist_ok=True)
DB_PATH = PROJECTS_DIR.parent / "db.json"
VOICES_DIR = Path("./voices")
VOICES_DIR.mkdir(parents=True, exist_ok=True)
STATIC_DIR = Path("./static")
STATIC_DIR.mkdir(parents=True, exist_ok=True)
