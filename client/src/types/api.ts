// Type definitions for BloomWatch API

export interface FlowerInfo {
  common_name: string;
  scientific_name: string;
}

export interface WebResearchSource {
  title: string;
  snippet: string;
  link: string;
  source: string;
}

export interface WebResearch {
  summary: string;
  source_count: number;
  sources: WebResearchSource[];
}

export interface Metadata {
  timestamp: string;
  processing_time_ms: number;
  llm_used: boolean;
  search_available: boolean;
  error?: string;
  fallback?: boolean;
}

export interface BloomExplanation {
  region: string;
  flower: FlowerInfo;
  abundance_level: "high" | "medium" | "low" | "none";
  season: string;
  climate: string;
  known_bloom_period: string;
  notes: string;
  explanation: string;
  factors: string[];
  web_research: WebResearch;
  metadata: Metadata;
  timestamp: string;
  processing_time_ms: number;
}

export interface ExplanationRequest {
  region: string;
  flower: string;
  coordinates?: [number, number];
  climate_data?: {
    temperature?: number;
    precipitation?: number;
    description?: string;
  };
  date?: string;
  use_mock_search?: boolean;
}

// Top Regions Types
export interface RegionInfo {
  name: string;
  country: string;
  full_name: string;
  mentions: number;
  confidence: number;
  coordinates: [number, number] | null;
  needs_geocoding: boolean;
  note?: string;
}

export interface TopRegionsRequest {
  country: string;
  flower: string;
  max_results?: number;
}

export interface TopRegionsResponse {
  country: string;
  flower: string;
  top_regions: RegionInfo[];
  total_sources: number;
  extraction_method: string;
  ai_summary?: string;
  error?: string;
}

// Abundance Data Types
export interface AbundancePoint {
  coordinates: [number, number]; // [longitude, latitude]
  value: number; // 0 to 1 representing abundance level
}

export interface AbundanceData {
  type: "FeatureCollection";
  features: Array<{
    type: "Feature";
    properties: {
      abundance: number; // 0 to 1 representing abundance level
    };
    geometry: {
      type: "Polygon" | "MultiPolygon";
      coordinates: any[]; // GeoJSON coordinates
    };
  }>;
}

// Classification Response Types
export interface ClassificationResponse {
  id: string;
  filename: string;
  timestamp: string;
  classification: string;
  confidence: number;
  location?: {
    lat: number;
    lng: number;
  } | null;
  similar_species: Array<{
    name: string;
    confidence: number;
  }>;
}

// Monthly Predictions Types
export interface MonthProbability {
  month: string;
  probability: number;
}

export interface MonthlyPredictionRequest {
  region: string;
  flower: string;
  climate_data?: {
    temperature?: number;
    precipitation?: number;
    description?: string;
  };
}

export interface MonthlyPredictionResponse {
  region: string;
  flower: string;
  month_probabilities: MonthProbability[];
  factors: { [key: string]: number };
  prediction_summary: string;
  top_months: string[];
}

// Chat Message Types
export interface ChatMessageRequest {
  message: string;
}

export interface ChatMessageResponse {
  response: string;
}
