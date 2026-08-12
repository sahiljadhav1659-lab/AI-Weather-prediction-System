import pandas as pd
import joblib
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    classification_report,
    ConfusionMatrixDisplay
)

# -------------------------
# Load Dataset
# -------------------------
df = pd.read_csv("dataset/clean_weather.csv")

# -------------------------
# Create Target Column
# -------------------------
df["Rain"] = (df["rain_sum"] > 0).astype(int)

# -------------------------
# Features
# -------------------------
X = df[
    [
        "temperature_2m_max",
        "temperature_2m_min",
        "apparent_temperature_max",
        "apparent_temperature_min",
        "precipitation_sum",
        "wind_speed_10m_max",
        "wind_gusts_10m_max",
        "weather_code"
    ]
]

# -------------------------
# Target
# -------------------------
y = df["Rain"]

# -------------------------
# Split Dataset
# -------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42
)

# -------------------------
# Train Model
# -------------------------
model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

model.fit(X_train, y_train)

# -------------------------
# Prediction
# -------------------------
y_pred = model.predict(X_test)

# -------------------------
# Accuracy
# -------------------------
accuracy = accuracy_score(y_test, y_pred)

print("\nAccuracy:", round(accuracy * 100, 2), "%")

print("\nConfusion Matrix")
print(confusion_matrix(y_test, y_pred))

print("\nClassification Report")
print(classification_report(y_test, y_pred))

# -------------------------
# Save Confusion Matrix Image
# -------------------------
ConfusionMatrixDisplay.from_predictions(
    y_test,
    y_pred,
    cmap="Blues"
)

plt.title("Confusion Matrix")
plt.savefig("static/graphs/confusion_matrix.png")
plt.close()

print("✅ Confusion Matrix Saved!")
# -------------------------
# Feature Importance Graph
# -------------------------

import matplotlib.pyplot as plt

feature_names = X.columns
importance = model.feature_importances_

plt.figure(figsize=(10,5))
plt.bar(feature_names, importance)

plt.xticks(rotation=45)
plt.title("Feature Importance")
plt.tight_layout()

plt.savefig("static/graphs/feature_importance.png")
plt.close()

print("✅ Feature Importance Graph Saved!")
# -------------------------
# Save Model
# -------------------------
joblib.dump(model, "models/weather_model.pkl")

print("✅ Model Saved Successfully!")