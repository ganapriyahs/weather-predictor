from fastapi import FastAPI, HTTPException, Query
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from prometheus_fastapi_instrumentator import Instrumentator # <-- Import this

from app.weather_client import WeatherClient
from app.model import WeatherPredictor

app = FastAPI(title="Real-Time Weather Predictor")

# 1. Setup Monitoring (Prometheus)
instrumentator = Instrumentator().instrument(app).expose(app)

# Mount the static directory
app.mount("/static", StaticFiles(directory="app/static"), name="static")

weather_client = WeatherClient()
predictor = WeatherPredictor()

@app.get("/")
def read_root():
    return FileResponse('app/static/index.html')

@app.get("/predict")
def predict_weather(city: str = Query(..., description="City name")):
    coords = weather_client.get_coordinates(city)
    if not coords:
        raise HTTPException(status_code=404, detail=f"City '{city}' not found.")

    live_data = weather_client.get_current_weather(coords['lat'], coords['lon'])
    if not live_data:
        raise HTTPException(status_code=503, detail="Failed to fetch weather data")

    live_data['city_info'] = {"name": coords['name'], "country": coords['country']}
    
    # Make the prediction
    prediction = predictor.predict(live_data)

    return {
        "location": coords['name'],
        "country": coords['country'],
        "current_weather": live_data,
        "prediction": prediction
    }