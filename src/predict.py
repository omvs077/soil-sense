"""Prediction engine with cryptographic integrity verification and agronomic diagnosis."""

import os
import json
import hashlib
from typing import Dict, Any, List
import joblib
import pandas as pd
import numpy as np

from src.config import (
    MODEL_PATH,
    CHECKSUM_PATH,
    NUMERIC_FEATURES,
    OPTIMAL_AGRONOMIC_RANGES,
    FEATURE_BOUNDS,
)
from src.validator import SoilSampleInput, validate_sample_dict


class SecurityError(Exception):
    """Raised when model integrity or security validation fails."""
    pass


class SoilPredictor:
    """Predictor with SHA-256 integrity verification, probabilistic confidence,

    and agronomic diagnostic heuristics.
    """

    def __init__(self, model_path: str = None, checksum_path: str = None):
        self.model_path = model_path or MODEL_PATH
        self.checksum_path = checksum_path or CHECKSUM_PATH
        self._pipeline = None
        self._classes = None
        self._load_and_verify_model()

    def _load_and_verify_model(self):
        """Verify SHA-256 integrity digest before loading pipeline (CWE-502 remediation)."""
        if not os.path.exists(self.model_path):
            raise FileNotFoundError(
                f"Model file not found at: {self.model_path}. Train the model first via 'python -m src.train'."
            )

        if not os.path.exists(self.checksum_path):
            raise SecurityError(
                f"Missing security checksum manifest at {self.checksum_path}. Untrusted model loading blocked."
            )

        with open(self.checksum_path, "r") as f:
            manifest = json.load(f)

        expected_hash = manifest.get("sha256")
        sha256 = hashlib.sha256()
        with open(self.model_path, "rb") as f:
            while chunk := f.read(8192):
                sha256.update(chunk)
        actual_hash = sha256.hexdigest()

        if actual_hash != expected_hash:
            raise SecurityError(
                f"Cryptographic integrity mismatch!\nExpected: {expected_hash}\nActual:   {actual_hash}\n"
                "Model file may have been modified or tampered with."
            )

        # Hash matches -> safe to deserialize
        self._pipeline = joblib.load(self.model_path)
        self._classes = list(self._pipeline.classes_)

    def generate_agronomic_diagnosis(self, sample_dict: Dict[str, float]) -> List[Dict[str, str]]:
        """Evaluate input features against ICAR/FAO agronomic bands to generate targeted advice."""
        diagnostics = []

        # 1. Nitrogen (N)
        n_val = sample_dict["N"]
        n_min, n_max = OPTIMAL_AGRONOMIC_RANGES["N"]
        if n_val < n_min:
            diagnostics.append(
                {
                    "parameter": "Nitrogen (N)",
                    "status": "Deficient",
                    "severity": "high",
                    "observation": f"Current {n_val:.1f} mg/kg is below optimal ({n_min}-{n_max} mg/kg).",
                    "recommendation": "Incorporate well-rotted farmyard manure (FYM), compost, or targeted split-dose urea/ammonium nitrate.",
                }
            )
        elif n_val > n_max:
            diagnostics.append(
                {
                    "parameter": "Nitrogen (N)",
                    "status": "Excessive",
                    "severity": "medium",
                    "observation": f"Current {n_val:.1f} mg/kg exceeds target upper boundary ({n_max} mg/kg).",
                    "recommendation": "Halt nitrogenous top-dressing; excessive N causes lodging and pest vulnerability.",
                }
            )

        # 2. Phosphorus (P)
        p_val = sample_dict["P"]
        p_min, p_max = OPTIMAL_AGRONOMIC_RANGES["P"]
        if p_val < p_min:
            diagnostics.append(
                {
                    "parameter": "Phosphorus (P)",
                    "status": "Deficient",
                    "severity": "high",
                    "observation": f"Current {p_val:.1f} mg/kg is low (optimal: {p_min}-{p_max} mg/kg).",
                    "recommendation": "Apply single superphosphate (SSP) or rock phosphate; consider phosphorus-solubilizing bacteria (PSB).",
                }
            )

        # 3. Potassium (K)
        k_val = sample_dict["K"]
        k_min, k_max = OPTIMAL_AGRONOMIC_RANGES["K"]
        if k_val < k_min:
            diagnostics.append(
                {
                    "parameter": "Potassium (K)",
                    "status": "Deficient",
                    "severity": "medium",
                    "observation": f"Current {k_val:.1f} mg/kg is below target ({k_min}-{k_max} mg/kg).",
                    "recommendation": "Supplement with muriate of potash (MOP) or wood ash to bolster stalk strength and drought resilience.",
                }
            )

        # 4. pH Reaction
        ph_val = sample_dict["pH"]
        ph_min, ph_max = OPTIMAL_AGRONOMIC_RANGES["pH"]
        if ph_val < 5.5:
            diagnostics.append(
                {
                    "parameter": "Soil pH",
                    "status": "Strongly Acidic",
                    "severity": "high",
                    "observation": f"pH {ph_val:.2f} inhibits nutrient availability and risks Al toxicity.",
                    "recommendation": "Apply agricultural lime (calcium carbonate) or dolomite to neutralize acidity.",
                }
            )
        elif ph_val > 8.2:
            diagnostics.append(
                {
                    "parameter": "Soil pH",
                    "status": "Alkaline / Sodic",
                    "severity": "high",
                    "observation": f"pH {ph_val:.2f} locks up micronutrients (Fe, Zn, Mn).",
                    "recommendation": "Apply agricultural gypsum ($CaSO_4$) followed by leaching; add organic sulfur/press mud.",
                }
            )

        # 5. Salinity (EC)
        ec_val = sample_dict["EC"]
        if ec_val > 2.0:
            diagnostics.append(
                {
                    "parameter": "Salinity (EC)",
                    "status": "Elevated Salinity",
                    "severity": "high",
                    "observation": f"EC {ec_val:.2f} dS/m creates osmotic stress, restricting plant water uptake.",
                    "recommendation": "Improve field drainage, leach root zones with fresh irrigation water, and avoid saline fertilizers.",
                }
            )

        # 6. Moisture
        m_val = sample_dict["Moisture"]
        if m_val < 20.0:
            diagnostics.append(
                {
                    "parameter": "Soil Moisture",
                    "status": "Moisture Deficit",
                    "severity": "medium",
                    "observation": f"Moisture at {m_val:.1f}% approaches crop wilting point.",
                    "recommendation": "Initiate irrigation schedule; implement crop residue mulching to retard evaporative loss.",
                }
            )
        elif m_val > 75.0:
            diagnostics.append(
                {
                    "parameter": "Soil Moisture",
                    "status": "Waterlogged",
                    "severity": "medium",
                    "observation": f"Moisture at {m_val:.1f}% indicates anaerobic soil saturation.",
                    "recommendation": "Clear drainage furrows to prevent root rot and denitrification.",
                }
            )

        if not diagnostics:
            diagnostics.append(
                {
                    "parameter": "General Balance",
                    "status": "Optimal Equilibrium",
                    "severity": "low",
                    "observation": "All parameters reside within healthy agronomic tolerance windows.",
                    "recommendation": "Maintain regular organic carbon cycles and soil conservation practices.",
                }
            )

        return diagnostics

    def predict_single(self, sample_input: SoilSampleInput) -> Dict[str, Any]:
        """Perform verified prediction with confidence probabilities and agronomic diagnosis."""
        df_input = sample_input.to_dataframe()
        raw_dict = {col: getattr(sample_input, col) for col in NUMERIC_FEATURES}

        pred_class = self._pipeline.predict(df_input)[0]

        # Probabilities
        if hasattr(self._pipeline, "predict_proba"):
            probs = self._pipeline.predict_proba(df_input)[0]
            prob_dict = {cls: float(prob) for cls, prob in zip(self._classes, probs)}
            confidence = float(np.max(probs))
        else:
            prob_dict = {pred_class: 1.0}
            confidence = 1.0

        diagnostics = self.generate_agronomic_diagnosis(raw_dict)

        # Normalized index (0 to 100 scale relative to optimal midpoint for radar/visuals)
        normalized_metrics = {}
        for feat in NUMERIC_FEATURES:
            val = raw_dict[feat]
            opt_min, opt_max = OPTIMAL_AGRONOMIC_RANGES[feat]
            midpoint = (opt_min + opt_max) / 2.0
            # Score: 100 if at midpoint, down towards 0 as it departs
            bound_min = FEATURE_BOUNDS[feat]["min"]
            bound_max = FEATURE_BOUNDS[feat]["max"]
            spread = max(midpoint - bound_min, bound_max - midpoint)
            score = max(0.0, min(100.0, 100.0 - (abs(val - midpoint) / spread) * 100.0))
            normalized_metrics[feat] = round(score, 1)

        return {
            "fertility_class": pred_class,
            "confidence": confidence,
            "probabilities": prob_dict,
            "diagnostics": diagnostics,
            "normalized_metrics": normalized_metrics,
            "input_values": raw_dict,
        }

    def predict_batch(self, df_samples: pd.DataFrame) -> pd.DataFrame:
        """Batch prediction on validated DataFrame."""
        df_feats = df_samples[NUMERIC_FEATURES]
        preds = self._pipeline.predict(df_feats)
        df_out = df_samples.copy()
        df_out["Predicted_Fertility"] = preds

        if hasattr(self._pipeline, "predict_proba"):
            probs = self._pipeline.predict_proba(df_feats)
            df_out["Confidence"] = np.max(probs, axis=1).round(3)
            for i, cls in enumerate(self._classes):
                df_out[f"Prob_{cls}"] = probs[:, i].round(3)

        return df_out
