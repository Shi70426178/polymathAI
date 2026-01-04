import json
from pathlib import Path

STATUS_DIR = Path("app/data/status")
STATUS_DIR.mkdir(parents=True, exist_ok=True)

def set_status(video_id, status, error=None):
    data = {"status": status}
    if error:
        data["error"] = error

    with open(STATUS_DIR / f"{video_id}.json", "w") as f:
        json.dump(data, f)

def get_status(video_id):
    file = STATUS_DIR / f"{video_id}.json"
    if not file.exists():
        return {"status": "unknown"}
    return json.loads(file.read_text())
