import logging
import httpx
from fastapi import HTTPException, status

import backend.app.utils.config as config

logger = logging.getLogger(__name__)


class SearchService:
    """Service for performing Google searches via Serper API."""

    @staticmethod
    async def search(query: str, num_results: int = 5) -> dict:
        """
        Search Google via Serper API.

        Args:
            query: Search query string
            num_results: Number of results to return (1-10)

        Returns:
            dict with search results and metadata
        """
        api_key = config.SERPER_API_KEY
        api_url = config.SERPER_API_URL

        if not api_key:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail={
                    "error": "Serper API Not Configured",
                    "message": "SERPER_API_KEY is not set. Please add it to your .env file."
                }
            )

        num_results = max(1, min(num_results, 10))

        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.post(
                    api_url,
                    json={
                        "q": query,
                        "num": num_results
                    },
                    headers={
                        "X-API-KEY": api_key,
                        "Content-Type": "application/json"
                    }
                )

                if response.status_code != 200:
                    logger.error(f"Serper API error: {response.status_code} - {response.text}")
                    raise HTTPException(
                        status_code=status.HTTP_502_BAD_GATEWAY,
                        detail={
                            "error": "Search API Error",
                            "message": f"Serper API returned status {response.status_code}"
                        }
                    )

                data = response.json()

                results = []
                for item in data.get("organic", []):
                    results.append({
                        "title": item.get("title", ""),
                        "link": item.get("link", ""),
                        "snippet": item.get("snippet", ""),
                        "position": item.get("position", 0)
                    })

                return {
                    "query": query,
                    "total_results": len(results),
                    "results": results,
                    "search_information": {
                        "total_results": data.get("searchInformation", {}).get("totalResults", "0"),
                        "search_time": data.get("searchInformation", {}).get("formattedSearchTime", "")
                    }
                }

        except httpx.TimeoutException:
            logger.error("Serper API request timed out")
            raise HTTPException(
                status_code=status.HTTP_504_GATEWAY_TIMEOUT,
                detail={
                    "error": "Search Timeout",
                    "message": "The search request timed out. Please try again."
                }
            )
        except httpx.RequestError as e:
            logger.error(f"Serper API request failed: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail={
                    "error": "Search Service Error",
                    "message": f"Failed to connect to search service: {str(e)}"
                }
            )
