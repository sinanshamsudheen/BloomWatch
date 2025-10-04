from pydantic import BaseModel
from typing import List, Dict, Optional, Any
from datetime import datetime

class Region(BaseModel):
    id: str
    name: str
    coordinates: List[float]  # [longitude, latitude]
    bounds: Optional[Dict[str, float]] = None  # {min_lat, max_lat, min_lon, max_lon}
    description: Optional[str] = None

class Flower(BaseModel):
    id: str
    name: str
    scientific_name: Optional[str] = None
    common_names: List[str] = []
    bloom_period: Optional[str] = None
    habitat: Optional[str] = None
    description: Optional[str] = None

class NDVIData(BaseModel):
    region: str
    date: str
    ndvi_values: List[List[float]]
    metadata: Optional[Dict[str, Any]] = None

class AbundanceData(BaseModel):
    region: str
    flower: str
    abundance_values: List[List[int]]
    ndvi_data: Optional[NDVIData] = None
    timestamp: datetime
    metadata: Optional[Dict[str, Any]] = None

class ClassificationResult(BaseModel):
    id: str
    filename: str
    classification: str
    confidence: float
    timestamp: datetime
    location: Optional[Dict[str, float]] = None
    similar_species: List[Dict[str, Any]] = []