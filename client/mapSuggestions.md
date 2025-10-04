MapLibre styles are managed in JSON documents specifying the map’s visual appearance. For your interactive globe requirement, you should focus on styles and properties related to base layers, sources, and camera/view controls that provide realistic and rich 3D-like interactions.

### Recommended MapLibre Style Properties for a Globe Map

- **version**: Set to the latest (currently 8) for full features.
- **name**: Name your style (e.g., “BloomWatch Global Style”).
- **sources**: Use vector or raster sources such as OpenStreetMap for global coverage.
- **layers**: 
  - Base layer: Clearly styled for natural terrain, land, and water (keep color-neutral, highlight greenery if possible).
  - Boundary/highlight layers: For region outlines, polygons, and dynamic overlays.
  - Heatmap layers: For abundance overlays—style with color gradients (greens and blues for nature themes).
- **center**: Set global coordinates (e.g., `[0][0]` for prime meridian).
- **zoom**: Keep default low (1 or 2) for global view. Increase dynamically when a region is selected.
- **pitch** and **bearing**: For globe-style effect, set pitch between 60-75 and allow user control of bearing (rotation).
- **metadata**: Use for style documentation—won’t affect visuals.
- **3D Visualization**: MapLibre doesn’t natively do full 3D, but high pitch angle simulates a tilted globe. Use realistic sphere projection layers if available.

### Style Recommendations

- Use a neutral world base, distinct continent outlines, smooth blue oceans, and subtle terrain shading.
- Add “globe” effect using high pitch angles in initial view (`"pitch": 60-75`) and allow bearing rotation controls for spin.
- Overlay NDVI or abundance regions with translucent, color-mapped polygons or heatmap layers for dynamic visualization.
- Configure transitions for zoom (from globe to region) with animated bearing/pitch changes for realism.
- Include a visible legend explaining overlay colors.

### Example Style Skeleton

```json
{
  "version": 8,
  "name": "BloomWatch Global Style",
  "center": [0, 0],
  "zoom": 1.5,
  "pitch": 65,
  "bearing": 0,
  "sources": {
    "osm": {
      "type": "vector",
      "url": "https://osm-source-url"
    }
  },
  "layers": [
    {
      "id": "base-terrain",
      "type": "background",
      "paint": {
        "background-color": "#061E3F"
      }
    },
    {
      "id": "abundance-heatmap",
      "type": "heatmap",
      "source": "osm",
      "paint": {
        "heatmap-color": [
          "interpolate", ["linear"], ["heatmap-density"],
          0, "#00C853",
          1, "#1DE9B6"
        ],
        "heatmap-intensity": 0.8
      }
    }
  ]
}
```

### Summary

- Select a “tilted globe” base map style with high pitch, low zoom, and bearing rotation enabled.
- Use natural terrain, land, and ocean colors that enhance overlay contrast.
- Add vector/raster polygon or heatmap layers for dynamic, real-time bloom/NDVI overlays.
- Adjust style transitions for fluid zoom and region targeting after input.

This style setup will make BloomWatch visually impressive and ensure smooth globe-to-region transitions as envisioned.

[1](https://maplibre.org/maplibre-style-spec/)