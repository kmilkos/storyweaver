from pydantic import BaseModel


class Voice(BaseModel):
    id: str
    name: str
    gender: str
    style: str
    source: str
    sample_path: str = ""


class VoicePreviewRequest(BaseModel):
    text: str = "This is a sample of my voice."
    voice_id: str = "kore"
