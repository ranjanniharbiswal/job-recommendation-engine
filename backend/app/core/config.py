# from pydantic_settings import BaseSettings
# from typing import List


# # class Settings(BaseSettings):
#     # OPENAI_API_KEY: str = ""
#     # ALLOWED_ORIGINS: List[str] = ["http://localhost:3000", "https://your-app.onrender.com"]
#     # FAISS_INDEX_PATH: str = "faiss_index"
#     # EMBEDDING_MODEL: str = "text-embedding-3-small"
#     # LLM_MODEL: str = "gpt-4o"
#     # MAX_TOKENS: int = 1500
# class Settings(BaseSettings):
#     GEMINI_API_KEY: str = ""
#     # ALLOWED_ORIGINS: list = ["http://localhost:3000"]
#     ALLOWED_ORIGINS=["http://localhost:3000","http://127.0.0.1:3000"]
#     LLM_MODEL: str = "gemini-1.5-flash"
#     EMBEDDING_MODEL: str = "models/embedding-001"
#     MAX_TOKENS: int = 1500
#     class Config:
#         env_file = ".env"


# settings = Settings()


# from pydantic_settings import BaseSettings

# class Settings(BaseSettings):
#     GEMINI_API_KEY: str = ""

#     # ALLOWED_ORIGINS: list[str] = [
#     #     "http://localhost:3000",
#     #     "http://127.0.0.1:3000"
#     # ]
#     ALLOWED_ORIGINS: list[str] = [
#         "http://localhost:3000",
#         "http://127.0.0.1:3000"
#     ]
#     LLM_MODEL: str = "gemini-1.5-flash"
#     EMBEDDING_MODEL: str = "models/embedding-001"
#     MAX_TOKENS: int = 1500

#     class Config:
#         env_file = ".env"

# settings = Settings()

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    GEMINI_API_KEY: str

    ALLOWED_ORIGINS: list[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ]

    FAISS_INDEX_PATH: str = "faiss_index"

    LLM_MODEL: str = "gemini-1.5-flash"
    EMBEDDING_MODEL: str = "models/embedding-001"
    MAX_TOKENS: int = 1500

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",      # Ignore unknown env variables
    )


settings = Settings()