"""Unit tests for the prediction engine, cryptographic checksums, and reproducibility."""

import os
import json
import pytest
from src.predict import SoilPredictor, SecurityError
from src.validator import SoilSampleInput
from src.config import CHECKSUM_PATH, MODEL_PATH


def test_prediction_output_format():
    """Verify that prediction produces expected classes, confidence, and diagnostics."""
    if not os.path.exists(MODEL_PATH):
        pytest.skip("Model artifact not yet trained. Run src.train first.")

    predictor = SoilPredictor()
    sample = SoilSampleInput(
        N=210.0,
        P=26.0,
        K=220.0,
        pH=6.8,
        EC=0.7,
        Moisture=40.0,
        Temperature=25.0,
        Humidity=70.0,
    )
    result = predictor.predict_single(sample)

    assert result["fertility_class"] in ["Low", "Medium", "High"]
    assert 0.0 <= result["confidence"] <= 1.0
    assert len(result["probabilities"]) == 3
    assert pytest.approx(sum(result["probabilities"].values()), abs=1e-3) == 1.0
    assert len(result["diagnostics"]) > 0
    assert "normalized_metrics" in result


def test_security_tamper_detection(tmp_path):
    """Verify that tampering with model file or checksum raises SecurityError."""
    if not os.path.exists(MODEL_PATH):
        pytest.skip("Model artifact not yet trained.")

    # Create dummy checksum with mismatched hash
    fake_checksum = tmp_path / "fake_checksum.json"
    fake_payload = {
        "model_file": "soil_fertility_pipeline.pkl",
        "sha256": "0000000000000000000000000000000000000000000000000000000000000000",
    }
    with open(fake_checksum, "w") as f:
        json.dump(fake_payload, f)

    with pytest.raises(SecurityError) as exc_info:
        SoilPredictor(model_path=str(MODEL_PATH), checksum_path=str(fake_checksum))
    assert "Cryptographic integrity mismatch" in str(exc_info.value)
