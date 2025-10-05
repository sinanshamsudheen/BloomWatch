import { useEffect, useRef, useState, useCallback } from "react";
import maplibregl from "maplibre-gl";
import "maplibre-gl/dist/maplibre-gl.css";
import { Loader2 } from "lucide-react";
import { toast } from "sonner";
import { RegionInfo } from "@/types/api";

interface MapViewProps {
  region?: string;
  flower?: string;
  coordinates?: [number, number];
  topRegions?: RegionInfo[];
  abundanceData?: import("@/types/api").AbundanceData;
  onLocationSelect?: (location: string, coordinates: [number, number]) => void;
}

const MapView = ({ region, flower, coordinates, topRegions, abundanceData, onLocationSelect }: MapViewProps) => {
  const mapContainer = useRef<HTMLDivElement>(null);
  const map = useRef<maplibregl.Map | null>(null);
  const [loading, setLoading] = useState(true);
  const [mapLoaded, setMapLoaded] = useState(false);
  const markersRef = useRef<maplibregl.Marker[]>([]);

  // Function to get coordinates for a region (simplified for demo)
  const getRegionCoordinates = useCallback((regionName?: string) => {
    if (!regionName) return [0, 0]; // Default to center of globe
    
    // Simplified mapping - in a real app, you'd use a geocoding service
    const regionMap: Record<string, [number, number]> = {
      "Amazon Rainforest": [-60, -3],
      "Sahara Desert": [13, 25],
      "Himalayas": [81, 28],
      "New York": [-74, 40.7],
      "London": [-0.1, 51.5],
      "Tokyo": [139.7, 35.7],
      "Sydney": [151, -33.9],
      "Mt. Fuji": [138.7, 35.4]
    };
    
    return regionMap[regionName] || [0, 0];
  }, []);

  // Function to determine zoom level (fixed at broader scale for all regions)
  const getZoomLevel = useCallback((regionName?: string) => {
    // Return zoom level 4 for broader view suitable for most regions
    return 4;
  }, []);

  // Effect for handling map reset event
  useEffect(() => {
    const handleResetMap = () => {
      if (map.current) {
        map.current.flyTo({
          center: [0, 20],
          zoom: 2.5,
          pitch: 0,
          bearing: 0,
          essential: true
        });
      }
    };

    window.addEventListener('resetMap', handleResetMap);
    
    return () => {
      window.removeEventListener('resetMap', handleResetMap);
    };
  }, []);

  useEffect(() => {
    if (mapContainer.current && !map.current) {
      // Initialize MapLibre GL JS with custom globe style
      map.current = new maplibregl.Map({
        container: mapContainer.current,
        style: {
          "version": 8,
          "name": "BloomWatch Global Style",
          "projection": {
            "type": "globe"
          },
          "sources": {
            "osm-raster": {
              "type": "raster",
              "tiles": [
                "https://a.tile.openstreetmap.org/{z}/{x}/{y}.png",
                "https://b.tile.openstreetmap.org/{z}/{x}/{y}.png",
                "https://c.tile.openstreetmap.org/{z}/{x}/{y}.png"
              ],
              "tileSize": 256,
              "attribution": "© OpenStreetMap contributors",
              "maxzoom": 19
            }
          },
          "sky": {
            "sky-color": "#080820",
            "sky-horizon-blend": 0.5,
            "horizon-color": "#1a1a2e",
            "horizon-fog-blend": 0.5,
            "fog-color": "#0f0f23",
            "fog-ground-blend": 0.5
          },
          "layers": [
            {
              "id": "background",
              "type": "background",
              "paint": {
                "background-color": "#000814"
              }
            },
            {
              "id": "osm-tiles",
              "type": "raster",
              "source": "osm-raster",
              "minzoom": 0,
              "maxzoom": 22,
              "paint": {
                "raster-opacity": 1
              }
            }
          ]
        },
        center: [0, 20], // starting position [lng, lat]
        zoom: 2.5, // starting zoom for better view (shows ~1000km scale)
        pitch: 0, // pitch for globe view (0 for direct view)
        bearing: 0, // starting bearing
        dragRotate: true, // Enable rotation
        touchPitch: true // Enable touch pitch
      });

      // Handle map load event
      map.current.on("load", () => {
        setLoading(false);
        setMapLoaded(true);
        
        // Add scale control to bottom-right
        map.current!.addControl(new maplibregl.ScaleControl({
          maxWidth: 100,
          unit: 'metric'
        }), "bottom-right");
      });

      // Handle style load error
      map.current.on("error", (e) => {
        console.error("Map error:", e.error);
        setLoading(false);
        toast.error("Failed to load map. Please check console for details.");
      });
    }

    return () => {
      if (map.current) {
        map.current.remove();
        map.current = null;
      }
    };
  }, []);

  // Update map view when region changes
  useEffect(() => {
    if (map.current && mapLoaded && region) {
      // Use provided coordinates or fall back to lookup
      const [lng, lat] = coordinates || getRegionCoordinates(region);
      
      // Determine zoom level based on region popularity
      const zoomLevel = getZoomLevel(region);

      // Animate to the new location with smooth globe rotation
      map.current.flyTo({
        center: [lng, lat],
        zoom: zoomLevel,
        pitch: 45,
        bearing: 0,
        duration: 2500,
        essential: true // This animation is considered essential with respect to accessibility
      });

      // Remove any existing markers
      if (map.current.getLayer("region-marker")) {
        map.current.removeLayer("region-marker");
        map.current.removeSource("region-marker");
      }

      // Add a marker for the selected region
      const markerData: GeoJSON.Feature<GeoJSON.Point> = {
        type: "Feature",
        properties: {},
        geometry: {
          type: "Point",
          coordinates: [lng, lat]
        }
      };

      map.current.addSource("region-marker", {
        type: "geojson",
        data: markerData
      });

      map.current.addLayer({
        id: "region-marker",
        type: "circle",
        source: "region-marker",
        paint: {
          "circle-radius": [
            "interpolate",
            ["linear"],
            ["zoom"],
            0, 6,
            10, 12
          ],
          "circle-color": "#F44336", // Red for the marker
          "circle-stroke-width": 2,
          "circle-stroke-color": "#FFFFFF",
          "circle-opacity": 0.9
        }
      });

      toast.success(`Zoomed to ${region}${flower ? ` for ${flower}` : ""}`);
    }
  }, [region, flower, coordinates, mapLoaded, getRegionCoordinates, getZoomLevel]);

  // Add NDVI abundance overlay when available
  useEffect(() => {
    if (map.current && mapLoaded && region) {
      // Remove existing NDVI layer if it exists
      if (map.current.getLayer("ndvi-overlay")) {
        map.current.removeLayer("ndvi-overlay");
      }
      if (map.current.getSource("ndvi-overlay")) {
        map.current.removeSource("ndvi-overlay");
      }

      // If abundance data is provided from backend, use it
      if (abundanceData) {
        // Use real abundance data from backend
        map.current.addSource("ndvi-overlay", {
          type: "geojson",
          data: abundanceData
        });

        map.current.addLayer({
          id: "ndvi-overlay",
          type: "fill",
          source: "ndvi-overlay",
          paint: {
            "fill-color": [
              "interpolate",
              ["linear"],
              ["get", "abundance"], // This comes from real NDVI data
              0,
              "#374151", // Low abundance - gray
              0.3,
              "#10B981", // Low-medium abundance - green
              0.6,
              "#F59E0B", // Medium-high abundance - amber
              1,
              "#EF4444"  // High abundance - red
            ],
            "fill-opacity": 0.6
          }
        });
      } else {
        // For demonstration, create a sample polygon around the selected region
        // Use provided coordinates or fall back to lookup
        const [lng, lat] = coordinates || getRegionCoordinates(region);
        
        // Create a sample polygon for demonstration - make it more region-specific based on region name
        let coordinatesPolygon;
        if (region && region.toLowerCase().includes('amazon')) {
          // Special shape for Amazon rainforest
          coordinatesPolygon = [
            [lng - 5, lat - 2],
            [lng + 2, lat - 4], 
            [lng + 7, lat],
            [lng + 2, lat + 4],
            [lng - 5, lat + 2],
            [lng - 5, lat - 2]
          ];
        } else if (region && region.toLowerCase().includes('himalaya')) {
          // Special shape for Himalayan region
          coordinatesPolygon = [
            [lng - 4, lat - 2],
            [lng + 1, lat - 3], 
            [lng + 5, lat - 1],
            [lng + 3, lat + 2],
            [lng - 2, lat + 3],
            [lng - 4, lat - 2]
          ];
        } else if (region && region.toLowerCase().includes('sahara')) {
          // Special shape for Sahara desert
          coordinatesPolygon = [
            [lng - 6, lat - 3],
            [lng + 4, lat - 5], 
            [lng + 8, lat + 1],
            [lng + 2, lat + 4],
            [lng - 6, lat + 2],
            [lng - 6, lat - 3]
          ];
        } else {
          // Default shape for other regions
          coordinatesPolygon = [
            [lng - 3, lat - 3],
            [lng + 3, lat - 3], 
            [lng + 3, lat + 3],
            [lng - 3, lat + 3],
            [lng - 3, lat - 3]
          ];
        }
        
        // Create a sample polygon for demonstration
        const ndviData: GeoJSON.FeatureCollection = {
          type: "FeatureCollection",
          features: [{
            type: "Feature",
            properties: {
              abundance: 0.7 // Example abundance value
            },
            geometry: {
              type: "Polygon",
              coordinates: [coordinatesPolygon]
            }
          }]
        };

        map.current.addSource("ndvi-overlay", {
          type: "geojson",
          data: ndviData
        });

        map.current.addLayer({
          id: "ndvi-overlay",
          type: "fill",
          source: "ndvi-overlay",
          paint: {
            "fill-color": [
              "interpolate",
              ["linear"],
              ["get", "abundance"], // This would come from real NDVI data
              0,
              "#374151", // Low abundance - gray
              0.3,
              "#10B981", // Low-medium abundance - green
              0.6,
              "#F59E0B", // Medium-high abundance - amber
              1,
              "#EF4444"  // High abundance - red
            ],
            "fill-opacity": 0.6
          }
        });
      }
    }
  }, [region, coordinates, mapLoaded, getRegionCoordinates, abundanceData]);

  // Highlight top regions with markers
  useEffect(() => {
    if (!map.current || !mapLoaded || !topRegions || topRegions.length === 0) {
      return;
    }

    // Clear existing markers
    markersRef.current.forEach(marker => marker.remove());
    markersRef.current = [];

    // Remove existing top regions layers
    if (map.current.getLayer("top-regions-circles")) {
      map.current.removeLayer("top-regions-circles");
    }
    if (map.current.getLayer("top-regions-labels")) {
      map.current.removeLayer("top-regions-labels");
    }
    if (map.current.getSource("top-regions")) {
      map.current.removeSource("top-regions");
    }

    // Filter regions that have coordinates
    const regionsWithCoords = topRegions.filter(r => r.coordinates && r.coordinates.length === 2);
    
    if (regionsWithCoords.length === 0) {
      toast.info("No coordinates available for top regions");
      return;
    }

    // Create GeoJSON for top regions
    const regionsGeoJSON: GeoJSON.FeatureCollection<GeoJSON.Point> = {
      type: "FeatureCollection",
      features: regionsWithCoords.map((region, index) => ({
        type: "Feature",
        properties: {
          name: region.name,
          full_name: region.full_name,
          rank: index + 1,
          confidence: region.confidence,
          mentions: region.mentions
        },
        geometry: {
          type: "Point",
          coordinates: region.coordinates!
        }
      }))
    };

    // Add source for top regions
    map.current.addSource("top-regions", {
      type: "geojson",
      data: regionsGeoJSON
    });

    // Add circle layer for regions
    map.current.addLayer({
      id: "top-regions-circles",
      type: "circle",
      source: "top-regions",
      paint: {
        "circle-radius": [
          "interpolate",
          ["linear"],
          ["zoom"],
          0, 8,
          5, 15,
          10, 25
        ],
        "circle-color": [
          "step",
          ["get", "rank"],
          "#10B981", // Rank 1 - Green
          2, "#3B82F6", // Rank 2 - Blue
          3, "#F59E0B", // Rank 3 - Amber
          4, "#EF4444", // Rank 4 - Red
          5, "#8B5CF6"  // Rank 5 - Purple
        ],
        "circle-opacity": 0.8,
        "circle-stroke-width": 3,
        "circle-stroke-color": "#FFFFFF",
        "circle-stroke-opacity": 1
      }
    });

    // Add labels for regions
    map.current.addLayer({
      id: "top-regions-labels",
      type: "symbol",
      source: "top-regions",
      layout: {
        "text-field": ["concat", ["to-string", ["get", "rank"]], ". ", ["get", "name"]],
        "text-font": ["Open Sans Bold"],
        "text-size": 14,
        "text-offset": [0, 2],
        "text-anchor": "top"
      },
      paint: {
        "text-color": "#FFFFFF",
        "text-halo-color": "#000000",
        "text-halo-width": 2
      }
    });

    // Add click handlers for regions
    map.current.on("click", "top-regions-circles", (e) => {
      if (!e.features || e.features.length === 0) return;
      
      const feature = e.features[0];
      const properties = feature.properties!;
      
      // Create popup content
      const popupContent = `
        <div style="font-family: system-ui; padding: 8px;">
          <h3 style="margin: 0 0 8px 0; font-size: 16px; font-weight: bold;">
            #${properties.rank} ${properties.name}
          </h3>
          <p style="margin: 4px 0; font-size: 13px; color: #666;">
            <strong>Mentions:</strong> ${properties.mentions}
          </p>
          <p style="margin: 4px 0; font-size: 13px; color: #666;">
            <strong>Confidence:</strong> ${properties.confidence.toFixed(1)}%
          </p>
          <p style="margin: 8px 0 0 0; font-size: 12px; color: #888;">
            ${properties.full_name}
          </p>
        </div>
      `;
      
      new maplibregl.Popup()
        .setLngLat(e.lngLat)
        .setHTML(popupContent)
        .addTo(map.current!);
    });

    // Change cursor on hover
    map.current.on("mouseenter", "top-regions-circles", () => {
      if (map.current) map.current.getCanvas().style.cursor = "pointer";
    });

    map.current.on("mouseleave", "top-regions-circles", () => {
      if (map.current) map.current.getCanvas().style.cursor = "";
    });

    // Fit map to show all regions
    if (regionsWithCoords.length > 0) {
      const bounds = new maplibregl.LngLatBounds();
      regionsWithCoords.forEach(region => {
        if (region.coordinates) {
          bounds.extend(region.coordinates as [number, number]);
        }
      });
      
      map.current.fitBounds(bounds, {
        padding: { top: 100, bottom: 100, left: 100, right: 100 },
        maxZoom: 6,
        duration: 2000
      });
      
      toast.success(`Showing ${regionsWithCoords.length} top region${regionsWithCoords.length > 1 ? 's' : ''} for ${flower}`);
    }

  }, [topRegions, mapLoaded, flower]);

  // Function to reset map to initial globe view
  const resetView = () => {
    if (map.current) {
      map.current.flyTo({
        center: [0, 20],
        zoom: 2.5,
        pitch: 0,
        bearing: 0,
        essential: true
      });
    }
  };

  return (
    <div className="relative w-full h-full bg-slate-900">
      {/* Map Container */}
      <div 
        ref={mapContainer} 
        className="absolute inset-0 w-full h-full [&_.maplibregl-ctrl-attrib]:hidden"
      />
      
      {/* Loading Overlay */}
      {loading && (
        <div className="absolute inset-0 bg-background/80 backdrop-blur-sm flex items-center justify-center z-10">
          <div className="text-center">
            <Loader2 className="h-12 w-12 animate-spin text-primary mx-auto mb-4" />
            <p className="text-foreground font-medium">Initializing 3D globe...</p>
            <p className="text-muted-foreground text-sm mt-1">Loading satellite data</p>
          </div>
        </div>
      )}

      {/* Reset Button - Top Right */}
      <div className="absolute top-6 right-6 z-20">
        <button
          onClick={resetView}
          className="p-2.5 bg-card/95 backdrop-blur-sm hover:bg-card rounded-lg border border-border shadow-soft transition-all hover:scale-105"
          aria-label="Reset view to globe"
          title="Reset to globe view"
        >
          <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
            <path d="M3 12a9 9 0 1 0 9-9 9.75 9.75 0 0 0-6.74 2.74L3 8"/>
            <path d="M3 3v5h5"/>
          </svg>
        </button>
      </div>

      {/* Legend */}
      <div className="absolute bottom-6 left-6 bg-card/95 backdrop-blur-sm rounded-lg p-4 border border-border shadow-soft z-20">
        <h4 className="text-sm font-semibold text-foreground mb-3">
          {topRegions && topRegions.length > 0 ? "Top Regions" : "Abundance"}
        </h4>
        {topRegions && topRegions.length > 0 ? (
          <div className="space-y-2">
            <div className="flex items-center gap-2">
              <div className="w-4 h-4 rounded-full bg-green-500 border-2 border-white" />
              <span className="text-xs text-muted-foreground">Rank 1</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-4 h-4 rounded-full bg-blue-500 border-2 border-white" />
              <span className="text-xs text-muted-foreground">Rank 2</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-4 h-4 rounded-full bg-amber-500 border-2 border-white" />
              <span className="text-xs text-muted-foreground">Rank 3</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-4 h-4 rounded-full bg-red-500 border-2 border-white" />
              <span className="text-xs text-muted-foreground">Rank 4</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-4 h-4 rounded-full bg-purple-500 border-2 border-white" />
              <span className="text-xs text-muted-foreground">Rank 5</span>
            </div>
          </div>
        ) : (
          <div className="space-y-2">
            <div className="flex items-center gap-2">
              <div className="w-4 h-4 rounded bg-gray-500" />
              <span className="text-xs text-muted-foreground">Low (0-0.3)</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-4 h-4 rounded bg-green-500" />
              <span className="text-xs text-muted-foreground">Low-Medium (0.3-0.6)</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-4 h-4 rounded bg-amber-500" />
              <span className="text-xs text-muted-foreground">Medium-High (0.6-0.8)</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-4 h-4 rounded bg-red-500" />
              <span className="text-xs text-muted-foreground">Very High (0.8-1.0)</span>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default MapView;
