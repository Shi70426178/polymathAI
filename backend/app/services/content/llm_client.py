from openai import OpenAI
from app.core.config import OPENAI_API_KEY, OPENAI_MODEL
from fastapi import HTTPException
import json

client = OpenAI(api_key=OPENAI_API_KEY)

def generate_social_content(text: str, category: str) -> dict:
    prompt = f"""
You are a professional social media content expert.

CRITICAL RULES:
- Transcript decides meaning
- Category is hint only
- Return STRICT JSON ONLY

Category: {category}

Transcript:
\"\"\"
{text}
\"\"\"

Return JSON:
{{
  "title": "...",
  "description": "...",
  "hashtags": ["#tag1"]
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

    raw = response.choices[0].message.content

    try:
        return json.loads(raw)
    except Exception:
        raise HTTPException(
            status_code=500,
            detail=f"Invalid AI response: {raw}"
        )
