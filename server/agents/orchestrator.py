"""
Master Orchestrator Agent - Coordinates all agents and handles the main workflow
"""
import logging
import asyncio
from typing import Dict, Any, Optional
from datetime import datetime
from crewai import Crew, Process
from langchain_openai import ChatOpenAI

from agents.explanation_agent import (
    create_explanation_agent,
    prepare_explanation_context,
    create_explanation_task,
    generate_fallback_explanation,
    FLOWER_DATABASE
)
from agents.web_search_agent import (
    perform_web_search,
    get_mock_search_results,
    extract_bloom_data_from_search
)

logger = logging.getLogger(__name__)


class BloomExplanationOrchestrator:
    """
    Master orchestrator for bloom explanation generation
    Coordinates between explanation agent and web search agent
    """
    
    def __init__(
        self,
        openai_api_key: str = "",
        serpapi_key: str = "",
        newsapi_key: str = "",
        timeout: int = 30,
        max_search_results: int = 5
    ):
        self.openai_api_key = openai_api_key
        self.serpapi_key = serpapi_key
        self.newsapi_key = newsapi_key
        self.timeout = timeout
        self.max_search_results = max_search_results
        
        # Initialize LLM if API key available
        self.llm = None
        if openai_api_key:
            try:
                self.llm = ChatOpenAI(
                    model="gpt-4o-mini",
                    temperature=0.7,
                    openai_api_key=openai_api_key
                )
                logger.info("LLM initialized successfully")
            except Exception as e:
                logger.error(f"Failed to initialize LLM: {str(e)}")
    
    async def orchestrate(
        self,
        region: str,
        flower: str,
        ndvi_score: float = 0.7,
        coordinates: Optional[tuple] = None,
        climate_data: Optional[Dict] = None,
        date: Optional[str] = None,
        use_mock_search: bool = False
    ) -> Dict[str, Any]:
        """
        Main orchestration method - coordinates all agents
        
        Args:
            region: Geographic location
            flower: Flower species name
            ndvi_score: NDVI vegetation index score
            coordinates: Optional (longitude, latitude) tuple
            climate_data: Optional climate data
            date: Optional date string
            use_mock_search: Use mock search results if True
        
        Returns:
            Complete response with explanation, search results, and metadata
        """
        start_time = datetime.utcnow()
        logger.info(f"Orchestrating bloom explanation for {flower} in {region}")
        
        try:
            # Run web search and explanation preparation concurrently
            search_task = self._run_web_search(region, flower, use_mock_search)
            context_task = self._prepare_context(
                region, flower, ndvi_score, coordinates, climate_data, date
            )
            
            # Wait for both tasks with timeout
            search_result, context = await asyncio.wait_for(
                asyncio.gather(search_task, context_task, return_exceptions=True),
                timeout=self.timeout
            )
            
            # Handle search errors gracefully
            if isinstance(search_result, Exception):
                logger.error(f"Search agent error: {search_result}")
                search_result = {
                    "synthesis": "Web search temporarily unavailable",
                    "raw_results": [],
                    "error": str(search_result)
                }
            
            # Add search synthesis to context
            web_synthesis = search_result.get("synthesis", "")
            
            # Generate explanation using agent or fallback
            explanation = await self._generate_explanation(
                context, web_synthesis
            )
            
            # Prepare response
            response = self._build_response(
                region, flower, explanation, context, search_result, start_time
            )
            
            logger.info(f"Successfully orchestrated explanation in {response['processing_time_ms']}ms")
            return response
            
        except asyncio.TimeoutError:
            logger.error(f"Orchestration timeout after {self.timeout}s")
            return self._build_fallback_response(
                region, flower, ndvi_score, "Timeout", start_time
            )
        except Exception as e:
            logger.error(f"Orchestration error: {str(e)}")
            return self._build_fallback_response(
                region, flower, ndvi_score, str(e), start_time
            )
    
    async def _run_web_search(
        self,
        region: str,
        flower: str,
        use_mock: bool = False
    ) -> Dict[str, Any]:
        """Run web search agent"""
        try:
            if use_mock or (not self.serpapi_key and not self.newsapi_key):
                logger.info("Using mock search results")
                return await get_mock_search_results(region, flower)
            
            return await perform_web_search(
                region=region,
                flower=flower,
                serpapi_key=self.serpapi_key,
                newsapi_key=self.newsapi_key,
                max_results=self.max_search_results,
                llm=self.llm
            )
        except Exception as e:
            logger.error(f"Web search failed: {str(e)}")
            return {
                "synthesis": "Web search unavailable",
                "raw_results": [],
                "error": str(e)
            }
    
    async def _prepare_context(
        self,
        region: str,
        flower: str,
        ndvi_score: float,
        coordinates: Optional[tuple],
        climate_data: Optional[Dict],
        date: Optional[str]
    ) -> Dict[str, Any]:
        """Prepare context for explanation"""
        return prepare_explanation_context(
            region=region,
            flower=flower,
            ndvi_score=ndvi_score,
            coordinates=coordinates,
            climate_data=climate_data,
            date=date
        )
    
    async def _generate_explanation(
        self,
        context: Dict[str, Any],
        web_synthesis: str
    ) -> str:
        """Generate explanation using CrewAI agent"""
        
        if not self.llm:
            logger.warning("LLM not available, using fallback")
            return generate_fallback_explanation(
                context['region'],
                context['flower']['common_name'],
                context['ndvi_score'],
                context
            )
        
        try:
            # Create agent and task
            explanation_agent = create_explanation_agent(self.llm)
            
            # Add web synthesis to context
            context_with_search = {**context, "web_research": web_synthesis}
            
            # Create and execute task
            task = create_explanation_task(explanation_agent, context_with_search)
            
            # Create crew and execute
            crew = Crew(
                agents=[explanation_agent],
                tasks=[task],
                process=Process.sequential,
                verbose=False
            )
            
            result = crew.kickoff()
            
            # Extract result text
            if hasattr(result, 'raw'):
                explanation = result.raw
            elif isinstance(result, str):
                explanation = result
            else:
                explanation = str(result)
            
            return explanation.strip()
            
        except Exception as e:
            logger.error(f"Agent explanation failed: {str(e)}")
            return generate_fallback_explanation(
                context['region'],
                context['flower']['common_name'],
                context['ndvi_score'],
                context
            )
    
    def _build_response(
        self,
        region: str,
        flower: str,
        explanation: str,
        context: Dict[str, Any],
        search_result: Dict[str, Any],
        start_time: datetime
    ) -> Dict[str, Any]:
        """Build complete response using search-derived data"""
        
        processing_time = (datetime.utcnow() - start_time).total_seconds() * 1000
        
        # Extract bloom data from search results
        raw_results = search_result.get("raw_results", [])
        bloom_data = extract_bloom_data_from_search(raw_results, flower, region)
        
        # Map bloom_status to abundance
        abundance_map = {
            "active": "high",
            "upcoming": "medium",
            "past": "low",
            "not_suitable": "none",
            "unknown": "medium"
        }
        
        abundance_level = bloom_data.get("abundance", "medium")
        if abundance_level == "unknown":
            abundance_level = abundance_map.get(bloom_data.get("bloom_status", "unknown"), "medium")
        
        # Extract key factors
        factors = [
            "Temperature and seasonal variations",
            "Precipitation and water availability",
            "Day length (photoperiod)",
            "Soil composition and nutrients",
            "Pollinator populations",
            "Regional climate patterns"
        ]
        
        # Format climate data
        climate = context.get('climate', 'Climate data not available')
        if isinstance(climate, dict):
            # Convert dict to readable string if climate_data was provided
            temp = climate.get('temperature', 'N/A')
            precip = climate.get('precipitation', 'N/A')
            climate = f"Temperature: {temp}°C, Precipitation: {precip}mm"
        
        return {
            "region": region,
            "flower": {
                "common_name": flower,
                "scientific_name": context['flower']['scientific_name']
            },
            "ndvi_score": context['ndvi_score'],  # Keep for reference but not used in logic
            "abundance_level": abundance_level,  # From search data
            "season": bloom_data.get("season", context['season']),  # Prefer search data
            "climate": climate,
            "known_bloom_period": bloom_data.get("season", context['known_bloom_period']),  # From search data
            "notes": context.get('notes', ''),
            "explanation": explanation,
            "factors": factors,
            "web_research": {
                "summary": search_result.get("synthesis", ""),
                "source_count": search_result.get("result_count", 0),
                "sources": search_result.get("raw_results", [])[:3]  # Top 3 sources
            },
            "metadata": {
                "timestamp": datetime.utcnow().isoformat(),
                "processing_time_ms": round(processing_time, 2),
                "llm_used": self.llm is not None,
                "search_available": search_result.get("result_count", 0) > 0
            },
            "timestamp": datetime.utcnow().isoformat(),
            "processing_time_ms": round(processing_time, 2)
        }
    
    def _build_fallback_response(
        self,
        region: str,
        flower: str,
        ndvi_score: float,
        error: str,
        start_time: datetime
    ) -> Dict[str, Any]:
        """Build fallback response on error"""
        
        processing_time = (datetime.utcnow() - start_time).total_seconds() * 1000
        
        flower_lower = flower.lower()
        flower_info = FLOWER_DATABASE.get(flower_lower, {
            "scientific": "Unknown species",
            "bloom_period": "Varies by region"
        })
        
        from agents.explanation_agent import get_abundance_level, get_current_season
        
        abundance = get_abundance_level(ndvi_score)
        
        notes = f"{'Peak blooming observed' if ndvi_score >= 0.7 else 'Active bloom period' if ndvi_score >= 0.4 else 'Limited vegetation activity'}"
        
        fallback_explanation = f"""Based on satellite vegetation data, {flower} shows {abundance} bloom activity in {region} (NDVI: {ndvi_score}). 
        
The current conditions suggest {'optimal' if ndvi_score >= 0.7 else 'moderate' if ndvi_score >= 0.4 else 'limited'} flowering patterns. Bloom timing is influenced by temperature, precipitation, day length, and local climate conditions. This species typically blooms during {flower_info['bloom_period']}.

For detailed analysis, please ensure API services are properly configured."""
        
        return {
            "region": region,
            "flower": {
                "common_name": flower,
                "scientific_name": flower_info["scientific"]
            },
            "ndvi_score": ndvi_score,
            "abundance_level": abundance,
            "season": f"{get_current_season()} {datetime.now().year}",
            "climate": "Climate data not available",
            "known_bloom_period": flower_info["bloom_period"],
            "notes": notes,
            "explanation": fallback_explanation,
            "factors": [
                "Temperature and seasonal variations",
                "Precipitation and water availability",
                "Day length (photoperiod)"
            ],
            "web_research": {
                "summary": "Search unavailable",
                "source_count": 0,
                "sources": []
            },
            "metadata": {
                "timestamp": datetime.utcnow().isoformat(),
                "processing_time_ms": round(processing_time, 2),
                "llm_used": False,
                "search_available": False,
                "error": error,
                "fallback": True
            },
            "timestamp": datetime.utcnow().isoformat(),
            "processing_time_ms": round(processing_time, 2)
        }


# Global orchestrator instance (initialized when needed)
_orchestrator_instance = None


def get_orchestrator(
    openai_api_key: str = "",
    serpapi_key: str = "",
    newsapi_key: str = "",
    timeout: int = 30,
    max_search_results: int = 5
) -> BloomExplanationOrchestrator:
    """Get or create orchestrator instance"""
    global _orchestrator_instance
    
    if _orchestrator_instance is None:
        _orchestrator_instance = BloomExplanationOrchestrator(
            openai_api_key=openai_api_key,
            serpapi_key=serpapi_key,
            newsapi_key=newsapi_key,
            timeout=timeout,
            max_search_results=max_search_results
        )
    
    return _orchestrator_instance
