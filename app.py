from flask import Flask, render_template, request, jsonify
import numpy as np
import joblib
import os

from notebook.train_model import train_and_save_model

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(BASE_DIR, "model")
MODEL_PATH = os.path.join(MODEL_DIR, "aqi_model.pkl")

# Auto-train if model missing
if not os.path.exists(MODEL_PATH):
    print("Model not found. Training model...")
    model = train_and_save_model(MODEL_PATH)
else:
    model = joblib.load(MODEL_PATH)

def cat(a):
    if a <= 50:
        return "Good", "Healthy"
    elif a <= 100:
        return "Moderate", "Acceptable"
    else:
        return "Poor", "Unhealthy"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    d = request.json
    features = np.array([[
        float(d["pm25"]),
        float(d["pm10"]),
        float(d["no2"]),
        float(d["so2"]),
        float(d["co"]),
    ]])

    aqi = model.predict(features)[0]
    c, h = cat(aqi)

    return jsonify(
        aqi=round(aqi, 2),
        category=c,
        health=h
    )
