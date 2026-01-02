from fastapi import APIRouter, HTTPException
from pathlib import Path
from app.services.content.generator import ContentGenerator
from pydantic import BaseModel
from app.core.config import STATUS_DIR
from app.utils.cleanup import cleanup_video_files
from app.core.config import OPENAI_API_KEY
from app.core.config import UPLOAD_DIR, AUDIO_DIR, TRANSCRIPT_DIR
from app.services.video.extractor import extract_audio
from app.services.speech.transcriber import Transcriber
# from app.services.content.llm_client import generate_social_content
# from app.core.config import TRANSCRIPT_DIR
router = APIRouter(prefix="/process", tags=["Processing"])

class GenerateContentRequest(BaseModel):
    category: str


@router.post("/extract-audio/{video_id}")
def extract_audio_api(video_id: str):
    matches = list(UPLOAD_DIR.glob(f"{video_id}.*"))
    if not matches:
        raise HTTPException(status_code=404, detail="Video not found")

    video_path = matches[0]

    try:
        audio_path = extract_audio(video_path, AUDIO_DIR)
    except Exception:
        raise HTTPException(status_code=500, detail="Audio extraction failed")

    return {
        "message": "Audio extracted successfully",
        "audio_file": audio_path.name
    }


@router.post("/transcribe/{video_id}")
def transcribe_audio(video_id: str):
    audio_matches = list(AUDIO_DIR.glob(f"{video_id}.wav"))
    if not audio_matches:
        raise HTTPException(status_code=404, detail="Audio not found")

    audio_path = audio_matches[0]

    transcriber = Transcriber()

    text = transcriber.transcribe(audio_path)

    transcript_path = TRANSCRIPT_DIR / f"{video_id}.txt"
    with open(transcript_path, "w", encoding="utf-8") as f:
        f.write(text)

    return {
        "message": "Transcription completed",
        "transcript": text
    }
@router.post("/generate-content/{video_id}")
def generate_content(video_id: str, body: GenerateContentRequest):

    # 🔒 OpenAI availability guard (ADD HERE)
    if not OPENAI_API_KEY:
        raise HTTPException(
            status_code=503,
            detail="AI generation temporarily unavailable. Please try again later."
        )

    lock_file = STATUS_DIR / f"{video_id}.lock"
    done_file = STATUS_DIR / f"{video_id}.done"

    # 🚫 If already completed, reuse result
    if done_file.exists():
        transcript_path = TRANSCRIPT_DIR / f"{video_id}.txt"
        text = transcript_path.read_text(encoding="utf-8")

        generator = ContentGenerator()
        content = generator.generate(
            transcript=text,
            category=body.category
        )

        return {
            "message": "Already processed (cached)",
            "content": content
        }

    # 🚫 If processing is ongoing
    if lock_file.exists():
        raise HTTPException(
            status_code=409,
            detail="Processing already in progress"
        )

    # 🔒 Create lock
    lock_file.touch()

    try:
        transcript_path = TRANSCRIPT_DIR / f"{video_id}.txt"
        if not transcript_path.exists():
            raise HTTPException(status_code=404, detail="Transcript not found")

        text = transcript_path.read_text(encoding="utf-8")

        generator = ContentGenerator()
        content = generator.generate(
            transcript=text,
            category=body.category
        )

        # ✅ Mark done
        done_file.touch()

        # 🧹 Cleanup heavy files (perfect place)
        cleanup_video_files(video_id)

        return {
            "message": "Content generated successfully",
            "content": content
        }

    finally:
        # 🔓 Always remove lock
        if lock_file.exists():
            lock_file.unlink()


@router.post("/full/{video_id}")
def full_pipeline(video_id: str):
    lock_file = STATUS_DIR / f"{video_id}.lock"
    if lock_file.exists():
        raise HTTPException(409, "Processing already in progress")

    lock_file.touch()

    # 1. Find video
    video_matches = list(UPLOAD_DIR.glob(f"{video_id}.*"))
    if not video_matches:
        raise HTTPException(status_code=404, detail="Video not found")

    video_path = video_matches[0]

    # 2. Extract audio
    try:
        audio_path = extract_audio(video_path, AUDIO_DIR)
    except Exception:
        raise HTTPException(status_code=500, detail="Audio extraction failed")

    # 3. Transcribe
    transcriber = Transcriber()

    text = transcriber.transcribe(audio_path)

    transcript_path = TRANSCRIPT_DIR / f"{video_id}.txt"
    transcript_path.write_text(text, encoding="utf-8")

    # 4. Generate content (NO language logic)
    generator = OpenAIContentGenerator()
    content = generator.generate(text)
    lock_file.unlink(missing_ok=True)

    return {
        "message": "Full pipeline completed",
        "video_id": video_id,
        "transcript": text,
        "content": content
    }
