import { useState } from "react";
import SearchBar from "@/components/SearchBar";
import InfoPanel from "@/components/InfoPanel";
import ImageUpload from "@/components/ImageUpload";
import MapView from "@/components/MapView";
import { Leaf, Loader2 } from "lucide-react";
import { BloomWatchAPI } from "@/services/api";
import { BloomExplanation, RegionInfo } from "@/types/api";
import { useToast } from "@/hooks/use-toast";

const Index = () => {
  const [selectedRegion, setSelectedRegion] = useState<string>();
  const [selectedFlower, setSelectedFlower] = useState<string>();
  const [selectedCoordinates, setSelectedCoordinates] = useState<[number, number]>();
  const [showResults, setShowResults] = useState(false);
  const [bloomData, setBloomData] = useState<BloomExplanation | null>(null);
  const [topRegions, setTopRegions] = useState<RegionInfo[]>([]);
  const [loading, setLoading] = useState(false);
  const { toast } = useToast();

  const handleSearch = async (region: string, flower: string, coordinates?: [number, number]) => {
    setSelectedRegion(region);
    setSelectedFlower(flower);
    setSelectedCoordinates(coordinates);
    setLoading(true);
    setShowResults(true);

    try {
      console.log("Fetching bloom data for:", { region, flower, coordinates });
      
      // Fetch real data from backend
      const data = await BloomWatchAPI.getBloomExplanation({
        region,
        flower,
        coordinates,
        use_mock_search: true, // Set to true for faster testing
      });

      console.log("Received bloom data:", data);
      setBloomData(data);
      
      // Extract country from region (simple approach - split by comma)
      const country = region.includes(',') ? region.split(',').pop()?.trim() : region;
      
      // Fetch top regions for the selected flower in the country
      if (country && flower) {
        try {
          console.log(`Fetching top regions for ${flower} in ${country}`);
          const regionsData = await BloomWatchAPI.getTopRegions({
            country,
            flower,
            max_results: 10
          });
          console.log("Top regions data:", regionsData);
          setTopRegions(regionsData.top_regions);
        } catch (regionsError) {
          console.error("Failed to fetch top regions:", regionsError);
          // Don't show error toast, just log it
        }
      }
      
      toast({
        title: "✅ Bloom data loaded",
        description: `Found information about ${data.flower.common_name} in ${region}`,
      });
    } catch (error) {
      console.error("Failed to fetch bloom data:", error);
      toast({
        title: "❌ Error loading data",
        description: error instanceof Error ? error.message : "Could not connect to the server.",
        variant: "destructive",
      });
      setBloomData(null);
    } finally {
      setLoading(false);
    }
  };

  const handleLocationSelect = (location: string, coordinates: [number, number]) => {
    setSelectedRegion(location);
    setSelectedCoordinates(coordinates);
    setShowResults(true);
  };

  const handleImageUpload = (file: File) => {
    console.log("Image uploaded:", file.name);
    // Simulate classification
    setTimeout(() => {
      setSelectedRegion("Amazon Rainforest");
      setSelectedFlower("Passion Flower");
      setShowResults(true);
    }, 2000);
  };

  return (
    <div className="min-h-screen bg-background flex flex-col">
      {/* Header */}
      <header className="relative z-50 bg-gradient-nature text-primary-foreground py-3 px-4 shadow-elevated">
        <div className="flex items-center gap-2">
          <div className="p-1.5 bg-primary-foreground/20 rounded-lg">
            <Leaf className="h-5 w-5" />
          </div>
          <div>
            <h1 className="text-xl font-bold">BloomWatch</h1>
            <p className="text-xs text-primary-foreground/80">
              Global Flower Bloom Exploration Platform
            </p>
          </div>
        </div>
      </header>

      {/* Search Bar */}
      <SearchBar onSearch={handleSearch} initialRegion={selectedRegion} />

      {/* Main Content */}
      <div className="flex-1 flex flex-col lg:flex-row relative overflow-hidden">
        {/* Left Panel - Information */}
        <aside className="w-full lg:w-[35%] bg-muted/30 p-4 overflow-y-auto space-y-3 max-h-[calc(100vh-80px)]">
          {!showResults ? (
            <>
              <InfoPanel
                title="Welcome to BloomWatch"
                content="Explore global flower blooms using real-time satellite data. Search for any region to see NDVI-based abundance maps, or upload a flower image to identify species and discover their most abundant locations."
                stats={[
                  { label: "Global Coverage", value: "195 countries" },
                  { label: "Flower Species", value: "12,000+" },
                  { label: "Data Points", value: "50M+" },
                ]}
              />
              
              <InfoPanel
                title="How It Works"
                content={`1. Search for a region or upload a flower image
2. View real-time NDVI abundance data
3. Explore bloom patterns and ecological insights
4. Discover optimal viewing seasons`}
              />
            </>
          ) : loading ? (
            <InfoPanel
              title="Loading bloom data..."
              content={
                <div className="flex items-center justify-center gap-2 py-4">
                  <Loader2 className="h-5 w-5 animate-spin text-primary" />
                  <span className="text-sm">AI agents are analyzing bloom patterns...</span>
                </div>
              }
            />
          ) : bloomData ? (
            <>
              <InfoPanel
                title={`${bloomData.flower.common_name} in ${bloomData.region}`}
                content={bloomData.notes}
                stats={[
                  { label: "Abundance", value: bloomData.abundance_level },
                  { label: "Season", value: bloomData.season },
                  { label: "Bloom Period", value: bloomData.known_bloom_period },
                ]}
              />

              <InfoPanel
                title="AI-Generated Ecological Explanation"
                content={bloomData.explanation}
              />

              {bloomData.web_research.source_count > 0 && (
                <InfoPanel
                  title="Recent Research & News"
                  content={bloomData.web_research.summary}
                  stats={[
                    { label: "Sources Found", value: bloomData.web_research.source_count.toString() },
                    { label: "Processing Time", value: `${bloomData.processing_time_ms.toFixed(0)}ms` },
                    { label: "AI Powered", value: bloomData.metadata.llm_used ? "Yes" : "No" },
                  ]}
                />
              )}

              <InfoPanel
                title="Additional Details"
                content={`Scientific Name: ${bloomData.flower.scientific_name}
Bloom Period: ${bloomData.known_bloom_period}
Climate: ${bloomData.climate}`}
              />
            </>
          ) : (
            <>
              <InfoPanel
                title={selectedFlower ? `${selectedFlower} in ${selectedRegion}` : `Exploring ${selectedRegion}`}
                content="Unable to load real-time data. Please ensure the backend server is running."
                stats={[
                  { label: "Status", value: "Offline" },
                  { label: "Server", value: "Not Connected" },
                  { label: "Mode", value: "Placeholder" },
                ]}
              />
            </>
          )}

          <ImageUpload onUpload={handleImageUpload} />
        </aside>

        {/* Right Panel - Map */}
        <main className="flex-1 relative">
          <MapView 
            region={selectedRegion} 
            flower={selectedFlower}
            coordinates={selectedCoordinates}
            topRegions={topRegions}
            onLocationSelect={handleLocationSelect}
          />
        </main>
      </div>
    </div>
  );
};

export default Index;