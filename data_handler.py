"""Dataset loading and preprocessing using Pandas."""

import os

import numpy as np
import pandas as pd


DATASET_PATH = os.path.join("dataset", "student_scores.csv")


def generate_dataset(path: str = DATASET_PATH, rows: int = 75) -> pd.DataFrame:
    """Generate realistic study hours vs marks dataset."""
    rng = np.random.default_rng(42)
    hours = np.round(rng.uniform(1, 9.5, rows), 1)
    marks = np.clip(12 + hours * 9.2 + rng.normal(0, 4, rows), 5, 100)
    df = pd.DataFrame({"Study_Hours": hours, "Marks": np.round(marks, 1)})
    os.makedirs(os.path.dirname(path), exist_ok=True)
    df.to_csv(path, index=False)
    return df


def load_dataset(path: str = DATASET_PATH) -> pd.DataFrame:
    """Load dataset from CSV or create if missing."""
    if not os.path.exists(path):
        return generate_dataset(path)
    return pd.read_csv(path)


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Clean dataset: missing values, duplicates, invalid ranges."""
    data = df.copy()
    data["Study_Hours"] = pd.to_numeric(data["Study_Hours"], errors="coerce")
    data["Marks"] = pd.to_numeric(data["Marks"], errors="coerce")
    data = data.dropna()
    data = data.drop_duplicates()
    data = data[(data["Study_Hours"] > 0) & (data["Study_Hours"] <= 24)]
    data = data[(data["Marks"] >= 0) & (data["Marks"] <= 100)]
    return data.reset_index(drop=True)
