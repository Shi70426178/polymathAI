from fastapi import APIRouter, UploadFile, File, HTTPException, Request, Depends
from uuid import uuid4
from pathlib import Path
from sqlalchemy.orm import Session
from datetime import date

from app.core.config import UPLOAD_DIR, ALLOWED_VIDEO_TYPES, MAX_VIDEO_MB
from app.db.database import SessionLocal
from app.db.models import IPUsage
from app.utils.ip import get_client_ip

router = APIRouter(prefix="/upload", tags=["Upload"])


# ---------------------
# DB Dependency
# ---------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ---------------------
# Upload with IP limit
# ---------------------
@router.post("/video")
async def upload_video(
    request: Request,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    # 🔒 IP-based daily limit
    client_ip = get_client_ip(request)
    today = date.today().isoformat()

    usage = (
        db.query(IPUsage)
        .filter(IPUsage.ip == client_ip, IPUsage.date == today)
        .first()
    )

    if usage and usage.count >= 3:
        raise HTTPException(
            status_code=429,
            detail={
                "code": "DAILY_LIMIT_REACHED",
                "message": "Daily free limit reached (3 uploads). Login & upgrade to continue."
            }
        )

    if not usage:
        usage = IPUsage(ip=client_ip, date=today, count=1)
        db.add(usage)
    else:
        usage.count += 1

    db.commit()

    # ---------------------
    # File validation
    # ---------------------
    if file.content_type not in ALLOWED_VIDEO_TYPES:
        raise HTTPException(
            status_code=400,
            detail="Unsupported video format"
        )

    # generate unique filename
    file_id = str(uuid4())
    extension = Path(file.filename).suffix
    save_path = UPLOAD_DIR / f"{file_id}{extension}"

    # read & validate size
    content = await file.read()
    size_mb = len(content) / (1024 * 1024)

    if size_mb > MAX_VIDEO_MB:
        raise HTTPException(
            status_code=400,
            detail="File too large"
        )

    # save file
    with open(save_path, "wb") as f:
        f.write(content)

    return {
        "message": "Video uploaded successfully",
        "video_id": file_id,
        "filename": save_path.name,
        "size_mb": round(size_mb, 2)
    }
