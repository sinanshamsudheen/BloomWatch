# BloomWatch Project Context

## Project Overview

BloomWatch is an open-source, rapid-deployment Earth observation platform that leverages NASA satellite data and free mapping tools to monitor, visualize, and explain global plant blooming events. It's designed as a hackathon-scale project to deliver an interactive regional abundance mapping system with ecological explanations and scalable architecture powered entirely by free APIs and open data.

## Architecture

### Frontend
- **Platform**: React with TypeScript, Vite build system
- **UI Framework**: shadcn/ui components with Tailwind CSS
- **Map Engine**: MapLibre GL JS (used as a simulated visualization in the current implementation)
- **Features**:
  - Interactive map/globe for global and regional selection
  - Region and flower name input workflow with search/autocomplete
  - NDVI abundance overlay visualization
  - Context panel for ecological explanations
  - Image upload functionality for flower classification

### Backend
- **Framework**: Planned to be FastAPI (Python 3.10.10) - not yet implemented
- **Data Sources**: NASA EarthData API (MODIS MOD13Q1 v061 for NDVI)
- **Processing**: GDAL, rasterio, pandas, numpy for geospatial processing
- **Planned Endpoints**:
  - `/abundance` – inputs: region + flower → outputs: abundance grid (GeoJSON)
  - `/explanation` – inputs: region + flower → outputs: short bloom summary
  - `/classify` – inputs: image → outputs: flower identification and location

### Model/Classification
- **NDVI-based estimation logic**: Maps NDVI ranges to vegetation abundance (proxy for bloom)
- **Planned Flower Detection**: YOLO/FastAI model for image-based flower identification
- **Reference Data**: Static CSV/JSON linking flowers, regions, habitats, bloom periods

## Current Implementation Status

The project currently has a well-designed frontend with:
- Split-screen layout (info panel on left, map visualization on right)
- Interactive search functionality for region and flower selection
- Simulated globe visualization with zoom controls
- Loading states and error handling
- Image upload functionality (currently simulated)

The backend implementation is planned but not yet created.

## Files and Directories

- `client/` - Frontend React application built with TypeScript, Vite, and shadcn/ui
- `server/` - Backend directory (currently only contains a placeholder README)
- `model/` - Directory for ML models and classification logic (currently only contains documentation)
- `logs/` - Directory for application logs

## Tech Stack

### Frontend Technologies
- **Framework**: React 18 with TypeScript
- **Build Tool**: Vite
- **UI Components**: shadcn/ui with Radix UI primitives
- **Styling**: Tailwind CSS with custom theme
- **Maps**: MapLibre GL JS (planned)
- **State Management**: React Query, React Hook Form
- **Icons**: Lucide React
- **Charts**: Recharts

### Planned Backend Technologies
- **Framework**: FastAPI (Python)
- **Geospatial Processing**: GDAL, rasterio, pandas, numpy
- **Data**: NASA EarthData API (MODIS MOD13Q1 v061 NDVI)

## Building and Running

### Frontend Development
```bash
cd client
bun install
bun run dev
```

### Frontend Production Build
```bash
cd client
bun run build
```

## API Endpoints (Planned)

- `GET /abundance` - Get NDVI abundance data for a region and flower
- `GET /explanation` - Get ecological explanation for bloom patterns
- `POST /classify` - Upload and classify flower images

## Development Conventions

- Type-safe React components with TypeScript
- Shadcn/ui component library for consistent UI
- Tailwind CSS for styling with custom design tokens
- Responsive design for all screen sizes
- Consistent error handling and loading states
- Nature-inspired aesthetic with green/blue color palette

## Project Objectives

1. Visualize NDVI-based abundance grids for user-selected regions and flowers
2. Offer interactivity for region selection on a globe/map using free tools
3. Fetch and preprocess MODIS NDVI data via NASA's EarthData API
4. Generate actionable bloom explanations with AI, linking ecological context
5. Build a demo-ready MVP within 24 hours (hackathon scope)

## Usage Scenarios

- Scientists tracking phenology shifts globally
- Farmers identifying optimal crop bloom windows
- Conservationists locating valuable flowering hotspots
- General public exploring bloom trends and ecological stories

## Next Steps

The project needs a backend implementation to connect with NASA's EarthData API and provide the real NDVI data processing capabilities that are currently simulated in the frontend.