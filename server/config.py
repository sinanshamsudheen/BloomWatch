import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # NASA EarthData API configuration
    NASA_API_URL: str = "https://nrt3.modaps.eosdis.nasa.gov/api/v2/content"
    NASA_API_KEY: str = os.getenv("NASA_API_KEY", "")
    
    # Server configuration
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", 8000))
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    
    # Database configuration (for future use)
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./bloomwatch.db")
    
    # ML model configuration (for future use)
    MODEL_PATH: str = os.getenv("MODEL_PATH", "./models/flower_classifier_v1.pkl")
    
    # Logging configuration
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    
    # CORS origins (to be configured based on frontend URL)
    FRONTEND_URL: str = os.getenv("FRONTEND_URL", "http://localhost:5173")
    
    # AI Agent Configuration
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    SERPAPI_API_KEY: str = os.getenv("SERPAPI_API_KEY", "")
    NEWSAPI_API_KEY: str = os.getenv("NEWSAPI_API_KEY", "")
    
    # Agent timeouts and limits
    AGENT_TIMEOUT: int = int(os.getenv("AGENT_TIMEOUT", 30))
    MAX_SEARCH_RESULTS: int = int(os.getenv("MAX_SEARCH_RESULTS", 5))

    class Config:
        env_file = ".env"

# Create settings instance
settings = Settings()