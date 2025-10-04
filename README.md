# BloomWatch

## Project Overview
BloomWatch is a web-based Earth observation application designed to leverage NASA satellite data and AI to monitor, visualize, and explain plant blooming events on a global scale. The platform serves as an interactive hub, allowing users to explore flowering hotspots, track phenology trends, detect flowering in user-uploaded images using AI, and receive accessible explanations about flowering patterns, climate impact, and seasonal changes. BloomWatch aims to empower scientists, farmers, travelers, and nature enthusiasts by making the dynamics of global vegetation engaging and understandable, contributing to climate awareness and biodiversity knowledge [file:1].

## End Goal
The primary objective is to build a live, polished web application that:
- Provides real-time, interactive maps of flowering activity worldwide
- Analyzes and visualizes trends in plant phenology leveraging satellite data
- Uses AI to detect and classify blooming states in user-submitted images
- Offers educational, context-sensitive explanations to users via GPT-powered natural language modules
- Supports actionable insights for agriculture, climate science, eco-tourism, and public engagement [file:1]

## Objectives
- **Visualization**: Interactive global map visualizing flowering activity using various views (satellite imagery, NDVI color layers, heatmaps)
- **Prediction/Monitoring**: Display phenological shifts and seasonal trends using NASA MODIS and Sentinel datasets
- **User Engagement**: Enable users to upload plant/flower photos for AI-based blooming detection and classification (YOLO-based)
- **Education/Storytelling**: Generate GPT-powered, region-specific micro-explanations about blooming events and their environmental significance [file:1]

## Key Features

### Global Flowering Map
- Mapbox-powered visualization
- Satellite imagery, NDVI (Normalized Difference Vegetation Index) coloring, blooming heatmaps
- Time slider to visualize seasonal/monthly changes in flowering

### AI Flower Detection
- Users upload images of plants/flowers
- YOLO model detects presence and blooming state
- Outputs classification linked to relevant phenology data for that species/region

### Smart Explanations
- Contextual, GPT-generated micro-explanations (e.g., reasons for cherry blossom timing in Japan)
- Region-specific output based on user selection

### Data Insights
- Time-series trend charts of flowering/vegetation indices by region
- Seasonal comparisons (e.g., Spring 2000 vs. Spring 2025)
- Climate mode/toggle to highlight decadal changes [file:1]

## Data Sources
- **NASA MODIS NDVI**: Global vegetation index data
- **Sentinel-2**: Satellite imagery via Google Earth Engine
- **Open Phenology Datasets**: USA-NPN, Global Phenology Database

## Technical Requirements

### Tech Stack
- **Frontend**: Lovable (for rapid UI prototyping)
- **Mapping**: Mapbox (multi-layer, with time slider control)
- **Backend**: Python (FastAPI/Flask for API/data integration)
- **AI/ML Models**: YOLO for flower detection; GPT for text explanations
- **Data Processing**: Pandas, NumPy, Google Earth Engine API [file:1]

### Workflow for AI Agents
1. Ingest relevant NASA, Sentinel, and public phenology datasets
2. Render interactive global flowering maps with selectable overlays and time sliders
3. Accept and preprocess user-uploaded images
4. Run YOLO detection/classification to determine blooming status; link results to map/phenology data
5. Generate and display GPT-based contextual explanations for trends, species information, and climate linkages

### Success Metrics
- **Coverage**: Global flowering data coverage, across all continents
- **User Engagement**: At least three interactive map layers, with a functioning time slider
- **AI Performance**: 80%+ accuracy in demo for flower detection
- **Educational Value**: Measurable improvement in user understanding via GPT explanations and feedback [file:1]

## User Personas and Stories
- **Farmer**: Uses the tool to optimize planting/harvest by monitoring local flowering trends
- **Scientist**: Studies global phenology data sets to research climate change impacts
- **Traveler**: Plans visits to natural attractions by checking flowering schedules
- **Student/Nature Lover**: Interactively learns about flowering phenomena worldwide

## Hackathon and Delivery Goals
- Deliver a polished demo web application within 24 hours for hackathon showcasing
- Demo highlights: global map, AI-powered photo uploads, GPT explanations
- Presentations should cover the global relevance in climate science, agriculture, and eco-tourism

## Future Roadmap
- Deeper integration with agricultural advisory systems and farmer mobile apps
- Biodiversity and conservation monitoring modules [file:1]

---

This documentation should inform AI agents about BloomWatch's scope, architecture, workflow, main use cases, and the concrete outcomes expected for both demo and production environments.
