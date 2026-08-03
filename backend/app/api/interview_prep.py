from fastapi import APIRouter, HTTPException
from app.models.schemas import InterviewPrepRequest, InterviewPrepResponse
from app.services.interview_prep_service import interview_prep_service

router = APIRouter()


@router.post("/generate", response_model=InterviewPrepResponse)
async def generate_interview_questions(request: InterviewPrepRequest):
    """
    Generate tailored interview questions using GPT-4.
    """
    if not request.candidate_profile.strip() or not request.job_description.strip():
        raise HTTPException(status_code=400, detail="Profile and job description are required.")

    try:
        categories = await interview_prep_service.generate(
            profile=request.candidate_profile,
            job=request.job_description,
        )
        return InterviewPrepResponse(categories=categories)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
