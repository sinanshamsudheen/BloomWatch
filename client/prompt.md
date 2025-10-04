Build the BloomWatch frontend as an interactive web application for global flower bloom exploration. Use a split-screen layout: the left half displays information, explanations, and context panels; the right half visualizes a map.

Core UI:
- Top center: Input Bar with search capability for users to enter a region/location and optionally a flower name. Inputs should be intuitive, support autocomplete, and clearly labeled.
- Right side: Realistic 3D rotating globe visualization (default view). The globe must be interactive, allowing rotation and zoom. (If true 3D is too complex, use a high-fidelity map with globe style and zoom/rotate functionality.)
- Upon region selection/search, smoothly transition (zoom) from the global map to the chosen region.
- Request backend API for abundance/heatmap data, and overlay the returned colored grid or polygons on the map. Region overlays must be clearly distinguished, with legends and high visual contrast.
- On result load, automatically display the most recent NDVI abundance layer and show a contextual "explanation panel" on the left. Explanations should be detailed, easy to understand, and dynamically updated based on region and flower queries.
- Always keep left side for information, featuring:
  - Project summary and feature highlights
  - Flower identification results (if available)
  - Heatmap statistics for selected region/flower
  - Ecological explanations and bloom insights
  - Loading/progress, error, or empty state messages
- On all pages, provide an “Upload Image” option (file input) for users to upload a flower or landscape photo. On image submission:
  - Send image to backend for classification
  - Show detected flower name/species, bloom status, and its most abundant region
  - Automatically zoom in to that region, update the heatmap overlay, and update the explanation panel accordingly

Design Details:
- Maintain modern, clean, and nature-inspired aesthetic throughout
- Responsive design for all screens and devices
- All interactions (search, region select, image upload, map zoom) must give instant feedback
- Place legends, map controls, and input bars for highest usability
- Prepare robust error and loading states so demo is fail-safe

Features to support:
- Interactive region selection by search, map-click, or drawing
- Flower name input/autocomplete
- Always-visible explanations and bloom statistics
- NDVI-based abundance overlays for clear visual feedback
- Image upload and AI-driven flower/bloom classification
- One-click zoom to most abundant region after image classification
- Clear legend and instructions for every major action

Use APIs endpoints: `/abundance` for NDVI overlays, `/explanation` for contextual info, and `/classify` for image upload (if implemented).

The experience should impress users and judges by being seamless, informative, and visually appealing. Emphasize global–regional transitions, real-time map updates, and rich left-side explanations.

