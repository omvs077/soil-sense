"""Configuration, paths, constants, and agronomic thresholds for Soil-Sense."""

import os
from pathlib import Path

# Base Paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_PATH = DATA_DIR / "raw" / "soil_fertility_dataset.csv"
PROCESSED_DATA_PATH = DATA_DIR / "processed" / "soil_fertility_clean.csv"

MODELS_DIR = PROJECT_ROOT / "models"
MODEL_PATH = MODELS_DIR / "soil_fertility_pipeline.pkl"
CHECKSUM_PATH = MODELS_DIR / "model_checksum.json"

REPORTS_DIR = PROJECT_ROOT / "reports"
FIGURES_DIR = REPORTS_DIR / "figures"
METRICS_PATH = REPORTS_DIR / "model_comparison_metrics.json"

# Features and Target
NUMERIC_FEATURES = [
    "N",
    "P",
    "K",
    "pH",
    "EC",
    "Moisture",
    "Temperature",
    "Humidity",
]

TARGET_COLUMN = "Fertility"
CLASS_NAMES = ["Low", "Medium", "High"]
CLASS_MAPPING = {"Low": 0, "Medium": 1, "High": 2}
REVERSE_CLASS_MAPPING = {0: "Low", 1: "Medium", 2: "High"}

# Random seed for reproducible experiments
RANDOM_STATE = 42

# Agronomic Valid Ranges (Strict Bounds for Input Sanitization)
FEATURE_BOUNDS = {
    "N": {"min": 0.0, "max": 500.0, "unit": "mg/kg", "default": 160.0, "step": 1.0},
    "P": {"min": 0.0, "max": 250.0, "unit": "mg/kg", "default": 22.0, "step": 1.0},
    "K": {"min": 0.0, "max": 600.0, "unit": "mg/kg", "default": 180.0, "step": 1.0},
    "pH": {"min": 3.0, "max": 11.0, "unit": "pH", "default": 6.8, "step": 0.1},
    "EC": {"min": 0.0, "max": 15.0, "unit": "dS/m", "default": 0.8, "step": 0.05},
    "Moisture": {"min": 0.0, "max": 100.0, "unit": "%", "default": 35.0, "step": 0.5},
    "Temperature": {"min": -5.0, "max": 55.0, "unit": "°C", "default": 26.0, "step": 0.5},
    "Humidity": {"min": 5.0, "max": 100.0, "unit": "%", "default": 65.0, "step": 1.0},
}

# Optimal Agronomic Target Bands (Used for Diagnostic Radar & Corrective Advice)
OPTIMAL_AGRONOMIC_RANGES = {
    "N": (140.0, 280.0),
    "P": (15.0, 30.0),
    "K": (130.0, 280.0),
    "pH": (6.2, 7.5),
    "EC": (0.0, 1.2),
    "Moisture": (25.0, 60.0),
    "Temperature": (18.0, 32.0),
    "Humidity": (50.0, 80.0),
}

# Soil Presets for Instant UI Testing
SOIL_PRESETS = {
    "Rich Alluvial Loam (High Fertility)": {
        "N": 230.0,
        "P": 28.0,
        "K": 220.0,
        "pH": 6.8,
        "EC": 0.65,
        "Moisture": 42.0,
        "Temperature": 25.0,
        "Humidity": 70.0,
    },
    "Standard Black Cotton Soil (Medium Fertility)": {
        "N": 145.0,
        "P": 14.0,
        "K": 160.0,
        "pH": 7.9,
        "EC": 1.15,
        "Moisture": 28.0,
        "Temperature": 29.0,
        "Humidity": 55.0,
    },
    "Degraded / Acidic Sandy Soil (Low Fertility)": {
        "N": 45.0,
        "P": 6.0,
        "K": 60.0,
        "pH": 4.8,
        "EC": 2.8,
        "Moisture": 14.0,
        "Temperature": 36.0,
        "Humidity": 30.0,
    },
    "Saline / Sodic Alkaline Soil (Low Fertility)": {
        "N": 80.0,
        "P": 9.0,
        "K": 95.0,
        "pH": 8.9,
        "EC": 3.6,
        "Moisture": 18.0,
        "Temperature": 32.0,
        "Humidity": 40.0,
    },
}
