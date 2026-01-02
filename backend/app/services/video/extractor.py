import subprocess
from pathlib import Path

def extract_audio(video_path: Path, audio_dir: Path) -> Path:
    audio_path = audio_dir / f"{video_path.stem}.wav"

    command = [
        "ffmpeg",
        "-y",
        "-i", str(video_path),
        "-vn",
        "-ac", "1",
        "-ar", "16000",
        "-t", "60",           
        "-f", "wav",
        str(audio_path)
    ]

    subprocess.run(command, check=True)
    return audio_path
