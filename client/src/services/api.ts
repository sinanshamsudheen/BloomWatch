// API service for BloomWatch backend communication

import { BloomExplanation, ExplanationRequest } from "@/types/api";

const API_BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

export class BloomWatchAPI {
  /**
   * Fetch bloom explanation from the backend
   */
  static async getBloomExplanation(
    request: ExplanationRequest
  ): Promise<BloomExplanation> {
    try {
      console.log(`Calling API: ${API_BASE_URL}/api/explain`);
      console.log("Request payload:", request);

      const response = await fetch(`${API_BASE_URL}/api/explain`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Accept": "application/json",
        },
        body: JSON.stringify(request),
        mode: "cors",
      });

      console.log("Response status:", response.status);

      if (!response.ok) {
        const errorText = await response.text();
        console.error("API error response:", errorText);
        throw new Error(`API error: ${response.status} ${response.statusText} - ${errorText}`);
      }

      const data: BloomExplanation = await response.json();
      console.log("Parsed response data:", data);
      return data;
    } catch (error) {
      console.error("Failed to fetch bloom explanation:", error);
      if (error instanceof TypeError && error.message.includes("fetch")) {
        throw new Error("Cannot connect to backend server. Please ensure it's running on port 8000.");
      }
      throw error;
    }
  }

  /**
   * Fetch bloom explanation using GET endpoint (backward compatible)
   */
  static async getBloomExplanationSimple(
    region: string,
    flower: string
  ): Promise<BloomExplanation> {
    try {
      const params = new URLSearchParams({
        region,
        flower,
      });

      const response = await fetch(
        `${API_BASE_URL}/api/explanation?${params}`
      );

      if (!response.ok) {
        throw new Error(`API error: ${response.status} ${response.statusText}`);
      }

      const data: BloomExplanation = await response.json();
      return data;
    } catch (error) {
      console.error("Failed to fetch bloom explanation:", error);
      throw error;
    }
  }

  /**
   * Health check endpoint
   */
  static async healthCheck(): Promise<boolean> {
    try {
      const response = await fetch(`${API_BASE_URL}/health`, {
        method: "GET",
      });
      return response.ok;
    } catch (error) {
      console.error("Health check failed:", error);
      return false;
    }
  }
}

// Mock data fallback for development/testing
export const mockBloomExplanation: BloomExplanation = {
  region: "Sample Region",
  flower: {
    common_name: "Sample Flower",
    scientific_name: "Flowrus Samplus",
  },
  abundance_level: "high",
  season: "Spring 2025",
  climate: "Temperature: 18°C, Precipitation: 45mm",
  known_bloom_period: "March to May",
  notes: "Active bloom period, favorable conditions",
  explanation:
    "This is a mock explanation. Connect to the backend to see real AI-generated insights.",
  factors: [
    "Temperature and seasonal variations",
    "Precipitation and water availability",
    "Day length (photoperiod)",
    "Soil composition and nutrients",
    "Pollinator populations",
    "Regional climate patterns",
  ],
  web_research: {
    summary: "Mock web research summary",
    source_count: 0,
    sources: [],
  },
  metadata: {
    timestamp: new Date().toISOString(),
    processing_time_ms: 0,
    llm_used: false,
    search_available: false,
  },
  timestamp: new Date().toISOString(),
  processing_time_ms: 0,
};
