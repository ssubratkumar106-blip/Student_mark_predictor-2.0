"""Train and evaluate Linear Regression model."""

import json
import os

import joblib
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split

from data_handler import clean_data, load_dataset

MODEL_PATH = os.path.join("model", "linear_regression.pkl")
METRICS_PATH = os.path.join("model", "metrics.json")


def train_and_save() -> dict:
    """Complete ML workflow: load, clean, train, test, save."""
    print("=" * 55)
    print("Student Marks Prediction - Model Training")
    print("=" * 55)

    df = load_dataset()
    print(f"\n[1] Dataset loaded: {len(df)} rows (Pandas)")

    df = clean_data(df)
    print(f"[2] Data cleaned: {len(df)} rows")
    print(f"    Missing values: {df.isnull().sum().sum()}")

    x = df[["Study_Hours"]].values
    y = df["Marks"].values

    x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=0.2, random_state=42
    )
    print(f"[3] Train/Test split: {len(x_train)} train, {len(x_test)} test")

    model = LinearRegression()
    model.fit(x_train, y_train)
    print("[4] Linear Regression model trained")

    y_train_pred = model.predict(x_train)
    y_test_pred = model.predict(x_test)

    def metrics(y_true, y_pred):
        mae = mean_absolute_error(y_true, y_pred)
        mse = mean_squared_error(y_true, y_pred)
        rmse = float(np.sqrt(mse))
        r2 = r2_score(y_true, y_pred)
        return {
            "mae": round(float(mae), 3),
            "mse": round(float(mse), 3),
            "rmse": round(float(rmse), 3),
            "r2_score": round(float(r2), 3),
            "accuracy": round(max(0, r2) * 100, 2),
        }

    train_metrics = metrics(y_train, y_train_pred)
    test_metrics = metrics(y_test, y_test_pred)

    print("\n--- Evaluation Metrics (Test Set) ---")
    print(f"MAE          : {test_metrics['mae']}")
    print(f"MSE          : {test_metrics['mse']}")
    print(f"RMSE         : {test_metrics['rmse']}")
    print(f"R2 Score     : {test_metrics['r2_score']}")
    print(f"Train Accuracy: {train_metrics['accuracy']}%")
    print(f"Test Accuracy : {test_metrics['accuracy']}%")

    os.makedirs("model", exist_ok=True)
    joblib.dump(model, MODEL_PATH)

    payload = {
        "train": train_metrics,
        "test": test_metrics,
        "coefficient": round(float(model.coef_[0]), 2),
        "intercept": round(float(model.intercept_), 2),
        "samples": len(df),
        "train_samples": len(x_train),
        "test_samples": len(x_test),
        "dataset_preview": df.head(8).to_dict(orient="records"),
        "train_hours": x_train.flatten().tolist(),
        "train_marks": y_train.tolist(),
    }

    with open(METRICS_PATH, "w", encoding="utf-8") as file:
        json.dump(payload, file, indent=2)

    print(f"\n[5] Model saved: {MODEL_PATH}")
    print(f"[6] Metrics saved: {METRICS_PATH}")
    print("\nTraining completed successfully!")
    return payload


if __name__ == "__main__":
    train_and_save()
