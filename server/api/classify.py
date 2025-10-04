from fastapi import APIRouter, HTTPException, File, UploadFile
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import logging
import uuid
from datetime import datetime

# For now, importing mock functions - these will be replaced with real image classification logic
from services.classification_service import classify_flower_image

router = APIRouter()

# Request/Response models
class ClassificationResponse(BaseModel):
    id: str
    filename: str
    timestamp: str
    classification: str
    confidence: float
    location: Optional[Dict[str, float]] = None
    similar_species: List[Dict[str, Any]]

@router.post("/classify", response_model=ClassificationResponse)
async def classify_image(file: UploadFile = File(...)):
    """
    Upload and classify a flower image
    """
    try:
        # Validate file type
        if not file.content_type.startswith("image/"):
            raise HTTPException(status_code=400, detail="Uploaded file must be an image")
        
        result = await classify_flower_image(file)
        return result
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Error classifying image: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")