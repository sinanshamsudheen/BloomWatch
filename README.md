# BloomWatch PRD – Hackathon Edition

## Overview
BloomWatch is an open-source, rapid-deployment Earth observation platform that leverages NASA satellite data and free mapping tools to monitor, visualize, and explain global plant blooming events. Designed for hackathon-scale delivery, it delivers interactive regional abundance mapping, ecological explanations, and scalable architecture powered entirely by free APIs and open data.

---

## Objectives
- **Visualize NDVI-based abundance grids for user-selected regions and flowers**
- **Offer interactivity for region selection on a globe/map using free tools**
- **Fetch and preprocess MODIS NDVI data via NASA's EarthData API**
- **Generate actionable bloom explanations with AI, linking ecological context**
- **Build a demo-ready MVP within 24 hours**

---

## Key Features

- Interactive map/globe for global and regional selection (MapLibre GL JS)
- Color-mapped overlay showing vegetation abundance (NDVI proxies blooming)
- Region and flower name input workflow (search/autocomplete)
- Data-driven abundance estimation with instant results
- GPT/AI-powered explanations about blooming phenomena for selected region
- Responsive frontend and robust FastAPI backend
- All components built using free/open-source or public APIs/libraries

---

## Architecture

### Frontend
- **Platform**: React (UI framework)
- **Map Engine**: MapLibre GL JS (Free, closest to Mapbox in features)
- **Features**:
  - Region selection (drawing, search, or click)
  - Flower name/species selector
  - NDVI abundance overlay (GeoJSON or raster tiles)
  - Context panel for ecological explanations
  - Legend, error messages, progress bars
  - Responsive layout

### Backend/API
- **Framework**: FastAPI (Python 3.10.10)
- **Data Fetching**: NASA EarthData API (MODIS MOD13Q1 v061 for NDVI)
- **Processing**: GDAL, rasterio, pandas, numpy (GeoTIFF/HDF to array, aggregation, bounding box filtering)
- **Endpoints**:
  - `/abundance` – inputs: region + flower → outputs: abundance grid (GeoJSON)
  - `/explanation` – inputs: region + flower → outputs: short bloom summary
- **Error/Empty State Handling**
- **Security**: Bearer token for authenticated NASA API access

### Model/Classification
- **NDVI-based estimation logic**: Maps NDVI ranges to vegetation abundance (proxy for bloom)
- **Optional Flower/Greenery Detection**: YOLO/FastAI model, MVP fallback to heuristic or static mapping
- **Reference Data**: Static CSV/JSON linking flowers, regions, habitats, bloom periods for explanations

### Mapping & Visualization
- **Base Map Data**: OpenStreetMap (for region context, via MapLibre)
- **Overlay Data**: All abundance data returned as color-mapped GeoJSON
- **User Experience**: Rich interactivity, real-time feedback

---

## Workflow/Data Flow

1. **User selects region and flower**
2. **Frontend requests `/abundance` from backend with parameters**
3. **Backend fetches NDVI imagery from MODIS MOD13Q1 via NASA API (Bearer Token), preprocesses to region boundaries**
4. **NDVI processed into abundance estimation grid or GeoJSON**
5. **Backend serves mapped data to frontend, which overlays colored NDVI abundance**
6. **Optional:** Frontend requests `/explanation` endpoint for ecological summary, generated via GPT/AI model
7. **User explores map, abundance, and explanations**

---

## Tech Stack

- **Frontend**: React, MapLibre GL JS, TypeScript, GeoJSON, OpenStreetMap
- **Backend**: FastAPI, Python 3.10.10, GDAL, rasterio, pandas, numpy
- **Data**: NASA EarthData API (MODIS MOD13Q1 v061 NDVI), reference CSV/JSON
- **AI/Explanations**: Qwen CLI, GPT (Sonnet 4.5), GitHub Copilot (coding & error handling)
- **Model**: Custom classifier and NDVI abundance heuristics (optional)
- **VCS & Deployment**: GitHub
- **Utilities**: Requirements.txt/Poetry, basic REST API clients

_All platform, datasets, and core tech stack components are free/open source or public datasets._

---

## Critical Hackathon Priorities

1. MapLibre GL-based interactive NDVI map + region/flower selection UI (MVP)
2. MODIS NDVI backend data pipeline via NASA EarthData API
3. Abundance estimation and frontend overlay workflow
4. Ecological explanation panel (AI-driven or static)
5. End-to-end demo robustness, error handling, clean UX

_Optional: AI-powered flower image classification, advanced GPT-based storytelling, multi-region comparison, deeper statistical analysis._

---

## Usage Scenarios

- Scientist tracking phenology shifts globally
- Farmer identifying optimal crop bloom windows
- Conservationist locating valuable flowering hotspots
- Public user exploring bloom trends and ecological stories

---

## Scalability & Next Steps

Post-hackathon, expand regional detail (Landsat or AVIRIS), improve detection models, add mobile support, connect with conservation/crop management systems, and enable real-time data pipelines.

---

By structuring BloomWatch in this way, you maximize impact, keep all development cost-free, and lay foundations for rapid scaling and future innovation.
