from pydantic import BaseModel, Field
from typing import Any, Dict, List

class ResearchRequest(BaseModel):
    query: str = Field(min_length=5)
    depth: str = "balanced"
    max_sources: int = Field(default=8, ge=3, le=20)

class Source(BaseModel):
    title: str
    url: str
    snippet: str = ""
    domain: str = ""

class ResearchResult(BaseModel):
    query: str
    plan: List[str]
    sources: List[Source]
    analysis: str
    verification: str
    final_answer: str
    confidence: float
    events: List[Dict[str, Any]]
