from fastapi import APIRouter, HTTPException
from app.models.schemas import MatchRequest, MatchResponse
from app.services.rag_pipeline import rag_pipeline

router = APIRouter()


@router.post("/match", response_model=MatchResponse)
async def match_jobs(request: MatchRequest):
    """
    Semantic job matching via RAG pipeline (LangChain + FAISS).
    Accepts a resume and list of job descriptions.
    Returns ranked matches with relevance scores.
    """
    if not request.resume.strip():
        raise HTTPException(status_code=400, detail="Resume cannot be empty.")
    if not request.job_descriptions:
        raise HTTPException(status_code=400, detail="At least one job description is required.")
    if len(request.job_descriptions) > 10:
        raise HTTPException(status_code=400, detail="Maximum 10 job descriptions per request.")

    try:
        matches = await rag_pipeline.match_jobs(request.resume, request.job_descriptions)
        return MatchResponse(matches=matches)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
