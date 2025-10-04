import { useState, useRef } from "react";
import { Upload, Image as ImageIcon, X } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { toast } from "sonner";

interface ImageUploadProps {
  onUpload: (file: File) => void;
}

const ImageUpload = ({ onUpload }: ImageUploadProps) => {
  const [preview, setPreview] = useState<string | null>(null);
  const [dragActive, setDragActive] = useState(false);
  const inputRef = useRef<HTMLInputElement>(null);

  const handleFile = (file: File) => {
    if (!file.type.startsWith("image/")) {
      toast.error("Please upload an image file");
      return;
    }

    const reader = new FileReader();
    reader.onload = (e) => {
      setPreview(e.target?.result as string);
    };
    reader.readAsDataURL(file);
    onUpload(file);
  };

  const handleDrag = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);

    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFile(e.dataTransfer.files[0]);
    }
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    e.preventDefault();
    if (e.target.files && e.target.files[0]) {
      handleFile(e.target.files[0]);
    }
  };

  const clearPreview = () => {
    setPreview(null);
    if (inputRef.current) {
      inputRef.current.value = "";
    }
  };

  return (
    <Card className="p-4 bg-card/95 backdrop-blur-sm border-border shadow-soft">
      <div className="flex items-center gap-2 mb-3">
        <div className="p-1.5 rounded-lg bg-gradient-bloom">
          <ImageIcon className="h-4 w-4 text-accent-foreground" />
        </div>
        <h3 className="text-base font-semibold text-foreground">Upload Flower Image</h3>
      </div>

      <div
        className={`relative border-2 border-dashed rounded-lg p-3 transition-all ${
          dragActive
            ? "border-primary bg-primary/5"
            : "border-border hover:border-primary/50"
        }`}
        onDragEnter={handleDrag}
        onDragLeave={handleDrag}
        onDragOver={handleDrag}
        onDrop={handleDrop}
      >
        {preview ? (
          <div className="relative">
            <img
              src={preview}
              alt="Preview"
              className="w-full h-24 object-cover rounded-lg"
            />
            <Button
              size="sm"
              variant="destructive"
              className="absolute top-1 right-1 h-6 w-6 p-0"
              onClick={clearPreview}
            >
              <X className="h-3 w-3" />
            </Button>
          </div>
        ) : (
          <div className="text-center py-2">
            <Upload className="mx-auto h-8 w-8 text-muted-foreground mb-2" />
            <p className="text-sm text-foreground font-medium mb-1">
              Click to upload or drag and drop
            </p>
            <p className="text-xs text-muted-foreground mb-2">
              PNG, JPG, WEBP up to 10MB
            </p>
            <Button
              onClick={() => inputRef.current?.click()}
              variant="outline"
              size="sm"
              className="border-primary text-primary hover:bg-primary/10 h-7 text-sm"
            >
              Select Image
            </Button>
          </div>
        )}
        <input
          ref={inputRef}
          type="file"
          className="hidden"
          accept="image/*"
          onChange={handleChange}
        />
      </div>

      {preview && (
        <Button
          className="w-full mt-3 bg-gradient-bloom hover:opacity-90 transition-opacity h-8 text-sm"
          onClick={() => toast.success("Image classification started!")}
        >
          Classify Flower
        </Button>
      )}
    </Card>
  );
};

export default ImageUpload;
