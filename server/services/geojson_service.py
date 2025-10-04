"""
GeoJSON Processing Service - Handles creation and manipulation of GeoJSON data for map visualization
"""
import logging
from typing import Dict, Any, List, Optional
from shapely.geometry import Point, Polygon, mapping
from shapely.ops import unary_union
import numpy as np
from config import settings

logger = logging.getLogger(__name__)

class GeoJSONProcessor:
    """
    Service class for handling GeoJSON operations
    """
    
    @staticmethod
    def create_point_geojson(longitude: float, latitude: float, properties: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Create a GeoJSON point feature
        """
        point = Point(longitude, latitude)
        
        feature = {
            "type": "Feature",
            "geometry": mapping(point),
            "properties": properties or {}
        }
        
        return feature
    
    @staticmethod
    def create_polygon_geojson(coordinates: List[List[List[float]]], properties: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Create a GeoJSON polygon feature
        coordinates format: [[[lon, lat], ...], [[lon, lat], ...]] for outer and inner rings
        """
        polygon = Polygon(shell=coordinates[0], holes=coordinates[1:] if len(coordinates) > 1 else [])
        
        feature = {
            "type": "Feature",
            "geometry": mapping(polygon),
            "properties": properties or {}
        }
        
        return feature
    
    @staticmethod
    def create_feature_collection(features: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Create a GeoJSON FeatureCollection
        """
        return {
            "type": "FeatureCollection",
            "features": features
        }
    
    @staticmethod
    def generate_grid_geojson(region_bounds: Dict[str, float], cell_size: float = 0.1) -> Dict[str, Any]:
        """
        Generate a grid of polygons covering a region for visualization purposes
        region_bounds: {min_lat, max_lat, min_lon, max_lon}
        """
        min_lat = region_bounds['min_lat']
        max_lat = region_bounds['max_lat']
        min_lon = region_bounds['min_lon']
        max_lon = region_bounds['max_lon']
        
        # Generate grid cells
        lon_range = np.arange(min_lon, max_lon, cell_size)
        lat_range = np.arange(min_lat, max_lat, cell_size)
        
        features = []
        for lon in lon_range:
            for lat in lat_range:
                # Create a square polygon for each grid cell
                cell_coords = [
                    [lon, lat],
                    [lon + cell_size, lat],
                    [lon + cell_size, lat + cell_size],
                    [lon, lat + cell_size],
                    [lon, lat]  # Close the polygon
                ]
                
                feature = GeoJSONProcessor.create_polygon_geojson([cell_coords], {
                    "id": f"cell_{lon}_{lat}",
                    "value": np.random.random()  # Random value for demonstration
                })
                features.append(feature)
        
        return GeoJSONProcessor.create_feature_collection(features)
    
    @staticmethod
    def merge_adjacent_polygons(features: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Merge adjacent polygons in a list of features
        """
        polygons = []
        for feature in features:
            if feature['geometry']['type'] == 'Polygon':
                # Convert GeoJSON coordinates to Shapely polygon
                poly = Polygon(feature['geometry']['coordinates'][0])
                polygons.append(poly)
        
        if not polygons:
            return features
        
        # Merge all polygons
        merged = unary_union(polygons)
        
        # Convert back to GeoJSON format
        if hasattr(merged, 'geoms'):  # MultiPolygon
            merged_features = []
            for poly in merged.geoms:
                # Create a new feature for each merged polygon
                feature = {
                    "type": "Feature",
                    "geometry": mapping(poly),
                    "properties": {"merged": True}
                }
                merged_features.append(feature)
            return merged_features
        else:  # Single polygon
            return [{
                "type": "Feature",
                "geometry": mapping(merged),
                "properties": {"merged": True}
            }]
    
    @staticmethod
    def add_abundance_values_to_geojson(geojson_data: Dict[str, Any], abundance_values: List[float], 
                                      property_name: str = "abundance") -> Dict[str, Any]:
        """
        Add abundance values to GeoJSON features
        """
        if geojson_data['type'] != 'FeatureCollection':
            raise ValueError("Input must be a FeatureCollection")
        
        if len(geojson_data['features']) != len(abundance_values):
            raise ValueError("Number of features must match number of abundance values")
        
        for i, feature in enumerate(geojson_data['features']):
            feature['properties'][property_name] = abundance_values[i]
        
        return geojson_data
    
    @staticmethod
    def validate_geojson(geojson_data: Dict[str, Any]) -> bool:
        """
        Basic validation of GeoJSON structure
        """
        if not isinstance(geojson_data, dict):
            return False
        
        geom_types = ['Point', 'LineString', 'Polygon', 'MultiPoint', 
                     'MultiLineString', 'MultiPolygon', 'GeometryCollection']
        
        if geojson_data.get('type') == 'FeatureCollection':
            if 'features' not in geojson_data:
                return False
            for feature in geojson_data['features']:
                if not GeoJSONProcessor.validate_geojson(feature):
                    return False
            return True
        elif geojson_data.get('type') == 'Feature':
            if 'geometry' not in geojson_data:
                return False
            return GeoJSONProcessor.validate_geojson(geojson_data['geometry'])
        elif geojson_data.get('type') in geom_types:
            if 'coordinates' not in geojson_data:
                return False
            return True
        else:
            return False

# Service functions
async def process_abundance_geojson(region: str, abundance_data: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Process abundance data into a GeoJSON format suitable for visualization
    """
    logger.info(f"Processing abundance GeoJSON for region: {region}")
    
    try:
        features = []
        for item in abundance_data:
            # Create polygon from coordinates if available, otherwise use point
            if 'coordinates' in item:
                feature = GeoJSONProcessor.create_polygon_geojson(
                    [item['coordinates']], 
                    {"abundance": item.get('abundance', 0.5), "name": item.get('name', region)}
                )
            else:
                # If no coordinates, create a default polygon for the region
                default_coords = get_default_coordinates_for_region(region)
                feature = GeoJSONProcessor.create_polygon_geojson(
                    [default_coords], 
                    {"abundance": item.get('abundance', 0.5), "name": item.get('name', region)}
                )
            
            features.append(feature)
        
        return GeoJSONProcessor.create_feature_collection(features)
    except Exception as e:
        logger.error(f"Error processing abundance GeoJSON: {str(e)}")
        raise

def get_default_coordinates_for_region(region: str) -> List[List[float]]:
    """
    Get default coordinates for common regions
    """
    region_coords = {
        "kerala": [[76.0, 8.0], [77.5, 8.0], [77.5, 12.5], [76.0, 12.5], [76.0, 8.0]],
        "alaska": [[-170.0, 50.0], [-130.0, 50.0], [-130.0, 72.0], [-170.0, 72.0], [-170.0, 50.0]],
        "hawaii": [[-161.0, 18.5], [-154.5, 18.5], [-154.5, 22.5], [-161.0, 22.5], [-161.0, 18.5]],
        "california": [[-125.0, 32.0], [-114.0, 32.0], [-114.0, 42.5], [-125.0, 42.5], [-125.0, 32.0]]
    }
    
    return region_coords.get(region.lower(), [[0.0, 0.0], [1.0, 0.0], [1.0, 1.0], [0.0, 1.0], [0.0, 0.0]])

async def validate_and_format_geojson(geojson_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate and ensure the GeoJSON conforms to requirements
    """
    if not GeoJSONProcessor.validate_geojson(geojson_data):
        raise ValueError("Invalid GeoJSON format")
    
    return geojson_data