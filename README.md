# Phone Comparison API

A FastAPI service that uses Ollama's LLM (Gemma 3 4B) to compare smartphones based on their specifications and price.

## Features

- Compare multiple phones with their specs and prices
- Get concise one-sentence comparison results
- Customizable comparison question
- Local LLM integration via Ollama

## Prerequisites

- Python 3.7+
- Ollama running locally (with Gemma 3 4B model installed)
- FastAPI
- Uvicorn

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/phone-comparison-api.git
   cd phone-comparison-api

## Sample Request

1. URL http://0.0.0.0:8000/compare-phones/
2. {
  "phones": [
    {
      "name": "Apple iPhone 16e",
      "specs": "Camera Mode:Photonic Engine;Portrait Lighting with six effects;Night mode;Panorama (up to 63MP);Spatial photos;Macro photography;Lens correction (Ultra Wide);Advanced red‑eye correction;Auto image stabilization;Burst mode;Photo geotagging;Image formats captured: HEIF and JPEG, Rear Camera : 48MP Fusion: 26 mm, ƒ/1.6 aperture, sensor‑shift optical image stabilization, 100% Focus Pixels, support for super-high-resolution photos (24MP and 48MP), Front Camera:12MP camera;ƒ/1.9 aperture;Autofocus with Focus Pixels;Retina Flash;Deep Fusion;Smart HDR 5;Next-generation portraits with Focus and Depth Control;Portrait Lighting with six effects;Animoji and Memoji;Latest-generation Photographic Styles;Wide color capture for photos and Live Photos;Lens correction",
      "price": 599.99
    },
    {
      "name": "Apple iPhone 16",
      "specs": "Camera Mode:Photonic Engine;Portrait Lighting with six effects;Night mode;Panorama (up to 63MP);Spatial photos;Macro photography;Lens correction (Ultra Wide);Advanced red‑eye correction;Auto image stabilization;Burst mode;Photo geotagging;Image formats captured: HEIF and JPEG,Rear Camera:48MP Fusion: 26 mm, ƒ/1.6 aperture, sensor‑shift optical image stabilization, 100% Focus Pixels, support for super-high-resolution photos (24MP and 48MP),Front Camera:12MP camera;ƒ/1.9 aperture;Autofocus with Focus Pixels;Retina Flash;Deep Fusion;Smart HDR 5;Next-generation portraits with Focus and Depth Control;Portrait Lighting with six effects;Animoji and Memoji;Latest-generation Photographic Styles;Wide color capture for photos and Live Photos;Lens correction",
      "price": 829.99
    }
  ],
  "user_question": "Which phone has better camera capabilities, compare beased on sensors and modes?"
}

