from fastapi import APIRouter, HTTPException, Query, Body
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
import logging

from agents.orchestrator import get_orchestrator
from config import settings

router = APIRouter()

logger = logging.getLogger(__name__)

# Request/Response models
class ExplanationRequest(BaseModel):
    region: str = Field(..., description="Geographic location/region")
    flower: str = Field(..., description="Flower species name")
    coordinates: Optional[tuple] = Field(None, description="(longitude, latitude) coordinates")
    climate_data: Optional[Dict[str, Any]] = Field(None, description="Optional climate data")
    date: Optional[str] = Field(None, description="Optional date string")
    use_mock_search: bool = Field(False, description="Use mock search results for testing")

class FlowerInfo(BaseModel):
    common_name: str
    scientific_name: str

class WebResearchData(BaseModel):
    summary: str
    source_count: int
    sources: List[Dict[str, Any]]

class MetadataResponse(BaseModel):
    timestamp: str
    processing_time_ms: float
    llm_used: bool
    search_available: bool
    error: Optional[str] = None
    fallback: Optional[bool] = None

class ExplanationResponse(BaseModel):
    region: str
    flower: FlowerInfo
    abundance_level: str
    season: str
    climate: str
    known_bloom_period: str
    notes: str
    explanation: str
    factors: List[str]
    web_research: WebResearchData
    metadata: MetadataResponse
    timestamp: str
    processing_time_ms: float

@router.post("/explain", response_model=ExplanationResponse)
async def explain_bloom_patterns(request: ExplanationRequest):
    """
    Generate comprehensive bloom explanation using AI agents
    
    This endpoint uses an agentic architecture with:
    - Master Orchestrator: Coordinates the workflow
    - Explanation Agent: Generates detailed botanical explanations
    - Web Search Agent: Fetches real-time data from SerpAPI and NewsAPI
    
    The agents work concurrently to provide rich, contextual bloom explanations.
    """
    try:
        # Get orchestrator instance
        orchestrator = get_orchestrator(
            openai_api_key=settings.OPENAI_API_KEY,
            serpapi_key=settings.SERPAPI_API_KEY,
            newsapi_key=settings.NEWSAPI_API_KEY,
            timeout=settings.AGENT_TIMEOUT,
            max_search_results=settings.MAX_SEARCH_RESULTS
        )
        
        # Run orchestration
        result = await orchestrator.orchestrate(
            region=request.region,
            flower=request.flower,
            coordinates=request.coordinates,
            climate_data=request.climate_data,
            date=request.date,
            use_mock_search=request.use_mock_search
        )
        
        return result
        
    except Exception as e:
        logger.error(f"Error in bloom explanation: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate explanation: {str(e)}"
        )

@router.get("/explanation", response_model=ExplanationResponse)
async def get_explanation(
    region: str = Query(..., description="Region to explain bloom patterns for"),
    flower: str = Query(..., description="Flower species to explain bloom patterns for"),
    use_mock_search: bool = Query(False, description="Use mock search for testing")
):
    """
    Get ecological explanation for bloom patterns (GET endpoint for backward compatibility)
    
    For more control, use the POST /explain endpoint.
    """
    request = ExplanationRequest(
        region=region,
        flower=flower,
        use_mock_search=use_mock_search
    )
    return await explain_bloom_patterns(request)