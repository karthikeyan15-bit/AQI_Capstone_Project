import os
import joblib
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split

# ---------- PATHS ----------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "dataset", "air_quality.csv")
MODEL_DIR = os.path.join(BASE_DIR, "model")
MODEL_PATH = os.path.join(MODEL_DIR, "aqi_model.pkl")

# ---------- CREATE MODEL FOLDER ----------
os.makedirs(MODEL_DIR, exist_ok=True)

# ---------- LOAD DATA ----------
df = pd.read_csv(DATA_PATH)

X = df.drop("aqi", axis=1)
y = df["aqi"]

# ---------- TRAIN ----------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = RandomForestRegressor(
    n_estimators=100,
    random_state=42
)
model.fit(X_train, y_train)

# ---------- SAVE MODEL ----------
joblib.dump(model, MODEL_PATH)

print("✅ Model trained and saved at:", MODEL_PATH)

