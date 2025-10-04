# 🚀 BloomWatch Server - AI Agent Setup Guide

## Quick Start Guide for Hackathon

This guide will get your AI-powered bloom explanation service running in minutes!

## Prerequisites

- Python 3.8+
- pip package manager
- Virtual environment (recommended)

## Step 1: Install Dependencies

```bash
cd server

# Activate virtual environment (if you have one)
source bloom_server_env/bin/activate  # Linux/Mac
# or
bloom_server_env\Scripts\activate  # Windows

# Install all required packages
pip install -r requirements.txt
```

This installs:
- FastAPI & Uvicorn (web server)
- CrewAI (agent framework)
- OpenAI & LangChain (LLM integration)
- SerpAPI & NewsAPI (web search)
- All other dependencies

## Step 2: Configure API Keys

### 2.1 Copy the example environment file

```bash
cp .env.example .env
```

### 2.2 Add your API keys to `.env`

```env
# REQUIRED for AI explanations
OPENAI_API_KEY=sk-your-actual-openai-key

# OPTIONAL but recommended for web search
SERPAPI_API_KEY=your-serpapi-key
NEWSAPI_API_KEY=your-newsapi-key
```

### 2.3 Where to get API keys

**OpenAI** (Required for AI-generated explanations):
1. Go to https://platform.openai.com/
2. Sign up or log in
3. Navigate to API Keys section
4. Create a new key
5. Copy and paste into `.env`

**SerpAPI** (Optional - for Google search):
1. Go to https://serpapi.com/
2. Sign up (free tier: 100 searches/month)
3. Copy your API key
4. Paste into `.env`

**NewsAPI** (Optional - for news search):
1. Go to https://newsapi.org/
2. Sign up (free tier: 100 requests/day)
3. Copy your API key
4. Paste into `.env`

> **Note**: The system works without SerpAPI/NewsAPI keys using mock data. Only OpenAI is required for AI explanations.

## Step 3: Test the Setup

Run the test script to verify everything is working:

```bash
python agents/test_agents.py
```

You should see:
```
🌸 BloomWatch AI Agents Test Suite 🌸
Test 1: Basic Orchestration (Mock Mode)
✓ Region: Kashmir Valley
✓ Flower: tulip
...
🎉 All Tests Passed!
```

## Step 4: Start the Server

```bash
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Server will start at: `http://localhost:8000`

## Step 5: Test the API

### Option A: Using cURL

```bash
curl -X POST "http://localhost:8000/api/explain" \
  -H "Content-Type: application/json" \
  -d '{
    "region": "Kashmir Valley",
    "flower": "tulip",
    "ndvi_score": 0.75,
    "use_mock_search": true
  }'
```

### Option B: Using the API docs

1. Open browser: http://localhost:8000/docs
2. Find the `/api/explain` endpoint
3. Click "Try it out"
4. Fill in the request body:
```json
{
  "region": "California",
  "flower": "sunflower",
  "ndvi_score": 0.82,
  "use_mock_search": false
}
```
5. Click "Execute"

### Option C: Using Python

```python
import requests

response = requests.post('http://localhost:8000/api/explain', json={
    "region": "Kashmir Valley",
    "flower": "tulip",
    "ndvi_score": 0.75
})

print(response.json()['explanation'])
```

## Understanding the Response

```json
{
  "region": "Kashmir Valley",
  "flower": "tulip",
  "scientific_name": "Tulipa",
  "explanation": "AI-generated detailed explanation...",
  "bloom_period": "March to May",
  "ndvi_score": 0.75,
  "abundance_level": "high",
  "season": "Spring 2025",
  "factors": ["Temperature...", "Precipitation...", ...],
  "web_research": {
    "summary": "Recent findings from web search...",
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

## Architecture Overview

```
┌─────────────────────────────────────────────┐
│           /api/explain Endpoint             │
└──────────────────┬──────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────┐
│        Master Orchestrator Agent            │
│  (Coordinates all agents concurrently)      │
└──────────┬─────────────────────┬────────────┘
           │                     │
           ▼                     ▼
┌──────────────────┐   ┌──────────────────────┐
│ Explanation Agent│   │ Web Search Agent     │
│                  │   │ ┌────────┐ ┌───────┐ │
│ Uses GPT-4o-mini │   │ │SerpAPI │ │NewsAPI│ │
│ Generates bloom  │   │ └────────┘ └───────┘ │
│ explanations     │   │ Real-time web search │
└──────────────────┘   └──────────────────────┘
           │                     │
           └─────────┬───────────┘
                     ▼
           ┌─────────────────┐
           │ Merged Response │
           └─────────────────┘
```

## Quick Troubleshooting

### "LLM not available" warning
- Check your `OPENAI_API_KEY` in `.env`
- Verify the key is valid and has credits
- System will use fallback explanations

### "Search unavailable" message
- SerpAPI/NewsAPI keys missing or invalid
- Set `"use_mock_search": true` for testing
- Or add the API keys to `.env`

### Module import errors
```bash
pip install -r requirements.txt --force-reinstall
```

### Port already in use
```bash
# Use a different port
python -m uvicorn main:app --reload --port 8001
```

## Development Tips

### 1. Use Mock Mode for Fast Testing

```json
{
  "region": "Test",
  "flower": "rose",
  "ndvi_score": 0.7,
  "use_mock_search": true  // No API calls!
}
```

### 2. Monitor API Usage

- OpenAI: https://platform.openai.com/usage
- SerpAPI: https://serpapi.com/dashboard
- NewsAPI: https://newsapi.org/account

### 3. Adjust Timeouts

In `.env`:
```env
AGENT_TIMEOUT=30  # Increase for slower connections
```

### 4. Enable Debug Logging

In `.env`:
```env
DEBUG=True
LOG_LEVEL=DEBUG
```

## Adding New Flowers

Edit `server/agents/explanation_agent.py`:

```python
FLOWER_DATABASE = {
    "your_flower": {
        "scientific": "Scientific Name",
        "bloom_period": "Month Range"
    },
    # ...
}
```

## Performance Optimization

1. **Use caching** for repeated queries (TODO)
2. **Limit search results** (default: 5 per source)
3. **Set appropriate timeouts** (default: 30s)
4. **Monitor API quotas** to avoid rate limits

## Next Steps

- [ ] Integrate with frontend map interface
- [ ] Add image analysis for uploaded photos
- [ ] Implement caching layer
- [ ] Add user feedback collection
- [ ] Deploy to production

## Support

For issues or questions:
1. Check the logs: `tail -f logs/server.log`
2. Run tests: `python agents/test_agents.py`
3. Review API docs: `http://localhost:8000/docs`

## Cost Estimates (Free Tiers)

- **OpenAI**: $5 free credit for new accounts
- **SerpAPI**: 100 searches/month free
- **NewsAPI**: 100 requests/day free

Typical costs:
- One explanation: ~$0.002-0.01 (OpenAI)
- Web searches: Free (within limits)

**Total for demo**: < $1 for 100+ queries! 🎉

---

Happy hacking! 🌸🚀
