from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
import logging
from datetime import datetime

from services.prediction_service import get_prediction_data

router = APIRouter()
logger = logging.getLogger(__name__)

# Request/Response models
class PredictionRequest(BaseModel):
    """
    Request model for bloom prediction
    """
    region: str = Field(..., description="Geographic region to predict bloom patterns for", example="Alaska")
    start_date: Optional[str] = Field(None, description="Start date for prediction in YYYY-MM-DD format", example="2025-04-01")
    end_date: Optional[str] = Field(None, description="End date for prediction in YYYY-MM-DD format", example="2025-04-10")
    climate_data: Optional[Dict[str, Any]] = Field(None, description="Optional climate data to inform predictions")

class PredictionResponse(BaseModel):
    """
    Response model for bloom prediction
    """
    region: str
    prediction_dates: List[str]
    temperature_forecast: List[float]
    bloom_start_probability: List[float]
    explanation: str
    heatmap_geojson: Dict[str, Any]

@router.post("/predict", 
             response_model=PredictionResponse,
             summary="Predict bloom patterns",
             description="Get climate and bloom predictions for a specific region using AI agents")
async def predict_bloom_patterns(request: PredictionRequest):
    """
    Get climate and bloom predictions for a specific region using AI agents
    
    This endpoint uses an agentic architecture with:
    - Prediction Agent: Generates climate forecasts and bloom probability predictions
    - Climate models: Analyzes temperature, precipitation, and seasonal patterns
    """
    try:
        # Validate inputs
        if not request.region:
            raise HTTPException(
                status_code=400,
                detail="Region parameter is required"
            )
        
        # Validate date format if provided
        if request.start_date:
            try:
                datetime.strptime(request.start_date, '%Y-%m-%d')
            except ValueError:
                raise HTTPException(
                    status_code=400,
                    detail="start_date must be in YYYY-MM-DD format"
                )
        
        if request.end_date:
            try:
                datetime.strptime(request.end_date, '%Y-%m-%d')
            except ValueError:
                raise HTTPException(
                    status_code=400,
                    detail="end_date must be in YYYY-MM-DD format"
                )
        
        prediction_data = await get_prediction_data(
            region=request.region,
            start_date=request.start_date,
            end_date=request.end_date,
            climate_data=request.climate_data
        )
        
        return PredictionResponse(
            region=prediction_data["region"],
            prediction_dates=prediction_data["prediction_dates"],
            temperature_forecast=prediction_data["temperature_forecast"],
            bloom_start_probability=prediction_data["bloom_start_probability"],
            explanation=prediction_data["explanation"],
            heatmap_geojson=prediction_data["heatmap_geojson"]
        )
    except HTTPException:
        # Re-raise HTTP exceptions as they are
        raise
    except Exception as e:
        logger.error(f"Error in prediction: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate prediction: {str(e)}"
        )

@router.get("/predict", 
            response_model=PredictionResponse,
            summary="Get bloom predictions (GET)",
            description="Get climate and bloom predictions for a specific region (GET endpoint for backward compatibility)")
async def get_prediction(
    region: str = Query(..., description="Region to predict bloom patterns for", example="Alaska"),
    start_date: Optional[str] = Query(None, description="Start date for prediction in YYYY-MM-DD format", example="2025-04-01"),
    end_date: Optional[str] = Query(None, description="End date for prediction in YYYY-MM-DD format", example="2025-04-10")
):
    """
    Get climate and bloom predictions for a specific region (GET endpoint for backward compatibility)
    
    For more control, use the POST /predict endpoint.
    """
    try:
        # Validate inputs
        if not region:
            raise HTTPException(
                status_code=400,
                detail="Region parameter is required"
            )
        
        # Validate date format if provided
        if start_date:
            try:
                datetime.strptime(start_date, '%Y-%m-%d')
            except ValueError:
                raise HTTPException(
                    status_code=400,
                    detail="start_date must be in YYYY-MM-DD format"
                )
        
        if end_date:
            try:
                datetime.strptime(end_date, '%Y-%m-%d')
            except ValueError:
                raise HTTPException(
                    status_code=400,
                    detail="end_date must be in YYYY-MM-DD format"
                )
        
        request = PredictionRequest(
            region=region,
            start_date=start_date,
            end_date=end_date
        )
        return await predict_bloom_patterns(request)
    except HTTPException:
        # Re-raise HTTP exceptions as they are
        raise
    except Exception as e:
        logger.error(f"Error in GET prediction: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate prediction: {str(e)}"
        )