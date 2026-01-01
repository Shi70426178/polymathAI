LANG_MAP = {
    "en": "English",
    "hi": "Hindi",
    "de": "German"
}

def lang_code_to_name(code: str) -> str:
    return LANG_MAP.get(code, "English")
