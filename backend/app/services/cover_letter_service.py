# from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings

from langchain.prompts import ChatPromptTemplate
from app.core.config import settings

COVER_LETTER_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """You are an expert career coach and cover letter writer.
Write a compelling, personalized cover letter (3-4 paragraphs, ~250 words) for the candidate.
- Be specific about the candidate's skills and how they match the role
- Avoid clichés and generic filler
- Sound confident and human, not robotic
- Start directly with "Dear Hiring Manager,"
- End with a strong closing sentence and "Sincerely, [Candidate Name]"
Tone: {tone}"""),
    ("human", "CANDIDATE PROFILE:\n{profile}\n\nJOB DESCRIPTION:\n{job}"),
])


class CoverLetterService:
    def __init__(self):
        # self.llm = ChatOpenAI(
        #     model=settings.LLM_MODEL,
        #     temperature=0.7,
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
        self.chain = COVER_LETTER_PROMPT | self.llm

    async def generate(self, profile: str, job: str, tone: str = "professional") -> str:
        response = await self.chain.ainvoke({
            "profile": profile,
            "job": job,
            "tone": tone,
        })
        return response.content


cover_letter_service = CoverLetterService()
