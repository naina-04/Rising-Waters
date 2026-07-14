# PROJECT DOCUMENTATION

## Rising Water
An AI-powered web application for real-time flood risk prediction using machine learning and live meteorological data.

---

### 1. Project Overview
**Rising Water** is an intelligent web application designed to predict the likelihood of flood events in real-time. By analyzing meteorological factors such as annual rainfall, monsoon intensity, temperature, and cloud visibility, the system provides an immediate risk probability. The platform utilizes an advanced **XGBoost Classification Model** trained on historical weather datasets to generate highly accurate predictions. 

Built using the **Flask** framework with a modern, glassmorphic UI, the application ensures a responsive and interactive experience. It integrates seamlessly with the **Open-Meteo API** for live weather fetching and the **RainViewer API** for an interactive, live precipitation radar map.

#### 1.1 Core Value Proposition
* **Instant Risk Analysis:** Turns localized meteorological inputs into a precise, easy-to-understand flood risk probability in seconds.
* **Keyless Live Data:** Automatically fetches live weather data (temperature, humidity, cloud visibility) based on user GPS coordinates without requiring manual API keys.
* **Live Radar Mapping:** Grounds predictions with an interactive, real-time Leaflet.js radar map showing global precipitation and storm movements.
* **Intuitive Dashboard:** Presents complex machine learning outputs in a sleek, user-friendly dashboard designed for both experts and the general public.

---

### 2. Key Features
| Feature | Description |
| :--- | :--- |
| **Location Auto-Detection** | Uses browser geolocation and OpenStreetMap Nominatim to automatically detect the user's city and coordinates. |
| **Live Weather Sync** | Integrates with Open-Meteo to automatically pull real-time temperature, humidity, and cloud visibility for the targeted region. |
| **XGBoost Prediction Engine** | Processes 25 independent environmental features through a highly optimized XGBoost model to classify flood risk (High/Low) and calculate exact probabilities. |
| **Interactive Radar Map** | Utilizes Leaflet.js and the public RainViewer API to overlay live rain and snow radar directly onto a dark-themed CartoDB map. |
| **Dynamic UI Dashboard** | Features a premium, glassmorphic design with animated gauges, progress bars, and an integrated chart switching system (Bar, Line, Pie, Donut). |
| **Educational Glossary** | Includes a dedicated "Understanding the Data" page to explain the significance of variables like Monsoon Intensity and Seasonal Rainfall. |

---

### 3. Use Case Scenarios

**Scenario 1 — Early Flood Warning and Evacuation Planning**
A meteorologist or local official uses the "Auto-Detect" feature for a coastal district. The system fetches the current weather, and the user inputs expected seasonal rainfall. The XGBoost model predicts an 85% (High Risk) probability of flooding, allowing authorities to issue evacuation advisories hours in advance.

**Scenario 2 — Disaster Response and Resource Allocation**
A disaster relief coordinator monitors multiple regions during the monsoon season. By manually entering city names (e.g., "Mumbai", "Chennai"), they instantly retrieve live weather data, radar maps, and risk classifications, helping them prioritize where to deploy rescue boats and resources.

**Scenario 3 — Public Awareness and Preparedness**
A homeowner living in a flood-prone valley uses the application to check their immediate risk during heavy rains. The visual dashboard and live precipitation map help them make an informed decision about securing their property.

---

### 4. Technical Architecture

#### 4.1 System Flow
`User` → `Browser (HTML/CSS/JS)` → `Flask Backend` → `[ XGBoost Model & Open-Meteo API ]` → `Dashboard Rendering (Chart.js & Leaflet.js)`

| Component | Role |
| :--- | :--- |
| **User** | Interacts with the frontend to input data or auto-detect location. |
| **Frontend UI** | Collects input, handles form validation, and renders the dynamic dashboard using Bootstrap 5, Chart.js, and Leaflet.js. |
| **Flask Backend** | Exposes REST routes (`/predict`, `/fetch_weather`); orchestrates API calls and data transformation. |
| **XGBoost Model** | The core machine learning engine that ingests the scaled feature matrix and outputs risk probabilities. |
| **Open-Meteo API** | Fetches live weather data and handles forward/reverse geocoding. |
| **RainViewer API** | Provides live raster tiles for the precipitation radar map. |

#### 4.2 Technology Stack
| Layer | Technology |
| :--- | :--- |
| **Backend Framework** | Python / Flask |
| **Frontend** | HTML5, CSS3, JavaScript (Vanilla), Bootstrap 5 |
| **Machine Learning** | Scikit-Learn, XGBoost, Pandas, Numpy |
| **Data Visualization** | Chart.js (Graphs), Leaflet.js (Maps) |
| **External APIs** | Open-Meteo (Weather/Geocoding), RainViewer (Radar), Nominatim (OSM) |
| **Version Control** | Git & GitHub |

---

### 5. System Requirements

#### 5.1 Hardware Requirements
| Component | Minimum Specification |
| :--- | :--- |
| **Processor** | Intel i3 / equivalent or higher |
| **RAM** | Minimum 4 GB |
| **Storage** | 2 GB free disk space |
| **Network** | Active internet connection (required for APIs and Maps) |

#### 5.2 Software Requirements
| Component | Specification |
| :--- | :--- |
| **Operating System** | Windows / Linux / macOS |
| **Language Runtime** | Python 3.8+ |
| **Backend Framework** | Flask |
| **Required Libraries** | `flask`, `pandas`, `numpy`, `xgboost`, `scikit-learn`, `requests`, `joblib` |
| **IDE** | Visual Studio Code / PyCharm / Jupyter Notebook |

---

### 6. Skills Required
* Python (Programming Language)
* Flask (Web Framework)
* Machine Learning & Classification Algorithms
* Data Preprocessing (Pandas, Scikit-Learn)
* Frontend Development (HTML, CSS, JS, Bootstrap)
* API Integration (REST APIs)
* Data Visualization & GIS Mapping (Chart.js, Leaflet)

---

### 7. Quality & Testing
The application features a modular design that separates frontend logic, API routing, and machine learning inference:
* **Model Evaluation:** The XGBoost model was rigorously tested during the training phase against historical datasets, achieving high accuracy metrics using confusion matrices and classification reports.
* **Frontend Resilience:** The JavaScript logic includes robust error handling for browser geolocation failures, API timeouts, and invalid user inputs.
* **Scalability:** The Flask architecture allows the model inference layer to be decoupled and easily deployed to cloud environments (like IBM Cloud or Heroku) with minimal configuration changes.

---

### 8. Conclusion
**Rising Water** demonstrates a highly practical, end-to-end application of Machine Learning in the realm of environmental safety and disaster management. By combining a highly accurate predictive model with real-time weather APIs and interactive visual mapping, it provides a comprehensive, user-friendly tool that bridges the gap between complex meteorological data and actionable public safety insights.
