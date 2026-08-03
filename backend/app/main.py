from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import jobs, cover_letter, interview_prep
from app.core.config import settings

app = FastAPI(
    title="AI Job Recommendation Engine",
    description="RAG-powered job matching with GPT-4 / Claude",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(jobs.router, prefix="/api/jobs", tags=["jobs"])
app.include_router(cover_letter.router, prefix="/api/cover-letter", tags=["cover-letter"])
app.include_router(interview_prep.router, prefix="/api/interview-prep", tags=["interview-prep"])


@app.get("/health")
def health():
    return {"status": "ok"}
