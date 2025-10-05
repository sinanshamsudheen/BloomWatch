#!/usr/bin/env python3
"""
Test script to verify YOLO model integration with the classification service
"""
import asyncio
import os
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock
import sys

# Add the server directory to the path to import modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

import tempfile
from io import BytesIO
from PIL import Image


class MockUploadFile:
    """Mock class to simulate FastAPI's UploadFile"""
    def __init__(self, file_path, filename):
        self.file_path = file_path
        self.filename = filename
        self.content_type = "image/jpeg"
        
    async def read(self):
        with open(self.file_path, "rb") as f:
            return f.read()
    
    async def seek(self, pos):
        # Mock seek function - not actually needed for our implementation
        pass


async def test_model_loading():
    """Test if the YOLO model loads correctly"""
    print("Testing YOLO model loading...")
    
    try:
        # Import here to catch any loading errors
        from services.classification_service import model, MODEL_PATH
        
        # Check if model file exists
        if not os.path.exists(MODEL_PATH):
            print(f"ERROR: Model file does not exist at {MODEL_PATH}")
            return False
            
        print(f"Model loaded successfully from {MODEL_PATH}")
        print(f"Model classes: {model.names if hasattr(model, 'names') else 'Unknown'}")
        return True
    except Exception as e:
        print(f"ERROR loading model: {e}")
        return False

async def test_classification_logic():
    """Test the classification logic with a mock file"""
    print("\nTesting classification logic...")
    
    # Create a temporary image file for testing
    # In reality, we would need an actual flower image, but we'll test the loading logic
    temp_image_path = os.path.join(tempfile.gettempdir(), "test_flower.jpg")
    
    # Create a dummy image for testing purposes
    try:
        # Create a simple dummy image
        img = Image.new('RGB', (224, 224), color='green')
        img.save(temp_image_path)
        
        # Create a mock UploadFile
        mock_file = MockUploadFile(temp_image_path, "test_flower.jpg")
        
        # Import the classification function after dependencies are available
        from services.classification_service import classify_flower_image
        
        # Test the classification function
        result = await classify_flower_image(mock_file)
        
        print(f"Classification result: {result}")
        
        # Clean up
        os.remove(temp_image_path)
        
        print("Classification logic test completed")
        return True
        
    except Exception as e:
        print(f"ERROR in classification test: {e}")
        import traceback
        traceback.print_exc()
        # Clean up in case of error
        if os.path.exists(temp_image_path):
            os.remove(temp_image_path)
        return False

async def main():
    print("Starting YOLO model integration tests...\n")
    
    # Test 1: Model loading
    model_loaded = await test_model_loading()
    
    if model_loaded:
        # Test 2: Classification logic
        classification_works = await test_classification_logic()
        
        if classification_works:
            print("\n✅ All tests passed! YOLO model integration appears to be working.")
        else:
            print("\n❌ Classification test failed.")
    else:
        print("\n❌ Model loading failed. Please check the model path and dependencies.")

if __name__ == "__main__":
    asyncio.run(main())