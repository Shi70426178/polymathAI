from openai import OpenAI

client = OpenAI(api_key="YOUR_API_KEY")


class OpenAIContentGenerator:
    def generate(self, transcript: str) -> dict:
        prompt = f"""
You are a social media expert.

Given this video transcript (it may be noisy, Hindi, English, or mixed),
understand the meaning and generate:

1. A short catchy title
2. A short description
3. 5–8 highly relevant hashtags (based on meaning, not keywords)

Transcript:
\"\"\"
{transcript}
\"\"\"

Respond strictly in JSON:
{{
  "title": "...",
  "description": "...",
  "hashtags": ["#tag1", "#tag2"]
}}
"""

        response = client.responses.create(
            model="gpt-5-mini",
            input=prompt
        )

        return response.output_parsed
