# BloomWatch - Global Flower Bloom Exploration Platform
<img width="1873" height="997" alt="image" src="https://github.com/user-attachments/assets/9f5be4ed-9341-4a97-8a0c-bf6410649a7a" />

## Overview
BloomWatch is an open-source, rapid-deployment Earth observation platform that leverages NASA satellite data and AI agents to monitor, visualize, and explain global plant blooming events. The platform features an interactive 3D globe interface with real-time bloom data, AI-generated ecological explanations, and flower identification from images.

---

## Objectives
- **Visualize bloom abundance for user-selected regions and flowers**
- **Provide interactive globe/map interface with region selection tools**
- **Generate AI-powered bloom explanations with real-time web research**
- **Enable flower identification from uploaded images**
- **Show top regions for specific flowers**

---

## Key Features

- **Interactive 3D Globe Visualization**: Using MapLibre GL JS with a beautiful globe projection
- **Region Search with Autocomplete**: Real-time location suggestions via OpenStreetMap Nominatim API
- **Flower Identification**: AI-powered flower recognition from uploaded images
- **AI-Powered Bloom Explanations**: CrewAI agents with OpenAI integration to generate detailed ecological explanations
- **Web Research Integration**: Real-time data from SerpAPI and NewsAPI for current bloom conditions
- **Top Regions Visualization**: Highlighting most popular locations for specific flowers
- **Monthly Bloom Predictions**: Seasonal bloom forecasts based on historical patterns
- **Chatbot Assistance**: AI-powered chat for bloom-related queries
- **Responsive Design**: Optimized for desktop and mobile experiences
- **Abundance Visualization**: Color-coded overlays showing bloom intensity

---

## Architecture

### Frontend
- **Platform**: React 18 with TypeScript
- **UI Framework**: Shadcn/ui components with Tailwind CSS
- **Map Engine**: MapLibre GL JS with 3D globe projection
- **State Management**: React Query for server state, React hooks for local state
- **Build Tool**: Vite
- **Features**:
  - Region search with autocomplete
  - Flower name input with suggestions
  - 3D globe visualization with abundance overlays
  - Context panel for AI-generated explanations
  - Image upload for flower classification
  - Top regions visualization
  - Responsive split-screen layout

### Backend
- **Framework**: FastAPI (Python 3.10+)
- **AI Integration**: CrewAI for agentic workflows, OpenAI for explanations
- **APIs**: SerpAPI and NewsAPI for real-time web research
- **Endpoints**:
  - `/api/explain` – Bloom explanations with web research (POST/GET)
  - `/api/abundance` – NDVI abundance data for region and flower
  - `/api/classify` – Flower image classification
  - `/api/top-regions` – Top regions for a specific flower in a country
  - `/api/monthly-predictions` – Seasonal bloom forecasts
  - `/api/chat` – AI-powered chat functionality
- **Security**: Environment-based API key configuration

### AI/Agents Architecture
- **Master Orchestrator**: Coordinates all AI agents and manages workflow
- **Explanation Agent**: Generates botanical bloom explanations using LLMs
- **Web Search Agent**: Retrieves real-time data from external sources
- **Concurrent Processing**: Agents run in parallel for faster responses
- **Fallback Mechanisms**: Graceful degradation when APIs are unavailable

### Visualization
- **Base Map**: OpenStreetMap tiles with custom globe styling
- **Abundance Overlay**: Color-coded GeoJSON polygons based on bloom intensity
- **Top Regions Markers**: Ranked visual indicators with popup information
- **Interactive Controls**: Zoom, rotation, and reset functionality
- **Legend Display**: Clear mapping of colors to bloom intensity levels

---

## Workflow/Data Flow

1. **User selects region and flower** via the search interface
2. **Frontend requests `/api/explain` with parameters**
3. **Backend orchestrator runs explanation agent and web search agent in parallel**
4. **Web search agent queries SerpAPI and NewsAPI for current bloom data**
5. **Explanation agent uses OpenAI to generate ecological explanations**
6. **Backend combines all data sources into a comprehensive response**
7. **Frontend displays results in the info panel and updates the map visualization**
8. **Optional**: User uploads flower image to `/api/classify` for identification
9. **Optional**: Backend determines top regions for the identified flower and displays them on the map

---

## Tech Stack

### Frontend
- **Framework**: React 18 with TypeScript
- **UI Components**: Shadcn/ui with Radix UI primitives
- **Styling**: Tailwind CSS with custom design tokens
- **Map**: MapLibre GL JS with 3D globe projection
- **State Management**: React Query, React Hook Form
- **Build Tool**: Vite
- **Icons**: Lucide React

### Backend
- **Framework**: FastAPI (Python 3.10+)
- **AI/Agents**: CrewAI, LangChain, OpenAI
- **APIs**: SerpAPI, NewsAPI
- **HTTP Client**: Requests
- **Data Processing**: NumPy
- **Geospatial**: GeoJSON for data exchange

### Visualization & UI
- **Map Engine**: MapLibre GL JS (free alternative to Mapbox)
- **UI Framework**: Radix UI primitives for accessibility
- **Styling**: Tailwind CSS with custom theme
- **Icons**: Lucide React

---

## Usage Scenarios

- **Scientists** tracking phenology shifts globally
- **Farmers** identifying optimal crop bloom windows
- **Conservationists** locating valuable flowering hotspots
- **Tourists** discovering when and where specific flowers bloom
- **Botanists** exploring bloom patterns and ecological relationships
- **General public** learning about plant phenology

---

## Current Status & Future Enhancements

### Currently Implemented
- ✅ Interactive 3D globe interface with custom styling
- ✅ Region search with autocomplete via Nominatim API
- ✅ AI-powered bloom explanations using CrewAI agents
- ✅ Web research integration for real-time data
- ✅ Image upload and flower classification
- ✅ Top regions visualization with ranked markers
- ✅ Monthly bloom predictions
- ✅ Chatbot functionality
- ✅ Abundance visualization overlay

### Planned Enhancements
- 🔲 Real NASA EarthData API integration (currently using mock data)
- 🔲 Advanced flower detection using computer vision models
- 🔲 Historical bloom pattern analysis
- 🔲 Multi-region comparison features
- 🔲 Mobile app development
- 🔲 Offline capability for field work
- 🔲 Integration with weather forecasting services

---

## Running the Application

### Prerequisites
- Node.js (v18+) and Bun for the frontend
- Python 3.10+ for the backend
- API keys for OpenAI, SerpAPI, and NewsAPI (optional, for full functionality)

### Frontend Setup
1. Navigate to the client directory: `cd client`
2. Install dependencies: `bun install`
3. Create `.env` file with API configuration:
   ```
   VITE_API_URL=http://localhost:8000
   ```
4. Start the development server: `bun run dev`

### Backend Setup
1. Navigate to the server directory: `cd server`
2. Create and activate a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies: `pip install -r requirements.txt`
4. Create a `.env` file with API keys:
   ```
   OPENAI_API_KEY=your_openai_key
   SERPAPI_API_KEY=your_serpapi_key
   NEWSAPI_API_KEY=your_newsapi_key
   ```
5. Start the server: `python main.py` or `uvicorn main:app --reload`

### API Endpoints
- `POST /api/explain` - Get bloom explanation with web research
- `GET /api/abundance` - Get abundance data for region and flower
- `POST /api/classify` - Upload and classify flower image
- `POST /api/top-regions` - Get top regions for a flower in a country
- `POST /api/monthly-predictions` - Get seasonal bloom forecasts
- `POST /api/chat` - Send message to bloom expert chatbot

---

By leveraging AI agents, real-time web research, and interactive visualization, BloomWatch provides a comprehensive platform for understanding global flower bloom patterns.
