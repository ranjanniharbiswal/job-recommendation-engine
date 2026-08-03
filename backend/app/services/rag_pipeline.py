"""
RAG Pipeline: LangChain + FAISS semantic job matching.

Flow:
  1. Embed resume chunks with OpenAI embeddings
  2. Embed each job description
  3. FAISS vector store for cosine similarity retrieval
  4. GPT-4 scores, explains matches and identifies skill gaps
"""

import json
import re
from typing import List

# from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings

from langchain.schema import Document
from langchain.prompts import ChatPromptTemplate

from app.core.config import settings
from app.models.schemas import JobMatch


MATCH_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """You are a recruitment AI using semantic similarity to match candidates to jobs.
Given a candidate profile and a job description, return a JSON object with:
{{
  "title": "Job title extracted from description",
  "company": "Company name extracted or 'Unknown'",
  "score": <integer 0-100 semantic similarity score>,
  "skills": ["list", "of", "relevant", "skills", "from", "job"],
  "reason": "2-3 sentence explanation of fit",
  "gap": "Key missing skill or experience, or null if none"
}}
Return ONLY the JSON object, no markdown, no preamble."""),
    ("human", "CANDIDATE PROFILE:\n{resume}\n\nJOB DESCRIPTION:\n{job}"),
])


class RAGPipeline:
    def __init__(self):
        # self.embeddings = OpenAIEmbeddings(
        #     model=settings.EMBEDDING_MODEL,
        #     openai_api_key=settings.OPENAI_API_KEY,
        # )
        # self.llm = ChatOpenAI(
        #     model=settings.LLM_MODEL,
        #     temperature=0.2,
        #     openai_api_key=settings.OPENAI_API_KEY,
        # )
        self.embeddings = GoogleGenerativeAIEmbeddings(
            model=settings.EMBEDDING_MODEL,
            google_api_key=settings.GEMINI_API_KEY,
        )
        # self.llm = ChatGoogleGenerativeAI(
        #     model=settings.LLM_MODEL,
        #     google_api_key=settings.GEMINI_API_KEY,
        # )
        self.llm = ChatGoogleGenerativeAI(
            model=settings.LLM_MODEL,
            google_api_key=settings.GEMINI_API_KEY,
            temperature=0.2,
        )

        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50,
        )
        self.chain = MATCH_PROMPT | self.llm

    def _build_resume_store(self, resume: str) -> FAISS:
        """Chunk resume and index into FAISS."""
        chunks = self.splitter.split_text(resume)
        docs = [Document(page_content=c, metadata={"source": "resume"}) for c in chunks]
        return FAISS.from_documents(docs, self.embeddings)

    def _retrieve_relevant_context(self, store: FAISS, query: str, k: int = 3) -> str:
        """Retrieve top-k resume chunks most relevant to the job."""
        results = store.similarity_search(query, k=k)
        return "\n".join(r.page_content for r in results)

    def _parse_match(self, raw: str) -> dict:
        clean = re.sub(r"```json|```", "", raw).strip()
        return json.loads(clean)

    async def match_jobs(self, resume: str, job_descriptions: List[str]) -> List[JobMatch]:
        store = self._build_resume_store(resume)
        matches = []

        for job_text in job_descriptions:
            # Retrieve the most relevant resume context for this specific job
            context = self._retrieve_relevant_context(store, job_text)

            response = await self.chain.ainvoke({
                "resume": context,
                "job": job_text,
            })

            try:
                data = self._parse_match(response.content)
                matches.append(JobMatch(**data))
            except Exception:
                # Fallback: include the job with a low score if parsing fails
                matches.append(JobMatch(
                    title="Unknown Role",
                    company="Unknown",
                    score=0,
                    skills=[],
                    reason="Could not parse match details.",
                    gap=None,
                ))

        # Sort by score descending
        matches.sort(key=lambda m: m.score, reverse=True)
        return matches


rag_pipeline = RAGPipeline()
