import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Leaf, TrendingUp, MapPin, Calendar, BarChart3 } from "lucide-react";
import { cn } from "@/lib/utils";

const Predictions = () => {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(true);
  
  // Mock data for Alaska predictions
  const predictionsData = {
    region: "Alaska",
    flower: "Alpine Forget-Me-Not",
    predictions: [
      { month: "Jan", prediction: 0.1 },
      { month: "Feb", prediction: 0.2 },
      { month: "Mar", prediction: 0.3 },
      { month: "Apr", prediction: 0.6 },
      { month: "May", prediction: 0.8 },
      { month: "Jun", prediction: 0.9 },
      { month: "Jul", prediction: 0.95 },
      { month: "Aug", prediction: 0.9 },
      { month: "Sep", prediction: 0.7 },
      { month: "Oct", prediction: 0.4 },
      { month: "Nov", prediction: 0.2 },
      { month: "Dec", prediction: 0.1 }
    ],
    peakMonths: ["June", "July"],
    factors: [
      "Temperature and seasonal variations",
      "Day length (photoperiod)",
      "Precipitation patterns",
      "Soil temperature"
    ]
  };

  useEffect(() => {
    // Simulate loading data
    const timer = setTimeout(() => {
      setLoading(false);
    }, 1500);
    
    return () => clearTimeout(timer);
  }, []);

  if (loading) {
    return (
      <div className="min-h-screen bg-background flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary mx-auto"></div>
          <p className="mt-4 text-lg text-muted-foreground">Loading predictions...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="relative z-50 bg-gradient-nature text-primary-foreground py-4 px-4 shadow-elevated">
        <div className="flex items-center gap-2">
          <div className="p-1.5 bg-primary-foreground/20 rounded-lg">
            <BarChart3 className="h-5 w-5" />
          </div>
          <div>
            <h1 className="text-xl font-bold">BloomWatch Predictions</h1>
            <p className="text-xs text-primary-foreground/80">
              Forecast models for flower blooms
            </p>
          </div>
        </div>
      </header>

      <div className="container mx-auto px-4 py-6 max-w-6xl">
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-2xl font-bold text-foreground">Bloom Predictions for {predictionsData.region}</h2>
          <Button 
            onClick={() => navigate('/')}
            variant="outline"
            className="flex items-center gap-2"
          >
            <MapPin className="h-4 w-4" />
            Back to Map
          </Button>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Main Prediction Chart */}
          <div className="lg:col-span-2">
            <Card className="p-6 bg-card/95 backdrop-blur-sm border-border shadow-soft">
              <h3 className="text-lg font-semibold mb-4 flex items-center gap-2">
                <TrendingUp className="h-5 w-5 text-primary" />
                Monthly Bloom Probability
              </h3>
              
              <div className="space-y-4">
                {predictionsData.predictions.map((item, index) => (
                  <div key={index} className="flex items-center">
                    <div className="w-12 text-sm font-medium text-muted-foreground">{item.month}</div>
                    <div className="flex-1 ml-4">
                      <div 
                        className="h-8 bg-gradient-to-r from-green-500 to-blue-500 rounded-full flex items-center justify-end pr-2 text-white text-xs font-bold"
                        style={{ width: `${item.prediction * 100}%` }}
                      >
                        {Math.round(item.prediction * 100)}%
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </Card>
          </div>

          {/* Info Panel */}
          <div className="space-y-6">
            <Card className="p-4 bg-card/95 backdrop-blur-sm border-border shadow-soft">
              <div className="flex items-center gap-2 mb-3">
                <div className="p-1.5 rounded-lg bg-gradient-nature">
                  <Leaf className="h-4 w-4 text-primary-foreground" />
                </div>
                <h3 className="text-lg font-semibold text-foreground">Prediction Summary</h3>
              </div>
              
              <div className="space-y-3">
                <div>
                  <p className="text-sm text-muted-foreground">Predicted Flower</p>
                  <p className="font-medium">{predictionsData.flower}</p>
                </div>
                
                <div>
                  <p className="text-sm text-muted-foreground">Peak Bloom Months</p>
                  <p className="font-medium">{predictionsData.peakMonths.join(", ")}</p>
                </div>
                
                <div>
                  <p className="text-sm text-muted-foreground">Current Season</p>
                  <p className="font-medium">Summer</p>
                </div>
              </div>
            </Card>

            <Card className="p-4 bg-card/95 backdrop-blur-sm border-border shadow-soft">
              <div className="flex items-center gap-2 mb-3">
                <div className="p-1.5 rounded-lg bg-gradient-nature">
                  <Calendar className="h-4 w-4 text-primary-foreground" />
                </div>
                <h3 className="text-lg font-semibold text-foreground">Bloom Calendar</h3>
              </div>
              
              <div className="space-y-2">
                {predictionsData.peakMonths.map((month, index) => (
                  <div key={index} className="p-2 rounded-lg bg-primary/10 border border-primary/20">
                    <p className="font-medium text-primary">{month}</p>
                    <p className="text-xs text-muted-foreground">Peak bloom potential</p>
                  </div>
                ))}
              </div>
            </Card>

            <Card className="p-4 bg-card/95 backdrop-blur-sm border-border shadow-soft">
              <div className="flex items-center gap-2 mb-3">
                <div className="p-1.5 rounded-lg bg-gradient-nature">
                  <TrendingUp className="h-4 w-4 text-primary-foreground" />
                </div>
                <h3 className="text-lg font-semibold text-foreground">Influencing Factors</h3>
              </div>
              
              <ul className="space-y-2">
                {predictionsData.factors.map((factor, index) => (
                  <li key={index} className="flex items-start">
                    <div className="mt-1 mr-2">
                      <div className="w-2 h-2 rounded-full bg-primary"></div>
                    </div>
                    <span className="text-sm">{factor}</span>
                  </li>
                ))}
              </ul>
            </Card>
          </div>
        </div>

        <div className="mt-8 text-center text-sm text-muted-foreground">
          <p>These predictions are based on historical climate data and phenological models.</p>
          <p className="mt-1">Actual bloom times may vary based on local conditions.</p>
        </div>
      </div>
    </div>
  );
};

export default Predictions;