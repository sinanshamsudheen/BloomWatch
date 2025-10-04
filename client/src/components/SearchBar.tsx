import { Search, Flower, MapPin, Loader2 } from "lucide-react";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { useState, useEffect, useRef } from "react";
import { toast } from "sonner";

interface SearchBarProps {
  onSearch: (region: string, flower: string, coordinates?: [number, number]) => void;
  initialRegion?: string;
}

interface LocationSuggestion {
  display_name: string;
  lat: string;
  lon: string;
  type: string;
  name: string;
}

const SearchBar = ({ onSearch, initialRegion }: SearchBarProps) => {
  const [region, setRegion] = useState("");
  const [flower, setFlower] = useState("");
  const [suggestions, setSuggestions] = useState<LocationSuggestion[]>([]);
  const [showSuggestions, setShowSuggestions] = useState(false);
  const [loading, setLoading] = useState(false);
  const [selectedIndex, setSelectedIndex] = useState(-1);
  const suggestionsRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  // Update region when initialRegion changes (from map click)
  useEffect(() => {
    if (initialRegion) {
      setRegion(initialRegion);
    }
  }, [initialRegion]);

  // Close suggestions when clicking outside
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (suggestionsRef.current && !suggestionsRef.current.contains(event.target as Node) &&
          inputRef.current && !inputRef.current.contains(event.target as Node)) {
        setShowSuggestions(false);
      }
    };

    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  // Fetch location suggestions from Nominatim API
  useEffect(() => {
    const fetchSuggestions = async () => {
      if (region.trim().length < 3) {
        setSuggestions([]);
        return;
      }

      setLoading(true);
      try {
        const response = await fetch(
          `https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(region)}&limit=5&addressdetails=1`,
          {
            headers: {
              'User-Agent': 'BloomWatch/1.0' // Nominatim requires a User-Agent
            }
          }
        );

        if (response.ok) {
          const data = await response.json();
          setSuggestions(data);
          setShowSuggestions(data.length > 0);
        }
      } catch (error) {
        console.error("Error fetching location suggestions:", error);
        toast.error("Failed to fetch location suggestions");
      } finally {
        setLoading(false);
      }
    };

    const debounceTimer = setTimeout(fetchSuggestions, 300);
    return () => clearTimeout(debounceTimer);
  }, [region]);

  const handleSearch = () => {
    if (region.trim()) {
      onSearch(region, flower);
      setShowSuggestions(false);
    }
  };

  const handleSuggestionClick = (suggestion: LocationSuggestion) => {
    setRegion(suggestion.display_name);
    setSuggestions([]);
    setShowSuggestions(false);
    const coordinates: [number, number] = [parseFloat(suggestion.lon), parseFloat(suggestion.lat)];
    onSearch(suggestion.display_name, flower, coordinates);
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === "Enter") {
      if (selectedIndex >= 0 && suggestions[selectedIndex]) {
        handleSuggestionClick(suggestions[selectedIndex]);
      } else {
        handleSearch();
      }
    } else if (e.key === "ArrowDown") {
      e.preventDefault();
      setSelectedIndex(prev => 
        prev < suggestions.length - 1 ? prev + 1 : prev
      );
    } else if (e.key === "ArrowUp") {
      e.preventDefault();
      setSelectedIndex(prev => prev > 0 ? prev - 1 : -1);
    } else if (e.key === "Escape") {
      setShowSuggestions(false);
      setSelectedIndex(-1);
    }
  };

  return (
    <div className="absolute top-4 left-1/2 -translate-x-1/2 z-50 w-full max-w-2xl px-4">
      <div className="bg-card/95 backdrop-blur-lg rounded-xl shadow-elevated border border-border p-3">
        <div className="flex flex-col md:flex-row gap-2">
          <div className="flex-1 relative">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground z-10" />
            {loading && (
              <Loader2 className="absolute right-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground animate-spin z-10" />
            )}
            <Input
              ref={inputRef}
              placeholder="Enter region or location..."
              value={region}
              onChange={(e) => setRegion(e.target.value)}
              onKeyDown={handleKeyPress}
              onFocus={() => suggestions.length > 0 && setShowSuggestions(true)}
              className="pl-10 pr-10 bg-background border-border focus:ring-primary"
              autoComplete="off"
            />
            
            {/* Autocomplete Dropdown */}
            {showSuggestions && suggestions.length > 0 && (
              <div 
                ref={suggestionsRef}
                className="absolute top-full mt-2 w-full bg-card border border-border rounded-lg shadow-elevated max-h-64 overflow-y-auto z-50"
              >
                {suggestions.map((suggestion, index) => (
                  <button
                    key={`${suggestion.lat}-${suggestion.lon}`}
                    onClick={() => handleSuggestionClick(suggestion)}
                    className={`w-full text-left px-4 py-3 hover:bg-accent transition-colors flex items-start gap-3 border-b border-border last:border-b-0 ${
                      index === selectedIndex ? 'bg-accent' : ''
                    }`}
                  >
                    <MapPin className="h-4 w-4 text-primary mt-0.5 flex-shrink-0" />
                    <div className="flex-1 min-w-0">
                      <p className="text-base font-medium text-foreground truncate">
                        {suggestion.name || suggestion.display_name.split(',')[0]}
                      </p>
                      <p className="text-sm text-muted-foreground truncate">
                        {suggestion.display_name}
                      </p>
                      <p className="text-sm text-muted-foreground mt-0.5">
                        {suggestion.type && (
                          <span className="inline-block px-1.5 py-0.5 bg-primary/10 text-primary rounded text-xs uppercase">
                            {suggestion.type}
                          </span>
                        )}
                      </p>
                    </div>
                  </button>
                ))}
              </div>
            )}
          </div>
          
          <div className="flex-1 relative">
            <Flower className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
            <Input
              placeholder="Flower name (optional)..."
              value={flower}
              onChange={(e) => setFlower(e.target.value)}
              onKeyDown={handleKeyPress}
              className="pl-10 bg-background border-border focus:ring-primary"
            />
          </div>
          
          <Button
            onClick={handleSearch}
            className="bg-gradient-nature hover:opacity-90 transition-opacity"
            disabled={!region.trim()}
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
