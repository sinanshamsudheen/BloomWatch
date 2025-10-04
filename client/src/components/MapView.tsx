import { useEffect, useRef, useState, useCallback } from "react";
import maplibregl from "maplibre-gl";
import "maplibre-gl/dist/maplibre-gl.css";
import { Loader2 } from "lucide-react";
import { toast } from "sonner";

interface MapViewProps {
  region?: string;
  flower?: string;
  coordinates?: [number, number];
  onLocationSelect?: (location: string, coordinates: [number, number]) => void;
}

const MapView = ({ region, flower, coordinates, onLocationSelect }: MapViewProps) => {
  const mapContainer = useRef<HTMLDivElement>(null);
  const map = useRef<maplibregl.Map | null>(null);
  const [loading, setLoading] = useState(true);
  const [mapLoaded, setMapLoaded] = useState(false);

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
        zoom: 1.2, // starting zoom for better globe view
        pitch: 0, // pitch for globe view (0 for direct view)
        bearing: 0, // starting bearing
        dragRotate: true, // Enable rotation
        touchPitch: true // Enable touch pitch
      });

      // Handle map load event
      map.current.on("load", () => {
        setLoading(false);
        setMapLoaded(true);
        
        // Add navigation controls
        map.current!.addControl(new maplibregl.NavigationControl(), "top-right");

        // Add scale control
        map.current!.addControl(new maplibregl.ScaleControl(), "bottom-left");
      });

      // Handle map clicks for location selection
      map.current.on("click", async (e) => {
        const { lng, lat } = e.lngLat;
        
        // Show loading toast
        const loadingToast = toast.loading("Fetching location...");
        
        try {
          // Reverse geocode the clicked location
          const response = await fetch(
            `https://nominatim.openstreetmap.org/reverse?format=json&lat=${lat}&lon=${lng}&zoom=10&addressdetails=1`,
            {
              headers: {
                'User-Agent': 'BloomWatch/1.0'
              }
            }
          );

          if (response.ok) {
            const data = await response.json();
            const locationName = data.display_name;
            
            // Call the callback with the selected location
            if (onLocationSelect) {
              onLocationSelect(locationName, [lng, lat]);
            }
            
            toast.success("Location selected!", { id: loadingToast });
          } else {
            toast.error("Could not fetch location details", { id: loadingToast });
          }
        } catch (error) {
          console.error("Error reverse geocoding:", error);
          toast.error("Failed to get location details", { id: loadingToast });
        }
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
      
      // Animate to the new location with smooth globe rotation
      map.current.flyTo({
        center: [lng, lat],
        zoom: 8,
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
  }, [region, flower, coordinates, mapLoaded, getRegionCoordinates]);

  // Add NDVI abundance overlay when available (this would come from the backend in a real implementation)
  useEffect(() => {
    if (map.current && mapLoaded && region) {
      // In a real implementation, you would fetch NDVI data from the backend
      // and add it as a GeoJSON or raster overlay
      
      // For demonstration, we'll create a sample polygon around the selected region
      if (map.current.getSource("ndvi-overlay")) {
        map.current.removeLayer("ndvi-overlay");
        map.current.removeSource("ndvi-overlay");
      }

      // Use provided coordinates or fall back to lookup
      const [lng, lat] = coordinates || getRegionCoordinates(region);
      
      // Create a sample polygon for demonstration
      const ndviData: GeoJSON.Feature<GeoJSON.Polygon> = {
        type: "Feature",
        properties: {
          abundance: 0.7 // Example abundance value
        },
        geometry: {
          type: "Polygon",
          coordinates: [[
            [lng - 3, lat - 3],
            [lng + 3, lat - 3], 
            [lng + 3, lat + 3],
            [lng - 3, lat + 3],
            [lng - 3, lat - 3]
          ]]
        }
      };

      // Remove existing NDVI layer if it exists
      if (map.current.getLayer("ndvi-overlay")) {
        map.current.removeLayer("ndvi-overlay");
      }
      if (map.current.getSource("ndvi-overlay")) {
        map.current.removeSource("ndvi-overlay");
      }

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
          "fill-opacity": [
            "interpolate",
            ["linear"],
            ["zoom"],
            0, 0.2,
            5, 0.5
          ]
        }
      });
    }
  }, [region, coordinates, mapLoaded, getRegionCoordinates]);

  // Function to reset map to initial globe view
  const resetView = () => {
    if (map.current) {
      map.current.flyTo({
        center: [0, 20],
        zoom: 1.2,
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
        className="absolute inset-0 w-full h-full"
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

      {/* Map Controls */}
      <div className="absolute bottom-6 right-6 flex flex-col gap-2 z-20">
        <button
          onClick={resetView}
          className="p-2 bg-card/95 backdrop-blur-sm hover:bg-card rounded-md border border-border shadow-soft z-20"
          aria-label="Reset view"
        >
          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
            <path d="M3 12a9 9 0 1 0 9-9 9.75 9.75 0 0 0-6.74 2.74L3 8"/>
            <path d="M3 3v5h5"/>
          </svg>
        </button>
      </div>

      {/* Legend */}
      <div className="absolute bottom-6 left-6 bg-card/95 backdrop-blur-sm rounded-lg p-4 border border-border shadow-soft z-20">
        <h4 className="text-sm font-semibold text-foreground mb-3">NDVI Abundance</h4>
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
      </div>
    </div>
  );
};

export default MapView;
