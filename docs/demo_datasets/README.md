# Soil-Sense Demo Datasets for Batch CSV Screening

These pre-packaged CSV datasets are ready for drag-and-drop upload in the **📁 Batch CSV Screening** tab of the Soil-Sense web dashboard.

---

## Available Demo Datasets

| File Name | Sample Count | Agronomic Archetype | Expected Classification Outcome |
| :--- | :--- | :--- | :--- |
| **[`demo_mixed_farm_survey.csv`](./demo_mixed_farm_survey.csv)** | 25 | Heterogeneous multi-plot field survey covering varied zones | **Mixed**: 10 High, 8 Medium, 7 Low |
| **[`demo_high_fertility_alluvial.csv`](./demo_high_fertility_alluvial.csv)** | 15 | Riverine alluvial loam with balanced NPK, neutral pH ($6.6 - 7.4$), and low EC | **100% High Fertility** (🟢) |
| **[`demo_degraded_saline_alkaline.csv`](./demo_degraded_saline_alkaline.csv)** | 15 | Salt-affected arid soil with severe macronutrient depletion and high EC ($> 2.5\text{ dS/m}$) | **100% Low Fertility** (🔴) |
| **[`demo_acidic_laterite_hill.csv`](./demo_acidic_laterite_hill.csv)** | 15 | High-rainfall hilly terrain with acidic pH ($4.2 - 5.2$) and strong phosphorus lockup | **Medium / Stressed Fertility** (🟡) |

---

## How to Test in the Web Dashboard
1. Open the web interface at **`http://localhost:8501`**.
2. Click on the **📁 Batch CSV Screening** tab.
3. Drag and drop any of the `.csv` files from this folder into the upload box (or click **Browse files** and navigate to `D:\My projects\Soil-sense\docs\demo_datasets`).
4. The system will automatically:
   - Validate input schemas and boundaries.
   - Run batch model predictions with probability confidence scores.
   - Display class breakdown metrics (High %, Medium %, Low %).
   - Provide a downloadable diagnostic report with one click.
