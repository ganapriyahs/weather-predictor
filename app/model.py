import random

class WeatherPredictor:
    def __init__(self):
        # Later, we will load a real model here
        # self.model = joblib.load("model.pkl")
        pass

    def predict(self, current_data: dict):
        """
        Predicts weather for the next hour based on current data.
        Returns a simplified prediction dictionary.
        """
        if not current_data:
            return {"error": "No data provided"}

        # REAL LOGIC GOES HERE LATER
        # input_features = [current_data['temperature'], current_data['humidity']...]
        # prediction = self.model.predict([input_features])

        # MOCK LOGIC: 
        # Predicts temp will change by random -1 to +1 degree
        current_temp = current_data.get("temperature", 0)
        predicted_temp = current_temp + random.uniform(-1, 1)

        return {
            "predicted_temperature_next_hour": round(predicted_temp, 2),
            "confidence_score": 0.95,
            "status": "prediction_successful"
        }