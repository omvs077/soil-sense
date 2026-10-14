"""Unit tests for input validation and sanitization schemas."""

import pytest
import pandas as pd
from src.validator import SoilSampleInput, validate_sample_dict, validate_batch_dataframe


def test_valid_soil_sample():
    """Verify that a valid soil sample passes schema validation."""
    valid_data = {
        "N": 160.0,
        "P": 25.0,
        "K": 180.0,
        "pH": 6.8,
        "EC": 0.85,
        "Moisture": 35.0,
        "Temperature": 26.0,
        "Humidity": 65.0,
    }
    sample = SoilSampleInput(**valid_data)
    assert sample.N == 160.0
    assert sample.pH == 6.8

    df = sample.to_dataframe()
    assert len(df) == 1
    assert list(df.columns) == ["N", "P", "K", "pH", "EC", "Moisture", "Temperature", "Humidity"]


def test_invalid_ph_out_of_bounds():
    """Verify that pH outside 3.0-11.0 is rejected."""
    bad_data = {
        "N": 160.0,
        "P": 25.0,
        "K": 180.0,
        "pH": 15.5,  # Exceeds max
        "EC": 0.85,
        "Moisture": 35.0,
        "Temperature": 26.0,
        "Humidity": 65.0,
    }
    with pytest.raises(Exception):
        SoilSampleInput(**bad_data)


def test_negative_nutrients_rejected():
    """Verify negative nitrogen concentration is rejected."""
    bad_data = {
        "N": -10.0,
        "P": 25.0,
        "K": 180.0,
        "pH": 6.8,
        "EC": 0.85,
        "Moisture": 35.0,
        "Temperature": 26.0,
        "Humidity": 65.0,
    }
    with pytest.raises(Exception):
        SoilSampleInput(**bad_data)


def test_non_numeric_injection_rejected():
    """Verify string injection causes validation error."""
    bad_data = {
        "N": "DROP TABLE soils",
        "P": 25.0,
        "K": 180.0,
        "pH": 6.8,
        "EC": 0.85,
        "Moisture": 35.0,
        "Temperature": 26.0,
        "Humidity": 65.0,
    }
    is_valid, sample, err = validate_sample_dict(bad_data)
    assert not is_valid
    assert sample is None
    assert "cannot be parsed as a float" in err


def test_batch_validation_success():
    """Verify batch validation accepts clean dataframe."""
    df = pd.DataFrame(
        [
            {"N": 180, "P": 20, "K": 200, "pH": 6.5, "EC": 0.7, "Moisture": 40, "Temperature": 25, "Humidity": 60},
            {"N": 70, "P": 8, "K": 80, "pH": 5.2, "EC": 2.2, "Moisture": 18, "Temperature": 32, "Humidity": 40},
        ]
    )
    is_valid, clean_df, errors = validate_batch_dataframe(df)
    assert is_valid
    assert len(clean_df) == 2
    assert len(errors) == 0


def test_batch_validation_missing_columns():
    """Verify batch validation detects missing required columns."""
    df_missing = pd.DataFrame([{"N": 180, "P": 20}])
    is_valid, _, errors = validate_batch_dataframe(df_missing)
    assert not is_valid
    assert any("Missing required columns" in e for e in errors)
