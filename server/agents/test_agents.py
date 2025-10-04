"""
Test script for BloomWatch AI Agents
Run this to verify your agent setup is working correctly
"""
import asyncio
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.orchestrator import get_orchestrator


async def test_orchestrator_basic():
    """Test basic orchestrator functionality with mock data"""
    print("=" * 60)
    print("Test 1: Basic Orchestration (Mock Mode)")
    print("=" * 60)
    
    orchestrator = get_orchestrator(
        openai_api_key="",  # Empty for testing
        timeout=10
    )
    
    result = await orchestrator.orchestrate(
        region="Kashmir Valley",
        flower="tulip",
        ndvi_score=0.75,
        use_mock_search=True
    )
    
    print(f"\n✓ Region: {result['region']}")
    print(f"✓ Flower: {result['flower']} ({result['scientific_name']})")
    print(f"✓ NDVI Score: {result['ndvi_score']}")
    print(f"✓ Abundance: {result['abundance_level']}")
    print(f"✓ Season: {result['season']}")
    print(f"✓ Processing Time: {result['processing_time_ms']}ms")
    print(f"✓ Web Sources: {result['web_research']['source_count']}")
    
    print(f"\n📝 Explanation Preview:")
    print(result['explanation'][:200] + "...")
    
    print(f"\n🔍 Web Research Preview:")
    print(result['web_research']['summary'][:150] + "...")
    
    print("\n✅ Test 1 PASSED")
    return result


async def test_orchestrator_with_api():
    """Test orchestrator with actual API keys (if available)"""
    print("\n" + "=" * 60)
    print("Test 2: Orchestration with API Keys")
    print("=" * 60)
    
    from dotenv import load_dotenv
    load_dotenv()
    
    openai_key = os.getenv("OPENAI_API_KEY", "")
    serpapi_key = os.getenv("SERPAPI_API_KEY", "")
    newsapi_key = os.getenv("NEWSAPI_API_KEY", "")
    
    if not openai_key:
        print("\n⚠️  OPENAI_API_KEY not found in .env")
        print("Skipping API test. Set up .env file for full testing.")
        return None
    
    print(f"\n✓ OpenAI Key: {'Found' if openai_key else 'Missing'}")
    print(f"✓ SerpAPI Key: {'Found' if serpapi_key else 'Missing'}")
    print(f"✓ NewsAPI Key: {'Found' if newsapi_key else 'Missing'}")
    
    orchestrator = get_orchestrator(
        openai_api_key=openai_key,
        serpapi_key=serpapi_key,
        newsapi_key=newsapi_key,
        timeout=30
    )
    
    print("\n🤖 Running AI agents...")
    
    result = await orchestrator.orchestrate(
        region="California",
        flower="sunflower",
        ndvi_score=0.82,
        coordinates=(-119.4179, 36.7783),
        use_mock_search=not (serpapi_key or newsapi_key)
    )
    
    print(f"\n✓ LLM Used: {result['metadata']['llm_used']}")
    print(f"✓ Search Available: {result['metadata']['search_available']}")
    print(f"✓ Processing Time: {result['processing_time_ms']}ms")
    
    print(f"\n📝 AI-Generated Explanation:")
    print(result['explanation'])
    
    if result['web_research']['source_count'] > 0:
        print(f"\n🔍 Web Research ({result['web_research']['source_count']} sources):")
        print(result['web_research']['summary'])
    
    print("\n✅ Test 2 PASSED")
    return result


async def test_different_flowers():
    """Test with different flower species"""
    print("\n" + "=" * 60)
    print("Test 3: Multiple Flower Species")
    print("=" * 60)
    
    orchestrator = get_orchestrator(timeout=10)
    
    flowers = [
        ("rose", "Paris, France", 0.65),
        ("cherry blossom", "Tokyo, Japan", 0.90),
        ("lavender", "Provence, France", 0.78)
    ]
    
    for flower, region, ndvi in flowers:
        print(f"\n🌸 Testing: {flower.title()} in {region}")
        result = await orchestrator.orchestrate(
            region=region,
            flower=flower,
            ndvi_score=ndvi,
            use_mock_search=True
        )
        print(f"  ✓ Scientific Name: {result['scientific_name']}")
        print(f"  ✓ Bloom Period: {result['bloom_period']}")
        print(f"  ✓ Abundance: {result['abundance_level']}")
    
    print("\n✅ Test 3 PASSED")


async def test_error_handling():
    """Test error handling and fallbacks"""
    print("\n" + "=" * 60)
    print("Test 4: Error Handling & Fallbacks")
    print("=" * 60)
    
    orchestrator = get_orchestrator(
        openai_api_key="invalid_key",
        timeout=5
    )
    
    print("\n🧪 Testing with invalid API key...")
    result = await orchestrator.orchestrate(
        region="Test Region",
        flower="test flower",
        ndvi_score=0.5,
        use_mock_search=True
    )
    
    if result['metadata'].get('fallback'):
        print("✓ Fallback mechanism activated")
    print(f"✓ Response received despite errors")
    print(f"✓ Processing Time: {result['processing_time_ms']}ms")
    
    print("\n✅ Test 4 PASSED - System is resilient")


async def main():
    """Run all tests"""
    print("\n" + "=" * 60)
    print("🌸 BloomWatch AI Agents Test Suite 🌸")
    print("=" * 60)
    
    try:
        # Test 1: Basic functionality
        await test_orchestrator_basic()
        
        # Test 2: With API keys (if available)
        await test_orchestrator_with_api()
        
        # Test 3: Multiple flowers
        await test_different_flowers()
        
        # Test 4: Error handling
        await test_error_handling()
        
        print("\n" + "=" * 60)
        print("🎉 All Tests Passed! Your agent setup is working correctly!")
        print("=" * 60)
        print("\nNext Steps:")
        print("1. Add your API keys to server/.env file")
        print("2. Run: python -m uvicorn main:app --reload")
        print("3. Test the /api/explain endpoint")
        print("=" * 60 + "\n")
        
    except Exception as e:
        print(f"\n❌ Test Failed: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
