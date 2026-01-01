from openai import OpenAI
from app.core.config import OPENAI_API_KEY, OPENAI_MODEL
from fastapi import HTTPException

client = OpenAI(api_key=OPENAI_API_KEY)


def generate_social_content(text: str, category: str) -> dict:
    prompt = f"""
You are a professional social media content expert.

You are given:
1. A video transcript (this is the PRIMARY source of truth)
2. A user-selected category (this is ONLY a hint)

CRITICAL RULES:
- The transcript determines the real meaning.
- The category is a soft hint only.
- If the transcript meaning conflicts with the category, IGNORE the category.
- Do NOT force hashtags just because of the category.
- Think like a human content creator.

User-selected category (hint only): {category}

Transcript:
\"\"\"
{text}
\"\"\"

Generate:
1. A short catchy title
2. A concise description
3. 5–8 relevant, intelligent hashtags

Return STRICT JSON ONLY in this format:
{{
  "title": "...",
  "description": "...",
  "hashtags": ["#tag1", "#tag2"]
}}
"""


    response = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[
            {"role": "system", "content": "You are an intelligent content creator."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.7,
    )

    return response.choices[0].message.parsed
