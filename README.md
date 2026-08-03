# 🚀 AI-Powered Job Recommendation Engine

<p align="center">

![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-green?logo=fastapi)
![React](https://img.shields.io/badge/React-18-61DAFB?logo=react)
![LangChain](https://img.shields.io/badge/LangChain-RAG-success)
![Gemini](https://img.shields.io/badge/Google-Gemini-orange?logo=google)
![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED?logo=docker)
![FAISS](https://img.shields.io/badge/FAISS-Vector%20Search-purple)
![License](https://img.shields.io/badge/License-MIT-blue)

</p>

An AI-powered career assistant that helps candidates:

- 🔍 Match resumes against multiple job descriptions using **RAG + FAISS**
- ✍️ Generate personalized cover letters
- 🎯 Generate interview questions tailored to a specific role
- 🤖 Powered by **Google Gemini**, **LangChain**, **FastAPI**, and **React**

---

# ✨ Features

### 🔍 AI Job Matching

- Resume semantic search using FAISS
- Gemini-powered job relevance scoring
- Skill gap identification
- Match explanation
- Ranked recommendations

---

### ✍️ AI Cover Letter Generator

- Personalized cover letters
- Multiple writing tones
- ATS-friendly language
- Job-specific customization

---

### 🎤 AI Interview Preparation

- Technical interview questions
- HR interview questions
- Scenario-based questions
- Project-based questions
- Role-specific preparation

---

# 🏗️ System Architecture

```
                        React Frontend
                               │
                        Axios / REST API
                               │
                    FastAPI Backend (Python)
          ┌────────────────────┼────────────────────┐
          │                    │                    │
     Job Matcher         Cover Letter        Interview Prep
          │
          ▼
      RAG Pipeline
          │
 ┌─────────────────────┐
 │ LangChain           │
 │ Recursive Splitter  │
 │ Gemini Embeddings   │
 │ FAISS Vector Store  │
 └─────────────────────┘
          │
          ▼
 Google Gemini 3.5 Flash
```

---

# 🧠 RAG Workflow

1️⃣ Resume is split into semantic chunks

2️⃣ Chunks are converted into vector embeddings using

```
models/gemini-embedding-001
```

3️⃣ FAISS creates an in-memory vector database

4️⃣ Every job description retrieves the most relevant resume chunks

5️⃣ Gemini analyzes:

- Resume
- Job Description
- Retrieved Context

6️⃣ Returns

- ✅ Match Score
- ✅ Matching Skills
- ✅ Skill Gaps
- ✅ AI Explanation

---

# 🛠 Tech Stack

| Category | Technology |
|-----------|------------|
| 🤖 LLM | Google Gemini 3.5 Flash |
| 🧠 Embeddings | Gemini Embedding 001 |
| 🔎 RAG | LangChain |
| 📚 Vector Database | FAISS |
| ⚡ Backend | FastAPI |
| 🎨 Frontend | React.js |
| 🐳 Containerization | Docker |
| 🔄 API | REST |
| 📦 Package Manager | npm + pip |
| ☁️ Deployment | Render |
| 🚀 CI/CD | GitHub Actions |

---

# 📂 Project Structure

```
job-engine/

├── backend
│   ├── app
│   │   ├── api
│   │   ├── core
│   │   ├── models
│   │   ├── services
│   │   └── main.py
│   │
│   ├── tests
│   ├── requirements.txt
│   ├── Dockerfile
│   └── .env.example
│
├── frontend
│   ├── src
│   ├── public
│   ├── Dockerfile
│   └── nginx.conf
│
├── docker-compose.yml
├── README.md
└── .github/workflows
```

---

# ⚙️ Installation

## Clone Repository

```bash
git clone https://github.com/<your-username>/job-engine.git

cd job-engine
```

---

## Configure Environment

Create

```
backend/.env
```

Example

```env
GEMINI_API_KEY=YOUR_GEMINI_API_KEY

LLM_MODEL=models/gemini-3.5-flash

EMBEDDING_MODEL=models/gemini-embedding-001

ALLOWED_ORIGINS=["http://localhost:3000"]

MAX_TOKENS=1500
```

---

## Run using Docker

```bash
docker compose up --build
```

---

Frontend

```
http://localhost:3000
```

Backend

```
http://localhost:8000
```

Swagger

```
http://localhost:8000/docs
```

---

# 📡 REST APIs

## 🔍 Match Jobs

```
POST /api/jobs/match
```

```json
{
  "resume":"...",
  "job_descriptions":[
    "...",
    "..."
  ]
}
```

---

## ✍️ Generate Cover Letter

```
POST /api/cover-letter/generate
```

```json
{
    "candidate_profile":"...",
    "job_description":"...",
    "tone":"professional"
}
```

---

## 🎤 Interview Preparation

```
POST /api/interview-prep/generate
```

```json
{
    "candidate_profile":"...",
    "job_description":"..."
}
```

---

# 🐳 Docker

```bash
docker compose up --build
```

Stop

```bash
docker compose down
```

---

# ☁️ Deployment

Deploy easily on

- Render
- Railway
- Azure
- AWS
- Google Cloud

---

# 🔄 GitHub Actions CI/CD

Every push to the **main** branch automatically

- ✅ Runs tests
- ✅ Builds Docker image
- ✅ Deploys application
- ✅ Updates Render service

---

# 📸 Screenshots

| Feature | Screenshot |
|----------|------------|
| 🔍 Job Matcher | Add Screenshot |
| ✍️ Cover Letter | Add Screenshot |
| 🎤 Interview Prep | Add Screenshot |

---

# 🎯 Future Improvements

- 📄 Resume PDF Upload

- 🧠 Resume Parsing

- 🌍 LinkedIn Profile Analysis

- 📈 ATS Resume Score

- 🎙 Mock Interview

- 🔊 Voice Interview

- 📊 Candidate Analytics Dashboard

- 🌐 Multi-language Support

---

# 👨‍💻 Author

**Nihar**

Java Backend Developer | AI Enthusiast

GitHub:
https://github.com/<your-username>

LinkedIn:
https://linkedin.com/in/<your-linkedin>

---

⭐ If you found this project useful, don't forget to Star the repository.