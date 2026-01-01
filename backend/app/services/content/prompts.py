def build_prompt(transcript: str, language: str):
    return f"""
You are a social media content generator.

RULES (VERY IMPORTANT):
- Generate output ONLY in this language: {language}
- Do NOT switch language
- Do NOT translate unless asked

Transcript:
\"\"\"{transcript}\"\"\"

Generate:
1. Catchy title
2. Short description
3. 5–7 relevant hashtags
"""
