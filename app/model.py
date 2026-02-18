import joblib
import os

class WeatherPredictor:
    def __init__(self):
        # Load the trained model
        # We use os.path to make sure we find the file correctly
        model_path = os.path.join(os.path.dirname(__file__), "weather_model.pkl")
        try:
            self.model = joblib.load(model_path)
        except Exception as e:
            print(f"Error loading model: {e}")
            self.model = None

    def predict(self, current_data: dict):
        if not current_data or self.model is None:
            return {"error": "Model not loaded or no data"}

        # Extract the feature our model expects (Current Temperature)
        current_temp = current_data.get("temperature")
        
        # Scikit-learn expects a 2D array: [[feature1, feature2...]]
        prediction = self.model.predict([[current_temp]])[0]

        return {
            "predicted_temperature_next_hour": round(prediction, 2),
            "model_type": "LinearRegression (v1)",
            "status": "success"
        }