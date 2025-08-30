from pydantic import BaseModel
from typing import List, Optional

class SummarizeRequest(BaseModel):
    text: str
    language: str = "th"
    max_tokens: int = 300
    sources: Optional[List[str]] = None

class SummaryResult(BaseModel):
    title: str = ""
    summary: str
    bullet_points: List[str] = []
    sources: List[str] = []

class QARequest(BaseModel):
    query: str
    top_k: int = 4

class QAResult(BaseModel):
    answer: str
    references: List[str] = []
