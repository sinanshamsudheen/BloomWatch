import { useEffect, useRef, useState } from "react";
import { Loader2, ZoomIn, ZoomOut, Maximize2 } from "lucide-react";
import { Button } from "@/components/ui/button";
import { toast } from "sonner";

interface MapViewProps {
  region?: string;
  flower?: string;
}

const MapView = ({ region, flower }: MapViewProps) => {
  const mapContainer = useRef<HTMLDivElement>(null);
  const [loading, setLoading] = useState(false);
  const [zoom, setZoom] = useState(1.5);
  const [rotation, setRotation] = useState(0);

  useEffect(() => {
    if (region) {
      setLoading(true);
      // Simulate loading
      setTimeout(() => {
        setLoading(false);
        setZoom(5);
        toast.success(`Zoomed to ${region}${flower ? ` for ${flower}` : ""}`);
      }, 1500);
    }
  }, [region, flower]);

  const handleZoomIn = () => setZoom(Math.min(zoom + 0.5, 10));
  const handleZoomOut = () => setZoom(Math.max(zoom - 0.5, 1));
  const handleReset = () => {
    setZoom(1.5);
    setRotation(0);
  };

  return (
    <div className="relative w-full h-full bg-gradient-to-b from-info/20 to-background">
      {/* Map Container */}
      <div
        ref={mapContainer}
        className="absolute inset-0 flex items-center justify-center overflow-hidden"
      >
        {/* Globe Visualization Placeholder */}
        <div
          className="relative rounded-full bg-gradient-to-br from-info to-primary shadow-glow transition-all duration-1000 ease-smooth"
          style={{
            width: `${zoom * 200}px`,
            height: `${zoom * 200}px`,
            transform: `rotate(${rotation}deg)`,
          }}
        >
          {/* Latitude/Longitude Grid */}
          <div className="absolute inset-0 rounded-full border-2 border-primary-foreground/20" />
          <div className="absolute inset-0 rounded-full border border-primary-foreground/10"
               style={{ clipPath: "inset(25% 0 25% 0)" }} />
          <div className="absolute inset-0 rounded-full border border-primary-foreground/10"
               style={{ clipPath: "inset(0 25% 0 25%)" }} />
          
          {/* Simulated Land Masses */}
          <div className="absolute top-1/4 left-1/3 w-1/4 h-1/6 bg-primary-glow/40 rounded-full blur-sm" />
          <div className="absolute top-1/2 left-1/4 w-1/3 h-1/5 bg-primary-glow/40 rounded-full blur-sm" />
          <div className="absolute bottom-1/3 right-1/4 w-1/5 h-1/6 bg-primary-glow/40 rounded-full blur-sm" />

          {region && (
            <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2">
              <div className="w-8 h-8 bg-accent rounded-full animate-pulse-glow" />
              <div className="absolute top-full mt-2 left-1/2 -translate-x-1/2 whitespace-nowrap bg-card px-3 py-1 rounded-full text-xs font-medium text-foreground border border-border shadow-elevated">
                {region}
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Loading Overlay */}
      {loading && (
        <div className="absolute inset-0 bg-background/80 backdrop-blur-sm flex items-center justify-center z-10">
          <div className="text-center">
            <Loader2 className="h-12 w-12 animate-spin text-primary mx-auto mb-4" />
            <p className="text-foreground font-medium">Loading region data...</p>
            <p className="text-muted-foreground text-sm mt-1">Fetching NDVI abundance</p>
          </div>
        </div>
      )}

      {/* Map Controls */}
      <div className="absolute bottom-6 right-6 flex flex-col gap-2 z-20">
        <Button
          size="icon"
          variant="outline"
          className="bg-card/95 backdrop-blur-sm hover:bg-card"
          onClick={handleZoomIn}
        >
          <ZoomIn className="h-4 w-4" />
        </Button>
        <Button
          size="icon"
          variant="outline"
          className="bg-card/95 backdrop-blur-sm hover:bg-card"
          onClick={handleZoomOut}
        >
          <ZoomOut className="h-4 w-4" />
        </Button>
        <Button
          size="icon"
          variant="outline"
          className="bg-card/95 backdrop-blur-sm hover:bg-card"
          onClick={handleReset}
        >
          <Maximize2 className="h-4 w-4" />
        </Button>
      </div>

      {/* Legend */}
      <div className="absolute bottom-6 left-6 bg-card/95 backdrop-blur-sm rounded-lg p-4 border border-border shadow-soft z-20">
        <h4 className="text-sm font-semibold text-foreground mb-3">NDVI Abundance</h4>
        <div className="space-y-2">
          <div className="flex items-center gap-2">
            <div className="w-4 h-4 rounded bg-destructive" />
            <span className="text-xs text-muted-foreground">Low (0-0.3)</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-4 h-4 rounded bg-accent" />
            <span className="text-xs text-muted-foreground">Medium (0.3-0.6)</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-4 h-4 rounded bg-primary" />
            <span className="text-xs text-muted-foreground">High (0.6-1.0)</span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default MapView;
