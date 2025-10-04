from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
import logging

from agents.web_search_agent import search_top_regions
from services.geocoding_service import geocode_regions
from config import settings

router = APIRouter()
logger = logging.getLogger(__name__)

# Request/Response models
class RegionInfo(BaseModel):
    """Information about a region with high flower abundance"""
    name: str = Field(..., description="Region name")
    country: str = Field(..., description="Country name")
    full_name: str = Field(..., description="Full region name with country")
    mentions: int = Field(..., description="Number of times mentioned in search results")
    confidence: float = Field(..., description="Confidence score (0-100)")
    coordinates: Optional[List[float]] = Field(None, description="[longitude, latitude] if available")
    needs_geocoding: bool = Field(True, description="Whether coordinates need to be geocoded")
    note: Optional[str] = Field(None, description="Additional notes")

class TopRegionsRequest(BaseModel):
    """Request model for finding top regions"""
    country: str = Field(..., description="Country to search within", example="India")
    flower: str = Field(..., description="Flower species name", example="lotus")
    max_results: int = Field(10, ge=5, le=20, description="Maximum search results to analyze")

class TopRegionsResponse(BaseModel):
    """Response model for top regions"""
    country: str
    flower: str
    top_regions: List[RegionInfo]
    total_sources: int
    extraction_method: str
    ai_summary: Optional[str] = None
    error: Optional[str] = None

@router.post("/top-regions",
             response_model=TopRegionsResponse,
             summary="Find top regions for flower abundance",
             description="Search for regions within a country with highest abundance of a specific flower")
async def get_top_regions(request: TopRegionsRequest):
    """
    Find the top 3-5 regions within a country where a specific flower is most abundant
    
    This endpoint:
    - Searches web sources for information about flower distribution
    - Identifies and ranks regions by mention frequency and relevance
    - Returns region names that can be highlighted on a globe
    """
    try:
        logger.info(f"Searching for top {request.flower} regions in {request.country}")
        
        # Import LLM if available
        llm = None
        if settings.OPENAI_API_KEY:
            try:
                from langchain_openai import ChatOpenAI
                llm = ChatOpenAI(
                    model="gpt-4o-mini",
                    temperature=0.7,
                    openai_api_key=settings.OPENAI_API_KEY
                )
            except Exception as e:
                logger.warning(f"Failed to initialize LLM: {str(e)}")
        
        # Search for top regions
        result = await search_top_regions(
            country=request.country,
            flower=request.flower,
            serpapi_key=settings.SERPAPI_API_KEY,
            newsapi_key=settings.NEWSAPI_API_KEY,
            max_results=request.max_results,
            llm=llm
        )
        
        # Geocode regions to get coordinates
        regions = result.get("top_regions", [])
        if regions:
            regions = await geocode_regions(regions)
            result["top_regions"] = regions
        
        return TopRegionsResponse(
            country=result.get("country", request.country),
            flower=result.get("flower", request.flower),
            top_regions=result.get("top_regions", []),
            total_sources=result.get("total_sources", 0),
            extraction_method=result.get("extraction_method", "text_analysis"),
            ai_summary=result.get("ai_summary"),
            error=result.get("error")
        )
        
    except Exception as e:
        logger.error(f"Error finding top regions: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to find top regions: {str(e)}"
        )

@router.get("/top-regions",
            response_model=TopRegionsResponse,
            summary="Find top regions (GET)",
            description="GET endpoint for finding top regions")
async def get_top_regions_simple(
    country: str = Query(..., description="Country to search within", example="India"),
    flower: str = Query(..., description="Flower species name", example="lotus"),
    max_results: int = Query(10, ge=5, le=20, description="Maximum search results")
):
    """
    GET endpoint for finding top regions (for easier testing)
    """
    request = TopRegionsRequest(
        country=country,
        flower=flower,
        max_results=max_results
    )
    return await get_top_regions(request)
