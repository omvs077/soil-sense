# Soil-Sense 🌱

> Precision Machine Learning System for Soil Fertility Classification (Low / Medium / High) based on chemical, physical, and environmental parameters.

---

## Quickstart

### 1. Prerequisites
- Python 3.10+
- Recommended drive: `D:` (to avoid `C:` drive storage exhaustion)

### 2. Environment Setup
```bash
# Clone the repository
git clone https://github.com/omvs077/soil-sense.git
cd soil-sense

# Create isolated virtual environment on D:
python -m venv .venv
.venv\Scripts\activate

# Install dependencies (redirect pip cache to D: to protect C:)
pip config set global.cache-dir D:\pip-cache
pip install -r requirements.txt
```

### 3. Train & Evaluate Models
```bash
python -m src.train
python -m src.evaluate
```

### 4. Launch Application
```bash
streamlit run app/app.py
```

---

## Project Structure
- `app/` — Modern Agritech Streamlit dashboard with Bento-grid layout, SVG gauges, and batch sample analysis.
- `src/` — Scikit-learn pipelines, model training, evaluation, validation schemas, and cryptographic model integrity verification.
- `data/` — Raw and processed soil measurement datasets.
- `models/` — Trained Scikit-learn pipelines with SHA-256 integrity checksums.
- `docs/` — Technical documentation, architecture blueprints, viva guide, and agronomic thresholds.

For detailed architecture, agronomic science, and security specifications, see [`docs/`](docs/).
