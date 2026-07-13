from flask import Flask, render_template, request, redirect, url_for
import numpy as np
import pandas as pd
import joblib
import os

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

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict_page')
def predict_page():
    return render_template('predict.html')

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

        # Predict
        prediction = model.predict(input_scaled_df)[0]

        if prediction == 1:
            return redirect(url_for('result'))
        else:
            return redirect(url_for('no_flood'))
            
    except Exception as e:
        print(f"Error during prediction: {e}")
        return "An error occurred during prediction. Please try again.", 500

@app.route('/result')
def result():
    return render_template('result.html')

@app.route('/no_flood')
def no_flood():
    return render_template('no_flood.html')

if __name__ == '__main__':
    app.run(debug=True)
