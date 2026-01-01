from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes.upload import router as upload_router
from app.api.routes.process import router as process_router
from dotenv import load_dotenv
load_dotenv()

app = FastAPI(
    title="Video to Social AI",
    version="0.1.0"
) 

# register routers AFTER app is created
app.include_router(upload_router)
app.include_router(process_router)
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
