import logging
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from langchain_openai import ChatOpenAI

from config import settings
from agents.prediction_agent import run_prediction_orchestration
from services.geojson_service import process_abundance_geojson, get_default_coordinates_for_region

logger = logging.getLogger(__name__)

class ClimatePredictionProcessor:
    @staticmethod
    async def get_prediction_data(region: str, start_date: Optional[str] = None, end_date: Optional[str] = None, climate_data: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Fetch climate and bloom prediction data for a given region using AI agent
        """
        logging.info(f"Fetching prediction data for region: {region}, start_date: {start_date}, end_date: {end_date}")
        
        # Initialize LLM if API key available
        llm = None
        if settings.OPENAI_API_KEY:
            try:
                llm = ChatOpenAI(
                    model="gpt-4o-mini",
                    temperature=0.7,
                    openai_api_key=settings.OPENAI_API_KEY
                )
                logger.info("LLM initialized for prediction")
            except Exception as e:
                logger.error(f"Failed to initialize LLM for prediction: {str(e)}")
        
        # Run prediction orchestration
        prediction_data = await run_prediction_orchestration(
            region=region,
            start_date=start_date,
            end_date=end_date,
            climate_data=climate_data,
            llm=llm
        )
        
        # Process the prediction results into appropriate GeoJSON format
        # Extract date range and corresponding probabilities for spatial visualization
        prediction_dates = prediction_data.get("prediction_dates", [])
        bloom_probabilities = prediction_data.get("bloom_start_probability", [])
        
        # Create abundance data from the prediction results for GeoJSON processing
        abundance_data = []
        for i, date in enumerate(prediction_dates):
            if i < len(bloom_probabilities):
                abundance_data.append({
                    "name": f"{region}_{date}",
                    "abundance": bloom_probabilities[i],
                    "date": date
                })
        
        # Update the heatmap_geojson with processed data
        try:
            processed_geojson = await process_abundance_geojson(region, abundance_data)
            prediction_data["heatmap_geojson"] = processed_geojson
        except Exception as e:
            logger.warning(f"Failed to process GeoJSON with abundance data: {str(e)}, using original")
            # Use default coordinates if processing fails
            default_coords = get_default_coordinates_for_region(region)
            
            # Regenerate heatmap with default coordinates
            features = []
            for i, date in enumerate(prediction_dates):
                if i < len(bloom_probabilities):
                    features.append({
                        "type": "Feature",
                        "properties": {
                            "temperature": prediction_data.get("temperature_forecast", [])[i],
                            "probability": bloom_probabilities[i],
                            "date": date
                        },
                        "geometry": {
                            "type": "Polygon",
                            "coordinates": [default_coords]
                        }
                    })
            
            prediction_data["heatmap_geojson"] = {
                "type": "FeatureCollection",
                "features": features
            }
        
        return prediction_data

# Service function to get prediction data
async def get_prediction_data(region: str, start_date: Optional[str] = None, end_date: Optional[str] = None, climate_data: Optional[Dict] = None) -> Dict[str, Any]:
    """
    Get prediction data for a specific region
    """
    try:
        # Fetch prediction data for the region using AI agent
        prediction_data = await ClimatePredictionProcessor.get_prediction_data(region, start_date, end_date, climate_data)
        
        return prediction_data
    except Exception as e:
        logger.error(f"Error in prediction service: {str(e)}")
        raise