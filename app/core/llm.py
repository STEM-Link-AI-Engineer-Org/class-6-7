from langchain_openai import ChatOpenAI

from app.config import settings

llm = ChatOpenAI(model=settings.OPENAI_MODEL_NAME, api_key=settings.OPENAI_API_KEY)
