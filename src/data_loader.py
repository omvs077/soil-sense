"""Data Ingestion, Benchmark Generation, and Preprocessing for Soil-Sense."""

import os
import numpy as np
import pandas as pd
from typing import Tuple
from src.config import (
    RAW_DATA_PATH,
    PROCESSED_DATA_PATH,
    NUMERIC_FEATURES,
    TARGET_COLUMN,
    RANDOM_STATE,
)


def generate_benchmark_dataset(
    n_samples: int = 1800, output_path: str = None
) -> pd.DataFrame:
    """Generate a scientifically calibrated, realistic soil benchmark dataset

    aligned with ICAR/FAO soil fertility thresholds and natural covariance.
    """
    np.random.seed(RANDOM_STATE)
    samples_per_class = n_samples // 3

    # 1. High Fertility: Balanced NPK, optimal pH (6.3-7.4), low EC (<1.2), good moisture (32-60%)
    high_n = np.random.normal(loc=230, scale=35, size=samples_per_class)
    high_p = np.random.normal(loc=28, scale=6, size=samples_per_class)
    high_k = np.random.normal(loc=240, scale=40, size=samples_per_class)
    high_ph = np.random.normal(loc=6.8, scale=0.35, size=samples_per_class)
    high_ec = np.random.normal(loc=0.65, scale=0.2, size=samples_per_class)
    high_moisture = np.random.normal(loc=44, scale=8, size=samples_per_class)
    high_temp = np.random.normal(loc=25, scale=4, size=samples_per_class)
    high_humidity = np.random.normal(loc=68, scale=9, size=samples_per_class)

    df_high = pd.DataFrame(
        {
            "N": high_n,
            "P": high_p,
            "K": high_k,
            "pH": high_ph,
            "EC": high_ec,
            "Moisture": high_moisture,
            "Temperature": high_temp,
            "Humidity": high_humidity,
            "Fertility": "High",
        }
    )

    # 2. Medium Fertility: Moderate nutrient levels, slight pH deviation, moderate EC
    med_n = np.random.normal(loc=150, scale=30, size=samples_per_class)
    med_p = np.random.normal(loc=16, scale=5, size=samples_per_class)
    med_k = np.random.normal(loc=155, scale=35, size=samples_per_class)
    # Bimodal or slightly offset pH
    med_ph = np.random.choice([5.9, 7.8], size=samples_per_class) + np.random.normal(
        0, 0.35, samples_per_class
    )
    med_ec = np.random.normal(loc=1.3, scale=0.35, size=samples_per_class)
    med_moisture = np.random.normal(loc=30, scale=7, size=samples_per_class)
    med_temp = np.random.normal(loc=28, scale=5, size=samples_per_class)
    med_humidity = np.random.normal(loc=55, scale=10, size=samples_per_class)

    df_med = pd.DataFrame(
        {
            "N": med_n,
            "P": med_p,
            "K": med_k,
            "pH": med_ph,
            "EC": med_ec,
            "Moisture": med_moisture,
            "Temperature": med_temp,
            "Humidity": med_humidity,
            "Fertility": "Medium",
        }
    )

    # 3. Low Fertility: Severe nutrient depletion, extreme pH (<5.3 or >8.4), salinity (EC>2.5), poor moisture
    low_n = np.random.normal(loc=65, scale=25, size=samples_per_class)
    low_p = np.random.normal(loc=7, scale=3, size=samples_per_class)
    low_k = np.random.normal(loc=75, scale=25, size=samples_per_class)
    low_ph = np.random.choice([4.9, 8.8], size=samples_per_class) + np.random.normal(
        0, 0.45, samples_per_class
    )
    low_ec = np.random.normal(loc=2.9, scale=0.8, size=samples_per_class)
    low_moisture = np.random.normal(loc=16, scale=6, size=samples_per_class)
    low_temp = np.random.normal(loc=34, scale=6, size=samples_per_class)
    low_humidity = np.random.normal(loc=35, scale=10, size=samples_per_class)

    df_low = pd.DataFrame(
        {
            "N": low_n,
            "P": low_p,
            "K": low_k,
            "pH": low_ph,
            "EC": low_ec,
            "Moisture": low_moisture,
            "Temperature": low_temp,
            "Humidity": low_humidity,
            "Fertility": "Low",
        }
    )

    df = pd.concat([df_high, df_med, df_low], ignore_index=True)

    # Physical clamping to valid boundaries
    df["N"] = df["N"].clip(lower=5.0, upper=450.0).round(1)
    df["P"] = df["P"].clip(lower=1.0, upper=180.0).round(1)
    df["K"] = df["K"].clip(lower=10.0, upper=550.0).round(1)
    df["pH"] = df["pH"].clip(lower=3.5, upper=10.5).round(2)
    df["EC"] = df["EC"].clip(lower=0.05, upper=10.0).round(2)
    df["Moisture"] = df["Moisture"].clip(lower=4.0, upper=92.0).round(1)
    df["Temperature"] = df["Temperature"].clip(lower=5.0, upper=48.0).round(1)
    df["Humidity"] = df["Humidity"].clip(lower=10.0, upper=98.0).round(1)

    # Shuffle rows
    df = df.sample(frac=1.0, random_state=RANDOM_STATE).reset_index(drop=True)

    target_path = output_path or RAW_DATA_PATH
    os.makedirs(os.path.dirname(target_path), exist_ok=True)
    df.to_csv(target_path, index=False)
    print(
        f"[INFO] Benchmark dataset generated ({len(df)} samples) saved to: {target_path}"
    )
    return df


def load_and_clean_data(file_path: str = None) -> pd.DataFrame:
    """Load soil dataset from raw path, perform hygiene checks, and save to processed directory."""
    path = file_path or RAW_DATA_PATH
    if not os.path.exists(path):
        print(f"[INFO] Raw dataset not found at '{path}'. Generating benchmark...")
        df = generate_benchmark_dataset(output_path=path)
    else:
        df = pd.read_csv(path)

    # Validate columns
    missing = [c for c in NUMERIC_FEATURES if c not in df.columns]
    if missing:
        raise ValueError(f"Dataset missing required feature columns: {missing}")
    if TARGET_COLUMN not in df.columns:
        raise ValueError(
            f"Dataset missing target column '{TARGET_COLUMN}'. Columns found: {list(df.columns)}"
        )

    # Clean data
    initial_len = len(df)
    df = df.dropna(subset=NUMERIC_FEATURES + [TARGET_COLUMN])
    df = df.drop_duplicates(subset=NUMERIC_FEATURES)

    # Standardize target labels
    df[TARGET_COLUMN] = df[TARGET_COLUMN].astype(str).str.strip().str.capitalize()
    valid_classes = {"Low", "Medium", "High"}
    df = df[df[TARGET_COLUMN].isin(valid_classes)]

    # Cast numeric columns
    for col in NUMERIC_FEATURES:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    df = df.dropna()

    os.makedirs(os.path.dirname(PROCESSED_DATA_PATH), exist_ok=True)
    df.to_csv(PROCESSED_DATA_PATH, index=False)
    print(
        f"[INFO] Cleaned dataset ({len(df)}/{initial_len} retained) saved to: {PROCESSED_DATA_PATH}"
    )
    return df


def get_train_test_split(test_size: float = 0.2) -> Tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
    """Load cleaned data and perform stratified train-test split."""
    from sklearn.model_selection import train_test_split

    df = load_and_clean_data()
    X = df[NUMERIC_FEATURES]
    y = df[TARGET_COLUMN]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=RANDOM_STATE, stratify=y
    )
    return X_train, X_test, y_train, y_test


if __name__ == "__main__":
    load_and_clean_data()
