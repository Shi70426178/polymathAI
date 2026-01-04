from pathlib import Path
from app.core.config import UPLOAD_DIR, AUDIO_DIR

def cleanup_video_files(video_id: str):
    """
    Deletes video and audio files related to a video_id.
    Safe to call after processing is complete.
    """

    # delete uploaded videos (any extension)
    for video_file in UPLOAD_DIR.glob(f"{video_id}.*"):
        try:
            video_file.unlink()
        except Exception as e:
            print(f"[CLEANUP] Failed to delete video {video_file}: {e}")

    # delete extracted audio (any format, not just .wav)
    for audio_file in AUDIO_DIR.glob(f"{video_id}.*"):
        try:
            audio_file.unlink()
        except Exception as e:
            print(f"[CLEANUP] Failed to delete audio {audio_file}: {e}")
