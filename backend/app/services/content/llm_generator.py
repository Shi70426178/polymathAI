class LLMContentGenerator:
    def __init__(self, llm_client):
        self.llm = llm_client

    def generate(self, text: str) -> dict:
        prompt = self._build_prompt(text)
        response = self.llm.generate(prompt)

        return self._parse_response(response)

    def _build_prompt(self, text: str) -> str:
        return f"""
You are a social media expert.

The following text is extracted from a short video.
The text may be broken, noisy, mixed language, or informal.

Your job:
1. Understand the topic and intent of the video
2. Generate a catchy TITLE
3. Generate RELEVANT, LOGICAL hashtags (not generic)
4. Hashtags should reflect the topic (gaming, sci-fi, comedy, vlog, etc.)

IMPORTANT RULES:
- Do NOT use generic hashtags unless they truly apply
- Think like a human creator
- Hashtags should make sense for discoverability

Video text:
\"\"\"
{text}
\"\"\"

Return output in EXACT JSON format:
{{
  "title": "...",
  "hashtags": ["#tag1", "#tag2", "#tag3"]
}}
"""

    def _parse_response(self, response: str) -> dict:
        import json
        return json.loads(response)
