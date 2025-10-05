# BloomWatch Project Structure and Workflow

## System Architecture Flowchart

```mermaid
graph TD
    subgraph "Frontend (React + TypeScript)"
        A[User Interface] --> B[Search Bar Component]
        A --> C[Map View Component]
        A --> D[Info Panel Component]
        A --> E[Image Upload Component]
        B --> F[API Service - bloomwatch.ts]
        C --> F
        D --> F
        E --> F
    end

    subgraph "Backend (FastAPI + Python)"
        G[FastAPI Server] --> H[API Routes]
        H --> I[Abundance Router]
        H --> J[Explanation Router]
        H --> K[Classify Router]
        H --> L[Top Regions Router]
        
        I --> M[NDVI Service]
        J --> N[Agentic Architecture]
        K --> O[Classification Service]
        L --> P[Top Regions Service]
        
        N --> Q[Orchestrator Agent]
        N --> R[Explanation Agent]
        N --> S[Web Search Agent]
        
        M --> T[Google Earth Engine API]
        M --> U[NASA EarthData API]
        R --> V[OpenAI API]
        S --> W[SERPAPI/NewsAPI]
        O --> X[YoloV8 Model]
    end
    
    subgraph "Data Sources"
        Y[NASA Satellite Data MODIS] --> T
        Z[Flower Image Dataset] --> X
    end
    
    subgraph "Machine Learning Models"
        AA[YoloV8 - Flower Classification] --> O
        AB[OpenAI - Explanation Generation] --> R
    end
    
    subgraph "External APIs"
        AC[OpenAI API] --> V
        AD[SERPAPI/NewsAPI] --> W
        AE[NASA EarthData API] --> U
        AF[Google Earth Engine API] --> T
    end

    F <--> G
    X --> AA
    V --> AB
    W --> N
    U --> M
    T --> M

    style A fill:#e1f5fe
    style G fill:#f3e5f5
    style Y fill:#e8f5e8
    style Z fill:#e8f5e8
    style AA fill:#fff3e0
    style AB fill:#fff3e0
    style AC fill:#fce4ec
    style AD fill:#fce4ec
    style AE fill:#fce4ec
    style AF fill:#fce4ec
```

## Detailed Workflow Process

### 1. User Interaction Flow
1. User accesses the BloomWatch web application
2. User can either:
   - Search for a specific region and flower species
   - Upload an image of a flower for classification
3. Frontend sends API requests to backend based on user action

### 2. Backend Processing Flows

#### Flow A: Region/Flower Search
1. Frontend calls `/api/explain` endpoint with region and flower
2. Backend orchestrates multiple agents:
   - **Explanation Agent**: Generates ecological explanations using OpenAI
   - **Web Search Agent**: Fetches real-time information from SERPAPI/NewsAPI
   - **Orchestrator**: Coordinates both agents and synthesizes responses
3. **NDVI Service** retrieves satellite data from NASA EarthData API
4. Backend returns bloom explanation with abundance data to frontend

#### Flow B: Image Classification
1. User uploads flower image via frontend
2. Frontend calls `/api/classify` endpoint
3. Backend uses **Classification Service** with YoloV8 model to identify flower species
4. Returns identified species back to frontend
5. Frontend can then initiate search for abundance data for identified species

#### Flow C: Top Regions Discovery
1. Frontend calls `/api/top-regions` to find optimal viewing locations
2. Backend processes request and returns top regions for specific flower species
3. Results displayed on map in frontend

### 3. Technical Components

#### Frontend Components
- **React Application**: Main UI built with TypeScript
- **Shadcn/UI**: Component library with Tailwind CSS
- **MapLibre GL**: Interactive map visualization
- **React Query**: Server state management
- **API Service**: Communication with backend

#### Backend Components
- **FastAPI**: Web framework with Pydantic models
- **CrewAI**: Agentic architecture for AI tasks
- **LangChain**: LLM integration and orchestration
- **Ultralytics**: YoloV8 model for flower classification
- **GDAL/rasterio**: Geospatial data processing

### 4. Data Flow
- User provides input (region + flower, or image file)
- Frontend sends request to backend APIs
- Backend processes with appropriate services
- External API calls (NASA, OpenAI, etc.) are made as needed
- Results are returned to frontend for display
- Map visualization is updated with relevant data

This architecture provides a comprehensive platform for exploring global flower bloom patterns using satellite data and AI-driven explanations.