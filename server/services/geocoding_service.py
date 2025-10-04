"""
Geocoding service for converting region names to coordinates
"""
import logging
from typing import Optional, Tuple, Dict, List
import re

logger = logging.getLogger(__name__)

# Database of known regions with coordinates [longitude, latitude]
# This is a fallback when geocoding APIs are not available
REGION_COORDINATES: Dict[str, List[float]] = {
    # India
    "kashmir": [75.0, 34.0],
    "kashmir valley": [74.8, 34.1],
    "srinagar": [74.8, 34.1],
    "kerala": [76.5, 10.5],
    "munnar": [77.06, 10.09],
    "ooty": [76.69, 11.41],
    "uttarakhand": [79.0, 30.3],
    "valley of flowers": [79.6, 30.7],
    "himalayan": [80.0, 30.0],
    "western ghats": [76.0, 15.0],
    "rajasthan": [73.0, 27.0],
    "tamil nadu": [78.0, 11.0],
    "karnataka": [76.0, 15.0],
    "bangalore": [77.6, 12.97],
    "coorg": [75.8, 12.4],
    "sikkim": [88.6, 27.6],
    "assam": [92.9, 26.2],
    "meghalaya": [91.4, 25.5],
    
    # USA
    "california": [-119.4, 36.8],
    "oregon": [-120.5, 44.0],
    "washington": [-120.7, 47.5],
    "texas": [-99.9, 31.5],
    "florida": [-81.5, 28.0],
    "arizona": [-111.7, 34.5],
    "colorado": [-105.5, 39.0],
    "new york": [-75.0, 43.0],
    "vermont": [-72.6, 44.0],
    "alaska": [-152.0, 64.0],
    
    # Japan
    "tokyo": [139.7, 35.7],
    "kyoto": [135.8, 35.0],
    "osaka": [135.5, 34.7],
    "hokkaido": [142.0, 43.0],
    "okinawa": [127.7, 26.3],
    
    # Europe
    "provence": [5.4, 43.9],
    "tuscany": [11.3, 43.4],
    "andalusia": [-4.5, 37.5],
    "netherlands": [5.3, 52.1],
    "scotland": [-4.2, 56.5],
    
    # China
    "yunnan": [101.0, 25.0],
    "sichuan": [103.0, 30.5],
    "tibet": [91.0, 31.0],
    "xinjiang": [87.0, 43.0],
    
    # Other
    "amazon": [-62.0, -3.0],
    "sahara": [9.0, 23.0],
    "madagascar": [46.7, -19.0],
    "new zealand": [174.0, -41.0],
}


def normalize_region_name(name: str) -> str:
    """Normalize region name for matching"""
    return re.sub(r'[^a-z\s]', '', name.lower().strip())


def get_coordinates_from_database(region_name: str, country: Optional[str] = None) -> Optional[List[float]]:
    """
    Get coordinates from the built-in database
    
    Args:
        region_name: Name of the region
        country: Optional country name for context
    
    Returns:
        [longitude, latitude] or None
    """
    normalized = normalize_region_name(region_name)
    
    # Direct match
    if normalized in REGION_COORDINATES:
        return REGION_COORDINATES[normalized]
    
    # Try partial matching
    for key, coords in REGION_COORDINATES.items():
        if normalized in key or key in normalized:
            return coords
    
    # Try matching with country
    if country:
        country_normalized = normalize_region_name(country)
        combined = f"{normalized} {country_normalized}"
        for key, coords in REGION_COORDINATES.items():
            if key in combined or combined in key:
                return coords
    
    return None


def estimate_country_center(country: str) -> Optional[List[float]]:
    """
    Get approximate center coordinates for a country
    
    Args:
        country: Country name
    
    Returns:
        [longitude, latitude] or None
    """
    country_centers = {
        "india": [78.0, 22.0],
        "usa": [-98.0, 39.0],
        "united states": [-98.0, 39.0],
        "china": [104.0, 35.0],
        "japan": [138.0, 36.0],
        "france": [2.3, 46.6],
        "germany": [10.4, 51.1],
        "italy": [12.6, 42.8],
        "spain": [-3.7, 40.4],
        "uk": [-3.4, 55.4],
        "united kingdom": [-3.4, 55.4],
        "australia": [133.8, -25.3],
        "brazil": [-51.9, -14.2],
        "canada": [-106.3, 56.1],
        "mexico": [-102.6, 23.6],
        "russia": [105.3, 61.5],
        "south africa": [25.0, -29.0],
        "netherlands": [5.3, 52.1],
        "switzerland": [8.2, 46.8],
        "austria": [14.6, 47.5],
        "norway": [8.5, 60.5],
        "sweden": [18.6, 60.1],
        "finland": [25.7, 61.9],
    }
    
    normalized = normalize_region_name(country)
    return country_centers.get(normalized)


async def geocode_region(region_name: str, country: Optional[str] = None) -> Optional[List[float]]:
    """
    Get coordinates for a region using various methods
    
    Priority:
    1. Built-in database
    2. Country center estimation
    3. Future: External geocoding API
    
    Args:
        region_name: Name of the region/location
        country: Optional country context
    
    Returns:
        [longitude, latitude] or None
    """
    # Try built-in database first
    coords = get_coordinates_from_database(region_name, country)
    if coords:
        logger.info(f"Found coordinates for {region_name} in database: {coords}")
        return coords
    
    # Try country center as fallback
    if country:
        coords = estimate_country_center(country)
        if coords:
            logger.info(f"Using country center for {region_name}, {country}: {coords}")
            return coords
    
    # Could integrate external geocoding API here (e.g., OpenStreetMap Nominatim)
    # For now, return None
    logger.warning(f"No coordinates found for {region_name}, {country}")
    return None


async def geocode_regions(regions: List[Dict]) -> List[Dict]:
    """
    Add coordinates to a list of regions
    
    Args:
        regions: List of region dictionaries with 'name' and 'country' fields
    
    Returns:
        Updated list with coordinates added
    """
    for region in regions:
        if not region.get('coordinates'):
            coords = await geocode_region(region.get('name', ''), region.get('country'))
            if coords:
                region['coordinates'] = coords
                region['needs_geocoding'] = False
            else:
                region['needs_geocoding'] = True
    
    return regions


def add_region_to_database(region_name: str, longitude: float, latitude: float) -> None:
    """
    Add a new region to the database (for future use/expansion)
    
    Args:
        region_name: Name of the region
        longitude: Longitude coordinate
        latitude: Latitude coordinate
    """
    normalized = normalize_region_name(region_name)
    REGION_COORDINATES[normalized] = [longitude, latitude]
    logger.info(f"Added {region_name} to geocoding database: [{longitude}, {latitude}]")
