from flask import Flask, render_template, request, jsonify
import numpy as np
import pandas as pd
import joblib
import os
import requests

app = Flask(__name__)

# Load the trained model and scaler
model_path = os.path.join('models', 'floods.save')
scaler_path = os.path.join('models', 'scaler.save')

model = joblib.load(model_path)
scaler = joblib.load(scaler_path)

# Define the expected feature columns in exact order used during training
FEATURE_COLUMNS = [
    'Monsoon_Intensity', 'Topography_Drainage', 'River_Management', 'Deforestation', 
    'Urbanization', 'Climate_Change', 'Dams_Quality', 'Siltation', 'Agricultural_Practices', 
    'Encroachments', 'Ineffective_Disaster_Preparedness', 'Drainage_Systems', 
    'Coastal_Vulnerability', 'Landslides', 'Watersheds', 'Deteriorating_Infrastructure', 
    'Population_Score', 'Wetland_Loss', 'Inadequate_Planning', 'Political_Factors', 
    'Annual_Rainfall', 'Seasonal_Rainfall', 'Temperature', 'Humidity', 'Cloud_Visibility'
]

# Default median values for infrastructural/environmental factors
DEFAULT_VALUES = {
    'Topography_Drainage': 5.0, 'River_Management': 5.0, 'Deforestation': 5.0, 
    'Urbanization': 5.0, 'Climate_Change': 5.0, 'Dams_Quality': 5.0, 'Siltation': 5.0, 
    'Agricultural_Practices': 5.0, 'Encroachments': 5.0, 'Ineffective_Disaster_Preparedness': 5.0, 
    'Drainage_Systems': 5.0, 'Coastal_Vulnerability': 5.0, 'Landslides': 5.0, 
    'Watersheds': 5.0, 'Deteriorating_Infrastructure': 5.0, 'Population_Score': 5.0, 
    'Wetland_Loss': 5.0, 'Inadequate_Planning': 5.0, 'Political_Factors': 5.0
}

def fetch_weather_from_coords(lat, lon):
    """Fetch accurate weather data from Open-Meteo API using coordinates.
    Open-Meteo uses national weather service data (NOAA, DWD, etc.) for high accuracy.
    No API key required.
    """
    weather_url = (
        f"https://api.open-meteo.com/v1/forecast?"
        f"latitude={lat}&longitude={lon}"
        f"&current=temperature_2m,relative_humidity_2m,cloud_cover"
        f"&timezone=auto"
    )
    response = requests.get(weather_url)
    if response.status_code != 200:
        return None
    
    data = response.json()
    current = data.get('current', {})
    
    temp = current.get('temperature_2m')
    humidity = current.get('relative_humidity_2m')
    # Cloud cover is 0-100%, we scale to 0-10 to match our dataset
    cloud_cover = current.get('cloud_cover', 50)
    cloud_visibility = round(10.0 - (cloud_cover / 10.0), 1)  # Higher cloud = lower visibility
    
    return {
        'temperature': temp,
        'humidity': humidity,
        'cloud_visibility': cloud_visibility
    }

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict_page')
def predict_page():
    return render_template('predict.html')

@app.route('/fetch_weather', methods=['POST'])
def fetch_weather():
    """Fetch weather by city name. Uses Open-Meteo geocoding + weather API."""
    try:
        data = request.get_json()
        city = data.get('city')

        # Step 1: Geocode city name to lat/lon using Open-Meteo Geocoding API
        geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1&language=en"
        geo_response = requests.get(geo_url)
        geo_data = geo_response.json()
        
        results = geo_data.get('results')
        if not results:
            return jsonify({'success': False, 'error': f'City "{city}" not found. Try a different spelling.'})
        
        location = results[0]
        lat = location['latitude']
        lon = location['longitude']
        city_name = location.get('name', city)
        country = location.get('country', '')

        # Step 2: Fetch weather from Open-Meteo
        weather = fetch_weather_from_coords(lat, lon)
        if not weather:
            return jsonify({'success': False, 'error': 'Failed to fetch weather data.'})

        return jsonify({
            'success': True,
            'city': f"{city_name}, {country}",
            **weather
        })

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/fetch_weather_coords', methods=['POST'])
def fetch_weather_coords():
    """Fetch weather using latitude and longitude from browser geolocation."""
    try:
        data = request.get_json()
        lat = data.get('lat')
        lon = data.get('lon')

        # Step 1: Fetch weather from Open-Meteo
        weather = fetch_weather_from_coords(lat, lon)
        if not weather:
            return jsonify({'success': False, 'error': 'Failed to fetch weather data.'})

        # Step 2: Reverse geocode to get city name using Nominatim (OpenStreetMap)
        city_name = "Your Location"
        try:
            nominatim_url = (
                f"https://nominatim.openstreetmap.org/reverse?"
                f"lat={lat}&lon={lon}&format=json&zoom=10"
            )
            headers = {'User-Agent': 'RisingWaters-FloodPrediction/1.0'}
            geo_response = requests.get(nominatim_url, headers=headers)
            if geo_response.status_code == 200:
                geo_data = geo_response.json()
                address = geo_data.get('address', {})
                city_name = address.get('city') or address.get('town') or address.get('village') or address.get('state_district') or 'Your Location'
        except Exception:
            pass  # If reverse geocoding fails, we still have the weather data

        return jsonify({
            'success': True,
            'city': city_name,
            **weather
        })

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get user inputs from the form
        user_inputs = {
            'Monsoon_Intensity': float(request.form['monsoon_intensity']),
            'Annual_Rainfall': float(request.form['annual_rainfall']),
            'Seasonal_Rainfall': float(request.form['seasonal_rainfall']),
            'Temperature': float(request.form['temperature']),
            'Humidity': float(request.form['humidity']),
            'Cloud_Visibility': float(request.form['cloud_visibility'])
        }

        # Combine user inputs with default medians to form the full 25 features
        input_data = {}
        for col in FEATURE_COLUMNS:
            if col in user_inputs:
                input_data[col] = user_inputs[col]
            else:
                input_data[col] = DEFAULT_VALUES[col]

        # Convert to DataFrame
        input_df = pd.DataFrame([input_data])

        # Scale the features
        input_scaled = scaler.transform(input_df)
        input_scaled_df = pd.DataFrame(input_scaled, columns=FEATURE_COLUMNS)

        # Predict Class and Probability
        prediction = int(model.predict(input_scaled_df)[0])
        probability = model.predict_proba(input_scaled_df)[0][1] * 100 

        return render_template('dashboard.html', 
                               prediction=prediction, 
                               probability=round(probability, 2), 
                               inputs=user_inputs)
            
    except Exception as e:
        print(f"Error during prediction: {e}")
        return "An error occurred during prediction. Please try again.", 500

if __name__ == '__main__':
    app.run(debug=True)
