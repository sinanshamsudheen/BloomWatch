# BloomWatch Server

The BloomWatch server is a FastAPI-based backend that processes satellite data from NASA's EarthObservation APIs to monitor and predict plant blooming events globally.

## Features

- **NDVI Data Processing**: Retrieves and processes Normalized Difference Vegetation Index (NDVI) data from NASA EarthData API
- **Bloom Abundance Mapping**: Generates abundance maps for specific flowers in specific regions
- **Ecological Explanations**: Provides contextual explanations for bloom patterns based on environmental factors
- **Image Classification**: Upload and classify flower images with location identification

## Architecture

The server is organized as follows:

```
server/
├── main.py          # FastAPI application entry point
├── requirements.txt # Python dependencies
├── .env            # Environment variables
├── api/            # API endpoints
│   ├── abundance.py
│   ├── explanation.py
│   └── classify.py
├── services/       # Business logic
│   ├── ndvi_service.py
│   ├── explanation_service.py
│   └── classification_service.py
├── models/         # Data models
│   └── data_models.py
└── config.py       # Configuration settings
```

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your NASA API key and other settings
```

3. Run the server:
```bash
python main.py
```

## API Endpoints

- `GET /api/abundance` - Get NDVI abundance data for a region and flower
- `GET /api/explanation` - Get ecological explanation for bloom patterns
- `POST /api/classify` - Upload and classify flower images

## NASA EarthData API Integration

The server connects to NASA's EarthData API to retrieve MODIS NDVI data. You'll need a NASA EarthData API key to access real data. For development purposes, mock data is generated when the API key is not provided.