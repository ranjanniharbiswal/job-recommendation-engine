import pytest
from httpx import AsyncClient, ASGITransport
from unittest.mock import AsyncMock, patch
from app.main import app
from app.models.schemas import JobMatch

@pytest.mark.asyncio
async def test_health():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        r = await client.get("/health")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}


@pytest.mark.asyncio
async def test_match_jobs_validation():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        r = await client.post("/api/jobs/match", json={"resume": "", "job_descriptions": []})
    assert r.status_code == 400


@pytest.mark.asyncio
async def test_cover_letter_validation():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        r = await client.post("/api/cover-letter/generate", json={"candidate_profile": "", "job_description": ""})
    assert r.status_code == 400


@pytest.mark.asyncio
async def test_match_jobs_mock():
    mock_matches = [
        {
            "title": "ML Engineer",
            "company": "Acme Corp",
            "score": 88,
            "skills": ["Python", "LangChain"],
            "reason": "Strong match on ML stack.",
            "gap": None,
        }
    ]
    with patch("app.api.jobs.rag_pipeline.match_jobs", new=AsyncMock(return_value=[
        # type("JobMatch", (), m)()
        JobMatch(**m) for m in mock_matches
    ])):
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            r = await client.post("/api/jobs/match", json={
                "resume": "Python developer with ML experience.",
                "job_descriptions": ["ML Engineer at Acme Corp — requires Python, LangChain."],
            })
    assert r.status_code == 200
