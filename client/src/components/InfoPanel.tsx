import { Card } from "@/components/ui/card";
import { Leaf, TrendingUp, MapPin, Info } from "lucide-react";
import { cn } from "@/lib/utils";

interface InfoPanelProps {
  title?: string;
  content?: string | React.ReactNode;
  stats?: { label: string; value: string }[];
  className?: string;
}

const InfoPanel = ({ title, content, stats, className }: InfoPanelProps) => {
  return (
    <Card className={cn("p-4 bg-card/95 backdrop-blur-sm border-border shadow-soft animate-fade-in", className)}>
      {title && (
        <div className="flex items-center gap-2 mb-3">
          <div className="p-1.5 rounded-lg bg-gradient-nature">
            <Leaf className="h-4 w-4 text-primary-foreground" />
          </div>
          <h3 className="text-sm font-semibold text-foreground">{title}</h3>
        </div>
      )}
      
      {content && (
        <div className="mb-3 text-xs text-muted-foreground leading-relaxed">
          {typeof content === 'string' ? (
            <div className="line-clamp-6 whitespace-pre-wrap">{content}</div>
          ) : (
            content
          )}
        </div>
      )}

      {stats && stats.length > 0 && (
        <div className="space-y-2">
          {stats.map((stat, index) => (
            <div key={index} className="flex items-center justify-between p-2 rounded-lg bg-muted/50">
              <span className="text-xs font-medium text-foreground flex items-center gap-1.5">
                {index === 0 && <TrendingUp className="h-3 w-3 text-primary" />}
                {index === 1 && <MapPin className="h-3 w-3 text-accent" />}
                {index === 2 && <Info className="h-3 w-3 text-info" />}
                {stat.label}
              </span>
              <span className="text-xs font-bold text-primary">{stat.value}</span>
            </div>
          ))}
        </div>
      )}
    </Card>
  );
};

export default InfoPanel;
