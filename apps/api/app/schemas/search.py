from pydantic import BaseModel
from typing import List

class SearchResult(BaseModel):
    type: str # mission, content, memory, attention
    id: str
    title: str
    description: str
    url: str
    updated_at: str

class SearchListResponse(BaseModel):
    results: List[SearchResult]
    total: int
