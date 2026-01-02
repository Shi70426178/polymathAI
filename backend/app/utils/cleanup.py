from pathlib import Path
from app.core.config import UPLOAD_DIR, AUDIO_DIR

def cleanup_video_files(video_id: str):
    """
    Deletes video and audio files related to a video_id.
    Safe to call after processing is complete.
    """

    # delete uploaded video (any extension)
    for video_file in UPLOAD_DIR.glob(f"{video_id}.*"):
        try:
            video_file.unlink()
        except Exception:
            pass

    # delete extracted audio
    audio_file = AUDIO_DIR / f"{video_id}.wav"
    if audio_file.exists():
        try:
            audio_file.unlink()
        except Exception:
            pass
