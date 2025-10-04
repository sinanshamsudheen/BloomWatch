"""
Explanation Agent - Generates detailed bloom explanations using LLM
"""
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime
from crewai import Agent, Task
from langchain_openai import ChatOpenAI

logger = logging.getLogger(__name__)


def get_abundance_level(ndvi_score: float) -> str:
    """Convert NDVI score to qualitative abundance level"""
    if ndvi_score >= 0.7:
        return "high"
    elif ndvi_score >= 0.4:
        return "medium"
    else:
        return "low"


def get_current_season() -> str:
    """Determine current season based on month"""
    month = datetime.now().month
    if month in [3, 4, 5]:
        return "Spring"
    elif month in [6, 7, 8]:
        return "Summer"
    elif month in [9, 10, 11]:
        return "Autumn"
    else:
        return "Winter"


# Flower database for quick reference with climate requirements
FLOWER_DATABASE = {
    "rose": {
        "scientific": "Rosa", 
        "bloom_period": "May to September",
        "climate": "temperate",
        "regions": "worldwide"
    },
    "rhododendron": {
        "scientific": "Rhododendron arboreum", 
        "bloom_period": "March to May",
        "climate": "cool temperate, mountainous",
        "regions": "Himalayas, high altitude"
    },
    "sunflower": {
        "scientific": "Helianthus annuus", 
        "bloom_period": "June to September",
        "climate": "temperate to warm",
        "regions": "worldwide"
    },
    "tulip": {
        "scientific": "Tulipa", 
        "bloom_period": "March to May",
        "climate": "cold temperate (requires winter chill)",
        "regions": "Kashmir, Netherlands, cold regions",
        "note": "Requires cold winter temperatures (vernalization). Not native to tropical regions."
    },
    "cherry blossom": {
        "scientific": "Prunus serrulata", 
        "bloom_period": "March to April",
        "climate": "temperate",
        "regions": "Japan, Korea, temperate zones"
    },
    "lotus": {
        "scientific": "Nelumbo nucifera", 
        "bloom_period": "June to August",
        "climate": "tropical to subtropical",
        "regions": "Asia, tropical wetlands"
    },
    "jasmine": {
        "scientific": "Jasminum", 
        "bloom_period": "June to September",
        "climate": "tropical to subtropical",
        "regions": "India, Southeast Asia, tropical"
    },
    "marigold": {
        "scientific": "Tagetes", 
        "bloom_period": "July to October",
        "climate": "tropical to temperate",
        "regions": "worldwide"
    },
    "lavender": {
        "scientific": "Lavandula", 
        "bloom_period": "June to August",
        "climate": "Mediterranean, temperate",
        "regions": "Mediterranean, temperate dry"
    },
    "orchid": {
        "scientific": "Orchidaceae", 
        "bloom_period": "Year-round (varies)",
        "climate": "tropical to temperate",
        "regions": "worldwide (diverse)"
    },
    "hibiscus": {
        "scientific": "Hibiscus rosa-sinensis",
        "bloom_period": "Year-round in tropics",
        "climate": "tropical",
        "regions": "Kerala, tropical regions"
    },
    "bougainvillea": {
        "scientific": "Bougainvillea",
        "bloom_period": "Year-round in tropics",
        "climate": "tropical to subtropical",
        "regions": "Kerala, tropical regions"
    },
}


def create_explanation_agent(llm: ChatOpenAI) -> Agent:
    """Create the botanical explanation agent"""
    return Agent(
        role="Expert Botanist and Ecologist",
        goal="Generate comprehensive, scientifically accurate bloom explanations that are accessible and informative",
        backstory="""You are a world-renowned botanist with decades of experience in plant phenology, 
        ecology, and climate science. You specialize in explaining complex botanical phenomena in ways 
        that are both scientifically rigorous and easily understood by the general public. You have deep 
        knowledge of flowering patterns, seasonal variations, ecological factors, and the impacts of 
        climate on plant life cycles.""",
        verbose=True,
        allow_delegation=False,
        llm=llm
    )


def check_climate_compatibility(flower: str, region: str) -> Dict[str, Any]:
    """Check if flower is climatically compatible with region"""
    flower_lower = flower.lower()
    region_lower = region.lower()
    
    # Tropical regions
    tropical_keywords = ["kerala", "tropical", "amazon", "equator", "singapore", "malaysia", "indonesia"]
    # Cold/temperate regions  
    cold_keywords = ["kashmir", "himalaya", "netherlands", "canada", "alaska", "siberia", "scandinavia"]
    
    is_tropical = any(keyword in region_lower for keyword in tropical_keywords)
    is_cold = any(keyword in region_lower for keyword in cold_keywords)
    
    flower_info = FLOWER_DATABASE.get(flower_lower, {})
    climate_req = flower_info.get("climate", "unknown")
    
    # Check compatibility
    compatible = True
    warning = None
    
    if "tulip" in flower_lower and is_tropical:
        compatible = False
        warning = "Tulips require cold winter temperatures and do not naturally grow in tropical climates like this region."
    elif "hibiscus" in flower_lower and is_cold:
        compatible = False
        warning = "Hibiscus is a tropical flower and cannot survive in cold climates."
    elif "cherry blossom" in flower_lower and is_tropical:
        compatible = False
        warning = "Cherry blossoms require temperate climates with distinct seasons and cold winters."
    
    return {
        "compatible": compatible,
        "warning": warning,
        "flower_climate": climate_req,
        "region_type": "tropical" if is_tropical else "cold/temperate" if is_cold else "unknown"
    }


def prepare_explanation_context(
    region: str,
    flower: str,
    ndvi_score: float = 0.7,
    coordinates: Optional[tuple] = None,
    climate_data: Optional[Dict] = None,
    date: Optional[str] = None,
    web_search_summary: Optional[str] = None
) -> Dict[str, Any]:
    """Prepare comprehensive context for explanation generation"""
    
    flower_lower = flower.lower()
    flower_info = FLOWER_DATABASE.get(flower_lower, {
        "scientific": "Unknown species",
        "bloom_period": "Varies by region",
        "climate": "unknown",
        "regions": "unknown"
    })
    
    # Check climate compatibility
    compatibility = check_climate_compatibility(flower, region)
    
    context = {
        "region": region,
        "flower": {
            "common_name": flower,
            "scientific_name": flower_info["scientific"]
        },
        "ndvi_score": ndvi_score,
        "abundance_level": get_abundance_level(ndvi_score),
        "season": f"{get_current_season()} {datetime.now().year}",
        "known_bloom_period": flower_info["bloom_period"],
        "timestamp": datetime.utcnow().isoformat()
    }
    
    # Add optional data
    if climate_data:
        context["climate"] = climate_data
    
    if coordinates:
        context["coordinates"] = {
            "longitude": coordinates[0],
            "latitude": coordinates[1]
        }
    
    if date:
        context["date"] = date
    
    if web_search_summary:
        context["web_research"] = web_search_summary
    
    # Add contextual notes based on NDVI score
    if compatibility["warning"]:
        context["notes"] = f"⚠️ Climate Warning: {compatibility['warning']}"
        context["climate_compatible"] = False
    else:
        context["climate_compatible"] = True
        if ndvi_score >= 0.8:
            context["notes"] = "Peak blooming observed, excellent vegetation health"
        elif ndvi_score >= 0.6:
            context["notes"] = "Active bloom period, favorable conditions"
        elif ndvi_score >= 0.3:
            context["notes"] = "Moderate bloom activity, typical for season"
        else:
            context["notes"] = "Low vegetation activity, may be off-season or stress conditions"
    
    # Add climate compatibility info
    context["compatibility"] = compatibility
    
    return context


def create_explanation_task(agent: Agent, context: Dict[str, Any]) -> Task:
    """Create the explanation generation task based on web research"""
    
    web_research_section = ""
    if context.get("web_research"):
        web_research_section = f"\n\nRecent Web Research Findings:\n{context['web_research']}\n"
    
    climate_warning = ""
    if not context.get("climate_compatible", True):
        climate_warning = f"\n\n⚠️ CLIMATE INCOMPATIBILITY: {context['compatibility']['warning']}"
    
    description = f"""Generate a factual, research-based explanation of blooming patterns using ONLY the web research data provided.

Context Data:
- Region: {context['region']}
- Flower: {context['flower']['common_name']} ({context['flower']['scientific_name']})
- Season: {context['season']}
- Known Bloom Period: {context['known_bloom_period']}
- Flower Climate Requirements: {context['flower'].get('climate', 'unknown')}
- Climate Compatibility: {context['compatibility']}{climate_warning}{web_research_section}

CRITICAL INSTRUCTIONS:
1. Base your explanation ENTIRELY on the web research findings provided above
2. DO NOT make assumptions - only use information from the search results
3. If the flower is climatically incompatible with the region, state this clearly and explain why it cannot grow there naturally
4. Cite specific findings from the research (e.g., "Research indicates...", "Recent studies show...")
5. If data is limited, acknowledge this honestly

Your explanation should cover:
1. Whether this flower actually grows/blooms in this region (based on search results)
2. Climate compatibility and requirements
3. Typical bloom season (if applicable)
4. Ecological context from the research
5. Any recent observations or news from the region
6. Honest assessment if information is limited

Keep it factual, honest, and based solely on the provided research. 150-250 words."""

    return Task(
        description=description,
        agent=agent,
        expected_output="A detailed, scientifically accurate explanation of bloom patterns in 150-250 words"
    )


async def generate_explanation(
    region: str,
    flower: str,
    ndvi_score: float = 0.7,
    coordinates: Optional[tuple] = None,
    climate_data: Optional[Dict] = None,
    date: Optional[str] = None,
    web_search_summary: Optional[str] = None,
    llm: Optional[ChatOpenAI] = None
) -> str:
    """
    Generate bloom explanation using the Explanation Agent
    
    Args:
        region: Geographic location name
        flower: Flower species name
        ndvi_score: NDVI vegetation index score (0.0 - 1.0)
        coordinates: Optional (longitude, latitude) tuple
        climate_data: Optional climate information dictionary
        date: Optional date string
        web_search_summary: Optional summary from web search agent
        llm: Optional LLM instance
    
    Returns:
        Generated explanation text
    """
    try:
        # Prepare context
        context = prepare_explanation_context(
            region, flower, ndvi_score, coordinates, climate_data, date, web_search_summary
        )
        
        # Create agent and task
        agent = create_explanation_agent(llm)
        task = create_explanation_task(agent, context)
        
        # Execute task
        result = task.execute()
        
        logger.info(f"Generated explanation for {flower} in {region}")
        return result
        
    except Exception as e:
        logger.error(f"Error generating explanation: {str(e)}")
        # Fallback to simple explanation
        return generate_fallback_explanation(region, flower, ndvi_score, context)


def generate_fallback_explanation(
    region: str,
    flower: str,
    ndvi_score: float,
    context: Dict[str, Any]
) -> str:
    """Generate a fallback explanation if agent fails"""
    abundance = context['abundance_level']
    
    return f"""Based on satellite NDVI analysis (score: {ndvi_score}), {flower} is currently experiencing {abundance} bloom activity in {region}. 

The vegetation index indicates {'excellent' if ndvi_score >= 0.7 else 'moderate' if ndvi_score >= 0.4 else 'limited'} photosynthetic activity, suggesting {'peak flowering conditions' if ndvi_score >= 0.7 else 'active growth with emerging blooms' if ndvi_score >= 0.4 else 'early or late season conditions'}. 

Ecological factors influencing bloom patterns include:
1. Seasonal temperature variations triggering flowering hormones
2. Precipitation patterns affecting water availability and soil moisture
3. Day length (photoperiod) signaling seasonal changes
4. Local climate conditions specific to {region}
5. Pollinator populations facilitating reproduction

The current {context['season']} period aligns with the typical bloom window of {context['known_bloom_period']}. {context['notes']}. This species plays an important role in the local ecosystem, supporting pollinator populations and contributing to regional biodiversity."""
