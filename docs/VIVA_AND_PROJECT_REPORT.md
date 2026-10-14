# Soil-Sense Academic Project Report & Viva Defense Guide

## 1. Project Overview & Problem Statement
Soil fertility evaluation is conventionally performed via chemical laboratory testing, requiring specialized personnel to interpret multiple interrelated biochemical markers. Soil-Sense provides an automated, explainable Machine Learning classification pipeline that maps primary nutrients (N, P, K), soil chemistry (pH, EC, moisture), and environmental factors into actionable fertility classes (**Low**, **Medium**, **High**) with probabilistic confidence and agronomic guidance.

---

## 2. Key Viva Voce Questions & Answers

### Q1: Why use Random Forest over a Single Decision Tree?
**Answer**: A single Decision Tree creates orthogonal axis-aligned splits and is prone to high variance (overfitting the training data). Random Forest is an ensemble bagging technique that constructs multiple uncorrelated decision trees through bootstrap aggregation and random feature subspacing. This reduces variance substantially while maintaining strong non-linear feature interaction modeling without requiring heavy computation.

### Q2: Why is Scikit-learn Pipeline critical here?
**Answer**: Preprocessing operations such as `StandardScaler` compute statistics ($\mu$ and $\sigma$) across feature columns. If fitted on the entire dataset prior to splitting, information from the test set leaks into the training pipeline (Data Leakage). Wrapping transformers and the estimator into an unified `Pipeline` guarantees that parameters are fitted solely on `X_train` during training folds.

### Q3: What metrics did you use, and why not just Accuracy?
**Answer**: In soil classification datasets, classes can be imbalanced (e.g. fewer "Low" or "High" fertility samples than "Medium"). High overall accuracy can mask a total failure to predict minority classes. We report **Macro-averaged F1-Score**, **Precision**, **Recall**, and inspect the full **Confusion Matrix** to ensure balanced diagnostic sensitivity across all three fertility tiers.

### Q4: How does your system protect against deserialization attacks (CWE-502)?
**Answer**: Python's `pickle` and `joblib` formats serialize bytecode and can execute arbitrary malicious code upon deserialization. Soil-Sense computes a cryptographic SHA-256 digest at training time and validates the model file against this hash prior to unpickling during inference.

### Q5: How did you ensure the project didn't exhaust C: drive storage?
**Answer**:
1. Virtual environment `.venv` created strictly on `D:`.
2. Global `pip` cache redirected to `D:\pip-cache` via `pip config`.
3. Temporary compilation directories pointed to `D:\temp`.
4. Avoided bloated deep-learning frameworks (TensorFlow, PyTorch) since tabular classification is ideally solved by tree-based ensemble methods.

---

## 3. Limitations & Future Scope
- **Current Limitations**: The model assumes regional representative soil characteristics and does not account for specific secondary micronutrients (Zinc, Boron, Iron) or biological microbiome assays.
- **Future Scope**:
  - Direct integration with low-cost field IoT sensors (LoRaWAN/ESP32 NPK sensors).
  - Geographic Information System (GIS) mapping with satellite-derived NDVI and multispectral soil reflection data.
  - Multi-crop suitability recommender based on crop-specific nutrient demand curves.
