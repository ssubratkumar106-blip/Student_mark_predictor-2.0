"""CLI prediction script."""

import argparse
import os
import sys

import joblib
import numpy as np

MODEL_PATH = os.path.join("model", "linear_regression.pkl")


def predict_marks(study_hours: float) -> float:
    """Predict marks for given study hours."""
    if not os.path.exists(MODEL_PATH):
        print("Model not found. Run: python train_model.py")
        sys.exit(1)

    if study_hours <= 0 or study_hours > 24:
        raise ValueError("Study hours must be between 0 and 24.")

    model = joblib.load(MODEL_PATH)
    value = float(model.predict(np.array([[study_hours]]))[0])
    return round(float(np.clip(value, 0, 100)), 2)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Predict marks from study hours.")
    parser.add_argument("hours", type=float, help="Study hours (0-24)")
    args = parser.parse_args()

    try:
        marks = predict_marks(args.hours)
        print(f"Study Hours    : {args.hours}")
        print(f"Predicted Marks: {marks}")
    except ValueError as error:
        print(f"Error: {error}")
        sys.exit(1)
