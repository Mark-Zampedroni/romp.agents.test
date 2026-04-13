from pydantic import BaseModel
from typing import List, Optional

class DocumentUpload(BaseModel):
    """Document upload metadata."""
    filename: str
    content: str

class QueryRequest(BaseModel):
    """Query request for RAG."""
    query: str
    top_k: int = 5

class QueryResponse(BaseModel):
    """Query response with relevant chunks."""
    query: str
    results: List[dict]
    answer: str

class HealthResponse(BaseModel):
    """Health check response."""
    status: str
    document_count: int
