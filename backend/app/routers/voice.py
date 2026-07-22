from __future__ import annotations

from fastapi import APIRouter
from fastapi.responses import FileResponse

from app.config import PROJECTS_DIR
from app.db.json_db import get_project, get_scene, save_scene
from app.models.scene import SceneStatus
from app.models.voice import VoicePreviewRequest
from app.services.tts import generate_speech, list_voices

router = APIRouter(prefix="/api", tags=["voice"])


@router.get("/voices")
def api_list_voices():
    return list_voices()


@router.post("/voices/preview")
async def api_preview_voice(body: VoicePreviewRequest):
    import tempfile

    tmp = tempfile.NamedTemporaryFile(suffix=".mp3", delete=False)
    try:
        await generate_speech(body.text, body.voice_id, tmp.name)
        return FileResponse(tmp.name, media_type="audio/mpeg")
    except Exception as e:
        return {"error": str(e)}


@router.post("/projects/{project_id}/scenes/{scene_id}/generate-audio")
async def api_generate_audio(project_id: str, scene_id: str):
    project = get_project(project_id)
    if not project:
        from fastapi import HTTPException
        raise HTTPException(404, "Project not found")

    scene = get_scene(scene_id)
    if not scene or scene.project_id != project_id:
        from fastapi import HTTPException
        raise HTTPException(404, "Scene not found")

    narration = scene.narration
    if not narration:
        from fastapi import HTTPException
        raise HTTPException(400, "Scene has no narration. Split scenes first.")

    project_dir = PROJECTS_DIR / project.slug
    project_dir.mkdir(parents=True, exist_ok=True)
    (project_dir / "audio").mkdir(exist_ok=True)

    output_path = project_dir / "audio" / f"scene_{scene.order:03d}.mp3"

    try:
        await generate_speech(narration, scene.voice_id, output_path)
    except Exception as e:
        from fastapi import HTTPException
        raise HTTPException(400, str(e))

    scene.audio_path = str(output_path)
    scene.status = SceneStatus.audio_generated
    save_scene(scene)

    return {"audio_path": scene.audio_path, "status": scene.status.value}
