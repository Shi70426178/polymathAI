from faster_whisper import WhisperModel


class Transcriber:
    def __init__(self):
        # Load model once (IMPORTANT for performance)
        self.model = WhisperModel(
            "medium",
            device="cpu",
            compute_type="int8"  # very important for CPU
        )

    def transcribe(self, audio_path: str) -> str:
        segments, info = self.model.transcribe(
            audio_path,
            vad_filter=True,
            beam_size=3
        )

        text_parts = []

        for i, segment in enumerate(segments):
            if i >= 30:  # ~1 minute of speech cap
                break
            text_parts.append(segment.text)

        return " ".join(text_parts)
