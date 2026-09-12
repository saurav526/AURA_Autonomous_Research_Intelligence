import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "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")
GROQ_MODEL = os.getenv("GROQ_MODEL", "openai/gpt-oss-120b")
FRONTEND_ORIGIN = os.getenv("FRONTEND_ORIGIN", "http://localhost:5173")
