import requests
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
import joblib

# 1. Fetch Historical Weather Data (Open-Meteo Archive API)
def fetch_training_data():
    print("Fetching historical weather data...")
    url = "https://archive-api.open-meteo.com/v1/archive"
    params = {
        "latitude": 51.5074, # London (Generic training location)
        "longitude": -0.1278,
        "start_date": "2023-01-01",
        "end_date": "2024-01-01",
        "hourly": "temperature_2m"
    }
    response = requests.get(url, params=params)
    data = response.json()
    
    # Convert to DataFrame
    df = pd.DataFrame({
        "time": data["hourly"]["time"],
        "temperature": data["hourly"]["temperature_2m"]
    })
    return df

# 2. Prepare Features (X) and Labels (y)
def prepare_data(df):
    # We want to predict NEXT hour's temp based on CURRENT temp
    # Feature: Current Temp (t)
    # Label:   Next Hour Temp (t+1)
    
    df['target'] = df['temperature'].shift(-1) # Shift data up by 1 row
    df = df.dropna() # Drop the last row (has no target)
    
    X = df[['temperature']] # Inputs (2D array)
    y = df['target']        # Outputs
    return X, y

# 3. Train and Save
def train():
    df = fetch_training_data()
    X, y = prepare_data(df)
    
    # Split into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Train a simple Linear Regression model
    model = LinearRegression()
    model.fit(X_train, y_train)
    
    # Evaluate
    predictions = model.predict(X_test)
    mae = mean_absolute_error(y_test, predictions)
    print(f"Model Trained! MAE: {mae:.2f}°C")
    print("This means the model is usually within", round(mae, 2), "degrees of the truth.")
    
    # Save the model to a file
    joblib.dump(model, "app/weather_model.pkl")
    print("Model saved to app/weather_model.pkl")

if __name__ == "__main__":
    train()