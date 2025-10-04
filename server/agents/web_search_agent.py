"""
Unified Web Search Agent - Searches SerpAPI and NewsAPI for relevant bloom information
"""
import logging
import asyncio
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from crewai import Agent, Task
from langchain_openai import ChatOpenAI

logger = logging.getLogger(__name__)

# Try importing search APIs
try:
    from serpapi import GoogleSearch
    SERPAPI_AVAILABLE = True
except ImportError:
    SERPAPI_AVAILABLE = False
    logger.warning("SerpAPI not available. Install with: pip install google-search-results")

try:
    from newsapi import NewsApiClient
    NEWSAPI_AVAILABLE = True
except ImportError:
    NEWSAPI_AVAILABLE = False
    logger.warning("NewsAPI not available. Install with: pip install newsapi-python")


def create_web_search_agent(llm: ChatOpenAI) -> Agent:
    """Create the web search agent"""
    return Agent(
        role="Research Analyst and Information Specialist",
        goal="Find and synthesize the most relevant, up-to-date information about flower blooming patterns, ecological conditions, and related news",
        backstory="""You are an expert research analyst specializing in environmental science and 
        botanical research. You excel at finding credible sources, filtering out noise, and synthesizing 
        information from multiple sources into clear, actionable insights. You have access to both 
        general web search and news databases to provide comprehensive, current information.""",
        verbose=True,
        allow_delegation=False,
        llm=llm
    )


async def search_serpapi(
    query: str,
    api_key: str,
    max_results: int = 5
) -> List[Dict[str, Any]]:
    """Search using SerpAPI"""
    if not SERPAPI_AVAILABLE or not api_key:
        logger.warning("SerpAPI not configured")
        return []
    
    try:
        params = {
            "q": query,
            "api_key": api_key,
            "num": max_results,
            "engine": "google"
        }
        
        search = GoogleSearch(params)
        results = search.get_dict()
        
        organic_results = results.get("organic_results", [])
        
        parsed_results = []
        for result in organic_results[:max_results]:
            parsed_results.append({
                "title": result.get("title", ""),
                "snippet": result.get("snippet", ""),
                "link": result.get("link", ""),
                "source": "SerpAPI"
            })
        
        logger.info(f"Found {len(parsed_results)} SerpAPI results for: {query}")
        return parsed_results
        
    except Exception as e:
        logger.error(f"SerpAPI search error: {str(e)}")
        return []


async def search_newsapi(
    query: str,
    api_key: str,
    max_results: int = 5
) -> List[Dict[str, Any]]:
    """Search using NewsAPI"""
    if not NEWSAPI_AVAILABLE or not api_key:
        logger.warning("NewsAPI not configured")
        return []
    
    try:
        newsapi = NewsApiClient(api_key=api_key)
        
        # Search for articles from the last 30 days
        from_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
        
        articles = newsapi.get_everything(
            q=query,
            from_param=from_date,
            language='en',
            sort_by='relevancy',
            page_size=max_results
        )
        
        parsed_results = []
        for article in articles.get('articles', [])[:max_results]:
            parsed_results.append({
                "title": article.get("title", ""),
                "snippet": article.get("description", ""),
                "link": article.get("url", ""),
                "source": "NewsAPI",
                "published_at": article.get("publishedAt", "")
            })
        
        logger.info(f"Found {len(parsed_results)} NewsAPI results for: {query}")
        return parsed_results
        
    except Exception as e:
        logger.error(f"NewsAPI search error: {str(e)}")
        return []


async def unified_search(
    region: str,
    flower: str,
    serpapi_key: str = "",
    newsapi_key: str = "",
    max_results: int = 5
) -> List[Dict[str, Any]]:
    """
    Perform unified search across SerpAPI and NewsAPI concurrently
    
    Args:
        region: Geographic location
        flower: Flower species
        serpapi_key: SerpAPI key
        newsapi_key: NewsAPI key
        max_results: Maximum results per source
    
    Returns:
        Combined list of search results
    """
    # Construct better search queries for accurate information
    general_query = f'"{flower}" flowers grow naturally "{region}" climate requirements native'
    news_query = f"{flower} flowering season {region} bloom timing climate"
    
    # Run searches concurrently
    serp_results, news_results = await asyncio.gather(
        search_serpapi(general_query, serpapi_key, max_results),
        search_newsapi(news_query, newsapi_key, max_results),
        return_exceptions=True
    )
    
    # Handle exceptions
    if isinstance(serp_results, Exception):
        logger.error(f"SerpAPI error: {serp_results}")
        serp_results = []
    
    if isinstance(news_results, Exception):
        logger.error(f"NewsAPI error: {news_results}")
        news_results = []
    
    # Combine results
    all_results = serp_results + news_results
    logger.info(f"Combined {len(all_results)} total search results")
    
    return all_results


def extract_bloom_data_from_search(results: List[Dict[str, Any]], flower: str, region: str) -> Dict[str, Any]:
    """Extract structured bloom data from search results"""
    if not results:
        return {
            "text_summary": "No recent web research available.",
            "bloom_status": "unknown",
            "season": "Data not available",
            "abundance": "unknown",
            "sources_count": 0
        }
    
    # Combine all text for analysis
    combined_text = ""
    summary_parts = []
    
    for i, result in enumerate(results[:10], 1):
        title = result.get('title', '').lower()
        snippet = result.get('snippet', '').lower()
        source = result.get('source', 'Unknown')
        
        combined_text += f" {title} {snippet}"
        
        if i <= 5:  # Store top 5 for display
            summary_parts.append(f"{i}. [{source}] {result.get('title', 'No title')}: {result.get('snippet', 'No description')}")
    
    # Extract bloom status
    bloom_status = "unknown"
    if any(word in combined_text for word in ["blooming", "in bloom", "flowering now", "currently blooming"]):
        bloom_status = "active"
    elif any(word in combined_text for word in ["will bloom", "expected", "upcoming", "soon"]):
        bloom_status = "upcoming"
    elif any(word in combined_text for word in ["finished", "ended", "past bloom"]):
        bloom_status = "past"
    elif any(word in combined_text for word in ["cannot grow", "not suitable", "doesn't grow", "incompatible"]):
        bloom_status = "not_suitable"
    
    # Extract season
    import re
    from datetime import datetime
    
    months = ["january", "february", "march", "april", "may", "june", 
              "july", "august", "september", "october", "november", "december"]
    found_months = [m for m in months if m in combined_text]
    
    if found_months:
        season = f"{found_months[0].capitalize()}"
        if len(found_months) > 1:
            season += f"-{found_months[-1].capitalize()}"
    elif "spring" in combined_text:
        season = "Spring"
    elif "summer" in combined_text:
        season = "Summer"
    elif "fall" in combined_text or "autumn" in combined_text:
        season = "Autumn"
    elif "winter" in combined_text:
        season = "Winter"
    elif "monsoon" in combined_text:
        season = "Monsoon"
    else:
        season = "Varies by region"
    
    # Extract abundance
    abundance = "medium"
    if any(word in combined_text for word in ["abundant", "common", "widespread", "numerous"]):
        abundance = "high"
    elif any(word in combined_text for word in ["rare", "uncommon", "scarce", "limited"]):
        abundance = "low"
    elif any(word in combined_text for word in ["does not grow", "absent", "not found"]):
        abundance = "none"
    
    return {
        "text_summary": "\n".join(summary_parts),
        "bloom_status": bloom_status,
        "season": season,
        "abundance": abundance,
        "sources_count": len(results),
        "combined_analysis": combined_text[:500]  # For debugging
    }


def synthesize_search_results(results: List[Dict[str, Any]]) -> str:
    """Synthesize search results into a coherent summary"""
    if not results:
        return "No recent web research available."
    
    summary_parts = []
    
    for i, result in enumerate(results[:5], 1):  # Limit to top 5
        title = result.get('title', 'No title')
        snippet = result.get('snippet', 'No description')
        source = result.get('source', 'Unknown')
        
        summary_parts.append(f"{i}. [{source}] {title}: {snippet}")
    
    return "\n".join(summary_parts)


def create_search_synthesis_task(agent: Agent, search_results: List[Dict[str, Any]], region: str, flower: str) -> Task:
    """Create task to synthesize search results"""
    
    results_text = synthesize_search_results(search_results)
    
    description = f"""Analyze and synthesize the following web search results about {flower} blooming patterns in {region}.

Search Results:
{results_text}

Your task:
1. Identify the most relevant and credible information
2. Extract key facts about blooming patterns, climate conditions, and ecological factors
3. Note any recent news or unusual patterns
4. Synthesize into a concise summary (100-150 words) that can inform bloom explanations
5. Prioritize scientific and ecological insights

Be critical of sources and focus on factual, verifiable information."""

    return Task(
        description=description,
        agent=agent,
        expected_output="A concise, factual summary of key findings from web research in 100-150 words"
    )


async def perform_web_search(
    region: str,
    flower: str,
    serpapi_key: str = "",
    newsapi_key: str = "",
    max_results: int = 5,
    llm: Optional[ChatOpenAI] = None
) -> Dict[str, Any]:
    """
    Perform unified web search and synthesize results
    
    Args:
        region: Geographic location
        flower: Flower species
        serpapi_key: SerpAPI key
        newsapi_key: NewsAPI key
        max_results: Maximum results per source
        llm: Optional LLM instance
    
    Returns:
        Dictionary with search results and synthesis
    """
    try:
        # Perform unified search
        search_results = await unified_search(
            region, flower, serpapi_key, newsapi_key, max_results
        )
        
        # If we have results and LLM, synthesize with agent
        if search_results and llm:
            try:
                agent = create_web_search_agent(llm)
                task = create_search_synthesis_task(agent, search_results, region, flower)
                synthesis = task.execute()
            except Exception as e:
                logger.error(f"Agent synthesis error: {str(e)}")
                synthesis = synthesize_search_results(search_results)
        else:
            synthesis = synthesize_search_results(search_results)
        
        return {
            "raw_results": search_results,
            "synthesis": synthesis,
            "result_count": len(search_results),
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Web search error: {str(e)}")
        return {
            "raw_results": [],
            "synthesis": "Web search temporarily unavailable.",
            "result_count": 0,
            "error": str(e),
            "timestamp": datetime.utcnow().isoformat()
        }


async def get_mock_search_results(region: str, flower: str) -> Dict[str, Any]:
    """Generate mock search results for testing without API keys"""
    mock_results = [
        {
            "title": f"{flower.title()} Blooming Patterns in {region}",
            "snippet": f"Recent studies show {flower} blooming patterns in {region} are influenced by temperature and precipitation.",
            "link": "https://example.com/study1",
            "source": "Mock SerpAPI"
        },
        {
            "title": f"Climate Impact on {flower.title()} Growth",
            "snippet": f"Climate change is affecting {flower} bloom timing in {region}, with earlier flowering observed.",
            "link": "https://example.com/news1",
            "source": "Mock NewsAPI"
        }
    ]
    
    synthesis = f"Recent research indicates that {flower} blooming in {region} is responding to climate variations, with temperature and precipitation playing key roles. Earlier bloom times have been observed in recent years."
    
    return {
        "raw_results": mock_results,
        "synthesis": synthesis,
        "result_count": len(mock_results),
        "timestamp": datetime.utcnow().isoformat(),
        "mock": True
    }


async def search_top_regions(
    country: str,
    flower: str,
    serpapi_key: str = "",
    newsapi_key: str = "",
    max_results: int = 10,
    llm: Optional[ChatOpenAI] = None
) -> Dict[str, Any]:
    """
    Search for regions/locations within a country with highest abundance of a specific flower
    
    Args:
        country: Country name to search within
        flower: Flower species name
        serpapi_key: SerpAPI key
        newsapi_key: NewsAPI key
        max_results: Maximum search results to fetch
        llm: Optional LLM for synthesis
    
    Returns:
        Dictionary with top regions and their details
    """
    try:
        # Construct targeted search query for finding top regions
        search_query = f'"{flower}" flowers best regions locations grow "{country}" where to find most abundant'
        
        logger.info(f"Searching for top {flower} regions in {country}")
        
        # Perform search
        search_results = await unified_search(
            region=country,
            flower=flower,
            serpapi_key=serpapi_key,
            newsapi_key=newsapi_key,
            max_results=max_results
        )
        
        # Extract region mentions from search results
        regions = extract_top_regions_from_search(search_results, flower, country)
        
        # If we have an LLM, use it to better analyze the results
        if llm and search_results:
            try:
                synthesis = await synthesize_region_results(search_results, flower, country, llm)
                regions['ai_summary'] = synthesis
            except Exception as e:
                logger.error(f"Failed to synthesize region results: {str(e)}")
        
        return regions
        
    except Exception as e:
        logger.error(f"Failed to search top regions: {str(e)}")
        return {
            "country": country,
            "flower": flower,
            "top_regions": [],
            "error": str(e)
        }


def extract_top_regions_from_search(
    search_results: List[Dict[str, Any]], 
    flower: str, 
    country: str
) -> Dict[str, Any]:
    """
    Extract and rank regions from search results
    
    Args:
        search_results: List of search result dictionaries
        flower: Flower name
        country: Country name
    
    Returns:
        Dictionary with ranked regions and coordinates
    """
    import re
    from collections import Counter
    
    # Common region/location indicators
    location_patterns = [
        r'in ([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)',
        r'at ([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)',
        r'near ([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)',
        r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*) region',
        r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*) valley',
        r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*) district',
        r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*) province',
        r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*) state',
    ]
    
    # Combine all text from search results
    all_text = " ".join([
        f"{result.get('title', '')} {result.get('snippet', '')}"
        for result in search_results
    ])
    
    # Extract potential region names
    found_regions = []
    for pattern in location_patterns:
        matches = re.findall(pattern, all_text)
        found_regions.extend(matches)
    
    # Count frequency of each region mention
    region_counts = Counter(found_regions)
    
    # Filter out common non-region words
    stop_words = {'The', 'This', 'That', 'These', 'Those', 'Many', 'Some', 'Most', 
                  'Each', 'Every', 'All', 'Both', 'Few', 'More', 'Other'}
    region_counts = {k: v for k, v in region_counts.items() if k not in stop_words}
    
    # Get top 5 regions by mention frequency
    top_regions_list = region_counts.most_common(5)
    
    # Format regions with estimated coordinates (would need geocoding API for real coords)
    regions_with_data = []
    for region_name, mentions in top_regions_list:
        regions_with_data.append({
            "name": region_name,
            "country": country,
            "full_name": f"{region_name}, {country}",
            "mentions": mentions,
            "confidence": min(mentions / len(search_results) * 100, 100) if search_results else 0,
            # Placeholder coordinates - should be replaced with geocoding
            "coordinates": None,
            "needs_geocoding": True
        })
    
    # If no regions found, return country-level fallback
    if not regions_with_data:
        regions_with_data = [{
            "name": country,
            "country": country,
            "full_name": country,
            "mentions": 0,
            "confidence": 50,
            "coordinates": None,
            "needs_geocoding": True,
            "note": "No specific regions identified - showing country level"
        }]
    logger.info(f"Extracted regions: {regions_with_data}")
    return {
        "country": country,
        "flower": flower,
        "top_regions": regions_with_data[:5],
        "total_sources": len(search_results),
        "extraction_method": "text_analysis"
    }


async def synthesize_region_results(
    search_results: List[Dict[str, Any]],
    flower: str,
    country: str,
    llm: ChatOpenAI
) -> str:
    """
    Use LLM to synthesize search results and identify top regions
    
    Args:
        search_results: Search results
        flower: Flower name
        country: Country name
        llm: LLM instance
    
    Returns:
        Synthesized text identifying top regions
    """
    try:
        agent = create_web_search_agent(llm)
        
        results_text = "\n".join([
            f"{i+1}. {r.get('title', 'No title')}: {r.get('snippet', 'No description')}"
            for i, r in enumerate(search_results[:10])
        ])
        
        task_description = f"""Based on the following search results, identify the TOP 3-5 SPECIFIC REGIONS or locations within {country} where {flower} flowers are most abundant or commonly found.

Search Results:
{results_text}

Your task:
1. Identify specific region names, cities, valleys, provinces, or districts mentioned
2. Rank them by how frequently and prominently they appear
3. Note any mentions of abundance, popularity, or famous growing areas
4. Return a concise list of the top 3-5 locations

Format your response as:
1. [Region Name] - [Brief reason why it's notable for this flower]
2. [Region Name] - [Brief reason]
...

Be specific with location names. If no specific regions are mentioned, state that clearly."""

        task = Task(
            description=task_description,
            agent=agent,
            expected_output="A ranked list of 3-5 specific regions with brief explanations"
        )
        
        result = task.execute()
        return str(result) if result else "No specific regions identified"
        
    except Exception as e:
        logger.error(f"Failed to synthesize region results: {str(e)}")
        return f"Analysis unavailable: {str(e)}"
