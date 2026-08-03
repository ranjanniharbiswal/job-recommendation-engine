from fastapi import APIRouter, HTTPException
from app.models.schemas import CoverLetterRequest, CoverLetterResponse
from app.services.cover_letter_service import cover_letter_service

router = APIRouter()


@router.post("/generate", response_model=CoverLetterResponse)
async def generate_cover_letter(request: CoverLetterRequest):
    """
    Generate a personalized cover letter using GPT-4.
    """
    if not request.candidate_profile.strip() or not request.job_description.strip():
        raise HTTPException(status_code=400, detail="Profile and job description are required.")

    try:
        letter = await cover_letter_service.generate(
            profile=request.candidate_profile,
            job=request.job_description,
            tone=request.tone or "professional",
        )
        return CoverLetterResponse(cover_letter=letter)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
