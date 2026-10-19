
import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest

FEATURES = ["temperature", "vibration", "usage_hours"]


def train_model():
    rng = np.random.default_rng(42)

    normal_data = pd.DataFrame({
        "temperature": rng.normal(37, 2, 500),
        "vibration": rng.normal(2, 0.5, 500),
        "usage_hours": rng.uniform(0, 5000, 500)
    })

    model = IsolationForest(
        n_estimators=100,
        contamination=0.05,
        random_state=42
    )

    model.fit(normal_data[FEATURES])
    return model


def analyse_equipment(model, temperature, vibration, usage_hours):
    readings = pd.DataFrame([{
        "temperature": temperature,
        "vibration": vibration,
        "usage_hours": usage_hours
    }])

    prediction = model.predict(readings[FEATURES])[0]
    score = model.decision_function(readings[FEATURES])[0]

    anomaly = prediction == -1

    if temperature >= 45 or vibration >= 4.5:
        priority = "HIGH"
        recommendation = "Arrange prompt inspection by qualified staff."
    elif (
        anomaly or temperature >= 41
        or vibration >= 3.5 or usage_hours >= 4000
    ):
        priority = "MEDIUM"
        recommendation = "Review equipment history and schedule inspection."
    else:
        priority = "LOW"
        recommendation = "Continue routine monitoring."

    return {
        "anomaly": anomaly,
        "anomaly_score": round(float(score), 4),
        "priority": priority,
        "recommendation": recommendation
    }

