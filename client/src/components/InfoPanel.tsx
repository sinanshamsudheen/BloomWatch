import { Card } from "@/components/ui/card";
import { Leaf, TrendingUp, MapPin, Info } from "lucide-react";
import { cn } from "@/lib/utils";

interface InfoPanelProps {
  title?: string;
  content?: string;
  stats?: { label: string; value: string }[];
  className?: string;
}

const InfoPanel = ({ title, content, stats, className }: InfoPanelProps) => {
  return (
    <Card className={cn("p-6 bg-card/95 backdrop-blur-sm border-border shadow-soft animate-fade-in", className)}>
      {title && (
        <div className="flex items-center gap-2 mb-4">
          <div className="p-2 rounded-lg bg-gradient-nature">
            <Leaf className="h-5 w-5 text-primary-foreground" />
          </div>
          <h3 className="text-lg font-semibold text-foreground">{title}</h3>
        </div>
      )}
      
      {content && (
        <div className="mb-4 text-sm text-muted-foreground leading-relaxed">
          {content}
        </div>
      )}

      {stats && stats.length > 0 && (
        <div className="space-y-3">
          {stats.map((stat, index) => (
            <div key={index} className="flex items-center justify-between p-3 rounded-lg bg-muted/50">
              <span className="text-sm font-medium text-foreground flex items-center gap-2">
                {index === 0 && <TrendingUp className="h-4 w-4 text-primary" />}
                {index === 1 && <MapPin className="h-4 w-4 text-accent" />}
                {index === 2 && <Info className="h-4 w-4 text-info" />}
                {stat.label}
              </span>
              <span className="text-sm font-bold text-primary">{stat.value}</span>
            </div>
          ))}
        </div>
      )}
    </Card>
  );
};

export default InfoPanel;
