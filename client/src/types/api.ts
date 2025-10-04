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
  ndvi_score: number;
  abundance_level: "high" | "medium" | "low";
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
  ndvi_score?: number;
  coordinates?: [number, number];
  climate_data?: {
    temperature?: number;
    precipitation?: number;
    description?: string;
  };
  date?: string;
  use_mock_search?: boolean;
}
