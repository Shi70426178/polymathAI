from fastapi import APIRouter, UploadFile, File, HTTPException
from uuid import uuid4
from pathlib import Path

from app.core.config import UPLOAD_DIR, ALLOWED_VIDEO_TYPES, MAX_VIDEO_MB

router = APIRouter(prefix="/upload", tags=["Upload"])


@router.post("/video")
async def upload_video(file: UploadFile = File(...)):
    # validate content type
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
