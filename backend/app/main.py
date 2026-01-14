from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from app.api.routes.upload import router as upload_router
from app.api.routes.process import router as process_router
from app.api.routes.auth import router as auth_router

from app.db.database import engine
from app.db.models import Base

load_dotenv()

# ✅ Create FastAPI app FIRST
app = FastAPI(
    title="Video to Social AI",
    version="0.1.0"
)

# ✅ Create DB tables
# Base.metadata.create_all(bind=engine)

# ✅ Register routers
app.include_router(upload_router)
app.include_router(process_router)
app.include_router(auth_router)

# ✅ Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"status": "Backend running"}

@app.get("/health")
def health():
    return {"status": "ok"}
