"""Input validation and sanitization schemas for Soil-Sense."""

import math
from typing import Dict, Any, List, Tuple
from pydantic import BaseModel, Field, field_validator
import pandas as pd
from src.config import FEATURE_BOUNDS, NUMERIC_FEATURES


class SoilSampleInput(BaseModel):
    """Pydantic model for validating a single soil sample measurement."""

    N: float = Field(
        ...,
        description="Available Nitrogen in mg/kg",
        ge=FEATURE_BOUNDS["N"]["min"],
        le=FEATURE_BOUNDS["N"]["max"],
    )
    P: float = Field(
        ...,
        description="Available Phosphorus in mg/kg",
        ge=FEATURE_BOUNDS["P"]["min"],
        le=FEATURE_BOUNDS["P"]["max"],
    )
    K: float = Field(
        ...,
        description="Available Potassium in mg/kg",
        ge=FEATURE_BOUNDS["K"]["min"],
        le=FEATURE_BOUNDS["K"]["max"],
    )
    pH: float = Field(
        ...,
        description="Soil pH level (0-14)",
        ge=FEATURE_BOUNDS["pH"]["min"],
        le=FEATURE_BOUNDS["pH"]["max"],
    )
    EC: float = Field(
        ...,
        description="Electrical Conductivity in dS/m",
        ge=FEATURE_BOUNDS["EC"]["min"],
        le=FEATURE_BOUNDS["EC"]["max"],
    )
    Moisture: float = Field(
        ...,
        description="Soil moisture percentage (0-100%)",
        ge=FEATURE_BOUNDS["Moisture"]["min"],
        le=FEATURE_BOUNDS["Moisture"]["max"],
    )
    Temperature: float = Field(
        ...,
        description="Ambient temperature in °C",
        ge=FEATURE_BOUNDS["Temperature"]["min"],
        le=FEATURE_BOUNDS["Temperature"]["max"],
    )
    Humidity: float = Field(
        ...,
        description="Relative humidity percentage (0-100%)",
        ge=FEATURE_BOUNDS["Humidity"]["min"],
        le=FEATURE_BOUNDS["Humidity"]["max"],
    )

    @field_validator("*", mode="before")
    @classmethod
    def check_finite_numeric(cls, v: Any) -> float:
        """Reject non-numeric, NaN, infinite, or None values."""
        if v is None:
            raise ValueError("Input value cannot be null/None.")
        try:
            val = float(v)
        except (ValueError, TypeError):
            raise ValueError(f"Value '{v}' cannot be parsed as a float.")
        if math.isnan(val) or math.isinf(val):
            raise ValueError("Value cannot be NaN or infinite.")
        return val

    def to_dataframe(self) -> pd.DataFrame:
        """Convert sample to single-row pandas DataFrame ordered by NUMERIC_FEATURES."""
        data = {col: [getattr(self, col)] for col in NUMERIC_FEATURES}
        return pd.DataFrame(data)


def validate_sample_dict(data: Dict[str, Any]) -> Tuple[bool, Any, str]:
    """Validate a dictionary of measurements.

    Returns:
        (is_valid, validated_model_or_none, error_message)
    """
    try:
        sample = SoilSampleInput(**data)
        return True, sample, ""
    except Exception as e:
        return False, None, str(e)


def validate_batch_dataframe(df: pd.DataFrame) -> Tuple[bool, pd.DataFrame, List[str]]:
    """Validate a batch dataframe uploaded via CSV.

    Ensures all NUMERIC_FEATURES exist and values conform to boundaries.
    Returns:
        (is_valid, clean_df, errors_list)
    """
    errors = []
    missing_cols = [col for col in NUMERIC_FEATURES if col not in df.columns]
    if missing_cols:
        return False, df, [f"Missing required columns: {', '.join(missing_cols)}"]

    validated_rows = []
    for idx, row in df.iterrows():
        row_dict = {col: row[col] for col in NUMERIC_FEATURES}
        is_valid, sample, err = validate_sample_dict(row_dict)
        if not is_valid:
            errors.append(f"Row {idx + 1}: {err}")
        else:
            validated_rows.append(row_dict)

    if errors:
        return False, pd.DataFrame(validated_rows), errors

    clean_df = pd.DataFrame(validated_rows)[NUMERIC_FEATURES]
    return True, clean_df, []
