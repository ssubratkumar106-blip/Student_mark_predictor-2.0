"""Student Marks Prediction web application."""

import json
import os

import joblib
import numpy as np
from flask import Flask, flash, redirect, render_template, request, url_for

from data_handler import load_dataset
from train_model import METRICS_PATH, MODEL_PATH, train_and_save

app = Flask(__name__)
app.secret_key = "student-marks-prediction"


def ensure_model():
    """Train model automatically if files are missing."""
    if not os.path.exists(MODEL_PATH) or not os.path.exists(METRICS_PATH):
        train_and_save()


def load_metrics() -> dict:
    """Load saved model metrics."""
    ensure_model()
    with open(METRICS_PATH, encoding="utf-8") as file:
        return json.load(file)


def load_model():
    """Load trained regression model."""
    ensure_model()
    return joblib.load(MODEL_PATH)


def predict_marks(study_hours: float) -> float:
    """Predict marks using trained model."""
    model = load_model()
    value = float(model.predict(np.array([[study_hours]]))[0])
    return round(float(np.clip(value, 0, 100)), 2)


def validate_hours(value: str):
    """Validate user input."""
    try:
        hours = float(value)
    except (TypeError, ValueError):
        return False, "Enter a valid number.", None

    if hours <= 0 or hours > 24:
        return False, "Study hours must be between 0 and 24.", None
    return True, "", hours


def get_chart_data(study_hours: float, predicted_marks: float) -> dict:
    """Build chart data for visual prediction."""
    metrics = load_metrics()
    model = load_model()
    line_x = [round(x, 1) for x in np.linspace(0.5, 10, 40)]
    line_y = [round(float(np.clip(model.predict([[x]])[0], 0, 100)), 2) for x in line_x]
    return {
        "train_hours": metrics.get("train_hours", []),
        "train_marks": metrics.get("train_marks", []),
        "line_x": line_x,
        "line_y": line_y,
        "pred_hours": study_hours,
        "pred_marks": predicted_marks,
        "coefficient": metrics.get("coefficient", 0),
        "intercept": metrics.get("intercept", 0),
    }


@app.context_processor
def inject_globals():
    """Share metrics with all templates."""
    try:
        metrics = load_metrics()
    except Exception:
        metrics = {}
    return {"metrics": metrics, "test_metrics": metrics.get("test", {})}


@app.route("/")
def index():
    """Home page."""
    df = load_dataset()
    metrics = load_metrics()
    return render_template(
        "index.html",
        dataset_preview=metrics.get("dataset_preview", df.head(8).to_dict(orient="records")),
        total_samples=metrics.get("samples", len(df)),
    )


@app.route("/predict", methods=["POST"])
def predict():
    """Handle prediction."""
    is_valid, message, study_hours = validate_hours(request.form.get("study_hours", ""))
    if not is_valid:
        flash(message, "error")
        return redirect(url_for("index"))

    predicted_marks = predict_marks(study_hours)
    chart_data = get_chart_data(study_hours, predicted_marks)
    metrics = load_metrics()

    return render_template(
        "result.html",
        study_hours=study_hours,
        predicted_marks=predicted_marks,
        chart_data=chart_data,
        test_accuracy=metrics.get("test", {}).get("accuracy", 0),
    )


if __name__ == "__main__":
    ensure_model()
    app.run(debug=True, host="0.0.0.0", port=5000)
