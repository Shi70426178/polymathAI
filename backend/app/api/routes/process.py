from fastapi import APIRouter, HTTPException
from pathlib import Path
import json
import re
import threading
from app.core.config import STATUS_DIR

from app.utils.status import set_status, get_status
from app.services.content.generator import ContentGenerator
from app.services.video.extractor import extract_audio
from app.services.speech.transcriber import Transcriber
from app.utils.cleanup import cleanup_video_files
from app.core.config import (
    OPENAI_API_KEY,
    UPLOAD_DIR,
    AUDIO_DIR,
    TRANSCRIPT_DIR,
    RESULT_DIR,
    STATUS_DIR, 
)


router = APIRouter(prefix="/process", tags=["Processing"])


# =========================
# Utils
# =========================

def safe_parse_content(raw):
    """
    Ensures AI output is always JSON-serializable
    """
    if isinstance(raw, dict):
        return raw

    if not isinstance(raw, str):
        return {"text": str(raw)}

    # remove ```json ``` wrappers
    cleaned = re.sub(r"```json|```", "", raw).strip()

    # try to extract JSON block
    match = re.search(r"\{[\s\S]*\}", cleaned)
    if match:
        try:
            return json.loads(match.group())
        except json.JSONDecodeError:
            pass

    return {"text": cleaned}



def run_pipeline(video_id: str):
    lock_file = STATUS_DIR / f"{video_id}.lock"

    try:
        # ✅ If result already exists, don’t reprocess
        result_path = RESULT_DIR / f"{video_id}.json"
        if result_path.exists():
            set_status(video_id, "completed")
            return

        set_status(video_id, "extracting_audio")

        video_matches = list(UPLOAD_DIR.glob(f"{video_id}.*"))
        if not video_matches:
            raise RuntimeError("Video not found")

        video_path = video_matches[0]

        # 1️⃣ Extract audio
        audio_path = extract_audio(video_path, AUDIO_DIR)

        set_status(video_id, "transcribing")

        # 2️⃣ Transcribe (Whisper API)
        transcriber = Transcriber()
        text = transcriber.transcribe(audio_path)

        transcript_path = TRANSCRIPT_DIR / f"{video_id}.txt"
        transcript_path.write_text(text, encoding="utf-8")

        set_status(video_id, "generating_content")

        # 3️⃣ Generate content
        if not OPENAI_API_KEY:
            raise RuntimeError("OpenAI API key missing")

        generator = ContentGenerator()
        raw = generator.generate(transcript=text, category="general")
        content = safe_parse_content(raw)

        # 4️⃣ Save result
        result_path.write_text(
            json.dumps(content, ensure_ascii=False, indent=2),
            encoding="utf-8"
        )

        # 5️⃣ Cleanup
        cleanup_video_files(video_id)

        set_status(video_id, "completed")

    except Exception as e:
        set_status(video_id, "failed", str(e))

    finally:
        # ✅ ALWAYS release lock
        lock_file.unlink(missing_ok=True)

# =========================
# Schemas
# =========================

# class GenerateContentRequest(BaseModel):
#     category: str


# =========================
# Routes
# =========================

@router.post("/extract-audio/{video_id}")
def extract_audio_api(video_id: str):
    matches = list(UPLOAD_DIR.glob(f"{video_id}.*"))
    if not matches:
        raise HTTPException(status_code=404, detail="Video not found")

    video_path = matches[0]

    try:
        audio_path = extract_audio(video_path, AUDIO_DIR)
    except Exception as e:
        print("❌ Audio extraction error:", e)
        raise HTTPException(status_code=500, detail="Audio extraction failed")

    return {
        "message": "Audio extracted successfully",
        "audio_file": audio_path.name,
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
    transcript_path.write_text(text, encoding="utf-8")

    return {
        "message": "Transcription completed",
        "transcript": text,
    }


# @router.post("/generate-content/{video_id}")
# def generate_content(video_id: str, body: GenerateContentRequest):

#     # 🔒 OpenAI availability guard
#     if not OPENAI_API_KEY:
#         raise HTTPException(
#             status_code=503,
#             detail="AI generation temporarily unavailable. Please try again later.",
#         )

#     lock_file = STATUS_DIR / f"{video_id}.lock"
#     done_file = STATUS_DIR / f"{video_id}.done"

#     # ♻️ Cached result
#     if done_file.exists():
#         transcript_path = TRANSCRIPT_DIR / f"{video_id}.txt"
#         text = transcript_path.read_text(encoding="utf-8")

#         generator = ContentGenerator()
#         raw = generator.generate(transcript=text, category=body.category)

#         print("🧠 RAW AI OUTPUT (cached):")
#         print(raw)

#         return {
#             "message": "Already processed (cached)",
#             "content": safe_parse_content(raw),
#         }

#     # 🚫 Prevent double processing
#     if lock_file.exists():
#         raise HTTPException(status_code=409, detail="Processing already in progress")

#     lock_file.touch()

#     try:
#         transcript_path = TRANSCRIPT_DIR / f"{video_id}.txt"
#         if not transcript_path.exists():
#             raise HTTPException(status_code=404, detail="Transcript not found")

#         text = transcript_path.read_text(encoding="utf-8")

#         generator = ContentGenerator()
#         raw = generator.generate(transcript=text, category=body.category)

#         print("🧠 RAW AI OUTPUT:")
#         print(raw)

#         content = safe_parse_content(raw)

#         done_file.touch()

#         # 🧹 cleanup heavy files
#         cleanup_video_files(video_id)

#         return {
#             "message": "Content generated successfully",
#             "content": content,
#         }

#     except HTTPException:
#         raise

#     except Exception as e:
#         print("❌ Content generation error:", e)
#         raise HTTPException(status_code=500, detail="Content generation failed")

#     finally:
#         if lock_file.exists():
#             lock_file.unlink()


@router.post("/start/{video_id}")
def start_processing(video_id: str):
    lock_file = STATUS_DIR / f"{video_id}.lock"

    if lock_file.exists():
        raise HTTPException(409, "Already processing")

    lock_file.touch()
    set_status(video_id, "processing")

    threading.Thread(
        target=run_pipeline,
        args=(video_id,),
        daemon=True
    ).start()

    return {"status": "started"}


@router.get("/status/{video_id}")
def process_status(video_id: str):
    return get_status(video_id)

@router.get("/result/{video_id}")
def get_result(video_id: str):
    result_path = RESULT_DIR / f"{video_id}.json"

    if not result_path.exists():
        raise HTTPException(404, "Result not ready")

    return json.loads(result_path.read_text(encoding="utf-8"))

@router.post("/full/{video_id}")
def full_pipeline(video_id: str):
    lock_file = STATUS_DIR / f"{video_id}.lock"

    if lock_file.exists():
        raise HTTPException(409, "Processing already in progress")

    lock_file.touch()

    try:
        # 1️⃣ Find video
        video_matches = list(UPLOAD_DIR.glob(f"{video_id}.*"))
        if not video_matches:
            raise HTTPException(status_code=404, detail="Video not found")

        video_path = video_matches[0]

        # 2️⃣ Extract audio
        audio_path = extract_audio(video_path, AUDIO_DIR)

        # 3️⃣ Transcribe
        transcriber = Transcriber()
        text = transcriber.transcribe(audio_path)

        transcript_path = TRANSCRIPT_DIR / f"{video_id}.txt"
        transcript_path.write_text(text, encoding="utf-8")

        # 4️⃣ Generate content
        if not OPENAI_API_KEY:
            raise HTTPException(
                status_code=503,
                detail="AI generation temporarily unavailable",
            )

        generator = ContentGenerator()
        raw = generator.generate(transcript=text, category="general")

        print("🧠 RAW AI OUTPUT (full pipeline):")
        print(raw)

        content = safe_parse_content(raw)

        cleanup_video_files(video_id)

        return {
            "message": "Full pipeline completed",
            "video_id": video_id,
            "transcript": text,
            "content": content,
        }

    finally:
        lock_file.unlink(missing_ok=True)
