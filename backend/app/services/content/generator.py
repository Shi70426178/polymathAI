from app.services.content.llm_client import generate_social_content


class ContentGenerator:
    def generate(self, transcript: str, category: str) -> dict:
        return generate_social_content(transcript, category)
