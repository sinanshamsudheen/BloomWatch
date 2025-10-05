from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
import logging
from datetime import datetime

from services.prediction_service import get_prediction_data

router = APIRouter()
logger = logging.getLogger(__name__)

class MonthlyPredictionRequest(BaseModel):
    """
    Request model for monthly bloom probability prediction
    """
    region: str = Field(..., description="Geographic region to predict bloom patterns for", example="California")
    flower: str = Field(..., description="Flower species to predict bloom patterns for", example="Lupine")
    climate_data: Optional[Dict[str, Any]] = Field(None, description="Optional climate data to inform predictions")

class MonthlyPredictionResponse(BaseModel):
    """
    Response model for monthly bloom probability prediction
    """
    region: str
    flower: str
    month_probabilities: List[Dict[str, Any]]  # List of {month: str, probability: float}
    factors: Dict[str, float]  # Factors affecting bloom probability with confidence scores
    prediction_summary: str  # AI-generated summary of predictions
    top_months: List[str]  # Top 4 months with highest bloom probability

@router.post("/monthly-predictions", 
             response_model=MonthlyPredictionResponse,
             summary="Predict bloom probability by month",
             description="Get bloom probability predictions by month for a specific region and flower")
async def get_monthly_predictions(request: MonthlyPredictionRequest):
    """
    Get bloom probability predictions by month for a specific region and flower
    """
    try:
        # Validate inputs
        if not request.region:
            raise HTTPException(
                status_code=400,
                detail="Region parameter is required"
            )
        
        if not request.flower:
            raise HTTPException(
                status_code=400,
                detail="Flower parameter is required"
            )
        
        # For now, return mock data that matches the structure needed by the frontend
        # In a real implementation, this would call ML models to generate actual predictions
        
        # Generate mock monthly probability data
        month_names = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", 
                      "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        # Mock probabilities - higher in spring/summer months for temperate flowers
        mock_probabilities = [0.1, 0.2, 0.4, 0.8, 0.9, 0.85, 
                             0.7, 0.5, 0.3, 0.2, 0.1, 0.1]
        
        month_probabilities = []
        for i, month in enumerate(month_names):
            month_probabilities.append({
                "month": month,
                "probability": mock_probabilities[i]
            })
        
        # Sort months by probability to find top 4
        sorted_months = sorted(month_probabilities, key=lambda x: x["probability"], reverse=True)
        top_months = [item["month"] for item in sorted_months[:4]]
        
        # Mock factors affecting bloom probability
        factors = {
            "Temperature": 0.8,
            "Precipitation": 0.7,
            "Day Length": 0.6,
            "Soil Moisture": 0.5,
            "Previous Blooms": 0.9,
        }
        
        # Mock prediction summary
        prediction_summary = f"Based on historical patterns and current environmental conditions, the bloom probability for {request.flower} is highest during spring months (April-May) in {request.region}. The optimal conditions include temperatures between 15-22°C and adequate precipitation. The model predicts the peak bloom period will occur in May with a probability of 90%."
        
        return MonthlyPredictionResponse(
            region=request.region,
            flower=request.flower,
            month_probabilities=month_probabilities,
            factors=factors,
            prediction_summary=prediction_summary,
            top_months=top_months
        )
    except HTTPException:
        # Re-raise HTTP exceptions as they are
        raise
    except Exception as e:
        logger.error(f"Error in monthly prediction: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate monthly prediction: {str(e)}"
        )