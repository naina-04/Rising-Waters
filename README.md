# Rising Water

An AI-powered web application for real-time flood risk prediction using machine learning and live meteorological data.

## Project Overview
**Rising Water** is an intelligent web application designed to predict the likelihood of flood events in real-time. By analyzing meteorological factors such as annual rainfall, monsoon intensity, temperature, and cloud visibility, the system provides an immediate risk probability. The platform utilizes an advanced **XGBoost Classification Model** trained on historical weather datasets to generate highly accurate predictions.

Built using the **Flask** framework with a modern, glassmorphic UI, the application ensures a responsive and interactive experience. It integrates seamlessly with the **Open-Meteo API** for live weather fetching and the **RainViewer API** for an interactive, live precipitation radar map.

## Key Features
- **Location Auto-Detection**: Uses browser geolocation and OpenStreetMap Nominatim to automatically detect the user's city and coordinates.
- **Live Weather Sync**: Integrates with Open-Meteo to automatically pull real-time temperature, humidity, and cloud visibility.
- **XGBoost Prediction Engine**: Processes 25 independent environmental features to classify flood risk (High/Low) and calculate exact probabilities.
- **Interactive Radar Map**: Utilizes Leaflet.js and the public RainViewer API to overlay live rain and snow radar.
- **Dynamic UI Dashboard**: Features a premium, glassmorphic design with animated gauges, progress bars, and integrated chart switching.

## Project Structure
- `dataset/`: Contains datasets used for model training.
- `models/`: Stores trained machine learning models.
- `notebooks/`: Jupyter notebooks for data analysis and model experimentation.
- `static/`: Static assets like CSS, JavaScript, and images.
- `templates/`: HTML templates for the Flask application.
- `app.py`: Main Flask application file.
- `documents/`: Project documentation (ignored in version control).

## Setup and Installation

### Requirements
- Python 3.8+
- Flask, Pandas, Numpy, XGBoost, Scikit-Learn, Requests, Joblib

### Installation
1. Clone the repository and navigate to the project directory.
2. Create a virtual environment and activate it.
3. Install dependencies: 
   ```bash
   pip install -r requirements.txt
   ```
4. Run the application: 
   ```bash
   python app.py
   ```
5. Access the application in your browser at `http://localhost:5000` (or as configured by Flask).
