from fastapi import FastAPI, HTTPException, Query
from fastapi.staticfiles import StaticFiles # Import this
from fastapi.responses import FileResponse # Import this
from app.weather_client import WeatherClient
from app.model import WeatherPredictor

app = FastAPI(title="Real-Time Weather Predictor")

# Mount the static directory
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Initialize our classes
weather_client = WeatherClient()
predictor = WeatherPredictor()

# Serve the HTML on the root route
@app.get("/")
def read_root():
    return FileResponse('app/static/index.html')

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/predict")
def predict_weather(city: str = Query(..., description="City name")):
    # ... (Keep existing logic exactly as is) ...
    coords = weather_client.get_coordinates(city)
    if not coords:
        raise HTTPException(status_code=404, detail=f"City '{city}' not found.")

    live_data = weather_client.get_current_weather(coords['lat'], coords['lon'])
    if not live_data:
        raise HTTPException(status_code=503, detail="Failed to fetch weather data")

    live_data['city_info'] = {"name": coords['name'], "country": coords['country']}
    prediction = predictor.predict(live_data)

    return {
        "location": coords['name'],
        "country": coords['country'],
        "current_weather": live_data,
        "prediction": prediction
    }