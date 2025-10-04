# BloomWatch – Model

## Objective
This component extracts flower or green area information from images or coordinates, powers NDVI-bloom mapping, and generates contextual ecological summaries using AI if required.

## Core Responsibilities
- Maintain any custom-trained or heuristic models for bloom/greenery/flower detection if time permits.
- Provide NDVI-to-abundance estimation logic (as simple as threshold mapping for MVP).
- Generate bloom explanations/context if not handled by backend.
- Package easy classifiers or scripts for use by backend.

## Final Goals
- Simple, clear NDVI-to-abundance conversion logic for backend.
- Optional: Demo-ready flower classification script/model, if images are needed for extension.
- Optional: AI/NLP script for regional ecological summary generation.

## Data Flow
- Receives: Region/flower or, optionally, user-uploaded image.
- Outputs: Bloom abundance score or class.
- Returns logic/classifier or context string to backend upon request.

## Tech Stack
- Python, pandas, scikit-learn, YOLO/FastAI (for rapid prototyping if flower/greenery detection included)
- CSV/JSON for lookup/reference data (flower-habitat mapping)

## Instructions
- Store model scripts and checkpoints here.
- Write docs for any custom preprocessing or invocation logic.
- Collaborate with server team for API/data pipeline format.

## Notes
For the 24hr hackathon, prioritize simple NDVI mapping, and provide clear integration docs for backend if a classifier is implemented.
