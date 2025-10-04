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


# Flower database for quick reference
FLOWER_DATABASE = {
    "rose": {"scientific": "Rosa", "bloom_period": "May to September"},
    "rhododendron": {"scientific": "Rhododendron arboreum", "bloom_period": "March to May"},
    "sunflower": {"scientific": "Helianthus annuus", "bloom_period": "June to September"},
    "tulip": {"scientific": "Tulipa", "bloom_period": "March to May"},
    "cherry blossom": {"scientific": "Prunus serrulata", "bloom_period": "March to April"},
    "lotus": {"scientific": "Nelumbo nucifera", "bloom_period": "June to August"},
    "jasmine": {"scientific": "Jasminum", "bloom_period": "June to September"},
    "marigold": {"scientific": "Tagetes", "bloom_period": "July to October"},
    "lavender": {"scientific": "Lavandula", "bloom_period": "June to August"},
    "orchid": {"scientific": "Orchidaceae", "bloom_period": "Year-round (varies)"},
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
        "bloom_period": "Varies by region"
    })
    
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
    if ndvi_score >= 0.8:
        context["notes"] = "Peak blooming observed, excellent vegetation health"
    elif ndvi_score >= 0.6:
        context["notes"] = "Active bloom period, favorable conditions"
    elif ndvi_score >= 0.3:
        context["notes"] = "Moderate bloom activity, typical for season"
    else:
        context["notes"] = "Low vegetation activity, may be off-season or stress conditions"
    
    return context


def create_explanation_task(agent: Agent, context: Dict[str, Any]) -> Task:
    """Create the explanation generation task"""
    
    web_research_section = ""
    if context.get("web_research"):
        web_research_section = f"\n- Recent Research & News: {context['web_research']}"
    
    description = f"""Generate a comprehensive, scientifically accurate explanation of the blooming patterns for the specified flower.

Context Data:
- Region: {context['region']}
- Flower: {context['flower']['common_name']} ({context['flower']['scientific_name']})
- Current NDVI Score: {context['ndvi_score']} (Abundance Level: {context['abundance_level']})
- Season: {context['season']}
- Known Bloom Period: {context['known_bloom_period']}
- Climate: {context.get('climate', 'Not available')}
- Observations: {context['notes']}{web_research_section}

Provide a comprehensive explanation covering:
1. Current bloom status and what the NDVI score indicates
2. Ecological factors influencing bloom patterns in this region
3. Seasonal timing and photoperiod effects
4. Climate and environmental conditions
5. Ecological or agricultural significance
6. Any notable patterns or recommendations for observers

Keep the explanation informative yet accessible, around 150-250 words. Be confident and authoritative, 
incorporating the latest research findings if available."""

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
