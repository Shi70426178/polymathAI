from faster_whisper import WhisperModel

# LOAD ONCE
_MODEL = WhisperModel(
    "medium",
    device="cpu",
    compute_type="int8"
)

class Transcriber:
    def transcribe(self, audio_path: str) -> str:
        segments, info = _MODEL.transcribe(
            audio_path,
            vad_filter=True,
            beam_size=3
        )

        text_parts = []
        for i, segment in enumerate(segments):
            if i >= 30:
                break
            text_parts.append(segment.text)

        return " ".join(text_parts)
