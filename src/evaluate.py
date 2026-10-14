"""Comprehensive model evaluation, confusion matrix generation, and feature importance reporting."""

import os
import json
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from sklearn.metrics import confusion_matrix, classification_report, accuracy_score, f1_score

from src.config import (
    FIGURES_DIR,
    METRICS_PATH,
    NUMERIC_FEATURES,
    CLASS_NAMES,
)
from src.data_loader import get_train_test_split
from src.predict import SoilPredictor


def run_evaluation_suite():
    """Run thorough evaluation of the champion pipeline on held-out test data."""
    print("=" * 60)
    print("📊 Soil-Sense Model Evaluation Suite")
    print("=" * 60)

    # 1. Initialize verified predictor
    predictor = SoilPredictor()
    pipeline = predictor._pipeline
    classes = predictor._classes

    # 2. Load held-out test set
    _, X_test, _, y_test = get_train_test_split()
    print(f"[INFO] Evaluating champion pipeline on {len(X_test)} untouched test samples...")

    y_pred = pipeline.predict(X_test)

    # 3. Compute Metrics
    acc = accuracy_score(y_test, y_pred)
    f1_macro = f1_score(y_test, y_pred, average="macro")
    clf_rep = classification_report(y_test, y_pred, output_dict=True)

    print(f"➔ Test Accuracy:   {acc:.4f} ({acc * 100:.2f}%)")
    print(f"➔ Macro F1-Score:  {f1_macro:.4f}")

    os.makedirs(FIGURES_DIR, exist_ok=True)

    # 4. Confusion Matrix Plot
    cm = confusion_matrix(y_test, y_pred, labels=classes)
    plt.figure(figsize=(7, 6))
    sns.heatmap(
        cm,
        annot=True,
        fmt="d",
        cmap="Blues",
        xticklabels=classes,
        yticklabels=classes,
        cbar=True,
    )
    plt.title("Confusion Matrix - Soil Fertility Prediction", fontsize=14, pad=15)
    plt.xlabel("Predicted Label", fontsize=12)
    plt.ylabel("True Label", fontsize=12)
    plt.tight_layout()

    cm_path = FIGURES_DIR / "confusion_matrix.png"
    plt.savefig(cm_path, dpi=300)
    plt.close()
    print(f"[FIGURE] Confusion matrix saved to: {cm_path}")

    # 5. Feature Importance Analysis
    classifier = pipeline.named_steps.get("classifier")
    feat_imp_path = None
    if hasattr(classifier, "feature_importances_"):
        importances = classifier.feature_importances_
        indices = np.argsort(importances)[::-1]
        ranked_feats = [NUMERIC_FEATURES[i] for i in indices]
        ranked_imps = [importances[i] for i in indices]

        plt.figure(figsize=(9, 5))
        bars = plt.barh(ranked_feats[::-1], ranked_imps[::-1], color="#10B981")
        plt.title("Feature Importance Ranking (Gini Impurity Reduction)", fontsize=14, pad=15)
        plt.xlabel("Relative Importance Score", fontsize=12)
        plt.tight_layout()

        feat_imp_path = FIGURES_DIR / "feature_importance.png"
        plt.savefig(feat_imp_path, dpi=300)
        plt.close()
        print(f"[FIGURE] Feature importance plot saved to: {feat_imp_path}")

    # 6. Generate Markdown Documentation
    doc_path = os.path.join(os.path.dirname(FIGURES_DIR), "..", "docs", "MODEL_EVALUATION.md")
    with open(doc_path, "w") as f:
        f.write("# Soil-Sense Model Evaluation & Benchmark Results\n\n")
        f.write("## 1. Executive Metrics\n")
        f.write(f"- **Overall Test Accuracy**: `{acc * 100:.2f}%`\n")
        f.write(f"- **Macro-Averaged F1-Score**: `{f1_macro:.4f}`\n\n")
        f.write("## 2. Per-Class Performance Breakdown\n\n")
        f.write("| Class | Precision | Recall | F1-Score | Support |\n")
        f.write("| :--- | :--- | :--- | :--- | :--- |\n")
        for cls in classes:
            metrics = clf_rep.get(cls, {})
            f.write(
                f"| **{cls}** | {metrics.get('precision', 0):.4f} | {metrics.get('recall', 0):.4f} | {metrics.get('f1-score', 0):.4f} | {metrics.get('support', 0)} |\n"
            )
        f.write(
            f"| **Macro Avg** | {clf_rep['macro avg']['precision']:.4f} | {clf_rep['macro avg']['recall']:.4f} | {clf_rep['macro avg']['f1-score']:.4f} | {len(y_test)} |\n"
        )
        f.write("\n## 3. Evaluation Artifacts\n")
        f.write(f"- Confusion Matrix saved at `reports/figures/confusion_matrix.png`\n")
        if feat_imp_path:
            f.write(f"- Feature Importances saved at `reports/figures/feature_importance.png`\n")

    print(f"[DOC] Evaluation summary updated in docs/MODEL_EVALUATION.md")
    print("=" * 60)


if __name__ == "__main__":
    run_evaluation_suite()
