from faster_whisper import WhisperModel
from pathlib import Path


class Transcriber:
    def __init__(self):
        # 🔥 BEST BALANCE FOR HINDI ON CPU
        self.model = WhisperModel(
            "medium",          # NOT small
            device="cpu",
            compute_type="int8"
        )

    def transcribe(self, audio_path: Path) -> str:
        segments, info = self.model.transcribe(
            str(audio_path),
            language="hi",      # FORCE Hindi
            beam_size=5,
            vad_filter=True     # removes silence
        )

        text = []
        for segment in segments:
            text.append(segment.text)

        return " ".join(text).strip()
