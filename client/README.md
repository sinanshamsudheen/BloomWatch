# BloomWatch – Client

## Objective
The frontend is the user’s gateway for exploring plant blooming activity globally. It delivers interactive maps, region/flower selection, and compelling visualization of abundance overlays and ecological insights.

## Core Responsibilities
- Show globe/map with free, interactive region selection (MapLibre GL JS).
- Accept user input for region and flower name.
- Display NDVI-derived abundance overlays (color-mapped, with legend).
- Request and show bloom explanations/context panels per region/flower.
- Ensure responsive, fast, and robust user experience.

## Final Goals
- Let users explore any region’s blooming potential instantly.
- Visual overlays and summary explanations are clear and intuitive.
- Frontend is demo-ready, responsive, and runs on Lovable with robust integration to backend APIs.

## Data Flow
1. User selects region and flower on map/input bar.
2. Send request to `/abundance` (and optionally `/explanation`) endpoint.
3. Receive and display abundance grid as overlay.
4. Show explanation/context in side/info panel.

## Tech Stack
- Lovable (prototyping)
- MapLibre GL JS (free/open-source interactive map and globe)
- JavaScript/TypeScript, GeoJSON, OpenStreetMap layers

## Instructions
- Install all frontend dependencies as needed (Lovable setup, npm install etc).
- Configure environment for backend endpoint URLs and map API keys if needed.
- Run client app in dev mode during hacking for rapid iteration.
