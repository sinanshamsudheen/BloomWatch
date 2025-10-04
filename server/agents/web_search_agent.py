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
    # Construct search queries
    general_query = f"{flower} bloom patterns {region} ecology phenology"
    news_query = f"{flower} blooming {region} climate agriculture"
    
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
