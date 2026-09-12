# import the Groq client and configuration settings
from groq import Groq
from .config import GROQ_API_KEY, GROQ_MODEL

if not GROQ_API_KEY:
    raise RuntimeError("GROQ_API_KEY is missing. Add it to backend/.env")

client = Groq(api_key=GROQ_API_KEY)

def chat(system: str, user: str, temperature: float = 0.2) -> str:
    response = client.chat.completions.create(
        model=GROQ_MODEL,
        temperature=temperature,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user}
        ]
    )
    return response.choices[0].message.content or ""
