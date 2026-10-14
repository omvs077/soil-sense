"""Soil-Sense - Precision Machine Learning Soil Fertility Diagnostic Platform Dashboard."""

import sys
from pathlib import Path

# Ensure project root is on sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import os
import io
import pandas as pd
import streamlit as st

from src.config import (
    FEATURE_BOUNDS,
    SOIL_PRESETS,
    NUMERIC_FEATURES,
    METRICS_PATH,
    FIGURES_DIR,
)
from src.validator import SoilSampleInput, validate_batch_dataframe
from src.predict import SoilPredictor, SecurityError
from app.ui_components import (
    render_header,
    render_fertility_badge,
    render_probability_bars,
    render_parameter_matrix,
    render_agronomic_advisory,
    render_disclaimer,
)


def load_css():
    """Inject bespoke CSS on every rerun so styling and wide layout never drop on refresh."""
    css_file = PROJECT_ROOT / "app" / "style.css"
    if css_file.exists():
        with open(css_file, "r", encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


@st.cache_resource
def get_predictor():
    """Cache verified model predictor instance."""
    try:
        return SoilPredictor()
    except Exception as e:
        return e


def main():
    # Guarantee wide layout and CSS injection on every single rerun / browser refresh
    try:
        st.set_page_config(
            page_title="Soil-Sense | Precision Soil Fertility ML",
            page_icon="🌱",
            layout="wide",
            initial_sidebar_state="collapsed",
        )
    except Exception:
        pass

    load_css()
    render_header()

    predictor = get_predictor()
    if isinstance(predictor, Exception):
        st.error(
            f"⚠️ **Model Initialization Alert**: {str(predictor)}\n\n"
            "Please ensure the ML pipeline is trained by running `python -m src.train`."
        )
        return

    # Tabs
    tab_single, tab_batch, tab_benchmarks = st.tabs(
        [
            "🔬 Field Sample Diagnostics",
            "📁 Batch CSV Screening",
            "📊 Model Evaluation & Benchmarks",
        ]
    )

    # =========================================================================
    # TAB 1: SINGLE SAMPLE DIAGNOSTICS
    # =========================================================================
    with tab_single:
        # Initialize session state with default preset
        if "sample_data" not in st.session_state:
            st.session_state.sample_data = {
                k: v["default"] for k, v in FEATURE_BOUNDS.items()
            }

        # Preset Quick-Load Selector
        st.markdown(
            '<div class="preset-title">⚡ Quick-Load Regional Soil Archetypes:</div>',
            unsafe_allow_html=True,
        )

        preset_short_names = {
            "Rich Alluvial Loam (High Fertility)": "🌾 Alluvial",
            "Standard Black Cotton Soil (Medium Fertility)": "🌋 Black Cotton",
            "Degraded / Acidic Sandy Soil (Low Fertility)": "🏜️ Acidic Sand",
            "Saline / Sodic Alkaline Soil (Low Fertility)": "🧂 Saline Sodic",
        }

        preset_cols = st.columns(len(SOIL_PRESETS))
        for idx, (p_full_name, p_vals) in enumerate(SOIL_PRESETS.items()):
            label = preset_short_names.get(p_full_name, p_full_name)
            with preset_cols[idx]:
                if st.button(label, key=f"btn_p_{idx}", use_container_width=True):
                    st.session_state.sample_data = p_vals.copy()
                    st.rerun()

        st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)

        col_input, col_result = st.columns([1.05, 1.25], gap="medium")

        # ---------------- INPUT CONTROLS COLUMN ----------------
        with col_input:
            # Card 1: Primary Macronutrients
            with st.container(border=True):
                st.markdown(
                    '<div class="card-header-bar"><span>🧪</span> Primary Macronutrient Profile</div>',
                    unsafe_allow_html=True,
                )

                n_val = st.slider(
                    "Nitrogen (N) — Available [mg/kg]",
                    min_value=FEATURE_BOUNDS["N"]["min"],
                    max_value=FEATURE_BOUNDS["N"]["max"],
                    value=float(st.session_state.sample_data["N"]),
                    step=FEATURE_BOUNDS["N"]["step"],
                    help="Optimal ICAR band: 140 - 280 mg/kg",
                )
                st.session_state.sample_data["N"] = n_val

                p_val = st.slider(
                    "Phosphorus (P) — Available [mg/kg]",
                    min_value=FEATURE_BOUNDS["P"]["min"],
                    max_value=FEATURE_BOUNDS["P"]["max"],
                    value=float(st.session_state.sample_data["P"]),
                    step=FEATURE_BOUNDS["P"]["step"],
                    help="Optimal ICAR band: 15 - 30 mg/kg",
                )
                st.session_state.sample_data["P"] = p_val

                k_val = st.slider(
                    "Potassium (K) — Available [mg/kg]",
                    min_value=FEATURE_BOUNDS["K"]["min"],
                    max_value=FEATURE_BOUNDS["K"]["max"],
                    value=float(st.session_state.sample_data["K"]),
                    step=FEATURE_BOUNDS["K"]["step"],
                    help="Optimal ICAR band: 130 - 280 mg/kg",
                )
                st.session_state.sample_data["K"] = k_val

            # Card 2: Soil Physico-chemical & Microclimate
            with st.container(border=True):
                st.markdown(
                    '<div class="card-header-bar"><span>🌡️</span> Physicochemical & Microclimate Metrics</div>',
                    unsafe_allow_html=True,
                )

                c1, c2 = st.columns(2)
                with c1:
                    ph_val = st.number_input(
                        "Soil pH (0 - 14)",
                        min_value=FEATURE_BOUNDS["pH"]["min"],
                        max_value=FEATURE_BOUNDS["pH"]["max"],
                        value=float(st.session_state.sample_data["pH"]),
                        step=FEATURE_BOUNDS["pH"]["step"],
                        help="Ideal neutral range: 6.2 - 7.5",
                    )
                    st.session_state.sample_data["pH"] = ph_val

                    ec_val = st.number_input(
                        "Electrical Cond. (EC) [dS/m]",
                        min_value=FEATURE_BOUNDS["EC"]["min"],
                        max_value=FEATURE_BOUNDS["EC"]["max"],
                        value=float(st.session_state.sample_data["EC"]),
                        step=FEATURE_BOUNDS["EC"]["step"],
                        help="Non-saline threshold: < 1.0 dS/m",
                    )
                    st.session_state.sample_data["EC"] = ec_val

                    moisture_val = st.slider(
                        "Moisture Content [%]",
                        min_value=FEATURE_BOUNDS["Moisture"]["min"],
                        max_value=FEATURE_BOUNDS["Moisture"]["max"],
                        value=float(st.session_state.sample_data["Moisture"]),
                        step=FEATURE_BOUNDS["Moisture"]["step"],
                        help="Optimal available water: 25 - 60%",
                    )
                    st.session_state.sample_data["Moisture"] = moisture_val

                with c2:
                    temp_val = st.slider(
                        "Ambient Temperature [°C]",
                        min_value=FEATURE_BOUNDS["Temperature"]["min"],
                        max_value=FEATURE_BOUNDS["Temperature"]["max"],
                        value=float(st.session_state.sample_data["Temperature"]),
                        step=FEATURE_BOUNDS["Temperature"]["step"],
                    )
                    st.session_state.sample_data["Temperature"] = temp_val

                    humidity_val = st.slider(
                        "Relative Humidity [%]",
                        min_value=FEATURE_BOUNDS["Humidity"]["min"],
                        max_value=FEATURE_BOUNDS["Humidity"]["max"],
                        value=float(st.session_state.sample_data["Humidity"]),
                        step=FEATURE_BOUNDS["Humidity"]["step"],
                    )
                    st.session_state.sample_data["Humidity"] = humidity_val

        # ---------------- RESULTS COLUMN ----------------
        with col_result:
            try:
                sample_obj = SoilSampleInput(**st.session_state.sample_data)
                pred_result = predictor.predict_single(sample_obj)

                # 1. High Impact Result Banner
                render_fertility_badge(
                    pred_result["fertility_class"], pred_result["confidence"]
                )

                # 2. Probability Distribution Card
                with st.container(border=True):
                    render_probability_bars(pred_result["probabilities"])

                # 3. Responsive Parameter Matrix Grid
                with st.container(border=True):
                    render_parameter_matrix(pred_result["input_values"])

                # 4. Actionable Agronomic Guidance
                with st.container(border=True):
                    render_agronomic_advisory(pred_result["diagnostics"])

            except Exception as e:
                st.error(f"Validation Error: {str(e)}")

    # =========================================================================
    # TAB 2: BATCH CSV SCREENING
    # =========================================================================
    with tab_batch:
        with st.container(border=True):
            st.markdown(
                '<div class="card-header-bar"><span>📁</span> Multi-Sample Batch Field Screening</div>'
                "<p style='color: #94a3b8; font-size: 0.88rem; margin: 0;'>"
                "Upload a tabular CSV file containing field test samples. The system performs schema validation, "
                "verifies agronomic boundaries, and evaluates each sample through the verified ML pipeline."
                "</p>",
                unsafe_allow_html=True,
            )

        col_b1, col_b2 = st.columns([1.5, 1])
        with col_b1:
            uploaded_file = st.file_uploader(
                "Upload Soil Samples CSV", type=["csv"], label_visibility="collapsed"
            )
        with col_b2:
            sample_template_df = pd.DataFrame([SOIL_PRESETS[k] for k in SOIL_PRESETS])
            csv_buffer = io.StringIO()
            sample_template_df.to_csv(csv_buffer, index=False)
            st.download_button(
                label="📥 Download Reference Sample CSV Template",
                data=csv_buffer.getvalue(),
                file_name="soil_samples_template.csv",
                mime="text/csv",
                use_container_width=True,
            )

        if uploaded_file is not None:
            try:
                raw_df = pd.read_csv(uploaded_file)
                st.info(f"Loaded {len(raw_df)} rows from uploaded file.")

                is_valid, clean_df, errors = validate_batch_dataframe(raw_df)

                if not is_valid:
                    st.error("Validation failed with the following issues:")
                    for err in errors[:5]:
                        st.write(f"- {err}")
                    if len(errors) > 5:
                        st.caption(f"... and {len(errors) - 5} more errors.")
                else:
                    batch_results = predictor.predict_batch(clean_df)

                    st.markdown("### Batch Classification Breakdown")
                    c_h, c_m, c_l = st.columns(3)
                    counts = batch_results["Predicted_Fertility"].value_counts()
                    total = len(batch_results)

                    with c_h:
                        st.metric(
                            "High Fertility Samples",
                            f"{counts.get('High', 0)} ({counts.get('High', 0)/total*100:.1f}%)",
                        )
                    with c_m:
                        st.metric(
                            "Medium Fertility Samples",
                            f"{counts.get('Medium', 0)} ({counts.get('Medium', 0)/total*100:.1f}%)",
                        )
                    with c_l:
                        st.metric(
                            "Low Fertility Samples",
                            f"{counts.get('Low', 0)} ({counts.get('Low', 0)/total*100:.1f}%)",
                        )

                    st.dataframe(batch_results, use_container_width=True)

                    export_buffer = io.StringIO()
                    batch_results.to_csv(export_buffer, index=False)
                    st.download_button(
                        label="💾 Export Diagnostic Predictions (CSV)",
                        data=export_buffer.getvalue(),
                        file_name="soil_fertility_predictions.csv",
                        mime="text/csv",
                    )

            except Exception as e:
                st.error(f"Error processing CSV: {str(e)}")

    # =========================================================================
    # TAB 3: MODEL EVALUATION & BENCHMARKS
    # =========================================================================
    with tab_benchmarks:
        with st.container(border=True):
            st.markdown(
                '<div class="card-header-bar"><span>📈</span> Model Benchmarks & Scientific Rigor</div>'
                "<p style='color: #94a3b8; font-size: 0.88rem; margin: 0;'>"
                "Three supervised classifiers (Decision Tree, K-Nearest Neighbors, Random Forest) were tested "
                "using Stratified 5-Fold Cross-Validation. The champion pipeline was evaluated on an untouched test set."
                "</p>",
                unsafe_allow_html=True,
            )

        col_m1, col_m2 = st.columns(2)
        with col_m1:
            cm_img = FIGURES_DIR / "confusion_matrix.png"
            if cm_img.exists():
                st.image(str(cm_img), caption="Champion Pipeline Confusion Matrix", use_container_width=True)
            else:
                st.info("Confusion matrix figure not yet generated. Run `python -m src.evaluate`.")

        with col_m2:
            fi_img = FIGURES_DIR / "feature_importance.png"
            if fi_img.exists():
                st.image(str(fi_img), caption="Feature Importance Ranking (Gini Impurity)", use_container_width=True)
            else:
                st.info("Feature importance figure not yet generated. Run `python -m src.evaluate`.")

        st.markdown("### ICAR & FAO Soil Quality Reference Standards")
        standards_data = [
            {"Parameter": "Nitrogen (N)", "Unit": "mg/kg", "Low Range": "< 140", "Optimal Range": "140 - 280", "High Range": "> 280"},
            {"Parameter": "Phosphorus (P)", "Unit": "mg/kg", "Low Range": "< 10", "Optimal Range": "15 - 30", "High Range": "> 30"},
            {"Parameter": "Potassium (K)", "Unit": "mg/kg", "Low Range": "< 110", "Optimal Range": "130 - 280", "High Range": "> 280"},
            {"Parameter": "pH Reaction", "Unit": "pH", "Low Range": "< 6.0 (Acidic)", "Optimal Range": "6.2 - 7.5 (Neutral)", "High Range": "> 8.0 (Alkaline)"},
            {"Parameter": "Electrical Cond. (EC)", "Unit": "dS/m", "Low Range": "—", "Optimal Range": "< 1.0 (Non-saline)", "High Range": "> 2.0 (Saline)"},
            {"Parameter": "Moisture", "Unit": "%", "Low Range": "< 20 (Wilting)", "Optimal Range": "25 - 60 (Available)", "High Range": "> 75 (Waterlogged)"},
        ]
        st.table(pd.DataFrame(standards_data))

    render_disclaimer()


if __name__ == "__main__":
    main()
