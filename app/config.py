# app/config.py
import os

from dotenv import load_dotenv
from pydantic import BaseModel


load_dotenv()


class Settings(BaseModel):
    """Loads settings from environment variables."""

    OPENAI_API_KEY: str = ""
    OPENAI_MODEL_NAME: str = "gpt-4.1"
    CONVEX_BASE_URL: str = ""


settings = Settings(
    OPENAI_API_KEY=os.getenv("OPENAI_API_KEY") or "",
    OPENAI_MODEL_NAME=os.getenv("OPENAI_MODEL_NAME", "gpt-4.1"),
    CONVEX_BASE_URL=os.getenv("CONVEX_BASE_URL") or "",
)

# Fail fast if essential keys are missing
if not settings.OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY environment variable not set.")

if not settings.CONVEX_BASE_URL:
    raise ValueError("CONVEX_BASE_URL environment variable not set.")
