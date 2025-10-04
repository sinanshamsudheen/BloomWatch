import { useState } from "react";
import SearchBar from "@/components/SearchBar";
import InfoPanel from "@/components/InfoPanel";
import ImageUpload from "@/components/ImageUpload";
import MapView from "@/components/MapView";
import { Leaf } from "lucide-react";

const Index = () => {
  const [selectedRegion, setSelectedRegion] = useState<string>();
  const [selectedFlower, setSelectedFlower] = useState<string>();
  const [showResults, setShowResults] = useState(false);

  const handleSearch = (region: string, flower: string) => {
    setSelectedRegion(region);
    setSelectedFlower(flower);
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
      <header className="relative z-50 bg-gradient-nature text-primary-foreground py-4 px-6 shadow-elevated">
        <div className="flex items-center gap-3">
          <div className="p-2 bg-primary-foreground/20 rounded-lg">
            <Leaf className="h-6 w-6" />
          </div>
          <div>
            <h1 className="text-2xl font-bold">BloomWatch</h1>
            <p className="text-sm text-primary-foreground/80">
              Global Flower Bloom Exploration Platform
            </p>
          </div>
        </div>
      </header>

      {/* Search Bar */}
      <SearchBar onSearch={handleSearch} />

      {/* Main Content */}
      <div className="flex-1 flex flex-col lg:flex-row relative">
        {/* Left Panel - Information */}
        <aside className="w-full lg:w-[40%] bg-muted/30 p-6 overflow-y-auto space-y-6">
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
                content="1. Search for a region or upload a flower image\n2. View real-time NDVI abundance data\n3. Explore bloom patterns and ecological insights\n4. Discover optimal viewing seasons"
              />
            </>
          ) : (
            <>
              <InfoPanel
                title={selectedFlower ? `${selectedFlower} in ${selectedRegion}` : `Exploring ${selectedRegion}`}
                content="Based on recent satellite imagery and NDVI analysis, this region shows high vegetation density with optimal bloom conditions. The data suggests peak flowering season is approaching."
                stats={[
                  { label: "NDVI Score", value: "0.78" },
                  { label: "Bloom Coverage", value: "67%" },
                  { label: "Best Season", value: "Spring" },
                ]}
              />

              <InfoPanel
                title="Ecological Context"
                content={`${selectedRegion} hosts diverse flora with ${selectedFlower ? `${selectedFlower} being particularly abundant` : "rich biodiversity"}. The region's climate and soil conditions create ideal growing environments. Recent weather patterns indicate favorable conditions for continued bloom development.`}
              />
            </>
          )}

          <ImageUpload onUpload={handleImageUpload} />
        </aside>

        {/* Right Panel - Map */}
        <main className="flex-1 relative">
          <MapView region={selectedRegion} flower={selectedFlower} />
        </main>
      </div>
    </div>
  );
};

export default Index;
