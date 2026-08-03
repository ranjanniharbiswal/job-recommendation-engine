from pydantic import BaseModel
from typing import List, Optional


class MatchRequest(BaseModel):
    resume: str
    job_descriptions: List[str]

class JobMatch(BaseModel):
    title: str
    company: str
    score: float
    skills: List[str]
    reason: str
    gap: Optional[str] = None

class MatchResponse(BaseModel):
    matches: List[JobMatch]


class CoverLetterRequest(BaseModel):
    candidate_profile: str
    job_description: str
    tone: Optional[str] = "professional"

class CoverLetterResponse(BaseModel):
    cover_letter: str


class InterviewPrepRequest(BaseModel):
    candidate_profile: str
    job_description: str

class InterviewCategory(BaseModel):
    name: str
    questions: List[str]

class InterviewPrepResponse(BaseModel):
    categories: List[InterviewCategory]
