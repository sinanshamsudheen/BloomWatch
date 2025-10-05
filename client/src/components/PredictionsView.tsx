import { useState, useEffect } from "react";
import ChatBot from "@/components/ChatBot";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell } from "recharts";
import { Calendar, Thermometer, Droplets, Sun, AlertCircle } from "lucide-react";
import { useToast } from "@/hooks/use-toast";
import { BloomWatchAPI } from "@/services/api";

interface MonthProbability {
  month: string;
  probability: number;
}

interface PredictionFactors {
  [key: string]: number;
}

interface MonthlyPredictionResponse {
  region: string;
  flower: string;
  month_probabilities: MonthProbability[];
  factors: PredictionFactors;
  prediction_summary: string;
  top_months: string[];
}

interface PredictionsViewProps {
  flower: string;
  region: string;
  onBack: () => void;
}

const PredictionsView = ({ flower, region, onBack }: PredictionsViewProps) => {
  const [predictions, setPredictions] = useState<MonthlyPredictionResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const { toast } = useToast();

  useEffect(() => {
    const fetchPredictions = async () => {
      setLoading(true);
      try {
        // Call the new API endpoint for monthly predictions
        const response = await BloomWatchAPI.getMonthlyPredictions({
          region,
          flower
        });
        setPredictions(response);
      } catch (error) {
        console.error("Failed to fetch monthly predictions:", error);
        toast({
          title: "❌ Error loading predictions",
          description: error instanceof Error ? error.message : "Could not connect to the server.",
          variant: "destructive",
        });
      } finally {
        setLoading(false);
      }
    };

    if (flower && region) {
      fetchPredictions();
    }
  }, [flower, region, toast]);

  // Get top 4 months from the API response
  const topFourMonths = predictions?.top_months?.slice(0, 4) || [];

  const factorIcons = {
    "Temperature": <Thermometer className="h-4 w-4" />,
    "Precipitation": <Droplets className="h-4 w-4" />,
    "Day Length": <Sun className="h-4 w-4" />,
    "Soil Moisture": <Droplets className="h-4 w-4" />,
    "Previous Blooms": <Calendar className="h-4 w-4" />,
  };

  return (
    <div className="flex flex-col h-full">
      <div className="flex justify-between items-center mb-4">
        <h2 className="text-2xl font-bold">Bloom Predictions</h2>
        <Button onClick={onBack} variant="outline">
          Back to Map
        </Button>
      </div>

      {loading ? (
        <div className="flex items-center justify-center h-full">
          <div className="flex flex-col items-center gap-2">
            <div className="animate-spin rounded-full h-10 w-10 border-b-2 border-primary"></div>
            <p>Generating bloom predictions...</p>
          </div>
        </div>
      ) : !predictions ? (
        <div className="flex flex-col items-center justify-center h-full text-center p-4">
          <AlertCircle className="h-12 w-12 text-muted-foreground mb-2" />
          <h3 className="text-lg font-medium mb-1">No predictions available</h3>
          <p className="text-muted-foreground mb-4">
            Unable to generate bloom predictions for {flower} in {region}
          </p>
          <Button onClick={onBack}>Back to Search</Button>
        </div>
      ) : (
        <div className="space-y-4 overflow-y-auto flex-1">
          <Card>
            <CardHeader>
              <CardTitle>
                Bloom Probability for {predictions.flower} in {predictions.region}
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="h-72">
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart
                    data={predictions.month_probabilities}
                    margin={{ top: 20, right: 30, left: 20, bottom: 60 }}
                  >
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis 
                      dataKey="month" 
                      angle={-45} 
                      textAnchor="end" 
                      height={60}
                      tick={{ fontSize: 12 }}
                    />
                    <YAxis 
                      domain={[0, 1]} 
                      tickCount={6}
                      tickFormatter={(value) => `${value * 100}%`}
                    />
                    <Tooltip 
                      formatter={(value) => [`${(value as number * 100).toFixed(1)}%`, "Bloom Probability"]}
                      labelFormatter={(label) => `Month: ${label}`}
                    />
                    <Bar dataKey="probability" name="Bloom Probability">
                      {predictions.month_probabilities.map((entry, index) => (
                        <Cell 
                          key={`cell-${index}`} 
                          fill={entry.probability > 0.7 ? "#10b981" : 
                                entry.probability > 0.4 ? "#f59e0b" : 
                                entry.probability > 0.1 ? "#ef4444" : "#9ca3af"} 
                        />
                      ))}
                    </Bar>
                  </BarChart>
                </ResponsiveContainer>
              </div>
              <p className="text-sm text-muted-foreground mt-2">
                Note: Bloom probability is determined using NDVI data to measure flower abundance
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Top Bloom Months</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                {topFourMonths.map((month, index) => {
                  // Find the probability for this month from the month_probabilities array
                  const monthData = predictions?.month_probabilities?.find(m => m.month === month);
                  return (
                    <div 
                      key={index} 
                      className="border rounded-lg p-4 text-center bg-muted/50"
                    >
                      <div className="text-2xl font-bold text-primary">
                        {monthData ? `${Math.round(monthData.probability * 100)}%` : 'N/A'}
                      </div>
                      <div className="text-lg font-medium">{month}</div>
                      <div className="text-sm text-muted-foreground">
                        {index === 0 ? "Peak Bloom" : 
                         index === 1 ? "High Bloom" : 
                         index === 2 ? "Moderate Bloom" : "Good Bloom"}
                      </div>
                    </div>
                  )
                })}
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Prediction Factors</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                {Object.entries(predictions.factors).map(([factor, confidence]) => (
                  <div key={factor} className="flex items-center justify-between">
                    <div className="flex items-center gap-2">
                      {factorIcons[factor as keyof typeof factorIcons] || <div className="w-4 h-4" />}
                      <span className="font-medium">{factor}</span>
                    </div>
                    <div className="flex items-center gap-2">
                      <div className="w-24 bg-muted rounded-full h-2.5">
                        <div 
                          className="bg-primary h-2.5 rounded-full" 
                          style={{ width: `${confidence * 100}%` }}
                        ></div>
                      </div>
                      <span className="text-sm text-muted-foreground">
                        {(confidence * 100).toFixed(0)}%
                      </span>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Prediction Summary</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-muted-foreground">{predictions.prediction_summary}</p>
            </CardContent>
          </Card>
        </div>
      )}
    </div>
  );
};

export default PredictionsView;