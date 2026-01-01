import re

TOPIC_RULES = {
    "sci-fi": [
        "machine", "robot", "ultron", "ai", "future", "alien", "technology"
    ],
    "fiction": [
        "imaginary", "story", "kahani", "kalpana", "fiction"
    ],
    "humor": [
        "funny", "mazaak", "joke", "hasna", "lol"
    ],
    "chaos": [
        "destroy", "end", "khatam", "danger", "attack", "tabahi"
    ],
    "gaming": [
        "game", "level", "player", "match", "kill", "win", "lose"
    ],
    "motivation": [
        "mehnat", "success", "focus", "goal", "dream", " मेहनत"
    ],
}

def infer_topics(text: str) -> list[str]:
    text = text.lower()
    detected = []

    for topic, signals in TOPIC_RULES.items():
        for word in signals:
            if re.search(rf"\b{re.escape(word)}\b", text):
                detected.append(topic)
                break

    return detected
