"""Generate rich, realistic demo CSV datasets for batch screening testing."""

import os
import pandas as pd
import numpy as np

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "docs", "demo_datasets")
os.makedirs(OUTPUT_DIR, exist_ok=True)


def generate_mixed_survey(n=25):
    """Mixed agricultural zone survey (mix of High, Medium, and Low fertility)."""
    np.random.seed(101)
    rows = []

    # 10 High fertility samples
    for _ in range(10):
        rows.append({
            "N": round(float(np.random.normal(235, 25)), 1),
            "P": round(float(np.random.normal(28, 4)), 1),
            "K": round(float(np.random.normal(230, 30)), 1),
            "pH": round(float(np.random.normal(6.8, 0.3)), 2),
            "EC": round(float(np.random.normal(0.65, 0.15)), 2),
            "Moisture": round(float(np.random.normal(42, 6)), 1),
            "Temperature": round(float(np.random.normal(25, 3)), 1),
            "Humidity": round(float(np.random.normal(68, 7)), 1),
        })

    # 8 Medium fertility samples
    for _ in range(8):
        rows.append({
            "N": round(float(np.random.normal(150, 20)), 1),
            "P": round(float(np.random.normal(16, 3)), 1),
            "K": round(float(np.random.normal(155, 25)), 1),
            "pH": round(float(np.random.choice([6.0, 7.8]) + np.random.normal(0, 0.2)), 2),
            "EC": round(float(np.random.normal(1.25, 0.25)), 2),
            "Moisture": round(float(np.random.normal(30, 5)), 1),
            "Temperature": round(float(np.random.normal(28, 3)), 1),
            "Humidity": round(float(np.random.normal(55, 6)), 1),
        })

    # 7 Low fertility samples
    for _ in range(7):
        rows.append({
            "N": round(float(np.random.normal(60, 18)), 1),
            "P": round(float(np.random.normal(7, 2)), 1),
            "K": round(float(np.random.normal(70, 20)), 1),
            "pH": round(float(np.random.choice([4.8, 8.8]) + np.random.normal(0, 0.3)), 2),
            "EC": round(float(np.random.normal(2.9, 0.6)), 2),
            "Moisture": round(float(np.random.normal(15, 4)), 1),
            "Temperature": round(float(np.random.normal(34, 4)), 1),
            "Humidity": round(float(np.random.normal(35, 7)), 1),
        })

    df = pd.DataFrame(rows)
    # Clip to valid boundaries
    df["N"] = df["N"].clip(5, 450)
    df["P"] = df["P"].clip(2, 200)
    df["K"] = df["K"].clip(10, 500)
    df["pH"] = df["pH"].clip(3.5, 10.5)
    df["EC"] = df["EC"].clip(0.1, 12.0)
    df["Moisture"] = df["Moisture"].clip(5, 90)
    df["Temperature"] = df["Temperature"].clip(10, 48)
    df["Humidity"] = df["Humidity"].clip(10, 95)

    df = df.sample(frac=1.0, random_state=101).reset_index(drop=True)
    out_path = os.path.join(OUTPUT_DIR, "demo_mixed_farm_survey.csv")
    df.to_csv(out_path, index=False)
    print(f"Generated {len(df)} samples -> {out_path}")


def generate_high_alluvial(n=15):
    """High fertility alluvial plains dataset."""
    np.random.seed(202)
    rows = []
    for _ in range(n):
        rows.append({
            "N": round(float(np.random.normal(245, 25)), 1),
            "P": round(float(np.random.normal(32, 5)), 1),
            "K": round(float(np.random.normal(250, 25)), 1),
            "pH": round(float(np.random.normal(6.9, 0.25)), 2),
            "EC": round(float(np.random.normal(0.55, 0.12)), 2),
            "Moisture": round(float(np.random.normal(45, 5)), 1),
            "Temperature": round(float(np.random.normal(24, 2.5)), 1),
            "Humidity": round(float(np.random.normal(72, 6)), 1),
        })
    df = pd.DataFrame(rows)
    df["N"] = df["N"].clip(160, 400)
    df["P"] = df["P"].clip(20, 100)
    df["K"] = df["K"].clip(160, 450)
    df["pH"] = df["pH"].clip(6.3, 7.6)
    df["EC"] = df["EC"].clip(0.2, 1.1)
    df["Moisture"] = df["Moisture"].clip(30, 65)
    df["Temperature"] = df["Temperature"].clip(18, 32)
    df["Humidity"] = df["Humidity"].clip(55, 90)

    out_path = os.path.join(OUTPUT_DIR, "demo_high_fertility_alluvial.csv")
    df.to_csv(out_path, index=False)
    print(f"Generated {len(df)} samples -> {out_path}")


def generate_degraded_saline(n=15):
    """Degraded, saline, and sodic soil samples."""
    np.random.seed(303)
    rows = []
    for _ in range(n):
        rows.append({
            "N": round(float(np.random.normal(65, 15)), 1),
            "P": round(float(np.random.normal(8, 2)), 1),
            "K": round(float(np.random.normal(75, 18)), 1),
            "pH": round(float(np.random.normal(8.7, 0.35)), 2),
            "EC": round(float(np.random.normal(3.4, 0.6)), 2),
            "Moisture": round(float(np.random.normal(16, 4)), 1),
            "Temperature": round(float(np.random.normal(35, 3.5)), 1),
            "Humidity": round(float(np.random.normal(32, 6)), 1),
        })
    df = pd.DataFrame(rows)
    df["N"] = df["N"].clip(15, 120)
    df["P"] = df["P"].clip(2, 14)
    df["K"] = df["K"].clip(25, 110)
    df["pH"] = df["pH"].clip(8.1, 9.8)
    df["EC"] = df["EC"].clip(2.2, 6.5)
    df["Moisture"] = df["Moisture"].clip(8, 25)
    df["Temperature"] = df["Temperature"].clip(26, 45)
    df["Humidity"] = df["Humidity"].clip(15, 50)

    out_path = os.path.join(OUTPUT_DIR, "demo_degraded_saline_alkaline.csv")
    df.to_csv(out_path, index=False)
    print(f"Generated {len(df)} samples -> {out_path}")


def generate_acidic_laterite(n=15):
    """Acidic laterite / hill soil samples."""
    np.random.seed(404)
    rows = []
    for _ in range(n):
        rows.append({
            "N": round(float(np.random.normal(75, 18)), 1),
            "P": round(float(np.random.normal(5, 1.5)), 1),
            "K": round(float(np.random.normal(65, 16)), 1),
            "pH": round(float(np.random.normal(4.7, 0.3)), 2),
            "EC": round(float(np.random.normal(0.45, 0.1)), 2),
            "Moisture": round(float(np.random.normal(26, 6)), 1),
            "Temperature": round(float(np.random.normal(26, 3)), 1),
            "Humidity": round(float(np.random.normal(78, 8)), 1),
        })
    df = pd.DataFrame(rows)
    df["N"] = df["N"].clip(20, 130)
    df["P"] = df["P"].clip(1, 10)
    df["K"] = df["K"].clip(20, 110)
    df["pH"] = df["pH"].clip(4.0, 5.3)
    df["EC"] = df["EC"].clip(0.1, 0.9)
    df["Moisture"] = df["Moisture"].clip(15, 50)
    df["Temperature"] = df["Temperature"].clip(18, 35)
    df["Humidity"] = df["Humidity"].clip(50, 95)

    out_path = os.path.join(OUTPUT_DIR, "demo_acidic_laterite_hill.csv")
    df.to_csv(out_path, index=False)
    print(f"Generated {len(df)} samples -> {out_path}")


if __name__ == "__main__":
    generate_mixed_survey()
    generate_high_alluvial()
    generate_degraded_saline()
    generate_acidic_laterite()
