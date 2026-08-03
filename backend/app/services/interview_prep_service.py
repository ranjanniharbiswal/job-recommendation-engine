import json
import re
# from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings

from langchain.prompts import ChatPromptTemplate
from app.core.config import settings
from app.models.schemas import InterviewCategory

PREP_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """You are a senior technical interviewer and career coach.
Generate 8 tailored interview questions for this candidate applying to this role.
Return ONLY valid JSON, no markdown, no preamble:
{{
  "categories": [
    {{
      "name": "Behavioral",
      "questions": ["Question 1?", "Question 2?", "Question 3?"]
    }},
    {{
      "name": "Technical",
      "questions": ["Question 1?", "Question 2?", "Question 3?"]
    }},
    {{
      "name": "Situational",
      "questions": ["Question 1?", "Question 2?"]
    }}
  ]
}}
Make questions specific to the candidate's background and the role requirements."""),
    ("human", "CANDIDATE:\n{profile}\n\nROLE:\n{job}"),
])


class InterviewPrepService:
    def __init__(self):
        # self.llm = ChatOpenAI(
        #     model=settings.LLM_MODEL,
        #     temperature=0.5,
        #     max_tokens=settings.MAX_TOKENS,
        #     openai_api_key=settings.OPENAI_API_KEY,
        # )
        self.embeddings = GoogleGenerativeAIEmbeddings(
            model=settings.EMBEDDING_MODEL,
            google_api_key=settings.GEMINI_API_KEY,
        )
        self.llm = ChatGoogleGenerativeAI(
            model=settings.LLM_MODEL,
            google_api_key=settings.GEMINI_API_KEY,
        )
        self.chain = PREP_PROMPT | self.llm

    async def generate(self, profile: str, job: str) -> list[InterviewCategory]:
        response = await self.chain.ainvoke({"profile": profile, "job": job})
        clean = re.sub(r"```json|```", "", response.content).strip()
        data = json.loads(clean)
        return [InterviewCategory(**cat) for cat in data.get("categories", [])]


interview_prep_service = InterviewPrepService()
