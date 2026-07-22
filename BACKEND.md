# StoryWeaver — Backend Architecture

## Tech Stack

| Component | Library |
|---|---|
| API Framework | FastAPI + Uvicorn |
| Text Parsing | PyMuPDF (PDF), plain text (TXT) |
| AI (extraction, scenes) | Google Gemini (`google-genai` SDK) |
| Image Generation | Google Imagen or Stability AI / OpenAI |
| Text-to-Speech | Edge-TTS (free) or ElevenLabs API |
| Video Assembly | MoviePy + FFmpeg |
| Image Processing | Pillow |
| Data Validation | Pydantic |
| Database | JSON file (`db.json`) |

---

## Project Structure

```
storyweaver/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                  # FastAPI app, CORS, static mount
│   │   ├── config.py                # Settings from .env
│   │   │
│   │   ├── routers/
│   │   │   ├── projects.py          # CRUD: list, create, get, delete projects
│   │   │   ├── characters.py        # Extract, list, update, delete characters
│   │   │   ├── scenes.py            # Split into scenes, edit, reorder
│   │   │   ├── images.py            # Generate scene image, regenerate
│   │   │   ├── voice.py             # List voices, preview clip, assign
│   │   │   └── export.py            # Compile video, download
│   │   │
│   │   ├── models/
│   │   │   ├── project.py           # Project, Chapter
│   │   │   ├── character.py         # Character
│   │   │   ├── scene.py             # Scene (narration, voice, image status)
│   │   │   └── voice.py             # Voice profile
│   │   │
│   │   ├── services/
│   │   │   ├── parser.py            # Extract text from TXT/PDF
│   │   │   ├── extractor.py         # Gemini: character list + scene breakdown
│   │   │   ├── image_gen.py         # Generate scene images
│   │   │   ├── tts.py               # Text-to-speech generation
│   │   │   └── video_compiler.py    # MoviePy: images + audio → video
│   │   │
│   │   └── db/
│   │       └── json_db.py           # Read/write projects to projects.json
│   │
│   ├── projects/                    # Per-project asset directory
│   │   └── {project_slug}/
│   │       ├── characters/          # Character reference images
│   │       ├── scenes/              # Scene images
│   │       ├── audio/               # Voiceover clips
│   │       └── exports/             # Final video files
│   │
│   ├── voices/                      # Voice sample previews
│   ├── requirements.txt
│   └── .env
│
└── frontend/                        # (designed via Stitch)
    └── index.html
```

---

## API Routes

### Projects
| Method | Route | Description |
|---|---|---|
| GET | /api/projects | List all projects |
| POST | /api/projects | Create project from uploaded file |
| GET | /api/projects/{id} | Get project detail (chapters, characters) |
| DELETE | /api/projects/{id} | Delete project |

### Characters
| Method | Route | Description |
|---|---|---|
| POST | /api/projects/{id}/characters/extract | AI scans novel → proposes characters |
| GET | /api/projects/{id}/characters | List characters |
| PUT | /api/projects/{id}/characters/{char_id} | Update character (name, description) |
| DELETE | /api/projects/{id}/characters/{char_id} | Remove character |
| POST | /api/projects/{id}/characters/{char_id}/generate-image | Generate character reference image |

### Scenes
| Method | Route | Description |
|---|---|---|
| POST | /api/projects/{id}/scenes/split | AI splits chapter into scenes |
| GET | /api/projects/{id}/scenes | List scenes for a chapter |
| PUT | /api/projects/{id}/scenes/{scene_id} | Update narration, voice, camera motion |
| POST | /api/projects/{id}/scenes/{scene_id}/generate-image | Generate scene image |
| POST | /api/projects/{id}/scenes/{scene_id}/generate-audio | Generate voiceover audio |

### Voices
| Method | Route | Description |
|---|---|---|
| GET | /api/voices | List available voices with sample URLs |
| POST | /api/voices/preview | Generate a short sample clip from text |

### Export
| Method | Route | Description |
|---|---|---|
| POST | /api/projects/{id}/export/preview | Generate preview (first 3 scenes) |
| POST | /api/projects/{id}/export/compile | Compile full video |
| GET | /api/projects/{id}/export/download | Download compiled video |
| GET | /api/projects/{id}/export/status | Check compilation progress |

---

## Data Models

### Project
```json
{
  "id": "uuid",
  "title": "The Great Gatsby",
  "author": "F. Scott Fitzgerald",
  "slug": "the-great-gatsby",
  "status": "draft",          
  "chapters": [{"id": "uuid", "title": "Chapter 1", "order": 1}],
  "character_ids": ["uuid1", "uuid2"],
  "created_at": "iso8601",
  "updated_at": "iso8601"
}
```

### Character
```json
{
  "id": "uuid",
  "project_id": "uuid",
  "name": "Jay Gatsby",
  "description": "Wealthy mysterious man in his 30s...",
  "role": "protagonist",
  "reference_prompt": "A tall man in 1920s attire...",
  "reference_image": "projects/slug/characters/gatsby.png",
  "color_tag": "#D946EF"
}
```

### Scene
```json
{
  "id": "uuid",
  "chapter_id": "uuid",
  "order": 3,
  "narration": "Gatsby stood at the end of the dock...",
  "character_ids": ["uuid1"],
  "voice_id": "fenrir",
  "camera_motion": "slow-zoom",
  "image_prompt": "A man in a white suit standing on a wooden dock...",
  "image_path": "projects/slug/scenes/scene_3.png",
  "audio_path": "projects/slug/audio/scene_3.mp3",
  "status": "draft"           
}
```

---

## Workflow Sequence

```
1. POST /api/projects (upload file)
   ├── parser.py extracts raw text
   └── returns project stub

2. POST /api/projects/{id}/characters/extract
   ├── extractor.py calls Gemini → character list
   └── returns proposed characters (user approves via PUT)

3. POST /api/projects/{id}/scenes/split
   ├── extractor.py calls Gemini → scene breakdown
   └── returns scenes with narration + image prompts

4. FOR each scene (user approval loop):
   ├── POST /api/projects/{id}/scenes/{scene_id}/generate-image
   ├── POST /api/projects/{id}/scenes/{scene_id}/generate-audio
   └── user reviews, edits, regenerates as needed

5. POST /api/projects/{id}/export/compile
   ├── video_compiler.py: MoviePy assembles all scenes
   │   - Ken Burns zoom on each image
   │   - Crossfade transitions
   │   - Audio overlay (voiceover + optional background)
   │   - Subtitles (optional)
   └── returns compiled video file
```

---

## Voice Options (Initial)

| Voice ID | Name | Gender | Style | Source |
|---|---|---|---|---|
| kore | Kore | Female | Warm, narrative | Gemini TTS |
| puck | Puck | Male | Energetic, bright | Gemini TTS |
| charon | Charon | Male | Deep, dramatic | Gemini TTS |
| fenrir | Fenrir | Male | Gruff, authoritative | Gemini TTS |
| zephyr | Zephyr | Neutral | Soft, atmospheric | Gemini TTS |
| edge-en-US-1 | Jenny (Edge) | Female | Natural, US | Edge-TTS |
| edge-en-US-2 | Guy (Edge) | Male | Natural, US | Edge-TTS |
| edge-en-GB-1 | Sonia (Edge) | Female | British | Edge-TTS |

---

## Environment Variables (.env)

```
GEMINI_API_KEY=xxx
STABILITY_API_KEY=xxx       # if using Stability AI
ELEVENLABS_API_KEY=xxx      # if using ElevenLabs
PROJECTS_DIR=./projects
```

---

## Running Locally

```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```
