"""Model training, cross-validation, comparison, and secure serialization."""

import os
import json
import hashlib
from datetime import datetime
import joblib
import pandas as pd
import numpy as np

from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import StratifiedKFold, cross_validate
from sklearn.metrics import classification_report, accuracy_score, f1_score

from src.config import (
    MODEL_PATH,
    CHECKSUM_PATH,
    METRICS_PATH,
    RANDOM_STATE,
    NUMERIC_FEATURES,
    CLASS_NAMES,
)
from src.data_loader import get_train_test_split


def compute_sha256(filepath: str) -> str:
    """Compute cryptographic SHA-256 checksum of a file."""
    sha256 = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(8192):
            sha256.update(chunk)
    return sha256.hexdigest()


def build_candidate_pipelines() -> dict:
    """Instantiate candidate classification pipelines with encapsulated preprocessing to prevent data leakage."""
    return {
        "Decision Tree": Pipeline(
            [
                ("imputer", SimpleImputer(strategy="median")),
                ("scaler", StandardScaler()),
                (
                    "classifier",
                    DecisionTreeClassifier(
                        max_depth=6,
                        min_samples_split=8,
                        random_state=RANDOM_STATE,
                        class_weight="balanced",
                    ),
                ),
            ]
        ),
        "K-Nearest Neighbors": Pipeline(
            [
                ("imputer", SimpleImputer(strategy="median")),
                ("scaler", StandardScaler()),
                (
                    "classifier",
                    KNeighborsClassifier(n_neighbors=7, weights="distance"),
                ),
            ]
        ),
        "Random Forest": Pipeline(
            [
                ("imputer", SimpleImputer(strategy="median")),
                ("scaler", StandardScaler()),
                (
                    "classifier",
                    RandomForestClassifier(
                        n_estimators=120,
                        max_depth=12,
                        min_samples_leaf=2,
                        random_state=RANDOM_STATE,
                        class_weight="balanced",
                        n_jobs=-1,
                    ),
                ),
            ]
        ),
    }


def train_and_evaluate_all():
    """Train candidates, compare cross-validated metrics, save the champion model with SHA-256 checksum."""
    print("=" * 60)
    print("[SOIL-SENSE] ML Pipeline Training & Verification Engine")
    print("=" * 60)

    X_train, X_test, y_train, y_test = get_train_test_split()
    print(
        f"[INFO] Training set: {len(X_train)} samples | Test set: {len(X_test)} samples"
    )

    pipelines = build_candidate_pipelines()
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=RANDOM_STATE)

    results = {}
    best_name = None
    best_f1 = -1.0
    champion_pipeline = None

    for name, pipe in pipelines.items():
        print(f"\n[TRAINING] Evaluating {name}...")
        cv_scores = cross_validate(
            pipe,
            X_train,
            y_train,
            cv=cv,
            scoring=["accuracy", "f1_macro", "precision_macro", "recall_macro"],
            return_train_score=False,
        )

        # Fit on full training set and evaluate on test set
        pipe.fit(X_train, y_train)
        y_pred = pipe.predict(X_test)
        test_acc = float(accuracy_score(y_test, y_pred))
        test_f1 = float(f1_score(y_test, y_pred, average="macro"))

        results[name] = {
            "cv_accuracy_mean": float(np.mean(cv_scores["test_accuracy"])),
            "cv_accuracy_std": float(np.std(cv_scores["test_accuracy"])),
            "cv_f1_macro_mean": float(np.mean(cv_scores["test_f1_macro"])),
            "cv_f1_macro_std": float(np.std(cv_scores["test_f1_macro"])),
            "test_accuracy": test_acc,
            "test_f1_macro": test_f1,
            "classification_report": classification_report(
                y_test, y_pred, output_dict=True
            ),
        }

        print(
            f"   -> CV Macro F1: {results[name]['cv_f1_macro_mean']:.4f} (+/- {results[name]['cv_f1_macro_std']:.4f})"
        )
        print(
            f"   -> Test Accuracy: {test_acc:.4f} | Test Macro F1: {test_f1:.4f}"
        )

        if test_f1 > best_f1:
            best_f1 = test_f1
            best_name = name
            champion_pipeline = pipe

    print("\n" + "=" * 60)
    print(f"[CHAMPION] Model Selected: {best_name} (Macro F1 = {best_f1:.4f})")
    print("=" * 60)

    # Save metrics report
    os.makedirs(os.path.dirname(METRICS_PATH), exist_ok=True)
    with open(METRICS_PATH, "w") as f:
        json.dump(
            {
                "timestamp": datetime.now().isoformat(),
                "champion_model": best_name,
                "comparison": results,
            },
            f,
            indent=2,
        )
    print(f"[INFO] Comparison metrics saved to: {METRICS_PATH}")

    # Persist champion pipeline
    os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
    joblib.dump(champion_pipeline, MODEL_PATH)
    print(f"[INFO] Pipeline persisted to: {MODEL_PATH}")

    # Compute & write SHA-256 checksum for CWE-502 tamper protection
    model_hash = compute_sha256(MODEL_PATH)
    checksum_payload = {
        "model_file": os.path.basename(MODEL_PATH),
        "sha256": model_hash,
        "algorithm": best_name,
        "features": NUMERIC_FEATURES,
        "classes": list(champion_pipeline.classes_),
        "generated_at": datetime.now().isoformat(),
        "test_f1_macro": best_f1,
    }
    with open(CHECKSUM_PATH, "w") as f:
        json.dump(checksum_payload, f, indent=2)
    print(f"[SECURITY] Checksum manifest written to: {CHECKSUM_PATH}")
    print(f"[SECURITY] SHA-256 Digest: {model_hash}")

    return best_name, results


if __name__ == "__main__":
    train_and_evaluate_all()
