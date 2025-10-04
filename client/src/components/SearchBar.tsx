import { Search, Flower } from "lucide-react";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { useState } from "react";

interface SearchBarProps {
  onSearch: (region: string, flower: string) => void;
}

const SearchBar = ({ onSearch }: SearchBarProps) => {
  const [region, setRegion] = useState("");
  const [flower, setFlower] = useState("");

  const handleSearch = () => {
    if (region.trim()) {
      onSearch(region, flower);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === "Enter") {
      handleSearch();
    }
  };

  return (
    <div className="absolute top-6 left-1/2 -translate-x-1/2 z-50 w-full max-w-2xl px-4">
      <div className="bg-card/95 backdrop-blur-lg rounded-xl shadow-elevated border border-border p-4">
        <div className="flex flex-col md:flex-row gap-3">
          <div className="flex-1 relative">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
            <Input
              placeholder="Enter region or location..."
              value={region}
              onChange={(e) => setRegion(e.target.value)}
              onKeyPress={handleKeyPress}
              className="pl-10 bg-background border-border focus:ring-primary"
            />
          </div>
          <div className="flex-1 relative">
            <Flower className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
            <Input
              placeholder="Flower name (optional)..."
              value={flower}
              onChange={(e) => setFlower(e.target.value)}
              onKeyPress={handleKeyPress}
              className="pl-10 bg-background border-border focus:ring-primary"
            />
          </div>
          <Button
            onClick={handleSearch}
            className="bg-gradient-nature hover:opacity-90 transition-opacity"
          >
            <Search className="h-4 w-4 mr-2" />
            Explore
          </Button>
        </div>
      </div>
    </div>
  );
};

export default SearchBar;
