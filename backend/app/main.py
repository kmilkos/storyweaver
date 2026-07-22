from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.config import PROJECTS_DIR, STATIC_DIR
from app.routers import characters, export, images, projects, scenes, settings, voice

app = FastAPI(title="StoryWeaver", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(characters.router)
app.include_router(export.router)
app.include_router(images.router)
app.include_router(projects.router)
app.include_router(scenes.router)
app.include_router(settings.router)
app.include_router(voice.router)

app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")
app.mount("/projects", StaticFiles(directory=str(PROJECTS_DIR)), name="projects")


@app.get("/api/health")
def health():
    return {"status": "ok", "app": "StoryWeaver"}
