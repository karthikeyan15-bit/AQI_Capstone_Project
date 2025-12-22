import os
import joblib
import pandas as pd
import numpy as np
from flask import Flask, render_template, request, jsonify
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "dataset", "air_quality.csv")
MODEL_DIR = os.path.join(BASE_DIR, "model")
MODEL_PATH = os.path.join(MODEL_DIR, "aqi_model.pkl")

os.makedirs(MODEL_DIR, exist_ok=True)

# ---------------- TRAIN MODEL IF NOT EXISTS ----------------
def train_and_save_model():
    df = pd.read_csv(DATA_PATH)

    # normalize column names
    df.columns = df.columns.str.strip().str.lower()

    TARGET = "aqi"
    X = df.drop(TARGET, axis=1)
    y = df[TARGET]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = RandomForestRegressor(
        n_estimators=50,
        max_depth=10,
        random_state=42
    )
    model.fit(X_train, y_train)

    joblib.dump(model, MODEL_PATH, compress=3)
    return model

# ---------------- LOAD OR CREATE MODEL ----------------
if not os.path.exists(MODEL_PATH):
    print("🔄 Training model for first time...")
    model = train_and_save_model()
else:
    print("✅ Loading existing model...")
    model = joblib.load(MODEL_PATH)

# ---------------- AQI CATEGORY ----------------
def aqi_category(aqi):
    if aqi <= 50:
        return "Good", "Healthy air quality"
    elif aqi <= 100:
        return "Moderate", "Acceptable air quality"
    else:
        return "Poor", "Unhealthy air quality"

# ---------------- ROUTES ----------------
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    data = request.json

    features = np.array([[
        float(data["pm25"]),
        float(data["pm10"]),
        float(data["no2"]),
        float(data["so2"]),
        float(data["co"]),
    ]])

    prediction = model.predict(features)[0]
    category, health = aqi_category(prediction)

    return jsonify(
        aqi=round(prediction, 2),
        category=category,
        health=health
    )

if __name__ == "__main__":
    app.run()
