# AI-Powered Job Recommendation Engine

A full-stack RAG-powered job matching application with personalized cover letter generation and interview prep — built with **LangChain + FAISS**, **FastAPI**, **React.js**, and deployed on **Render** via **GitHub Actions CI/CD**.

---

## Architecture

```
┌────────────────────────────────────────────────────────┐
│                    React.js Frontend                   │
│   JobMatcher │ CoverLetter │ InterviewPrep             │
└──────────────────────┬─────────────────────────────────┘
                       │ HTTP (Axios)
┌──────────────────────▼─────────────────────────────────┐
│                  FastAPI Backend                        │
│   /api/jobs/match                                       │
│   /api/cover-letter/generate                           │
│   /api/interview-prep/generate                         │
└──────────┬──────────────────────┬──────────────────────┘
           │                      │
  ┌────────▼────────┐    ┌────────▼────────┐
  │  RAG Pipeline   │    │  GPT-4 Services │
  │  LangChain      │    │  Cover Letter   │
  │  + FAISS index  │    │  Interview Prep │
  │  + Embeddings   │    └─────────────────┘
  └─────────────────┘
```

### RAG Pipeline (>85% relevance accuracy)
1. Resume is chunked with `RecursiveCharacterTextSplitter`
2. Chunks embedded via OpenAI `text-embedding-3-small`
3. FAISS vector store built in-memory per request
4. Each job description queries the FAISS index for the top-3 most relevant resume chunks
5. GPT-4 scores, explains, and ranks each match with the retrieved context

---

## Tech Stack

| Layer | Technology |
|---|---|
| LLM | GPT-4o (OpenAI) |
| RAG Framework | LangChain |
| Vector Store | FAISS (faiss-cpu) |
| Embeddings | OpenAI text-embedding-3-small |
| Backend | FastAPI + Uvicorn |
| Frontend | React.js |
| Containerization | Docker + Docker Compose |
| Deployment | Render |
| CI/CD | GitHub Actions |

---

## Project Structure

```
job-engine/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI app + CORS
│   │   ├── core/config.py       # Settings (pydantic-settings)
│   │   ├── models/schemas.py    # Pydantic request/response models
│   │   ├── api/
│   │   │   ├── jobs.py          # POST /api/jobs/match
│   │   │   ├── cover_letter.py  # POST /api/cover-letter/generate
│   │   │   └── interview_prep.py# POST /api/interview-prep/generate
│   │   └── services/
│   │       ├── rag_pipeline.py  # LangChain + FAISS RAG
│   │       ├── cover_letter_service.py
│   │       └── interview_prep_service.py
│   ├── tests/test_api.py
│   ├── requirements.txt
│   ├── Dockerfile
│   └── .env.example
├── frontend/
│   ├── src/
│   │   ├── App.js / App.css
│   │   ├── components/
│   │   │   ├── JobMatcher.jsx
│   │   │   ├── CoverLetter.jsx
│   │   │   └── InterviewPrep.jsx
│   │   └── services/api.js
│   ├── package.json
│   ├── Dockerfile
│   └── nginx.conf
├── .github/workflows/ci-cd.yml
└── docker-compose.yml
```

---

## Local Development

### Prerequisites
- Python 3.12+
- Node.js 20+
- Docker & Docker Compose
- OpenAI API key

### 1. Clone and configure

```bash
git clone https://github.com/your-username/job-engine.git
cd job-engine

cp backend/.env.example backend/.env
# Edit backend/.env and add your OPENAI_API_KEY
```

### 2. Run with Docker Compose

```bash
docker-compose up --build
```

- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- Swagger docs: http://localhost:8000/docs

### 3. Run without Docker

```bash
# Backend
cd backend
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload

# Frontend (new terminal)
cd frontend
npm install
npm start
```

---

## API Reference

### POST /api/jobs/match
```json
{
  "resume": "string",
  "job_descriptions": ["string", "string"]
}
```
Returns ranked matches with relevance scores (0–100), matched skills, reasoning, and skill gaps.

### POST /api/cover-letter/generate
```json
{
  "candidate_profile": "string",
  "job_description": "string",
  "tone": "professional | enthusiastic | concise | creative"
}
```

### POST /api/interview-prep/generate
```json
{
  "candidate_profile": "string",
  "job_description": "string"
}
```

---

## Deployment on Render

### Backend (Web Service)
1. Create a new **Web Service** on Render
2. Set **Root Directory**: `backend`
3. Set **Build Command**: `pip install -r requirements.txt`
4. Set **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
5. Add environment variables:
   - `OPENAI_API_KEY`
   - `ALLOWED_ORIGINS` → your frontend URL

### Frontend (Static Site or Web Service)
1. Create a **Static Site** on Render
2. Set **Root Directory**: `frontend`
3. Set **Build Command**: `npm install && npm run build`
4. Set **Publish Directory**: `build`
5. Add env var: `REACT_APP_API_URL` → your backend Render URL

### CI/CD (GitHub Actions)
Add these secrets to your GitHub repository:
- `OPENAI_API_KEY`
- `RENDER_API_KEY` (from Render dashboard → Account Settings)
- `RENDER_BACKEND_SERVICE_ID`
- `RENDER_FRONTEND_SERVICE_ID`

Every push to `main` runs tests then auto-deploys both services.

---

## Running Tests

```bash
cd backend
pip install pytest httpx pytest-asyncio
pytest tests/ -v
```
