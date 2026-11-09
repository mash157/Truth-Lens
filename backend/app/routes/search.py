from fastapi import APIRouter
from pydantic import BaseModel, Field
from backend.app.services.search import SearchService

router = APIRouter()


class SearchRequest(BaseModel):
    """Request model for search endpoint."""
    query: str = Field(..., min_length=1, max_length=500, description="Search query")
    num_results: int = Field(5, ge=1, le=10, description="Number of results (1-10)")


class SearchResult(BaseModel):
    """Single search result."""
    title: str
    link: str
    snippet: str
    position: int


class SearchResponse(BaseModel):
    """Response model for search endpoint."""
    query: str
    total_results: int
    results: list[SearchResult]
    search_information: dict


@router.post("/search", response_model=SearchResponse)
async def search_google(request: SearchRequest):
    """
    Search Google via Serper API.

    Use this endpoint to find supporting or opposing sources for news articles.
    """
    result = await SearchService.search(
        query=request.query,
        num_results=request.num_results
    )
    return result
