import os
import logging
from typing import Dict, Any, List
from fastapi import UploadFile
import uuid
from datetime import datetime
from io import BytesIO
from ultralytics import YOLO
from PIL import Image
import tempfile
import cv2
import numpy as np

# Load the trained YOLO model
MODEL_PATH = "/mnt/e/Projects/VSC/Bloomwatch/BloomWatch/model/runs/detect/yolov8_flower_model_final/weights/best.pt"
model = YOLO(MODEL_PATH)

# Define flower class names based on your trained model's classes
# Retrieved from model.names during initialization
CLASS_NAMES = list(model.names.values()) if hasattr(model, 'names') else [
    "cactus", "lily", "lotus", "rose", "tulip"
]

async def classify_flower_image(file: UploadFile) -> Dict[str, Any]:
    """
    Classify a flower image using the trained YOLO model
    """
    logging.info(f"Classifying image: {file.filename}")
    
    # Generate a unique ID for this classification
    classification_id = str(uuid.uuid4())
    
    # Read the file content
    contents = await file.read()
    await file.seek(0)  # Reset file pointer
    
    # Save uploaded file temporarily to process with YOLO
    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1]) as temp_file:
        temp_file.write(contents)
        temp_file_path = temp_file.name
    
    try:
        # Run YOLO prediction on the image
        results = model(temp_file_path)
        
        # Process results
        predictions = []
        for r in results:
            # Extract class names and confidence scores
            boxes = r.boxes
            if boxes is not None:
                for box in boxes:
                    cls = int(box.cls[0])
                    conf = float(box.conf[0])
                    
                    # Get the class name (handle case where cls index might be out of range)
                    if cls < len(CLASS_NAMES):
                        class_name = CLASS_NAMES[cls]
                    else:
                        class_name = f"Unknown class {cls}"
                    
                    predictions.append({
                        "class": class_name,
                        "confidence": conf
                    })
        
        # Determine the primary classification (highest confidence)
        if predictions:
            # Sort by confidence to get the highest
            predictions.sort(key=lambda x: x["confidence"], reverse=True)
            primary_prediction = predictions[0]
            
            classification_result = primary_prediction["class"]
            confidence = primary_prediction["confidence"]
            
            # Get up to 2 additional similar species based on other predictions
            similar_species = []
            for pred in predictions[1:3]:  # Get next 2 predictions
                similar_species.append({
                    "name": pred["class"],
                    "confidence": pred["confidence"]
                })
        else:
            # If no flowers detected, return a default response
            classification_result = "No flower detected"
            confidence = 0.0
            similar_species = []
        
        return {
            "id": classification_id,
            "filename": file.filename,
            "timestamp": datetime.utcnow().isoformat(),
            "classification": classification_result,
            "confidence": confidence,
            "location": None,  # Would be determined from EXIF data or user input in future
            "similar_species": similar_species
        }
    
    finally:
        # Clean up the temporary file
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)