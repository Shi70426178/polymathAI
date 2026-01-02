import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parents[2]


DATA_DIR = BASE_DIR / "data"
UPLOAD_DIR = DATA_DIR / "uploads"
AUDIO_DIR = DATA_DIR / "audio"
TRANSCRIPT_DIR = DATA_DIR / "transcripts"
RESULT_DIR = DATA_DIR / "results"
STATUS_DIR = DATA_DIR / "status"
STATUS_DIR.mkdir(parents=True, exist_ok=True)

MAX_VIDEO_MB = 100
ALLOWED_VIDEO_TYPES = ["video/mp4", "video/mkv", "video/webm"]

# OpenAI (Mini model)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = "gpt-4o-mini"

for path in [UPLOAD_DIR, AUDIO_DIR, TRANSCRIPT_DIR, RESULT_DIR]:
    path.mkdir(parents=True, exist_ok=True)
