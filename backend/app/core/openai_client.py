from openai import OpenAI
from app.core.config import OPENAI_API_KEY, OPENAI_MODEL

if not OPENAI_API_KEY:
    raise RuntimeError("OPENAI_API_KEY not set")

client = OpenAI(api_key=OPENAI_API_KEY)
DEFAULT_MODEL = OPENAI_MODEL
