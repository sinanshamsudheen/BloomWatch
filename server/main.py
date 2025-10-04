from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, Any
import os
import uvicorn
import logging

# Import API routes
from api.abundance import router as abundance_router
from api.explanation import router as explanation_router
from api.classify import router as classify_router

# Import configuration
from config import settings

# Configure logging
logging.basicConfig(level=getattr(logging, settings.LOG_LEVEL.upper()))
logger = logging.getLogger(__name__)

# Create FastAPI app instance
app = FastAPI(
    title="BloomWatch API",
    description="API for monitoring global plant blooming events using NASA satellite data",
    version="0.1.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        settings.FRONTEND_URL, 
        "http://localhost:5173", 
        "http://localhost:3000",
        "http://localhost:8080",  # Add port 8080 for your frontend
        "*"  # Allow all origins for development (remove in production)
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(abundance_router, prefix="/api", tags=["abundance"])
app.include_router(explanation_router, prefix="/api", tags=["explanation"])
app.include_router(classify_router, prefix="/api", tags=["classify"])

# Root endpoint
@app.get("/")
async def root():
    return {"message": "Welcome to BloomWatch API"}

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG
    )