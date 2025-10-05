# BloomWatch Image Classification and Visualization Flow

## Detailed Image Upload Flow

```mermaid
graph TD
    A[User uploads flower image] --> B[Frontend calls /api/classify]
    B --> C[Backend classification service]
    C --> D{Load YoloV8 model}
    D --> E[Process image for flower classification]
    E --> F{Classify flower species}
    F --> G[Class: 'rose', confidence: 0.87]
    G --> H[Return classification result to frontend]
    H --> I[Frontend auto-fills flower field with 'rose']
    I --> J[User selects region to search]
    J --> K[Frontend calls /api/abundance with region='Kashmir' & flower='rose']
    K --> L[Backend abundance service processes request]
    L --> M[Fetch NDVI data from NASA EarthData API]
    M --> N[Process satellite data for bloom abundance]
    N --> O[Generate abundance heatmap data]
    O --> P[Return heatmap data to frontend]
    P --> Q[Frontend renders gradient heatmap on map]
    Q --> R[User sees bloom abundance visualization]
    
    style A fill:#e1f5fe
    style D fill:#fff3e0
    style F fill:#fff3e0
    style L fill:#f3e5f5
    style M fill:#fce4ec
    style Q fill:#e8f5e8
    style R fill:#e8f5e8