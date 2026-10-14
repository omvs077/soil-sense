# Soil-Sense Technical Architecture & Security Specification

## 1. System Overview
Soil-Sense is an end-to-end Machine Learning classification platform that maps 8 soil physicochemical and environmental features into three fertility tiers (**Low**, **Medium**, **High**):
- **Primary Nutrients**: Nitrogen ($N$, mg/kg), Phosphorus ($P$, mg/kg), Potassium ($K$, mg/kg)
- **Soil Chemistry**: pH, Electrical Conductivity ($EC$, dS/m), Moisture (%)
- **Microclimate**: Temperature (°C), Relative Humidity (%)

---

## 2. Storage & Zero-Bloat Sandbox Architecture

The system enforces strict disk containment on the secondary drive (`D:`):
- **Virtual Environment**: `.venv` placed directly inside the workspace directory.
- **Pip Cache**: Persistent wheel cache redirected to `D:\pip-cache`.
- **Temp Build Sandbox**: `$env:TEMP` / `$env:TMP` redirected to `D:\temp` during compilation to prevent exhaustion of system `C:` space.
- **Dependency Footprint**: Constrained to Scikit-learn, Pandas, NumPy, Pydantic, and Streamlit (< 400 MB total vs. > 3.5 GB for Deep Learning alternatives).

---

## 3. Security Hardening & Vulnerability Remediation

### 3.1 Model Deserialization Protection (CWE-502)
- **Vulnerability**: Standard `pickle` and `joblib` loading can execute arbitrary malicious bytecode.
- **Remediation**:
  - During model serialization, a cryptographic **SHA-256 digest** is computed and written to `models/model_checksum.json`.
  - The prediction runtime reads the candidate model file, computes its SHA-256 hash, and compares it against the signed manifest before deserializing.
  - Model loading is constrained strictly to the internal `models/` directory.

### 3.2 Preprocessing Data Leakage Prevention
- **Vulnerability**: Fitting feature transformers (e.g. `StandardScaler`) across the entire dataset prior to splitting leaks test distribution information.
- **Remediation**:
  - All preprocessing transformations are wrapped inside a Scikit-learn `Pipeline` alongside the estimator.
  - Transformers are fitted strictly on `X_train` during `fit()` and applied via `transform()` on `X_test` and production inference.

### 3.3 Input Validation & Boundary Enforcement
- Input values are parsed and validated through a Pydantic schema (`SoilSampleSchema`) before reaching the model:
  - $0 \le \text{pH} \le 14$
  - $0 \le \text{Moisture} \le 100\%$
  - $0 \le \text{Humidity} \le 100\%$
  - $\text{Nutrients } (N, P, K) \ge 0$
  - $\text{Temperature } -10^\circ\text{C} \le T \le 60^\circ\text{C}$
  - $0 \le \text{EC} \le 20 \text{ dS/m}$

---

## 4. Machine Learning Pipeline

```
Raw CSV / User Input
       │
       ▼
Input Validation (Pydantic / Agronomic Bounds)
       │
       ▼
Scikit-learn Pipeline
   ├── Median Imputer (handles unexpected nulls)
   ├── Robust / Standard Scaler (z-score normalization)
   └── Random Forest Classifier (n_estimators=100, class_weight='balanced')
       │
       ▼
Probability Distribution & Fertility Classification (Low / Medium / High)
       │
       ▼
Agronomic Diagnosis Engine (Deficiency flags & Soil health recommendations)
```
