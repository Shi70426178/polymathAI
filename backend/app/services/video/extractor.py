import subprocess
from pathlib import Path


def extract_audio(video_path: Path, output_dir: Path) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)

    audio_path = output_dir / f"{video_path.stem}.wav"

    command = [
        "ffmpeg",
        "-y",
        "-i", str(video_path),
    
        # 🔥 AUDIO CLEANING (VERY IMPORTANT)
        "-vn",
        "-ac", "1",
        "-ar", "16000",
        "-af", "highpass=f=80, lowpass=f=8000, volume=1.5",
    
        str(audio_path)
    ]

 
    subprocess.run(
        command,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=True
    )

    return audio_path
