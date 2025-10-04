# BloomWatch AI Agents - CrewAI Architecture

This directory contains the AI agent system for BloomWatch, implementing an agentic architecture using CrewAI.

## Architecture Overview

The system uses three main components working together:

### 1. Master Orchestrator (`orchestrator.py`)
- **Role**: Main coordinator and REST API handler
- **Responsibilities**:
  - Receives requests from the `/explain` endpoint
  - Coordinates concurrent agent execution
  - Manages timeouts and error handling
  - Synthesizes final responses
  - Handles fallback scenarios gracefully

### 2. Explanation Agent (`explanation_agent.py`)
- **Role**: Botanical expert and explanation generator
- **Responsibilities**:
  - Generates detailed, region-specific bloom explanations
  - Uses LLM (GPT-4o-mini) for natural language generation
  - Incorporates NDVI scores, seasonal data, and climate context
  - Enriches responses with web search findings
  - Provides scientific accuracy with accessible language

### 3. Unified Web Search Agent (`web_search_agent.py`)
- **Role**: Real-time information researcher
- **Responsibilities**:
  - Queries SerpAPI for general web searches on phenology and ecology
  - Queries NewsAPI for recent news and agricultural updates
  - Runs searches concurrently for speed
  - Filters and synthesizes results
  - Provides up-to-date factual content

## Workflow

```
User Request → /explain endpoint
       ↓
Master Orchestrator
       ↓
   ┌───────────────┐
   ↓               ↓
Explanation    Web Search
   Agent         Agent
   ↓               ↓
   (concurrent execution)
   ↓               ↓
   └───────┬───────┘
           ↓
    Merged Response
           ↓
    Return to User
```

## Setup

### 1. Install Dependencies

```bash
cd server
pip install -r requirements.txt
```

### 2. Configure API Keys

Create a `.env` file in the `server` directory:

```env
# Required for AI agents
OPENAI_API_KEY=sk-your-openai-key-here

# Optional but recommended for web search
SERPAPI_API_KEY=your-serpapi-key-here
NEWSAPI_API_KEY=your-newsapi-key-here

# Agent configuration (optional)
AGENT_TIMEOUT=30
MAX_SEARCH_RESULTS=5
```

### 3. Get API Keys

- **OpenAI**: https://platform.openai.com/api-keys
- **SerpAPI**: https://serpapi.com/
- **NewsAPI**: https://newsapi.org/

## Usage

### Basic Request

```python
POST /api/explain
{
  "region": "Kashmir Valley",
  "flower": "tulip",
  "ndvi_score": 0.75
}
```

### Advanced Request

```python
POST /api/explain
{
  "region": "Kashmir Valley",
  "flower": "tulip",
  "ndvi_score": 0.75,
  "coordinates": [74.8370, 34.0837],
  "climate_data": {
    "temperature": 18.5,
    "precipitation": 45.2
  },
  "date": "2025-04-15",
  "use_mock_search": false
}
```

### Response Structure

```json
{
  "region": "Kashmir Valley",
  "flower": "tulip",
  "scientific_name": "Tulipa",
  "explanation": "Detailed AI-generated explanation...",
  "bloom_period": "March to May",
  "ndvi_score": 0.75,
  "abundance_level": "high",
  "season": "Spring 2025",
  "factors": [...],
  "web_research": {
    "summary": "Synthesized findings from web search...",
    "source_count": 5,
    "sources": [...]
  },
  "metadata": {
    "timestamp": "2025-04-15T10:30:00Z",
    "processing_time_ms": 2345.67,
    "llm_used": true,
    "search_available": true
  }
}
```

## Features

### Concurrent Execution
- Agents run in parallel for faster responses
- Typical response time: 2-5 seconds
- Timeout protection prevents hanging

### Graceful Fallbacks
- Works without API keys (uses mock data)
- Handles individual agent failures
- Always returns a response

### Mock Mode
- Use `"use_mock_search": true` for testing
- No API keys required for development
- Fast iteration

### Error Handling
- Comprehensive logging
- Detailed error messages
- Maintains service availability

## Development

### Testing Without API Keys

```python
# Use mock search mode
POST /api/explain
{
  "region": "Test Region",
  "flower": "rose",
  "ndvi_score": 0.8,
  "use_mock_search": true
}
```

### Adding New Flowers

Edit `explanation_agent.py`:

```python
FLOWER_DATABASE = {
    "your_flower": {
        "scientific": "Scientific Name",
        "bloom_period": "Month to Month"
    },
    # ...
}
```

### Customizing Agents

Each agent can be customized:

```python
# In orchestrator.py
self.llm = ChatOpenAI(
    model="gpt-4",  # Change model
    temperature=0.5,  # Adjust creativity
)
```

## Performance Tips

1. **Use caching** for repeated queries
2. **Limit search results** to 3-5 per source
3. **Set appropriate timeouts** (20-30s recommended)
4. **Monitor API usage** to avoid rate limits

## Troubleshooting

### "LLM not available" Warning
- Check `OPENAI_API_KEY` in `.env`
- Verify API key is valid
- System will use fallback explanations

### "Search unavailable" Message
- Check `SERPAPI_API_KEY` and `NEWSAPI_API_KEY`
- Verify API quotas
- Use `use_mock_search: true` for testing

### Timeout Errors
- Increase `AGENT_TIMEOUT` in config
- Check internet connectivity
- Verify API service status

## Architecture Benefits

1. **Modular**: Each agent is independent and testable
2. **Scalable**: Easy to add new agents or data sources
3. **Resilient**: Graceful degradation on failures
4. **Fast**: Concurrent execution minimizes latency
5. **Rich**: Combines AI reasoning with real-time data

## Future Enhancements

- [ ] Image analysis agent for uploaded flower photos
- [ ] Climate data integration agent
- [ ] Historical bloom pattern analysis
- [ ] Multi-region comparison agent
- [ ] Caching layer for repeated queries
- [ ] Rate limiting and quota management

## License

Part of the BloomWatch project.
