from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import logging

# For now, importing mock functions - these will be replaced with real NASA API integration
from services.ndvi_service import get_abundance_data

router = APIRouter()

# Request/Response models
class AbundanceRequest(BaseModel):
    region: str
    flower: str
    start_date: Optional[str] = None
    end_date: Optional[str] = None

class AbundanceResponse(BaseModel):
    region: str
    flower: str
    ndvi_data: Dict[str, Any]  # GeoJSON structure
    abundance_grid: Dict[str, Any]

@router.get("/abundance", response_model=AbundanceResponse)
async def get_abundance(
    region: str = Query(..., description="Region to analyze"),
    flower: str = Query(..., description="Flower species to track"),
    start_date: Optional[str] = Query(None, description="Start date in YYYY-MM-DD format"),
    end_date: Optional[str] = Query(None, description="End date in YYYY-MM-DD format")
):
    """
    Get NDVI abundance data for a specific region and flower species
    """
    try:
        result = await get_abundance_data(region, flower, start_date, end_date)
        return result
    except Exception as e:
        logging.error(f"Error retrieving abundance data: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")